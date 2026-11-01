"""AQUAL point mass in a uniform field, finite volume on (ln r, theta). Section 4.2. Units G=M=a0=1.
Writes cache/efe_<foot>.npz (s, M) and partials/efe_<foot>.json."""
from crg1_core import *
import scipy.sparse as sp, scipy.sparse.linalg as spl
import sys

def mu(x): return x / (1 + x)

def ye_of(foot):
    v = [float(r["log_eN_noclu"]) for r in csv.DictReader(open(os.path.join(INP, "clusters", "chae21_env.csv"))) if r["log_eN_noclu"].strip() not in ("", "nan")]
    return 10 ** np.median(v) * 1.2e-10 / A0[foot]

def solve(ye, rmin=0.05, ncell_dec=60, nth=64, tol=1e-9, maxit=3000, conv="phi"):
    xe = 0.5 * (ye + math.sqrt(ye * ye + 4 * ye))
    rmax = 60 / xe
    nr = int(round(math.log10(rmax / rmin) * ncell_dec))
    uf = np.linspace(math.log(rmin), math.log(rmax), nr + 1); du = uf[1] - uf[0]
    rf = np.exp(uf); rc = np.exp(0.5 * (uf[1:] + uf[:-1]))
    thf = np.linspace(0, math.pi, nth + 1); dth = thf[1] - thf[0]; thc = 0.5 * (thf[1:] + thf[:-1])
    w = np.cos(thf[:-1]) - np.cos(thf[1:])          # exact solid-angle weights, sum 2
    Le = 1 / (1 + xe); mue = mu(xe)
    rghost = rf[-1] * math.exp(0.5 * du)
    rp = rghost * np.sqrt(np.sin(thc) ** 2 + np.cos(thc) ** 2 / (1 + Le))
    Pg = xe * rghost * np.cos(thc) - 1 / (mue * math.sqrt(1 + Le) * rp)
    # initial state: isolated deep field + uniform
    Ph = xe * np.outer(rc, np.cos(thc)) + np.log(rc)[:, None]
    idx = lambda i, j: i * nth + j
    N = nr * nth
    # geometry
    Ar = rf[:, None] ** 2 * w[None, :]                 # area of radial face (per 2 pi)
    dA_th = 0.5 * (rf[1:] ** 2 - rf[:-1] ** 2)[:, None] * np.sin(thf[1:-1])[None, :]  # area of theta face
    rhs0 = np.zeros(N)
    rhs0[idx(0, np.arange(nth))] = (1 / rmin ** 2) * Ar[0, :]   # div(mu grad Phi) cell balance: outward face flux at inner boundary is -(1/rmin^2) A
    prev = None
    for it in range(1, maxit + 1):
        # radial faces interior i=1..nr-1 and outer face nr
        Pe = np.vstack([Ph, Pg[None, :]])              # nr+1 rows incl ghost
        rcE = np.append(rc, rghost)
        gn = (Pe[1:] - Pe[:-1]) / (rf[1:, None] * du)  # normal derivative at faces 1..nr
        dth_c = np.zeros_like(Pe)
        dth_c[:, 1:-1] = (Pe[:, 2:] - Pe[:, :-2]) / (2 * dth)
        dth_c[:, 0] = (Pe[:, 1] - Pe[:, 0]) / (2 * dth)
        dth_c[:, -1] = (Pe[:, -1] - Pe[:, -2]) / (2 * dth)
        gt = 0.5 * (dth_c[1:] / rcE[1:, None] + dth_c[:-1] / rcE[:-1, None])
        mu_r = mu(np.sqrt(gn ** 2 + gt ** 2))
        # theta faces
        gnt = (Ph[:, 1:] - Ph[:, :-1]) / (rc[:, None] * dth)
        dPdu = np.zeros_like(Pe)
        dPdu[1:-1] = (Pe[2:] - Pe[:-2]) / (2 * du)
        dPdu[0] = (Pe[1] - Pe[0]) / du
        dPdu[-1] = (Pe[-1] - Pe[-2]) / du
        gr_c = dPdu[:-1] / rc[:, None]
        gtt = 0.5 * (gr_c[:, 1:] + gr_c[:, :-1])
        mu_t = mu(np.sqrt(gnt ** 2 + gtt ** 2))
        # assemble
        I, J, V = [], [], []
        diag = np.zeros(N); rhs = rhs0.copy()
        cr = mu_r[:-1] * Ar[1:-1, :] / (rf[1:-1, None] * du)   # faces between i, i+1
        ii = idx(np.arange(nr - 1)[:, None], np.arange(nth)[None, :]).ravel()
        jj = ii + nth; c = cr.ravel()
        I += [ii, jj]; J += [jj, ii]; V += [c, c]
        np.add.at(diag, ii, -c); np.add.at(diag, jj, -c)
        co = mu_r[-1] * Ar[-1, :] / (rf[-1] * du)
        io = idx(nr - 1, np.arange(nth))
        np.add.at(diag, io, -co); rhs[io] -= co * Pg
        ct = mu_t * dA_th / (rc[:, None] * dth)
        ia = idx(np.arange(nr)[:, None], np.arange(nth - 1)[None, :]).ravel()
        ib = ia + 1; c = ct.ravel()
        I += [ia, ib]; J += [ib, ia]; V += [c, c]
        np.add.at(diag, ia, -c); np.add.at(diag, ib, -c)
        I.append(np.arange(N)); J.append(np.arange(N)); V.append(diag)
        A = sp.csc_matrix((np.concatenate(V), (np.concatenate(I), np.concatenate(J))), shape=(N, N))
        new = spl.spsolve(A, rhs).reshape(nr, nth)
        ch = float(np.max(np.abs(new - Ph) / np.maximum(np.abs(new), 1e-12)))
        Ph = new
        if ch < tol: break
    # M at faces 1..nr
    Pe = np.vstack([Ph, Pg[None, :]])
    gn = (Pe[1:] - Pe[:-1]) / (rf[1:, None] * du)
    M = rf[1:] ** 2 * (w[None, :] * gn).sum(1) / 2
    return rf[1:], M, dict(x_e=xe, y_e=ye, iters=it, last_change=ch, nr=nr)

def Miso(s): return nu(1.0 / s ** 2)

class CS:
    def __init__(s, sv, Mv):
        s.s, s.M = np.asarray(sv), np.asarray(Mv)
        s.ls = np.log(s.s); s.C = s.M / Miso(s.s)
    def __call__(s, x):
        x = np.asarray(x, float)
        out = np.interp(np.log(x), s.ls, s.C)
        out[x < s.s[0]] = 1.0
        hi = x > s.s[-1]
        out[hi] = s.M[-1] / Miso(x[hi])
        return out

def get(foot, reading="own"):
    if reading == "own":
        d = np.load(os.path.join(CACHE, "efe_%s.npz" % foot))
    else:
        d = np.load(os.path.join(INP, "clusters", "efe_table_%s.npz" % foot))
    return CS(d["s"], d["M"])

def main():
    for foot in ("canonical", "alt"):
        if have_part("efe_" + foot) and os.path.exists(os.path.join(CACHE, "efe_%s.npz" % foot)): continue
        t = time.time()
        s, M, info = solve(ye_of(foot))
        np.savez(os.path.join(CACHE, "efe_%s.npz" % foot), s=s, M=M)
        g = np.load(os.path.join(INP, "clusters", "efe_table_%s.npz" % foot))
        Mi = np.exp(np.interp(np.log(g["s"]), np.log(s), np.log(M)))
        rel = np.abs(Mi / g["M"] - 1)
        Cg = g["M"] / Miso(g["s"]); Co = Mi / Miso(g["s"])
        info.update(nfaces=len(s), n_given=len(g["s"]), s_own=[s[0], s[-1]], s_given=[g["s"][0], g["s"][-1]],
                    max_rel_diff_M=rel.max(), max_rel_diff_M_excl_ends=rel[3:-3].max(),
                    max_rel_diff_at_s=g["s"][rel.argmax()], x_e_given=float(g["x_e"]), y_e_given=float(g["y_e"]),
                    max_abs_diff_C=float(np.abs(Cg - Co).max()))
        save_part("efe_" + foot, info); log("efe %s %.1fs %s" % (foot, time.time() - t, info))

if __name__ == "__main__": main()
