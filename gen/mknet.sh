#!/bin/bash
# 1. netlist sar10_adc.sch with xschem (simulation netlist + LVS netlist)
# 2. compare the xschem netlist, device by device, with the reference netlist built from gen/design.py
# 3. check every device size against the sky130 minimum W / L
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDK=${PDK:-sky130A}
B="$(cd "$(dirname "$0")/.." && pwd)"; cd "$B" || exit 1
mkdir -p netlist netlist/lvs
xschem --rcfile xschemrc -n -s -q -x --tcl "set top_is_subckt 1" -o netlist sar10_adc.sch > netlist/xschem.log 2>&1 || { echo "xschem failed"; cat netlist/xschem.log; exit 1; }
xschem --rcfile xschemrc -n -s -q -x --tcl "set top_is_subckt 1; set lvs_netlist 1" -o netlist/lvs sar10_adc.sch > netlist/lvs/xschem.log 2>&1 || echo "LVS netlist failed"
grep -i "error\|warn\|not found" netlist/xschem.log netlist/lvs/xschem.log
python3 - <<'PY'
import sys; sys.path.insert(0, 'gen')
import design, netlist
cells = design.build()
netlist.emit(cells, 'netlist/sar10_adc_ref.spice')
bad = 0; n = 0
for c in cells.values():
    for i in c.insts:
        if i.kind == 'mos':
            n += 1
            wf = i.kw['W'] / i.kw['nf']
            if wf < 0.42 - 1e-9 or i.kw['L'] < 0.15 - 1e-9:
                bad += 1; print('SIZE VIOLATION', c.name, i.name, i.kw)
        if i.kind == 'mim' and (i.kw['W'] < 2 or i.kw['L'] < 2):
            bad += 1; print('SIZE VIOLATION', c.name, i.name, i.kw)
print('device size check: %d MOS device types checked, %d violations' % (n, bad))
PY
python3 gen/cmpnet.py netlist/sar10_adc.spice netlist/sar10_adc_ref.spice | tail -1
