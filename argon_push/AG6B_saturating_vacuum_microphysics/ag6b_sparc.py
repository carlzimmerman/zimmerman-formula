"""AG6B A5 (raw SPARC, CFG4 H2 C2 line) + verdict assembly.

Criteria: FROZEN_CRITERIA.md (committed alone, dbcaeba9e). Reads ag6b_media_results.json (this lane) and, read-only,
CFG4_common / CFG4_galaxy_law_results.json / CFG695 cfg695_results.json / AG4b ag4b_results.json.
A5: rms <= 0.110 dex with Upsilon_disk in 0.50-0.80 on BOTH footings (CFG4 statistic exactly as CFG695 S2: SPARC 175, weights
(V/e_V)^2, Upsilon_bul = 1.4 Upsilon_disk, one global Upsilon_disk profiled on 0.30-1.20 step 0.01).
kappa = 1/2 FITTED; both footings, never pooled; no particle species; not theory closed.

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 ag6b_sparc.py      (AG6B_MUTATE=1: Mu5 nu = 1 must give rms >= 0.25; exit 1 iff it bites)
"""
import os, sys, json, math

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LANES = os.path.join(REPO, "campaign_fresh_gravity")
sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402  (read only)
from scipy import special  # noqa: E402

MUT = os.environ.get("AG6B_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ag6b_sparc{TAG}.out"), "w")
RES = {"lane": "AG6B", "script": "ag6b_sparc.py", "criteria": "dbcaeba9e", "mutate": MUT, "A5": {}, "controls": {}, "checks": {}}


def P_(s=""):
    print(s)
    OUT.write(s + "\n")
    OUT.flush()


def check(key, ok, detail=""):
    RES["checks"][key] = dict(ok=bool(ok), detail=detail)
    P_(f"  [{'PASS' if ok else 'FAIL'}] {key}: {detail}")
    return bool(ok)


P_(__doc__.strip())
Z = 2.0 * math.sqrt(8.0 * math.pi / 3.0)
assert abs(Z - C4.Z_FRAME) < 1e-12 and abs(C4.A0["canonical"] - 9.3603e-11) < 1e-15 and abs(C4.A0["alt"] - 1.1312e-10) < 1e-15

# ------------------------------------------------------------------ CFG4 statistic (verbatim construction from CFG695 S2)
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
P_(f"\nSPARC: {len(GAL)} galaxies, {len(Rm)} points")


def fit(nuf, a0v):
    with np.errstate(all="ignore"):
        gb = np.where(OK, GB, 1.0)
        r_ = np.log10(np.where(OK, GO, 1.0)) - np.log10(np.where(OK, nuf(gb / a0v) * gb, 1.0))
    mse = (WW * r_ ** 2).sum(0) / WW.sum(0)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i])


sg = 1 / math.sqrt(2 * math.pi)
LAWS = {   # dimensionless polarization U(x), x = g/a0; u_max
    "n1": (lambda x: x / (1 + x), 1.0),
    "n2": (lambda x: x + 0.5 - np.sqrt(x * x + 0.25), 0.5),
    "F1": (lambda x: -0.5 * np.expm1(-2 * x), 0.5),
    "F2": (lambda x: x * special.erfc(x / (sg * math.sqrt(2))) + sg * math.sqrt(2 / math.pi) * (-np.expm1(-x * x / (2 * sg * sg))),
           1 / math.pi),
    "F3": (lambda x: np.where(x <= 0.5, x - x * x, 0.25), 0.25),
}


def nu_from_U(Uf, umx):
    """nu(y) = x/y with x - U(x) = y (g_N = g - u), by bisection on [y, y + u_max] (U <= u_max, U' < 1)."""
    def nu(y):
        y = np.maximum(y, 1e-300)
        lo, hi = y.copy(), y + umx
        for _ in range(90):
            mid = 0.5 * (lo + hi)
            f = mid - Uf(mid) - y
            lo = np.where(f < 0, mid, lo)
            hi = np.where(f < 0, hi, mid)
        return 0.5 * (lo + hi) / y
    return nu


# ------------------------------------------------------------------ controls
P_("\nCONTROLS")
ref4 = json.load(open(os.path.join(LANES, "CFG4_galaxy_law_results.json")))["numbers"]["H2"]
r695 = json.load(open(os.path.join(LANES, "CFG695_saturating_vacuum", "cfg695_results.json")))["numbers"]["S2"]
r4b = json.load(open(os.path.join(REPO, "argon_push", "AG4b_sparc_population_upsilon", "ag4b_results.json")))["controls"]["K1_n2_reported"]
K = {}
for f in C4.FOOTS:
    rm, um = fit(C4.nu_mono, C4.A0[f])
    r1, u1 = fit(nu_from_U(*LAWS["n1"]), C4.A0[f])
    r2, u2 = fit(nu_from_U(*LAWS["n2"]), C4.A0[f])
    K[f] = dict(K1=(r1, u1, r695[f]["rms"], r695[f]["U"]), K2=(rm, um, ref4[f"{f}|nu_mono"]["rms"], ref4[f"{f}|nu_mono"]["U"]),
                K3=(r2, u2, r4b[f][0], r4b[f][1]))
    P_(f"  {f:9s}: K1 n=1 (numerical inversion) {r1:.6f}@{u1:.2f} vs CFG695 {r695[f]['rms']:.6f}@{r695[f]['U']:.2f} | "
       f"K2 nu_mono {rm:.6f}@{um:.2f} vs CFG4 {ref4[f'{f}|nu_mono']['rms']:.6f}@{ref4[f'{f}|nu_mono']['U']:.2f} | "
       f"K3 n=2 {r2:.6f}@{u2:.2f} vs AG4b {r4b[f][0]:.6f}@{r4b[f][1]:.2f}")
RES["controls"] = K
k1 = check("K1 numerical-inversion solver reproduces CFG695 S2 (rms 1e-6, Upsilon exact), both footings",
           all(abs(K[f]["K1"][0] - K[f]["K1"][2]) <= 1e-6 and K[f]["K1"][1] == K[f]["K1"][3] for f in C4.FOOTS))
k2 = check("K2 CFG4 nu_mono H2 reproduced (rms 1e-6, Upsilon exact), both footings",
           all(abs(K[f]["K2"][0] - K[f]["K2"][2]) <= 1e-6 and K[f]["K2"][1] == K[f]["K2"][3] for f in C4.FOOTS))
k3 = check("K3 n=2 global scan reproduces AG4b K1_n2_reported (rms 5e-5, Upsilon exact), both footings",
           all(abs(K[f]["K3"][0] - K[f]["K3"][2]) <= 5e-5 and K[f]["K3"][1] == K[f]["K3"][3] for f in C4.FOOTS))
ctrl = k1 and k2 and k3


def line(rms, U):
    return bool(rms <= 0.110 and 0.50 <= U <= 0.80)


if MUT:
    S = {f: fit(lambda y: np.ones_like(y), C4.A0[f]) for f in C4.FOOTS}
    bite = all(S[f][0] >= 0.25 for f in C4.FOOTS)
    RES["mutate_bites"] = {"Mu5": bool(bite)}
    P_(f"\nMUTATE Mu5 nu = 1: " + "; ".join(f"{f} {S[f][0]:.4f}@{S[f][1]:.2f}" for f in C4.FOOTS) + f"  -> bites: {bite}")
    json.dump(RES, open(os.path.join(HERE, f"ag6b_sparc_results{TAG}.json"), "w"), indent=1, default=float)
    OUT.close()
    sys.exit(1 if bite else 0)

# ------------------------------------------------------------------ A5
P_("\nA5  raw SPARC, CFG4 H2 line (rms <= 0.110 and Upsilon 0.50-0.80, both footings)")
A5_SPEC = {   # candidate: (law, a0 multiplier)
    "C-1": ("n1", 1.0), "C-3b1": ("n1", 1.0), "E-1": ("n2", 1.0),
    "F-1": ("F1", 1.0), "F-2": ("F2", 1.0), "F-3": ("F3", 1.0),
    "C-5": ("n1", Z), "E-2": ("n2", 2 * Z),
}
A5 = {}
for key, (law, mult) in A5_SPEC.items():
    per = {}
    for f in C4.FOOTS:
        if law == "n1" and mult == 1.0:
            rr, uu = K[f]["K1"][0], K[f]["K1"][1]
        elif law == "n2" and mult == 1.0:
            rr, uu = K[f]["K3"][0], K[f]["K3"][1]
        else:
            rr, uu = fit(nu_from_U(*LAWS[law]), mult * C4.A0[f])
        per[f] = dict(rms=rr, U=uu, passes=line(rr, uu), a0_used=mult * C4.A0[f])
    A5[key] = dict(law=law, a0_multiplier=mult, footings=per, passes=all(per[f]["passes"] for f in C4.FOOTS))
    P_(f"  {key:6s} law {law} @ {mult:.4f} a0: " + " | ".join(f"{f} {per[f]['rms']:.4f} dex @ Ups {per[f]['U']:.2f}"
                                                         for f in C4.FOOTS) + f"  -> {'PASS' if A5[key]['passes'] else 'FAIL'}")
RES["A5"] = A5

# ------------------------------------------------------------------ verdict assembly (frozen rule, section 7)
med = json.load(open(os.path.join(HERE, "ag6b_media_results.json")))
cands = med["candidates"]
P_("\nVERDICT ASSEMBLY")
rows = {}
for k, v in cands.items():
    a14 = bool(v.get("pass_A1_A4"))
    a5 = A5.get(k, {}).get("passes")
    if k == "F-5":
        a5 = True  # in-family spectra: same laws as C-1 (n=1) / E-1 (n=2), both A5 PASS; by construction, never natural
    rows[k] = dict(natural=bool(v.get("natural")), A1_A4=a14, A5=a5, in_family=bool(v.get("in_family")), n_cap=v.get("n_cap"))
nat_pass = [k for k, r in rows.items() if r["natural"] and r["A1_A4"] and r["A5"] is True]
nat_pass_n = {k: rows[k]["n_cap"] for k in nat_pass}
fam_nat = {k: n for k, n in nat_pass_n.items() if rows[k]["in_family"]}
P_(f"  natural candidates passing A1-A5: {nat_pass_n}")
P_(f"  of which in the capacity family: {fam_nat}")
not_scored = [k for k, r in rows.items() if r["A1_A4"] and r["A5"] is None]
P_(f"  A1-A4 passers not SPARC-scored (not natural: two scales / n free; no knob scans): {not_scored}")
ns = sorted({str(n) for n in nat_pass_n.values()})
if not nat_pass:
    verdict = "SCOPED NO-GO"
elif len(fam_nat) >= 1 and len({str(n) for n in fam_nat.values()}) == 1 and len(nat_pass) == len(fam_nat):
    verdict = "DERIVATION (pending second-prediction condition)"
else:
    verdict = "CANDIDATE"
reason = (f"natural passers carry n_cap in {ns}: in-family n = {sorted({str(n) for n in fam_nat.values()})} "
          f"(C-1/C-3b1 Langmuir n=1, E-1 Deser-Levin n=2) plus out-of-family MaxEnt spectra; physics does not pick n")
# discriminators between natural passers (by law)
SPm = med["second_predictions"]
lawname = {"C-1": "C-1 (n=1)", "C-3b1": "C-1 (n=1)", "E-1": "E-1 (n=2)", "F-1": "F-1 exp", "F-2": "F-2 half-normal",
           "F-3": "F-3 uniform"}
laws_present = sorted({lawname[k] for k in nat_pass if k in lawname})
DISC = {}
for i in range(len(laws_present)):
    for j in range(i + 1, len(laws_present)):
        A_, B_ = laws_present[i], laws_present[j]
        a, b = SPm[A_], SPm[B_]
        cand = {"S-a capacity": a["u_max_over_a0"] / b["u_max_over_a0"]}
        for xx in ("3.0", "10.0"):
            if a["tail"][xx] > 0 and b["tail"][xx] > 0:
                cand[f"S-b tail x={xx}"] = a["tail"][xx] / b["tail"][xx]
        for xx in ("0.1", "1.0", "10.0"):
            ga, gb_ = a["gap_Rprime"][xx], b["gap_Rprime"][xx]
            if np.isfinite(ga) and np.isfinite(gb_) and ga > 0 and gb_ > 0:
                cand[f"S-c gap x={xx}"] = ga / gb_
        if "kinetic_Gamma_ratio" in a and "kinetic_Gamma_ratio" in b:
            for xx in ("1.0", "10.0"):
                cand[f"S-d kinetic x={xx}"] = a["kinetic_Gamma_ratio"][xx] / b["kinetic_Gamma_ratio"][xx]
        cand["S-e gN at 99% capacity"] = a["gN_at_99pct"] / b["gN_at_99pct"]
        best = max(cand, key=lambda q: abs(math.log(cand[q])))
        mm = SPm["static_minimax"].get(f"{A_} | {B_}") or SPm["static_minimax"].get(f"{B_} | {A_}")
        DISC[f"{A_} | {B_}"] = dict(largest=best, ratio=cand[best], all=cand, static_minimax_dex=mm["minimax"],
                                    walls=(a["wall"], b["wall"]), testable_now=False)
        P_(f"  {A_:16s} vs {B_:16s}: largest second-prediction ratio {best} = {cand[best]:.4g} "
           f"(static laws differ by <= {mm['minimax']:.4f} dex after a0 rescale); walls {a['wall']} / {b['wall']}")
RES["verdict"] = dict(class_=verdict, reason=reason, natural_passers=nat_pass_n, in_family_natural=fam_nat,
                      not_scored=not_scored, discriminators=DISC,
                      testable_now="NONE: S-a needs late-type strong lenses with kinematic M/L (AG4c: not on disk); "
                                   "S-b needs phantom acceleration to ~0.01 a0 at g >= 10 a0; S-c/S-d need time-dependent "
                                   "fields (no data path)",
                      attached=["T-A scoped no-go: analytic equilibrium dielectrics (Langevin, Brillouin, Landau, Born-Infeld, "
                                "Euler-Heisenberg, GL depairing, FJC) give g_N ~ g^3 (V ~ r^1/6)",
                                "T-F2: IFR capacity spectra give n_cap >= 2; n = 1 needs a decreasing-hazard c^-3 spectrum"])
P_(f"\nVERDICT: {verdict}")
P_(f"  {reason}")
P_("  attached: T-A scoped no-go on analytic dielectric saturation; T-F2 bound (IFR => n_cap >= 2)")
json.dump(RES, open(os.path.join(HERE, f"ag6b_sparc_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(0 if ctrl else 1)
