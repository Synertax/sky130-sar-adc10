#!/bin/bash
export PDK_ROOT=/foss/pdks PDK=sky130A
# the vendor cells' implant edges differ by 5 nm between cells: next to a tap this can leave a sub-minimum notch (klayout nsdm.1 / psdm.1).
# It depends on which cells end up beside / above a tap, so try a few placement densities until the macro is clean.
for DIG_TAPD in 12 13 14 11; do
for DIG_DENS in 0.75 0.70 0.80 0.65 0.72 0.78 0.68 0.60; do
export DIG_DENS DIG_TAPD
cd /foss/designs/Analog/SAR_ADC10/layout/work/dig && python3 ../../gen/dig.py pins.json && openroad -exit or.tcl > or.log 2>&1
grep -E "ERROR|Number of violations" or.log | tail -3
cd .. && rm -f sar10_dig.mag && cat > _def.tcl <<'T'
lef read /foss/pdks/sky130A/libs.ref/sky130_fd_sc_hd/techlef/sky130_fd_sc_hd__nom.tlef
def read dig/sar10_dig.def
load sar10_dig
select top cell
puts "DIGBBOX [box values]"
expand
drc on
drc style drc(full)
drc check
drc catchup
puts "DRC_TOTAL [drc list count total]"
foreach {why boxes} [drc listall why] { puts "DRC_WHY [llength $boxes] :: $why :: [lrange $boxes 0 1]" }
save sar10_dig
gds write sar10_dig.gds
quit -noprompt
T
magic -dnull -noconsole -rcfile $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc _def.tcl 2>&1 | grep -E "DRC_|DIGBBOX|rror" | cut -c1-250 | head
klayout -b -r /foss/pdks/sky130A/libs.tech/klayout/drc/sky130A_mr.drc -rd input=sar10_dig.gds -rd report=kl_dig.xml -rd feol=true -rd beol=false -rd offgrid=false > kl_dig.log 2>&1
NV=$(grep -c "<category>'[np]sdm" kl_dig.xml); echo "macro tap $DIG_TAPD density $DIG_DENS: implant notches $NV"
[ "$NV" = "0" ] && break 2
done
done
