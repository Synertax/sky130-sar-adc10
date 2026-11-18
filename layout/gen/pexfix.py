"""Post-layout netlist = magic wire parasitics + PDK capacitor devices.
magic extracts the metal inside the PDK capacitor cell as ordinary wire capacitance (and drops the device in a flat netlist).
The cell's own C0-C1 capacitance is replaced by the PDK model: subtract (units x c_int) from every top-plate/bit-line
capacitor and add the capacitor instances taken from the LVS netlist."""
import re, sys, collections
raw, lay, cint, out = sys.argv[1:5]
LUMP = '--devices' not in sys.argv
cint = float(open(cint).read().split()[0])
J = lambda p: re.sub(r'\n\+', ' ', open(p).read())
top = re.search(r'\.subckt sar10_adc .*?\n(.*)\.ends', J(lay), re.S).group(1)
caps = [l.split() for l in top.split('\n') if 'cap_vpp' in l]
n = collections.Counter()
for t in caps:
    if t[1] != t[2]: n[frozenset((t[1], t[2]))] += 1
L = []; fixed = 0
for l in J(raw).split('\n'):
    t = l.split()
    if t and t[0][0] == 'C' and frozenset((t[1], t[2])) in n:
        v = t[3]; v = float(v[:-1]) * {'f': 1, 'p': 1e3, 'a': 1e-3}[v[-1]]
        v2 = max(v - n[frozenset((t[1], t[2]))] * cint, 0.0); fixed += 1
        l = '%s %s %s %.4ff' % (t[0], t[1], t[2], v2)
    if l.startswith('.ends'):
        if LUMP:      # same capacitance as the PDK model (0.578 c0-c1, 0.179 m3-c1, 0.444 m3-c0, 0.104 c0 shield-substrate), one element per net pair
            tot = collections.Counter()
            for t in caps:
                c0, c1, b, m3 = t[1:5]
                for x, y, v in ((c0, c1, 0.578), (m3, c1, 0.179), (m3, c0, 0.444), (c0, b, 0.104)):
                    if x != y: tot[tuple(sorted((x, y)))] += v
            L += ['CU%d %s %s %.4ff' % (i, x, y, v) for i, ((x, y), v) in enumerate(sorted(tot.items()))]
        else:
            L += ['XU%d %s %s %s %s %s' % (i, t[1], t[2], t[3], t[4], t[5]) for i, t in enumerate(caps)]
    L.append(l)
open(out, 'w').write('\n'.join(L) + '\n')
print('pexfix: %d capacitor devices added, %d top-plate capacitors corrected by c_int = %.4f fF/unit' % (len(caps), fixed, cint))
