"""Digital part (slices + ctrl) -> structural verilog + OpenROAD script.  Runs inside the container (needs the PDK)."""
import re, sys, json, os
sys.path.insert(0, '/foss/designs/Analog/SAR_ADC10/layout/gen'); import lay
PDK = '/foss/pdks/sky130A/libs.ref/sky130_fd_sc_hd'
S = lay.subckts('/foss/designs/Analog/SAR_ADC10/netlist/sar10_adc_ref.spice')
lib = lay.subckts(PDK + '/spice/sky130_fd_sc_hd.spice')
top = S['sar10_adc'][1]
insts = []          # (name, cell, {pin: net})
for t in top:
    sub = t[-1]
    if sub not in ('sar10_slice', 'sar10_ctrl'): continue
    ports = S[sub][0]; m = dict(zip(ports, t[1:-1]))
    for u in S[sub][1]:
        cell = u[-1]; pins = lib[cell][0]
        conn = {}
        for p, n in zip(pins, u[1:-1]):
            if p in ('VGND', 'VNB', 'VPB', 'VPWR'): continue
            conn[p] = m.get(n, t[0] + '_' + n)
        insts.append((t[0] + '_' + u[0], cell, conn))
nets = sorted({n for i in insts for n in i[2].values()})
ins = ['OUTP', 'OUTN', 'CLK']
outs = ['CLKC', 'SAMP', 'EOC'] + ['B%d' % i for i in range(10)] + ['DP%d' % i for i in range(1, 10)] + ['DNB%d' % i for i in range(1, 10)] + ['DN%d' % i for i in range(1, 9)] + ['DPB%d' % i for i in range(1, 9)]
v = ['module sar10_dig (%s);' % ', '.join(ins + outs)] + ['  input %s;' % n for n in ins] + ['  output %s;' % n for n in outs]
v += ['  wire %s;' % n for n in nets if n not in ins + outs]
for n, c, conn in insts: v.append('  %s %s (%s);' % (c, n, ', '.join('.%s(%s)' % kv for kv in conn.items())))
open('sar10_dig.v', 'w').write('\n'.join(v) + '\nendmodule\n')
print(len(insts), 'cells', len(nets), 'nets')
J = json.load(open(sys.argv[1])); W, NR, pins = J['W'], J['NR'], J['pins']; MG = J.get('margin', 0)
H = (NR + 2) * 2.72
def loopfix():
    """pin the clock-loop cells (comparator outputs -> VALID -> delay line -> CLKC) in the top row right under the comparator pins:
    these nets set the bit-cycle time, the placer would otherwise scatter them along the 148 um block"""
    if not pins or 'OUTN' not in pins or not J.get('loopfix', False): return []
    order = ['XCTL_xqp', 'XCTL_xrun'] + sorted((n for n, c, k in insts if re.match(r'XCTL_xd\d+$', n)), key=lambda n: int(n[7:])) + ['XCTL_xv', 'XCTL_xvb', 'XCTL_xg', 'XCTL_xgb', 'XCTL_xqn']   # VALID gate centred: equal OUTN / OUTP branches
    y = 2720 * NR; ori = 'R0' if (NR - 1) % 2 == 0 else 'MX'
    x0 = 2300 + 460 * round((pins['OUTN'][1] * 1000 - 1400 - 2300) / 460)
    return ['set blk [ord::get_db_block]', 'set taps {}',
            'foreach i [$blk getInsts] { set bb [$i getBBox]; if {[string match TAP* [$i getName]] && [$bb yMin] == %d} { lappend taps [list [$bb xMin] [$bb xMax]] } }' % y,
            'set x %d' % x0,
            'foreach n {%s} { set i [$blk findInst $n]; set w [[$i getMaster] getWidth]; set ok 0; while {!$ok} { set ok 1; foreach t $taps { if {$x < [lindex $t 1] && [expr {$x + $w}] > [lindex $t 0]} { set x [lindex $t 1]; set ok 0 } } }; $i setOrient %s; $i setLocation $x %d; $i setPlacementStatus FIRM; puts "LOOPFIX $n $x"; set x [expr {$x + $w}] }' % (' '.join(order), ori, y)]
def cluster():
    """hand placement: every cell fixed.  Clock loop in the centre under the comparator pins, the ten slices as 4-row columns on both
    sides (MSB slices nearest), output flops on the far left.  Keeps QP / QN / VALIDB / CLKC and the MSB latch outputs short."""
    if not J.get('cluster', False): return None
    SITE = 460; g = lambda um: 2300 + SITE * round((um * 1000 - 2300) / SITE)
    xc = pins['OUTN'][1]; CW = J.get('colw', 13); LW = 27
    xl = g(xc) - SITE * (LW // 2 + 5 * CW)                    # left edge of the slice columns
    col = {}
    for j, k in enumerate([9, 7, 5, 3, 1]): col[k] = xl + j * CW * SITE
    xloop = xl + 5 * CW * SITE
    for j, k in enumerate([2, 4, 6, 8, 10]): col[k] = xloop + LW * SITE + j * CW * SITE
    order = [9, 7, 5, 3, 1, 'L', 2, 4, 6, 8, 10]
    srow = {3: ['xsp', 'xlp', 'xlpb'], 2: ['xsn', 'xln', 'xlnb'], 1: ['xdec', 'xst', 'xt'], 0: ['xtb']}
    lrow = {3: ['xqn', 'xv', 'xqp', 'xvb', 'xg', 'xgb'], 2: ['xd%d' % i for i in range(1, 2 * 3 + 1)], 1: ['xrun', 'xsd', 'xr1', 'xr2', 'xr3'], 0: ['xs1', 'xs2', 'xe']}
    have = {n for n, c, k in insts}
    lrow[2] = sorted((n[5:] for n in have if re.match(r'XCTL_xd\d+$', n)), key=lambda n: int(n[2:]))
    fl = {3: [9, 7, 5], 2: [3, 1, 2], 1: [4, 6], 0: [8, 10]}
    rows = []; used = set()
    for r in range(4):
        seq = [('@', xl - SITE * 17 * len(fl[r]) - SITE)]
        for k in fl[r]: seq += [('XS%d_xb' % k,), ('-',)]
        for o in order:
            if o == 'L':
                seq.append(('@', xloop))
                for n in lrow[r]: seq += [('XCTL_' + n,), ('-',)]
            else:
                seq.append(('@', col[o]))
                for n in srow[r]: seq += [('XS%d_%s' % (o, n),), ('-',)]
        rows.append((2720 * (r + 1), 'R0' if r % 2 == 0 else 'MX', seq))
        used |= {t[0] for t in seq if len(t) == 1 and t[0] != '-'}
    rest = sorted(have - used)
    if rest: rows[0][2].extend([('@', col[10] + CW * SITE)] + [x for n in rest for x in ((n,), ('-',))])
    assert not (used - have), used - have
    o = ['set blk [ord::get_db_block]']
    for y, ori, seq in rows:
        o += ['set taps {}', 'foreach i [$blk getInsts] { set bb [$i getBBox]; if {[string match TAP* [$i getName]] && [$bb yMin] == %d} { lappend taps [list [$bb xMin] [$bb xMax]] } }' % y, 'set x 0']
        for t in seq:
            if t[0] == '@': o.append('if {$x < %d} { set x %d }' % (t[1], t[1]))
            elif t[0] == '-': o.append('set x [expr {$x + %d}]' % SITE)
            else: o.append('set i [$blk findInst %s]; set w [[$i getMaster] getWidth]; set ok 0; while {!$ok} { set ok 1; foreach t $taps { if {$x < [lindex $t 1] && [expr {$x + $w}] > [lindex $t 0]} { set x [lindex $t 1]; set ok 0 } } }; $i setOrient %s; $i setLocation $x %d; $i setPlacementStatus FIRM; set x [expr {$x + $w}]' % (t[0], ori, y))
    return o
def nudge():
    """after global placement move each slice's CDAC pre-drivers (and output flop) onto their latch gate, then let detailed placement
    legalise: the weak latch outputs (a31oi / nor2b) then only see local wire, the long wires to the CDAC pins are driven by inv_4"""
    if not J.get('nudge', False): return []
    have = {n for n, c, k in insts}; o = ['set blk [ord::get_db_block]']
    for n in sorted(have):
        m = re.match(r'(XS\d+)_x(gdp|adpb|gdpb|gdn|adnb|gdnb|b|lp|ln|dec)$', n)
        if not m: continue
        anchor = m.group(1) + '_' + {'gdp': 'xlpb', 'adpb': 'xlpb', 'gdpb': 'xlpb', 'gdn': 'xlnb', 'adnb': 'xlnb', 'gdnb': 'xlnb', 'b': 'xlpb', 'lp': 'xlpb', 'ln': 'xlnb', 'dec': 'xlpb'}[m.group(2)]
        o.append('set a [[$blk findInst %s] getLocation]; [$blk findInst %s] setLocation [lindex $a 0] [lindex $a 1]' % (anchor, n))
    return o
o = ['read_lef %s/techlef/sky130_fd_sc_hd__nom.tlef' % PDK, 'read_lef %s/lef/sky130_fd_sc_hd.lef' % PDK,
     'read_verilog sar10_dig.v', 'link_design sar10_dig',
     'initialize_floorplan -die_area {0 0 %g %g} -core_area {%g 2.72 %g %g} -site unithd' % (W, H, MG, W - MG, H - 2.72), 'make_tracks']
if pins:
    for n, (layer, x, y) in pins.items(): o.append('place_pin -pin_name %s -layer %s -location {%g %g} -pin_size {0.3 0.8} -force_to_die_boundary' % (n, layer, x, y))
else: o.append('place_pins -hor_layers met3 -ver_layers met2')
o += ['tapcell -distance 12 -tapcell_master sky130_fd_sc_hd__tapvpwrvgnd_1'] + (cluster() or (loopfix() + ['global_placement -density %s' % os.environ.get('DIG_DENS', '0.75')] + nudge())) + ['detailed_placement',
      'filler_placement {sky130_fd_sc_hd__fill_8 sky130_fd_sc_hd__fill_4 sky130_fd_sc_hd__fill_2 sky130_fd_sc_hd__fill_1}',
      'check_placement', 'set_routing_layers -signal met1-met3', 'global_route', 'detailed_route', 'write_def sar10_dig.def', 'exit']
open('or.tcl', 'w').write('\n'.join(o) + '\n')
