#!/bin/bash
# flat parasitic extraction + GDS export + klayout DRC (run inside layout/work after drc.sh)
export PDK_ROOT=/foss/pdks PDK=sky130A
cat > _pex.tcl <<'T'
load sar10_adc
select top cell
gds write sar10_adc.gds
extract do local
extract all
ext2spice format ngspice
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice cthresh 0.005
ext2spice -o sar10_adc_pex_raw.spice
puts done
quit -noprompt
T
rm -f sar10_adc_flat.mag sar10_adc_flat.ext
magic -dnull -noconsole -rcfile $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc _pex.tcl 2>&1 | grep -iE "^error|illegal" | head -5
ls -la sar10_adc.gds sar10_adc_pex_raw.spice; grep -c "^C" sar10_adc_pex_raw.spice; grep -c "^X" sar10_adc_pex_raw.spice; grep "^.subckt" sar10_adc_pex_raw.spice | cut -c1-200
rm -f t_uc1.mag t_uc1.ext
cat > _ci.tcl <<'T'
source t_uc1.tcl
load t_uc1
select top cell
extract do local
extract all
ext2spice format ngspice
ext2spice hierarchy off
ext2spice cthresh 0.001
ext2spice -o t_uc1_pex.spice
quit -noprompt
T
magic -dnull -noconsole -rcfile $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc _ci.tcl > /dev/null 2>&1
rm -f t_uc1.mag; grep "^C" t_uc1_pex.spice | grep -w "T" | grep -w "B" | awk '{v=$4; sub(/f/,"",v); print v}' > ucap_cint.txt; cat ucap_cint.txt
if grep -q floatm3 sar10_adc_lay.spice; then python3 ../gen/pexfix.py sar10_adc_pex_raw.spice sar10_adc_lay.spice ucap_cint.txt sar10_adc_pex_fix.spice; else cp sar10_adc_pex_raw.spice sar10_adc_pex_fix.spice; fi
python3 ../gen/pexwrap.py sar10_adc_pex_fix.spice sar10_adc_pex.spice
