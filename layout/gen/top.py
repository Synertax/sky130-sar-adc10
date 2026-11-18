"""SAR_ADC10 full layout generator -> magic Tcl.   python3 top.py [stage]   (stage: pins | full)"""
import lay, sys, json, math
from lay import Cell, row, via1, via2, via3
REF = '../../netlist/sar10_adc_ref.spice'
S = lay.subckts(REF); INST = {t[0]: t for t in S['sar10_adc'][1]}
UW, RP = 1.82, 1.96
FB = 0.88        # bottom of the top-plate fingers: trims the unit capacitance

def expand(name):
    tok = INST[name]; sub = tok[-1]; m = dict(zip(S[sub][0], tok[1:-1])); g = lambda n: m.get(n, name + '_' + n)
    out = []
    for u in S[sub][1]:
        if 'fet_01v8' in u[5]:
            out.append(dict(name=name + '_' + u[0], kind='n' if 'nfet' in u[5] else 'p', W=lay.par(u, 'W'), L=lay.par(u, 'L'),
                            D=g(u[1]), G=g(u[2]), S=g(u[3]), B=g(u[4])))
    return out, g

# ------------------------------------------------------------------ unit capacitor
def ucap_shapes(c, x, y, dummy=False):
    def r(l, a, b, cc, d): c.rect(l, x + a, y + b, x + cc, y + d)
    for m in ('m1', 'm2'):
        r(m, 0, 0, UW, 0.32); r(m, 0, 0, 0.14, UW); r(m, UW - 0.14, 0, UW, UW); r(m, 0, UW - 0.14, UW, UW)
        for fx in (0.56, 1.12): r(m, fx, 0.32, fx + 0.14, 1.12)
        r(m, 0.28, 1.26, 1.54, 1.54)
        for fx in (0.28, 0.84, 1.40): r(m, fx, FB, fx + 0.14, 1.26)
        if dummy: r(m, 0.6, 1.54, 1.22, 1.68)
    for vx in (0.20, 0.63, 1.19, 1.62): r('via1', vx - 0.13, 0.03, vx + 0.13, 0.29)
    r('via1', 0.78, 1.27, 1.04, 1.53)
    for a in (0.0, 1.45):          # bottom-plate guard strips on m3: the top-plate spine only sees its own cell
        r('m3', a, 0.0, a + 0.37, 1.66); r('via2', (a + 0.06) if a < 1 else (a + 0.03), 0.03, (a + 0.34) if a < 1 else (a + 0.31), 0.31)
def ucap_cell():
    c = Cell('sar10_ucap'); ucap_shapes(c, 0, 0)
    c.rect('via2', 0.77, 1.26, 1.05, 1.54); c.rect('m3', 0.745, -0.07, 1.075, 1.89)
    c.label('T', 'm3', 0.91, 0.9); c.label('B', 'm2', 0.07, 0.07)
    return c

# ------------------------------------------------------------------ CDAC array (local coords, P side)
SEQ = ['A', 'a', 'B', 'A', 'b', 'a', 'ma', 'mb', 'mc', 'md', 'a', 'b', 'A', 'B', 'a', 'A']
def colcells(kind):
    cn = {'A': (1, 'H'), 'a': (1, 'L'), 'B': (2, 'H'), 'b': (2, 'L')}
    if kind in cn: return [cn[kind]] * 32
    if kind == 'ma': return [(3, 'H')] * 16 + [(3, 'L')] * 16
    if kind == 'md': return [(3, 'L')] * 16 + [(3, 'H')] * 16
    mb = [(4, 'H')] * 8 + [(5, 'H')] * 4 + [(6, 'H')] * 2 + [(7, 'H'), (8, 'H'), (9, 'H'), (7, 'L')] + [(6, 'L')] * 2 + [(5, 'L')] * 4 + [(4, 'L')] * 8
    if kind == 'mb': return mb
    mc = mb[::-1]; mc[15] = (9, 'L'); mc[16] = (8, 'L'); return mc
YB = -2.4
def cdac(c, netname):
    pins = []; x = 0.0; cols = []
    def strapv(cx, r):          # bottom-plate strap only on the outer edges (under the m3 bottom-plate guards), never under the
        for m in ('m1', 'm2'):  # top-plate spine: every unit then sees the same top-to-bottom coupling whatever its neighbours are
            c.rect(m, cx, r * RP + UW, cx + 0.37, (r + 1) * RP); c.rect(m, cx + 1.45, r * RP + UW, cx + UW, (r + 1) * RP)
    # left dummy column
    for r in range(34):
        ucap_shapes(c, x, r * RP, True)
        if r < 33: strapv(x, r)
    c.rect('m2', 0.75, YB, 1.07, 0.1); pins.append(('VREFN', 0.91, 0.91, YB + 0.25))
    prev = x; x += UW + 0.30
    for i, kind in enumerate(SEQ):
        cells = colcells(kind)
        segs = []                       # (net, j_first, j_last) top->bottom
        for j, bh in enumerate(cells):
            n = netname(*bh)
            if segs and segs[-1][0] == n: segs[-1][2] = j
            else: segs.append([n, j, j])
        cw = 0.6 + (len(segs) - 1) * 0.8
        if i == 8: x += 0.3
        if i < 8: cx = x; tx = [cx + UW + 0.3 + k * 0.8 for k in range(len(segs))]
        else: cx = x + cw; tx = [cx - 0.3 - k * 0.8 for k in range(len(segs))]
        for j, bh in enumerate(cells):
            r = 32 - j; c.inst('sar10_ucap', cx, r * RP)
            if j + 1 < 32 and netname(*cells[j + 1]) == netname(*bh): strapv(cx, r - 1)
        for k, (n, j0, j1) in enumerate(segs[::-1]):       # lowest segment -> nearest track
            y = (32 - j1) * RP
            if i < 8: c.rect('m2', cx + 1.75, y, tx[k] + 0.16, y + 0.32)
            else: c.rect('m2', tx[k] - 0.16, y, cx + 0.07, y + 0.32)
            c.rect('via1', tx[k] - 0.13, y + 0.03, tx[k] + 0.13, y + 0.29)
            c.rect('m1', tx[k] - 0.16, YB, tx[k] + 0.16, y + 0.32)
            c.rect('via1', tx[k] - 0.13, YB + 0.12, tx[k] + 0.13, YB + 0.38); c.rect('m2', tx[k] - 0.19, YB + 0.03, tx[k] + 0.19, YB + 0.47)
            pins.append((n, tx[k], tx[k], YB + 0.25))
        for r in (0, 33):
            ucap_shapes(c, cx, r * RP, True); c.rect('m3', cx + 0.745, r * RP - 0.07, cx + 1.075, r * RP + 2.0)
            c.rect('m2', prev + UW - 0.05, r * RP + 0.8, cx + 0.05, r * RP + 1.1)
        cols.append(cx); prev = cx; x += UW + cw
    x += 0.30
    for r in range(34):                # right dummy column
        ucap_shapes(c, x, r * RP, True)
        if r < 33: strapv(x, r)
    for r in (0, 33): c.rect('m2', prev + UW - 0.05, r * RP + 0.8, x + 0.05, r * RP + 1.1)
    bar = (cols[0] + 0.745, 33 * RP + 1.96, cols[-1] + 1.075, 33 * RP + 2.76)
    c.rect('m3', *bar)
    bbar = (cols[-1] + 0.745, -1.1, x + UW + 2.1, -0.3); c.rect('m3', *bbar)       # only the innermost spine: no bit-line track runs under it
    c.rect('m3', cols[-1] + 0.745, -0.5, cols[-1] + 1.075, 0.0)
    return pins, (bar, bbar), x + UW

# ------------------------------------------------------------------ router
class Router:
    def __init__(s, c): s.c = c; s.v = []; s.h = []; s.ob3 = []; s.ob4 = []
    def vfree(s, x, y0, y1, net):
        if y0 > y1: y0, y1 = y1, y0
        for a, b, cc, d in s.ob3:
            if x + 0.55 > a and x - 0.55 < cc and y1 + 0.55 > b and y0 - 0.55 < d: return False
        for vx, a, b, n in s.v:
            if abs(vx - x) < 0.7999 and (n != net or abs(vx - x) > 0.001) and y1 + 0.6 > a and y0 - 0.6 < b: return False
        return True
    def hfree(s, y, x0, x1, net):
        for a, b, cc, d in s.ob4:
            if y + 0.55 > b and y - 0.55 < d and x1 + 0.55 > a and x0 - 0.55 < cc: return False
        for hy, a, b, n in s.h:
            if abs(hy - y) < 0.7999 and (n != net or abs(hy - y) > 0.001) and x1 + 0.6 > a and x0 - 0.6 < b: return False
        return True
    def vert(s, x, y0, y1, net):
        if y0 > y1: y0, y1 = y1, y0
        if y1 - y0 < 0.5: y1 = y0 + 0.5
        s.c.rect('m3', x - 0.15, y0 - 0.25, x + 0.15, y1 + 0.25); s.v.append((x, y0 - 0.25, y1 + 0.25, net))
    def horz(s, y, x0, x1, net):
        if x1 - x0 < 0.5: x1 = x0 + 0.5
        s.c.rect('m4', x0 - 0.25, y - 0.15, x1 + 0.25, y + 0.15); s.h.append((y, x0 - 0.25, x1 + 0.25, net))
    @staticmethod
    def xs(p):
        a, b = p[1], p[2]
        if b - a < 0.6: return [(a + b) / 2]
        a += 0.25; b -= 0.25; m = (a + b) / 2; out = [m]; k = 1
        while m - k * 0.2 >= a or m + k * 0.2 <= b:
            if m + k * 0.2 <= b: out.append(m + k * 0.2)
            if m - k * 0.2 >= a: out.append(m - k * 0.2)
            k += 1
        return out
    def two(s, p, q):
        net = p[0]; lo = max(p[1], q[1]); hi = min(p[2], q[2])
        if lo <= hi:
            cand = s.xs((net, lo, hi, 0)) if hi - lo >= 0.6 else ([(lo + hi) / 2] if (p[2] - p[1] < 0.6 or q[2] - q[1] < 0.6 or hi - lo > 0.4) else [])
            for x in cand:
                x = lay.q(x)
                if abs(p[3] - q[3]) > 0.3 and s.vfree(x, p[3], q[3], net):
                    s.vert(x, p[3], q[3], net); via2(s.c, x, p[3]); via2(s.c, x, q[3]); return True
        ym = round((p[3] + q[3]) / 2 / 0.8) * 0.8
        for k in range(0, 300):
            for y in ((ym + k * 0.8, ym - k * 0.8) if k else (ym,)):
                y = lay.q(y)
                if abs(y - p[3]) < 1.2 or abs(y - q[3]) < 1.2: continue
                xp = next((x for x in s.xs(p)[:300] if s.vfree(x, p[3], y, net)), None)
                if xp is None: continue
                xq = next((x for x in s.xs(q)[:300] if abs(x - xp) >= 1.0 and s.vfree(x, q[3], y, net)), None)
                if xq is None: continue
                if not s.hfree(y, min(xp, xq), max(xp, xq), net): continue
                xp, xq = lay.q(xp), lay.q(xq)
                s.vert(xp, p[3], y, net); s.vert(xq, q[3], y, net); s.horz(y, min(xp, xq), max(xp, xq), net)
                via2(s.c, xp, p[3]); via2(s.c, xq, q[3]); via3(s.c, xp, y); via3(s.c, xq, y); return True
        return False
    def net(s, pins):
        def dist(p, q):
            gap = max(0, max(p[1], q[1]) - min(p[2], q[2]))
            return gap + abs(p[3] - q[3])
        pins = sorted(pins, key=lambda p: (p[3], p[1])); done = [pins[0]]; rest = pins[1:]
        while rest:
            prog = False
            for r in sorted(rest, key=lambda r: min(dist(r, c) for c in done)):
                for c in sorted(done, key=lambda c: dist(r, c))[:8]:
                    if s.two(c, r): done.append(r); rest.remove(r); prog = True; break
                if prog: break
            if not prog: break
        for r in rest: print('UNROUTED', r)
        return len(rest)

# ------------------------------------------------------------------ blocks
def place(top, blk, pins, allpins, mx=None, ren=None):
    top.merge(blk, mx=mx)
    for n, a, b, y in pins:
        if ren: n = ren(n)
        if mx is not None: a, b = 2 * mx - b, 2 * mx - a
        allpins.setdefault(n, []).append((n, lay.q(a), lay.q(b), lay.q(y)))

def devrow(c, x0, y0, devs):
    """one row: N section (VSS rail) + one P section per bulk net"""
    secs = [('n', 'VSS', [d for d in devs if d['kind'] == 'n'])]
    for b in dict.fromkeys(d['B'] for d in devs if d['kind'] == 'p'):
        secs.append(('p', b, [d for d in devs if d['kind'] == 'p' and d['B'] == b]))
    secs = [s for s in secs if s[2]]
    p, xe, yt = row(c, x0, y0, secs)
    return [(n, a, b, y) for n, (a, b, y) in p.items()], xe, yt

def est(devs):
    w = 0
    for d in devs: w += lay.mos_len(lay.nfing(d['W'])[0], d['L']) + lay.DGAP
    return w + 3 * 0.5 + 2 * lay.SGAP

def mim(c, x, y, top_net, bot_net):
    """9x9 MIM: bottom plate m3, top plate via mimcc to m4.  M2 landing pins for both plates."""
    c.rect('m3', x, y, x + 9.6, y + 10.6); c.rect('mimcap', x + 0.3, y + 0.3, x + 9.3, y + 9.3)
    c.rect('mimcc', x + 0.7, y + 0.7, x + 8.9, y + 8.9); c.rect('m4', x + 0.5, y + 0.5, x + 9.1, y + 12.5)
    via2(c, x + 2.0, y + 10.0)                       # bottom plate -> m2 pad
    via3(c, x + 6.0, y + 12.1); via2(c, x + 6.0, y + 12.1)      # top plate m4 -> m3 pad -> m2 pad
    c.rect('m2', x - 4.6, y + 9.84, x + 2.2, y + 10.16); c.rect('m2', x - 4.6, y + 11.94, x + 6.2, y + 12.26)
    return [(bot_net, x - 4.6, x - 1.7, y + 10.0), (top_net, x - 4.6, x - 1.7, y + 12.1)], (x - 0.8, y - 0.8, x + 10.4, y + 12.5)

def pring(c, x0, y0, x1, y1, P, pinx=None):
    """P+ substrate guard ring (inner edge = the given box), tied to VSS through an m2 pin on the bottom side"""
    w = 0.34
    for a, b, cc, d in ((x0 - w, y0 - w, x1 + w, y0), (x0 - w, y1, x1 + w, y1 + w), (x0 - w, y0 - w, x0, y1 + w), (x1, y0 - w, x1 + w, y1 + w)):
        c.rect('psd', a, b, cc, d)
        hz = (cc - a) > (d - b)
        i = (0.12, 0.085) if hz else (0.085, 0.12)
        c.rect('psc', a + i[0], b + i[1], cc - i[0], d - i[1]); c.rect('mcon', a + i[0], b + i[1], cc - i[0], d - i[1])
        c.rect('li', a + 0.03, b + 0.03, cc - 0.03, d - 0.03); c.rect('m1', a - 0.03, b - 0.03, cc + 0.03, d + 0.03)
    px = x0 + 0.3 if pinx is None else pinx; yy = y0 - w / 2
    via1(c, px + 0.3, yy); via1(c, px + 0.9, yy); c.rect('m2', px, yy - 0.16, px + 1.2, yy + 0.16)
    P.setdefault('VSS', []).append(('VSS', lay.q(px), lay.q(px + 1.2), lay.q(yy)))

def build(stage):
    top = Cell('sar10_adc'); P = {}; R = Router(top)
    # ---- array geometry
    tmp = Cell('t'); apins, bars, Wa = cdac(tmp, lambda b, h: 'XDP%d_B%s' % (b, h))
    X0 = 3.0; CX = lay.q(X0 + Wa + 12.0); Wm = math.floor(2 * CX / 0.46) * 0.46; NR = 5; Hm = (NR + 2) * 2.72
    # ---- driver rows
    y = Hm + 4.0
    def drivers(names, y):
        c = Cell('t'); pins = []; cur = []; rows = []
        for n in names:
            d = expand(n)[0]
            for dd in d:
                if dd['kind'] == 'n': dd['B'] = 'VSS'
            if cur and est(cur + d) > Wa: rows.append(cur); cur = []
            cur += d
        rows.append(cur)
        for rw in rows:
            p, xe, yt = devrow(c, X0, y, rw); pins += p; y = yt + 1.5
        return c, pins, y
    cP, pP, yP = drivers(['XDP%d' % i for i in range(1, 10)], y)
    cN, pN, yN = drivers(['XDN%d' % i for i in range(1, 9)], y)
    # MSB drivers on the inner edge (next to the centre corridor): P block mirrored about its own centre, N block = its mirror about CX
    mP = X0 + Wa / 2; shN = 2 * (CX - mP)
    place(top, cP, pP, P, mx=mP)
    cNs = Cell('t'); cNs.merge(cN, dx=shN); place(top, cNs, [(n, a + shN, b + shN, yy) for n, a, b, yy in pN], P)
    y2 = max(yP, yN) + 1.0
    # ---- arrays
    AY = lay.q(y2 + 18.0 - YB)
    for side in 'PN':
        c = Cell('t')
        nn = (lambda b, h: 'XDP%d_B%s' % (b, h)) if side == 'P' else (lambda b, h: ('VREFP' if h == 'H' else 'VREFN') if b == 9 else 'XDN%d_B%s' % (b, h))
        ap, (bar, bbar), _ = cdac(c, nn)
        sh = Cell('t'); sh.merge(c, dx=X0, dy=AY)
        place(top, sh, [(n, a + X0, b + X0, yy + AY) for n, a, b, yy in ap], P, mx=None if side == 'P' else CX)
        seen = set()
        for n, a, b, yy in ap:
            if n in seen or n.startswith('VREF'): continue
            seen.add(n); xx = a + X0 if side == 'P' else 2 * CX - (a + X0); top.label(n, 'm2', xx, yy + AY, False)
    barP = (bar[0] + X0, bar[1] + AY, bar[2] + X0, bar[3] + AY)
    aL, aR, aB, aT = X0, X0 + Wa, AY - 1.1, barP[3]
    XT = lay.q(X0 + Wa + 1.7)        # top-plate drop to the comparator, just inside the corridor
    top.label('TOPP', 'm3', barP[0] + 1.0, barP[1] + 0.4, False); top.label('TOPN', 'm3', 2 * CX - barP[0] - 1.0, barP[1] + 0.4, False)
    for mxx in (None, CX):
        a, b = (aL, aR) if mxx is None else (2 * CX - aR, 2 * CX - aL)
        R.ob3.append((a, aB, b, aT)); R.ob4.append((a, aB, b, aT))
        R.ob3.append((b, aB, b + 2.4, AY - 0.3) if mxx is None else (a - 2.4, aB, a, AY - 0.3))
    for sgn in (0, 1):
        a, b = (aL - 1.0, aR + 0.6) if sgn == 0 else (2 * CX - aR - 0.6, 2 * CX - aL + 1.0)
        pring(top, a, AY + YB - 0.8, b, aT + 0.5, P, pinx=(a - 0.3) if sgn == 0 else (b - 0.9))
    # ---- comparator (band A), mirrored device order
    yA = Hm + 5.5
    d = {x['name'].split('_')[1][1:]: x for x in expand('XCMP')[0]}
    NK = ('M3', 'M1', 'M0', 'M0B', 'M2', 'M4'); PK = ('M5', 'M9', 'M7', 'M8', 'M10', 'M6')     # PMOS above the NMOS of the same net: risers line up
    for k in ('M0B', 'M2', 'M4', 'M6', 'M8', 'M10'): d[k]['flip'] = True       # right half = mirror image of the left half
    # single wiring channel: NMOS row below, PMOS row mirrored upside down above, one m2 track per net shared by both rows.
    # bottom -> top: VSS, TAIL, TOPP|TOPN, XN|XP, OUTN, CLKC, OUTP, VDD  (NMOS-only nets nearest the NMOS row)
    LN = ('XCMP_TAIL', 'TOPP', 'XCMP_XN', 'OUTN', 'CLKC', 'OUTP'); SH = (('TOPP', 'TOPN'), ('XCMP_XN', 'XCMP_XP'))
    def x0for(keys, dg):
        return CX - 0.7 - (sum(lay.mos_len(lay.nfing(d[k]['W'])[0], d[k]['L']) for k in keys) + (len(keys) - 1) * dg) / 2
    def mirror_y(src, dst, ym):
        for l_, ax, ay, bx, by in src.shapes: dst.rect(l_, ax, 2 * ym - by, bx, 2 * ym - ay)
    best = None
    for dgN in (0.9, 1.0, 1.1, 1.2, 1.4):
        for dgP in [round(0.9 + 0.05 * k, 2) for k in range(23)]:
            cn = Cell('t'); rn = []
            p1, xe, yt = row(cn, x0for(NK, dgN), yA, [('n', 'VSS', [d[k] for k in NK])], dgap=dgN, full=False, order=LN, share=SH, rlog=rn)
            cq = Cell('t'); rp = []
            p2, xe2, ytp = row(cq, x0for(PK, dgP), 0.0, [('p', 'VDD', [d[k] for k in PK])], dgap=dgP, full=False, order=LN[::-1], share=SH,
                               tracks_extra=('TOPP', 'TOPN', 'XCMP_TAIL'), rlog=rp)
            ym = (p1['VSS'][2] + p2['VDD'][2] + 7 * lay.TP) / 2
            rpm = [(x, 2 * ym - b, 2 * ym - a, n) for x, a, b, n in rp]
            def clash(r1, r2):        # m1 risers (via pads +-0.16) of the two rows: other nets need 0.14 spacing; the same net must
                dx = abs(r1[0] - r2[0])   # either overlap (merge) or keep 0.14 too -- a 0..0.14 notch is a spacing error as well
                if not (r1[1] < r2[2] + 0.14 and r2[1] < r1[2] + 0.14): return False
                return dx < 0.46 if r1[3] != r2[3] else 0.30 < dx < 0.46
            bad_ = [(r1, r2) for r1 in rn for r2 in rpm if clash(r1, r2)]
            if not bad_: best = (dgN, dgP); break
        if best: break
    assert best, 'no conflict-free comparator channel'
    print('comparator channel: dgap N %.2f P %.2f' % best)
    c = Cell('t'); c.shapes += cn.shapes; mirror_y(cq, c, ym)
    p2m = {n: (a, b, 2 * ym - y) for n, (a, b, y) in p2.items()}
    for n in set(p1) & set(p2m):
        if n not in ('VSS', 'VDD'): assert abs(p1[n][2] - p2m[n][2]) < 1e-6, (n, p1[n], p2m[n])
    yt = 2 * ym - 0.0            # top of the comparator (mirrored PMOS tap rail)
    merged = {}
    for src in (p1, p2m):
        for n, (a, b, y) in src.items():
            if n in merged: a0, b0, _ = merged[n]; merged[n] = (min(a, a0), max(b, b0), y)
            else: merged[n] = (a, b, y)
    for n, (a, b, y) in merged.items(): c.rect('m2', a, y - 0.16, b, y + 0.16)       # bridge the NMOS and PMOS pieces of each net
    assert merged['XCMP_XN'][1] + 0.3 < merged['XCMP_XP'][0], 'XN/XP share overlap'
    cp = [(n, a, b, y) for n, (a, b, y) in merged.items()]
    for n, a, b, yy in list(cp):
        if n == 'TOPP':
            xv = XT; c.rect('m2', xv - 0.5, yy - 0.16, a + 0.1, yy + 0.16); cp.append(('_T', xv, yy, 0))
        if n == 'TOPN':
            xv = 2 * CX - XT; c.rect('m2', b - 0.1, yy - 0.16, xv + 0.5, yy + 0.16); cp.append(('_T', xv, yy, 0))
    tv = [(x, yy) for n, x, yy, _ in cp if n == '_T']; cp = [q_ for q_ in cp if q_[0] not in ('_T', 'TOPP', 'TOPN')]
    place(top, c, cp, P)
    xlo = min(x0for(NK, best[0]), x0for(PK, best[1])); xhi = max(xe, xe2)
    pring(top, xlo - 1.2, yA - 0.8, xhi + 1.2, yt + 0.8, P, pinx=xlo - 0.6)
    yt2 = yt
    for x, yy in tv:
        net = 'TOPP' if x < CX else 'TOPN'; R.vert(x, AY - 0.7, yy, net); via2(top, x, yy)
    yB = aT + 3.2
    # ---- bootstrapped switches (band B)
    c = Cell('t'); dv, g = expand('XBSP')
    bp, xe, ytb = devrow(c, X0, yB, dv)
    mp, mrect = mim(c, xe + 6.0, yB, g('TOP'), g('BOT')); bp += mp
    ren = lambda n: n.replace('XBSP', 'XBSN').replace('VIP', 'VIN').replace('TOPP', 'TOPN')
    place(top, c, bp, P); place(top, c, bp, P, mx=CX, ren=ren)
    for mxx in (None, CX):      # substrate guard ring around each bootstrapped switch (devices only; the MIM sits outside)
        ga, gb = X0 - 1.2, xe + 1.0
        if mxx is not None: ga, gb = 2 * CX - gb, 2 * CX - ga
        pring(top, ga, yB - 0.8, gb, ytb + 0.5, P, pinx=(ga + 0.3) if mxx is None else (gb - 1.5))
    for mxx in (None, CX):
        a, b = (mrect[0], mrect[2]) if mxx is None else (2 * CX - mrect[2], 2 * CX - mrect[0])
        R.ob3.append((a, mrect[1], b, mrect[3])); R.ob4.append((a, mrect[1], b, mrect[3]))
    # top plates -> switch outputs (direct m3 from the bars)
    for net in ('TOPP', 'TOPN'):
        pn = [p for p in P[net] if p[3] > yB][0]; P[net].remove(pn)
        lo, hi = (max(pn[1], barP[0]), min(pn[2], barP[2])) if net == 'TOPP' else (max(pn[1], 2 * CX - barP[2]), min(pn[2], 2 * CX - barP[0]))
        x = lay.q((lo + hi) / 2); R.vert(x, barP[3] - 0.4, pn[3], net); via2(top, x, pn[3])
        assert not P[net], P[net]
        del P[net]
    H = max(ytb, mrect[3] + yB * 0) + 2.0
    # ---- digital macro pins
    bad = 0
    for n in sorted(P):
        if n.startswith('XCMP_') and len(P[n]) > 1: bad += R.net(P[n])
    for n in ('OUTP', 'OUTN', 'CLKC'):          # join the comparator's own tracks first, keep the widest as the pin
        cpn = [p for p in P[n] if yA < p[3] < yt2 + 1]; bad += R.net(cpn)
        P[n] = [p for p in P[n] if not (yA < p[3] < yt2 + 1)] + [max(cpn, key=lambda p: p[2] - p[1])]
    R.ob3.append((0, 0, Wm, Hm)); R.ob4.append((0, 0, Wm, Hm))
    dnets = ['SAMP', 'OUTN', 'OUTP', 'CLKC'] + ['DP%d' % i for i in range(1, 10)] + ['DNB%d' % i for i in range(1, 10)] + ['DN%d' % i for i in range(1, 9)] + ['DPB%d' % i for i in range(1, 9)]
    used = []; dpin = {}
    def slot(x):
        k = round((x - 0.23) / 0.46)
        for dk in sorted(range(-200, 200), key=abs):
            xx = lay.q(0.23 + (k + dk) * 0.46)
            if 3.0 < xx < Wm - 3.0 and all(abs(xx - u) >= 0.9 for u in used): used.append(xx); return xx
    for n in dnets:
        tr = [p for p in P[n]]; tr.sort(key=lambda p: p[3])
        x = (tr[0][1] + tr[0][2]) / 2 if n not in ('SAMP',) else CX
        if n == 'SAMP':
            x = next(xx for xx in sorted([lay.q(0.23 + k * 0.46) for k in range(int((CX - 5) / 0.46), int((CX + 5) / 0.46))], key=lambda v: abs(v - CX)) if all(abs(xx - u) >= 0.9 for u in used) and R.vfree(xx, Hm + 1.3, aT + 1.6, n)); used.append(x); dpin[n] = ('met2', x, Hm); continue
        if n in ('OUTP', 'OUTN', 'CLKC'):
            w = max(tr, key=lambda p: p[2] - p[1])
            cand = [lay.q(0.23 + k * 0.46) for k in range(int(w[1] / 0.46) + 2, int(w[2] / 0.46) - 1)]
            cand = sorted(cand, key={'OUTN': lambda v: v, 'OUTP': lambda v: -v, 'CLKC': lambda v: abs(v - CX)}[n])   # OUTN left, OUTP right, CLKC centre
            x = next(xx for xx in cand if all(abs(xx - u) >= 0.9 for u in used) and R.vfree(xx, Hm + 1.3, w[3], n)); used.append(x); dpin[n] = ('met2', x, Hm); continue
        dpin[n] = ('met2', slot(x), Hm)
    bn = ['B%d' % i for i in range(10)] + ['EOC', 'CLK']
    bn = ['B%d' % i for i in range(9, -1, -1)] + ['EOC', 'CLK']      # under the slice cores (centre), MSB first
    for i, n in enumerate(bn): dpin[n] = ('met2', slot(CX - 7 + i * 14 / (len(bn) - 1)), 0)
    json.dump(dict(W=Wm, NR=NR, margin=2.3, cluster=False, loopfix=True, nudge=True, pins=dpin), open('../work/dig/pins.json', 'w'))
    print('chip %.2f x %.2f um, array %.2f, macro %.2f x %.2f' % (2 * CX, H, Wa, Wm, Hm))
    if stage == 'pins': return None
    top.inst('sar10_dig', 0, 0)
    for n, (l, x, yy) in dpin.items():
        if yy > 0:
            top.rect('m2', x - 0.15, Hm - 0.5, x + 0.15, Hm + 1.6); P.setdefault(n, []).append((n, x, x, Hm + 1.3)); R.v.append((x, Hm + 0.8, Hm + 3.6, n))
        else:
            top.rect('m2', x - 0.15, -1.2, x + 0.15, 0.5); top.label(n, 'm2', x, -0.9)
    # macro supply straps (even rails VSS on the left, odd rails VDD on the right)
    for k in range(NR + 1):
        yy = 2.72 + k * 2.72
        if k % 2 == 0: top.rect('m1', 0.5, yy - 0.24, 2.5, yy + 0.24); via1(top, 0.8, yy)
        else: top.rect('m1', Wm - 2.5, yy - 0.24, Wm - 0.5, yy + 0.24); via1(top, Wm - 0.8, yy)
    top.rect('m2', 0.64, 2.4, 0.96, Hm + 1.6); top.rect('m2', Wm - 0.96, 2.4, Wm - 0.64, Hm + 1.6)
    P['VSS'].append(('VSS', 0.8, 0.8, Hm + 1.3)); P['VDD'].append(('VDD', lay.q(Wm - 0.8), lay.q(Wm - 0.8), Hm + 1.3))
    # ---- routing
    for n in P:
        for p in P[n]:
            if p[1] == p[2] and abs(p[3] - (AY + YB + 0.25)) < 0.01: R.v.append((p[1], p[3] - 12.0, p[3] + 0.5, n))
    order = ['OUTP', 'OUTN', 'CLKC', 'SAMP'] + sorted(n for n in dpin if n in P) + sorted((n for n in P if '_B' in n and n[-1] in 'HL'), reverse=True) 
    order = list(dict.fromkeys(order))
    order += sorted(n for n in P if n not in order and n not in ('VDD', 'VSS', 'VREFP', 'VREFN')) + ['VREFP', 'VREFN', 'VDD', 'VSS']
    for n in order:
        if n.startswith('XCMP_'): continue
        if len(P[n]) < 2:
            continue
        bad += R.net(P[n])
    print('unrouted', bad, 'm3 wires', len(R.v), 'm4 wires', len(R.h))
    for n in ('VIP', 'VIN', 'VDD', 'VSS', 'VREFP', 'VREFN'):
        p = sorted(P[n], key=lambda p: -(p[2] - p[1]))[0]; top.label(n, 'm2', p[1] + 0.3, p[3])
    return top

if __name__ == '__main__':
    stage = sys.argv[1] if len(sys.argv) > 1 else 'full'
    t = build(stage)
    if t:
        lay.tcl([ucap_cell(), t], '../work/sar10_adc.tcl', instoff={'sar10_ucap': (0, -0.07), 'sar10_dig': (2.11, 0)})
        print('shapes', len(t.shapes), 'insts', len(t.insts))
