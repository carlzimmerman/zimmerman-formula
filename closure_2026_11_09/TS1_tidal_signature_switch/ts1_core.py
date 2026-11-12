#!/usr/bin/env python3
"""TS1 (FROZEN_CRITERIA.md 4b352f2a37) core: the tidal signature I, the switch s = max(0, I/2), the closed forms (KA-T1..T5,
numeric checks from finite differences of potentials), the Gaussian-Hessian ensemble (KA-T7, T6 <s>_w, T2 voids), and the
two-mass direction-averaged switch for T3.
    python3 ts1_core.py   -> parts/core.json, ts1_core.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(HERE, "parts"), exist_ok=True)
CRIT = "4b352f2a37"
def I_of_eig(l):
    l = np.asarray(l, float); den = (np.sum(l * l, axis=-1) / 6.0) ** 1.5; return np.where(den > 0, -np.prod(l, axis=-1) / np.where(den > 0, den, 1), 0.0)
def I_of_H(H): return I_of_eig(np.linalg.eigvalsh(H))
def s_of_I(I): return np.maximum(0.0, np.asarray(I, float) / 2.0)
def I_sph(x):
    t = 3 * np.asarray(x, float) - 2; return -t / ((t * t + 2) / 6) ** 1.5
def s_sph(x): return s_of_I(I_sph(x))
def hess_fd(phi, x0, h=1e-4):
    x0 = np.asarray(x0, float); H = np.zeros((3, 3)); E = np.eye(3) * h
    for i in range(3):
        for j in range(3): H[i, j] = (phi(x0 + E[i] + E[j]) - phi(x0 + E[i] - E[j]) - phi(x0 - E[i] + E[j]) + phi(x0 - E[i] - E[j])) / (4 * h * h)
    return H
def H_point(M, d):                                                     # Hessian of Phi = -M/|d| (G = 1)
    d = np.asarray(d, float); r = np.linalg.norm(d); n = d / r; return M / r ** 3 * (np.eye(3) - 3 * np.outer(n, n))
def sbar_two_mass(r, D, x_lens=0.0, nmu=64):
    """direction-averaged s at distance r from a lens (spherical, local x) with an equal point mass at distance D (G M = 1 units:
    lens u = M_lens(<r)/r^3 with M_lens = 1). Average over cos(theta) uniform (axisymmetric)."""
    mu, w = np.polynomial.legendre.leggauss(nmu); out = 0.0
    for m_, w_ in zip(mu, w):
        n = np.array([math.sqrt(max(0.0, 1 - m_ * m_)), 0.0, m_]); u = 1.0 / r ** 3
        Hl = u * (np.eye(3) + (3 * x_lens - 3) * np.outer(n, n))       # eigen ((3x-2)u along n, u, u)
        Hn = H_point(1.0, r * n - np.array([0.0, 0.0, D]))
        out += w_ * float(s_of_I(I_of_H(Hl + Hn)))
    return out / 2.0
if __name__ == "__main__":
    L = []; P = lambda s: (print(s), L.append(s)); R = dict(criteria=CRIT)
    pm = lambda x: -1.0 / np.linalg.norm(x); x0 = np.array([0.7, -0.4, 1.1])
    ka1 = float(I_of_H(hess_fd(pm, x0)))
    sheet = lambda x: 0.5 * 3.0 * x[0] ** 2                              # 1D plane wave / sheet interior (only xx curvature)
    ka2 = float(I_of_H(hess_fd(sheet, x0)))
    line = lambda x: math.log(math.hypot(x[0], x[1]))                    # line mass along z (2 G lambda ln R)
    ka3 = float(I_of_H(hess_fd(line, x0)))
    iso = lambda x: 0.5 * 0.8 * float(np.dot(x, x))                       # isotropic overdensity
    ka4 = float(I_of_H(hess_fd(iso, x0))); void = float(I_of_H(hess_fd(lambda x: -iso(x), x0)))
    sis = lambda x: math.log(np.linalg.norm(x))                          # isothermal sphere Phi = sigma^2 ln r: x = 1/3
    ka5 = float(I_of_H(hess_fd(sis, x0)))
    R["KA_T"] = dict(T1_point_mass=ka1, T2_sheet=ka2, T3_line=ka3, T4_isotropic_over=ka4, T4_void=void, T4_orchestrator_stated=-2 / math.sqrt(3), T5_SIS=ka5,
                     closed_forms=dict(point=2.0, sheet=0.0, line=0.0, iso=-2 * math.sqrt(2), void=2 * math.sqrt(2), sis=2 * math.sqrt(2), Isph_x0=float(I_sph(0.0)), Isph_third=float(I_sph(1 / 3)), Isph_1=float(I_sph(1.0)), x_off=2 / 3))
    ok = abs(ka1 - 2) < 1e-4 and abs(ka2) < 1e-6 and abs(ka3) < 1e-4 and abs(ka4 + 2 * math.sqrt(2)) < 1e-4 and abs(ka5 - 2 * math.sqrt(2)) < 1e-4 and abs(void - 2 * math.sqrt(2)) < 1e-4
    R["KA_T"]["pass_"] = bool(ok)
    P(f"KA-T: point {ka1:.6f} (2), sheet {ka2:.2e} (0), line {ka3:.2e} (0), isotropic overdensity {ka4:.6f} (-2 sqrt2 = {-2*math.sqrt(2):.6f}; orchestrator's -2/sqrt3 = {-2/math.sqrt(3):.4f} does NOT match), void {void:.6f}, SIS {ka5:.6f} (2 sqrt2) -> {'PASS' if ok else 'FAIL'}")
    # Gaussian isotropic Hessian ensemble
    rng = np.random.default_rng(20261109); N = 2_000_000; G_ = rng.standard_normal((N, 3, 3)); S = (G_ + np.transpose(G_, (0, 2, 1))) / math.sqrt(2); xi = rng.standard_normal(N)
    H = S + xi[:, None, None] * np.eye(3)[None]; c11 = float(np.mean(H[:, 0, 0] ** 2)); c12 = float(np.mean(H[:, 0, 1] ** 2)); c1122 = float(np.mean(H[:, 0, 0] * H[:, 1, 1]))
    ka7 = abs(c11 / c12 / 3 - 1) < 0.02 and abs(c1122 / c12 - 1) < 0.02
    ev = np.linalg.eigvalsh(H); I = I_of_eig(ev); s = s_of_I(I); tr = ev.sum(1); w = tr * tr
    sw = float(np.sum(s * w) / np.sum(w)); sv = float(s.mean()); fon = float(np.mean(s > 0)); spos = float(s[tr > 0].mean()); sneg = float(s[tr < 0].mean())
    swpos = float(np.sum((s * w)[tr > 0]) / np.sum(w[tr > 0])); swneg = float(np.sum((s * w)[tr < 0]) / np.sum(w[tr < 0]))
    R["KA_T7"] = dict(c11_over_c12=c11 / c12, c1122_over_c12=c1122 / c12, pass_=bool(ka7))
    R["T6_ensemble"] = dict(N=N, s_w_delta2=sw, s_volume=sv, frac_on=fon, s_overdense=spos, s_underdense=sneg, s_w_overdense=swpos, s_w_underdense=swneg, s_max=float(s.max()))
    R["T2_voids"] = dict(s_void_centre=math.sqrt(2), s_mean_underdense=sneg, s_w_underdense=swneg)
    P(f"KA-T7 ensemble <H11^2>/<H12^2> {c11/c12:.4f} (3), <H11H22>/<H12^2> {c1122/c12:.4f} (1) -> {'PASS' if ka7 else 'FAIL'}")
    P(f"T6 linear web: <s>_w (delta^2-weighted) {sw:.4f}; volume <s> {sv:.4f}; fraction on {fon:.3f}; <s> overdense {spos:.4f} / underdense {sneg:.4f}; weighted over / under {swpos:.4f} / {swneg:.4f}; max s {s.max():.4f}")
    P(f"T2 voids: s at an isotropic void centre sqrt2 = {math.sqrt(2):.4f}; mean over the underdense half {sneg:.4f}")
    # T3 table: direction-averaged s vs r / D for x_lens = 0
    tab = {f"{q:.3f}": sbar_two_mass(q, 1.0) for q in (0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.45, 0.5, 0.6, 0.8)}
    R["T3_sbar_vs_r_over_D"] = tab; P("T3 direction-averaged s vs r/D (x_lens 0): " + " ".join(f"{k}:{v:.3f}" for k, v in tab.items()))
    json.dump(R, open(os.path.join(HERE, "parts", "core.json"), "w"), indent=1); open(os.path.join(HERE, "ts1_core.out"), "w").write("\n".join(L) + "\n")
