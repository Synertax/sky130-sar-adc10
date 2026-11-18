"""xschem .sch / .sym writer, connectivity self-check and PNG preview for the cells in design.py."""
import os, re, math
import design

XS = os.environ.get('XSCHEM_SKY130', '/home/claude/tools/xs130')
HDR = 'v {xschem version=3.4.8RC file_version=1.3}\nG {}\nK {}\nV {}\nS {}\nF {}\nE {}\n'
SUPPLY = ('VDD', 'VSS', 'VREFP', 'VREFN')
DEV = {  # xschem "devices" library pins
    'ipin': {'p': (0, 0)}, 'opin': {'p': (0, 0)}, 'iopin': {'p': (0, 0)}, 'lab_pin': {'p': (0, 0)},
    'lab_wire': {'p': (0, 0)}, 'noconn': {'p': (0, 0)}, 'gnd': {'p': (0, 0)},
    'vsource': {'p': (0, -30), 'm': (0, 30)}, 'res': {'P': (0, -30), 'M': (0, 30)}, 'capa': {'p': (0, -30), 'm': (0, 30)},
}
_cache = {}


def snap(v):
    return int(round(v / 10.0)) * 10


def parse_sym(text):
    """returns dict(pins={name:(x,y)}, order=[names], prims=[...])"""
    pins, order, prims = {}, [], []
    for ln in text.split('\n'):
        m = re.match(r'B 5 (\S+) (\S+) (\S+) (\S+) \{name=(\S+)', ln)
        if m:
            x = (float(m.group(1)) + float(m.group(3))) / 2
            y = (float(m.group(2)) + float(m.group(4))) / 2
            pins[m.group(5)] = (snap(x), snap(y))
            order.append(m.group(5))
            continue
        m = re.match(r'L \d+ (\S+) (\S+) (\S+) (\S+)', ln)
        if m:
            prims.append(('L',) + tuple(float(m.group(i)) for i in range(1, 5)))
            continue
        m = re.match(r'B \d+ (\S+) (\S+) (\S+) (\S+)', ln)
        if m:
            x1, y1, x2, y2 = (float(m.group(i)) for i in range(1, 5))
            prims += [('L', x1, y1, x2, y1), ('L', x2, y1, x2, y2), ('L', x2, y2, x1, y2), ('L', x1, y2, x1, y1)]
            continue
        m = re.match(r'P \d+ (\d+) (.*?) \{', ln)
        if m:
            v = [float(t) for t in m.group(2).split()]
            for i in range(0, len(v) - 2, 2):
                prims.append(('L', v[i], v[i + 1], v[i + 2], v[i + 3]))
            continue
        m = re.match(r'A \d+ (\S+) (\S+) (\S+) (\S+) (\S+)', ln)
        if m:
            prims.append(('A',) + tuple(float(m.group(i)) for i in range(1, 6)))
            continue
        m = re.match(r'T \{(.*?)\} (\S+) (\S+) (\d) (\d) (\S+) (\S+)', ln)
        if m:
            prims.append(('T', m.group(1), float(m.group(2)), float(m.group(3)), int(m.group(4)), int(m.group(5)), float(m.group(6))))
    return dict(pins=pins, order=order, prims=prims)


def symref(i):
    if i.kind == 'mos':
        return 'sky130_fd_pr/%s.sym' % (i.kw['model'].replace('nfet_', 'nfet3_') if use3(i) else i.kw['model'])
    if i.kind == 'vpp':
        return 'sar10_vpp.sym' if 'floatm3' in design.P['UNITCAP'] else 'sky130_fd_pr/vpp_cap.sym'
    if i.kind == 'mim':
        return 'sky130_fd_pr/cap_mim_m3_1.sym'
    if i.kind == 'std':
        return 'sky130_stdcells/%s.sym' % i.kw['cell']
    if i.kind == 'sub':
        return '%s.sym' % i.kw['cell']
    if i.kind == 'dev':
        return 'devices/%s.sym' % i.kw['dev']
    raise ValueError(i.kind)


def use3(i):
    """NMOS whose bulk is VSS but whose source is not: drawn with the 3-terminal symbol (body=VSS attribute)"""
    return i.kind == 'mos' and i.kw['model'].startswith('nfet_') and i.conn['B'] == 'VSS' and i.conn['S'] != 'VSS' and i.conn['D'] != 'VSS'


def sym_of(i, cells):
    ref = symref(i)
    if ref in _cache:
        return _cache[ref]
    if i.kind == 'sub':
        s = parse_sym(symbol_text(cells[i.kw['cell']]))
    elif i.kind == 'dev':
        s = dict(pins=DEV[i.kw['dev']], order=list(DEV[i.kw['dev']]), prims=[])
    else:
        _p = os.path.join(XS, ref)
        if not os.path.exists(_p): _p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ref)
        s = parse_sym(open(_p).read())
    _cache[ref] = s
    return s


def xf(px, py, rot, flip):
    if flip:
        px = -px
    if rot == 1:
        px, py = -py, px
    elif rot == 2:
        px, py = -px, -py
    elif rot == 3:
        px, py = py, -px
    return px, py


def pinpos(i, pin, cells):
    px, py = sym_of(i, cells)['pins'][pin]
    dx, dy = xf(px, py, getattr(i, 'rot', 0), i.flip)
    return (i.x + dx, i.y + dy)


# ------------------------------------------------------------------ symbols
def sym_geometry(c):
    """pin coordinates for a generated symbol"""
    side = {s: [p for p in c.pins if p[2] == s] for s in 'LRTB'}
    if c.symshape == 'comp':
        pos = {'INP': (-80, -40), 'INN': (-80, 40), 'OUTP': (100, -20), 'OUTN': (100, 20), 'CLK': (0, 80), 'VDD': (0, -80), 'VSS': (-40, 80)}
        return pos, None
    nl, nr, nt, nb = (len(side[s]) for s in 'LRTB')
    tb_pitch = 80
    W = max(160, tb_pitch * max(nt, nb) + 40)
    W = int(math.ceil(W / 40.0)) * 40
    rows = max(nl, nr, 1)
    H = 20 * rows + 40 + (20 if nt else 0) + (20 if nb else 0)
    H = int(math.ceil(H / 40.0)) * 40
    if c.symshape in ('dac', 'switch'):
        H = max(H, 160)
    pos = {}
    y0 = -int(round((max(nl, nr, 1) - 1) * 10 / 20.0)) * 20
    for s, x in (('L', -W // 2 - 20), ('R', W // 2 + 20)):
        for k, p in enumerate(side[s]):
            pos[p[0]] = (x, y0 + 20 * k)
    for s, y in (('T', -H // 2 - 20), ('B', H // 2 + 20)):
        n = len(side[s])
        x0 = -((n - 1) * tb_pitch) // 2
        x0 = int(round(x0 / 20.0)) * 20
        for k, p in enumerate(side[s]):
            pos[p[0]] = (x0 + tb_pitch * k, y)
    return pos, (W, H)


def symbol_text(c):
    pos, wh = sym_geometry(c)
    o = ['v {xschem version=3.4.8RC file_version=1.3}', 'G {}',
         'K {type=subcircuit\nformat="@name @pinlist @symname"\ntemplate="name=x1"\n}', 'V {}', 'S {}', 'F {}', 'E {}']
    L = lambda x1, y1, x2, y2: o.append('L 4 %g %g %g %g {}' % (x1, y1, x2, y2))
    T = lambda s, x, y, rot=0, flip=0, sz=0.2, extra='': o.append('T {%s} %g %g %d %d %g %g {%s}' % (s, x, y, rot, flip, sz, sz, extra))
    if c.symshape == 'comp':
        for a, b in (((-60, -80), (-60, 80)), ((-60, 80), (80, 0)), ((80, 0), (-60, -80))):
            L(a[0], a[1], b[0], b[1])
        L(-80, -40, -60, -40); L(-80, 40, -60, 40); L(45, -20, 100, -20); L(45, 20, 100, 20)
        L(0, 80, 0, 46); L(0, -80, 0, -46); L(-40, 80, -40, 69)
        T('+', -54, -52, sz=0.35); T('-', -53, 28, sz=0.35)
        T('INP', -85, -56, flip=1, sz=0.15); T('INN', -85, 24, flip=1, sz=0.15)
        T('OUTP', 62, -36, sz=0.15); T('OUTN', 62, 4, sz=0.15)
        T('CLK', 5, 62, sz=0.15); T('VDD', 5, -76, sz=0.15); T('VSS', -35, 72, sz=0.15)
        T('@name', -60, -105, sz=0.25); T('@symname', -50, -8, sz=0.18)
    else:
        W, H = wh
        w, h = W // 2, H // 2
        L(-w, -h, w, -h); L(w, -h, w, h); L(w, h, -w, h); L(-w, h, -w, -h)
        for p in c.pins:
            x, y = pos[p[0]]
            if p[2] == 'L':
                L(x, y, -w, y); T(p[0], -w + 6, y - 6, sz=0.18)
            elif p[2] == 'R':
                L(x, y, w, y); T(p[0], w - 6, y - 6, flip=1, sz=0.18)
            elif p[2] == 'T':
                L(x, y, x, -h); T(p[0], x, -h + 4, sz=0.18, extra='hcenter=true')
            else:
                L(x, y, x, h); T(p[0], x, h - 18, sz=0.18, extra='hcenter=true')
        T('@name', -w, -h - 22 - (20 if any(p[2] == 'T' for p in c.pins) else 0), sz=0.25)
        if c.symshape == 'dac':      # capacitor glyph
            L(-16, -6, 16, -6); L(-16, 6, 16, 6); L(0, -6, 0, -22); L(0, 6, 0, 22)
            T('@symname', 0, 30, sz=0.2, extra='hcenter=true')
            T('2 x %d C' % getattr(c, 'm', 1), 0, -44, sz=0.2, extra='hcenter=true')
        elif c.symshape == 'switch':  # switch glyph
            L(-40, 0, -14, 0); L(14, 0, 40, 0); L(-14, 0, 12, -14)
            o.append('A 4 -14 0 3 0 360 {}'); o.append('A 4 14 0 3 0 360 {}')
            T('@symname', 0, 20, sz=0.2, extra='hcenter=true')
            T('bootstrapped', 0, -44, sz=0.18, extra='hcenter=true')
        else:
            T('@symname', 0, -10, sz=0.25, extra='hcenter=true')
    for p in c.pins:
        x, y = pos[p[0]]
        o.append('B 5 %g %g %g %g {name=%s dir=%s}' % (x - 2.5, y - 2.5, x + 2.5, y + 2.5, p[0], p[1]))
    return '\n'.join(o) + '\n'


# ------------------------------------------------------------------ schematic assembly
class Sch:
    """resolved drawing of one cell: instances, wire segments, labels, ports; with connectivity check"""

    def __init__(s, c, cells):
        s.c, s.cells = c, cells
        s.segs = []      # (net, x1,y1,x2,y2)
        s.labs = []      # (net, x, y, rot, kind)
        s.ports = []     # (name, dir, x, y, flip)
        s.ncs = []
        s.pin_at = {}    # (inst, pin) -> (x,y)
        for i in c.insts:
            sy = sym_of(i, cells)
            for p in sy['pins']:
                if p in i.conn:
                    s.pin_at[(i.name, p)] = pinpos(i, p, cells)
                elif i.kind != 'std' and not (p == 'B' and use3(i)):
                    raise ValueError('%s.%s: pin %s not connected' % (c.name, i.name, p))
        s.build()

    def pt(s, p):
        if isinstance(p, str):
            if p.startswith('port:'):
                for (n, d, x, y, f) in s.ports:
                    if n == p[5:]:
                        return (x, y)
                raise KeyError(p)
            a, b = p.split('.')
            return s.pin_at[(a, b)]
        return p

    def build(s):
        c = s.c
        for (name, x, y, flip) in getattr(c, 'portspec', []):
            d = [p[1] for p in c.pins if p[0] == name][0]
            s.ports.append((name, d, x, y, flip))
        for net, pts in c.wires:
            mode = 'h'
            cur = None
            for p in pts:
                if p in ('h', 'v'):
                    mode = p
                    continue
                q = s.pt(p)
                if cur is not None and cur != q:
                    if cur[0] == q[0] or cur[1] == q[1]:
                        s.segs.append((net, cur[0], cur[1], q[0], q[1]))
                    else:
                        mid = (q[0], cur[1]) if mode == 'h' else (cur[0], q[1])
                        s.segs.append((net, cur[0], cur[1], mid[0], mid[1]))
                        s.segs.append((net, mid[0], mid[1], q[0], q[1]))
                    mode = 'h'
                cur = q
        for lb in c.labels:
            net, p, rot = lb[:3]
            x, y = s.pt(p)
            s.labs.append((net, x, y, rot, lb[3] if len(lb) > 3 else 'lab_pin'))
        for p in getattr(c, 'ncspec', []):
            s.ncs.append(s.pt(p))
        # bulk ties and automatic labels on pins nothing else touches
        touched = s.touched()
        tied = set()
        for i in c.insts:
            if i.kind == 'mos' and not use3(i):
                b, sp, dp = s.pin_at[(i.name, 'B')], s.pin_at[(i.name, 'S')], s.pin_at[(i.name, 'D')]
                if b not in touched:
                    if i.conn['B'] == i.conn['S']:
                        s.segs.append((i.conn['B'], b[0], b[1], sp[0], sp[1])); tied.add(b)
                    elif i.conn['B'] == i.conn['D']:
                        s.segs.append((i.conn['B'], b[0], b[1], dp[0], dp[1])); tied.add(b)
        for i in c.insts:
            sy = sym_of(i, s.cells)
            for p, (px, py) in sy['pins'].items():
                if p not in i.conn:
                    continue
                q = s.pin_at[(i.name, p)]
                if q in touched or q in tied:
                    continue
                dx, dy = xf(px, py, getattr(i, 'rot', 0), i.flip)
                if i.kind == 'mos' and p in ('D', 'S', 'B'):
                    rot = 0 if i.flip else 2
                    if getattr(i, 'rot', 0) in (1, 3):
                        rot = 2
                    elif p != 'B':
                        e = (q[0], q[1] + (20 if dy > 0 else -20))
                        s.segs.append((i.conn[p], q[0], q[1], e[0], e[1]))
                        q = e
                elif i.kind in ('sub', 'dev') and dx == 0 and dy != 0 and i.kind == 'sub':
                    e = (q[0], q[1] + (20 if dy > 0 else -20))
                    s.segs.append((i.conn[p], q[0], q[1], e[0], e[1]))
                    q = e
                    rot = 2
                else:
                    rot = 0 if dx < 0 else 2
                s.labs.append((i.conn[p], q[0], q[1], rot, 'lab_pin'))
        s.name_unlabeled()
        s.split()
        s.check()

    def touched(s):
        t = set()
        for (n, x1, y1, x2, y2) in s.segs:
            t.add((x1, y1)); t.add((x2, y2))
        for l in s.labs:
            t.add((l[1], l[2]))
        for p in s.ports:
            t.add((p[2], p[3]))
        for p in s.ncs:
            t.add(p)
        # pins lying in the interior of a segment
        for q in s.pin_at.values():
            for (n, x1, y1, x2, y2) in s.segs:
                if on_seg(q, x1, y1, x2, y2):
                    t.add(q)
        return t

    def nodes(s):
        """all electrical points: (x,y) -> list of (net, description)"""
        N = {}
        for (iname, p), q in s.pin_at.items():
            i = [k for k in s.c.insts if k.name == iname][0]
            N.setdefault(q, []).append((i.conn[p], '%s.%s' % (iname, p)))
        for (net, x, y, rot, kind) in s.labs:
            N.setdefault((x, y), []).append((net, 'label'))
        for (name, d, x, y, f) in s.ports:
            N.setdefault((x, y), []).append((name, 'port'))
        return N

    def split(s):
        """split segments at every node / segment endpoint in their interior, so every connection is end-to-end"""
        pts = set(s.nodes().keys())
        for (n, x1, y1, x2, y2) in s.segs:
            pts.add((x1, y1)); pts.add((x2, y2))
        out = []
        for (n, x1, y1, x2, y2) in s.segs:
            assert x1 == x2 or y1 == y2, 'non-manhattan wire in %s net %s' % (s.c.name, n)
            inner = sorted(p for p in pts if on_seg(p, x1, y1, x2, y2, strict=True))
            if (x1, y1) > (x2, y2):
                inner = inner[::-1]
            chain = [(x1, y1)] + inner + [(x2, y2)]
            for a, b in zip(chain, chain[1:]):
                if a != b:
                    out.append((n, a[0], a[1], b[0], b[1]))
        s.segs = sorted(set(out))

    def name_unlabeled(s):
        """give every wired internal net without label/port a lab_wire so net names survive netlisting"""
        named = set(l[0] for l in s.labs) | set(p[0] for p in s.ports)
        by = {}
        for sg in s.segs:
            by.setdefault(sg[0], []).append(sg)
        for net, segs in by.items():
            if net in named:
                continue
            hs = [g for g in segs if g[2] == g[4]] or segs
            g = max(hs, key=lambda g: abs(g[3] - g[1]) + abs(g[4] - g[2]))
            L = abs(g[3] - g[1]) + abs(g[4] - g[2])
            for f in (0.5, 0.4, 0.6, 0.3, 0.7, 0.2, 0.8):
                x, y = snap(g[1] + (g[3] - g[1]) * f), snap(g[2] + (g[4] - g[2]) * f)
                if not any(o[0] != net and on_seg((x, y), o[1], o[2], o[3], o[4]) for o in s.segs):
                    break
            s.labs.append((net, x, y, 0, 'lab_wire'))

    def check(s):
        N = s.nodes()
        par = {}

        def find(a):
            while par.setdefault(a, a) != a:
                par[a] = par[par[a]]
                a = par[a]
            return a

        def union(a, b):
            par[find(a)] = find(b)
        for q in N:
            find(q)
        for (n, x1, y1, x2, y2) in s.segs:
            union((x1, y1), (x2, y2))
        # sanity: no node in the interior of a segment after split; no overlapping collinear different-net segments
        for (n, x1, y1, x2, y2) in s.segs:
            for q in N:
                assert not on_seg(q, x1, y1, x2, y2, strict=True)
        comp = {}
        for q in list(par):
            comp.setdefault(find(q), []).append(q)
        netcomps = {}
        for root, pts in comp.items():
            nets = set()
            for q in pts:
                for (net, what) in N.get(q, []):
                    nets.add(net)
            segnets = set(g[0] for g in s.segs if find((g[1], g[2])) == root)
            if len(nets | segnets) > 1:
                raise ValueError('%s: SHORT between nets %s at %s' % (s.c.name, sorted(nets | segnets), pts[:4]))
            if not nets:
                raise ValueError('%s: dangling wire %s at %s' % (s.c.name, segnets, pts[:3]))
            net = list(nets)[0]
            haslabel = any(w in ('label', 'port') for q in pts for (nn, w) in N.get(q, []))
            netcomps.setdefault(net, []).append(haslabel)
        for net, cs in netcomps.items():
            if len(cs) > 1 and not all(cs):
                raise ValueError('%s: net %s is split into %d pieces and one has no label' % (s.c.name, net, len(cs)))
        # every wire segment crossing check: endpoints only (crossings without endpoint are not connections)
        want = set(v for i in s.c.insts for v in i.conn.values() if not (i.kind == 'std' and False))
        missing = set(p[0] for p in s.c.pins) - set(netcomps)
        if getattr(s.c, 'is_tb', False):
            missing = set()
        if missing:
            raise ValueError('%s: ports %s not drawn' % (s.c.name, sorted(missing)))
        return True

    # ---------------------------------------------------------------- output
    def text(s):
        c = s.c
        o = [HDR.rstrip('\n')]
        for (t, x, y, sz) in getattr(c, 'texts', []):
            o.append('T {%s} %g %g 0 0 %g %g {}' % (t, x, y, sz, sz))
        for (x, y, val) in getattr(c, 'code', []):
            o.append('C {code_shown.sym} %g %g 0 0 {name=SIM only_toplevel=false value="%s"}' % (x, y, val))
        for (n, x1, y1, x2, y2) in s.segs:
            o.append('N %g %g %g %g {lab=%s}' % (x1, y1, x2, y2, n))
        k = 0
        for (name, d, x, y, flip) in s.ports:
            k += 1
            o.append('C {%s.sym} %g %g 0 %d {name=p%d lab=%s}' % ({'in': 'ipin', 'out': 'opin', 'inout': 'iopin'}[d], x, y, flip, k, name))
        for (net, x, y, rot, kind) in s.labs:
            k += 1
            if kind == 'gnd':
                o.append('C {gnd.sym} %g %g 0 0 {name=l%d lab=0}' % (x, y, k))
                continue
            o.append('C {%s.sym} %g %g %d 0 {name=l%d sig_type=std_logic lab=%s}' % (kind, x, y, rot, k, net))
        for (x, y) in s.ncs:
            k += 1
            o.append('C {noconn.sym} %g %g 2 0 {name=nc%d}' % (x, y, k))
        for i in c.insts:
            o.append('C {%s} %g %g %d %d {%s}' % (symref(i), i.x, i.y, getattr(i, 'rot', 0), i.flip, inst_attrs(i)))
        return '\n'.join(o) + '\n'


def on_seg(p, x1, y1, x2, y2, strict=False):
    x, y = p
    if x1 == x2 == x and min(y1, y2) <= y <= max(y1, y2):
        return not strict or (y != y1 and y != y2)
    if y1 == y2 == y and min(x1, x2) <= x <= max(x1, x2):
        return not strict or (x != x1 and x != x2)
    return False


MOS_EXPR = ('ad="expr(\'int((@nf + 1)/2) * @W / @nf * 0.29\')" pd="expr(\'2*int((@nf + 1)/2) * (@W / @nf + 0.29)\')" '
            'as="expr(\'int((@nf + 2)/2) * @W / @nf * 0.29\')" ps="expr(\'2*int((@nf + 2)/2) * (@W / @nf + 0.29)\')" '
            'nrd="expr(\'0.29 / @W \')" nrs="expr(\'0.29 / @W \')" sa=0 sb=0 sd=0')


def inst_attrs(i):
    k = i.kw
    if i.kind == 'mos':
        return 'name=%s L=%g W=%g %snf=%d mult=1 %s model=%s spiceprefix=X' % (
            i.name, k['L'], k['W'], 'body=VSS ' if use3(i) else '', k['nf'], MOS_EXPR, k['model'])
    if i.kind == 'vpp':
        return 'name=%s model=%s mult=%d spiceprefix=X' % (i.name, design.P['UNITCAP'], k['mult'])
    if i.kind == 'mim':
        return 'name=%s model=cap_mim_m3_1 W=%g L=%g MF=1 spiceprefix=X' % (i.name, k['W'], k['L'])
    if i.kind == 'std':
        return 'name=%s VGND=VSS VNB=VSS VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ ' % (i.name.lower() if i.name[0] in 'xX' else 'x' + i.name)
    if i.kind == 'sub':
        return 'name=%s' % (i.name if i.name[0] in 'xX' else 'x' + i.name)
    if i.kind == 'dev':
        return 'name=%s %s' % (i.name, k['attrs'])
    raise ValueError(i.kind)


# ------------------------------------------------------------------ preview
def render(sch, path, scale=1.0):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Arc
    c = sch.c
    xs, ys = [], []
    fig, ax = plt.subplots()

    def line(x1, y1, x2, y2, col='k', lw=0.8):
        ax.plot([x1, x2], [y1, y2], color=col, lw=lw, solid_capstyle='round')
        xs.extend([x1, x2]); ys.extend([y1, y2])

    for i in c.insts:
        sy = sym_of(i, sch.cells)
        rot = getattr(i, 'rot', 0)
        for pr in sy['prims']:
            if pr[0] == 'L':
                a = xf(pr[1], pr[2], rot, i.flip); b = xf(pr[3], pr[4], rot, i.flip)
                line(i.x + a[0], i.y + a[1], i.x + b[0], i.y + b[1], '#207020')
            elif pr[0] == 'A':
                cx, cy = xf(pr[1], pr[2], rot, i.flip)
                ax.add_patch(Arc((i.x + cx, i.y + cy), 2 * pr[3], 2 * pr[3], color='#207020', lw=0.8))
            elif pr[0] == 'T':
                t = pr[1]
                if t.startswith('@name'):
                    t = i.name
                elif t in ('@symname', '@model'):
                    t = i.kw.get('cell', i.kw.get('model', '')) if i.kind != 'vpp' else 'vpp x%d' % i.kw['mult']
                    if i.kind == 'mos':
                        t = '%s %g/%g' % (i.kw['model'].replace('_01v8', ''), i.kw['W'], i.kw['L'])
                elif '@' in t or len(t) > 12:
                    continue
                tx, ty = xf(pr[2], pr[3], rot, i.flip)
                ha = 'right' if (pr[5] ^ i.flip) else 'left'
                ax.text(i.x + tx, i.y + ty, t, fontsize=max(3.0, 22 * pr[6]) * scale, color='#804000', ha=ha, va='top')
    for (n, x1, y1, x2, y2) in sch.segs:
        line(x1, y1, x2, y2, '#1040c0', 1.0)
    cnt = {}
    for (n, x1, y1, x2, y2) in sch.segs:
        for q in ((x1, y1), (x2, y2)):
            cnt[q] = cnt.get(q, 0) + 1
    for q, k in cnt.items():
        if k >= 3:
            ax.plot([q[0]], [q[1]], 'o', color='#1040c0', ms=2.5)
    for (net, x, y, rot, kind) in sch.labs:
        if kind == 'gnd':
            ax.plot([x], [y], 'v', color='k', ms=5)
        elif kind == 'lab_wire':
            ax.text(x, y - 2, net, fontsize=5 * scale, color='#a000a0', ha='center', va='bottom')
        else:
            ax.plot([x], [y], 's', color='#c00000', ms=1.5)
            ax.text(x + (6 if rot == 2 else -6), y, net, fontsize=6 * scale, color='#c00000', ha='left' if rot == 2 else 'right', va='center')
    for (name, d, x, y, flip) in sch.ports:
        left = (d == 'in') ^ bool(flip)
        ax.plot([x], [y], '>' if d == 'in' else 'D', color='#c00000', ms=4)
        ax.text(x + (-12 if left else 12), y, name, fontsize=7.5 * scale, color='#c00000', ha='right' if left else 'left', va='center', weight='bold')
        xs.append(x); ys.append(y)
    for (x, y) in sch.ncs:
        ax.plot([x], [y], 'x', color='gray', ms=4)
    for (t, x, y, sz) in getattr(c, 'texts', []):
        ax.text(x, y, t, fontsize=18 * sz * scale, color='#303030', ha='left', va='top', wrap=True)
        xs.append(x); ys.append(y)
    w, h = max(xs) - min(xs) + 200, max(ys) - min(ys) + 120
    ax.set_xlim(min(xs) - 120, max(xs) + 120); ax.set_ylim(max(ys) + 60, min(ys) - 60)
    ax.set_aspect('equal'); ax.axis('off')
    fig.set_size_inches(max(6, w / 110.0), max(4, h / 110.0))
    fig.savefig(path, dpi=110, bbox_inches='tight')
    plt.close(fig)


def write_all(cells, outdir, preview=None):
    os.makedirs(outdir, exist_ok=True)
    res = {}
    allc = dict(cells)
    for t in design.testbenches():
        allc[t.name] = t
    cace = {t.name: t for t in design.cace_templates()}
    allc.update(cace)
    for name, c in allc.items():
        sch = Sch(c, cells)
        od = os.path.join(outdir, 'cace', 'templates') if name in cace else outdir
        os.makedirs(od, exist_ok=True)
        open(os.path.join(od, name + '.sch'), 'w').write(sch.text())
        if name in cells:
            open(os.path.join(outdir, name + '.sym'), 'w').write(symbol_text(c))
        if preview:
            os.makedirs(preview, exist_ok=True)
            render(sch, os.path.join(preview, name + '.png'))
        res[name] = sch
    return res


if __name__ == '__main__':
    import sys
    cells = design.build()
    only = sys.argv[3:] if len(sys.argv) > 3 else None
    if only:
        for n in only:
            sch = Sch(cells[n], cells)
            render(sch, os.path.join(sys.argv[2], n + '.png'))
            print(n, 'ok', len(sch.segs), 'segments')
    else:
        write_all(cells, sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
        print('wrote', len(cells), 'cells')
