v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sar10_adc} -720 -1080 0 0 0.7 0.7 {}
T {10-bit asynchronous SAR ADC, sky130A, 1.8 V.  CLK high = sample (bootstrapped top-plate sampling), CLK low = convert (self-timed).
Split-capacitor CDAC: every bit capacitor is two halves resting at VREFP / VREFN, so the common mode stays constant with no Vcm reference.
Bits 9..1 switch both sides (cells XDP/XDN 1..8), the last step switches one unit on the P side only.  B9..B0 update at EOC rising.} -720 -1030 0 0 0.3 0.3 {}
T {CDAC, P side (top plate TOPP)} 0 -500 0 0 0.35 0.35 {}
T {CDAC, N side (top plate TOPN)} 0 0 0 0 0.35 0.35 {}
T {SAR logic: one slice per bit, token T ripples left to right} 0 500 0 0 0.35 0.35 {}
N 4420 820 4460 820 {lab=B0}
N 3940 820 3980 820 {lab=B1}
N 3460 820 3500 820 {lab=B2}
N 2980 820 3020 820 {lab=B3}
N 2500 820 2540 820 {lab=B4}
N 2020 820 2060 820 {lab=B5}
N 1540 820 1580 820 {lab=B6}
N 1060 820 1100 820 {lab=B7}
N 580 820 620 820 {lab=B8}
N 100 820 140 820 {lab=B9}
N 4400 60 4400 -120 {lab=CLKC}
N 4750 60 4400 60 {lab=CLKC}
N 5020 -220 5100 -220 {lab=CLKC}
N 5100 -220 5100 60 {lab=CLKC}
N 5100 60 4750 60 {lab=CLKC}
N 5020 -100 5180 -100 {lab=EOC}
N 4500 -180 4600 -180 {lab=OUTN}
N 4600 -200 4710 -200 {lab=OUTN}
N 4600 -180 4600 -200 {lab=OUTN}
N 4710 -200 4820 -200 {lab=OUTN}
N 4500 -220 4660 -220 {lab=OUTP}
N 4660 -220 4820 -220 {lab=OUTP}
N 100 700 240 700 {lab=T1}
N 240 700 380 700 {lab=T1}
N 580 700 720 700 {lab=T2}
N 720 700 860 700 {lab=T2}
N 1060 700 1200 700 {lab=T3}
N 1200 700 1340 700 {lab=T3}
N 1540 700 1680 700 {lab=T4}
N 1680 700 1820 700 {lab=T4}
N 2020 700 2160 700 {lab=T5}
N 2160 700 2300 700 {lab=T5}
N 2500 700 2640 700 {lab=T6}
N 2640 700 2780 700 {lab=T6}
N 2980 700 3120 700 {lab=T7}
N 3120 700 3260 700 {lab=T7}
N 3460 700 3600 700 {lab=T8}
N 3600 700 3740 700 {lab=T8}
N 3940 700 4080 700 {lab=T9}
N 4080 700 4220 700 {lab=T9}
N -380 60 0 60 {lab=TOPN}
N 0 60 480 60 {lab=TOPN}
N 0 100 0 60 {lab=TOPN}
N 480 60 960 60 {lab=TOPN}
N 480 100 480 60 {lab=TOPN}
N 960 60 1440 60 {lab=TOPN}
N 960 100 960 60 {lab=TOPN}
N 1440 60 1920 60 {lab=TOPN}
N 1440 100 1440 60 {lab=TOPN}
N 1920 60 1930 60 {lab=TOPN}
N 1920 100 1920 60 {lab=TOPN}
N 1930 60 2400 60 {lab=TOPN}
N 2400 60 2880 60 {lab=TOPN}
N 2400 100 2400 60 {lab=TOPN}
N 2880 60 3360 60 {lab=TOPN}
N 2880 100 2880 60 {lab=TOPN}
N 3360 60 3840 60 {lab=TOPN}
N 3360 100 3360 60 {lab=TOPN}
N 3840 60 4240 60 {lab=TOPN}
N 3840 100 3840 60 {lab=TOPN}
N 4240 -160 4320 -160 {lab=TOPN}
N 4240 60 4240 -160 {lab=TOPN}
N -380 -440 0 -440 {lab=TOPP}
N 0 -440 480 -440 {lab=TOPP}
N 0 -400 0 -440 {lab=TOPP}
N 480 -440 960 -440 {lab=TOPP}
N 480 -400 480 -440 {lab=TOPP}
N 960 -440 1440 -440 {lab=TOPP}
N 960 -400 960 -440 {lab=TOPP}
N 1440 -440 1910 -440 {lab=TOPP}
N 1440 -400 1440 -440 {lab=TOPP}
N 1910 -440 1920 -440 {lab=TOPP}
N 1920 -440 2400 -440 {lab=TOPP}
N 1920 -400 1920 -440 {lab=TOPP}
N 2400 -440 2880 -440 {lab=TOPP}
N 2400 -400 2400 -440 {lab=TOPP}
N 2880 -440 3360 -440 {lab=TOPP}
N 2880 -400 2880 -440 {lab=TOPP}
N 3360 -440 3840 -440 {lab=TOPP}
N 3360 -400 3360 -440 {lab=TOPP}
N 3840 -440 4200 -440 {lab=TOPP}
N 3840 -400 3840 -440 {lab=TOPP}
N 4200 -440 4200 -240 {lab=TOPP}
N 4200 -240 4320 -240 {lab=TOPP}
N -500 -540 -500 -560 {lab=VDD}
N -500 -40 -500 -60 {lab=VDD}
N 0 620 0 600 {lab=VDD}
N 480 620 480 600 {lab=VDD}
N 960 620 960 600 {lab=VDD}
N 1440 620 1440 600 {lab=VDD}
N 1920 620 1920 600 {lab=VDD}
N 2400 620 2400 600 {lab=VDD}
N 2880 620 2880 600 {lab=VDD}
N 3360 620 3360 600 {lab=VDD}
N 3840 620 3840 600 {lab=VDD}
N 4320 620 4320 600 {lab=VDD}
N 4400 -280 4400 -300 {lab=VDD}
N 4920 -300 4920 -320 {lab=VDD}
N -720 60 -620 60 {lab=VIN}
N -720 -440 -620 -440 {lab=VIP}
N 3840 300 3840 320 {lab=VREFN}
N 0 900 0 920 {lab=VSS}
N 480 900 480 920 {lab=VSS}
N 960 900 960 920 {lab=VSS}
N 1440 900 1440 920 {lab=VSS}
N 1920 900 1920 920 {lab=VSS}
N 2400 900 2400 920 {lab=VSS}
N 2880 900 2880 920 {lab=VSS}
N 3360 900 3360 920 {lab=VSS}
N 3840 900 3840 920 {lab=VSS}
N 4320 900 4320 920 {lab=VSS}
N 4920 -20 4920 0 {lab=VSS}
C {ipin.sym} -720 -440 0 0 {name=p1 lab=VIP}
C {ipin.sym} -720 60 0 0 {name=p2 lab=VIN}
C {ipin.sym} -720 -190 0 0 {name=p3 lab=CLK}
C {opin.sym} 5180 -100 0 0 {name=p4 lab=EOC}
C {opin.sym} 140 820 0 0 {name=p5 lab=B9}
C {opin.sym} 620 820 0 0 {name=p6 lab=B8}
C {opin.sym} 1100 820 0 0 {name=p7 lab=B7}
C {opin.sym} 1580 820 0 0 {name=p8 lab=B6}
C {opin.sym} 2060 820 0 0 {name=p9 lab=B5}
C {opin.sym} 2540 820 0 0 {name=p10 lab=B4}
C {opin.sym} 3020 820 0 0 {name=p11 lab=B3}
C {opin.sym} 3500 820 0 0 {name=p12 lab=B2}
C {opin.sym} 3980 820 0 0 {name=p13 lab=B1}
C {opin.sym} 4460 820 0 0 {name=p14 lab=B0}
C {iopin.sym} -720 -860 0 0 {name=p15 lab=VDD}
C {iopin.sym} -720 -830 0 0 {name=p16 lab=VREFP}
C {iopin.sym} -720 -800 0 0 {name=p17 lab=VREFN}
C {iopin.sym} -720 -770 0 0 {name=p18 lab=VSS}
C {lab_pin.sym} -500 -560 2 0 {name=l19 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -540 -340 0 0 {name=l20 sig_type=std_logic lab=SAMP}
C {lab_pin.sym} -460 -340 2 0 {name=l21 sig_type=std_logic lab=VSS}
C {lab_pin.sym} -500 -60 2 0 {name=l22 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -540 160 0 0 {name=l23 sig_type=std_logic lab=SAMP}
C {lab_pin.sym} -460 160 2 0 {name=l24 sig_type=std_logic lab=VSS}
C {lab_pin.sym} -200 -300 0 0 {name=l25 sig_type=std_logic lab=DP1}
C {lab_pin.sym} -200 -280 0 0 {name=l26 sig_type=std_logic lab=DNB1}
C {lab_pin.sym} -120 -200 0 0 {name=l27 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -40 -200 0 0 {name=l28 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 40 -200 2 0 {name=l29 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 120 -200 2 0 {name=l30 sig_type=std_logic lab=VSS}
C {lab_pin.sym} -200 200 0 0 {name=l31 sig_type=std_logic lab=DN1}
C {lab_pin.sym} -200 220 0 0 {name=l32 sig_type=std_logic lab=DPB1}
C {lab_pin.sym} -120 300 0 0 {name=l33 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -40 300 0 0 {name=l34 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 40 300 2 0 {name=l35 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 120 300 2 0 {name=l36 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 280 -300 0 0 {name=l37 sig_type=std_logic lab=DP2}
C {lab_pin.sym} 280 -280 0 0 {name=l38 sig_type=std_logic lab=DNB2}
C {lab_pin.sym} 360 -200 0 0 {name=l39 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 440 -200 0 0 {name=l40 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 520 -200 2 0 {name=l41 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 600 -200 2 0 {name=l42 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 280 200 0 0 {name=l43 sig_type=std_logic lab=DN2}
C {lab_pin.sym} 280 220 0 0 {name=l44 sig_type=std_logic lab=DPB2}
C {lab_pin.sym} 360 300 0 0 {name=l45 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 440 300 0 0 {name=l46 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 520 300 2 0 {name=l47 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 600 300 2 0 {name=l48 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 760 -300 0 0 {name=l49 sig_type=std_logic lab=DP3}
C {lab_pin.sym} 760 -280 0 0 {name=l50 sig_type=std_logic lab=DNB3}
C {lab_pin.sym} 840 -200 0 0 {name=l51 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 920 -200 0 0 {name=l52 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 1000 -200 2 0 {name=l53 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 1080 -200 2 0 {name=l54 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 760 200 0 0 {name=l55 sig_type=std_logic lab=DN3}
C {lab_pin.sym} 760 220 0 0 {name=l56 sig_type=std_logic lab=DPB3}
C {lab_pin.sym} 840 300 0 0 {name=l57 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 920 300 0 0 {name=l58 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 1000 300 2 0 {name=l59 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 1080 300 2 0 {name=l60 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1240 -300 0 0 {name=l61 sig_type=std_logic lab=DP4}
C {lab_pin.sym} 1240 -280 0 0 {name=l62 sig_type=std_logic lab=DNB4}
C {lab_pin.sym} 1320 -200 0 0 {name=l63 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1400 -200 0 0 {name=l64 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 1480 -200 2 0 {name=l65 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 1560 -200 2 0 {name=l66 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1240 200 0 0 {name=l67 sig_type=std_logic lab=DN4}
C {lab_pin.sym} 1240 220 0 0 {name=l68 sig_type=std_logic lab=DPB4}
C {lab_pin.sym} 1320 300 0 0 {name=l69 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1400 300 0 0 {name=l70 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 1480 300 2 0 {name=l71 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 1560 300 2 0 {name=l72 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1720 -300 0 0 {name=l73 sig_type=std_logic lab=DP5}
C {lab_pin.sym} 1720 -280 0 0 {name=l74 sig_type=std_logic lab=DNB5}
C {lab_pin.sym} 1800 -200 0 0 {name=l75 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1880 -200 0 0 {name=l76 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 1960 -200 2 0 {name=l77 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 2040 -200 2 0 {name=l78 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1720 200 0 0 {name=l79 sig_type=std_logic lab=DN5}
C {lab_pin.sym} 1720 220 0 0 {name=l80 sig_type=std_logic lab=DPB5}
C {lab_pin.sym} 1800 300 0 0 {name=l81 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1880 300 0 0 {name=l82 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 1960 300 2 0 {name=l83 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 2040 300 2 0 {name=l84 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2200 -300 0 0 {name=l85 sig_type=std_logic lab=DP6}
C {lab_pin.sym} 2200 -280 0 0 {name=l86 sig_type=std_logic lab=DNB6}
C {lab_pin.sym} 2280 -200 0 0 {name=l87 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2360 -200 0 0 {name=l88 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 2440 -200 2 0 {name=l89 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 2520 -200 2 0 {name=l90 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2200 200 0 0 {name=l91 sig_type=std_logic lab=DN6}
C {lab_pin.sym} 2200 220 0 0 {name=l92 sig_type=std_logic lab=DPB6}
C {lab_pin.sym} 2280 300 0 0 {name=l93 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2360 300 0 0 {name=l94 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 2440 300 2 0 {name=l95 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 2520 300 2 0 {name=l96 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2680 -300 0 0 {name=l97 sig_type=std_logic lab=DP7}
C {lab_pin.sym} 2680 -280 0 0 {name=l98 sig_type=std_logic lab=DNB7}
C {lab_pin.sym} 2760 -200 0 0 {name=l99 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2840 -200 0 0 {name=l100 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 2920 -200 2 0 {name=l101 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 3000 -200 2 0 {name=l102 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2680 200 0 0 {name=l103 sig_type=std_logic lab=DN7}
C {lab_pin.sym} 2680 220 0 0 {name=l104 sig_type=std_logic lab=DPB7}
C {lab_pin.sym} 2760 300 0 0 {name=l105 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2840 300 0 0 {name=l106 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 2920 300 2 0 {name=l107 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 3000 300 2 0 {name=l108 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 3160 -300 0 0 {name=l109 sig_type=std_logic lab=DP8}
C {lab_pin.sym} 3160 -280 0 0 {name=l110 sig_type=std_logic lab=DNB8}
C {lab_pin.sym} 3240 -200 0 0 {name=l111 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 3320 -200 0 0 {name=l112 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 3400 -200 2 0 {name=l113 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 3480 -200 2 0 {name=l114 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 3160 200 0 0 {name=l115 sig_type=std_logic lab=DN8}
C {lab_pin.sym} 3160 220 0 0 {name=l116 sig_type=std_logic lab=DPB8}
C {lab_pin.sym} 3240 300 0 0 {name=l117 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 3320 300 0 0 {name=l118 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 3400 300 2 0 {name=l119 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 3480 300 2 0 {name=l120 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 3640 -300 0 0 {name=l121 sig_type=std_logic lab=DP9}
C {lab_pin.sym} 3640 -280 0 0 {name=l122 sig_type=std_logic lab=DNB9}
C {lab_pin.sym} 3720 -200 0 0 {name=l123 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 3800 -200 0 0 {name=l124 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 3880 -200 2 0 {name=l125 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 3960 -200 2 0 {name=l126 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 3760 300 0 0 {name=l127 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 3840 320 2 0 {name=l128 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 3920 300 2 0 {name=l129 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 4400 -300 2 0 {name=l130 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 4360 -120 0 0 {name=l131 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 4820 -180 0 0 {name=l132 sig_type=std_logic lab=CLK}
C {lab_pin.sym} 4820 -160 0 0 {name=l133 sig_type=std_logic lab=DEC10}
C {lab_pin.sym} 5020 -200 2 0 {name=l134 sig_type=std_logic lab=QP}
C {lab_pin.sym} 5020 -180 2 0 {name=l135 sig_type=std_logic lab=QN}
C {lab_pin.sym} 5020 -160 2 0 {name=l136 sig_type=std_logic lab=VALIDB}
C {lab_pin.sym} 5020 -140 2 0 {name=l137 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} 5020 -120 2 0 {name=l138 sig_type=std_logic lab=SAMP}
C {lab_pin.sym} 4920 -320 2 0 {name=l139 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 4920 0 2 0 {name=l140 sig_type=std_logic lab=VSS}
C {lab_pin.sym} -100 700 0 0 {name=l141 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} -100 720 0 0 {name=l142 sig_type=std_logic lab=QP}
C {lab_pin.sym} -100 740 0 0 {name=l143 sig_type=std_logic lab=QN}
C {lab_pin.sym} -100 760 0 0 {name=l144 sig_type=std_logic lab=VALIDB}
C {lab_pin.sym} -100 780 0 0 {name=l145 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} -100 800 0 0 {name=l146 sig_type=std_logic lab=EOC}
C {lab_pin.sym} 100 740 2 0 {name=l147 sig_type=std_logic lab=DP1}
C {lab_pin.sym} 100 760 2 0 {name=l148 sig_type=std_logic lab=DPB1}
C {lab_pin.sym} 100 780 2 0 {name=l149 sig_type=std_logic lab=DN1}
C {lab_pin.sym} 100 800 2 0 {name=l150 sig_type=std_logic lab=DNB1}
C {lab_pin.sym} 0 600 2 0 {name=l151 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 0 920 2 0 {name=l152 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 380 720 0 0 {name=l153 sig_type=std_logic lab=QP}
C {lab_pin.sym} 380 740 0 0 {name=l154 sig_type=std_logic lab=QN}
C {lab_pin.sym} 380 760 0 0 {name=l155 sig_type=std_logic lab=VALIDB}
C {lab_pin.sym} 380 780 0 0 {name=l156 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} 380 800 0 0 {name=l157 sig_type=std_logic lab=EOC}
C {lab_pin.sym} 580 740 2 0 {name=l158 sig_type=std_logic lab=DP2}
C {lab_pin.sym} 580 760 2 0 {name=l159 sig_type=std_logic lab=DPB2}
C {lab_pin.sym} 580 780 2 0 {name=l160 sig_type=std_logic lab=DN2}
C {lab_pin.sym} 580 800 2 0 {name=l161 sig_type=std_logic lab=DNB2}
C {lab_pin.sym} 480 600 2 0 {name=l162 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 480 920 2 0 {name=l163 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 860 720 0 0 {name=l164 sig_type=std_logic lab=QP}
C {lab_pin.sym} 860 740 0 0 {name=l165 sig_type=std_logic lab=QN}
C {lab_pin.sym} 860 760 0 0 {name=l166 sig_type=std_logic lab=VALIDB}
C {lab_pin.sym} 860 780 0 0 {name=l167 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} 860 800 0 0 {name=l168 sig_type=std_logic lab=EOC}
C {lab_pin.sym} 1060 740 2 0 {name=l169 sig_type=std_logic lab=DP3}
C {lab_pin.sym} 1060 760 2 0 {name=l170 sig_type=std_logic lab=DPB3}
C {lab_pin.sym} 1060 780 2 0 {name=l171 sig_type=std_logic lab=DN3}
C {lab_pin.sym} 1060 800 2 0 {name=l172 sig_type=std_logic lab=DNB3}
C {lab_pin.sym} 960 600 2 0 {name=l173 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 960 920 2 0 {name=l174 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1340 720 0 0 {name=l175 sig_type=std_logic lab=QP}
C {lab_pin.sym} 1340 740 0 0 {name=l176 sig_type=std_logic lab=QN}
C {lab_pin.sym} 1340 760 0 0 {name=l177 sig_type=std_logic lab=VALIDB}
C {lab_pin.sym} 1340 780 0 0 {name=l178 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} 1340 800 0 0 {name=l179 sig_type=std_logic lab=EOC}
C {lab_pin.sym} 1540 740 2 0 {name=l180 sig_type=std_logic lab=DP4}
C {lab_pin.sym} 1540 760 2 0 {name=l181 sig_type=std_logic lab=DPB4}
C {lab_pin.sym} 1540 780 2 0 {name=l182 sig_type=std_logic lab=DN4}
C {lab_pin.sym} 1540 800 2 0 {name=l183 sig_type=std_logic lab=DNB4}
C {lab_pin.sym} 1440 600 2 0 {name=l184 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1440 920 2 0 {name=l185 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1820 720 0 0 {name=l186 sig_type=std_logic lab=QP}
C {lab_pin.sym} 1820 740 0 0 {name=l187 sig_type=std_logic lab=QN}
C {lab_pin.sym} 1820 760 0 0 {name=l188 sig_type=std_logic lab=VALIDB}
C {lab_pin.sym} 1820 780 0 0 {name=l189 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} 1820 800 0 0 {name=l190 sig_type=std_logic lab=EOC}
C {lab_pin.sym} 2020 740 2 0 {name=l191 sig_type=std_logic lab=DP5}
C {lab_pin.sym} 2020 760 2 0 {name=l192 sig_type=std_logic lab=DPB5}
C {lab_pin.sym} 2020 780 2 0 {name=l193 sig_type=std_logic lab=DN5}
C {lab_pin.sym} 2020 800 2 0 {name=l194 sig_type=std_logic lab=DNB5}
C {lab_pin.sym} 1920 600 2 0 {name=l195 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1920 920 2 0 {name=l196 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2300 720 0 0 {name=l197 sig_type=std_logic lab=QP}
C {lab_pin.sym} 2300 740 0 0 {name=l198 sig_type=std_logic lab=QN}
C {lab_pin.sym} 2300 760 0 0 {name=l199 sig_type=std_logic lab=VALIDB}
C {lab_pin.sym} 2300 780 0 0 {name=l200 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} 2300 800 0 0 {name=l201 sig_type=std_logic lab=EOC}
C {lab_pin.sym} 2500 740 2 0 {name=l202 sig_type=std_logic lab=DP6}
C {lab_pin.sym} 2500 760 2 0 {name=l203 sig_type=std_logic lab=DPB6}
C {lab_pin.sym} 2500 780 2 0 {name=l204 sig_type=std_logic lab=DN6}
C {lab_pin.sym} 2500 800 2 0 {name=l205 sig_type=std_logic lab=DNB6}
C {lab_pin.sym} 2400 600 2 0 {name=l206 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2400 920 2 0 {name=l207 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 2780 720 0 0 {name=l208 sig_type=std_logic lab=QP}
C {lab_pin.sym} 2780 740 0 0 {name=l209 sig_type=std_logic lab=QN}
C {lab_pin.sym} 2780 760 0 0 {name=l210 sig_type=std_logic lab=VALIDB}
C {lab_pin.sym} 2780 780 0 0 {name=l211 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} 2780 800 0 0 {name=l212 sig_type=std_logic lab=EOC}
C {lab_pin.sym} 2980 740 2 0 {name=l213 sig_type=std_logic lab=DP7}
C {lab_pin.sym} 2980 760 2 0 {name=l214 sig_type=std_logic lab=DPB7}
C {lab_pin.sym} 2980 780 2 0 {name=l215 sig_type=std_logic lab=DN7}
C {lab_pin.sym} 2980 800 2 0 {name=l216 sig_type=std_logic lab=DNB7}
C {lab_pin.sym} 2880 600 2 0 {name=l217 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 2880 920 2 0 {name=l218 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 3260 720 0 0 {name=l219 sig_type=std_logic lab=QP}
C {lab_pin.sym} 3260 740 0 0 {name=l220 sig_type=std_logic lab=QN}
C {lab_pin.sym} 3260 760 0 0 {name=l221 sig_type=std_logic lab=VALIDB}
C {lab_pin.sym} 3260 780 0 0 {name=l222 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} 3260 800 0 0 {name=l223 sig_type=std_logic lab=EOC}
C {lab_pin.sym} 3460 740 2 0 {name=l224 sig_type=std_logic lab=DP8}
C {lab_pin.sym} 3460 760 2 0 {name=l225 sig_type=std_logic lab=DPB8}
C {lab_pin.sym} 3460 780 2 0 {name=l226 sig_type=std_logic lab=DN8}
C {lab_pin.sym} 3460 800 2 0 {name=l227 sig_type=std_logic lab=DNB8}
C {lab_pin.sym} 3360 600 2 0 {name=l228 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 3360 920 2 0 {name=l229 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 3740 720 0 0 {name=l230 sig_type=std_logic lab=QP}
C {lab_pin.sym} 3740 740 0 0 {name=l231 sig_type=std_logic lab=QN}
C {lab_pin.sym} 3740 760 0 0 {name=l232 sig_type=std_logic lab=VALIDB}
C {lab_pin.sym} 3740 780 0 0 {name=l233 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} 3740 800 0 0 {name=l234 sig_type=std_logic lab=EOC}
C {lab_pin.sym} 3940 740 2 0 {name=l235 sig_type=std_logic lab=DP9}
C {lab_pin.sym} 3940 760 2 0 {name=l236 sig_type=std_logic lab=DPB9}
C {lab_pin.sym} 3940 780 2 0 {name=l237 sig_type=std_logic lab=DN9}
C {lab_pin.sym} 3940 800 2 0 {name=l238 sig_type=std_logic lab=DNB9}
C {lab_pin.sym} 3840 600 2 0 {name=l239 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 3840 920 2 0 {name=l240 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 4220 720 0 0 {name=l241 sig_type=std_logic lab=QP}
C {lab_pin.sym} 4220 740 0 0 {name=l242 sig_type=std_logic lab=QN}
C {lab_pin.sym} 4220 760 0 0 {name=l243 sig_type=std_logic lab=VALIDB}
C {lab_pin.sym} 4220 780 0 0 {name=l244 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} 4220 800 0 0 {name=l245 sig_type=std_logic lab=EOC}
C {lab_pin.sym} 4420 720 2 0 {name=l246 sig_type=std_logic lab=DEC10}
C {lab_pin.sym} 4420 740 2 0 {name=l247 sig_type=std_logic lab=DP10}
C {lab_pin.sym} 4320 600 2 0 {name=l248 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 4320 920 2 0 {name=l249 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 1910 -440 0 0 {name=l250 sig_type=std_logic lab=TOPP}
C {lab_wire.sym} 1930 60 0 0 {name=l251 sig_type=std_logic lab=TOPN}
C {lab_wire.sym} 4660 -220 0 0 {name=l252 sig_type=std_logic lab=OUTP}
C {lab_wire.sym} 4710 -200 0 0 {name=l253 sig_type=std_logic lab=OUTN}
C {lab_wire.sym} 4750 60 0 0 {name=l254 sig_type=std_logic lab=CLKC}
C {lab_wire.sym} 240 700 0 0 {name=l255 sig_type=std_logic lab=T1}
C {lab_wire.sym} 720 700 0 0 {name=l256 sig_type=std_logic lab=T2}
C {lab_wire.sym} 1200 700 0 0 {name=l257 sig_type=std_logic lab=T3}
C {lab_wire.sym} 1680 700 0 0 {name=l258 sig_type=std_logic lab=T4}
C {lab_wire.sym} 2160 700 0 0 {name=l259 sig_type=std_logic lab=T5}
C {lab_wire.sym} 2640 700 0 0 {name=l260 sig_type=std_logic lab=T6}
C {lab_wire.sym} 3120 700 0 0 {name=l261 sig_type=std_logic lab=T7}
C {lab_wire.sym} 3600 700 0 0 {name=l262 sig_type=std_logic lab=T8}
C {lab_wire.sym} 4080 700 0 0 {name=l263 sig_type=std_logic lab=T9}
C {noconn.sym} 100 720 2 0 {name=nc264}
C {noconn.sym} 580 720 2 0 {name=nc265}
C {noconn.sym} 1060 720 2 0 {name=nc266}
C {noconn.sym} 1540 720 2 0 {name=nc267}
C {noconn.sym} 2020 720 2 0 {name=nc268}
C {noconn.sym} 2500 720 2 0 {name=nc269}
C {noconn.sym} 2980 720 2 0 {name=nc270}
C {noconn.sym} 3460 720 2 0 {name=nc271}
C {noconn.sym} 3940 720 2 0 {name=nc272}
C {noconn.sym} 4420 760 2 0 {name=nc273}
C {noconn.sym} 4420 780 2 0 {name=nc274}
C {noconn.sym} 4420 800 2 0 {name=nc275}
C {noconn.sym} 4420 700 2 0 {name=nc276}
C {sar10_boot.sym} -500 -440 0 0 {name=XBSP}
C {sar10_boot.sym} -500 60 0 0 {name=XBSN}
C {sar10_dac128.sym} 0 -300 0 0 {name=XDP1}
C {sar10_dac128.sym} 0 200 0 0 {name=XDN1}
C {sar10_dac64.sym} 480 -300 0 0 {name=XDP2}
C {sar10_dac64.sym} 480 200 0 0 {name=XDN2}
C {sar10_dac32.sym} 960 -300 0 0 {name=XDP3}
C {sar10_dac32.sym} 960 200 0 0 {name=XDN3}
C {sar10_dac16.sym} 1440 -300 0 0 {name=XDP4}
C {sar10_dac16.sym} 1440 200 0 0 {name=XDN4}
C {sar10_dac8.sym} 1920 -300 0 0 {name=XDP5}
C {sar10_dac8.sym} 1920 200 0 0 {name=XDN5}
C {sar10_dac4.sym} 2400 -300 0 0 {name=XDP6}
C {sar10_dac4.sym} 2400 200 0 0 {name=XDN6}
C {sar10_dac2.sym} 2880 -300 0 0 {name=XDP7}
C {sar10_dac2.sym} 2880 200 0 0 {name=XDN7}
C {sar10_dac1.sym} 3360 -300 0 0 {name=XDP8}
C {sar10_dac1.sym} 3360 200 0 0 {name=XDN8}
C {sar10_dac1.sym} 3840 -300 0 0 {name=XDP9}
C {sar10_dacdum.sym} 3840 200 0 0 {name=XDN9}
C {sar10_comp.sym} 4400 -200 0 0 {name=XCMP}
C {sar10_ctrl.sym} 4920 -160 0 0 {name=XCTL}
C {sar10_slice.sym} 0 760 0 0 {name=XS1}
C {sar10_slice.sym} 480 760 0 0 {name=XS2}
C {sar10_slice.sym} 960 760 0 0 {name=XS3}
C {sar10_slice.sym} 1440 760 0 0 {name=XS4}
C {sar10_slice.sym} 1920 760 0 0 {name=XS5}
C {sar10_slice.sym} 2400 760 0 0 {name=XS6}
C {sar10_slice.sym} 2880 760 0 0 {name=XS7}
C {sar10_slice.sym} 3360 760 0 0 {name=XS8}
C {sar10_slice.sym} 3840 760 0 0 {name=XS9}
C {sar10_slice.sym} 4320 760 0 0 {name=XS10}
