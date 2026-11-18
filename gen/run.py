#!/usr/bin/env python3
"""One command per experiment: build -> checks -> quick multi-input test -> FFT, each stage only if the previous passed.
   python3 gen/run.py NAME [--design gen/design_X.py] [--stage build|quick|fft|all] [--from quick|fft] [--note ..] [--predict ..]
Prints a scorecard against spec.json and appends ONE line to results.csv.  Runs inside the container."""
import argparse, os, sys, subprocess, json, time, types, re, shutil, datetime
R = '/foss/designs/Analog/SAR_ADC10'
sys.path.insert(0, R + '/gen')
os.environ.update(PDK_ROOT='/foss/pdks', PDK='sky130A', XSCHEM_SKY130='/foss/pdks/sky130A/libs.tech/xschem')
p = argparse.ArgumentParser()
p.add_argument('name'); p.add_argument('--design'); p.add_argument('--stage', default='all'); p.add_argument('--from', dest='frm', default='build')
p.add_argument('--note', default=''); p.add_argument('--predict', default=''); p.add_argument('--fs', type=float, default=25e6)
p.add_argument('--amp', type=float, default=1.4); p.add_argument('--layout', default='', help='suffix: copies layout/gen/{top,dig,lay}_SUF.py into place'); p.add_argument('--npts', type=int, default=32)
A = p.parse_args()
SPEC = json.load(open(R + '/spec.json')); W = R + '/layout/work'; PEX = '%s/%s_pex.spice' % (W, A.name)
r = dict(variant=A.name, note=A.note, predict=A.predict); fails = []
def sh(cmd, cwd=R):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True).stdout
def num(pat, s, d=None, f=float):
    m = re.search(pat, s); return f(m.group(1)) if m else d
def gate(key, ok, msg):
    if not ok: fails.append(msg)
    return ok
OUT = '%s/sim/run_%s' % (R, A.name); os.makedirs(OUT, exist_ok=True)
def capreport():
    """per-net extracted capacitance (total + 3 largest couplings) and CDAC bit weights from the pex netlist"""
    if not os.path.exists(PEX): return
    import collections
    C = collections.defaultdict(float); T = collections.defaultdict(lambda: collections.defaultdict(float))
    for l in open(PEX):
        t = l.split()
        if not t or not t[0].startswith('C') or len(t) < 4: continue
        m = re.match(r'([0-9.e+-]+)([a-z]*)', t[3].lower())
        if not m: continue
        x = float(m.group(1)) * {'f': 1, 'p': 1e3, 'a': 1e-3, 'n': 1e6}.get(m.group(2)[:1], 1e15)
        for a_, b_ in ((t[1], t[2]), (t[2], t[1])): C[a_] += x; T[a_][b_] += x
    sn = lambda n: n.replace('sar10_dig_0/', 'dig/')
    with open(OUT + '/netcaps.csv', 'w') as f:
        f.write('net,total_fF,coupling1,fF1,coupling2,fF2,coupling3,fF3\n')
        for n in sorted(C, key=lambda n: -C[n]):
            if n in ('VSS', 'VDD', 'VREFP', 'VREFN') or re.search(r'/a_\d+_\d+#|^a_\d|^w_\d', n) or C[n] < 0.5: continue
            top3 = sorted(T[n].items(), key=lambda kv: -kv[1])[:3]
            f.write('%s,%.2f,%s\n' % (sn(n), C[n], ','.join('%s,%.2f' % (sn(k), v) for k, v in top3)))
    with open(OUT + '/bitweights.csv', 'w') as f:
        f.write('bit,units,BH_to_TOPP_fF,BL_to_TOPP_fF,fF_per_unit_H,fF_per_unit_L,err_vs_MSB_pct\n')
        ref = T['XDP1_BH']['TOPP'] / 128 if T['XDP1_BH']['TOPP'] else 1
        for b in range(1, 10):
            u = 2 ** (8 - b) if b < 9 else 1; h = T['XDP%d_BH' % b]['TOPP']; l_ = T['XDP%d_BL' % b]['TOPP']
            f.write('%d,%d,%.3f,%.3f,%.4f,%.4f,%.2f\n' % (b, u, h, l_, h / u, l_ / u, 100 * ((h + l_) / 2 / u / ref - 1)))
        f.write('# TOPP total %.1f fF (VSS %.1f); TOPN total %.1f fF (VSS %.1f)\n' % (C['TOPP'], T['TOPP']['VSS'], C['TOPN'], T['TOPN']['VSS']))
def finish():
    try: capreport()
    except Exception as e: print('capreport skipped:', e)
    order = ['schem', 'unrouted', 'drc', 'klayout', 'lvs', 'q_missing', 'q_tmax', 'q_inl', 'enob', 'sfdr', 'tmax', 'tvalid', 'tmean', 'power', 'missing']
    r['verdict'] = 'PASS' if not fails else 'FAIL: ' + '; '.join(fails)
    if not fails and 'enob' not in r: r['verdict'] = 'PASS (stopped before FFT)'
    path = R + '/results.csv'; new = not os.path.exists(path)
    with open(path, 'a') as f:
        if new: f.write('date,variant,' + ','.join(order) + ',verdict,predict,note\n')
        f.write('%s,%s,%s,%s,%s,%s\n' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), A.name, ','.join(str(r.get(k, '')) for k in order),
                                         r['verdict'], A.predict.replace(',', ';'), A.note.replace(',', ';')))
    json.dump(dict(r, spec=SPEC, fails=fails, args=vars(A), files=sorted(os.listdir(OUT))), open(OUT + '/data.json', 'w'), indent=1)
    print('DATA ' + OUT)
    print('SUMMARY %s | ' % A.name + ' '.join('%s=%s' % (k, r[k]) for k in order if k in r) + ' | ' + r['verdict'])
    if 'tmax' in r: print('goal: conversion %.1f ns vs goal %.1f ns' % (r['tmax'], SPEC['goal_tconv_ns']))
    sys.exit(0)
stages = ['build', 'quick', 'fft']; i0 = stages.index(A.frm); i1 = 2 if A.stage == 'all' else stages.index(A.stage)
# ---------------------------------------------------------------- build + physical checks
if i0 <= 0:
    if A.design: shutil.copyfile(os.path.join(R, A.design), R + '/gen/design.py')
    for f_ in ('top', 'dig', 'lay'):
        src = '%s/layout/gen/%s_%s.py' % (R, f_, A.layout)
        if A.layout and os.path.exists(src): shutil.copyfile(src, '%s/layout/gen/%s.py' % (R, f_))
    shutil.copyfile(R + '/gen/design.py', R + '/gen/design_%s.py' % A.name) if not os.path.exists(R + '/gen/design_%s.py' % A.name) else None
    o = sh('python3 gen/draw.py . 2>&1 | tail -2; bash gen/mknet.sh 2>&1 | tail -3')
    r['schem'] = 'ok' if 'IDENTICAL' in o else 'DIFF'
    if r['schem'] != 'ok': print(o)
    if not gate('schem', r['schem'] == 'ok', 'schematic netlist differs: ' + o.strip().split('\n')[-1][:80]): finish()
    o = sh('python3 top.py 2>&1 | tail -4', R + '/layout/gen'); r['unrouted'] = num(r'unrouted (\d+)', o, -1, int)
    if r['unrouted'] != 0: print(o)
    if not gate('unrouted', 0 <= r['unrouted'] <= SPEC['unrouted_max'], 'unrouted %s' % r['unrouted']): finish()
    o = sh('bash ../gen/mkdig.sh | tail -2; bash ../gen/drc.sh sar10_adc.tcl sar10_adc | head -4', W); r['drc'] = num(r'DRC_TOTAL (\d+)', o, -1, int)
    o = sh('bash ../gen/lvs.sh | tail -8', W); r['lvs'] = 'match' if 'Circuits match uniquely' in o else 'FAIL'
    sh('bash ../gen/pex.sh | tail -1', W)
    sh('klayout -b -r /foss/pdks/sky130A/libs.tech/klayout/drc/sky130A_mr.drc -rd input=sar10_adc.gds -rd report=kl_drc.xml -rd feol=true -rd beol=true -rd offgrid=true > kl_drc.log 2>&1', W)
    r['klayout'] = open(W + '/kl_drc.xml').read().count('<item>') if os.path.exists(W + '/kl_drc.xml') else -1
    shutil.copyfile(W + '/sar10_adc_pex.spice', PEX); shutil.copyfile(W + '/sar10_adc.gds', '%s/%s.gds' % (W, A.name))
    gate('drc', 0 <= r['drc'] <= SPEC['drc_magic_max'], 'magic DRC %s' % r['drc'])
    gate('klayout', 0 <= r['klayout'] <= SPEC['drc_klayout_max'], 'klayout DRC %s' % r['klayout'])
    gate('lvs', r['lvs'] == 'match', 'LVS mismatch')
    if fails or i1 == 0: finish()
import numpy as np, flow, tb
a = types.SimpleNamespace(env='foss', dut=PEX, fs=A.fs, duty=0.25, vdd=1.8, amp=A.amp, acc='hi', keep=False, out='%s/sim/run_%s' % (R, A.name), corner='tt', temp=27, N=64, M=13, par=12)
os.makedirs(a.out, exist_ok=True); a.dutfile, a.std = flow.prep_dut(a, a.out)
# ---------------------------------------------------------------- quick test: spread DC inputs, every conversion must finish
if i0 <= 1:
    rng = np.random.RandomState(1); vds = list(np.linspace(-A.amp, A.amp, A.npts) + rng.uniform(-0.02, 0.02, A.npts))
    code, vs, res, tc = flow.points_run(a, a.out, vds, 12, corner='tt', temp=27, vdd=1.8)
    lsb = 2 * 1.8 / 1024; ok = ~np.isnan(tc)
    np.savetxt(OUT + '/quick.csv', np.c_[vds, vs, code, res / lsb, tc * 1e9], fmt='%.6f', delimiter=',', header='vd_set_V,vd_sampled_V,code,residue_LSB,tconv_ns', comments='')
    r['q_missing'] = int((~ok).sum()); r['q_tmax'] = round(float(np.nanmax(tc)) * 1e9, 2) if ok.any() else -1
    try:
        k, err = flow.lin_fit(code[ok], vs[ok], res[ok], lsb); r['q_inl'] = round(float(np.abs(err).max()), 2)
    except Exception: r['q_inl'] = -1
    gate('q_missing', r['q_missing'] <= SPEC['quick_missing_eoc_max'], '%d of %d quick conversions never finished' % (r['q_missing'], A.npts))
    gate('q_tmax', 0 < r['q_tmax'] <= SPEC['quick_tconv_max_ns'], 'quick conversion %.2f ns' % r['q_tmax'])
    gate('q_inl', 0 <= r['q_inl'] <= SPEC['quick_inl_max_lsb'], 'quick nonlinearity %.2f LSB' % r['q_inl'])
    if fails or i1 == 1: finish()
# ---------------------------------------------------------------- FFT
code, vs, tc, (pv, pr), dt = flow.sine_run(a, a.out, 64, 13, 12, corner='tt', temp=27, vdd=1.8)
f = tb.fft_metrics(code)
r.update(enob=round(f['enob'], 2), sfdr=round(f['sfdr'], 1), tmax=round(float(np.nanmax(tc)) * 1e9, 2), tmean=round(float(np.nanmean(tc)) * 1e9, 2),
         power=round((pv + pr) * 1e6, 1), missing=int(np.isnan(tc).sum()),
         tvalid=round(float(np.nanmax([x for k_ in sorted(flow.LAST_TVALID) for x in flow.LAST_TVALID[k_]])) * 1e9, 2))
np.savetxt(OUT + '/fft_samples.csv', np.c_[np.arange(len(code)), vs, code, tc * 1e9], fmt='%.6f', delimiter=',', header='n,vd_sampled_V,code,tconv_ns', comments='')
x_ = code - code.mean(); X_ = np.abs(np.fft.rfft(x_)) / (len(x_) / 2) / 512; X_[0] = 1e-12
np.savetxt(OUT + '/spectrum.csv', np.c_[np.arange(len(X_)) * A.fs / 64 / 1e6, 20 * np.log10(np.maximum(X_, 1e-7))], fmt='%.4f', delimiter=',', header='freq_MHz,dBFS', comments='')
gate('missing', r['missing'] <= SPEC['missing_eoc_max'], '%d FFT conversions never finished' % r['missing'])
gate('enob', r['enob'] >= SPEC['enob_min'], 'ENOB %.2f < %.2f' % (r['enob'], SPEC['enob_min']))
gate('tmax', r['tmax'] <= SPEC['tconv_max_ns'], 'conversion %.2f ns > %.1f' % (r['tmax'], SPEC['tconv_max_ns']))
gate('power', r['power'] <= SPEC['power_max_uw'], 'power %.0f uW' % r['power'])
finish()
