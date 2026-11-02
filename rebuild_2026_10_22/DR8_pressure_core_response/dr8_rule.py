"""DR8: the stated rule and its variants, standalone. M_i = M0(r_i), P = M0(r0) r_i / r0.
RULE: r_i/r_f = 1 + M_b(r_f)/(M_i + P). RULE_F: r_i/r_f = (M_i + M_b(r_f) + P)/((1+F) M_i + P). BLUM0: RULE at P = 0. Posited, not derived. kappa = 1/2 FITTED, unused; not theory closed."""
import numpy as np
from scipy.optimize import brentq
BS = lambda x: 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
def infer_r0(r, M0, B=BS):
    """r0 from M0's own shape, ratio of two points below any truncation. Returns r0, C with M0 = C B(r/r0), and the last untruncated index."""
    inc = np.where(np.diff(M0) > 0)[0]; n = int(inc[-1]);  # r[n] is the last point certainly below a truncation
    i1 = int(np.searchsorted(M0[:n + 1], 1e-3 * M0[n])); i1 = min(i1, n - 1); lq = np.log(M0[i1] / M0[n])
    f = lambda l: float(np.log(B(r[i1] / np.exp(l)) / B(r[n] / np.exp(l))) - lq)
    l0 = brentq(f, np.log(r[n]) - 12, np.log(r[n]) + 6, xtol=1e-12); r0 = float(np.exp(l0)); return r0, float(M0[n] / B(r[n] / r0)), n
def rule(r, Mb, M0, F, variant="RULE", r0=None, C=None, B=BS, iters=200):
    """Returns M_f on r, last relative change, crossings of r_f(r_i), the ordered r_f. Same damped iteration and read-back as X39's contract."""
    lr = np.log(r)
    if r0 is None: r0, C, _ = infer_r0(r, M0, B)
    Mr0 = float(C * B(np.asarray(1.0)))
    P = 0.0 * r if variant == "BLUM0" else Mr0 * r / r0
    Mb_at = lambda x: np.interp(np.log(np.maximum(x, r[0])), lr, Mb, left=Mb[0], right=Mb[-1])
    rf = r.copy(); new = rf
    for _ in range(iters):
        if variant == "RULE_F": new = r * ((1 + F) * M0 + P) / np.maximum(M0 + Mb_at(rf) + P, 1e-300)
        else: new = r / (1 + Mb_at(rf) / np.maximum(M0 + P, 1e-300))
        rf = 0.5 * rf + 0.5 * new
    conv = float(np.max(np.abs(new / rf - 1))); order = np.maximum.accumulate(rf); cross = int(np.sum(rf < order - 1e-12 * order))
    return np.interp(lr, np.log(order), M0, left=0.0, right=M0[-1]), conv, cross, order
