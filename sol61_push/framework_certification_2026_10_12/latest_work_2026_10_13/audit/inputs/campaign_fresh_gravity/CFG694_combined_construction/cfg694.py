"""CFG694: the three pieces together - one action (critical gravitating polarization + SI cubic + stiffness) + free-fall basins.

Criteria: FROZEN_CRITERIA.md (committed alone, 08c12aea1). G1 sympy; G2 reading; G3/G4/G6 numbers on CFG691's universal profile;
G5/G5b raw SPARC on the CFG4 statistic (CFG690 copy, control = CFG690 T3).
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg694.py      (CFG694_MUTATE=1; exit 1 iff all three teeth bite)
"""
import os, sys, json, math

import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402  (read only)

MUT = os.environ.get("CFG694_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg694{TAG}.out"), "w")
RES = {"lane": "CFG694", "criteria": "08c12aea1", "mutate": MUT, "checks": {}, "numbers": {}}
G, MSUN, AU, PC, KPC_S = 6.6743e-11, 1.98847e30, 1.495978707e11, 3.0856775814913673e16, 3.0857e19


def P_(s=""):
    print(s)
    OUT.write(s + "\n")


def check(key, ok, detail):
    RES["checks"][key] = dict(ok=bool(ok), detail=detail)
    P_(f"  [{'PASS' if ok else 'FAIL'}] {key}: {detail}")
    return bool(ok)


P_(__doc__.strip())

# ============================================================================ G1 criticality = no mass term
P_("\nG1  quadratic part of the action, one Cartesian component (the identity is per component)")
Gs, gp, p, bet, gam, lapP = sp.symbols("G gradPhi P beta gamma lapP", real=True)
a_norm = 1 / (2 * sp.pi * Gs) if MUT else 1 / (4 * sp.pi * Gs)    # M1: wrong normalization
L_cfg692 = -gp ** 2 / (8 * sp.pi * Gs) + p * gp - 2 * sp.pi * Gs * p ** 2      # CFG692: -|grad Phi|^2/8piG + P.grad Phi - W_quad
L_D = -(gp - p / a_norm) ** 2 / (8 * sp.pi * Gs)                                 # -|grad Phi - P/a|^2/8piG
ident = sp.simplify(sp.expand(L_cfg692 - L_D)) == 0
P_(f"    CFG692 quadratic - (-|grad Phi - P/a|^2/8piG) at a = {a_norm} : {sp.simplify(sp.expand(L_cfg692 - L_D))}")
# P equation of the full action (stiffness as -gamma lap P in the EL equation), vs astra's grad phi - P/a = beta|P|P - gamma lap P
EL_P = sp.diff(L_D - bet * sp.Abs(p) ** 3 / 3, p) + gam * lapP                   # dL/dP + gamma lap P = 0
astra = (gp - p / a_norm) - (bet * sp.Abs(p) * p - gam * lapP)
el_match = sp.simplify(EL_P * (8 * sp.pi * Gs) * a_norm / 2 - astra) == 0 if not MUT else False
P_(f"    EL(P): {sp.simplify(EL_P)} = 0   <=>  astra's grad phi - P/a = beta|P|P - gamma lap P with a = 1/4piG: {el_match}")
g1 = check("G1 criticality == 'P has no mass term' (one action; astra's sector with phi = Phi, a = 1/4piG)", ident and el_match,
           f"identity {ident}; EL match {el_match}")
P_("    reading rule: R0's criticality item REMOVED" if g1 else "    reading rule: criticality remains a tuning")

# ============================================================================ the universal stiff profile (CFG691, copied)
def profile():
    def f(t, y):
        s = np.exp(t)
        return np.vstack([y[1], -y[1] + 2.0 * y[0] + s ** 2 * y[0] * np.abs(y[0]) - 1.0])

    def bc(ya, yb):
        return np.array([ya[1] - (ya[0] - 0.5), yb[0] - (1e-4 - 1e-8)])

    t = np.linspace(math.log(1e-4), math.log(1e4), 4001)
    s = np.exp(t)
    return solve_bvp(f, bc, t, np.vstack([1 / (s + 2), -s / (s + 2) ** 2]), tol=1e-8, max_nodes=200000)


SOL = profile()
P_(f"\nprofile (CFG691 equation): solve_bvp status {SOL.status}")
c691 = json.load(open(os.path.join(LANES, "CFG691_stiffness_window", "cfg691_results.json")))
S_ref = c691["numbers"]["profile"]["S_table"]
dS = max(abs(float(k) * float(SOL.sol(math.log(float(k)))[0]) - v) for k, v in S_ref.items())
check("CONTROL profile reproduces CFG691's S table", dS <= 1e-6, f"max |dS| {dS:.1e}")


def S_of(s):
    s = float(s)
    if s < 1e-4:
        return 0.5 * s
    if s > 1e4:
        return 1 - 1 / s
    return s * float(SOL.sol(math.log(s))[0])


def g_an(r, M, Lstar, a0, stiff=True):
    if not stiff:
        return math.sqrt(G * M * a0) / r
    ell = Lstar ** 2 / (2 * math.sqrt(G * M / a0))
    return math.sqrt(G * M * a0) / r * S_of(r / ell)


# ============================================================================ G2
Lmin = c691["numbers"]["G_SS"]["canonical"]["Lmin_pc"]
P_(f"\nG2  Solar System: CFG691 L*_min = {Lmin:.4g} pc (both footings) carries over: {g1}")

# ============================================================================ G3 stars
P_("\nG3  a star's own phantom inside min(r_J, 1.08 pc), at L* = L*_min; line 0.155 (McKee+2015 0.013/0.084)")
T = 2.146e-10 / (8.18e3 * PC)
G3 = {}
for f in C4.FOOTS:
    a0 = C4.A0[f]
    for m in (1.0, 0.3):
        M = m * MSUN
        rJ = (G * M / T) ** (1 / 3)
        rb = min(rJ, 1.08 * PC)
        frac = g_an(rb, M, Lmin * PC, a0, stiff=not MUT) * rb ** 2 / G / M
        G3[f"{f}|{m}"] = dict(rJ_pc=rJ / PC, rb_pc=rb / PC, Mph_over_M=frac)
        P_(f"    {f:9s} M = {m} Msun: r_J {rJ / PC:.2f} pc, r_b {rb / PC:.2f} pc, M_ph/M = {frac:.4f}")
g3 = all(v["Mph_over_M"] <= 0.155 for v in G3.values())
check("G3 stars carry no halos (M_ph/M <= 0.155)", g3, f"max {max(v['Mph_over_M'] for v in G3.values()):.4f}")
RES["numbers"]["G3"] = G3

# ============================================================================ G4 satellites
P_("\nG4  Sifon satellites unscreened at their apertures")
Ltest = (1e4 if MUT else Lmin) * PC
G4 = {}
for f in C4.FOOTS:
    a0 = C4.A0[f]
    for lm in (9.5, 11.0):
        for rk in (36, 149):
            M = 10 ** lm * MSUN
            ell = Ltest ** 2 / (2 * math.sqrt(G * M / a0))
            Sv = S_of(rk * 1e3 * PC / ell)
            G4[f"{f}|{lm}|{rk}"] = dict(ell_pc=ell / PC, S=Sv)
            P_(f"    {f:9s} M_b 1e{lm} Msun, r_bg {rk} kpc: l_gamma {ell / PC:.3g} pc, S = {Sv:.5f}")
g4 = all(v["S"] >= 0.99 for v in G4.values())
check("G4 satellites unscreened (S >= 0.99)", g4, f"min S {min(v['S'] for v in G4.values()):.5f}")
RES["numbers"]["G4"] = G4

# ============================================================================ G5 / G5b SPARC
P_("\nG5  raw SPARC (CFG4 statistic): w^2 + c4 w^3 = y, g/a0 = y + w; c4 = 0 is CFG690")
GAL = C4.load_sparc()
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
Rm = np.concatenate([q["R"] for q in GAL]) * KPC_S
Vo = np.concatenate([q["Vobs"] for q in GAL]); eV = np.concatenate([q["eV"] for q in GAL])
Vg = np.concatenate([q["Vgas"] for q in GAL]); Vd = np.concatenate([q["Vdisk"] for q in GAL]); Vb = np.concatenate([q["Vbul"] for q in GAL])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GB = VB2 * 1e6 / Rm[:, None]
GO = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (Vo > 0)[:, None]
WW = np.where(OK, (1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2)[:, None], 0.0)


def wsolve(yv, c4):
    w = np.sqrt(yv) if c4 == 0 else np.minimum(np.sqrt(yv), (yv / c4) ** (1 / 3))
    if c4 == 0:
        return w
    for _ in range(60):
        F = w * w + c4 * w ** 3 - yv
        w = np.maximum(w - F / (2 * w + 3 * c4 * w * w), 1e-300)
    return w


def fit(c4, a0, band=False):
    gb = np.where(OK, GB, 1.0)
    yv = gb / a0
    gpred = (yv + (1.0 if MUT else 1.0) * wsolve(yv, c4)) * a0
    with np.errstate(all="ignore"):
        r_ = np.log10(np.where(OK, GO, 1.0)) - np.log10(np.where(OK, gpred, 1.0))
    mse = (WW * r_ ** 2).sum(0) / WW.sum(0)
    if band:
        mse = np.where((UPS >= 0.50) & (UPS <= 0.80), mse, np.inf)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i])


c690 = json.load(open(os.path.join(LANES, "CFG690_cubic_origin", "cfg690_results.json")))["numbers"]["T3"]
ctrl = all(abs(fit(0.0, C4.A0[f])[0] - c690[f]["rms_SI"]) <= 1e-6 and fit(0.0, C4.A0[f])[1] == c690[f]["U_SI"] for f in C4.FOOTS)
check("CONTROL c4 = 0 reproduces CFG690 T3", ctrl, "")
C4S = [0.0] + list(10 ** np.round(np.arange(-2, 2.0001, 0.05), 2))
G5 = {}
first_pass = None
for c in C4S:
    row = {}
    for f in C4.FOOTS:
        rs, us = fit(c, C4.A0[f])
        row[f] = dict(rms=rs, U=us, passes=bool(rs <= 0.110 and 0.50 <= us <= 0.80))
    G5[f"{c:g}"] = row
    if first_pass is None and all(row[f]["passes"] for f in C4.FOOTS):
        first_pass = c
for c in (0.0, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0):
    k = f"{c:g}" if c else "0"
    rr = G5.get(k) or G5[min(G5, key=lambda kk: abs(float(kk) - c))]
    P_(f"    c4 = {c:6g}: " + "; ".join(f"{f} {rr[f]['rms']:.4f} @ U {rr[f]['U']:.2f}" for f in C4.FOOTS))
RES["numbers"]["G5"] = G5
if first_pass is not None:
    P_(f"    smallest c4 passing H2 on both footings: {first_pass:g}: " + "; ".join(
        f"{f} {G5[f'{first_pass:g}'][f]['rms']:.4f} @ {G5[f'{first_pass:g}'][f]['U']:.2f}" for f in C4.FOOTS) + "  => REQUIRES A SECOND CONSTANT")
else:
    P_("    no c4 in [0.01, 100] passes H2 on both footings")
RES["numbers"]["G5b_first_pass_c4"] = first_pass
g5 = all(G5["0"][f]["passes"] for f in C4.FOOTS)
P_(f"    C2 (c4 = 0, the construction as built): {'PASS' if g5 else 'FAIL (Upsilon band), inherited from CFG690'}")

# ============================================================================ G6 predictions
P_("\nG6  (reported) predictions at L* = L*_min")
for f in C4.FOOTS:
    a0 = C4.A0[f]
    wb = [g_an(d * AU, 2 * MSUN, Lmin * PC, a0) / (G * 2 * MSUN / (d * AU) ** 2) for d in (1e3, 3e3, 1e4)]
    P_(f"    {f:9s} wide binaries 2 Msun at 1e3/3e3/1e4 AU: anomaly/Newton {wb[0]:.1e} / {wb[1]:.1e} / {wb[2]:.1e} (Newtonian)")

# ============================================================================ verdict
if MUT:
    bites = dict(M1=not g1, M2=not g3, M3=not g4)
    RES["mutate_bites"] = bites
    P_(f"\nMUTATE: {bites}")
    rc = 1 if all(bites.values()) else 0
else:
    v = "COMBINED CONSTRUCTION CONSISTENT" if (g1 and g3 and g4) else "NOT CONSISTENT"
    RES["verdict"] = dict(construction=v, C2="PASS" if g5 else "FAIL (Upsilon band)", G5b_c4=first_pass)
    P_(f"\nVERDICT: {v}; C2 {'PASS' if g5 else 'FAIL (Upsilon band)'}; G5b smallest passing c4 = {first_pass}")
    rc = 0 if ctrl else 1
json.dump(RES, open(os.path.join(HERE, f"cfg694_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(rc)
