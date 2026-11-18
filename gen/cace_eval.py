#!/usr/bin/env python3
"""Post-processing for the CACE testbenches (called from the ngspice .control block).
  cace_eval.py fft    RAW FS DUTY NCYC VDD OUT   -> enob sndr sfdr thd p_total t_conv
  cace_eval.py static RAW FS DUTY NCYC VDD OUT   -> code_err p_total p_vdd p_ref t_conv e_conv
All values are written in SI units on one line (CACE scales them for display)."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tb

mode, raw, fs, duty, ncyc, vdd, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(float(sys.argv[5])), float(sys.argv[6]), sys.argv[7]
m = dict(T=1 / fs, ts=duty / fs, t0=1e-9, ncyc=ncyc, nbit=10, vdd=vdd, vref=vdd, fs=fs)
d = tb.read_raw(raw)
cs = tb.codes(d, m)[1:]                     # first conversion starts from the power-up state: dropped
code = np.array([c[0] for c in cs]); vs = np.array([c[1] for c in cs]); tc = np.array([c[2] for c in cs])
pv, pr = tb.power(d, m, 1)
tconv = float(np.nanmax(tc)) if not np.isnan(tc).all() else 1.0
if np.isnan(tc).any():
    tconv = 1.0                             # a conversion never finished: make the spec fail loudly
if mode == 'fft':
    f = tb.fft_metrics(code)
    vals = [f['enob'], f['sndr'], f['sfdr'], f['thd'], pv + pr, tconv]
else:
    i, j = int(np.argmin(vs)), int(np.argmax(vs))
    line = code[i] + (vs - vs[i]) * (code[j] - code[i]) / (vs[j] - vs[i])
    err = float(np.abs(code - line).max())  # end-point error of the 8 test inputs, in LSB (includes +-0.5 LSB quantisation)
    vals = [err, pv + pr, pv, pr, tconv, (pv + pr) / fs]
open(out, 'w').write(' '.join('%.6g' % v for v in vals) + '\n')
print(mode, vals)
