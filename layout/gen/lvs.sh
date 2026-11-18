#!/bin/bash
# run inside layout/work after drc.sh created the .mag files
export PDK_ROOT=/foss/pdks PDK=sky130A
python3 ../gen/lvsref.py sar10_adc_ref.spice
cat > _ext.tcl <<'T'
load sar10_adc
select top cell
extract do local
extract all
ext2spice lvs
ext2spice -o sar10_adc_lay.spice
quit -noprompt
T
magic -dnull -noconsole -rcfile $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc _ext.tcl 2>&1 | grep -iE "error|warning: |illegal" | sort | uniq -c | head -8
grep -c "sar10_ucap" sar10_adc_lay.spice; grep -n "^.subckt" sar10_adc_lay.spice | cut -c1-150 | tail -6
netgen -batch lvs "sar10_adc_lay.spice sar10_adc" "sar10_adc_ref.spice sar10_adc" $PDK_ROOT/sky130A/libs.tech/netgen/sky130A_setup.tcl lvs.out > netgen.log 2>&1
tail -25 netgen.log | cut -c1-200
