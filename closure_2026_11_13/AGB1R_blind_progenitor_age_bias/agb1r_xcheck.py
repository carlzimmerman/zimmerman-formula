"""AGB1R cross-check (not a frozen step): brute-force grids for Part A's fork fits, to test that Nelder-Mead found the
global minimum of each constrained and unconstrained fit. Per fork (A = 0, 1, free):
 best:  3-D grid Om 0.05-0.70 (0.01), w0 -1.6-0.6 (0.025), wa -3-2 (0.05), then NM polish from the grid best;
 q0=0:  2-D grid Om (0.0025) x wa (0.01) with w0 tied, NM polish;
 never: the 3-D grid restricted to points with min q(z) >= 0 on [0, 2.33], penalty NM polish.
Usage: python3 agb1r_xcheck.py SAMPLE. Writes agb1r_xcheck_<SAMPLE>.json / .out."""
import os, sys, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agb1r_common import (load_des, sample_keep, SN, BAO, PartA, build_template, in_box, qz, QZ, minq, nm_polished,
                          q0 as q0f, dump, HERE)

S = sys.argv[1]
t0 = time.time()
logf = open(os.path.join(HERE, f"agb1r_xcheck_{S}.out"), "w")
def log(s):
    print(s, flush=True); logf.write(s + "\n"); logf.flush()
D = load_des(); keep = sample_keep(D, S)
TT = build_template("S"); sn = SN(D, keep, TT["spline"](D["zhd"][keep]))
model = PartA(sn, BAO("overlap" if S == "bao_overlap" else "all"))
mine = json.load(open(os.path.join(HERE, f"agb1r_A_{S}.json")))

Oms = np.round(np.arange(0.05, 0.7001, 0.01), 4); Oms[0] = 0.0501; Oms[-1] = 0.6999
w0s = np.round(np.arange(-1.6, 0.6001, 0.025), 4); was = np.round(np.arange(-3.0, 2.0001, 0.05), 4)
# feasibility mask for never-accelerated
feas = np.zeros((len(Oms), len(w0s), len(was)), bool)
W0, WA = np.meshgrid(w0s, was, indexing="ij")
for i, Om in enumerate(Oms):
    z = QZ[:, None, None]
    w = W0[None] + WA[None]*z/(1 + z)
    fde = (1 + z)**(3*(1 + W0[None] + WA[None]))*np.exp(-3*WA[None]*z/(1 + z))
    q = 0.5 + 1.5*w*(1 - Om)*fde/(Om*(1 + z)**3 + (1 - Om)*fde)
    feas[i] = q.min(axis=0) >= 0
log(f"{S}: 3-D grid {feas.size} points, {feas.sum()} satisfy q >= 0 on [0, 2.33]")

res = {}
for lab, A in (("A0", 0.0), ("A1", 1.0), ("Afree", None)):
    chi = np.full(feas.shape, np.inf)
    for i, Om in enumerate(Oms):
        for j, w0 in enumerate(w0s):
            for k, wa in enumerate(was):
                if in_box(Om, w0, wa): chi[i, j, k] = model.eval(Om, w0, wa, A)["chi2"]
    f = lambda x: model.eval(*x, A)["chi2"] if in_box(*x) else 1e10
    i, j, k = np.unravel_index(np.argmin(chi), chi.shape)
    xb, vb = nm_polished(f, [Oms[i], w0s[j], was[k]], [0.01, 0.05, 0.1])
    # q0 = 0
    best2 = (np.inf, None)
    for Om in np.arange(0.0525, 0.7, 0.0025):
        w0 = -1/(3*(1 - Om))
        for wa in np.arange(-3.0, 2.0001, 0.01):
            if in_box(Om, w0, wa):
                v = model.eval(Om, w0, wa, A)["chi2"]
                if v < best2[0]: best2 = (v, (Om, wa))
    g = lambda x: f((x[0], -1/(3*(1 - x[0])), x[1]))
    xq, vq = nm_polished(g, best2[1], [0.005, 0.05])
    # never
    cn = np.where(feas, chi, np.inf); i, j, k = np.unravel_index(np.argmin(cn), cn.shape)
    x = np.array([Oms[i], w0s[j], was[k]]); gridnever = float(cn[i, j, k])
    for L in (1e2, 1e4, 1e6, 1e8):
        h = lambda xx, L=L: (f(xx) + L*max(0.0, -minq(*xx)[0])**2) if f(xx) < 1e10 else 1e10
        x, _ = nm_polished(h, x, [0.005, 0.02, 0.05])
    vn = f(x); mq = minq(*x)[0]
    if mq < -1e-3: vn_use = gridnever; xn = (Oms[i], w0s[j], was[k])
    else: vn_use = vn; xn = tuple(x)
    fk = mine["forks"][lab]
    rec = dict(best=dict(chi2=vb, x=list(xb)), q0zero=dict(chi2=vq, Om=xq[0], wa=xq[1]),
               never=dict(chi2=vn_use, x=list(xn), grid_chi2=gridnever, minq=mq),
               dchi2_today=vq - vb, dchi2_never=vn_use - vb,
               nm_best=fk["best"]["chi2"], nm_q0=fk["q0zero"]["chi2"], nm_never=fk["never"]["chi2"])
    res[lab] = rec
    log(f"{S} {lab}: best grid+NM {vb:.4f} (NM run {fk['best']['chi2']:.4f}) at Om {xb[0]:.4f} w0 {xb[1]:+.4f} wa {xb[2]:+.4f}")
    log(f"   q0=0 grid+NM {vq:.4f} (NM run {fk['q0zero']['chi2']:.4f}) at Om {xq[0]:.4f} wa {xq[1]:+.4f};"
        f" dchi2_today {vq - vb:.4f} (NM run {fk['dchi2_today']:.4f})")
    log(f"   never grid {gridnever:.4f}, grid+NM {vn_use:.4f} (NM run {fk['never']['chi2']:.4f}) at Om {xn[0]:.4f}"
        f" w0 {xn[1]:+.4f} wa {xn[2]:+.4f} (min q {mq:+.2e}); dchi2_never {vn_use - vb:.4f} (NM run {fk['dchi2_never']:.4f})")
res["runtime_s"] = time.time() - t0
dump(res, os.path.join(HERE, f"agb1r_xcheck_{S}.json"))
log(f"done in {res['runtime_s']:.0f} s")
