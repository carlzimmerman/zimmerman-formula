"""CFG692: gravitating polarization - the bound charge div P of a vacuum polarization field as the cold mass.

Criteria: FROZEN_CRITERIA.md (committed alone, 097b2feee). Units: u = 4 pi G |P| (an acceleration).
W(P) = 2 pi G P^2 + (4 pi G)^2 P^3/(3 a0)  =>  W'(P) = u + u^2/a0 (critical medium + SI cubic). Antiscreening: g = g_N + u.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg692.py      (CFG692_MUTATE=1: off-critical, screening sign, nu = 1; exit 1 iff all bite)
"""
import os, sys, json, math

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402  (read only)

MUT = os.environ.get("CFG692_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg692{TAG}.out"), "w")
RES = {"lane": "CFG692", "criteria": "097b2feee", "mutate": MUT, "checks": {}, "numbers": {}}


def P_(s=""):
    print(s)
    OUT.write(s + "\n")


def check(key, ok, detail):
    RES["checks"][key] = dict(ok=bool(ok), detail=detail)
    P_(f"  [{'PASS' if ok else 'FAIL'}] {key}: {detail}")
    return bool(ok)


P_(__doc__.strip())
g, gN, a0, u, G, x, Pm, c, s_, k, gam = sp.symbols("g g_N a_0 u G x P c s k gamma", positive=True)
crit = sp.Rational(11, 10) if MUT else 1                     # M1: W''(0) = 4 pi G * 1.1
sign = -1 if MUT else 1                                       # M2: screening sign

# ============================================================================ T1 static law
P_("\nT1  static law: W'(P) = g and g = g_N + sign*u")
Wp = crit * u + u ** 2 / a0                                   # W'(P) in acceleration units
u_of_g = [r for r in sp.solve(sp.Eq(Wp, g), u) if sp.simplify(r.subs({g: 1, a0: 1})) .is_positive][0]
gN_of_g = sp.simplify(g - sign * u_of_g)
mu = sp.simplify(gN_of_g / g)
P_(f"    u(g) = {u_of_g};  g_N(g) = {gN_of_g};  mu(x = g/a0) = {sp.simplify(mu.subs(g, x * a0))}")
deep = sp.limit(gN_of_g / (g ** 2 / a0), g, 0)
newt = sp.limit(mu, g, sp.oo)
P_(f"    deep: lim g->0 g_N/(g^2/a0) = {deep};  Newtonian: lim g->oo mu = {newt};  high-field u ~ {sp.limit(u_of_g / sp.sqrt(a0 * g), g, sp.oo)} sqrt(a0 g)")
t1 = check("T1 deep g_N = g^2/a0 and mu -> 1", deep == 1 and newt == 1, f"deep ratio {deep}, mu(oo) {newt}")
# inverse: given g_N
gsol = sp.solve(sp.Eq(gN_of_g, gN), g)
P_(f"    inverse g(g_N): {gsol}")
nu_closed = sp.simplify(gN + sp.sqrt(a0 * gN))
inv_match = any(sp.simplify(gg - nu_closed) == 0 for gg in gsol)
P_(f"    equals g_N + sqrt(a0 g_N) (nu = 1 + y^-1/2, the CFG690 interpolation): {inv_match}")

# ============================================================================ T2 stability (fixed baryons)
P_("\nT2  second variation per mode: Q = diag(W'', W'/P) - 4 pi G khat khat^T  (+ gamma k^2 I); khat = (c, s), c^2 + s^2 = 1")
# with u = 4 pi G P: W'' = 4 pi G dW'/du ; W'/P = 4 pi G W'/u
A = sp.simplify(4 * sp.pi * G * sp.diff(Wp, u))
B = sp.simplify(4 * sp.pi * G * Wp / u)
margin_L = sp.simplify(A - 4 * sp.pi * G)
margin_T = sp.simplify(B - 4 * sp.pi * G)
cond = sp.simplify(c ** 2 / (A / (4 * sp.pi * G)) + (1 - c ** 2) / (B / (4 * sp.pi * G)))   # PD iff < 1
P_(f"    W'' = {A};  W'/P = {B};  longitudinal margin W'' - 4piG = {margin_L};  transverse-with-k-along-dP margin = {margin_T}")
P_(f"    PD condition (gamma = 0): c^2/(W''/4piG) + s^2/((W'/P)/4piG) = {cond} < 1")
num = [float(cond.subs({u: uu, a0: 1, c: cc})) for uu in (1e-4, 1e-2, 1, 1e2) for cc in (0, 0.5, 1)]
pd = all(v < 1 for v in num) and sp.simplify(margin_L).subs({u: 1, a0: 1, G: 1}).is_positive
t2 = check("T2 static medium stable for every P > 0 at gamma = 0", pd,
           f"max PD condition over u/a0 in {{1e-4..1e2}}, all k directions = {max(num):.6f} (< 1); longitudinal margin {margin_L}")
P_("    deep regime (u << a0): margins -> 0 as u/a0 -> 0 (the medium is near-critical there; restoring rate ~ sqrt(8 pi G u/(a0 I)))")

# ============================================================================ T3 lensing and ledger
P_("\nT3  (a) Poisson: lap Phi = 4 pi G (rho_b + div P): the cold mass rho_c = div P is in the one equation that sets the metric")
r, M = sp.symbols("r M", positive=True)
Pdeep = sp.sqrt(G * M * a0) / (4 * sp.pi * G * r)          # u = g = sqrt(G M a0)/r in the deep tail
rho_c = sp.simplify(sp.diff(r ** 2 * Pdeep, r) / r ** 2)
Mc = sp.simplify(4 * sp.pi * r ** 2 * Pdeep)
Mc_int = sp.simplify(sp.integrate(4 * sp.pi * r ** 2 * rho_c, (r, 0, r)))
P_(f"    (b) deep spherical: P = {Pdeep};  rho_c = div P = {rho_c};  M_c(<r) = surface flux 4 pi r^2 P = {Mc} (= volume integral {Mc_int})")
t3 = check("T3 deep cold mass rho_c ~ r^-2, M_c(<r) ~ r, M_c = surface flux (moved, not created)",
           sp.simplify(rho_c * r ** 2).has(r) is False and sp.simplify(Mc / r).has(r) is False and sp.simplify(Mc - Mc_int) == 0,
           "the compensating negative bound charge sits where P falls to zero: the outer edge of each polarized region")

# ============================================================================ T4 raw SPARC
P_("\nT4  raw SPARC, CFG4 statistic (CFG690 copy), nu from T1")
GAL = C4.load_sparc(); NG = len(GAL)
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2); KPC_S = 3.0857e19
Rm = np.concatenate([q["R"] for q in GAL]) * KPC_S
Vo = np.concatenate([q["Vobs"] for q in GAL]); eV = np.concatenate([q["eV"] for q in GAL])
Vg = np.concatenate([q["Vgas"] for q in GAL]); Vd = np.concatenate([q["Vdisk"] for q in GAL]); Vb = np.concatenate([q["Vbul"] for q in GAL])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GB = VB2 * 1e6 / Rm[:, None]
GO = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (Vo > 0)[:, None]
WW = np.where(OK, (1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2)[:, None], 0.0)


def fit(nuf, a0v):
    with np.errstate(all="ignore"):
        gb = np.where(OK, GB, 1.0)
        r_ = np.log10(np.where(OK, GO, 1.0)) - np.log10(np.where(OK, nuf(gb / a0v) * gb, 1.0))
    mse = (WW * r_ ** 2).sum(0) / WW.sum(0)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i])


nu_T1 = sp.lambdify(x, sp.simplify(nu_closed.subs({gN: x * a0}) / (x * a0)) if inv_match else 1 + x ** -0.5, "numpy")
NU = (lambda yy: np.ones_like(yy)) if MUT else nu_T1
ref = json.load(open(os.path.join(LANES, "CFG4_galaxy_law_results.json")))["numbers"]["H2"]
T4, ctrl = {}, True
for f in C4.FOOTS:
    rm, um = fit(C4.nu_mono, C4.A0[f])
    ctrl &= abs(rm - ref[f"{f}|nu_mono"]["rms"]) <= 1e-6 and um == ref[f"{f}|nu_mono"]["U"]
    rs, us = fit(NU, C4.A0[f])
    T4[f] = dict(rms=rs, U=us, passes=bool(rs <= 0.110 and 0.50 <= us <= 0.80))
    P_(f"    {f:9s}: nu_crit {rs:.4f} dex @ Upsilon {us:.2f}  (nu_mono control {rm:.4f} @ {um:.2f})")
RES["numbers"]["T4"] = T4
cT4 = check("T4 CONTROL reproduces CFG4 nu_mono", ctrl, "")
t4 = check("T4 C2 line on both footings", all(T4[f]["passes"] for f in C4.FOOTS), "")

# ============================================================================ T5 external field
P_("\nT5  S2: satellite (g_i << g_e) linear response about the host's P(g_e)")
uf = sp.lambdify((g, a0), u_of_g)
gNf = sp.lambdify((g, a0), gN_of_g)
dudg = sp.lambdify((g, a0), sp.diff(u_of_g, g))
T5 = {}
gi = 0.01
nu_iso = gi / gNf(gi, 1.0)
for ge in (0.1, 1.0):
    nl = 1 / (1 - sign * dudg(ge, 1.0)); nt = 1 / (1 - sign * uf(ge, 1.0) / ge)
    T5[str(ge)] = dict(nu_par=nl, nu_perp=nt)
    P_(f"    g_e = {ge:4.1f} a0: satellite boost nu_par {nl:.3f}, nu_perp {nt:.3f}   vs isolated at g_i = 0.01 a0: {nu_iso:.2f}")
T5["isolated_gi_0.01"] = nu_iso
RES["numbers"]["T5"] = T5
s2_fail = all(abs(T5[k]["nu_par"] - nu_iso) / nu_iso > 1e-3 for k in ("0.1", "1.0"))
check("T5 S2 (ignore external fields)", not s2_fail, "boost depends on g_e: S2 FAILS" if s2_fail else "boost independent of g_e")

# ============================================================================ T6 Solar System (reported)
P_("\nT6  (reported) high-field residual dg/g_N = sqrt(a0/g_N)")
GM, AU = 1.32712440018e20, 1.495978707e11
T6 = {f: {n: math.sqrt(C4.A0[f] / (GM / (d * AU) ** 2)) for n, d in (("1AU", 1.0), ("Saturn", 9.58))} for f in C4.FOOTS}
for f in C4.FOOTS:
    P_(f"    {f:9s}: 1 AU {T6[f]['1AU']:.3e}; Saturn {T6[f]['Saturn']:.3e}")
RES["numbers"]["T6"] = T6

# ============================================================================ verdict / MUTATE
rows = dict(R0="R0-SHAPED (criticality + SI)", M1a="UNTESTED (P-wave radiation named, not run)",
            M1c="PASS (fixed baryons, gamma = 0)" if t2 else "FAIL",
            M2a_M2b="PASS structurally: cold mass = surface flux of P, moved not created" if t3 else "FAIL",
            M3a="CONDITIONAL (Newtonian lensing = dynamics; Phi = Psi not derived)",
            C2="PASS" if t4 else "FAIL (Upsilon band, = CFG690)", S2="FAIL" if s2_fail else "PASS",
            S5="needs stiffness screening (CFG691 analogue not run for this equation)")
if MUT:
    bites = dict(M1=not t1, M2=not t1, M3=all(T4[f]["rms"] >= 0.25 for f in C4.FOOTS))
    RES["mutate_bites"] = bites
    P_(f"\nMUTATE: {bites}")
    rc = 1 if all(bites.values()) else 0
else:
    RES["verdict"] = rows
    P_("\nVERDICT (CFG679 rows): " + "; ".join(f"{k} {v}" for k, v in rows.items()))
    rc = 0 if cT4 else 1


def js(o):
    if isinstance(o, dict):
        return {str(kk): js(v) for kk, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [js(v) for v in o]
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    if isinstance(o, sp.Basic):
        return str(o)
    return o


json.dump(js(RES), open(os.path.join(HERE, f"cfg692_results{TAG}.json"), "w"), indent=1)
OUT.close()
sys.exit(rc)
