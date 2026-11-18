v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sar10_slice} -520 -600 0 0 0.7 0.7 {}
T {SAR bit slice (all sky130_fd_sc_hd cells).  Window = TPREV & !T: inside it the comparator result sets the P latch (INP>INN) or the N latch.
Each latch is one AND-OR-invert gate (set | hold) plus a NOR with reset, so a decision reaches the CDAC switch through two gates:
LPB falls -> DP rises and, one inverter later, DPB falls.  DEC = bit decided.  The token T sets once DEC is high and the comparator is back in reset
(VALIDB high): this closes the window and opens the next slice.  B = DP registered at EOC.  RSTB low clears everything.} -520 -550 0 0 0.3 0.3 {}
N 990 -240 1060 -240 {lab=B}
N 280 -40 300 -40 {lab=DEC}
N 300 -100 300 -80 {lab=DEC}
N 300 -100 1060 -100 {lab=DEC}
N 300 -80 300 -40 {lab=DEC}
N 300 -80 340 -80 {lab=DEC}
N 300 -40 300 80 {lab=DEC}
N 300 80 560 80 {lab=DEC}
N 1060 140 1000 140 {lab=DN}
N 1060 240 1000 240 {lab=DNB}
N 1060 -160 1000 -160 {lab=DP}
N 1060 -120 1000 -120 {lab=DPB}
N -520 -320 780 -320 {lab=EOC}
N 780 -320 780 -240 {lab=EOC}
N 780 -240 810 -240 {lab=EOC}
N -520 120 -460 120 {lab=QN}
N -520 -240 -460 -240 {lab=QP}
N -520 -100 -460 -100 {lab=RSTB}
N 460 -40 500 -40 {lab=STB}
N 500 -80 530 -80 {lab=STB}
N 500 -40 500 -80 {lab=STB}
N 530 -80 560 -80 {lab=STB}
N 540 -10 540 40 {lab=T}
N 540 40 560 40 {lab=T}
N 680 -60 720 -60 {lab=T}
N 720 -60 720 -10 {lab=T}
N 720 -60 1060 -60 {lab=T}
N 720 -10 540 -10 {lab=T}
N 520 -40 560 -40 {lab=TB}
N 520 10 520 -40 {lab=TB}
N 680 60 720 60 {lab=TB}
N 720 10 520 10 {lab=TB}
N 720 60 720 10 {lab=TB}
N -520 -200 -460 -200 {lab=TPREV}
N -520 340 320 340 {lab=VALIDB}
N 320 -40 340 -40 {lab=VALIDB}
N 320 340 320 -40 {lab=VALIDB}
C {ipin.sym} -520 -240 0 0 {name=p1 lab=QP}
C {ipin.sym} -520 -200 0 0 {name=p2 lab=TPREV}
C {ipin.sym} -520 -100 0 0 {name=p3 lab=RSTB}
C {ipin.sym} -520 120 0 0 {name=p4 lab=QN}
C {ipin.sym} -520 340 0 0 {name=p5 lab=VALIDB}
C {ipin.sym} -520 -320 0 0 {name=p6 lab=EOC}
C {opin.sym} 1060 -240 0 0 {name=p7 lab=B}
C {opin.sym} 1060 -160 0 0 {name=p8 lab=DP}
C {opin.sym} 1060 -120 0 0 {name=p9 lab=DPB}
C {opin.sym} 1060 -100 0 0 {name=p10 lab=DEC}
C {opin.sym} 1060 -60 0 0 {name=p11 lab=T}
C {opin.sym} 1060 140 0 0 {name=p12 lab=DN}
C {opin.sym} 1060 240 0 0 {name=p13 lab=DNB}
C {iopin.sym} -520 -420 0 0 {name=p14 lab=VDD}
C {iopin.sym} -520 -390 0 0 {name=p15 lab=VSS}
C {lab_pin.sym} -460 -240 0 0 {name=l16 sig_type=std_logic lab=QP}
C {lab_pin.sym} -460 -200 0 0 {name=l17 sig_type=std_logic lab=TPREV}
C {lab_pin.sym} -460 -100 0 0 {name=l18 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} -460 120 0 0 {name=l19 sig_type=std_logic lab=QN}
C {lab_pin.sym} 1000 -160 0 0 {name=l20 sig_type=std_logic lab=DP}
C {lab_pin.sym} 1000 -120 0 0 {name=l21 sig_type=std_logic lab=DPB}
C {lab_pin.sym} 1000 140 0 0 {name=l22 sig_type=std_logic lab=DN}
C {lab_pin.sym} 1000 240 0 0 {name=l23 sig_type=std_logic lab=DNB}
C {lab_pin.sym} 720 60 2 0 {name=l24 sig_type=std_logic lab=TB}
C {lab_pin.sym} -340 -260 0 0 {name=l25 sig_type=std_logic lab=QP}
C {lab_pin.sym} -340 -220 0 0 {name=l26 sig_type=std_logic lab=TPREV}
C {lab_pin.sym} -340 -180 0 0 {name=l27 sig_type=std_logic lab=TB}
C {lab_pin.sym} -340 -140 0 0 {name=l28 sig_type=std_logic lab=LP}
C {lab_pin.sym} -180 -200 2 0 {name=l29 sig_type=std_logic lab=LPB}
C {lab_pin.sym} -80 -220 0 0 {name=l30 sig_type=std_logic lab=LPB}
C {lab_pin.sym} -80 -180 0 0 {name=l31 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} 40 -200 2 0 {name=l32 sig_type=std_logic lab=LP}
C {lab_pin.sym} -340 140 0 0 {name=l33 sig_type=std_logic lab=QN}
C {lab_pin.sym} -340 180 0 0 {name=l34 sig_type=std_logic lab=TPREV}
C {lab_pin.sym} -340 220 0 0 {name=l35 sig_type=std_logic lab=TB}
C {lab_pin.sym} -340 260 0 0 {name=l36 sig_type=std_logic lab=LN}
C {lab_pin.sym} -180 200 2 0 {name=l37 sig_type=std_logic lab=LNB}
C {lab_pin.sym} -80 180 0 0 {name=l38 sig_type=std_logic lab=LNB}
C {lab_pin.sym} -80 220 0 0 {name=l39 sig_type=std_logic lab=RSTB}
C {lab_pin.sym} 40 200 2 0 {name=l40 sig_type=std_logic lab=LN}
C {lab_pin.sym} 160 -60 0 0 {name=l41 sig_type=std_logic lab=LPB}
C {lab_pin.sym} 160 -20 0 0 {name=l42 sig_type=std_logic lab=LNB}
C {lab_pin.sym} 340 0 0 0 {name=l43 sig_type=std_logic lab=TB}
C {lab_pin.sym} 810 -220 0 0 {name=l44 sig_type=std_logic lab=LP}
C {lab_pin.sym} -300 480 0 0 {name=l45 sig_type=std_logic lab=LPB}
C {lab_pin.sym} -220 480 2 0 {name=l46 sig_type=std_logic lab=DP}
C {lab_pin.sym} -120 480 0 0 {name=l47 sig_type=std_logic lab=LPB}
C {lab_pin.sym} -40 480 2 0 {name=l48 sig_type=std_logic lab=ADPB}
C {lab_pin.sym} 40 480 0 0 {name=l49 sig_type=std_logic lab=ADPB}
C {lab_pin.sym} 120 480 2 0 {name=l50 sig_type=std_logic lab=DPB}
C {lab_pin.sym} 260 480 0 0 {name=l51 sig_type=std_logic lab=LNB}
C {lab_pin.sym} 340 480 2 0 {name=l52 sig_type=std_logic lab=DN}
C {lab_pin.sym} 440 480 0 0 {name=l53 sig_type=std_logic lab=LNB}
C {lab_pin.sym} 520 480 2 0 {name=l54 sig_type=std_logic lab=ADNB}
C {lab_pin.sym} 600 480 0 0 {name=l55 sig_type=std_logic lab=ADNB}
C {lab_pin.sym} 680 480 2 0 {name=l56 sig_type=std_logic lab=DNB}
C {lab_wire.sym} 530 -80 0 0 {name=l57 sig_type=std_logic lab=STB}
C {sky130_stdcells/a31oi_1.sym} -260 -200 0 0 {name=xlpb VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nor2b_1.sym} -20 -200 0 0 {name=xlp VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/a31oi_1.sym} -260 200 0 0 {name=xlnb VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nor2b_1.sym} -20 200 0 0 {name=xln VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nand2_1.sym} 220 -40 0 0 {name=xdec VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nand3_1.sym} 400 -40 0 0 {name=xst VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nand2_1.sym} 620 -60 0 0 {name=xt VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nand2_1.sym} 620 60 0 0 {name=xtb VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/dfxtp_1.sym} 900 -230 0 0 {name=xb VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_4.sym} -260 480 0 0 {name=xgdp VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} -80 480 0 0 {name=xadpb VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_4.sym} 80 480 0 0 {name=xgdpb VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_4.sym} 300 480 0 0 {name=xgdn VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 480 480 0 0 {name=xadnb VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_4.sym} 640 480 0 0 {name=xgdnb VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
