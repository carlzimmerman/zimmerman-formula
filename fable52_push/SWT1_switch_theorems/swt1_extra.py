#!/usr/bin/env python3
"""SWT1 extras: REPORTED ONLY, written after the graded run (swt1.py) and disclosed as such in RESULT.md. No label rests on them.

E1  a non-trivial check of the polarizability solver: a coated sphere against its closed form.
E2  T3 concentration bracket: the same cosmic share confined to R_h / 2, R_h / 4, R_h / 8.
E3  what a pressure-balance bubble predicts at the 59 KiDS points (Brouwer+2021 Fig. 9 files on disk): the law inside the wall,
    the compensated field outside it (baryons + the swept-up component), projected as 4 G DeltaSigma, against the data and errors.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, json, math, importlib.util
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

# reuse swt1's functions without re-running its main body: exec the part above the first known answer
src = open(os.path.join(HERE, "swt1.py")).read()
cut = src.index("RES = dict(lane=")
NS = {"__file__": os.path.join(HERE, "swt1.py"), "__name__": "swt1_lib"}
argv0 = sys.argv; sys.argv = ["swt1.py"]; exec(compile(src[:cut], "swt1.py", "exec"), NS); sys.argv = argv0
G, MS, MPC, KPC, A0 = NS["G"], NS["MS"], NS["MPC"], NS["KPC"], NS["A0"]
alpha_generic, p_wall, Rms, R_DUST, RHO_D0, Mph, dMph, u_in = (NS[k] for k in
    ("alpha_generic", "p_wall", "Rms", "R_DUST", "RHO_D0", "Mph", "dMph", "u_in"))
RES = dict(lane="SWT1", part="extras, reported only", note="kappa = 1/2 FITTED; not theory closed; adopts nothing")

# ------------------------------------------------------------------ E1 coated sphere
def coated_exact(m1, m2, x3):
    """core mu m1 inside a = x R, shell mu m2 to R, host 1. x3 = (a / R)^3."""
    num = (m2 - 1) * (m1 + 2 * m2) + x3 * (m1 - m2) * (1 + 2 * m2)
    den = (m2 + 2) * (m1 + 2 * m2) + 2 * x3 * (m2 - 1) * (m1 - m2)
    return num / den
rows = []
for m1, m2, x in ((1.0, 0.05, 0.5), (3.0, 0.2, 0.3), (0.1, 2.0, 0.7)):
    # uniform core: f proportional to r, L = 1. At the interface f and mu f' are continuous, so L jumps to (m1 / m2).
    # The solver then carries the Riccati equation through the shell: a real test of its evolution and of the matching.
    al, _ = alpha_generic(lambda s: m2, lambda s: m2, lambda s: 0.0, math.log(x), 0.0, L0=m1 / m2)
    ex = coated_exact(m1, m2, x ** 3); rows.append(dict(mu_core=m1, mu_shell=m2, a_over_R=x, alpha=al, exact=ex, err=abs(al - ex)))
    P(f"E1 coated sphere core {m1} shell {m2} a/R {x}: alpha {al:.6f}, closed form {ex:.6f}, err {abs(al-ex):.1e}")
RES["E1_coated_sphere"] = dict(rows=rows, max_err=max(r["err"] for r in rows))

# ------------------------------------------------------------------ E2 concentration bracket
P("")
BINS = (9.4, 10.45, 10.7, 10.9)
E2 = {}
for f, a0 in A0.items():
    E2[f] = {}
    for lm in BINS:
        Mb = 10 ** lm * MS; Rh0 = Rms("NC", Mb, 0.0, 1.0); row = {}
        for div in (1, 2, 4, 8):
            Rh = Rh0 / div
            r = np.logspace(math.log10(1e-2 * KPC), math.log10(Rh), 6001)
            Md = R_DUST * Mb * r / Rh
            pd = G * R_DUST * Mb ** 2 * (1 + R_DUST * r / Rh) / (8 * math.pi * Rh * r ** 3)
            ratio = p_wall(G * Mb / r ** 2 / a0, a0) / pd
            rmax = min(200 * KPC, Rh); ins = r <= rmax
            dM = np.diff(np.concatenate([[0.0], Md]))
            row[f"Rh/{div}"] = dict(R_Mpc=Rh / MPC, ratio_at_edge=float(ratio[-1]), min_ratio_beyond_1kpc=float(ratio[r > KPC].min()),
                                    M_unc_over_Mb=float(np.sum(dM[ins & (ratio < 1)]) / Mb), carrier_inside=float(np.sum(dM[ins]) / Mb))
        E2[f][str(lm)] = row
        P(f"E2 [{f}] log M_b {lm}: share inside R_h, R_h/2, R_h/4, R_h/8 -> uncleared inside 200 kpc "
          + " / ".join(f"{row[k]['M_unc_over_Mb']:.2f} of {row[k]['carrier_inside']:.2f}" for k in row)
          + " M_b; ratio at the edge " + " / ".join(f"{row[k]['ratio_at_edge']:.2f}" for k in row))
RES["E2_concentration"] = E2

# ------------------------------------------------------------------ E3 KiDS points for pressure-balance bubbles
P("")
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar"); Gpc = 4.52e-30; PCm = NS["PC"]
mids = [9.4, 10.45, 10.7, 10.9]; LE = []
for i, lm in enumerate(mids, 1):
    a = np.loadtxt(os.path.join(DATA, f"Fig-9_RAR-KiDS-isolated_Massbin-{i}.txt"), comments="#")
    gbar = a[:, 0]; gobs = 4 * Gpc * a[:, 1] / a[:, 4] * PCm; err = 4 * Gpc * a[:, 3] / a[:, 4] * PCm
    for gb, go, e in zip(gbar, gobs, err):
        if go > 0: LE.append(dict(lm=lm, gbar=gb, gobs=go, err=e, Mb=10 ** lm * MS))
P(f"E3 KiDS points loaded: {len(LE)} (the record's 59)")

def proj_g(R, Mb, a0, Rb, Msw, n=6000):
    """4 G DeltaSigma at projected R for: point M_b; the law's phantom inside R_b; a shell in [R_b, 1.1 R_b] carrying the swept-up
    component minus the phantom's surface layer (compensation). Numerical projection on r = R cosh t."""
    Mnet = Msw - Mph(Rb, Mb, a0); Vsh = 4 * math.pi / 3 * ((1.1 * Rb) ** 3 - Rb ** 3); rho_sh = Mnet / Vsh
    def rho(r):
        out = np.zeros_like(r)
        ins = r < Rb; out[ins] = dMph(r[ins], Mb, a0) / (4 * math.pi * r[ins] ** 2)
        sh = (r >= Rb) & (r <= 1.1 * Rb); out[sh] = rho_sh
        return out
    def Menc(r):
        if r < Rb: return Mph(r, Mb, a0)
        if r <= 1.1 * Rb: return Mph(Rb, Mb, a0) + rho_sh * 4 * math.pi / 3 * (r ** 3 - Rb ** 3)
        return Msw
    rmaxx = 1.1 * Rb
    if R >= rmaxx:
        Sig = 0.0; Mcyl = Msw
    else:
        tm = math.acosh(rmaxx / R); t = np.linspace(0.0, tm, n); r = R * np.cosh(t)
        Sig = 2 * np.trapz(rho(r) * r, t)                                   # 2 int rho r dr / sqrt(r^2 - R^2), dr = R sinh t dt
        # mass inside the cylinder of radius R: sphere of radius R plus the caps beyond it
        Mcyl = Menc(R) + np.trapz(4 * math.pi * r ** 2 * rho(r) * (1 - np.tanh(t)) * R * np.sinh(t), t)
    return 4 * G * ((Mb + Mcyl) / (math.pi * R * R) - Sig)

E3 = {}
for f, a0 in A0.items():
    E3[f] = {}
    for sig in (17.5, 35.0, 52.5):
        for dlt, tag in ((0.0, "mean"), (4.55, "5.55x")):
            pamb = RHO_D0 * (sig * 1e3) ** 2
            rows = []; chi_law = chi_mod = 0.0; nout = 0; nbad = 0; worst = 0.0
            for d in LE:
                Mb = d["Mb"]
                Rb = math.exp(brentq(lambda lr: math.log(float(p_wall(G * Mb / math.exp(2 * lr) / a0, a0)) / pamb), math.log(1e-3 * KPC), math.log(1e4 * MPC)))
                Msw = 4 * math.pi / 3 * Rb ** 3 * RHO_D0 * (1 + dlt)
                R = math.sqrt(G * Mb / d["gbar"])
                glw = a0 * float(u_in(d["gbar"] / a0)); gm = proj_g(R, Mb, a0, Rb, Msw)
                sh = math.log10(gm / glw) if gm > 0 else float("-inf")
                chi_law += ((glw - d["gobs"]) / d["err"]) ** 2; chi_mod += ((gm - d["gobs"]) / d["err"]) ** 2
                out = R > Rb; nout += out
                if not (abs(sh) <= 0.05): nbad += 1
                if math.isfinite(sh): worst = min(worst, sh)
                rows.append(dict(lm=d["lm"], R_Mpc=R / MPC, Rb_Mpc=Rb / MPC, outside=bool(out), shift_dex=(sh if math.isfinite(sh) else None),
                                 z_model=(gm - d["gobs"]) / d["err"], z_law=(glw - d["gobs"]) / d["err"]))
            E3[f][f"sig{sig}_{tag}"] = dict(points=len(LE), outside_wall=int(nout), over_0p05=int(nbad), worst_shift_dex=worst,
                                           chi2_law=chi_law, chi2_model=chi_mod, rows=rows)
            P(f"E3 [{f}] dispersion {sig} km/s, swept component at {tag} density: {nout} of {len(LE)} points outside the wall; "
              f"{nbad} beyond 0.05 dex of the law (worst {worst:+.2f} dex or negative signal); chi2 vs data: law {chi_law:.1f}, bubble {chi_mod:.1f}")
RES["E3_kids_points"] = E3
P("")
P("(E3's chi2 uses the Fig. 9 per-point errors only, no covariance and no hot-gas term; it is a pointer, not a grade.)")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, "swt1_extra.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "swt1_extra.out"), "w").write("\n".join(OUT) + "\n")
