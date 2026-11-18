v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sar10_boot} -460 -400 0 0 0.7 0.7 {}
T {Bootstrapped NMOS sampling switch.
CK high (track): CB floats between VIN and G, so Vgs(MSW) = VDD for any input.
CK low (hold): G = 0, CB recharged to VDD through MP1 / MN1.} -460 -350 0 0 0.3 0.3 {}
N 0 30 0 60 {lab=BOT}
N 0 60 0 110 {lab=BOT}
N 0 60 80 60 {lab=BOT}
N 80 60 80 170 {lab=BOT}
N 80 170 200 170 {lab=BOT}
N 200 130 200 170 {lab=BOT}
N 200 170 210 170 {lab=BOT}
N 210 170 340 170 {lab=BOT}
N 340 130 340 170 {lab=BOT}
N 340 170 340 220 {lab=BOT}
N -460 -40 -380 -40 {lab=CK}
N -380 -100 -380 -40 {lab=CK}
N -380 -40 -380 20 {lab=CK}
N -380 20 -360 20 {lab=CK}
N -360 -100 -380 -100 {lab=CK}
N -320 -70 -320 -40 {lab=CKB}
N -320 -40 -320 -10 {lab=CKB}
N -320 -40 -260 -40 {lab=CKB}
N 500 -30 500 0 {lab=G}
N 500 0 640 0 {lab=G}
N 640 0 640 30 {lab=G}
N 640 0 760 0 {lab=G}
N 760 0 760 280 {lab=G}
N 640 90 640 120 {lab=GX}
N 640 120 640 150 {lab=GX}
N 0 -140 0 -110 {lab=TOP}
N 0 -110 0 -70 {lab=TOP}
N 0 -70 0 -30 {lab=TOP}
N 0 -70 100 -70 {lab=TOP}
N 100 -240 300 -240 {lab=TOP}
N 100 -70 100 -240 {lab=TOP}
N 300 -240 500 -240 {lab=TOP}
N 500 -240 500 -90 {lab=TOP}
N 500 -60 500 -90 {lab=TOP}
N -320 -130 -320 -150 {lab=VDD}
N -320 -100 -320 -130 {lab=VDD}
N 0 -170 0 -190 {lab=VDD}
N 200 -170 200 -190 {lab=VDD}
N 200 -140 200 -170 {lab=VDD}
N -460 320 340 320 {lab=VIN}
N 340 280 340 320 {lab=VIN}
N 340 320 730 320 {lab=VIN}
N 790 320 880 320 {lab=VOUT}
N -320 20 -320 50 {lab=VSS}
N -320 50 -320 70 {lab=VSS}
N 0 140 0 170 {lab=VSS}
N 0 170 0 190 {lab=VSS}
N 640 180 640 210 {lab=VSS}
N 640 210 640 230 {lab=VSS}
N 200 -110 200 -60 {lab=Z}
N 200 -60 200 40 {lab=Z}
N 200 40 200 70 {lab=Z}
N 330 -60 200 -60 {lab=Z}
N 340 40 200 40 {lab=Z}
N 340 70 340 40 {lab=Z}
N 460 -60 330 -60 {lab=Z}
C {ipin.sym} -460 -40 0 0 {name=p1 lab=CK}
C {ipin.sym} -460 320 0 0 {name=p2 lab=VIN}
C {opin.sym} 880 320 0 0 {name=p3 lab=VOUT}
C {iopin.sym} -460 -240 0 0 {name=p4 lab=VDD}
C {iopin.sym} -460 -210 0 0 {name=p5 lab=VSS}
C {lab_pin.sym} -260 -40 2 0 {name=l6 sig_type=std_logic lab=CKB}
C {lab_pin.sym} 760 0 2 0 {name=l7 sig_type=std_logic lab=G}
C {lab_pin.sym} -320 -150 2 0 {name=l8 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -320 70 2 0 {name=l9 sig_type=std_logic lab=VSS}
C {lab_pin.sym} -40 -140 0 0 {name=l10 sig_type=std_logic lab=G}
C {lab_pin.sym} 0 -190 2 0 {name=l11 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -40 140 0 0 {name=l12 sig_type=std_logic lab=CKB}
C {lab_pin.sym} 0 190 2 0 {name=l13 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 160 -140 0 0 {name=l14 sig_type=std_logic lab=CK}
C {lab_pin.sym} 200 -190 2 0 {name=l15 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 160 100 0 0 {name=l16 sig_type=std_logic lab=CK}
C {lab_pin.sym} 300 100 0 0 {name=l17 sig_type=std_logic lab=G}
C {lab_pin.sym} 300 250 0 0 {name=l18 sig_type=std_logic lab=G}
C {lab_pin.sym} 600 60 0 0 {name=l19 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 600 180 0 0 {name=l20 sig_type=std_logic lab=CKB}
C {lab_pin.sym} 640 230 2 0 {name=l21 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 300 -240 0 0 {name=l22 sig_type=std_logic lab=TOP}
C {lab_wire.sym} 210 170 0 0 {name=l23 sig_type=std_logic lab=BOT}
C {lab_wire.sym} 330 -60 0 0 {name=l24 sig_type=std_logic lab=Z}
C {lab_wire.sym} 640 120 0 0 {name=l25 sig_type=std_logic lab=GX}
C {sky130_fd_pr/pfet_01v8.sym} -340 -100 0 0 {name=MPI L=0.15 W=6 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} -340 20 0 0 {name=MNI L=0.15 W=3 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} -20 -140 0 0 {name=MP1 L=0.15 W=2 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/cap_mim_m3_1.sym} 0 0 0 0 {name=CB model=cap_mim_m3_1 W=9 L=9 MF=1 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} -20 140 0 0 {name=MN1 L=0.15 W=2 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 180 -140 0 0 {name=MP4 L=0.15 W=6 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8.sym} 180 100 0 0 {name=MN4 L=0.15 W=1 body=VSS nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8.sym} 320 100 0 0 {name=MN4B L=0.15 W=1 body=VSS nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 480 -60 0 0 {name=MP2 L=0.15 W=4 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8.sym} 320 250 0 0 {name=MN3 L=0.15 W=4 body=VSS nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8.sym} 620 60 0 0 {name=MN2A L=0.15 W=12 body=VSS nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 620 180 0 0 {name=MN2 L=0.15 W=12 nf=1 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8.sym} 760 300 1 0 {name=MSW L=0.15 W=5 body=VSS nf=2 mult=1 ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')" pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')" as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')" ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')" nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')" sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
