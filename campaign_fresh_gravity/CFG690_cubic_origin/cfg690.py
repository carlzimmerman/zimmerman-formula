"""CFG690: does deep-regime scale invariance (SI) fix astra's cubic |P|^3, and is SI independent of the law?

Criteria: FROZEN_CRITERIA.md (committed alone, d87cde1d4). T1/T2 sympy; T3 raw SPARC on the CFG4 statistic (copied, with controls
that reproduce CFG4's committed numbers); T4 Solar-System residual, reported only.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

Run from anywhere:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg690.py      (CFG690_MUTATE=1 for the MUTATE run; exit 1 iff all bite)
"""
import os, sys, json, math

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import CFG4_common as C4  # noqa: E402  (read only: A0, FOOTS, nu_mono, load_sparc)

MUT = os.environ.get("CFG690_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg690{TAG}.out"), "w")
RES = {"lane": "CFG690", "criteria": "d87cde1d4", "mutate": MUT, "checks": {}, "numbers": {}}


def P(s=""):
    print(s)
    OUT.write(s + "\n")


def check(key, ok, detail):
    RES["checks"][key] = dict(ok=bool(ok), detail=detail)
    P(f"  [{'PASS' if ok else 'FAIL'}] {key}: {detail}")
    return bool(ok)


P(__doc__.strip())
lam, p, n, beta, a, alpha, c = sp.symbols("lambda p n beta a alpha c", positive=True)

# ============================================================================ T1  SI uniqueness
P("\nT1  SI: x,t -> lambda x, lambda t; fixed mass => rho_b -> lambda^-3 rho_b, d^3x -> lambda^3 d^3x, phi -> phi (+ const ln lambda)")
n_W = 2 if MUT else n                                          # M1: W = |P|^2
fac_W = sp.simplify(lam ** 3 * (p / lam) ** n_W / p ** n_W)     # int W d^3x, deep fields: P -> P/lambda
sol_n = sp.solve(sp.Eq(sp.log(fac_W) / sp.log(lam), 0), n) if not MUT else []
P(f"    int |P|^n d^3x scales as {sp.simplify(fac_W)}; invariant for all lambda iff n in {sol_n}")
t1a_pow = (not MUT) and sol_n == [3]
if MUT:
    t1a_pow = sp.simplify(fac_W - 1) == 0
Wf = sp.Function("W")
# general W: lambda^3 W(p/lambda) = W(p) for all lambda; set lambda = p => p^3 W(1) = W(p)
fe = sp.Eq(lam ** 3 * Wf(p / lam), Wf(p))
gen = sp.Eq(fe.lhs.subs(lam, p), fe.rhs)
P(f"    general W: {fe}  at lambda = p  ->  {gen}  =>  W(p) = W(1) p^3 (homogeneous degree 3)")
# and W = c p^3 satisfies it identically
t1a_gen = sp.simplify(fe.lhs.subs(Wf(p / lam), c * (p / lam) ** 3) - c * p ** 3) == 0
rho_exp = -2 if MUT else -3                                     # M2: wrong mass scaling
fac_src = sp.simplify(lam ** 3 * lam ** rho_exp)
P(f"    source int alpha rho_b phi d^3x scales as {fac_src} (phi's additive ln(lambda) shift multiplies the fixed mass: no force)")
# quadratic and stiffness terms
fac_quad_on = sp.simplify(lam ** 3 * (lam ** -2) ** 2)          # on-shell D = alpha M/(4 pi r^2) -> lambda^-2
fac_quad_off = sp.simplify(lam ** 3 * (lam ** -1) ** 2)         # off-shell grad phi - P/a -> lambda^-1
fac_stiff = sp.simplify(lam ** 3 * (lam ** -2) ** 2)            # grad P -> lambda^-2
P(f"    quadratic |grad phi - P/a|^2 = |D|^2/a^2: on-shell (Gauss fixes D) {fac_quad_on}; off-shell {fac_quad_off} (a constraint "
  f"term that enforces P = a grad phi in the deep regime); stiffness |grad P|^2: {fac_stiff}")
deep_eff = sp.simplify(lam ** 3 * (beta * a ** 3 * (p / lam) ** 3 / 3) / (beta * a ** 3 * p ** 3 / 3))
P(f"    deep effective action on P = a grad phi: int beta a^3 |grad phi|^3/3 d^3x scales as {deep_eff} (the AQUAL deep form)")
t1 = check("T1 SI forces the cubic", t1a_pow and t1a_gen and fac_src == 1 and fac_quad_on == lam ** -1 and fac_stiff == lam ** -1,
           f"|P|^n invariant iff n = 3: {t1a_pow}; general W homogeneous degree 3: {t1a_gen}; source factor {fac_src}; "
           f"quadratic on-shell {fac_quad_on}, stiffness {fac_stiff} (irrelevant at large lambda)")

# ============================================================================ T2  is SI the law restated?
P("\nT2  W = beta |P|^n / n, gamma = 0, point source: D = a beta p^(n-1) (from grad phi = P/a + beta p^(n-2) P), D = alpha M/(4 pi r^2)")
M, r, G, a0, A0 = sp.symbols("M r G a_0 A_0", positive=True)
D = alpha * M / (4 * sp.pi * r ** 2)
pn = (D / (a * beta)) ** (1 / (n - 1))
V2 = sp.simplify(alpha * pn / a * r)                             # deep: g ~ alpha p / a
dlnV2_dlnr = sp.simplify(sp.diff(sp.log(V2), r) * r)
dlnV4_dlnM = sp.simplify(2 * sp.diff(sp.log(V2), M) * M)
n_flat = sp.solve(sp.Eq(dlnV2_dlnr, 0), n)
n_btfr = sp.solve(sp.Eq(dlnV4_dlnM, 1), n)
P(f"    dlnV^2/dlnr = {dlnV2_dlnr}  -> flat iff n in {n_flat};  dlnV^4/dlnM = {dlnV4_dlnM}  -> V^4 propto M iff n in {n_btfr}")
t2a = n_flat == [3] and n_btfr == [3]
# (b) dimensional analysis: V = A0^x M^y r^z, [A0] = L^4 M^-1 T^-4
x, y, z = sp.symbols("x y z")
sol = sp.solve([sp.Eq(4 * x + z, 1), sp.Eq(-x + y, 0), sp.Eq(-4 * x, -1)], [x, y, z], dict=True)
P(f"    SI + G, a0 only as A0 = G a0 ([L^4 M^-1 T^-4]): V = A0^x M^y r^z with [V] = L T^-1  ->  {sol}  (unique; no r dependence)")
t2b = sol == [{x: sp.Rational(1, 4), y: sp.Rational(1, 4), z: 0}]
# (c) the deep law is SI-invariant; Newton is not
gdeep = sp.sqrt(A0 * M) / r
inv_deep = sp.simplify(gdeep.subs(r, lam * r) * lam / gdeep)      # accelerations scale as lambda^-1 under SI
inv_newt = sp.simplify((G * M / (lam * r) ** 2) * lam / (G * M / r ** 2))
P(f"    deep law g = sqrt(A0 M)/r: g(lambda r) / (g(r)/lambda) = {inv_deep};  Newton: {inv_newt}")
t2c = inv_deep == 1 and inv_newt != 1
t2 = check("T2 SI is equivalent to the deep law (flat + BTFR)", t2a and t2b and t2c,
           f"(a) flat and BTFR iff n = 3: {t2a}; (b) SI + dims => V = (A0 M)^1/4: {t2b}; (c) deep law SI-invariant, Newton not: {t2c}")
R0 = "R0-SHAPED, REDUCED" if (t1 and t2) else "R0-SHAPED (unchanged)"
P(f"    reading rule: no committed source derives SI independently (searched before the freeze) => cubic R0 status: {R0}")

# ============================================================================ T3  raw SPARC, CFG4 statistic (copied)
P("\nT3  raw SPARC: astra's gamma = 0 interpolation nu_SI(y) = 1 + y^-1/2 on the CFG4 statistic (gamma = 0 limit)")
GAL = C4.load_sparc()
NG = len(GAL)
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
KPC_S = 3.0857e19
Rm = np.concatenate([g["R"] for g in GAL]) * KPC_S
Vo = np.concatenate([g["Vobs"] for g in GAL])
eV = np.concatenate([g["eV"] for g in GAL])
Vg = np.concatenate([g["Vgas"] for g in GAL])
Vd = np.concatenate([g["Vdisk"] for g in GAL])
Vb = np.concatenate([g["Vbul"] for g in GAL])
GI = np.concatenate([np.full(len(g["R"]), i) for i, g in enumerate(GAL)])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GB = VB2 * 1e6 / Rm[:, None]
GO = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (Vo > 0)[:, None]
WPT = 1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2
WW = np.where(OK, WPT[:, None], 0.0)
ONEHOT = np.zeros((NG, len(Rm)))
ONEHOT[GI, np.arange(len(Rm))] = 1.0


def fit(nuf, a0v):
    with np.errstate(all="ignore"):
        r_ = np.log10(np.where(OK, GO, 1.0)) - np.log10(np.where(OK, nuf(np.where(OK, GB, 1.0) / a0v) * np.where(OK, GB, 1.0), 1.0))
    S, W = ONEHOT @ (WW * r_ ** 2), ONEHOT @ WW
    mse = S.sum(0) / W.sum(0)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i])


NEWTON = lambda yy: np.ones_like(np.asarray(yy, float))
NU_SI = (lambda yy: np.ones_like(np.asarray(yy, float))) if MUT else (lambda yy: 1.0 + np.asarray(yy, float) ** -0.5)
ref = json.load(open(os.path.join(os.path.dirname(HERE), "CFG4_galaxy_law_results.json")))["numbers"]["H2"]
ctrl, T3 = True, {}
P(f"    SPARC: {NG} galaxies, {len(Rm)} points; Upsilon_disk grid {UPS[0]:.2f}-{UPS[-1]:.2f}")
for f in C4.FOOTS:
    rm, um = fit(C4.nu_mono, C4.A0[f])
    rn, un = fit(NEWTON, C4.A0[f])
    rs, us = fit(NU_SI, C4.A0[f])
    dm = abs(rm - ref[f"{f}|nu_mono"]["rms"]); dn = abs(rn - ref[f"{f}|Newton"]["rms"])
    okc = dm <= 1e-6 and dn <= 1e-6 and um == ref[f"{f}|nu_mono"]["U"] and un == ref[f"{f}|Newton"]["U"]
    ctrl &= okc
    T3[f] = dict(rms_SI=rs, U_SI=us, rms_mono=rm, U_mono=um, rms_newton=rn, U_newton=un, d_SI_minus_mono=rs - rm,
                 passes=bool(rs <= 0.110 and 0.50 <= us <= 0.80))
    P(f"    {f:9s} a0 {C4.A0[f]:.4e}: nu_SI {rs:.4f} dex @ U {us:.2f}  |  nu_mono {rm:.4f} @ {um:.2f} (CFG4 {ref[f'{f}|nu_mono']['rms']:.4f}"
      f" @ {ref[f'{f}|nu_mono']['U']:.2f})  |  Newton {rn:.4f} @ {un:.2f}  |  nu_SI - mono {rs - rm:+.4f}")
RES["numbers"]["T3"] = T3
# POST-HOC (added after the first run, disclosed in the README; no verdict weight): rms of nu_SI with Upsilon_disk held at the
# band edge 0.50, to size the Upsilon-band failure.
i50 = int(np.where(UPS == 0.50)[0][0])
for f in C4.FOOTS:
    with np.errstate(all="ignore"):
        r_ = np.log10(np.where(OK, GO, 1.0)) - np.log10(np.where(OK, NU_SI(np.where(OK, GB, 1.0) / C4.A0[f]) * np.where(OK, GB, 1.0), 1.0))
    T3[f]["rms_SI_at_U050_posthoc"] = math.sqrt((WW[:, i50] * r_[:, i50] ** 2).sum() / WW[:, i50].sum())
    P(f"    POST-HOC {f:9s}: nu_SI rms at Upsilon_disk 0.50 = {T3[f]['rms_SI_at_U050_posthoc']:.4f} dex (no verdict weight)")
c3 = check("T3 CONTROL reproduces CFG4 nu_mono and Newton (|d rms| <= 1e-6, Upsilon exact)", ctrl, "both footings")
t3 = all(T3[f]["passes"] for f in C4.FOOTS)
check("T3 nu_SI passes the CFG4 H2 line on both footings (gamma = 0 limit)", t3,
      "; ".join(f"{f} {T3[f]['rms_SI']:.4f}@{T3[f]['U_SI']:.2f}" for f in C4.FOOTS))

# ============================================================================ T4  Solar System residual at gamma = 0 (reported)
P("\nT4  (reported only) high-field residual dg/g_N = y^-1/2 at gamma = 0")
GM_SUN, AU = 1.32712440018e20, 1.495978707e11
T4 = {}
for f in C4.FOOTS:
    T4[f] = {}
    for name, d in (("1 AU", 1.0), ("Saturn 9.58 AU", 9.58)):
        gN = GM_SUN / (d * AU) ** 2
        T4[f][name] = dict(gN=gN, dg_over_g=(gN / C4.A0[f]) ** -0.5)
        P(f"    {f:9s} {name:15s}: g_N {gN:.3e} m/s^2, dg/g_N {T4[f][name]['dg_over_g']:.3e}")
RES["numbers"]["T4"] = T4

# ============================================================================ verdict / MUTATE
if MUT:
    bites = dict(M1=not t1a_pow, M2=fac_src != 1, M3=all(T3[f]["rms_SI"] >= 0.25 for f in C4.FOOTS))
    P(f"\nMUTATE: {bites}")
    RES["mutate_bites"] = bites
    rc = 1 if all(bites.values()) else 0
else:
    RES["verdict"] = dict(cubic_R0=R0, C2_gamma0="PASS" if t3 else "FAIL")
    P(f"\nVERDICT: cubic R0 = {R0}; astra gamma = 0 interpolation on SPARC (C2) = {'PASS' if t3 else 'FAIL'}")
    rc = 0 if c3 else 1


def js(o):
    if isinstance(o, dict):
        return {str(k): js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [js(v) for v in o]
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    if isinstance(o, sp.Basic):
        return str(o)
    return o


json.dump(js(RES), open(os.path.join(HERE, f"cfg690_results{TAG}.json"), "w"), indent=1)
OUT.close()
sys.exit(rc)
