"""Scripted layout engine for SAR_ADC10: cells are lists of magic paint rectangles, emitted as a magic Tcl script."""
import re, math
G = 0.005
def q(v): return round(round(v / G) * G, 3)

IW = {}          # instance widths (for mirrored placement of symmetric cells)

class Cell:
    def __init__(s, name): s.name = name; s.shapes = []; s.insts = []; s.labels = []
    def rect(s, l, x0, y0, x1, y1):
        if x1 < x0: x0, x1 = x1, x0
        if y1 < y0: y0, y1 = y1, y0
        s.shapes.append((l, q(x0), q(y0), q(x1), q(y1)))
    def inst(s, cell, x, y): s.insts.append((cell, q(x), q(y)))
    def label(s, t, l, x, y, port=True): s.labels.append((t, l, q(x), q(y), port))
    def merge(s, o, dx=0, dy=0, mx=None, iw=1.82):
        f = (lambda x: x) if mx is None else (lambda x: 2 * mx - x)
        for l, x0, y0, x1, y1 in o.shapes: s.rect(l, f(x0) + dx, y0 + dy, f(x1) + dx, y1 + dy)
        for c, x, y in o.insts: s.inst(c, (x if mx is None else 2 * mx - x - IW.get(c, iw)) + dx, y + dy)
        for t, l, x, y, p in o.labels: s.label(t, l, f(x) + dx, y + dy, p)
    def bbox(s):
        xs = [v for sh in s.shapes for v in (sh[1], sh[3])]; ys = [v for sh in s.shapes for v in (sh[2], sh[4])]
        return min(xs), min(ys), max(xs), max(ys)

def tcl(cells, path, instoff=None):
    """instoff: {cellname: (dx,dy)} lower-left bbox offset of instanced cells relative to their origin"""
    instoff = instoff or {}
    o = ['drc off', 'snap internal']
    for c in cells:
        o.append('load %s -silent' % c.name)
        o.append('select top cell'); 
        for l, x0, y0, x1, y1 in c.shapes:
            o.append('box %gum %gum %gum %gum\npaint %s' % (x0, y0, x1, y1, l))
        for n, x, y in c.insts:
            dx, dy = instoff.get(n, (0, 0))
            o.append('box %gum %gum %gum %gum\ngetcell %s child 0 0' % (x, y, x + 0.1, y + 0.1, n))
        for t, l, x, y, p in c.labels:
            o.append('box %gum %gum %gum %gum\nlabel %s c %s' % (x - 0.05, y - 0.05, x + 0.05, y + 0.05, t, l))
            if p: o.append('port make')
        o.append('save %s' % c.name)
    open(path, 'w').write('\n'.join(o) + '\n')

# ---------------------------------------------------------------- MOS primitive
SDW = 0.30
def nfing(W, wmax=2.0):
    nf = max(1, math.ceil(W / wmax - 1e-9))
    while round(W * 1000) % (nf * 5) != 0: nf += 1
    return nf, W / nf

def mos_len(nf, L): return nf * (L + SDW) + SDW

def mos(c, kind, x, y, wf, L, nf, flip=False):
    if flip:                    # mirror image about the device centre: gate contact on the right
        tc = Cell('t'); t = mos(tc, kind, x, y, wf, L, nf); xc = x + mos_len(nf, L) / 2
        c.merge(tc, mx=xc)
        return dict(sd=[2 * xc - v for v in t['sd']], sdtop=t['sdtop'], g=2 * xc - t['g'], gtop=t['gtop'], x1=t['x1'])
    """vertical-gate MOS, diffusion lower-left at (x,y). returns terminals: sd = list of m1 strips (cx), g = gate pad cx; top y of each"""
    dl, ct = ('ndiff', 'ndc') if kind == 'n' else ('pdiff', 'pdc')
    p = L + SDW; X1 = x + mos_len(nf, L)
    c.rect(dl, x, y, X1, y + wf)
    sd = []
    for i in range(nf + 1):
        sx = x + i * p + (SDW - 0.17) / 2
        c.rect(ct, sx, y + 0.06, sx + 0.17, y + wf - 0.06)
        c.rect('li', sx, y - 0.02, sx + 0.17, y + wf + 0.02)
        c.rect('mcon', sx, y + 0.06, sx + 0.17, y + wf - 0.06)
        c.rect('m1', sx - 0.03, y, sx + 0.20, y + wf)
        sd.append(sx + 0.085)
    by = y + wf + 0.15
    for i in range(nf):
        gx = x + SDW + i * p
        c.rect('poly', gx, y - 0.13, gx + L, by + 0.33)
    c.rect('poly', x - 0.62, by, x + SDW + (nf - 1) * p + L, by + 0.33)
    c.rect('pc', x - 0.54, by + 0.08, x - 0.37, by + 0.25)
    c.rect('li', x - 0.66, by + 0.08, x - 0.25, by + 0.25)
    c.rect('mcon', x - 0.54, by + 0.08, x - 0.37, by + 0.25)
    c.rect('m1', x - 0.60, by + 0.02, x - 0.31, by + 0.31)
    return dict(sd=sd, sdtop=y + wf, g=x - 0.455, gtop=by + 0.31, x1=X1)

def via1(c, x, y):       # centre
    c.rect('via1', x - 0.13, y - 0.13, x + 0.13, y + 0.13); c.rect('m1', x - 0.16, y - 0.16, x + 0.16, y + 0.16); c.rect('m2', x - 0.16, y - 0.16, x + 0.16, y + 0.16)
def via2(c, x, y):
    c.rect('via2', x - 0.14, y - 0.14, x + 0.14, y + 0.14); c.rect('m2', x - 0.19, y - 0.19, x + 0.19, y + 0.19); c.rect('m3', x - 0.25, y - 0.25, x + 0.25, y + 0.25)
def via3(c, x, y):
    c.rect('via3', x - 0.16, y - 0.16, x + 0.16, y + 0.16); c.rect('m3', x - 0.25, y - 0.25, x + 0.25, y + 0.25); c.rect('m4', x - 0.25, y - 0.25, x + 0.25, y + 0.25)

# ---------------------------------------------------------------- row block
DGAP, SGAP, TP = 0.9, 1.8, 0.5
def row(c, x0, y0, sections, tracks_extra=(), dgap=None, full=False, order=(), share=(), rlog=None):
    """sections: list of (kind 'n'|'p', railnet, [dev,...]); dev = dict(name, W, L, D, G, S).  The rail carries railnet
    (substrate / well tap).  Returns (pins {net: (xa, xb, y)}, x_end, y_top)."""
    devs = [d for s in sections for d in s[2]]
    for d in devs: d['nf'], d['wf'] = nfing(d['W'])
    wmax = max(d['wf'] for d in devs)
    yd = y0 + 0.75; yc = yd + wmax + 0.48 + 0.4
    nets = []
    for s in sections:
        for n in [s[1]] + [d[k] for d in s[2] for k in 'DGS']:
            if n not in nets: nets.append(n)
    for n in tracks_extra:
        if n not in nets: nets.append(n)
    if order:                   # explicit bottom-to-top track order (rail first); share: (a, b) pairs on one track, left / right half
        nets = nets[:1] + [n for n in order if n in nets] + [n for n in nets[1:] if n not in order]
    sec = {b: a for a, b in share if a in nets and b in nets}
    lv = [n for n in nets if n not in sec]
    ty = {n: yc + i * TP for i, n in enumerate(lv)}
    for b, a in sec.items(): ty[b] = ty[a]
    span = {}
    def riser(net, cx, ytop):
        c.rect('m1', cx - 0.115, ytop - 0.05, cx + 0.115, ty[net]); via1(c, cx, ty[net])
        if rlog is not None: rlog.append((cx, min(ytop - 0.05, ty[net]) - 0.16, max(ytop - 0.05, ty[net]) + 0.16, net))
        a, b = span.get(net, (cx, cx)); span[net] = (min(a, cx), max(b, cx))
    x = x0
    for kind, rail, dl in sections:
        xs = x; x += 0.7
        for d in dl:
            t = mos(c, kind, x, yd, d['wf'], d['L'], d['nf'], d.get('flip', False))
            for i, cx in enumerate(t['sd']):
                net = d['S'] if i % 2 == 0 else d['D']
                if net == rail: c.rect('m1', cx - 0.115, y0 + 0.2, cx + 0.115, yd + 0.05)
                else: riser(net, cx, t['sdtop'])
            riser(d['G'], t['g'], t['gtop'])
            x = t['x1'] + (dgap or DGAP)
        xe = x - (dgap or DGAP) + (1.2 if dl and dl[-1].get('flip') else 0.6)    # a flipped last device has its gate pad on the right: keep the rail riser clear of it
        tp, tc = ('psd', 'psc') if kind == 'n' else ('nsd', 'nsc')
        c.rect(tp, xs, y0 + 0.03, xe, y0 + 0.37); c.rect(tc, xs + 0.12, y0 + 0.115, xe - 0.12, y0 + 0.285)
        c.rect('li', xs + 0.02, y0 + 0.115, xe - 0.02, y0 + 0.285)
        c.rect("mcon", xs + 0.12, y0 + 0.115, xe - 0.12, y0 + 0.285); c.rect('m1', xs, y0, xe, y0 + 0.4)
        riser(rail, xe - 0.25, y0 + 0.4)
        if kind == 'p': c.rect('nwell', xs - 0.2, y0 - 0.17, xe + 0.2, yd + wmax + 0.25)
        x = xe + SGAP
    for s_ in sections: span[s_[1]] = (x0 + 0.3, x - SGAP - 0.3)
    if full:
        for n in span: span[n] = (x0 + 0.3, x - SGAP - 0.3)
    pins = {}
    for n in nets:
        if n not in span: continue
        a, b = span[n]; a -= 0.3; b += 0.3
        if b - a < 1.2:
            if n in sec or n in sec.values(): a, b = (a + b) / 2 - 0.6, (a + b) / 2 + 0.6      # symmetric pairs: centred stub
            else: b = a + 1.2
        c.rect('m2', a, ty[n] - 0.16, b, ty[n] + 0.16); pins[n] = (a, b, ty[n])
    for b, a in sec.items():
        if b in pins and a in pins and pins[b][0] < pins[a][1] + 0.3 and pins[a][0] < pins[b][1] + 0.3: raise ValueError('shared track overlap %s %s' % (a, b))
    return pins, x - SGAP, yc + len(lv) * TP

# ---------------------------------------------------------------- netlist
def subckts(path):
    s = re.sub(r'\n\+', ' ', open(path).read()); out = {}
    for m in re.finditer(r'\.subckt (\S+)(.*?)\n(.*?)\.ends', s, re.S):
        out[m.group(1)] = (m.group(2).split(), [l.split() for l in m.group(3).split('\n') if l.strip() and not l.startswith('*')])
    return out
def par(tok, k, default=None):
    for t in tok:
        if t.lower().startswith(k.lower() + '='): return float(t.split('=')[1])
    return default
