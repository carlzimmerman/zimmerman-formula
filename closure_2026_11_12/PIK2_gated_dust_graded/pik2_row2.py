#!/usr/bin/env python3
"""PIK2 row 2 (criteria 95edd35e0b): linear visibility, health H2 and growth-factor criterion G2 about FRW, per gate, threshold
xi, mu_K and footing, in the sub-horizon Newtonian reduction certified in pik2_row0.py:
    ddot delta + 2 H dot delta = K rho_m delta - K rho_d k^2 delta / M,  M = mu^2 + beta k^2,  beta = (1+e1)^2 / K_P,
    K_P = 1 - k^2 [ s2 (rho_d/rho_c)^2 / (2 mu^2 Qbar) - theta Lstar^2 / 2 ],  e1 = s1 rho_d / (Qbar^2 rho_c),
k physical [Mpc^-1], c = 1, theta = 1 (Pi > 0 branch, gamma_L acts) or 0 (Pi < 0 branch).
  H2: K_P > 0 and M > 0 at every physical k in [1e-4, 1e6] Mpc^-1 and z in [0, 3400], both branches.
  G2: |D_gate / D_ungated - 1| <= 0.01 at comoving k = 0.01, 0.05, 0.2 h/Mpc, z 3400 -> 0 (ungated = S = 1 with P, same branch).
  python3 pik2_row2.py [--mutate]   (M-S2: sign of the s2 term flipped)
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pik2_common as CM

MUT = "--mutate" in sys.argv
TAG = "pik2_row2_MUTATE" if MUT else "pik2_row2"
OUT = []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
S2SIGN = -1.0 if MUT else 1.0
OMB_H2 = 0.02237                     # baryon density used for the growth background only (disclosed; ratio criterion)
ZGRID = np.expm1(np.linspace(0.0, math.log(3401.0), 140))
KGRID = np.geomspace(1e-4, 1e6, 241)
KCOM = (0.01, 0.05, 0.2)


def bg(f, mu):
    I0 = CM.KD1[f]["I0"]; H0 = 100 * CM.H_LIT / CM.C_KMS; Om_d = I0 / (3 * H0 ** 2); Om_b = OMB_H2 / CM.H_LIT ** 2
    Om_r = CM.KD1[f]["Omega_r"]; Om_L = 1 - Om_d - Om_b - Om_r; w0 = I0 / (4 * mu * mu)
    return dict(H0=H0, Om_d=Om_d, Om_b=Om_b, Om_r=Om_r, Om_L=Om_L, w0=w0, I0=I0)


def coeffs(gate, xi, mu, f, a, theta):
    s1, s2 = CM.GATES[gate][1]; s2 = S2SIGN * s2
    B = bg(f, mu); r = a ** -3 * (1 + B["w0"] / a ** 3) / xi            # rho_d(a)/rho_c
    qb = B["I0"] / (2 * mu * mu * a ** 3); Qb = 1 + qb
    e1 = s1 * r / Qb ** 2
    c2 = s2 * r * r / (2 * mu * mu * Qb) - theta * (CM.LSTAR_PC[f] * 1e-6) ** 2 / 2
    return e1, c2


def health(gate, xi, mu, f):
    worst = None; fails = []
    for theta in (1, 0):
        for z in ZGRID:
            a = 1 / (1 + z); e1, c2 = coeffs(gate, xi, mu, f, a, theta)
            KP = 1 - KGRID ** 2 * c2
            with np.errstate(divide="ignore", invalid="ignore"):
                M = mu * mu + (1 + e1) ** 2 / KP * KGRID ** 2
            bad = (KP <= 0) | (M <= 0)
            if bad.any():
                fails.append((theta, float(z), float(KGRID[bad][0]), float(KGRID[bad][-1])))
    if not fails:
        return dict(ok=True)
    zs = [x[1] for x in fails]
    return dict(ok=False, n=len(fails), z_range=[min(zs), max(zs)],
                branches=sorted(set(x[0] for x in fails)), k_first_at_zmax=[x[2] for x in fails if x[1] == max(zs)][0],
                k_lowest=min(x[2] for x in fails))


def growth(gate, xi, mu, f, kcom, theta, ungated=False):
    B = bg(f, mu); h = CM.H_LIT
    def H(a): return B["H0"] * math.sqrt(B["Om_r"] * a ** -4 + (B["Om_d"] * (1 + B["w0"] / a ** 3) + B["Om_b"]) * a ** -3 + B["Om_L"])
    def rhs(la, y):
        a = math.exp(la); Ha = H(a); eps = 1e-5
        dlnH = (math.log(H(a * math.exp(eps))) - math.log(H(a * math.exp(-eps)))) / (2 * eps)
        Kd = 1.5 * B["H0"] ** 2 * B["Om_d"] * (1 + B["w0"] / a ** 3) * a ** -3; Km = Kd + 1.5 * B["H0"] ** 2 * B["Om_b"] * a ** -3
        k = kcom * h / a
        if ungated:
            e1, c2 = 0.0, -theta * (CM.LSTAR_PC[f] * 1e-6) ** 2 / 2
        else:
            e1, c2 = coeffs(gate, xi, mu, f, a, theta)
        KP = 1 - k * k * c2; M = mu * mu + (1 + e1) ** 2 / KP * k * k
        press = Kd * k * k / M
        return [y[1], -(2 + dlnH) * y[1] + (Km - press) / Ha ** 2 * y[0]]
    a0 = 1 / 3401.0
    if not ungated:   # singular coefficient: M(k) or K_P(k) changes sign along the history at this k -> no growth number (reported)
        for aa in np.geomspace(a0, 1.0, 400):
            e1, c2 = coeffs(gate, xi, mu, f, aa, theta); k = kcom * h / aa; KP = 1 - k * k * c2
            if KP <= 0 or mu * mu + (1 + e1) ** 2 / KP * k * k <= 0: return float("nan")
    sol = solve_ivp(rhs, (math.log(a0), 0.0), [a0, a0], method="LSODA", rtol=1e-8, atol=1e-14)
    if not sol.success or not np.isfinite(sol.y[0, -1]): return float("nan")
    return float(sol.y[0, -1])


RES = dict(lane="PIK2", file=TAG, criteria="95edd35e0b", rows={}, note=CM.NOTE)
P(f"PIK2 row 2{' [MUTATE M-S2: s2 sign flipped]' if MUT else ''}: H2 on z 0-3400 x k 1e-4..1e6 /Mpc (physical), both Pi branches; G2 growth ratio at k = {KCOM} h/Mpc")
REF = {}
for f in CM.FOOT:
    for mlab, mu in CM.MU_LIST(f).items():
        for kc in KCOM:
            for th in (1, 0):
                REF[(f, mlab, kc, th)] = growth(None, None, mu, f, kc, th, ungated=True)
for f in CM.FOOT:
    RES["rows"][f] = {}
    for mlab, mu in CM.MU_LIST(f).items():
        RES["rows"][f][mlab] = {}
        P(f"\n[{f}] mu = {mu:.5g} ({mlab})")
        for g in CM.GRADED:
            s1, s2 = CM.GATES[g][1]
            vis = "VISIBLE" if (s1 != 0 or s2 != 0) else "INVISIBLE at linear order"
            rows = []
            for i, lx in enumerate(CM.LOGXI):
                xi = 10.0 ** lx; hh = health(g, xi, mu, f)
                do_g = hh["ok"] or (i % 40 == 0)
                gr = {}
                if do_g:
                    if s1 == 0 and s2 == 0:
                        gr = {f"{kc}_{th}": 1.0 for kc in KCOM for th in (1, 0)}
                    else:
                        for kc in KCOM:
                            for th in (1, 0):
                                d = growth(g, xi, mu, f, kc, th); gr[f"{kc}_{th}"] = d / REF[(f, mlab, kc, th)]
                g2 = (all(np.isfinite(v) and abs(v - 1) <= 0.01 for v in gr.values()) if gr else None)
                rows.append(dict(logxi=float(lx), H2=hh, G2_ratios=gr, G2=g2, row2_pass=bool(hh["ok"] and g2)))
            npass = sum(r["row2_pass"] for r in rows); nh = sum(r["H2"]["ok"] for r in rows)
            passxi = [r["logxi"] for r in rows if r["row2_pass"]]
            RES["rows"][f][mlab][g] = dict(visibility=vis, s1=s1, s2=S2SIGN * s2, n_H2_pass=nh, n_row2_pass=npass,
                                           logxi_pass=passxi, table=rows)
            ex = next((r for r in rows if not r["H2"]["ok"]), None)
            exg = [r for r in rows if r["G2_ratios"]]
            gsum = (f"growth ratios at log xi {exg[len(exg) // 2]['logxi']}: " + ", ".join(f"{k}:{v:.4f}" for k, v in exg[len(exg) // 2]["G2_ratios"].items())) if exg else ""
            P(f"  {g:3s} {vis:25s} H2 passes {nh}/{len(rows)} xi; row 2 passes {npass}/{len(rows)}"
              + (f" (log xi {min(passxi):.2f}..{max(passxi):.2f})" if passxi else "")
              + (f"; first H2 fail at log xi {ex['logxi']}: z {ex['H2']['z_range'][0]:.3g}-{ex['H2']['z_range'][1]:.4g}, branches {ex['H2']['branches']}, lowest bad k {ex['H2']['k_lowest']:.3g}/Mpc" if ex else "")
              + ("; " + gsum if gsum else ""))
P(f"\nruntime {time.time() - T0:.0f} s"); P(CM.NOTE)
json.dump(CM.clean(RES), open(os.path.join(CM.HERE, TAG + ".json"), "w"), indent=0)
open(os.path.join(CM.HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
