"""Testbench deck writer + raw-file reader + analysis for sar10_adc."""
import math, os, struct, sys
import numpy as np

ENV = {
    'local': dict(lib='/home/claude/tools/pr/models/sky130.lib.spice',
                  vpp='/home/claude/tools/pr/cells/{c}/sky130_fd_pr__{c}.model.spice',
                  std=lambda cells: ['/home/claude/tools/schd/cells/%s/sky130_fd_sc_hd__%s.spice' % (c.split('_')[0], c) for c in cells]),
    'foss': dict(lib='/foss/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice',
                 vpp='/foss/pdks/sky130A/libs.ref/sky130_fd_pr/spice/sky130_fd_pr__{c}.model.spice',
                 std=lambda cells: ['/foss/pdks/sky130A/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice']),
}
SPICEINIT = 'set ngbehavior=hsa\nset ng_nomodcheck\nset skywaterpdk\noption noinit\n'


def deck(dut, env='local', corner='tt', temp=27, vdd=1.8, fs=20e6, duty=0.25, ncyc=8, vd=None, sine=None,
         amp=1.7, vcm=0.9, rs=50.0, probes=(), stdcells=(), unitcap=None,
         raw='out.raw', tmax=40e-12, extra='', nbit=10, vref=None, klu=True, acc='fast'):
    """vd: list of differential DC inputs (one per cycle)  |  sine: (N, M, n0) coherent sine, samples n0..n0+ncyc-1"""
    e = ENV[env]
    T = 1.0 / fs
    ts = duty * T
    t0 = 1e-9
    vref = vdd if vref is None else vref
    L = ['* sar10_adc testbench (generated)', '.lib %s %s' % (e['lib'], corner)]
    L += ['.include %s' % p for p in e['std'](stdcells)]
    if unitcap is None:
        import design; unitcap = design.P['UNITCAP']
    L.append('.include %s' % e['vpp'].format(c=unitcap))
    L.append('.include %s' % dut)
    L += ['.temp %g' % temp, 'Vvdd VDD 0 %g' % vdd, 'Vvss VSS 0 0', 'Vrefp VREFP 0 %g' % vref, 'Vrefn VREFN 0 0',
          'Vclk CLK 0 PULSE(0 %g %g 50p 50p %g %g)' % (vdd, t0, ts - 50e-12, T)]
    if sine:
        N, M, n0 = sine
        fin = M * fs / N
        # sampling instant of cycle k: t0 + ts + k*T ; make global sample n0+k see phase 2*pi*M*(n0+k)/N
        tsamp = t0 + ts + 50e-12
        ph = 360.0 * ((M * n0 / N - fin * tsamp) % 1.0)
        L.append('Vsp VIPS 0 SIN(%g %g %g 0 0 %g)' % (vcm, amp / 2, fin, ph))
        L.append('Vsn VINS 0 SIN(%g %g %g 0 0 %g)' % (vcm, -amp / 2, fin, ph))
    else:
        pp, pn = [], []
        for k, v in enumerate(vd):
            ta = t0 + ts + k * T + 1e-9  # change shortly after the sampling edge of cycle k -> seen by cycle k+1
            if k == 0:
                pp += [0, vcm + v / 2]; pn += [0, vcm - v / 2]
            else:
                tb = t0 + ts + (k - 1) * T + 1e-9
                pp += [tb + 0.2e-9, vcm + v / 2]; pn += [tb + 0.2e-9, vcm - v / 2]
            pp += [ta, vcm + v / 2]; pn += [ta, vcm - v / 2]
        L.append('Vsp VIPS 0 PWL(%s)' % ' '.join('%.6g' % x for x in pp))
        L.append('Vsn VINS 0 PWL(%s)' % ' '.join('%.6g' % x for x in pn))
    L += ['Rsp VIPS VIP %g' % rs, 'Rsn VINS VIN %g' % rs]
    L.append('x1 VIP VIN CLK %s EOC VDD VREFP VREFN VSS sar10_adc' % ' '.join('B%d' % i for i in range(nbit - 1, -1, -1)))
    L += ['C%d B%d 0 5f' % (i, i) for i in range(nbit)] + ['Ceoc EOC 0 5f']
    sv = ['v(vip)', 'v(vin)', 'v(clk)', 'v(eoc)'] + ['v(b%d)' % i for i in range(nbit)] + ['i(vvdd)', 'i(vrefp)', 'i(vsp)']
    sv += ['v(%s)' % p for p in probes]
    L.append('.save ' + ' '.join(sv))
    opt = {'hi': 'reltol=1e-4 abstol=1e-13 vntol=1e-7 chgtol=1e-16 method=gear rshunt=1e15',
           'mid': 'reltol=2e-4 abstol=1e-13 vntol=1e-7 chgtol=1e-16 method=gear rshunt=1e15',
           'fast': 'reltol=5e-4 abstol=1e-12 vntol=1e-6 method=gear rshunt=1e15'}[acc]
    L.append('.option ' + opt + (' klu' if klu else ''))
    if extra:
        L.append(extra)
    tstop = t0 + ncyc * T + 0.5e-9
    L.append('.tran 20p %g 0 %g uic' % (tstop, tmax))
    L += ['.control', 'set filetype=binary', 'run', 'write %s' % raw, '.endc', '.end']
    meta = dict(T=T, ts=ts, t0=t0, ncyc=ncyc, nbit=nbit, vdd=vdd, vref=vref, fs=fs)
    return '\n'.join(L) + '\n', meta


def read_raw(path):
    with open(path, 'rb') as f:
        data = f.read()
    i = data.index(b'Binary:\n')
    head = data[:i].decode('ascii', 'replace').split('\n')
    nv = npnt = 0
    names = []
    inv = False
    for ln in head:
        if ln.startswith('No. Variables:'):
            nv = int(ln.split(':')[1])
        elif ln.startswith('No. Points:'):
            npnt = int(ln.split(':')[1])
        elif ln.startswith('Variables:'):
            inv = True
        elif inv and ln.strip():
            p = ln.split()
            names.append(p[1].lower())
    a = np.frombuffer(data, dtype='<f8', count=nv * npnt, offset=i + 8).reshape(npnt, nv)
    return {n: a[:, k] for k, n in enumerate(names)}


def at(d, sig, t):
    return np.interp(t, d['time'], d[sig])


def codes(d, m):
    """returns per cycle: code, sampled differential input, conversion time, validity"""
    T, ts, t0, n, nb, vdd = m['T'], m['ts'], m['t0'], m['ncyc'], m['nbit'], m['vdd']
    t = d['time']
    out = []
    for k in range(n):
        tsmp = t0 + ts + k * T + 50e-12          # CLK falling edge (end of fall)
        tend = t0 + (k + 1) * T                # next CLK rising edge
        if tend > t[-1] + 1e-10:              # (the run may stop a few fs before the last edge)
            break
        tend = min(tend, t[-1])
        code = 0
        for b in range(nb):
            code |= (1 if at(d, 'v(b%d)' % b, tend) > vdd / 2 else 0) << b
        vs = at(d, 'v(vip)', tsmp) - at(d, 'v(vin)', tsmp)
        # EOC rising edge inside this cycle
        sel = (t >= tsmp) & (t <= tend)
        e = d['v(eoc)'][sel]
        tt = t[sel]
        idx = np.where((e[1:] > vdd / 2) & (e[:-1] <= vdd / 2))[0]
        tconv = (tt[idx[0]] - tsmp) if len(idx) else float('nan')
        out.append((code, vs, tconv))
    return out


def datavalid(d, m):
    """per cycle: time (from the sampling edge) at which the output bits B9..B0 hold this conversion's code:
    the later of the EOC edge and the last B transition in the cycle (EOC -> flop clock-to-Q).  nan if no EOC."""
    T, ts, t0, n, nb, vdd = m['T'], m['ts'], m['t0'], m['ncyc'], m['nbit'], m['vdd']
    t = d['time']; out = []
    for k in range(n):
        tsmp = t0 + ts + k * T + 50e-12; tend = t0 + (k + 1) * T
        if tend > t[-1] + 1e-10: break
        sel = (t >= tsmp) & (t <= min(tend, t[-1])); tt = t[sel]
        e = d['v(eoc)'][sel]; ie = np.where((e[1:] > vdd / 2) & (e[:-1] <= vdd / 2))[0]
        if not len(ie): out.append(float('nan')); continue
        last = tt[ie[0]]
        for b in range(nb):
            x = d['v(b%d)' % b][sel]; ix = np.where((x[1:] > vdd / 2) != (x[:-1] > vdd / 2))[0]
            if len(ix): last = max(last, tt[ix[-1]])
        out.append(last - tsmp)
    return out


def power(d, m, k0=1):
    """average supply power over whole cycles k0.. (W): vdd, vref"""
    T, t0, n = m['T'], m['t0'], m['ncyc']
    t = d['time']
    a, b = t0 + k0 * T, t0 + n * T
    sel = (t >= a) & (t <= b)
    f = lambda s: -np.trapezoid(d[s][sel], t[sel]) / (b - a)
    return f('i(vvdd)') * m['vdd'], f('i(vrefp)') * m['vref']


def fft_metrics(code, nbit=10):
    x = np.asarray(code, float)
    N = len(x)
    x = x - x.mean()
    X = np.abs(np.fft.rfft(x)) ** 2
    X[0] = 0
    ks = int(np.argmax(X))
    ps = X[ks]
    rest = X.copy(); rest[ks] = 0; rest[0] = 0
    pn = rest.sum()
    sndr = 10 * math.log10(ps / pn) if pn > 0 else float('inf')
    sfdr = 10 * math.log10(ps / rest.max()) if rest.max() > 0 else float('inf')
    amp = 2 * math.sqrt(ps) / N
    dbfs = 20 * math.log10(amp / (2 ** nbit / 2))
    # harmonics 2..5 (aliased)
    ph = 0
    for h in range(2, 6):
        kk = (h * ks) % N
        if kk > N // 2:
            kk = N - kk
        if kk not in (0, ks):
            ph += X[kk]
    thd = 10 * math.log10(ph / ps) if ph > 0 else float('-inf')
    return dict(N=N, bin=ks, sndr=sndr, enob=(sndr - 1.76) / 6.02, sfdr=sfdr, thd=thd, dbfs=dbfs,
                enob_fs=(sndr - dbfs - 1.76) / 6.02)
