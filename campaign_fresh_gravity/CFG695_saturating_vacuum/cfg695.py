"""CFG695: a vacuum whose polarization saturates at a0: W'(u) = u/(1 - u/a0), u = 4 pi G |P|.

Criteria: FROZEN_CRITERIA.md (committed alone, dd0f52abe; origin post-hoc from CFG694 G5b, disclosed). S1 sympy; S2 raw SPARC
(CFG4 statistic, CFG690 copy; controls); S3 Solar-System carry-over; S4 surface-density bound reported.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg695.py      (CFG695_MUTATE=1: saturation at 2 a0, nu = 1; exit 1 iff both bite)
"""
import os, sys, json, math

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402  (read only)

MUT = os.environ.get("CFG695_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg695{TAG}.out"), "w")
RES = {"lane": "CFG695", "criteria": "dd0f52abe", "mutate": MUT, "checks": {}, "numbers": {}}


def P_(s=""):
    print(s)
    OUT.write(s + "\n")


def check(key, ok, detail):
    RES["checks"][key] = dict(ok=bool(ok), detail=detail)
    P_(f"  [{'PASS' if ok else 'FAIL'}] {key}: {detail}")
    return bool(ok)


P_(__doc__.strip())
u, g, gN, a0, G, c = sp.symbols("u g g_N a_0 G c", positive=True)
usat = 2 * a0 if MUT else a0                                          # M1: saturation at 2 a0

# ============================================================================ S1 structure
P_("\nS1  structure")
Wp = u / (1 - u / usat)                                               # W'(u) in acceleration units
W = sp.integrate(Wp, (u, 0, u)) / (4 * sp.pi * G)                     # W as energy density: dW/dP = W'(u), dP = du/4piG
ser = sp.series(sp.simplify(W), u, 0, 5).removeO()
expect = u ** 2 / (8 * sp.pi * G) + u ** 3 / (12 * sp.pi * G * a0) + u ** 4 / (16 * sp.pi * G * a0 ** 2)
# frozen normalisations in P: 2 pi G P^2, (4 pi G)^2 P^3/(3 a0), c4 (4 pi G)^3 P^4/(4 a0^2) with c4 = 1; P = u/4piG
s1a = sp.simplify(sp.expand(ser - expect)) == 0
P_(f"    W(u) = {sp.simplify(W)};  series to u^4: {sp.expand(ser)}  == critical + SI cubic + c4=1 quartic: {s1a}")
usol = sp.solve(sp.Eq(Wp, g), u)[0]
law = sp.simplify(g - usol)
s1b = sp.simplify(law - g ** 2 / (g + a0)) == 0 and sp.limit(law / (g ** 2 / a0), g, 0) == 1
P_(f"    u(g) = {sp.simplify(usol)};  g_N(g) = {law};  == g^2/(g + a0): {sp.simplify(law - g ** 2 / (g + a0)) == 0};  "
   f"deep coefficient lim g_N/(g^2/a0) = {sp.limit(law / (g ** 2 / a0), g, 0)};  high-field u -> {sp.limit(usol, g, sp.oo)}")
A = sp.simplify(4 * sp.pi * G * sp.diff(Wp, u))                        # W''
B = sp.simplify(4 * sp.pi * G * Wp / u)                                # W'/P
cond = sp.simplify(c ** 2 / (A / (4 * sp.pi * G)) + (1 - c ** 2) / (B / (4 * sp.pi * G)))
vals = [float(cond.subs({u: f_ * a0, c: cc})) for f_ in (1e-4, 0.01, 0.3, 0.9, 0.999) for cc in (0, 0.5, 1)]
s1c = max(vals) < 1
P_(f"    W'' = {A}; W'/P = {B}; PD condition max over u/a0 in (1e-4..0.999), all k = {max(vals):.6f} (< 1)")
s1 = check("S1 expansion, resummed law, stability", s1a and s1b and s1c, f"(a) {s1a} (b) {s1b} (c) {s1c}")

# ============================================================================ S2 raw SPARC
P_("\nS2  raw SPARC, CFG4 statistic: nu_simple = (1 + sqrt(1 + 4/y))/2")
GAL = C4.load_sparc()
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


NU_SIMPLE = (lambda y: np.ones_like(y)) if MUT else (lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-300))))
ref = json.load(open(os.path.join(LANES, "CFG4_galaxy_law_results.json")))["numbers"]["H2"]
c690 = json.load(open(os.path.join(LANES, "CFG690_cubic_origin", "cfg690_results.json")))["numbers"]["T3"]
ctrl, S2 = True, {}
for f in C4.FOOTS:
    rm, um = fit(C4.nu_mono, C4.A0[f])
    r9, u9 = fit(lambda y: 1 + np.maximum(y, 1e-300) ** -0.5, C4.A0[f])
    ctrl &= abs(rm - ref[f"{f}|nu_mono"]["rms"]) <= 1e-6 and um == ref[f"{f}|nu_mono"]["U"]
    ctrl &= abs(r9 - c690[f]["rms_SI"]) <= 1e-6 and u9 == c690[f]["U_SI"]
    rs, us = fit(NU_SIMPLE, C4.A0[f])
    S2[f] = dict(rms=rs, U=us, passes=bool(rs <= 0.110 and 0.50 <= us <= 0.80), rms_mono=rm, U_mono=um)
    P_(f"    {f:9s}: saturating vacuum {rs:.4f} dex @ Upsilon {us:.2f}   (nu_mono {rm:.4f} @ {um:.2f}; CFG690 cubic {r9:.4f} @ {u9:.2f})")
RES["numbers"]["S2"] = S2
check("S2 CONTROLS reproduce CFG4 nu_mono and CFG690 T3", ctrl, "")
s2 = check("S2 C2 line (rms <= 0.110, Upsilon 0.50-0.80) on both footings", all(S2[f]["passes"] for f in C4.FOOTS),
           "; ".join(f"{f} {S2[f]['rms']:.4f}@{S2[f]['U']:.2f}" for f in C4.FOOTS))

# ============================================================================ S3 Solar System carry-over
P_("\nS3  Sun's screened inner anomaly GM/L*^2 at L* = 5.75 pc vs a0")
GM, PC = 1.32712440018e20, 3.0856775814913673e16
Lmin = json.load(open(os.path.join(LANES, "CFG691_stiffness_window", "cfg691_results.json")))["numbers"]["G_SS"]["canonical"]["Lmin_pc"]
inner = GM / (Lmin * PC) ** 2
S3 = {f: inner / C4.A0[f] for f in C4.FOOTS}
for f in C4.FOOTS:
    P_(f"    {f:9s}: u/a0 = {S3[f]:.2e}")
s3 = check("S3 saturation negligible in the screened Solar System (u/a0 <= 1e-3)", all(v <= 1e-3 for v in S3.values()), "")

# ============================================================================ S4 surface density (reported)
P_("\nS4  (reported) u <= a0  =>  M_ph(<r) <= a0 r^2/G  =>  mean phantom surface density <= a0/(pi G) = 2 Sigma_M (Sigma_M = a0/2piG)")
for f in C4.FOOTS:
    sm = C4.A0[f] / (2 * math.pi * 6.6743e-11) / (1.98847e30 / PC ** 2)
    P_(f"    {f:9s}: Sigma_M = {sm:.0f} Msun/pc^2; bound a0/(pi G) = {2 * sm:.0f} Msun/pc^2")

if MUT:
    bites = dict(M1=not s1, M2=all(S2[f]["rms"] >= 0.25 for f in C4.FOOTS))
    RES["mutate_bites"] = bites
    P_(f"\nMUTATE: {bites}")
    rc = 1 if all(bites.values()) else 0
else:
    ok = s1 and s2 and s3
    RES["verdict"] = "SATURATING VACUUM PASSES C2" if ok else "FAILS"
    P_(f"\nVERDICT: {RES['verdict']} (R0-SHAPED: saturation; M1a, B1, relativistic completion open; kappa fitted)")
    rc = 0 if ctrl else 1
json.dump(RES, open(os.path.join(HERE, f"cfg695_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(rc)
