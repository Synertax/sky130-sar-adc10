v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sar10_dacdum} -160 -300 0 0 0.7 0.7 {}
T {Static dummy pair: 1 unit to VREFP + 1 unit to VREFN.
Balances the single-sided LSB cell on the other top plate.} -160 -250 0 0 0.3 0.3 {}
N 0 -40 0 0 {lab=TOP}
N 0 0 0 40 {lab=TOP}
N 0 0 140 0 {lab=TOP}
N 0 100 0 130 {lab=VREFN}
N 0 -100 0 -130 {lab=VREFP}
C {iopin.sym} 140 0 0 0 {name=p1 lab=TOP}
C {iopin.sym} 0 -130 0 0 {name=p2 lab=VREFP}
C {iopin.sym} 0 130 0 0 {name=p3 lab=VREFN}
C {iopin.sym} -160 130 0 0 {name=p4 lab=VSS}
C {lab_pin.sym} -20 -60 0 0 {name=l5 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 20 60 2 0 {name=l6 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/vpp_cap.sym} 0 -70 0 0 {name=CH model=cap_vpp_01p8x01p8_m1m2_noshield mult=1 spiceprefix=X}
C {sky130_fd_pr/vpp_cap.sym} 0 70 2 0 {name=CL model=cap_vpp_01p8x01p8_m1m2_noshield mult=1 spiceprefix=X}
