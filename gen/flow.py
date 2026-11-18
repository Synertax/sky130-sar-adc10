#!/usr/bin/env python3
"""Simulation flow for sar10_adc.
  flow.py dc      --out DIR [--vd v1,v2,...]
  flow.py fft     --out DIR --N 256 --M 31 [--fs 20e6] [--corner tt] [--temp 27] [--par 12]
  flow.py corners --out DIR [--fs 20e6] [--N 24 --M 5]
Common: --env local|foss, --dut FILE (default: reference netlist from design.py), --duty, --vdd, --amp
"""
import argparse, math, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import design, netlist, tb

import threading
INI_LOCK = threading.Lock()
NG = {'local': '/home/claude/tools/ng/bin/ngspice', 'foss': 'ngspice'}


def prep_dut(a, d):
    cells = design.build()
    ref = os.path.join(d, 'dut_ref.spice')
    netlist.emit(cells, ref)
    return (a.dut or ref), netlist.std_used(cells)


def run_deck(a, d, name, **kw):
    os.makedirs(d, exist_ok=True)
    raw = os.path.join(d, name + '.raw')
    v = kw.get('vdd', 1.8)
    if 'vd' in kw:                       # DC points are given for a 1.8 V reference: scale with the supply
        kw['vd'] = [x * v / 1.8 for x in kw['vd']]
    s, m = tb.deck(a.dutfile, env=a.env, stdcells=a.std, raw=raw, duty=a.duty, fs=a.fs, amp=a.amp * v / 1.8, vcm=v / 2,
                   acc=a.acc, **kw)
    open(os.path.join(d, name + '.spice'), 'w').write(s)
    with INI_LOCK:                        # one writer at a time: parallel chunks share the directory
        ini = os.path.join(d, '.spiceinit')
        if not os.path.exists(ini):
            open(ini, 'w').write(tb.SPICEINIT + 'set num_threads=1\n')
    t = time.time()
    r = subprocess.run([NG[a.env], '-b', name + '.spice'], cwd=d, capture_output=True, text=True)
    open(os.path.join(d, name + '.log'), 'w').write(r.stdout + r.stderr)
    if not os.path.exists(raw):
        raise RuntimeError('ngspice failed for %s: %s' % (name, (r.stdout + r.stderr)[-800:]))
    data = tb.read_raw(raw)
    if not a.keep:
        os.remove(raw)
    return data, m, time.time() - t


LAST_TVALID = {}      # filled by sine_run: {chunk start: [data-valid time per sample]}


def sine_run(a, d, N, M, par, tagp='c', **kw):
    """coherent sine split into `par` parallel chunks; returns codes[N], vs[N], tconv[N], (pvdd, pref)"""
    par = min(par, N)
    bounds = [round(i * N / par) for i in range(par + 1)]
    jobs = [(bounds[i], bounds[i + 1] - bounds[i]) for i in range(par)]

    def one(j):
        n0, ln = j
        data, m, dt = run_deck(a, d, '%s%03d' % (tagp, n0), sine=(N, M, n0 - 1), ncyc=ln + 1, **kw)
        cs = tb.codes(data, m)[1:]
        LAST_TVALID[n0] = tb.datavalid(data, m)[1:]
        return n0, cs, tb.power(data, m, 1), dt

    with ThreadPoolExecutor(par) as ex:
        res = list(ex.map(one, jobs))
    res.sort()
    cs = [c for r in res for c in r[1]]
    pv = sum(r[2][0] * len(r[1]) for r in res) / len(cs)
    pr = sum(r[2][1] * len(r[1]) for r in res) / len(cs)
    return (np.array([c[0] for c in cs]), np.array([c[1] for c in cs]), np.array([c[2] for c in cs]), (pv, pr),
            max(r[3] for r in res))


def linfit_resid(code, vs):
    A = np.vstack([vs, np.ones(len(vs))]).T
    g, o = np.linalg.lstsq(A, code + 0.5, rcond=None)[0]
    return g, o, (code + 0.5) - (g * vs + o)


def cmd_dc(a):
    vd = [float(x) for x in a.vd.split(',')]
    data, m, dt = run_deck(a, a.out, 'dc', vd=vd, ncyc=len(vd), corner=a.corner, temp=a.temp, vdd=a.vdd)
    lsb = 2 * a.vdd / 1024
    L = ['dc test corner=%s temp=%g vdd=%g fs=%g  (sim %.0f s)' % (a.corner, a.temp, a.vdd, a.fs, dt)]
    for (c, vs, tc) in tb.codes(data, m):
        L.append('vd=%9.5f code=%4d ideal=%8.2f tconv=%.2f ns' % (vs, c, vs / lsb + 512, tc * 1e9))
    L.append('P_vdd %.1f uW  P_ref %.1f uW' % tuple(x * 1e6 for x in tb.power(data, m)))
    out = '\n'.join(L)
    print(out)
    open(os.path.join(a.out, 'result.txt'), 'w').write(out + '\n')


def cmd_fft(a):
    t = time.time()
    code, vs, tc, (pv, pr), dt = sine_run(a, a.out, a.N, a.M, a.par, corner=a.corner, temp=a.temp, vdd=a.vdd)
    f = tb.fft_metrics(code)
    g, o, res = linfit_resid(code, vs)
    ptot = pv + pr
    fom = ptot / (2 ** f['enob'] * a.fs)
    L = ['FFT  N=%d M=%d fs=%.3g Hz fin=%.4g Hz corner=%s temp=%g vdd=%g amp=%.2f Vpk-diff  (wall %.0f s)' % (
        a.N, a.M, a.fs, a.M * a.fs / a.N, a.corner, a.temp, a.vdd, a.amp, time.time() - t),
        'code range %d..%d  signal %.2f dBFS' % (code.min(), code.max(), f['dbfs']),
        'SNDR %.2f dB  ENOB %.3f bit  SFDR %.2f dB  THD %.2f dB' % (f['sndr'], f['enob'], f['sfdr'], f['thd']),
        'conversion time max %.2f ns  mean %.2f ns  (available %.2f ns)' % (np.nanmax(tc) * 1e9, np.nanmean(tc) * 1e9, (1 - a.duty) / a.fs * 1e9),
        'power: VDD %.1f uW + VREF %.1f uW = %.1f uW   energy/conv %.2f pJ   FoM_W %.2f fJ/conv-step' % (
            pv * 1e6, pr * 1e6, ptot * 1e6, ptot / a.fs * 1e12, fom * 1e15),
        'missing EOC: %d' % int(np.isnan(tc).sum()),
        'output data valid max %.2f ns  (EOC + flop clock-to-Q; must be < available)' % (np.nanmax([x for k_ in sorted(LAST_TVALID) for x in LAST_TVALID[k_]]) * 1e9)]
    out = '\n'.join(L)
    print(out)
    open(os.path.join(a.out, 'result.txt'), 'w').write(out + '\n')
    np.savetxt(os.path.join(a.out, 'codes.txt'), np.c_[code, vs, tc], fmt='%d %.7f %.4e')
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        x = code - code.mean()
        X = np.abs(np.fft.rfft(x)) / (len(x) / 2) / 512
        X[0] = 1e-12
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(np.arange(len(X)) * a.fs / a.N / 1e6, 20 * np.log10(np.maximum(X, 1e-7)), lw=0.9)
        ax.set_xlabel('frequency (MHz)'); ax.set_ylabel('dBFS'); ax.set_ylim(-120, 5); ax.grid(alpha=0.3)
        ax.set_title('sar10_adc  %s %g C  fs=%.3g MS/s  SNDR %.1f dB  ENOB %.2f  SFDR %.1f dB' % (a.corner, a.temp, a.fs / 1e6, f['sndr'], f['enob'], f['sfdr']))
        fig.tight_layout(); fig.savefig(os.path.join(a.out, 'spectrum.png'), dpi=110)
    except Exception as e:
        print('plot skipped:', e)


def points_run(a, d, vds, par, probes=('x1.topp', 'x1.topn'), **kw):
    """DC input list split into parallel chunks; returns code, sampled vd, final top-plate residue, tconv"""
    par = min(par, len(vds))
    bounds = [round(i * len(vds) / par) for i in range(par + 1)]

    def one(i):
        lo, hi = bounds[i], bounds[i + 1]
        vv = [vds[lo]] + list(vds[lo:hi])
        data, m, dt = run_deck(a, d, 'p%03d' % lo, vd=vv, ncyc=len(vv), probes=list(probes), **kw)
        cs = tb.codes(data, m)[1:]
        res = []
        for k in range(1, len(vv)):
            te = m['t0'] + (k + 1) * m['T'] - 0.2e-9
            res.append(tb.at(data, 'v(x1.topp)', te) - tb.at(data, 'v(x1.topn)', te))
        return lo, cs, res

    with ThreadPoolExecutor(par) as ex:
        out = sorted(ex.map(one, range(par)))
    cs = [c for r in out for c in r[1]]
    rs = [x for r in out for x in r[2]]
    return np.array([c[0] for c in cs]), np.array([c[1] for c in cs]), np.array(rs), np.array([c[2] for c in cs])


def cmd_lin(a):
    """static linearity without quantisation noise: input = k1*code + k2*residue + k0 ; report the fit residual"""
    t = time.time()
    n = a.N
    vds = list(np.linspace(-a.amp, a.amp, n))
    code, vs, res, tc = points_run(a, a.out, vds, a.par, corner=a.corner, temp=a.temp, vdd=a.vdd)
    lsb = 2 * a.vdd / 1024
    k, err = lin_fit(code, vs, res, lsb)
    # odd / 3rd order content
    x = vs / a.amp
    c3 = np.linalg.lstsq(np.vstack([x ** 3 - 0.6 * x, x ** 2 - 1 / 3.0, np.ones(n)]).T, err, rcond=None)[0]
    L = ['static linearity, %d DC points +-%.2f V, corner=%s temp=%g vdd=%g (wall %.0f s)' % (n, a.amp, a.corner, a.temp, a.vdd, time.time() - t),
         'fit: input[LSB] = %.5f*(code without LSB) + %.4f*residue[LSB] + %.2f' % (k[0], k[1], k[2]),
         'nonlinearity (INL-like, quantisation removed): max %.3f LSB  rms %.3f LSB   3rd-order term %.3f LSB  2nd-order %.3f LSB' % (
             np.abs(err).max(), err.std(), c3[0], c3[1]),
         'vd[V]   code  residue[LSB]  error[LSB]'] + ['%7.4f %5d %8.3f %8.3f' % (vs[i], code[i], res[i] / lsb, err[i]) for i in range(n)]
    out = '\n'.join(L)
    print(out)
    open(os.path.join(a.out, 'result.txt'), 'w').write(out + '\n')


def lin_fit(code, vs, res, lsb):
    A = np.vstack([(code >> 1) * 2, res / lsb, np.ones(len(vs))]).T   # the last decision does not move the DAC
    k = np.linalg.lstsq(A, vs / lsb, rcond=None)[0]
    return k, vs / lsb - A @ k


def cmd_corners(a):
    """per PVT point: N DC inputs -> static nonlinearity (quantisation removed), conversion time, power"""
    combos = [(c, t, a.vdd) for c in ('tt', 'ss', 'ff', 'sf', 'fs') for t in (-40, 27, 125)]
    combos += [('tt', 27, round(a.vdd * 0.9, 3)), ('tt', 27, round(a.vdd * 1.1, 3)), ('ss', 125, round(a.vdd * 0.9, 3)), ('ff', -40, round(a.vdd * 1.1, 3))]
    vds = list(np.linspace(-a.amp, a.amp, a.N))

    def one(cb):
        c, t, v = cb
        d = os.path.join(a.out, '%s_%g_%g' % (c, t, v))
        try:
            vv = [vds[0]] + vds
            data, m, dt = run_deck(a, d, 'pts', vd=list(vv), ncyc=len(vv), probes=['x1.topp', 'x1.topn'], corner=c, temp=t, vdd=v)
            cs = tb.codes(data, m)[1:]
            code = np.array([x[0] for x in cs]); vs = np.array([x[1] for x in cs]); tc = np.array([x[2] for x in cs])
            res = np.array([tb.at(data, 'v(x1.topp)', m['t0'] + (k + 1) * m['T'] - 0.2e-9) - tb.at(data, 'v(x1.topn)', m['t0'] + (k + 1) * m['T'] - 0.2e-9)
                            for k in range(1, len(vv))])
            lsb = 2 * v / 1024
            k, err = lin_fit(code, vs, res, lsb)
            pv, pr = tb.power(data, m, 1)
            return '%-3s %5g %5.2f | %7.4f %7.2f | %6.3f %6.3f | %6.2f %6.2f | %6.1f %5.1f | %d' % (
                c, t, v, 1 / k[0], k[2] + 512, np.abs(err).max(), err.std(), np.nanmax(tc) * 1e9, np.nanmean(tc) * 1e9,
                pv * 1e6, pr * 1e6, int(np.isnan(tc).sum()))
        except Exception as e:
            return '%-3s %5g %5.2f | FAILED %s' % (c, t, v, str(e)[:200])

    with ThreadPoolExecutor(a.par) as ex:
        rows = list(ex.map(one, combos))
    L = ['PVT sweep: %d DC inputs over +-%.2f*VDD/1.8 V, fs=%.3g, duty=%.2f; available conversion time %.2f ns' % (
        a.N, a.amp, a.fs, a.duty, (1 - a.duty) / a.fs * 1e9),
        'static nonlinearity = error of input vs (code, final residue) fit: quantisation removed, like INL',
        'cor  temp   vdd |    gain  offset | INL max  rms(LSB) | tconv max mean(ns) | Pvdd  Pref(uW) | missing EOC'] + rows
    out = '\n'.join(L)
    print(out)
    open(os.path.join(a.out, 'result.txt'), 'w').write(out + '\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('cmd')
    p.add_argument('--out', required=True)
    p.add_argument('--env', default='foss')
    p.add_argument('--dut', default=None)
    p.add_argument('--fs', type=float, default=20e6)
    p.add_argument('--duty', type=float, default=0.25)
    p.add_argument('--vdd', type=float, default=1.8)
    p.add_argument('--amp', type=float, default=1.7)
    p.add_argument('--corner', default='tt')
    p.add_argument('--temp', type=float, default=27)
    p.add_argument('--N', type=int, default=64)
    p.add_argument('--M', type=int, default=13)
    p.add_argument('--par', type=int, default=12)
    p.add_argument('--vd', default='1.7,1.0,0.3,0.01,-0.01,-0.3,-1.0,-1.7')
    p.add_argument('--keep', action='store_true')
    p.add_argument('--acc', default='fast')
    p.add_argument('--set', default='', help='override design params, e.g. NDLY=3,W_IN=6')
    a = p.parse_args()
    for kv in a.set.split(','):
        if kv:
            k, v = kv.split('=')
            design.P[k] = type(design.P[k])(v)
    os.makedirs(a.out, exist_ok=True)
    a.out = os.path.abspath(a.out)
    if a.dut:
        a.dut = os.path.abspath(a.dut)
    a.dutfile, a.std = prep_dut(a, a.out)
    {'dc': cmd_dc, 'fft': cmd_fft, 'corners': cmd_corners, 'lin': cmd_lin}[a.cmd](a)
