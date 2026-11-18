#!/bin/bash
# usage: drc.sh script.tcl topcell   (run inside layout/work)
export PDK_ROOT=/foss/pdks PDK=sky130A
for c in $(grep '^load' $1 | awk '{print $2}'); do rm -f $c.mag; done
cat > _drc_$2.tcl <<T
source $1
load $2
select top cell
expand
drc on
drc style drc(full)
drc check
drc catchup
set n [drc list count total]
puts "DRC_TOTAL \$n"
foreach {why boxes} [drc listall why] {
  puts "DRC_WHY [llength \$boxes] :: \$why :: [lrange \$boxes 0 2]"
}
quit -noprompt
T
magic -dnull -noconsole -rcfile $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc _drc_$2.tcl 2>&1 | grep -E "DRC_|rror|nknown|invalid" | cut -c1-330
