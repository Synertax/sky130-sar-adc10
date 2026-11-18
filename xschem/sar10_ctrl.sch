v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sar10_ctrl} -720 -580 0 0 0.7 0.7 {}
T {Asynchronous clock loop (sky130_fd_sc_hd cells).  VALID = comparator has decided.
CLKC falls as soon as VALID rises and rises again one delay-line time (XD1..XD2) after the comparator is back in reset:
that delay is the DAC settling time.  The loop stops when the last bit is decided (DECL) and during sampling (CLKS high).} -720 -530 0 0 0.3 0.3 {}
N 920 0 1060 0 {lab=CLKC}
N 800 0 820 0 {lab=CLKCB}
N 820 0 840 0 {lab=CLKCB}
N -720 -200 -640 -200 {lab=CLKS}
N -720 -140 300 -140 {lab=DECL}
N 300 -140 300 -120 {lab=DECL}
N 300 -120 320 -120 {lab=DECL}
N -80 0 -50 0 {lab=DL1}
N -50 0 -20 0 {lab=DL1}
N 920 180 1060 180 {lab=EOC}
N -720 -20 -600 -20 {lab=OUTN}
N -600 -100 -480 -100 {lab=OUTN}
N -600 -20 -600 -100 {lab=OUTN}
N -600 -20 -500 -20 {lab=OUTN}
N -720 20 -600 20 {lab=OUTP}
N -600 20 -600 100 {lab=OUTP}
N -600 20 -500 20 {lab=OUTP}
N -600 100 -480 100 {lab=OUTP}
N -400 100 1060 100 {lab=QN}
N -400 -100 1060 -100 {lab=QP}
N 60 -200 110 -200 {lab=RSTB}
N 110 -270 1060 -270 {lab=RSTB}
N 110 -200 110 -270 {lab=RSTB}
N 110 -200 160 -200 {lab=RSTB}
N 440 -140 540 -140 {lab=RUN}
N 540 -140 640 -140 {lab=RUN}
N 640 -140 640 -40 {lab=RUN}
N 640 -40 680 -40 {lab=RUN}
N -420 -200 -360 -200 {lab=SAMP}
N -360 -300 1060 -300 {lab=SAMP}
N -360 -200 -360 -300 {lab=SAMP}
N 240 -200 260 -200 {lab=SAMPD}
N 260 -200 280 -200 {lab=SAMPD}
N 280 -200 280 -160 {lab=SAMPD}
N 280 -160 320 -160 {lab=SAMPD}
N -560 -200 -530 -200 {lab=SB1}
N -530 -200 -500 -200 {lab=SB1}
N -380 0 -350 0 {lab=VALID}
N -350 0 -320 0 {lab=VALID}
N -240 0 -200 0 {lab=VALIDB}
N -200 0 -200 60 {lab=VALIDB}
N -200 0 -160 0 {lab=VALIDB}
N -200 60 660 60 {lab=VALIDB}
N 660 40 680 40 {lab=VALIDB}
N 660 60 660 40 {lab=VALIDB}
N 660 60 1060 60 {lab=VALIDB}
N 60 0 370 0 {lab=VD}
N 370 0 680 0 {lab=VD}
C {ipin.sym} -720 -200 0 0 {name=p1 lab=CLKS}
C {ipin.sym} -720 -140 0 0 {name=p2 lab=DECL}
C {ipin.sym} -720 -20 0 0 {name=p3 lab=OUTN}
C {ipin.sym} -720 20 0 0 {name=p4 lab=OUTP}
C {opin.sym} 1060 -300 0 0 {name=p5 lab=SAMP}
C {opin.sym} 1060 -270 0 0 {name=p6 lab=RSTB}
C {opin.sym} 1060 -100 0 0 {name=p7 lab=QP}
C {opin.sym} 1060 0 0 0 {name=p8 lab=CLKC}
C {opin.sym} 1060 60 0 0 {name=p9 lab=VALIDB}
C {opin.sym} 1060 100 0 0 {name=p10 lab=QN}
C {opin.sym} 1060 180 0 0 {name=p11 lab=EOC}
C {iopin.sym} -720 -400 0 0 {name=p12 lab=VDD}
C {iopin.sym} -720 -370 0 0 {name=p13 lab=VSS}
C {lab_pin.sym} -20 -200 0 0 {name=l14 sig_type=std_logic lab=CLKS}
C {lab_pin.sym} 840 180 0 0 {name=l15 sig_type=std_logic lab=DECL}
C {lab_wire.sym} -50 0 0 0 {name=l16 sig_type=std_logic lab=DL1}
C {lab_wire.sym} -530 -200 0 0 {name=l17 sig_type=std_logic lab=SB1}
C {lab_wire.sym} 260 -200 0 0 {name=l18 sig_type=std_logic lab=SAMPD}
C {lab_wire.sym} -350 0 0 0 {name=l19 sig_type=std_logic lab=VALID}
C {lab_wire.sym} 370 0 0 0 {name=l20 sig_type=std_logic lab=VD}
C {lab_wire.sym} 540 -140 0 0 {name=l21 sig_type=std_logic lab=RUN}
C {lab_wire.sym} 820 0 0 0 {name=l22 sig_type=std_logic lab=CLKCB}
C {sky130_stdcells/inv_1.sym} -600 -200 0 0 {name=xs1 VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_4.sym} -460 -200 0 0 {name=xs2 VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_4.sym} 20 -200 0 0 {name=xr3 VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 200 -200 0 0 {name=xsd VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nor2_1.sym} 380 -140 0 0 {name=xrun VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_4.sym} -440 -100 0 0 {name=xqp VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nand2_1.sym} -440 0 0 0 {name=xv VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_4.sym} -440 100 0 0 {name=xqn VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_4.sym} -280 0 0 0 {name=xvb VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} -120 0 0 0 {name=xd1 VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 20 0 0 0 {name=xd2 VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nand3_1.sym} 740 0 0 0 {name=xg VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_4.sym} 880 0 0 0 {name=xgb VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/buf_4.sym} 880 180 0 0 {name=xe VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
