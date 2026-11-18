"""LVS reference netlist from the simulation reference netlist (runs in the container).
Changes vs the schematic netlist: unit caps -> sar10_ucap instances (one per unit), driver NMOS bulk VREFN -> VSS (same potential, no deep n-well)."""
import re, sys
R = '/foss/designs/Analog/SAR_ADC10/netlist/sar10_adc_ref.spice'
LIB = '/foss/pdks/sky130A/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice'
out = ['* LVS reference for sar10_adc']
used = set(); custom = False
for l in re.sub(r'\n\+', ' ', open(R).read()).split('\n'):
    t = l.split()
    if not t or l.startswith('*'): continue
    if 'cap_vpp' in l and 'floatm3' not in l:          # custom unit capacitor sar10_ucap (T = c1, B = c0)
        m = int(float([x for x in t if x.startswith('m=')][0][2:])); custom = True
        out += ['%s_%d %s %s sar10_ucap' % (t[0], i, t[2], t[1]) for i in range(m)]; continue
    if 'cap_vpp' in l:
        m = int(float([x for x in t if x.startswith('m=')][0][2:]))
        out += ['%s_%d %s' % (t[0], i, ' '.join(t[1:6])) for i in range(m)]; continue
    if 'fet_01v8' in l:
        if 'nfet' in l and t[4] == 'VREFN': t[4] = 'VSS'      # driver NMOS bulk: p-substrate (same potential as VREFN)
        keep = t[:6] + [x for x in t[6:] if x.split('=')[0] in ('L', 'W', 'm')]
        out.append(' '.join(keep)); continue
    if t[-1].startswith('sky130_fd_sc_hd__'): used.add(t[-1])
    out.append(l)
lib = re.sub(r'\n\+', ' ', open(LIB).read())
for c in sorted(used):
    m = re.search(r'\.subckt %s .*?\.ends' % c, lib, re.S); out.append(m.group(0))
if custom: out.append('.subckt sar10_ucap T B\n.ends')
open(sys.argv[1], 'w').write('\n'.join(out) + '\n')
