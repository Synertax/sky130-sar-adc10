v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sar10_dac32} -160 -470 0 0 0.7 0.7 {}
T {CDAC cell: 2 x 32 unit capacitors (cap_vpp_01p8x01p8_m1m2_noshield, 0.78 fF each), each half with its reference switch (inverter between VREFP and VREFN).
The two pre-driver stages sit in the bit slice, next to the latch, so the long wire is driven by a strong gate.
Rest state (DH=0, DL=1): BH = VREFP, BL = VREFN.  DH=1 pulls TOP down, DL=0 pushes TOP up.} -160 -420 0 0 0.3 0.3 {}
N 340 -190 340 -160 {lab=BH}
N 340 -160 340 -130 {lab=BH}
N 340 -160 420 -160 {lab=BH}
N 420 -160 500 -160 {lab=BH}
N 340 130 340 160 {lab=BL}
N 340 160 340 190 {lab=BL}
N 340 160 420 160 {lab=BL}
N 420 160 500 160 {lab=BL}
N -160 -160 280 -160 {lab=DH}
N 280 -220 280 -160 {lab=DH}
N 280 -160 280 -100 {lab=DH}
N 280 -100 300 -100 {lab=DH}
N 300 -220 280 -220 {lab=DH}
N -160 160 280 160 {lab=DL}
N 280 100 280 160 {lab=DL}
N 280 160 280 220 {lab=DL}
N 280 220 300 220 {lab=DL}
N 300 100 280 100 {lab=DL}
N 500 -100 500 0 {lab=TOP}
N 500 0 500 100 {lab=TOP}
N 500 0 620 0 {lab=TOP}
N 340 -100 340 -70 {lab=VREFN}
N 340 -70 340 -50 {lab=VREFN}
N 340 220 340 250 {lab=VREFN}
N 340 250 340 270 {lab=VREFN}
N 340 -250 340 -270 {lab=VREFP}
N 340 -220 340 -250 {lab=VREFP}
N 340 70 340 50 {lab=VREFP}
N 340 100 340 70 {lab=VREFP}
C {ipin.sym} -160 -160 0 0 {name=p1 lab=DH}
C {ipin.sym} -160 160 0 0 {name=p2 lab=DL}
C {iopin.sym} 620 0 0 0 {name=p3 lab=TOP}
C {iopin.sym} -160 -330 0 0 {name=p4 lab=VDD}
C {iopin.sym} -160 -300 0 0 {name=p5 lab=VREFP}
C {iopin.sym} -160 300 0 0 {name=p6 lab=VREFN}
C {iopin.sym} -160 330 0 0 {name=p7 lab=VSS}
C {lab_pin.sym} 340 -270 2 0 {name=l8 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 340 -50 2 0 {name=l9 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 340 50 2 0 {name=l10 sig_type=std_logic lab=VREFP}
C {lab_pin.sym} 340 270 2 0 {name=l11 sig_type=std_logic lab=VREFN}
C {lab_pin.sym} 480 -120 0 0 {name=l12 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 520 120 2 0 {name=l13 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 420 -160 0 0 {name=l14 sig_type=std_logic lab=BH}
C {lab_wire.sym} 420 160 0 0 {name=l15 sig_type=std_logic lab=BL}
C {sky130_fd_pr/pfet_01v8.sym} 320 -220 0 0 {name=MP3H L=0.15 W=3.6 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 320 -100 0 0 {name=MN3H L=0.15 W=1.44 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 320 100 0 0 {name=MP3L L=0.15 W=3.6 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 320 220 0 0 {name=MN3L L=0.15 W=1.44 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/vpp_cap.sym} 500 -130 0 0 {name=CH model=cap_vpp_01p8x01p8_m1m2_noshield mult=32 spiceprefix=X}
C {sky130_fd_pr/vpp_cap.sym} 500 130 2 0 {name=CL model=cap_vpp_01p8x01p8_m1m2_noshield mult=32 spiceprefix=X}
