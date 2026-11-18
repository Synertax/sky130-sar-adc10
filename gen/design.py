"""10-bit asynchronous SAR ADC, sky130A - single source of truth.
Every cell is described once here (devices + nets + drawing); netlist.py / draw.py emit
a reference SPICE netlist and xschem .sch/.sym files from this description."""
import math

P = dict(  # ---- tunable design parameters -------------------------------------
    NBIT=10,
    UNITCAP='cap_vpp_01p8x01p8_m1m2_noshield',
    # comparator (StrongARM)
    W_IN=4.0, W_TAIL=4.0, W_LN=2.0, W_LP=2.0, W_RST=1.0, L_IN=0.15,
    # bootstrapped switch
    W_SW=5.0, CB_W=9.0, CB_L=9.0, W_DIS=12.0, W_Z=6.0, W_CKI=6.0, W_P2=4.0, W_N3=4.0,
    # CDAC driver: final-stage nmos width per unit cap, limits
    DRV_WN_PER_UNIT=0.045, DRV_WN_MIN=0.42, DRV_PN=2.5, DRV_PRE=3.0,
    # async loop delay (number of inverter pairs in the DAC-settling delay line)
    NDLY=1,
    PRE_CELL='inv_4',      # second pre-driver stage of every CDAC switch (in the slice)
)


class Inst:
    def __init__(s, kind, name, conn, **kw):
        s.kind, s.name, s.conn, s.kw = kind, name, conn, kw
        s.x = s.y = 0
        s.flip = 0
        s.rot = 0


class Cell:
    def __init__(s, name, pins, doc=''):
        s.name, s.pins, s.doc = name, pins, doc  # pins: [(name, dir, side)]
        s.insts = []
        s.wires = []     # (net, [points])  point = (x,y) | 'INST.PIN' | 'port:NAME' | 'h' | 'v'
        s.labels = []    # (net, point, rot)
        s.texts = []     # (text, x, y, size)
        s.portspec = []  # (name, x, y, flip)
        s.ncspec = []
        s.symshape = 'box'

    def _add(s, i, at):
        if at:
            i.x, i.y = at[0], at[1]
            i.flip = at[2] if len(at) > 2 else 0
            i.rot = at[3] if len(at) > 3 else 0
        s.insts.append(i)
        return i

    def mos(s, name, model, d, g, src, b, W, L=0.15, nf=1, at=None):
        return s._add(Inst('mos', name, dict(D=d, G=g, S=src, B=b), model=model, W=W, L=L, nf=nf), at)

    def vpp(s, name, c0, c1, b, mult, at=None):
        return s._add(Inst('vpp', name, dict(c0=c0, c1=c1, b=b), mult=mult), at)

    def mim(s, name, c0, c1, W, L, at=None):
        return s._add(Inst('mim', name, dict(c0=c0, c1=c1), W=W, L=L), at)

    def std(s, name, cell, at=None, **conn):
        return s._add(Inst('std', name, conn, cell=cell), at)

    def sub(s, name, cell, at=None, **conn):
        return s._add(Inst('sub', name, conn, cell=cell), at)

    def dev(s, name, dev, attrs, at=None, **conn):
        return s._add(Inst('dev', name, conn, dev=dev, attrs=attrs), at)

    def w(s, net, *pts):
        s.wires.append((net, list(pts)))

    def lab(s, net, p, rot=0, kind='lab_pin'):
        s.labels.append((net, p, rot, kind))

    def gnd(s, p):
        s.labels.append(('0', p, 0, 'gnd'))

    def port(s, name, x, y, flip=0):
        s.portspec.append((name, x, y, flip))

    def nc(s, p):
        s.ncspec.append(p)

    def text(s, t, x, y, sz=0.4):
        s.texts.append((t, x, y, sz))

    def title(s, x, y):
        s.text(s.name, x, y, 0.7)
        s.text(s.doc, x, y + 50, 0.3)


def r2(x):
    return round(x * 100) / 100.0


def nfing(W, wmax=5.0):
    return max(1, int(math.ceil(W / wmax - 1e-9)))


CELLS = {}


def reg(c):
    CELLS[c.name] = c
    return c


# =============================================================== comparator
def comparator():
    p = P
    c = reg(Cell('sar10_comp', [('INP', 'in', 'L'), ('INN', 'in', 'L'), ('CLK', 'in', 'B'),
                                ('OUTP', 'out', 'R'), ('OUTN', 'out', 'R'), ('VDD', 'inout', 'T'), ('VSS', 'inout', 'B')],
                 'StrongARM latch comparator. CLK low: OUTP, OUTN, XP, XN precharged to VDD (reset).\n'
                 'CLK high: evaluate. INP > INN -> OUTN falls, OUTP stays high.'))
    c.symshape = 'comp'
    c.mos('M0', 'nfet_01v8', 'TAIL', 'CLK', 'VSS', 'VSS', r2(p['W_TAIL'] / 2), at=(-20, 320))      # tail split in two halves:
    c.mos('M0B', 'nfet_01v8', 'TAIL', 'CLK', 'VSS', 'VSS', r2(p['W_TAIL'] / 2), at=(80, 320, 1))   # mirror-symmetric layout
    c.mos('M1', 'nfet_01v8', 'XN', 'INP', 'TAIL', 'VSS', p['W_IN'], p['L_IN'], at=(-200, 180))
    c.mos('M2', 'nfet_01v8', 'XP', 'INN', 'TAIL', 'VSS', p['W_IN'], p['L_IN'], at=(200, 180, 1))
    c.mos('M3', 'nfet_01v8', 'OUTN', 'OUTP', 'XN', 'VSS', p['W_LN'], at=(-160, 40, 1))
    c.mos('M4', 'nfet_01v8', 'OUTP', 'OUTN', 'XP', 'VSS', p['W_LN'], at=(160, 40))
    c.mos('M5', 'pfet_01v8', 'OUTN', 'OUTP', 'VDD', 'VDD', p['W_LP'], at=(-160, -120, 1))
    c.mos('M6', 'pfet_01v8', 'OUTP', 'OUTN', 'VDD', 'VDD', p['W_LP'], at=(160, -120))
    c.mos('M7', 'pfet_01v8', 'OUTN', 'CLK', 'VDD', 'VDD', p['W_RST'], at=(-360, -120))
    c.mos('M8', 'pfet_01v8', 'OUTP', 'CLK', 'VDD', 'VDD', p['W_RST'], at=(360, -120, 1))
    c.mos('M9', 'pfet_01v8', 'XN', 'CLK', 'VDD', 'VDD', p['W_RST'], at=(-360, 60))
    c.mos('M10', 'pfet_01v8', 'XP', 'CLK', 'VDD', 'VDD', p['W_RST'], at=(360, 60, 1))
    c.port('INP', -320, 180); c.port('INN', 320, 180, 1); c.port('CLK', -140, 320)
    c.port('OUTP', 460, -20); c.port('OUTN', 460, -60)
    c.port('VDD', -560, -240); c.port('VSS', -560, -210)
    c.w('INP', 'port:INP', 'M1.G'); c.w('INN', 'port:INN', 'M2.G'); c.w('CLK', 'port:CLK', 'M0.G')
    c.w('TAIL', 'M1.S', (-180, 250), (180, 250), 'M2.S'); c.w('TAIL', (0, 250), 'M0.D'); c.w('TAIL', 'M0B.D', 'v', (0, 250))
    c.w('XN', 'M3.S', 'M1.D'); c.w('XN', 'M9.D', (-340, 110), (-180, 110))
    c.w('XP', 'M4.S', 'M2.D'); c.w('XP', 'M10.D', (340, 110), (180, 110))
    c.w('OUTN', 'M5.D', 'M3.D'); c.w('OUTN', 'M7.D', (-340, -80), (-180, -80))
    c.w('OUTN', (-180, -60), (100, -60)); c.w('OUTN', (100, -60), 'port:OUTN')
    c.w('OUTN', 'M6.G', (100, -120), (100, 40), 'M4.G')
    c.w('OUTP', 'M6.D', 'M4.D'); c.w('OUTP', 'M8.D', (340, -80), (180, -80))
    c.w('OUTP', (-100, -20), (180, -20)); c.w('OUTP', (180, -20), 'port:OUTP')
    c.w('OUTP', 'M5.G', (-100, -120), (-100, 40), 'M3.G')
    c.title(-560, -400)
    return c


# =============================================================== bootstrapped switch
def boot():
    p = P
    c = reg(Cell('sar10_boot', [('VIN', 'in', 'L'), ('VOUT', 'out', 'R'), ('VDD', 'inout', 'T'),
                                ('CK', 'in', 'B'), ('VSS', 'inout', 'B')],
                 'Bootstrapped NMOS sampling switch.\n'
                 'CK high (track): CB floats between VIN and G, so Vgs(MSW) = VDD for any input.\n'
                 'CK low (hold): G = 0, CB recharged to VDD through MP1 / MN1.'))
    c.symshape = 'switch'
    c.mos('MPI', 'pfet_01v8', 'CKB', 'CK', 'VDD', 'VDD', p['W_CKI'], at=(-340, -100))
    c.mos('MNI', 'nfet_01v8', 'CKB', 'CK', 'VSS', 'VSS', r2(p['W_CKI'] / 2), at=(-340, 20))
    c.mos('MP1', 'pfet_01v8', 'TOP', 'G', 'VDD', 'TOP', 2.0, at=(-20, -140))
    c.mim('CB', 'TOP', 'BOT', p['CB_W'], p['CB_L'], at=(0, 0))
    c.mos('MN1', 'nfet_01v8', 'BOT', 'CKB', 'VSS', 'VSS', 2.0, at=(-20, 140))
    c.mos('MP4', 'pfet_01v8', 'Z', 'CK', 'VDD', 'VDD', p['W_Z'], at=(180, -140))
    c.mos('MN4', 'nfet_01v8', 'Z', 'CK', 'BOT', 'VSS', 1.0, at=(180, 100))
    c.mos('MN4B', 'nfet_01v8', 'Z', 'G', 'BOT', 'VSS', 1.0, at=(320, 100))
    c.mos('MP2', 'pfet_01v8', 'G', 'Z', 'TOP', 'TOP', p['W_P2'], at=(480, -60))
    c.mos('MN3', 'nfet_01v8', 'BOT', 'G', 'VIN', 'VSS', p['W_N3'], at=(320, 250))
    c.mos('MN2A', 'nfet_01v8', 'G', 'VDD', 'GX', 'VSS', p['W_DIS'], at=(620, 60))
    c.mos('MN2', 'nfet_01v8', 'GX', 'CKB', 'VSS', 'VSS', p['W_DIS'], at=(620, 180))
    c.mos('MSW', 'nfet_01v8', 'VOUT', 'G', 'VIN', 'VSS', p['W_SW'], nf=nfing(p['W_SW'], 4.0), at=(760, 300, 0, 1))
    c.port('CK', -460, -40); c.port('VIN', -460, 320); c.port('VOUT', 880, 320)
    c.port('VDD', -460, -240); c.port('VSS', -460, -210)
    c.w('CK', 'port:CK', (-380, -40)); c.w('CK', 'MPI.G', (-380, -100), (-380, 20), 'MNI.G')
    c.w('CKB', 'MPI.D', 'MNI.D'); c.w('CKB', (-320, -40), (-260, -40)); c.lab('CKB', (-260, -40), 2)
    c.w('TOP', 'MP1.D', 'CB.c0'); c.w('TOP', (0, -70), (100, -70), (100, -240), (500, -240), 'MP2.S')
    c.w('BOT', 'CB.c1', 'MN1.D'); c.w('BOT', (0, 60), (80, 60), (80, 170), (340, 170))
    c.w('BOT', 'MN4.S', (200, 170)); c.w('BOT', 'MN4B.S', 'MN3.D')
    c.w('Z', 'MP4.D', 'MN4.D'); c.w('Z', 'MP2.G', (200, -60)); c.w('Z', 'MN4B.D', (340, 40), (200, 40))
    c.w('VIN', 'port:VIN', 'MSW.S'); c.w('VIN', 'MN3.S', (340, 320))
    c.w('VOUT', 'MSW.D', 'port:VOUT')
    c.w('GX', 'MN2A.S', 'MN2.D')
    c.w('G', 'MP2.D', (500, 0), (640, 0), 'MN2A.D'); c.w('G', (640, 0), (760, 0), 'MSW.G'); c.lab('G', (760, 0), 2)
    c.title(-460, -400)
    return c


# =============================================================== CDAC bit cell
def dacbit(m):
    p = P
    c = reg(Cell('sar10_dac%d' % m, [('DH', 'in', 'L'), ('DL', 'in', 'L'), ('TOP', 'inout', 'T'),
                                     ('VDD', 'inout', 'B'), ('VREFP', 'inout', 'B'), ('VREFN', 'inout', 'B'), ('VSS', 'inout', 'B')],
                 'CDAC cell: 2 x %d unit capacitors (%s, 0.78 fF each), each half with its reference switch (inverter between VREFP and VREFN).\n'
                 'The two pre-driver stages sit in the bit slice, next to the latch, so the long wire is driven by a strong gate.\n'
                 'Rest state (DH=0, DL=1): BH = VREFP, BL = VREFN.  DH=1 pulls TOP down, DL=0 pushes TOP up.' % (m, p['UNITCAP'])))
    c.symshape = 'dac'
    c.m = m
    wn = r2(max(p['DRV_WN_MIN'], m * p['DRV_WN_PER_UNIT']))
    wp = r2(wn * p['DRV_PN'])
    wn2 = r2(max(0.42, wn / p['DRV_PRE'])); wp2 = r2(max(0.84, wp / p['DRV_PRE']))
    wn1 = r2(max(0.42, wn2 / p['DRV_PRE'])); wp1 = r2(max(0.84, wp2 / p['DRV_PRE']))
    for d, y in (('H', -160), ('L', 160)):
        x = 320
        mp, mn = 'MP3%s' % d, 'MN3%s' % d
        c.mos(mp, 'pfet_01v8', 'B' + d, 'D' + d, 'VREFP', 'VREFP', wp, nf=nfing(wp), at=(x, y - 60))
        c.mos(mn, 'nfet_01v8', 'B' + d, 'D' + d, 'VREFN', 'VREFN', wn, nf=nfing(wn), at=(x, y + 60))
        c.w('D' + d, mp + '.G', (x - 40, y - 60), (x - 40, y + 60), mn + '.G')
        c.w('B' + d, mp + '.D', mn + '.D')
        c.port('D' + d, -160, y)
        c.w('D' + d, 'port:D' + d, (x - 40, y))
    c.vpp('CH', 'BH', 'TOP', 'VSS', m, at=(500, -130))
    c.vpp('CL', 'BL', 'TOP', 'VSS', m, at=(500, 130, 0, 2))
    c.w('BH', (340, -160), 'CH.c0'); c.w('BL', (340, 160), 'CL.c0')
    c.port('TOP', 620, 0)
    c.w('TOP', 'CH.c1', 'CL.c1'); c.w('TOP', (500, 0), 'port:TOP')
    c.port('VDD', -160, -330); c.port('VREFP', -160, -300); c.port('VREFN', -160, 300); c.port('VSS', -160, 330)
    c.title(-160, -470)
    return c


def dacdum():
    c = reg(Cell('sar10_dacdum', [('TOP', 'inout', 'T'), ('VREFP', 'inout', 'B'), ('VREFN', 'inout', 'B'), ('VSS', 'inout', 'B')],
                 'Static dummy pair: 1 unit to VREFP + 1 unit to VREFN.\nBalances the single-sided LSB cell on the other top plate.'))
    c.symshape = 'dac'
    c.vpp('CH', 'VREFP', 'TOP', 'VSS', 1, at=(0, -70))
    c.vpp('CL', 'VREFN', 'TOP', 'VSS', 1, at=(0, 70, 0, 2))
    c.port('TOP', 140, 0)
    c.w('TOP', 'CH.c1', 'CL.c1'); c.w('TOP', (0, 0), 'port:TOP')
    c.w('VREFP', 'CH.c0', (0, -130)); c.port('VREFP', 0, -130)
    c.w('VREFN', 'CL.c0', (0, 130)); c.port('VREFN', 0, 130)
    c.port('VSS', -160, 130)
    c.title(-160, -300)
    return c


# =============================================================== SAR bit slice
SC = dict(VGND='VSS', VNB='VSS', VPB='VDD', VPWR='VDD')


def slice_():
    c = reg(Cell('sar10_slice', [('TPREV', 'in', 'L'), ('QP', 'in', 'L'), ('QN', 'in', 'L'), ('VALIDB', 'in', 'L'),
                                 ('RSTB', 'in', 'L'), ('EOC', 'in', 'L'),
                                 ('T', 'out', 'R'), ('DEC', 'out', 'R'), ('DP', 'out', 'R'), ('DPB', 'out', 'R'),
                                 ('DN', 'out', 'R'), ('DNB', 'out', 'R'), ('B', 'out', 'R'),
                                 ('VDD', 'inout', 'T'), ('VSS', 'inout', 'B')],
                 'SAR bit slice (all sky130_fd_sc_hd cells).  Window = TPREV & !T: inside it the comparator result sets the P latch (INP>INN) or the N latch.\n'
                 'Each latch is one AND-OR-invert gate (set | hold) plus a NOR with reset, so a decision reaches the CDAC switch through two gates:\n'
                 'LPB falls -> DP rises and, one inverter later, DPB falls.  DEC = bit decided.  The token T sets once DEC is high and the comparator is back in reset\n'
                 '(VALIDB high): this closes the window and opens the next slice.  B = DP registered at EOC.  RSTB low clears everything.'))
    c.std('XLPB', 'a31oi_1', A1='QP', A2='TPREV', A3='TB', B1='LP', Y='LPB', at=(-260, -200))
    c.std('XLP', 'nor2b_1', A='LPB', B_N='RSTB', Y='LP', at=(-20, -200))
    c.std('XLNB', 'a31oi_1', A1='QN', A2='TPREV', A3='TB', B1='LN', Y='LNB', at=(-260, 200))
    c.std('XLN', 'nor2b_1', A='LNB', B_N='RSTB', Y='LN', at=(-20, 200))
    c.std('XDEC', 'nand2_1', A='LPB', B='LNB', Y='DEC', at=(220, -40))
    c.std('XST', 'nand3_1', A='DEC', B='VALIDB', C='TB', Y='STB', at=(400, -40))
    c.std('XT', 'nand2_1', A='STB', B='TB', Y='T', at=(620, -60))
    c.std('XTB', 'nand2_1', A='T', B='DEC', Y='TB', at=(620, 60))
    c.std('XB', 'dfxtp_1', CLK='EOC', D='LP', Q='B', at=(900, -230))
    for j, (src, dst) in enumerate((('LPB', 'DP'), ('LNB', 'DN'))):      # CDAC switch pre-drivers: true side one gate, complement two
        c.std('XG' + dst, P['PRE_CELL'], A=src, Y=dst, at=(-260 + 560 * j, 480))
        c.std('XA' + dst + 'B', 'inv_1', A=src, Y='A' + dst + 'B', at=(-80 + 560 * j, 480))
        c.std('XG' + dst + 'B', P['PRE_CELL'], A='A' + dst + 'B', Y=dst + 'B', at=(80 + 560 * j, 480))
    X = 1060
    c.port('QP', -520, -240); c.port('TPREV', -520, -200); c.port('RSTB', -520, -100); c.port('QN', -520, 120)
    c.port('VALIDB', -520, 340); c.port('EOC', -520, -320)
    c.port('B', X, -240); c.port('DP', X, -160); c.port('DPB', X, -120); c.port('DEC', X, -100); c.port('T', X, -60)
    c.port('DN', X, 140); c.port('DNB', X, 240)
    c.port('VDD', -520, -420); c.port('VSS', -520, -390)
    for n_, y_ in (('QP', -240), ('TPREV', -200), ('RSTB', -100), ('QN', 120)):
        c.w(n_, 'port:' + n_, (-460, y_)); c.lab(n_, (-460, y_), 0)
    for n_, y_ in (('DP', -160), ('DPB', -120), ('DN', 140), ('DNB', 240)):
        c.w(n_, 'port:' + n_, (X - 60, y_)); c.lab(n_, (X - 60, y_), 0)
    c.w('DEC', 'XDEC.Y', (300, -40)); c.w('DEC', (300, -100), (300, 80), 'XTB.B')
    c.w('DEC', (300, -80), 'XST.A'); c.w('DEC', (300, -100), 'port:DEC')
    c.w('VALIDB', 'port:VALIDB', (320, 340), (320, -40), 'XST.B')
    c.w('STB', 'XST.Y', (500, -40), (500, -80), 'XT.A')
    c.w('T', 'XT.Y', 'port:T'); c.w('T', (720, -60), (720, -10), (540, -10), (540, 40), 'XTB.A')
    c.w('TB', 'XTB.Y', (720, 60), (720, 10), (520, 10), (520, -40), 'XT.B'); c.lab('TB', (720, 60), 2)
    c.w('EOC', 'port:EOC', (780, -320), (780, -240), 'XB.CLK')
    c.w('B', 'XB.Q', 'port:B')
    c.title(-520, -600)
    return c


# =============================================================== async control
def ctrl():
    p = P
    c = reg(Cell('sar10_ctrl', [('OUTP', 'in', 'L'), ('OUTN', 'in', 'L'), ('CLKS', 'in', 'L'), ('DECL', 'in', 'L'),
                                ('CLKC', 'out', 'R'), ('QP', 'out', 'R'), ('QN', 'out', 'R'), ('VALIDB', 'out', 'R'),
                                ('RSTB', 'out', 'R'), ('SAMP', 'out', 'R'), ('EOC', 'out', 'R'),
                                ('VDD', 'inout', 'T'), ('VSS', 'inout', 'B')],
                 'Asynchronous clock loop (sky130_fd_sc_hd cells).  VALID = comparator has decided.\n'
                 'CLKC falls as soon as VALID rises and rises again one delay-line time (XD1..XD%d) after the comparator is back in reset:\n'
                 'that delay is the DAC settling time.  The loop stops when the last bit is decided (DECL) and during sampling (CLKS high).'
                 % (2 * p['NDLY'])))
    n = 2 * p['NDLY']
    xl = -120 + 140 * (n - 1)
    xg = max(740, xl + 160)
    xo = xg + 320
    c.std('XS1', 'inv_1', A='CLKS', Y='SB1', at=(-600, -200))
    c.std('XS2', 'inv_4', A='SB1', Y='SAMP', at=(-460, -200))
    c.std('XR3', 'inv_4', A='CLKS', Y='RSTB', at=(20, -200))      # slices released as the sampling clock falls (was 3 stages after SAMP)
    c.std('XSD', 'inv_1', A='RSTB', Y='SAMPD', at=(200, -200))
    c.std('XRUN', 'nor2_1', A='SAMPD', B='DECL', Y='RUN', at=(380, -140))
    c.std('XQP', 'inv_4', A='OUTN', Y='QP', at=(-440, -100))
    c.std('XV', 'nand2_1', A='OUTN', B='OUTP', Y='VALID', at=(-440, 0))
    c.std('XQN', 'inv_4', A='OUTP', Y='QN', at=(-440, 100))
    c.std('XVB', 'inv_4', A='VALID', Y='VALIDB', at=(-280, 0))
    prev = 'VALIDB'
    for i in range(n):
        nxt = 'VD' if i == n - 1 else 'DL%d' % (i + 1)
        c.std('XD%d' % (i + 1), 'inv_1', A=prev, Y=nxt, at=(-120 + 140 * i, 0))
        if i:
            c.w(prev, 'XD%d.Y' % i, 'XD%d.A' % (i + 1))
        prev = nxt
    if n: c.std('XG', 'nand3_1', A='RUN', B='VD', C='VALIDB', Y='CLKCB', at=(xg, 0))
    else: c.std('XG', 'nand2_1', A='RUN', B='VALIDB', Y='CLKCB', at=(xg, 0))
    c.std('XGB', 'inv_4', A='CLKCB', Y='CLKC', at=(xg + 140, 0))
    c.std('XE', 'buf_4', A='DECL', X='EOC', at=(xg + 140, 180))   # done as soon as the last bit is decided
    c.port('CLKS', -720, -200); c.port('DECL', -720, -140); c.port('OUTN', -720, -20); c.port('OUTP', -720, 20)
    c.port('SAMP', xo, -300); c.port('RSTB', xo, -270); c.port('QP', xo, -100); c.port('CLKC', xo, 0)
    c.port('VALIDB', xo, 60); c.port('QN', xo, 100); c.port('EOC', xo, 180)
    c.port('VDD', -720, -400); c.port('VSS', -720, -370)
    c.w('CLKS', 'port:CLKS', 'XS1.A'); c.w('SB1', 'XS1.Y', 'XS2.A')
    c.w('SAMP', 'XS2.Y', (-360, -200)); c.w('SAMP', (-360, -200), (-360, -300), 'port:SAMP')
    c.w('RSTB', 'XR3.Y', 'XSD.A'); c.w('RSTB', (110, -200), (110, -270), 'port:RSTB')
    c.w('SAMPD', 'XSD.Y', (280, -200), (280, -160), 'XRUN.A')
    c.w('DECL', 'port:DECL', (300, -140), (300, -120), 'XRUN.B')
    c.w('OUTN', 'port:OUTN', 'XV.A'); c.w('OUTN', (-600, -20), (-600, -100), 'XQP.A')
    c.w('OUTP', 'port:OUTP', 'XV.B'); c.w('OUTP', (-600, 20), (-600, 100), 'XQN.A')
    c.w('QP', 'XQP.Y', 'port:QP'); c.w('QN', 'XQN.Y', 'port:QN')
    c.w('VALID', 'XV.Y', 'XVB.A')
    if n:
        c.w('VALIDB', 'XVB.Y', 'XD1.A'); c.w('VALIDB', (-200, 0), (-200, 60), (xg - 80, 60), (xg - 80, 40), 'XG.C')
        c.w('VD', 'XD%d.Y' % n, 'XG.B')
        c.w('RUN', 'XRUN.Y', (xg - 100, -140), (xg - 100, -40), 'XG.A')
    else:
        c.w('VALIDB', 'XVB.Y', (-200, 0), (-200, 60), (xg - 80, 60), 'v', 'XG.B')
        c.w('RUN', 'XRUN.Y', (xg - 100, -140), 'v', 'XG.A')
    c.w('VALIDB', (xg - 80, 60), 'port:VALIDB')
    c.w('CLKCB', 'XG.Y', 'XGB.A'); c.w('CLKC', 'XGB.Y', 'port:CLKC')
    c.w('EOC', 'XE.X', 'port:EOC')
    c.title(-720, -580)
    return c


# =============================================================== top
def top():
    import draw
    n = P['NBIT']
    pins = [('VIP', 'in', 'L'), ('VIN', 'in', 'L'), ('CLK', 'in', 'L')]
    pins += [('B%d' % i, 'out', 'R') for i in range(n - 1, -1, -1)] + [('EOC', 'out', 'R')]
    pins += [('VDD', 'inout', 'T'), ('VREFP', 'inout', 'T'), ('VREFN', 'inout', 'B'), ('VSS', 'inout', 'B')]
    c = reg(Cell('sar10_adc', pins,
                 '10-bit asynchronous SAR ADC, sky130A, 1.8 V.  CLK high = sample (bootstrapped top-plate sampling), CLK low = convert (self-timed).\n'
                 'Split-capacitor CDAC: every bit capacitor is two halves resting at VREFP / VREFN, so the common mode stays constant with no Vcm reference.\n'
                 'Bits 9..1 switch both sides (cells XDP/XDN 1..%d), the last step switches one unit on the P side only.  B9..B0 update at EOC rising.' % (n - 2)))
    sup = dict(VDD='VDD', VSS='VSS')
    ref = dict(VDD='VDD', VSS='VSS', VREFP='VREFP', VREFN='VREFN')
    g = lambda name: draw.sym_geometry(CELLS[name])[0]
    PX = 480
    yP, yN = -300, 200
    dg = g('sar10_dac1')
    rP, rN = yP + dg['TOP'][1] - 40, yN + dg['TOP'][1] - 40
    bg = g('sar10_boot')
    xb = -500
    c.sub('XBSP', 'sar10_boot', VIN='VIP', CK='SAMP', VOUT='TOPP', at=(xb, rP), **sup)
    c.sub('XBSN', 'sar10_boot', VIN='VIN', CK='SAMP', VOUT='TOPN', at=(xb, rN), **sup)
    c.port('VIP', xb - 220, rP); c.port('VIN', xb - 220, rN); c.port('CLK', xb - 220, (rP + rN) // 2)
    c.w('VIP', 'port:VIP', 'XBSP.VIN'); c.w('VIN', 'port:VIN', 'XBSN.VIN')
    for k in range(1, n):
        x = (k - 1) * PX
        if k < n - 1:
            m = 2 ** (n - 2 - k)
            c.sub('XDP%d' % k, 'sar10_dac%d' % m, DH='DP%d' % k, DL='DNB%d' % k, TOP='TOPP', at=(x, yP), **ref)
            c.sub('XDN%d' % k, 'sar10_dac%d' % m, DH='DN%d' % k, DL='DPB%d' % k, TOP='TOPN', at=(x, yN), **ref)
        else:
            c.sub('XDP%d' % k, 'sar10_dac1', DH='DP%d' % k, DL='DNB%d' % k, TOP='TOPP', at=(x, yP), **ref)
            c.sub('XDN%d' % k, 'sar10_dacdum', TOP='TOPN', VREFP='VREFP', VREFN='VREFN', VSS='VSS', at=(x, yN))
        c.w('TOPP', 'XDP%d.TOP' % k, (x, rP)); c.w('TOPN', 'XDN%d.TOP' % k, (x, rN))
    xc = (n - 2) * PX + 560
    yc = (rP + rN) // 2
    yc = int(round(yc / 20.0)) * 20
    c.sub('XCMP', 'sar10_comp', INP='TOPP', INN='TOPN', CLK='CLKC', OUTP='OUTP', OUTN='OUTN', at=(xc, yc), **sup)
    c.w('TOPP', 'XBSP.VOUT', (xc - 200, rP), (xc - 200, yc - 40), 'XCMP.INP')
    c.w('TOPN', 'XBSN.VOUT', (xc - 160, rN), (xc - 160, yc + 40), 'XCMP.INN')
    cg = g('sar10_ctrl')
    xk = xc + 520
    yk = yc - 20 - cg['OUTP'][1]
    c.sub('XCTL', 'sar10_ctrl', CLKS='CLK', OUTP='OUTP', OUTN='OUTN', DECL='DEC%d' % n, SAMP='SAMP',
          RSTB='RSTB', CLKC='CLKC', QP='QP', QN='QN', VALIDB='VALIDB', EOC='EOC', at=(xk, yk), **sup)
    c.w('OUTP', 'XCMP.OUTP', 'XCTL.OUTP')
    c.w('OUTN', 'XCMP.OUTN', (xc + 200, yc + 20), (xc + 200, yk + cg['OUTN'][1]), 'XCTL.OUTN')
    xr = xk + cg['CLKC'][0] + 80
    c.w('CLKC', 'XCTL.CLKC', (xr, yk + cg['CLKC'][1]), (xr, yc + 260), (xc, yc + 260), 'XCMP.CLK')
    c.port('EOC', xr + 80, yk + cg['EOC'][1])
    c.w('EOC', 'XCTL.EOC', 'port:EOC')
    sg = g('sar10_slice')
    yS = 760
    for k in range(1, n + 1):
        x = (k - 1) * PX
        c.sub('XS%d' % k, 'sar10_slice', QP='QP', QN='QN', TPREV=('RSTB' if k == 1 else 'T%d' % (k - 1)),
              VALIDB='VALIDB', RSTB='RSTB', EOC='EOC', T='T%d' % k, DEC='DEC%d' % k, DP='DP%d' % k, DPB='DPB%d' % k,
              DN='DN%d' % k, DNB='DNB%d' % k, B='B%d' % (n - k), at=(x, yS), **sup)
        if k > 1:
            c.w('T%d' % (k - 1), 'XS%d.T' % (k - 1), 'XS%d.TPREV' % k)
        c.port('B%d' % (n - k), x + sg['B'][0] + 40, yS + sg['B'][1])
        c.w('B%d' % (n - k), 'XS%d.B' % k, 'port:B%d' % (n - k))
        if k < n:
            c.nc('XS%d.DEC' % k)
        else:
            c.nc('XS%d.DPB' % k); c.nc('XS%d.DN' % k); c.nc('XS%d.DNB' % k); c.nc('XS%d.T' % k)
    c.port('VDD', xb - 220, rP - 420); c.port('VREFP', xb - 220, rP - 390)
    c.port('VREFN', xb - 220, rP - 360); c.port('VSS', xb - 220, rP - 330)
    c.title(xb - 220, rP - 640)
    c.text('CDAC, P side (top plate TOPP)', 0, rP - 60, 0.35)
    c.text('CDAC, N side (top plate TOPN)', 0, rN - 60, 0.35)
    c.text('SAR logic: one slice per bit, token T ripples left to right', 0, yS - 260, 0.35)
    return c


def build():
    CELLS.clear()
    comparator(); boot()
    for m in (128, 64, 32, 16, 8, 4, 2, 1):
        dacbit(m)
    dacdum(); slice_(); ctrl(); top()
    return CELLS


# =============================================================== interactive testbench
TB_CODE = r"""* sar10_adc bench: 16 conversions of a 4.0625 MHz sine at 20 MS/s (CLK high = sample).
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
"""


def testbenches():
    import draw
    c = Cell('tb_sar10', [], 'Interactive testbench for sar10_adc: 50 ohm differential sine source, 20 MS/s sampling clock, ideal 1.8 V supply and reference.')
    c.is_tb = True
    g = draw.sym_geometry(CELLS['sar10_adc'])[0]
    c.sub('x1', 'sar10_adc', at=(0, 0), VIP='VIP', VIN='VIN', CLK='CLK', EOC='EOC', VDD='VDD', VREFP='VREFP', VREFN='0', VSS='0',
          **{'B%d' % i: 'B%d' % i for i in range(10)})
    yp, yn, yc = g['VIP'][1], g['VIN'][1], g['CLK'][1]
    xl = g['VIP'][0]
    c.dev('Rsp', 'res', 'value=50 footprint=1206 device=resistor m=1', at=(xl - 180, yp, 0, 1), P='VIP', M='VIPS')
    c.dev('Rsn', 'res', 'value=50 footprint=1206 device=resistor m=1', at=(xl - 380, yn, 0, 1), P='VIN', M='VINS')
    c.dev('Vsp', 'vsource', 'value=\\"SIN(0.9 0.85 4.0625e6)\\" savecurrent=false', at=(xl - 560, 200), p='VIPS', m='0')
    c.dev('Vsn', 'vsource', 'value=\\"SIN(0.9 -0.85 4.0625e6)\\" savecurrent=false', at=(xl - 720, 200), p='VINS', m='0')
    c.dev('Vclk', 'vsource', 'value=\\"PULSE(0 1.8 1n 50p 50p 12.45n 50n)\\" savecurrent=false', at=(xl - 100, 200), p='CLK', m='0')
    c.dev('Vvdd', 'vsource', 'value=1.8 savecurrent=true', at=(xl - 720, -360), p='VDD', m='0')
    c.dev('Vrefp', 'vsource', 'value=1.8 savecurrent=true', at=(xl - 520, -360), p='VREFP', m='0')
    c.w('VIP', 'Rsp.P', 'x1.VIP'); c.w('VIPS', 'Vsp.p', (xl - 560, yp), 'Rsp.M')
    c.w('VIN', 'Rsn.P', 'x1.VIN'); c.w('VINS', 'Vsn.p', (xl - 720, yn), 'Rsn.M')
    c.w('CLK', 'Vclk.p', (xl - 100, yc), 'x1.CLK')
    for v in ('Vsp', 'Vsn', 'Vclk', 'Vvdd', 'Vrefp'):
        c.gnd(v + '.m')
    c.lab('VDD', 'Vvdd.p', 2); c.lab('VREFP', 'Vrefp.p', 2)
    for pn in ('VREFN', 'VSS'):
        x, y = g[pn]
        c.w('0', 'x1.' + pn, (x, y + 40)); c.gnd((x, y + 40))
    c.code = [(g['B9'][0] + 260, -420, TB_CODE.replace('"', '\\"').replace('{', '\\{').replace('}', '\\}'))]
    c.title(xl - 720, -640)
    return [c]


# =============================================================== CACE templates
CACE_HEAD = r"""* CACE template for sar10_adc: %s
* CACE fills in every CACE{...} placeholder for each corner / temperature / supply.

.lib CACE{PDK_ROOT}/CACE{PDK}/libs.tech/ngspice/sky130.lib.spice CACE{corner}
.include CACE{PDK_ROOT}/CACE{PDK}/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice
.include CACE{PDK_ROOT}/CACE{PDK}/libs.ref/sky130_fd_pr/spice/sky130_fd_pr__cap_vpp_01p8x01p8_m1m2_noshield.model.spice
.include CACE{DUT_path}
.temp CACE{temperature}

.param VSUP=CACE{vdd}
.param FS=CACE{fs}
.param TS={0.25/FS}
Vvdd  VDD   0 {VSUP}
Vvss  VSS   0 0
Vrefp VREFP 0 {VSUP}
Vrefn VREFN 0 0
Vclk  CLK   0 PULSE(0 {VSUP} 1n 50p 50p {TS-50p} {1/FS})
Rsp VIPS VIP 50
Rsn VINS VIN 50
"""
CACE_TAIL = r"""
.save v(vip) v(vin) v(clk) v(eoc) v(b9) v(b8) v(b7) v(b6) v(b5) v(b4) v(b3) v(b2) v(b1) v(b0) i(vvdd) i(vrefp)
.option reltol=1e-4 abstol=1e-13 vntol=1e-7 chgtol=1e-16 method=gear klu rshunt=1e15
.tran 20p {1.5n+%d/FS} 0 40p uic

.control
  set filetype=binary
  run
  write CACE{simpath}/CACE{filename}_CACE{N}.raw
  shell python3 CACE{root}/gen/cace_eval.py %s CACE{simpath}/CACE{filename}_CACE{N}.raw CACE{fs} 0.25 %d CACE{vdd} CACE{simpath}/CACE{filename}_CACE{N}.data
.endc
"""


def cace_code(kind):
    if kind == 'fft':
        n = 65
        src = ("* 64 coherent samples (+1 start-up conversion) of a sine at 13/64 of the sample rate, 1.7 V peak differential\n"
               "Vsp VIPS 0 SIN(0.9 0.85 {13*FS/64})\nVsn VINS 0 SIN(0.9 -0.85 {13*FS/64})\n")
        return CACE_HEAD % 'dynamic performance (FFT)' + src + CACE_TAIL % (n, 'fft', n)
    vd = [1.7, 1.7, 1.0, 0.3, 0.01, -0.01, -0.3, -1.0, -1.7]
    n = len(vd)
    pp, pn = ['0 %g' % (0.9 + vd[0] / 2)], ['0 %g' % (0.9 - vd[0] / 2)]
    for k in range(1, n):
        t = '{1n+TS+1n+%d/FS}' % (k - 1)
        t2 = '{1n+TS+1.2n+%d/FS}' % (k - 1)
        pp += ['%s %g %s %g' % (t, 0.9 + vd[k - 1] / 2, t2, 0.9 + vd[k] / 2)]
        pn += ['%s %g %s %g' % (t, 0.9 - vd[k - 1] / 2, t2, 0.9 - vd[k] / 2)]
    src = ("* 8 DC inputs: VIP-VIN = +1.7 +1.0 +0.3 +0.01 -0.01 -0.3 -1.0 -1.7 V (each changed just after a sampling edge)\n"
           "Vsp VIPS 0 PWL(%s)\nVsn VINS 0 PWL(%s)\n" % ('\n+ '.join(pp), '\n+ '.join(pn)))
    return CACE_HEAD % 'function, power and conversion time' + src + CACE_TAIL % (n, 'static', n)


def cace_templates():
    import draw
    out = []
    g = draw.sym_geometry(CELLS['sar10_adc'])[0]
    for kind in ('static', 'fft'):
        c = Cell('tb_cace_' + kind, [], 'CACE template (%s). Edit the code block, not the netlist.' % kind)
        c.is_tb = True
        c.sub('x1', 'sar10_adc', at=(0, 0), **{p[0]: p[0] for p in CELLS['sar10_adc'].pins})
        c.pins = list(CELLS['sar10_adc'].pins)      # ipin / opin / iopin on every DUT pin (sources are in the code block)
        for p in c.pins:
            c.port(p[0], g[p[0]][0], g[p[0]][1])
        c.code = [(g['B9'][0] + 260, -420, cace_code(kind).replace('"', '\\"').replace('{', '\\{').replace('}', '\\}'))]
        c.title(g['VIP'][0] - 300, -520)
        out.append(c)
    return out
