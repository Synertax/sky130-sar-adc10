"""Loop-timing comparison schematic vs post-layout: one conversion, edge times of the self-timed loop."""
import sys, os, types, numpy as np
sys.path.insert(0, '/foss/designs/Analog/SAR_ADC10/gen'); import flow, tb
CO, TE, VD = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); FS = float(sys.argv[4]) if len(sys.argv) > 4 else 25e6
def run(tag, dut, pr):
    a = types.SimpleNamespace(env='foss', dut=dut, fs=FS, duty=0.25, vdd=VD, amp=1.5, acc='hi', keep=False, out='/foss/designs/Analog/SAR_ADC10/sim/diag_' + tag)
    os.makedirs(a.out, exist_ok=True)
    a.dutfile, a.std = flow.prep_dut(a, a.out)
    d, m, dt = flow.run_deck(a, a.out, 'd', vd=[0.4, -0.9], ncyc=2, corner=CO, temp=TE, vdd=VD, probes=list(pr.values()))
    t = d['time']; keys = {k.lower(): k for k in d}
    def edges(name, th=VD / 2):
        x = d[keys['v(%s)' % pr[name].lower()]]; s = x > th; i = np.where(s[1:] != s[:-1])[0]
        return [(t[j] + (th - x[j]) / (x[j + 1] - x[j]) * (t[j + 1] - t[j]), int(s[j + 1])) for j in i]
    t0 = 1e-9 + 0.25 / FS          # first sampling edge
    print('==', tag, 'sim %.0f s' % dt, ' P_vdd %.1f uW P_ref %.1f uW' % tuple(x * 1e6 for x in tb.power(d, m)))
    for n in pr:
        e = [(round((tt - t0) * 1e9, 3), s) for tt, s in edges(n) if t0 - 0.2e-9 < tt < t0 + 2 / FS]
        print('  %-7s' % n, ' '.join('%s%.2f' % ('+' if s else '-', tt) for tt, s in e[:40]))
S = dict(clkc='x1.clkc', outp='x1.outp', outn='x1.outn', validb='x1.validb', qp='x1.qp', dp1='x1.dp1', dpb1='x1.dpb1', dn1='x1.dn1', dec1='x1.dec1', t1='x1.t1', bl1='x1.xdp1.bh', dp2='x1.dp2', dn2='x1.dn2', rstb='x1.rstb', samp='x1.samp')
L = dict(eoc='eoc', b9='b9', clkc='x1.sar10_dig_0/CLKC', outp='x1.sar10_dig_0/OUTP', outn='x1.sar10_dig_0/OUTN', dp1='x1.sar10_dig_0/DP1', dn1='x1.sar10_dig_0/DN1', bl1='x1.XDP1_BH', dp2='x1.sar10_dig_0/DP2', dn2='x1.sar10_dig_0/DN2', samp='x1.sar10_dig_0/SAMP')
DUT = sys.argv[5] if len(sys.argv) > 5 else '/foss/designs/Analog/SAR_ADC10/layout/work/sar10_adc_pex.spice'
import re
_t = open(DUT).read()
def find(*c):
    for k in c:
        m = re.search(r'sar10_dig_0/' + k + r'(?=\s)', _t)
        if m: return 'x1.' + m.group(0)
for nm, c in dict(qp=(r'XCTL_xqp/Y', r'XS\d+_xlpb/A1'), valid=('XCTL_xv/Y', 'XCTL_xvb/A'), validb=('XCTL_xvb/Y', 'XCTL_xg/B', r'XS\d+_xst/B'),
                  clkcb=('XCTL_xg/Y', 'XCTL_xgb/A'), lpb1=('XS1_xlpb/Y', 'XS1_xlp/A', 'XS1_xdec/A', 'XS1_xgdp/A'), lp1=('XS1_xlp/Y', 'XS1_xlpb/B1', 'XS1_xgdpb/A'),
                  t1=('XS1_xt/Y', 'XS1_xtb/A', r'XS2_xlpb/A2')).items():
    f = find(*c)
    if f: L[nm] = f
    else: print('no net for', nm)
L['dnb1'] = 'x1.sar10_dig_0/DNB1'; L['dpb1'] = 'x1.sar10_dig_0/DPB1'
run('pex', sys.argv[5] if len(sys.argv) > 5 else '/foss/designs/Analog/SAR_ADC10/layout/work/sar10_adc_pex.spice', L)
