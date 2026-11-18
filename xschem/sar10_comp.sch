v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sar10_comp} -560 -400 0 0 0.7 0.7 {}
T {StrongARM latch comparator. CLK low: OUTP, OUTN, XP, XN precharged to VDD (reset).
CLK high: evaluate. INP > INN -> OUTN falls, OUTP stays high.} -560 -350 0 0 0.3 0.3 {}
N -140 320 -40 320 {lab=CLK}
N 320 180 220 180 {lab=INN}
N -320 180 -220 180 {lab=INP}
N -340 -90 -340 -80 {lab=OUTN}
N -340 -80 -180 -80 {lab=OUTN}
N -180 -90 -180 -80 {lab=OUTN}
N -180 -80 -180 -60 {lab=OUTN}
N -180 -60 -180 10 {lab=OUTN}
N -180 -60 100 -60 {lab=OUTN}
N 100 -120 100 -60 {lab=OUTN}
N 100 -60 100 40 {lab=OUTN}
N 100 -60 460 -60 {lab=OUTN}
N 100 40 140 40 {lab=OUTN}
N 140 -120 100 -120 {lab=OUTN}
N -140 -120 -100 -120 {lab=OUTP}
N -100 -120 -100 -20 {lab=OUTP}
N -100 -20 -100 40 {lab=OUTP}
N -100 -20 180 -20 {lab=OUTP}
N -100 40 -140 40 {lab=OUTP}
N 180 -90 180 -80 {lab=OUTP}
N 180 -80 180 -20 {lab=OUTP}
N 180 -20 180 10 {lab=OUTP}
N 180 -20 460 -20 {lab=OUTP}
N 340 -90 340 -80 {lab=OUTP}
N 340 -80 180 -80 {lab=OUTP}
N -180 210 -180 250 {lab=TAIL}
N -180 250 0 250 {lab=TAIL}
N 0 250 0 290 {lab=TAIL}
N 0 250 60 250 {lab=TAIL}
N 60 250 0 250 {lab=TAIL}
N 60 250 180 250 {lab=TAIL}
N 60 290 60 250 {lab=TAIL}
N 180 250 180 210 {lab=TAIL}
N -340 -150 -340 -170 {lab=VDD}
N -340 -120 -340 -150 {lab=VDD}
N -340 30 -340 10 {lab=VDD}
N -340 60 -340 30 {lab=VDD}
N -180 -150 -180 -170 {lab=VDD}
N -180 -120 -180 -150 {lab=VDD}
N 180 -150 180 -170 {lab=VDD}
N 180 -120 180 -150 {lab=VDD}
N 340 -150 340 -170 {lab=VDD}
N 340 -120 340 -150 {lab=VDD}
N 340 30 340 10 {lab=VDD}
N 340 60 340 30 {lab=VDD}
N 0 320 0 350 {lab=VSS}
N 0 350 0 370 {lab=VSS}
N 60 320 60 350 {lab=VSS}
N 60 350 60 370 {lab=VSS}
N -340 90 -340 110 {lab=XN}
N -340 110 -260 110 {lab=XN}
N -260 110 -180 110 {lab=XN}
N -180 70 -180 110 {lab=XN}
N -180 110 -180 150 {lab=XN}
N 180 70 180 110 {lab=XP}
N 180 110 180 150 {lab=XP}
N 260 110 180 110 {lab=XP}
N 340 90 340 110 {lab=XP}
N 340 110 260 110 {lab=XP}
C {ipin.sym} -320 180 0 0 {name=p1 lab=INP}
C {ipin.sym} 320 180 0 1 {name=p2 lab=INN}
C {ipin.sym} -140 320 0 0 {name=p3 lab=CLK}
C {opin.sym} 460 -20 0 0 {name=p4 lab=OUTP}
C {opin.sym} 460 -60 0 0 {name=p5 lab=OUTN}
C {iopin.sym} -560 -240 0 0 {name=p6 lab=VDD}
C {iopin.sym} -560 -210 0 0 {name=p7 lab=VSS}
C {lab_pin.sym} 0 370 2 0 {name=l8 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 100 320 2 0 {name=l9 sig_type=std_logic lab=CLK}
C {lab_pin.sym} 60 370 0 0 {name=l10 sig_type=std_logic lab=VSS}
C {lab_pin.sym} -180 -170 0 0 {name=l11 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 180 -170 2 0 {name=l12 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -380 -120 0 0 {name=l13 sig_type=std_logic lab=CLK}
C {lab_pin.sym} -340 -170 2 0 {name=l14 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 380 -120 2 0 {name=l15 sig_type=std_logic lab=CLK}
C {lab_pin.sym} 340 -170 0 0 {name=l16 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -380 60 0 0 {name=l17 sig_type=std_logic lab=CLK}
C {lab_pin.sym} -340 10 2 0 {name=l18 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 380 60 2 0 {name=l19 sig_type=std_logic lab=CLK}
C {lab_pin.sym} 340 10 0 0 {name=l20 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 0 250 0 0 {name=l21 sig_type=std_logic lab=TAIL}
C {lab_wire.sym} -260 110 0 0 {name=l22 sig_type=std_logic lab=XN}
C {lab_wire.sym} 260 110 0 0 {name=l23 sig_type=std_logic lab=XP}
C {sky130_fd_pr/nfet_01v8.sym} -20 320 0 0 {name=M0 L=0.15 W=2 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 80 320 0 1 {name=M0B L=0.15 W=2 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8.sym} -200 180 0 0 {name=M1 L=0.15 W=4 body=VSS nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8.sym} 200 180 0 1 {name=M2 L=0.15 W=4 body=VSS nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8.sym} -160 40 0 1 {name=M3 L=0.15 W=2 body=VSS nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8.sym} 160 40 0 0 {name=M4 L=0.15 W=2 body=VSS nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} -160 -120 0 1 {name=M5 L=0.15 W=2 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 160 -120 0 0 {name=M6 L=0.15 W=2 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} -360 -120 0 0 {name=M7 L=0.15 W=1 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 360 -120 0 1 {name=M8 L=0.15 W=1 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} -360 60 0 0 {name=M9 L=0.15 W=1 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 360 60 0 1 {name=M10 L=0.15 W=1 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
