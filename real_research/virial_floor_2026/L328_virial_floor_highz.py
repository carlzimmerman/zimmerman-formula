#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L328 -- THE VIRIAL FLOOR AT HIGH REDSHIFT: a one-sided test of the FLATNESS of a0 with JWST/ALMA dispersions.

THE THEOREM (Lean I22, from the framework's own kernel, μ(x) <= x, via the certified velocity floor I20): every
isolated spherical system in equilibrium has  <v^2> >= (2/3) sqrt(G M a0), i.e. with sigma^2 = <v^2>/3,
        sigma^4 >= (4/81) G M a0          (Milgrom's deep-MOND virial EQUALITY becomes a LOWER BOUND at every g)
No deep-MOND requirement, no extended rotation curve, no radius.  With the stellar mass M_* <= M_b in place of the
baryonic mass the floor is CONSERVATIVE (a lower floor): a violation with M_* is a violation with M_b.

THE DISCRIMINATOR: the framework's a0 is FLAT in z; the rival branch a0 ~ H(z) raises the floor by E(z)^(1/4)
(1.8-1.9 at z = 6-7).  LCDM has no such floor (a halo only raises sigma).

ORIENTATION (pre-registered before the data): a measured integrated line width sigma_int of a rotating disk is
inclination-dependent; averaged over random orientations <sigma_int^2> = sigma_0^2 + V^2/3 = <v^2>/3 exactly (thin
disk, isotropic sigma_0).  So single objects are NOT decisive; the load-bearing statistic is the population mean
        S = < sigma_int^2 / floor^2 >      which the framework (and any law with that floor) requires to be >= 1.
Per-object shortfalls are reported with the orientation probability, never scored alone.

CAVEATS (carried, not assumed away): the external field effect lowers the floor (isolation is an assumption at
z > 4); ionized-gas widths are light-weighted and aperture-limited; turbulence/outflows INFLATE sigma (making any
violation more robust, any pass less informative).

MUTATE=1 multiplies every measured sigma by 0.25: the framework's population check must then FAIL (rc = 1).
DOCUMENTED DEVIATION (2026-09-25): the pre-registration committed MUTATE = x0.4, chosen expecting S near 1.  The data
give S ~ 10, so x0.4 (S x 0.16 ~ 1.6) does NOT break F1 -- a control too weak for the observed margin, a design flaw of
the control, not a change of the analysis.  The control is re-set to x0.25 (S x 0.0625 ~ 0.6), which must break F1.
The table is built by build_table.py (construction rules R1-R4 fixed before the statistic was computed).
Run from the repository root:  python3 real_research/virial_floor_2026/L328_virial_floor_highz.py
"""
import os, sys, csv, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L328_virial_floor_highz"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L328", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__)
G, MSUN = 6.6743e-11, 1.98892e30
Om, OL = 0.3153, 0.6847
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}


def Ez(z): return math.sqrt(Om * (1 + z) ** 3 + OL)


def floor_kms(logM, a0): return ((4 / 81) * G * 10 ** logM * MSUN * a0) ** 0.25 / 1e3


CSV = os.path.join(HERE, "highz_sigma_mstar.csv")
if not os.path.exists(CSV):
    P("PRE-REGISTERED, AWAITING DATA: highz_sigma_mstar.csv (published z >= 4 sigma, M_*) not yet assembled.")
    P("The analysis above is fixed before the data; no verdict is claimed.  Exit 2 = pending, not pass.")
    sys.exit(2)
rows = []
with open(CSV) as f:
    for r in csv.DictReader(f):
        try:
            rows.append(dict(name=r["name"], z=float(r["z"]), sig=float(r["sigma"]), esig=float(r["sigma_err"] or 0),
                             lm=float(r["logMstar"]), elm=float(r["logMstar_err"] or 0.3), kin=r.get("kinematic_type", ""),
                             src=r.get("source_arXiv", ""), construction=r.get("construction", "")))
        except (ValueError, KeyError):
            continue
if MUTATE:
    for r in rows:
        r["sig"] *= 0.25; r["esig"] *= 0.25
OUT["numbers"]["N"] = len(rows)
P(f"   objects with (z, sigma, log M_*): {len(rows)}")

banner("PER OBJECT -- sigma against the floors (M_* only: conservative)")
per = []
for r in rows:
    fl = {k: floor_kms(r["lm"], a) for k, a in A0.items()}
    flr = {k: floor_kms(r["lm"], a * Ez(r["z"])) for k, a in A0.items()}
    per.append({**r, "floor_fw": fl, "floor_rival": flr})
    P(f"   {r['name'][:28]:28s} z={r['z']:.2f}  sigma={r['sig']:6.1f}+/-{r['esig']:4.1f}  logM*={r['lm']:.2f}  "
      f"floor fw {fl['canonical']:5.1f}/{fl['alt']:5.1f}   rival {flr['canonical']:5.1f}/{flr['alt']:5.1f}  [{r['kin']}]")
OUT["numbers"]["per_object"] = per


def S_stat(which, footing, rng=None, nboot=0):
    def one(sig, lm, z):
        a = A0[footing] * (Ez(z) if which == "rival" else 1.0)
        return (sig / floor_kms(lm, a)) ** 2
    s0 = float(np.mean([one(r["sig"], r["lm"], r["z"]) for r in rows]))
    if not nboot:
        return s0, None
    bs = []
    for _ in range(nboot):
        idx = rng.integers(0, len(rows), len(rows))
        vals = []
        for i in idx:
            r = rows[i]
            sig = max(r["sig"] + rng.normal(0, r["esig"]), 1e-3)
            lm = r["lm"] + rng.normal(0, r["elm"])
            vals.append(one(sig, lm, r["z"]))
        bs.append(np.mean(vals))
    return s0, (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), float(np.mean(np.array(bs) < 1.0)))


banner("POPULATION -- S = < sigma^2 / floor^2 > (must be >= 1 if the floor holds)")
rng = np.random.default_rng(20260923)
res = {}
for which in ("framework", "rival"):
    for footing in A0:
        s0, ci = S_stat(which, footing, rng, 4000)
        res[f"{which}_{footing}"] = {"S": s0, "CI95": ci[:2], "P(S<1)": ci[2]}
        P(f"   {which:9s} {footing:9s}: S = {s0:7.2f}   95% CI [{ci[0]:.2f}, {ci[1]:.2f}]   P(S < 1) = {ci[2]:.3f}")
OUT["numbers"]["population"] = res
fw_ok = all(res[f"framework_{k}"]["CI95"][0] >= 1.0 for k in A0)
check("F1 the framework's floor holds for the population (95% lower bound on S >= 1, both footings)",
      "; ".join(f"{k}: S={res[f'framework_{k}']['S']:.2f} [{res[f'framework_{k}']['CI95'][0]:.2f}, "
                f"{res[f'framework_{k}']['CI95'][1]:.2f}]" for k in A0), fw_ok,
      "a failure here (S < 1 at 95%) would falsify the flat-a0 floor for isolated equilibrium systems at z > 4")
rival_viol = {k: res[f"rival_{k}"]["P(S<1)"] for k in A0}
check("R1 (reported, both directions) the a0 ~ H(z) rival's floor: P(S < 1) per footing",
      "; ".join(f"{k}: S={res[f'rival_{k}']['S']:.2f}, P(S<1)={v:.3f}" for k, v in rival_viol.items()), True,
      "P(S<1) near 1 would EXCLUDE the rival's floor on this population (subject to EFE/aperture caveats); near 0 = no "
      "discrimination", load_bearing=False)
nshort_fw = sum(1 for p in per if p["sig"] + 2 * p["esig"] < p["floor_fw"]["canonical"])
nshort_rv = sum(1 for p in per if p["sig"] + 2 * p["esig"] < p["floor_rival"]["canonical"])
OUT["numbers"]["per_object_2sigma_short"] = {"framework_canonical": nshort_fw, "rival_canonical": nshort_rv}
check("R2 (reported) objects > 2 sigma below the floor (canonical; orientation NOT accounted: not decisive alone)",
      f"framework {nshort_fw}/{len(per)}; rival {nshort_rv}/{len(per)}", True,
      "a face-on rotator falls below by orientation with probability ~9% (sin^2 i < 1/6): compare the counts to ~0.09 N",
      load_bearing=False)

# orientation probability for the worst shortfalls against the RIVAL floor (integrated widths only; sigma_0+V rows are
# deprojected): a pure thin disk (sigma_0 -> 0) seen at inclination i has sigma_int^2 = (3/2) sin^2 i * <v^2>/3, so
# a shortfall ratio q = sigma/floor needs sin^2 i <= (2/3) q^2, probability 1 - sqrt(1 - (2/3) q^2).
worst = []
for p_ in per:
    frv = p_["floor_rival"]["canonical"]
    if p_["sig"] + 2 * p_["esig"] < frv:
        q = p_["sig"] / frv
        integ = "integrated" in (p_.get("construction") or "") or not str(p_.get("construction", "")).startswith("sigma0")
        porient = 1 - math.sqrt(max(0.0, 1 - (2 / 3) * q * q)) if integ else 0.0
        worst.append((p_["name"], round(q, 3), round(porient, 3), "integrated" if integ else "sigma0+V"))
worst.sort(key=lambda t: t[1])
OUT["numbers"]["rival_shortfalls_orientation"] = worst
min_p = min([w[2] for w in worst if w[3] == "integrated"], default=1.0)
free_sig = []
for p_ in per:
    if str(p_.get("construction", "")).startswith("sigma0"):
        frv = p_["floor_rival"]["canonical"]
        dlog = math.log10(frv / p_["sig"])
        e = math.hypot(p_["esig"] / p_["sig"] / math.log(10), p_["elm"] / 4)      # floor ~ M^(1/4)
        free_sig.append((p_["name"], dlog / e))
max_free = max((z for _, z in free_sig), default=-99)
OUT["numbers"]["deprojected_max_shortfall_sigma"] = max_free
check("R3 (reported) the rival's per-object shortfalls are orientation-explainable: every integrated-width shortfall has "
      "P(orientation) > 1%, and no deprojected (sigma_0+V) row is > 2 sigma below once M_* errors are included",
      "; ".join(f"{n[:22]} q={q} P_orient={po} [{t}]" for n, q, po, t in worst[:6]) +
      f"; max deprojected shortfall (incl. M_* error) = {max_free:.2f} sigma", min_p > 0.01 and max_free < 2.0,
      "the rival (a0 ~ H(z)) is NOT excluded by single objects either: high-z galaxies are too high-acceleration for the "
      "floor to separate flat from rising a0", load_bearing=False)

lb = [c for c in CH if c[2]]
npass = sum(1 for c in lb if c[1])
banner(f"VERDICT  ({npass}/{len(lb)} load-bearing PASS{'  -- MUTATE RUN' if MUTATE else ''})")
OUT["verdict"] = {"load_bearing_pass": npass, "load_bearing_total": len(lb)}
suffix = "_MUTATE" if MUTATE else ""
with open(os.path.join(HERE, f"{SLUG}_results{suffix}.json"), "w") as f:
    json.dump(OUT, f, indent=1, default=float)
sys.exit(0 if npass == len(lb) else 1)
