v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {tb_sar10} -840 -640 0 0 0.7 0.7 {}
T {Interactive testbench for sar10_adc: 50 ohm differential sine source, 20 MS/s sampling clock, ideal 1.8 V supply and reference.} -840 -590 0 0 0.3 0.3 {}
C {code_shown.sym} 380 -420 0 0 {name=SIM only_toplevel=false value="* sar10_adc bench: 16 conversions of a 4.0625 MHz sine at 20 MS/s (CLK high = sample).
* Netlist + Simulate from xschem.  Corner on the .lib line, temperature on .temp.
* For ENOB / corners / power use the flow instead:  python3 gen/flow.py fft --out sim/x --N 256 --M 31

.lib /foss/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice tt
.include /foss/pdks/sky130A/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice
.include /foss/pdks/sky130A/libs.ref/sky130_fd_pr/spice/sky130_fd_pr__cap_vpp_01p8x01p8_m1m2_noshield.model.spice
.temp 27
.option reltol=2e-4 abstol=1e-13 vntol=1e-7 chgtol=1e-16 method=gear klu rshunt=1e15
.save v(vip) v(vin) v(clk) v(eoc) v(b9) v(b8) v(b7) v(b6) v(b5) v(b4) v(b3) v(b2) v(b1) v(b0)
.save v(x1.topp) v(x1.topn) v(x1.clkc) v(x1.outp) v(x1.outn) i(vvdd) i(vrefp)
.tran 20p 851n 0 40p uic

.control
  run
  let msbs = 512*(v(b9) gt 0.9) + 256*(v(b8) gt 0.9) + 128*(v(b7) gt 0.9) + 64*(v(b6) gt 0.9) + 32*(v(b5) gt 0.9)
  let code = msbs + 16*(v(b4) gt 0.9) + 8*(v(b3) gt 0.9) + 4*(v(b2) gt 0.9) + 2*(v(b1) gt 0.9) + (v(b0) gt 0.9)
  let vd = v(vip) - v(vin)
  meas tran i_vdd AVG i(vvdd) FROM=51n TO=851n
  meas tran i_ref AVG i(vrefp) FROM=51n TO=851n
  let p_uw = -1.8e6*(i_vdd + i_ref)
  echo total power $&p_uw uW at 20 MS/s
  plot code
  plot vd v(eoc) v(clk)
  plot v(x1.topp) v(x1.topn) v(x1.clkc) xlimit 60n 80n
.endc
"}
N -40 180 -40 220 {lab=0}
N 40 180 40 220 {lab=0}
N -220 -60 -170 -60 {lab=CLK}
N -220 170 -220 -60 {lab=CLK}
N -170 -60 -120 -60 {lab=CLK}
N -470 -80 -300 -80 {lab=VIN}
N -300 -80 -120 -80 {lab=VIN}
N -840 -80 -720 -80 {lab=VINS}
N -840 170 -840 -80 {lab=VINS}
N -720 -80 -530 -80 {lab=VINS}
N -270 -100 -200 -100 {lab=VIP}
N -200 -100 -120 -100 {lab=VIP}
N -680 -100 -500 -100 {lab=VIPS}
N -680 170 -680 -100 {lab=VIPS}
N -500 -100 -330 -100 {lab=VIPS}
C {gnd.sym} -680 230 0 0 {name=l1 lab=0}
C {gnd.sym} -840 230 0 0 {name=l2 lab=0}
C {gnd.sym} -220 230 0 0 {name=l3 lab=0}
C {gnd.sym} -840 -330 0 0 {name=l4 lab=0}
C {gnd.sym} -640 -330 0 0 {name=l5 lab=0}
C {lab_pin.sym} -840 -390 2 0 {name=l6 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -640 -390 2 0 {name=l7 sig_type=std_logic lab=VREFP}
C {gnd.sym} -40 220 0 0 {name=l8 lab=0}
C {gnd.sym} 40 220 0 0 {name=l9 lab=0}
C {lab_pin.sym} 120 -100 2 0 {name=l10 sig_type=std_logic lab=B9}
C {lab_pin.sym} 120 -80 2 0 {name=l11 sig_type=std_logic lab=B8}
C {lab_pin.sym} 120 -60 2 0 {name=l12 sig_type=std_logic lab=B7}
C {lab_pin.sym} 120 -40 2 0 {name=l13 sig_type=std_logic lab=B6}
C {lab_pin.sym} 120 -20 2 0 {name=l14 sig_type=std_logic lab=B5}
C {lab_pin.sym} 120 0 2 0 {name=l15 sig_type=std_logic lab=B4}
C {lab_pin.sym} 120 20 2 0 {name=l16 sig_type=std_logic lab=B3}
C {lab_pin.sym} 120 40 2 0 {name=l17 sig_type=std_logic lab=B2}
C {lab_pin.sym} 120 60 2 0 {name=l18 sig_type=std_logic lab=B1}
C {lab_pin.sym} 120 80 2 0 {name=l19 sig_type=std_logic lab=B0}
C {lab_pin.sym} 120 100 2 0 {name=l20 sig_type=std_logic lab=EOC}
C {lab_pin.sym} -40 -180 0 0 {name=l21 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 40 -180 2 0 {name=l22 sig_type=std_logic lab=VREFP}
C {lab_wire.sym} -200 -100 0 0 {name=l23 sig_type=std_logic lab=VIP}
C {lab_wire.sym} -500 -100 0 0 {name=l24 sig_type=std_logic lab=VIPS}
C {lab_wire.sym} -300 -80 0 0 {name=l25 sig_type=std_logic lab=VIN}
C {lab_wire.sym} -720 -80 0 0 {name=l26 sig_type=std_logic lab=VINS}
C {lab_wire.sym} -170 -60 0 0 {name=l27 sig_type=std_logic lab=CLK}
C {sar10_adc.sym} 0 0 0 0 {name=x1}
C {devices/res.sym} -300 -100 1 0 {name=Rsp value=50 footprint=1206 device=resistor m=1}
C {devices/res.sym} -500 -80 1 0 {name=Rsn value=50 footprint=1206 device=resistor m=1}
C {devices/vsource.sym} -680 200 0 0 {name=Vsp value=\"SIN(0.9 0.85 4.0625e6)\" savecurrent=false}
C {devices/vsource.sym} -840 200 0 0 {name=Vsn value=\"SIN(0.9 -0.85 4.0625e6)\" savecurrent=false}
C {devices/vsource.sym} -220 200 0 0 {name=Vclk value=\"PULSE(0 1.8 1n 50p 50p 12.45n 50n)\" savecurrent=false}
C {devices/vsource.sym} -840 -360 0 0 {name=Vvdd value=1.8 savecurrent=true}
C {devices/vsource.sym} -640 -360 0 0 {name=Vrefp value=1.8 savecurrent=true}
