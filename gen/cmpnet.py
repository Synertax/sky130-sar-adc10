#!/usr/bin/env python3
"""Compare the xschem netlist with the reference netlist generated from design.py (device by device)."""
import sys, re, collections
def load(path):
    txt = open(path).read().replace('\n+', ' ')
    subs, cur = {}, None
    for ln in txt.split('\n'):
        ln = ln.strip()
        if not ln or ln.startswith('*'):
            continue
        t = ln.split()
        if t[0].lower() == '.subckt':
            cur = t[1].lower(); subs[cur] = dict(ports=[x.lower() for x in t[2:]], inst=[])
        elif t[0].lower() == '.ends':
            cur = None
        elif cur and t[0][0].lower() == 'x':
            nets = [x.lower() for x in t[1:] if '=' not in x]
            par = dict(x.lower().split('=', 1) for x in t[1:] if '=' in x)
            keep = {k: ('%g' % float(v)) for k, v in par.items() if k in ('l', 'w', 'nf', 'mult', 'mf')}
            subs[cur]['inst'].append((t[0].lower(), nets[-1], nets[:-1], keep))
    return subs
def canon(sub):
    cnt = collections.Counter(n for i in sub['inst'] for n in i[2])
    for p in sub['ports']: cnt[p] += 1
    f = lambda n: '?' if cnt[n] == 1 else n
    return sorted((i[0], i[1], tuple(f(n) for n in i[2]), tuple(sorted(i[3].items()))) for i in sub['inst'])
a, b = load(sys.argv[1]), load(sys.argv[2])
bad = 0
for name in sorted(set(a) | set(b)):
    if name not in a or name not in b:
        print('MISSING subckt', name, 'in', 'xschem' if name not in a else 'reference'); bad += 1; continue
    if a[name]['ports'] != b[name]['ports']:
        print(name, 'PORT ORDER differs:', a[name]['ports'], b[name]['ports']); bad += 1
    ca, cb = canon(a[name]), canon(b[name])
    if ca != cb:
        bad += 1
        print(name, 'DIFFERS')
        for x in ca:
            if x not in cb: print('   xschem only:', x)
        for x in cb:
            if x not in ca: print('   ref only   :', x)
    else:
        print('%-14s match  (%d devices)' % (name, len(ca)))
print('RESULT:', 'IDENTICAL' if not bad else '%d MISMATCHES' % bad)
sys.exit(1 if bad else 0)
