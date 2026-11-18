"""Turn magic's flat extraction into a drop-in DUT netlist: same subckt name and pin order as the schematic."""
import re, sys
s = re.sub(r'\n\+', ' ', open(sys.argv[1]).read())
hdr = '.subckt sar10_adc VIP VIN CLK ' + ' '.join('B%d' % i for i in range(9, -1, -1)) + ' EOC VDD VREFP VREFN VSS'
s, n = re.subn(r'\.subckt sar10_adc(_flat)? [^\n]*', hdr, s); assert n == 1
open(sys.argv[2], 'w').write('* sar10_adc post-layout netlist (magic flat extraction, C only)\n' + s)
