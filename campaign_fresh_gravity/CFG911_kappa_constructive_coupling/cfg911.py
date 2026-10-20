#!/usr/bin/env python3
"""CFG911 -- kappa constructive lane. HYPOTHESIS BUILDING, not a derivation.

Question (FROZEN_CRITERIA.md, committed alone first): write down the minimal pi-free couplings of a dynamical rho_DE to the
law's saturation scale (a0 = kappa c sqrt(G rho_DE) = kappa sqrt(G eps_DE)) that could give kappa = 1/2 without inserting it,
grade each (SELECTS 1/2 WITH A SECOND PREDICTION / TRADE / IDENTITY / MENU-MISS / EXCLUDED) and compute what ELSE each
predicts.  kappa = 1/2 is FITTED (CFG493); footings never pooled; not theory closed.

Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG911_kappa_constructive_coupling/cfg911.py
    CFG911_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG911_kappa_constructive_coupling/cfg911.py
Reads (read only): fable_independent_2026/L273_desi_a0z_band.py (DESI DR2 w0wa, correlations, Omega_m), the CFG829 results
JSON, and this script's own text (I1).  sympy + numpy, one process, seconds.
"""
import os, re, json, math, sys
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MUT = os.environ.get("CFG911_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = {"lane": "CFG911", "mutate": MUT, "label": "HYPOTHESIS BUILDING (not a derivation)"}
CHECKS = []


def check(name, ok, detail="", expectation_error=None):
    """expectation_error: text explaining why a FROZEN expectation was wrong (the check is kept as frozen and still counts
    as FAIL; such failures are listed and do not set the normal-run exit code, see README)"""
    CHECKS.append({"name": name, "pass": bool(ok), "detail": detail, "expectation_error": None if ok else expectation_error})
    tagx = "PASS" if ok else ("FAIL AS FROZEN (expectation error, disclosed)" if expectation_error else "FAIL")
    print(f"  [{tagx}] {name}" + (f"\n         ({detail})" if detail else "")
          + (f"\n         expectation error: {expectation_error}" if (expectation_error and not ok) else ""), flush=True)


def hdr(t):
    print("\n" + "=" * 110 + f"\n{t}\n" + "=" * 110, flush=True)


# ---------------------------------------------------------------------------------------------------------------------
# symbols.  PI is a tracked stand-in for pi so that pi-weights can be read off exactly.
# ---------------------------------------------------------------------------------------------------------------------
G, c, eps, rho, hbar = sp.symbols("G c epsilon rho hbar", positive=True)
PI = sp.Symbol("PI", positive=True)
xi, s_, n_, Gt, v_ = sp.symbols("xi s n Gtilde v", positive=True)
lam, mu, nu = sp.symbols("lambda_s mu_s nu_s", positive=True)
w = sp.Symbol("w", real=True)
a0s, u, g = sp.symbols("a0 u g", positive=True)
K = 4 * PI * G                                     # the record's K = 4 pi G (CFG723: div P = rho - rho_bar)
HALF2 = sp.Rational(1, 4)                          # kappa^2 for kappa = 1/2 (the comparison target, never a premise)
W_DATA = (0.227, 0.607)                            # rules section 7, rho_DE footing


def S(txt):
    """sympify a stored string with the lane's own symbols (keeps assumptions)"""
    return sp.sympify(txt, locals={"PI": PI, "xi": xi, "Gtilde": Gt, "kappa_law": sp.Symbol("kappa_law", positive=True)})


def to_PI(e):
    return sp.simplify(sp.sympify(e).subs(sp.pi, PI))


def pi_weight(e):
    e = to_PI(e)
    if e == 0:
        return None
    wt = sp.simplify(PI * sp.diff(sp.log(e), PI))
    return wt


def numval(e):
    return float(sp.N(sp.sympify(e).subs(PI, sp.pi)))


# ---------------------------------------------------------------------------------------------------------------------
# parameter sets (normal + the four frozen mutations)
# ---------------------------------------------------------------------------------------------------------------------
BASE = dict(name="base", EIN=8 * PI, w_norm=sp.Integer(-1), d=4, planted=False)
MUTS = [dict(BASE, name="M1 Einstein 8piG -> 4piG", EIN=4 * PI),
        dict(BASE, name="M2 w = -1 -> -0.9", w_norm=sp.Rational(-9, 10)),
        dict(BASE, name="M3 d = 4 -> 5", d=5),
        dict(BASE, name="M4 planted insertion", planted=True)]


def omega_sphere(k):
    """area of the unit k-sphere S^k (real pi)"""
    return 2 * sp.pi ** sp.Rational(k + 1, 2) / sp.gamma(sp.Rational(k + 1, 2))


def hemi_fraction(nsp):
    """one-sided flux of an isotropic bath / (v * energy density) in nsp space dimensions (real pi)"""
    return sp.gamma(sp.Rational(nsp, 2)) / (2 * sp.sqrt(sp.pi) * sp.gamma(sp.Rational(nsp + 1, 2)))


# ---------------------------------------------------------------------------------------------------------------------
# the candidate family N0-N8 (FROZEN_CRITERIA section 4).  Each returns a dict of facts; grading is mechanical (section 5).
# variants: name -> kappa^2 (sympy).  free: list of free constants left in kappa^2 after the construction's own rules.
# ---------------------------------------------------------------------------------------------------------------------
def gfun(name, ww):
    return {"eps": sp.Integer(1), "V": (1 - ww) / 2, "-p": -ww, "X": (1 + ww) / 2, "trace": 1 - 3 * ww,
            "active": -(1 + 3 * ww)}[name]


def candidates(P):
    EIN, wn, d = P["EIN"], P["w_norm"], P["d"]
    C = []
    # N0: premise A as a bimetric horizon coupling ------------------------------------------------------------------
    Ht2 = 2 * EIN * Gt * eps / ((d - 1) * (d - 2) * c ** 2)        # 8 pi G_d convention; d = 4 -> (8 pi/3) Gt eps / c^2
    Rt = c / sp.sqrt(Ht2)
    vars0 = {"Schwarzschild form c^2/(2R~)": c ** 2 / (2 * Rt), "de Sitter form c^2/R~": c ** 2 / Rt}
    k2_0 = {k: sp.simplify(a ** 2 / (G * eps)) for k, a in vars0.items()}
    GtA = sp.solve(sp.Eq(G * (eps / c ** 2) * Rt ** 2, c ** 2), Gt)[0]          # premise A: G rho R~^2 = c^2
    C.append(dict(id="N0", title="premise A as a bimetric horizon coupling (G~ for the a0 sector's metric)",
                  variants=k2_0, free=["Gtilde/G"],
                  at_premiseA={k: sp.simplify(v.subs(Gt, GtA)) for k, v in k2_0.items()},
                  natural={k: sp.simplify(v.subs(Gt, G)) for k, v in k2_0.items()},
                  GtA_over_G=sp.simplify(GtA / G), uses_HA=True, xclass="X7 (Schwarzschild surface gravity at a "
                  "horizon that is not Schwarzschild; k05 H1)", pi_declared=None))
    # N1: multiplier portal on eps (premise A as an action term) -----------------------------------------------------
    C.append(dict(id="N1", title="multiplier portal lambda[a0^2 - xi G eps] (premise A as an action term)",
                  variants={"F = eps": xi * gfun("eps", wn)}, free=["xi"], uses_HA=True, xclass=None, pi_declared=0))
    # N2: the stress-invariant portals --------------------------------------------------------------------------------
    for nm in ("V", "-p", "X", "trace", "active"):
        C.append(dict(id=f"N2[{nm}]", title=f"stress-invariant portal F = {nm}", variants={f"F = {nm}": xi * gfun(nm, wn)},
                      free=["xi"], uses_HA=True, xclass=None, pi_declared=0,
                      unit_xi=sp.simplify(gfun(nm, wn))))
    # N3: G-free tie (dimensional), variants a/b/c handled in section C
    C.append(dict(id="N3", title="G-free tie through c only", variants={}, free=["l* (new length)"], uses_HA=False,
                  xclass=None, pi_declared=None))
    # N4: canonical field-strength portal ------------------------------------------------------------------------------
    C.append(dict(id="N4", title="canonical field-strength portal eps = s F^2, a0 = sqrt(G) F",
                  variants={"s = 1/2 (canonical)": 1 / sp.Rational(1, 2), "s = 1": sp.Integer(1)}, free=[], uses_HA=True,
                  xclass=None, pi_declared=0))
    # N5: trace-share portal ---------------------------------------------------------------------------------------------
    trace_vac = 1 - (d - 1) * wn                                    # |T| / eps for w = wn in d dimensions
    C.append(dict(id="N5", title="trace-share portal a0^2 = G |T| / N_d",
                  variants={"N_d = d^2": sp.simplify(trace_vac / d ** 2), "N_d = d": sp.simplify(trace_vac / d),
                            "N_d = 1": sp.simplify(trace_vac)}, free=[], uses_HA=True,
                  xclass="X4 (where the 4 = d lands is a convention)", pi_declared=0))
    # N6: dynamical portal (kappa as N1); its local/back-reaction numbers are in section E
    C.append(dict(id="N6", title="dynamical quintessence portal a0(phi)^2 = xi G V(phi)", variants={"xi G V": xi}, free=["xi"],
                  uses_HA=True, xclass=None, pi_declared=0))
    # N7: areal horizon (record K433) ------------------------------------------------------------------------------------
    Om = omega_sphere(d - 2)
    k2_7 = sp.simplify(2 * EIN.subs(PI, sp.pi) / ((d - 1) * (d - 2) * Om ** sp.Rational(2, d - 2)))   # n = 1
    C.append(dict(id="N7", title="areal-horizon portal a0 = n c^2/sqrt(A_L) (record K433)", variants={"n = 1": to_PI(k2_7)},
                  free=[], uses_HA=False, xclass=None, pi_declared=0))
    # N8: hemispherical-flux (effusion) portal at v = c ---------------------------------------------------------------
    nsp = d - 1
    f_n = hemi_fraction(nsp)
    Omn = omega_sphere(nsp - 1)                                     # full solid angle in nsp space dims (4 pi at nsp = 3)
    Kd_over_G = Omn                                                 # Gauss-law K_d = Omega G
    C.append(dict(id="N8", title="hemispherical-flux portal (isotropic bath, v = c)",
                  variants={"(a) G Phi1/c [H_A]": to_PI(f_n), "(b) K I/c": to_PI(Kd_over_G / Omn),
                            "(b') K Phi1/(c Omega/2)": to_PI(Kd_over_G * f_n / (Omn / 2)), "(c) K Phi1/c": to_PI(Kd_over_G * f_n)},
                  free=[], uses_HA=True, xclass=None, pi_declared={"(a) G Phi1/c [H_A]": 0, "(b) K I/c": 0,
                                                                     "(b') K Phi1/(c Omega/2)": 0, "(c) K Phi1/c": 1}))
    if P["planted"]:
        # M4: N1 with xi computed from the law's own a0 (circular) and labelled "derived"
        kl = sp.Symbol("kappa_law", positive=True)
        a0_law = kl * sp.sqrt(G * eps)
        C.append(dict(id="N1*", title="PLANTED: multiplier with xi := a0_law^2/(G eps), labelled 'derived'",
                      variants={"xi from the law": sp.simplify(a0_law ** 2 / (G * eps))}, free=[], uses_HA=True, xclass=None,
                      pi_declared=0, follows_law=True))
    return C


# ---------------------------------------------------------------------------------------------------------------------
# A. symbolic kappa^2, free symbols, pi-weights, scaling, rename test (I2, I3, I4, I8)
# ---------------------------------------------------------------------------------------------------------------------
def kappa_out(cand, kappa_law):
    """rename test (I4): TRADE candidates solve their free constant from the law; determinate ones ignore the law."""
    outs = {}
    for k, k2 in cand["variants"].items():
        k2 = sp.sympify(k2)
        if cand.get("follows_law"):
            outs[k] = float(sp.sqrt(k2.subs(sp.Symbol("kappa_law", positive=True), kappa_law)))
        elif xi in k2.free_symbols:
            xsol = sp.solve(sp.Eq(k2, kappa_law ** 2), xi)
            outs[k] = float(sp.sqrt(k2.subs(xi, xsol[0]))) if xsol else None
        elif k2.free_symbols - {PI}:
            outs[k] = None                                       # free constant other than xi (e.g. Gtilde)
        else:
            outs[k] = numval(sp.sqrt(k2))
    return outs


def analyse(P, verbose=True):
    C = candidates(P)
    res = {}
    for cd in C:
        r = {"title": cd["title"], "variants": {}, "free": cd["free"], "uses_HA": cd["uses_HA"], "xclass": cd["xclass"]}
        for k, k2 in cd["variants"].items():
            k2 = sp.sympify(k2)
            fs = sorted(str(x) for x in (k2.free_symbols - {PI}))
            pw = pi_weight(k2) if k2 != 0 else None
            val = numval(sp.sqrt(k2)) if not (k2.free_symbols - {PI}) and k2 != 0 and numval(k2) > 0 else None
            r["variants"][k] = {"kappa2": str(k2), "free_symbols": fs, "pi_weight": None if pw is None else str(pw),
                                "kappa": val}
        for extra in ("at_premiseA", "natural"):
            if extra in cd:
                r[extra] = {k: {"kappa2": str(v), "kappa": numval(sp.sqrt(v)), "pi_weight": str(pi_weight(v))}
                            for k, v in cd[extra].items()}
        if "GtA_over_G" in cd:
            r["GtA_over_G"] = str(cd["GtA_over_G"])
        if "unit_xi" in cd:
            r["unit_xi_kappa2"] = str(cd["unit_xi"])
            r["unit_xi_kappa"] = numval(sp.sqrt(cd["unit_xi"])) if numval(cd["unit_xi"]) > 0 else 0.0
        r["rename_half"] = kappa_out(cd, sp.Rational(1, 2))
        r["rename_two_fifths"] = kappa_out(cd, sp.Rational(2, 5))
        r["pi_declared"] = cd.get("pi_declared")
        r["follows_law"] = bool(cd.get("follows_law"))
        res[cd["id"]] = r
    return C, res


# ---------------------------------------------------------------------------------------------------------------------
# inputs for the second predictions (read only)
# ---------------------------------------------------------------------------------------------------------------------
def read_inputs():
    txt = open(os.path.join(ROOT, "fable_independent_2026", "L273_desi_a0z_band.py")).read()
    DESI = {}
    for m in re.finditer(r'"([A-Za-z0-9+]+)": dict\(w0=(-?[\d.]+), sw0=([\d.]+), wa=(-?[\d.]+), swa=([\d.]+)\)', txt):
        DESI[m.group(1)] = dict(w0=float(m.group(2)), sw0=float(m.group(3)), wa=float(m.group(4)), swa=float(m.group(5)))
    mr = re.search(r"public chains: (-0\.\d+) \(Pantheon\+\),\s+(-0\.\d+) \(Union3\), (-0\.\d+) \(DESY5\)", txt)
    mo = re.search(r"per-combination Omega_m = (0\.\d+) / (0\.\d+) / (0\.\d+)", txt)
    mL = re.search(r"\nOM = (0\.\d+);", txt)
    if mr:
        for k, v in zip(("Pantheon+", "Union3", "DESY5"), mr.groups()):
            DESI[k]["rho"] = float(v)
    if mo:
        for k, v in zip(("Pantheon+", "Union3", "DESY5"), mo.groups()):
            DESI[k]["Om"] = float(v)
    OM_L = float(mL.group(1)) if mL else None
    js = json.load(open(os.path.join(ROOT, "campaign_fresh_gravity", "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829_results.json")))
    A = {"canonical": (js["canonical|nu_e|blue (u-r<2.5)"]["window"]["A"], js["canonical|nu_e|blue (u-r<2.5)"]["window"]["sA"]),
         "alt": (js["alt|nu_e|blue (u-r<2.5)"]["window"]["A"], js["alt|nu_e|blue (u-r<2.5)"]["window"]["sA"])}
    return DESI, OM_L, A


f_DE = lambda z, w0, wa: (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))
w_of = lambda z, w0, wa: w0 + wa * z / (1 + z)
GNUM = {"eps": lambda ww: np.ones_like(np.asarray(ww, float)), "V": lambda ww: (1 - ww) / 2, "-p": lambda ww: -ww,
        "X": lambda ww: (1 + ww) / 2, "trace": lambda ww: 1 - 3 * ww, "active": lambda ww: -(1 + 3 * ww)}
PORTALS = ["eps", "V", "-p", "trace", "active", "X"]


def a0_ratio(portal, z, w0, wa):
    Fz = f_DE(z, w0, wa) * GNUM[portal](w_of(z, w0, wa))
    F0 = GNUM[portal](np.asarray(w0, float))
    with np.errstate(invalid="ignore"):
        r = Fz / F0
        return np.where(r > 0, np.sqrt(np.where(r > 0, r, 1.0)), np.nan)


def main():
    print("CFG911 -- kappa constructive lane: minimal pi-free couplings of a dynamical rho_DE (HYPOTHESIS BUILDING, not a derivation)")
    print(f"mode: {'MUTATE' if MUT else 'normal'}.  kappa = 1/2 FITTED (CFG493); footing rho_DE declared; rho_crit printed separately.")

    # ------------------------------------------------------------------------------------------------------------- K1 (I1)
    hdr("K1 (I1): forbidden constants absent from this script")
    src = open(os.path.abspath(__file__)).read()
    parts = [("9.36", "e-11"), ("9.360", "3e-11"), ("1.13", "e-10"), ("1.131", "2e-10"), ("1.2", "e-10"), ("5.78", "88"),
             ("0.17", "27"), ("0.4", "17"), ("0.4", "5"), ("0.4", "65"), ("0.5", "3"), ("0.5", "5"), ("0.5", "51"), ("1.07", "66e-10")]
    hits = []
    for a, b in parts:
        tok = a + b
        if re.search(r"(?<![\d.])" + re.escape(tok) + r"(?![\d])", src.replace("(\"" + a + "\", \"" + b + "\")", "")):
            hits.append(tok)
    check("K1 no footing a0, measured kappa, Z = 5.79.. or 0.17.. literal appears in the script", not hits, f"hits: {hits}")

    # ------------------------------------------------------------------------------------------------------------- A
    hdr("A. The family N0-N8: kappa^2 per admissible variant (symbolic), free constants, pi-weights, rename test")
    C, R = analyse(BASE)
    for cid, r in R.items():
        print(f"\n  {cid}: {r['title']}   [H_A used: {r['uses_HA']}; X-class: {r['xclass']}]")
        for k, vv in r["variants"].items():
            kap = f"{vv['kappa']:.6f}" if vv["kappa"] is not None else "-"
            print(f"     {k:34s} kappa^2 = {vv['kappa2']:24s} free {vv['free_symbols']}  pi-weight {vv['pi_weight']}  kappa {kap}")
        for extra in ("at_premiseA", "natural"):
            if extra in r:
                for k, vv in r[extra].items():
                    print(f"     [{extra}] {k:30s} kappa^2 = {vv['kappa2']:12s} kappa {vv['kappa']:.6f}  pi-weight {vv['pi_weight']}")
        if "GtA_over_G" in r:
            print(f"     premise A requires Gtilde/G = {r['GtA_over_G']}")
        if "unit_xi_kappa2" in r:
            print(f"     report-only unit-xi value: kappa^2 = {r['unit_xi_kappa2']} -> kappa = {r['unit_xi_kappa']:.4f}")
        print(f"     rename test: kappa_law = 1/2 -> {r['rename_half']};  kappa_law = 2/5 -> {r['rename_two_fifths']}")
    OUT["family"] = R

    # K2 (I2): every kappa^2 printed symbolically -- done above; record that each variant has a symbolic form
    n_var = sum(len(r["variants"]) for r in R.values())
    check("K2 (I2) every admissible variant's kappa^2 is printed symbolically with its free symbols",
          all("kappa2" in vv for r in R.values() for vv in r["variants"].values()) and n_var >= 17, f"{n_var} variants")

    # K3 (I3): scaling G -> lam G, eps -> mu nu^2 eps (rho -> mu rho, c -> nu c): a0 -> nu sqrt(lam mu) a0, kappa invariant
    bad = []
    for cd in C:
        for k, k2 in cd["variants"].items():
            k2 = sp.sympify(k2)
            if k2 == 0:
                continue                                    # F_X at w = -1: a0 = 0 scales trivially
            a0 = sp.sqrt(k2 * G * eps)
            a0s_ = a0.subs({G: lam * G, Gt: lam * Gt, eps: mu * nu ** 2 * eps, c: nu * c}, simultaneous=True)
            ratio = sp.simplify(a0s_ / a0 / (nu * sp.sqrt(lam * mu)))
            if ratio != 1:
                bad.append((cd["id"], k, str(ratio)))
    check("K3 (I3) every variant scales as a0 -> nu sqrt(lam mu) a0 under G -> lam G, rho -> mu rho, c -> nu c (kappa invariant)",
          not bad, f"failures: {bad}")

    # K4 (I4) rename test summary
    follow, stay = [], []
    for cid, r in R.items():
        for k in r["variants"]:
            a, b = r["rename_half"][k], r["rename_two_fifths"][k]
            if a is None or b is None:
                continue
            (follow if abs(a - b) > 1e-12 else stay).append(f"{cid}:{k}")
    trade_follow = all(any(x.startswith(cid) for x in follow) for cid in ("N1", "N2[V]", "N2[-p]", "N2[trace]", "N2[active]", "N6"))
    det_stay = all(any(x.startswith(cid) for x in stay) for cid in ("N4", "N5", "N7", "N8"))
    check("K4 (I4) rename test at kappa_law = 2/5: the xi portals follow the law (consistency relations = TRADE); N4, N5, N7, N8 "
          "do not move (their outputs are their own numbers, so their comparison with 2/5 fails)", trade_follow and det_stay,
          f"follow {len(follow)}, stay {len(stay)}")

    # K8 (I8) pi-weights vs declared classes
    mism = []
    for cid, r in R.items():
        decl = r["pi_declared"]
        if decl is None:
            continue
        for k, vv in r["variants"].items():
            d_ = decl[k] if isinstance(decl, dict) else decl
            if vv["pi_weight"] is None:
                continue
            if sp.sympify(vv["pi_weight"]) != d_:
                mism.append((cid, k, vv["pi_weight"], d_))
    check("K8 (I8) pi-weight of every kappa^2 equals its declared class (0 for the H_A portals, N7 and N8 (a)(b)(b'); 1 for N8 (c))",
          not mism, f"mismatches: {mism}")
    # N0 natural (Gtilde = G) values are H-type, pi-odd; premise-A values pi-free
    r0 = R["N0"]
    check("K8b N0: with Gtilde = G (no premise A) both forms are pi-odd (Einstein's 8pi survives); premise A's Gtilde/G = 3/(8 pi) "
          "makes them pi-free {1/4, 1}",
          all(sp.sympify(v["pi_weight"]) == 1 for v in r0["natural"].values())
          and sorted(round(v["kappa"], 12) for v in r0["at_premiseA"].values()) == [0.5, 1.0]
          and sp.simplify(S(r0["GtA_over_G"]) - 3 / (8 * PI)) == 0,
          f"natural {[round(v['kappa'], 4) for v in r0['natural'].values()]}, premise A {[round(v['kappa'], 4) for v in r0['at_premiseA'].values()]}")

    # K7 (I7): no hbar anywhere in the family's kappa^2
    check("K7 (I7) no hbar in any kappa^2 of the family (N3's hbar variant is handled separately and reported hbar-bearing)",
          all("hbar" not in vv["kappa2"] for r in R.values() for vv in r["variants"].values()))

    # K5 (I5): N0 and N7 hold for every rho (posits through Friedmann, not data selections)
    check("K5 (I5) N0 and N7 kappa^2 are rho-independent identities of their posits (they hold for every rho: posit, not a "
          "data selection; no Friedmann tautology is scored)",
          all("epsilon" not in vv["kappa2"] and "rho" not in vv["kappa2"] for cid in ("N0", "N7") for vv in R[cid]["variants"].values()))

    # ------------------------------------------------------------------------------------------------------------- B
    hdr("B. Record cross-checks (K9-K14)")
    DESI, OM_L, A829 = read_inputs()
    print(f"  DESI DR2 (parsed from L273): {json.dumps(DESI)}")
    print(f"  LambdaCDM Omega_m for E(z) (L273): {OM_L};  CFG829 blue-lens A: {A829}")
    OUT["inputs"] = {"DESI": DESI, "Om_LCDM": OM_L, "CFG829_A_blue": A829}
    ok_parse = (len(DESI) == 3 and all(k in DESI[x] for x in DESI for k in ("w0", "wa", "sw0", "swa", "rho", "Om")) and OM_L is not None)
    check("K0 inputs parsed from the tracked L273 file (three DESI fits with sigmas, the L275 correlations, Omega_m) and CFG829 JSON",
          ok_parse)
    k9 = float(a0_ratio("eps", 2.5, DESI["DESY5"]["w0"], DESI["DESY5"]["wa"]))
    check("K9 the density portal reproduces L273's a0(2.5)/a0(0) = 0.82 (DESY5) within 0.01", abs(k9 - 0.82) < 0.01, f"{k9:.4f}",
          expectation_error="0.82 is PAPER7's rounded point value and equals the Pantheon+ pair (10^-0.085 = 0.822); L273's own "
          "check of 'DESY5 = 0.82' used a 0.03 tolerance and its table prints 0.796 = -0.099 dex for DESY5; K9b tests L273's table")
    l273o = open(os.path.join(ROOT, "fable_independent_2026", "L273_desi_a0z_band.out")).read()
    m25 = re.search(r"\n\s+2\.5\s+\+0\.000\s+(-0\.\d+)\s+(-0\.\d+)\s+(-0\.\d+)\s+\|", l273o)
    mine = [float(np.log10(a0_ratio("eps", 2.5, DESI[k]["w0"], DESI[k]["wa"]))) for k in ("DESY5", "Pantheon+", "Union3")]
    k9b = m25 is not None and all(abs(a - float(b)) < 0.0015 for a, b in zip(mine, m25.groups()))
    check("K9b (added post-freeze) the density portal reproduces L273's printed z = 2.5 row (DESY5, Pantheon+, Union3) within 0.0015 dex",
          k9b, f"L273.out {m25.groups() if m25 else None}; this script {[round(x, 4) for x in mine]}")
    mp = re.search(r"\n\s+2\.5\s+(\+0\.\d+)\s+(\+0\.\d+)\s+(\+0\.\d+)\s+(-0\.\d+)\n", l273o)
    minep = [float(np.log10(a0_ratio("-p", 2.5, DESI[k]["w0"], DESI[k]["wa"]))) for k in ("DESY5", "Pantheon+", "Union3")]
    k9c = mp is not None and all(abs(a - float(b)) < 0.0015 for a, b in zip(minep, mp.groups()[:3]))
    check("K9c (added post-freeze) the pressure portal F = -p reproduces L273 Part 4's stage-17 pressure-law row at z = 2.5 "
          "(DESY5, Pantheon+, Union3) within 0.0015 dex", k9c, f"L273.out {mp.groups()[:3] if mp else None}; this script {[round(x, 4) for x in minep]}")
    check("K10 CFG829 blue-lens amplitudes read from JSON equal the README's 1.016 +/- 0.086 (canonical), 0.928 +/- 0.078 (alt)",
          abs(A829["canonical"][0] - 1.016) < 1e-3 and abs(A829["canonical"][1] - 0.086) < 1e-3
          and abs(A829["alt"][0] - 0.928) < 1e-3 and abs(A829["alt"][1] - 0.078) < 1e-3)
    # K11: N7 at kappa = 1/2 -> a0 sqrt(A)/c^2 = sqrt6/4 (K433's sqrt6/8 on a0/2)
    nsym = sp.Symbol("nn", positive=True)
    k2_7n = nsym ** 2 * to_PI(sp.sympify(R["N7"]["variants"]["n = 1"]["kappa2"]))
    nhalf = sp.solve(sp.Eq(k2_7n, HALF2), nsym)[0]
    check("K11 N7: kappa^2 = 2n^2/3 and kappa = 1/2 needs a0 sqrt(A)/c^2 = n = sqrt6/4 exactly (record K433's sqrt6/8 on a0/2)",
          sp.simplify(k2_7n - 2 * nsym ** 2 / 3) == 0 and sp.simplify(nhalf - sp.sqrt(6) / 4) == 0, f"n(1/2) = {nhalf}")
    # K12: W_rem closed form and the simple law
    a0 = a0s
    Wrem = -(a0 / K) * (u + a0 * sp.log(1 - u / a0)) - u ** 2 / (2 * K)
    k12a = sp.simplify(K * sp.diff(Wrem, u) - u ** 2 / (a0 - u)) == 0
    gN = sp.simplify(u ** 2 / (a0 - u)).subs(u, a0 * g / (a0 + g))
    k12b = sp.simplify(gN - g ** 2 / (g + a0)) == 0
    check("K12 W_rem = -(a0/K)[u + a0 ln(1 - u/a0)] - u^2/2K satisfies K W_rem' = u^2/(a0 - u) (canonical S2) and with "
          "g = a0 u/(a0 - u) gives g_N = g^2/(g + a0)", k12a and k12b)
    # K13: hemisphere fraction
    th = sp.Symbol("theta", positive=True)
    f3_int = sp.simplify(omega_sphere(1) * sp.integrate(sp.cos(th) * sp.sin(th), (th, 0, sp.pi / 2)) / omega_sphere(2))
    f2_int = sp.simplify(2 * sp.integrate(sp.cos(th), (th, 0, sp.pi / 2)) / omega_sphere(1))
    check("K13 one-sided flux fraction: direct integral 1/4 at n = 3 and 1/pi at n = 2, equal to the Gamma-function formula",
          f3_int == sp.Rational(1, 4) and sp.simplify(f2_int - 1 / sp.pi) == 0
          and sp.simplify(hemi_fraction(3) - f3_int) == 0 and sp.simplify(hemi_fraction(2) - f2_int) == 0, f"n=3 {f3_int}, n=2 {f2_int}")
    # K4b: k04 consistency for N4 (four-form instance not re-run)
    Zs, bet, bs = sp.symbols("Z beta b", positive=True)
    k04 = 2 * bet ** 2 / (Zs + 2 * bs * bet ** 2)
    check("K4b N4 is consistent with k04's four-form formula: kappa^2 = 2 beta^2/(Z + 2 b beta^2) = 2 at Z = 1, beta = 1, b = 0 "
          "(= 1/s with s = 1/2); the four-form door itself is p63's (pending, not run here)", k04.subs({Zs: 1, bet: 1, bs: 0}) == 2)

    # ------------------------------------------------------------------------------------------------------------- grading
    def grade_one(cid, r, extra_excl=None):
        labels, notes = [], []
        vals = [vv["kappa"] for vv in r["variants"].values()]
        free = bool(r["free"]) and not (cid == "N4" or cid == "N5" or cid == "N7" or cid == "N8")
        if extra_excl:
            labels.append("EXCLUDED"); notes.append(extra_excl)
        if r["xclass"] and cid in ("N5",):
            labels.append("EXCLUDED"); notes.append(r["xclass"])
        if r["follows_law"]:
            labels.append("IDENTITY"); notes.append("output follows kappa_law (insertion/circular)")
        if free:
            labels.append("TRADE"); notes.append(f"free: {r['free']}")
        det_vals = [v for v in vals if v is not None]
        if not free and not r["follows_law"]:
            if len(set(round(v, 12) for v in det_vals)) > 1:
                labels.append("MENU")
                if any(abs(v - 0.5) < 1e-12 for v in det_vals):
                    notes.append("1/2 is a menu member (spurious under rules section 4)")
            elif len(det_vals) == 1:
                v = det_vals[0]
                if abs(v - 0.5) < 1e-12:
                    labels.append("SELECTS-1/2-CANDIDATE")
                else:
                    labels.append("MISS" if not (W_DATA[0] <= v <= W_DATA[1]) else "CONSISTENT")
        sev = ["EXCLUDED", "TRADE", "IDENTITY", "MENU", "MISS", "CONSISTENT", "SELECTS-1/2-CANDIDATE"]
        gradev = sorted(labels, key=lambda x: sev.index(x))[0] if labels else "UNGRADED"
        half_seen = any(v is not None and abs(v - 0.5) < 1e-12 for v in det_vals) or (
            "at_premiseA" in r and any(abs(vv["kappa"] - 0.5) < 1e-12 for vv in r["at_premiseA"].values()))
        return {"grade": gradev, "labels": labels, "notes": notes, "half_appears": bool(half_seen)}

    # ------------------------------------------------------------------------------------------------------------- C
    hdr("C. N3: the G-free tie (dimensional analysis) and its variants")
    # dimensions [M, L, T]
    dims = {"a0": (0, 1, -2), "eps": (1, -1, -2), "rho": (1, -3, 0), "c": (0, 1, -1), "G": (-1, 3, -2), "hbar": (1, 2, -1)}

    def nullspace(names):
        M = sp.Matrix([[dims[nm][i] for nm in names] for i in range(3)])
        return M.nullspace()
    ns_a = nullspace(["a0", "eps", "c"]); ns_a2 = nullspace(["a0", "rho", "c"])
    ns_b = nullspace(["a0", "eps", "c", "hbar"]); ns_g = nullspace(["a0", "eps", "c", "G"])
    print(f"  {{a0, eps, c}}: {len(ns_a)} groups; {{a0, rho, c}}: {len(ns_a2)}; {{a0, eps, c, hbar}}: {len(ns_b)} "
          f"({[list(v) for v in ns_b]}); {{a0, eps, c, G}}: {len(ns_g)} ({[list(v) for v in ns_g]})")
    check("K15 N3: {a0, eps or rho, c} have no dimensionless group (a G-free tie needs a new dimensional constant: TRADE); "
          "adding hbar gives one group (hbar-bearing, wall 3); adding G gives exactly the law's kappa",
          len(ns_a) == 0 and len(ns_a2) == 0 and len(ns_b) == 1 and len(ns_g) == 1)
    # report-only sizes: the law's unit sqrt(G eps_L) and the hbar variant c^2/l_DE
    Gn, cn, hbn = 6.67430e-11, 2.99792458e8, 1.054571817e-34
    H0 = 67.4e3 / 3.0856775814913673e22
    OmL = 0.685
    rhoL = OmL * 3 * H0 ** 2 / (8 * math.pi * Gn)
    epsL = rhoL * cn ** 2
    unit = math.sqrt(Gn * epsL)
    lDE = (hbn * cn / epsL) ** 0.25
    print(f"  report-only: eps_L = {epsL:.4e} J/m^3, law unit sqrt(G eps_L) = {unit:.4e} m/s^2, l_DE = (hbar c/eps)^(1/4) = "
          f"{lDE:.3e} m, c^2/l_DE = {cn ** 2 / lDE:.3e} m/s^2 = {cn ** 2 / lDE / unit:.2e} x the law's unit")
    # (a) l* from the DE field scale 1/sqrt(V''), exponential potential: V'' = lambda^2 V / phi_P^2
    lam_s = sp.Symbol("lambda_V", positive=True); nn = sp.Symbol("nn", positive=True)
    phiP2_E = c ** 4 / (8 * PI * G); phiP2_G = c ** 4 / G
    k2_E = sp.simplify((nn * c ** 2 * sp.sqrt(lam_s ** 2 * eps / phiP2_E)) ** 2 / (G * eps))
    k2_G = sp.simplify((nn * c ** 2 * sp.sqrt(lam_s ** 2 * eps / phiP2_G)) ** 2 / (G * eps))
    print(f"  (a) a0 = n c^2 sqrt(V''), V = V0 exp(-lambda phi/phi_P): Einstein-normalised phi_P -> kappa^2 = {k2_E} "
          f"(pi-weight {pi_weight(k2_E)}); G-normalised -> kappa^2 = {k2_G} (pi-weight {pi_weight(k2_G)}): slope lambda free")
    # (c) horizon length c/H: H-type
    k2_c = sp.simplify((nn * c * sp.sqrt(8 * PI * G * eps / (3 * c ** 2))) ** 2 / (G * eps))
    print(f"  (c) a0 = n c H_L: kappa^2 = {k2_c} (pi-weight {pi_weight(k2_c)}: odd for any rational n; and real horizons drift with H(z), S8)")
    N3v = {"(a) field-scale l* (Einstein phi_P)": ("TRADE", "lambda_V, n free; pi-odd"),
           "(a') field-scale l* (G phi_P = H_A)": ("TRADE", "lambda_V, n free"),
           "(b) hbar length l_DE": ("EXCLUDED", f"hbar-bearing (wall 3); {cn ** 2 / lDE / unit:.1e} x the law's unit"),
           "(c) horizon c/H": ("EXCLUDED", "H-type, pi-odd (X3), drifts with H(z) (S8)")}
    check("K16 N3 variant (a) is a TRADE in both normalisations (Einstein pi-odd, G-normalised pi-free), (c) is pi-odd",
          pi_weight(k2_E) == 1 and pi_weight(k2_G) == 0 and pi_weight(k2_c) == 1 and lam_s in k2_E.free_symbols)
    OUT["N3"] = {"nullspaces": {"a0,eps,c": len(ns_a), "a0,rho,c": len(ns_a2), "a0,eps,c,hbar": len(ns_b), "a0,eps,c,G": len(ns_g)},
                 "hbar_variant_over_unit": cn ** 2 / lDE / unit, "variants": N3v,
                 "kappa2_a_Einstein": str(k2_E), "kappa2_a_G": str(k2_G), "kappa2_c": str(k2_c)}

    # ------------------------------------------------------------------------------------------------------------- D
    hdr("D. Second predictions of the portals (kappa-free): a0(z)/a0(0) = sqrt(F(z)/F(0)) under the DESI DR2 CPL fits")
    ZS = [0.25, 0.5, 1.06, 1.42, 2.0, 2.5]
    tab = {}
    for nm, dd in DESI.items():
        tab[nm] = {}
        print(f"\n  {nm} (w0 {dd['w0']}, wa {dd['wa']}, Om {dd['Om']}): log10 a0(z)/a0(0) [dex]")
        print("     z     " + " ".join(f"{p:>9s}" for p in PORTALS) + "   rival H(z)/H0")
        for z in ZS:
            row = [float(np.log10(a0_ratio(p, z, dd["w0"], dd["wa"]))) for p in PORTALS]
            Ez = math.sqrt(dd["Om"] * (1 + z) ** 3 + (1 - dd["Om"]) * f_DE(z, dd["w0"], dd["wa"]))
            tab[nm][z] = dict(zip(PORTALS, row)); tab[nm][z]["rival_H"] = math.log10(Ez)
            print(f"   {z:5.2f}  " + " ".join(f"{x:+9.3f}" if np.isfinite(x) else f"{'undef':>9s}" for x in row) + f"   {math.log10(Ez):+9.3f}")
    OUT["a0z_dex"] = {nm: {str(z): v for z, v in t.items()} for nm, t in tab.items()}
    # DESI band for the eps portal and the portal differences (Gaussian, L275 correlations)
    rng = np.random.default_rng(911)
    band = {}
    print("\n  68% DESI band (Gaussian in w0, wa with the L275 correlation), 100k draws: eps portal and (portal - eps) at z = 1.06 and 2.0")
    for nm, dd in DESI.items():
        cov = np.array([[dd["sw0"] ** 2, dd["rho"] * dd["sw0"] * dd["swa"]], [dd["rho"] * dd["sw0"] * dd["swa"], dd["swa"] ** 2]])
        with np.errstate(all="ignore"):                    # spurious BLAS FP flags on this platform (as in L273); checked below
            smp = rng.multivariate_normal([dd["w0"], dd["wa"]], cov, size=100000, method="cholesky")
        assert np.isfinite(smp).all()
        band[nm] = {}
        for z in (1.06, 2.0):
            base_ = np.log10(a0_ratio("eps", z, smp[:, 0], smp[:, 1]))
            ent = {"eps": [float(x) for x in np.nanpercentile(base_, [16, 50, 84])]}
            for p in ("V", "-p", "trace", "active"):
                dif = np.log10(a0_ratio(p, z, smp[:, 0], smp[:, 1])) - base_
                ent[p + "-eps"] = [float(x) for x in np.nanpercentile(dif, [16, 50, 84])]
            band[nm][z] = ent
            print(f"   {nm:10s} z = {z:4.2f}: eps {ent['eps'][1]:+.3f} [{ent['eps'][0]:+.3f}, {ent['eps'][2]:+.3f}]  " +
                  "  ".join(f"{p}-eps {ent[p + '-eps'][1]:+.3f} [{ent[p + '-eps'][0]:+.3f},{ent[p + '-eps'][2]:+.3f}]" for p in ("V", "-p", "trace", "active")))
    OUT["band"] = {nm: {str(z): v for z, v in b.items()} for nm, b in band.items()}

    # running at z = 0: d ln a0 / d ln a = (1/2)[-3(1+w0) + (g'(w0)/g(w0)) (-wa)]
    hdr("D2. The a0-w running law (second prediction, kappa-free): d ln a0/d ln a at z = 0, in units of H0")
    w0s, was = sp.symbols("w0 wa", real=True)
    run_sym, run_num, run_expr = {}, {}, {}
    for p in PORTALS:
        gp = gfun(p, w)
        expr = sp.simplify(sp.Rational(1, 2) * (-3 * (1 + w0s) + (sp.diff(gp, w) / gp).subs(w, w0s) * (-was)))
        run_sym[p] = str(expr); run_expr[p] = expr
        run_num[p] = {nm: float(expr.subs({w0s: dd["w0"], was: dd["wa"]})) for nm, dd in DESI.items()}
        print(f"  {p:7s} d ln a0/d ln a|0 = {str(expr):42s} " + "  ".join(f"{nm} {run_num[p][nm]:+.3f}" for nm in DESI))
    print("  (eps portal: the sign of da0/dt is the sign of -(1 + w): a0 grows today only if the dark energy is phantom.)")
    OUT["running"] = {"symbolic": run_sym, "numbers": run_num}
    check("K17 the density portal's running is -(3/2)(1 + w0) exactly (the a0-w relation); the other portals add a w_a term",
          sp.simplify(run_expr["eps"] + sp.Rational(3, 2) * (1 + w0s)) == 0
          and all(was in run_expr[p].free_symbols for p in ("V", "-p", "trace", "active", "X")))

    # testability of the portal shapes against the record (Jeanneau refit) -- section 6 rule
    EL = lambda z: math.sqrt(OM_L * (1 + z) ** 3 + (1 - OM_L))
    Dj = 0.243 / math.log10(EL(1.06))
    print(f"\n  Jeanneau mapping (approximate): D = 0.243 / log10 E(1.06) = {Dj:.3f}; record Delta_b = +0.140 +/- 0.272 at z = 1.06")
    spread = {}
    jtab = {}
    for nm in DESI:
        vals = {p: tab[nm][1.06][p] for p in ("eps", "V", "-p", "trace", "active")}
        spread[nm] = max(vals.values()) - min(vals.values())
        jtab[nm] = {p: (-Dj * x, (-Dj * x - 0.140) / 0.272) for p, x in vals.items()}
        print(f"   {nm:10s} portal spread at z = 1.06: {spread[nm]:.3f} dex;  Delta_b pred (pull vs record): " +
              "  ".join(f"{p} {jtab[nm][p][0]:+.3f} ({jtab[nm][p][1]:+.2f})" for p in vals))
    testable_now = any(sp_ > 0.272 for sp_ in spread.values())
    sep2 = {nm: max(tab[nm][2.0][p] for p in ("eps", "V", "-p", "trace", "active")) - min(tab[nm][2.0][p] for p in ("eps", "V", "-p", "trace", "active")) for nm in DESI}
    print(f"   portal spread at z = 2.0: {json.dumps({k: round(v, 3) for k, v in sep2.items()})} dex -> a 3 sigma split of the extreme "
          f"portals needs sigma(log a0) <= {min(sep2.values()) / 3:.3f} dex (about {100 * (10 ** (min(sep2.values()) / 3) - 1):.0f}%) at z = 2")
    OUT["portal_testability"] = {"spread_z1.06": spread, "testable_now": testable_now, "spread_z2": sep2, "Jeanneau_D": Dj,
                                 "Jeanneau_pred": jtab}
    check("K18 (section 6) the portal shapes are NOT testable now: their spread at z = 1.06 is below the record's honest band 0.272 dex",
          not testable_now, f"spreads {json.dumps({k: round(v, 3) for k, v in spread.items()})}")

    # ------------------------------------------------------------------------------------------------------------- D3 kinetic
    hdr("D3. The kinetic portal F_X = (eps + p)/2: crossing, thawing variant, KiDS and Jeanneau comparisons")
    zc = {nm: (lambda x: x / (1 - x))(-(1 + dd["w0"]) / dd["wa"]) for nm, dd in DESI.items()}
    print("  CPL crossing w(z_c) = -1 (a0 -> 0 there, undefined beyond): " + "  ".join(f"{k} z_c = {v:.3f}" for k, v in zc.items()))
    kin = {}
    for nm, dd in DESI.items():
        kin[nm] = {}
        for zl in (0.15, 0.25, 0.35, 1.06):
            a = 1 / (1 + zl)
            r = math.sqrt(a ** 3 * math.exp((1 + dd["w0"]) * (1 - a ** 3)))
            Ap = math.sqrt(r)
            kin[nm][zl] = {"a0_ratio": r, "dex": math.log10(r), "A_pred": Ap,
                           "sig_can": (A829["canonical"][0] - Ap) / A829["canonical"][1],
                           "sig_alt": (A829["alt"][0] - Ap) / A829["alt"][1],
                           "Delta_b": -Dj * math.log10(r), "pull_J": (-Dj * math.log10(r) - 0.140) / 0.272}
        print(f"   thawing 1 + w = (1 + w0) a^3, {nm:10s}: " + "  ".join(
            f"z {zl}: a0 x{kin[nm][zl]['a0_ratio']:.3f} ({kin[nm][zl]['dex']:+.3f} dex), A {kin[nm][zl]['A_pred']:.3f} "
            f"[{kin[nm][zl]['sig_can']:+.1f} / {kin[nm][zl]['sig_alt']:+.1f} sigma]" for zl in (0.15, 0.25, 0.35)))
        print(f"      at z = 1.06: a0 {kin[nm][1.06]['dex']:+.3f} dex, Delta_b {kin[nm][1.06]['Delta_b']:+.3f} vs +0.140 +/- 0.272 "
              f"(pull {kin[nm][1.06]['pull_J']:+.2f})")
    kin_excl = all(kin[nm][0.25]["sig_can"] > 3 and kin[nm][0.25]["sig_alt"] > 3 for nm in DESI)
    OUT["kinetic"] = {"z_c": zc, "thawing": {nm: {str(z): v for z, v in d_.items()} for nm, d_ in kin.items()}, "excluded_by_data": kin_excl}
    print(f"  section 6 rule: EXCLUDED iff thawing A at z_l = 0.25 is > 3 sigma below CFG829 on both footings -> {kin_excl}")

    # ------------------------------------------------------------------------------------------------------------- E N6
    hdr("E. N6, the dynamical portal: the a0-charge q = -a0 dW_rem/da0|_u, local variation of a0, EP scale, back-reaction")
    dWda0 = sp.simplify(sp.diff(Wrem, a0))
    q_expr = sp.simplify(-a0 * dWda0)
    q_g = sp.simplify(q_expr.subs(u, a0 * g / (a0 + g)))
    x = sp.Symbol("x", positive=True)
    hq = sp.simplify((q_g * K / a0 ** 2).subs(g, x * a0))            # q = (a0^2/K) h(x), x = g/a0
    ser = sp.series(hq, x, 0, 7).removeO()
    big = sp.limit(hq / x, x, sp.oo)
    print(f"  dW_rem/da0|_u = {dWda0}")
    print(f"  q(g) = (a0^2/K) h(g/a0), h(x) = {sp.simplify(hq)}")
    print(f"  deep (x << 1): h = {sp.expand(ser)}  ->  q ~ g^3/(3 K a0);   Newtonian (x >> 1): h/x -> {big}  ->  q ~ a0 g / K")
    check("K19 the a0-charge has the stated limits: q -> g^3/(3 K a0) (deep) and q -> a0 g/K (Newtonian)",
          sp.simplify(sp.series(hq, x, 0, 4).removeO() - x ** 3 / 3) == 0 and big == 1)
    h_hand = x / (1 + x) + x - 2 * sp.log(1 + x)                 # the same function written stably for numerics
    check("K19b the hand-written stable form x/(1+x) + x - 2 ln(1+x) equals the symbolic h(x)", sp.simplify(sp.expand_log(h_hand - hq, force=True)) == 0)
    ser_f = sp.lambdify(x, ser, "numpy")

    def h_num(xx):
        xx = np.asarray(xx, float)
        small = xx < 1e-2
        out = np.empty_like(xx)
        out[small] = ser_f(xx[small])
        xb = xx[~small]
        out[~small] = xb / (1 + xb) + xb - 2 * np.log1p(xb)
        return out

    trap = getattr(np, "trapezoid", None) or np.trapz
    Kn = 4 * math.pi * Gn
    a0_rep = 0.5 * unit                    # report-only: the law's unit at kappa = 1/2 (FITTED); magnitudes only
    Msun, MEarth = 1.98847e30, 5.9722e24

    def local_dlna0(M, r_obs, r_min):
        rM = math.sqrt(Gn * M / a0_rep)
        rr = np.logspace(math.log10(r_min), math.log10(1e4 * rM), 200001)
        gN = Gn * M / rr ** 2
        gg = 0.5 * (gN + np.sqrt(gN ** 2 + 4 * gN * a0_rep))
        q = (a0_rep ** 2 / Kn) * h_num(gg / a0_rep)
        inner = rr <= r_obs
        I1 = trap(q[inner] * rr[inner] ** 2, rr[inner]) / r_obs
        I2 = trap(q[~inner] * rr[~inner], rr[~inner])
        Q = 4 * math.pi * trap(q * rr ** 2, rr)
        return Gn / (2 * cn ** 4) * 4 * math.pi * (I1 + I2), Q, rM

    loc = {}
    for nm, M, robs, rmin in (("Sun at 1 AU", Msun, 1.495978707e11, 6.957e8), ("MW-like 6e10 Msun at 8 kpc", 6e10 * Msun, 8 * 3.0857e19, 3.0857e18),
                              ("cluster 1e14 Msun at 1 Mpc", 1e14 * Msun, 3.0857e22, 3.0857e19), ("Earth at its surface", MEarth, 6.371e6, 1e5)):
        dl, Q, rM = local_dlna0(M, robs, rmin)
        loc[nm] = {"dln_a0_per_lambda2": dl, "Q_over_a0_M_rM": Q / (a0_rep * M * rM), "r_M_m": rM, "G_M_a0_over_c4": Gn * M * a0_rep / cn ** 4}
        print(f"   {nm:28s} delta ln a0 = {dl:.2e} lambda^2   (G M a0/c^4 = {Gn * M * a0_rep / cn ** 4:.2e}; r_M = {rM:.2e} m; "
              f"int q dV = {Q / (a0_rep * M * rM):.2f} a0 M r_M)")
    # back-reaction: all baryons in 10^10.5 Msun objects (upper-bound style), Omega_b h^2 = 0.02221 (CFG886)
    rho_crit_h2 = 3 * (100e3 / 3.0856775814913673e22) ** 2 / (8 * math.pi * Gn)
    rho_b = 0.02221 * rho_crit_h2
    Mt = 10 ** 10.5 * Msun
    _, Qt, rMt = local_dlna0(Mt, 3.0857e19, 3.0857e17)
    qbar = rho_b * Qt / Mt
    br = qbar / (2 * epsL)
    print(f"   cosmic back-reaction: <q> = rho_b x (int q dV / M) = {qbar:.2e} J/m^3 for all baryons in 10^10.5 Msun objects; "
          f"<q>/(2V) = {br:.1e} of the dark energy's slope\n   (int q dV grows as (1/3) a0 M r_M ln(R_out/r_M) in the deep tail; R_out = 1e4 r_M here, so the "
          f"back-reaction is uncertain by a log factor of order 2-3; the local values converge)")
    fin = all(np.isfinite(v["dln_a0_per_lambda2"]) and v["dln_a0_per_lambda2"] > 0 for v in loc.values()) and np.isfinite(br) and br > 0
    silent = fin and all(abs(v["dln_a0_per_lambda2"]) < 1e-3 for k, v in loc.items() if "Earth" not in k) \
        and abs(loc["Earth at its surface"]["dln_a0_per_lambda2"]) < 1e-15 and abs(br) < 1e-3
    OUT["N6"] = {"dW_da0": str(dWda0), "h_x": str(sp.simplify(hq)), "local": loc, "backreaction_fraction": br, "silent": silent}
    check("K20 (section 6) N6 is SILENT: galaxy/cluster delta ln a0 < 1e-3 lambda^2, Earth < 1e-15 lambda^2, back-reaction < 1e-3",
          silent, f"MW {loc['MW-like 6e10 Msun at 8 kpc']['dln_a0_per_lambda2']:.1e}, cluster {loc['cluster 1e14 Msun at 1 Mpc']['dln_a0_per_lambda2']:.1e}, "
          f"Earth {loc['Earth at its surface']['dln_a0_per_lambda2']:.1e}, back-reaction {br:.1e}")

    # ------------------------------------------------------------------------------------------------------------- F N8
    hdr("F. N8's second prediction: the bath's equation of state against the DESI w0 values")
    w_bath = 1.0 / 3.0
    zs8 = {nm: (w_bath - dd["w0"]) / dd["sw0"] for nm, dd in DESI.items()}
    print("  isotropic bath of quanta at v = c: w = 1/3 (any v: w = v^2/3c^2 >= 0); the Lorentz-invariant vacuum has T^{0i} = 0 in "
          "every frame, so its one-sided flux is 0 and the portal gives a0 = 0")
    print("  (1/3 - w0)/sigma_w0: " + "  ".join(f"{k} {v:.1f}" for k, v in zs8.items()))
    n8_excl = all(v > 5 for v in zs8.values())
    OUT["N8_w"] = {"z_scores": zs8, "excluded": n8_excl}
    check("K21 (section 6) N8's bath needs w = +1/3, more than 5 sigma above w0 for all three DESI fits (EXCLUDED)", n8_excl,
          f"min {min(zs8.values()):.1f} sigma")

    # N0 second prediction: R* = c/sqrt(G rho_L)
    Rstar = cn / math.sqrt(Gn * rhoL)
    RH = cn / H0
    print(f"\n  N0's second prediction: a horizon of the a0 sector's metric at R* = c/sqrt(G rho_L) = {Rstar:.3e} m = {Rstar / 3.0857e25:.2f} Gpc "
          f"(Hubble radius c/H0 = {RH / 3.0857e25:.2f} Gpc); GR has no horizon there (k05 H1)")
    OUT["N0_Rstar_Gpc"] = Rstar / 3.0857e25

    # ------------------------------------------------------------------------------------------------------------- G grading
    hdr("G. Grades (FROZEN_CRITERIA section 5) and the lane outcome (section 7)")
    grades = {}
    for cid, r in R.items():
        extra = None
        if cid == "N8" and n8_excl:
            extra = "second prediction w = +1/3 excluded by DESI w0"
        if cid == "N2[X]" and kin_excl:
            extra = "thawing KiDS amplitude > 3 sigma low on both footings"
        if cid == "N0":
            gr = {"grade": "TRADE", "labels": ["TRADE", "MENU (at premise A)", "X7 posit"],
                  "notes": [f"free Gtilde/G; premise A needs Gtilde/G = {r['GtA_over_G']}; then {{1/2 (Schwarzschild form, X7), 1 (de Sitter form)}}"],
                  "half_appears": True}
        elif cid == "N3":
            gr = {"grade": "TRADE", "labels": ["TRADE (a, a')", "EXCLUDED (b, c)"], "notes": ["candidate grade = least severe surviving "
                  "construction (README disclosure)"] + [f"{k}: {v[0]} ({v[1]})" for k, v in N3v.items()], "half_appears": False}
        else:
            gr = grade_one(cid, r, extra)
        if cid == "N2[X]" and not kin_excl:
            gr["notes"].append(f"sign-limited: a0 = 0 at w = -1; incompatible with the DESI CPL crossing (z_c {', '.join(f'{v:.2f}' for v in zc.values())}) "
                               "if confirmed; thawing variant not excluded by data")
        grades[cid] = gr
        print(f"  {cid:12s} {gr['grade']:24s} labels {gr['labels']}  {'; '.join(gr['notes'])}")
    OUT["grades"] = grades
    selects = [cid for cid, g_ in grades.items() if g_["grade"] == "SELECTS-1/2-CANDIDATE"]
    half_menus = [cid for cid, g_ in grades.items() if g_["half_appears"] and g_["grade"] != "SELECTS-1/2-CANDIDATE"]
    lane = ("CONSTRUCTIVE CANDIDATE" if selects else ("1/2 ONLY IN MENUS OR POSITS" if half_menus else "NO 1/2 AT ALL"))
    OUT["lane_outcome"] = lane
    OUT["half_in_menus_or_posits"] = half_menus
    print(f"\n  SELECTS 1/2 WITH A SECOND PREDICTION: {selects or 'none'}")
    print(f"  1/2 appears only as a menu member or through a posit in: {half_menus}")
    print(f"  LANE OUTCOME: {lane}")

    # K14: classifier controls
    planted = {
        "P-select": {"title": "planted determinate 1/2", "variants": {"v": {"kappa": 0.5}}, "free": [], "xclass": None, "follows_law": False},
        "P-trade": {"title": "planted xi row", "variants": {"v": {"kappa": None}}, "free": ["xi"], "xclass": None, "follows_law": False},
        "P-menu": {"title": "planted menu with 1/2", "variants": {"a": {"kappa": 0.5}, "b": {"kappa": 1.0}}, "free": [], "xclass": None,
                   "follows_law": False}}
    pg = {k: grade_one(k, v)["grade"] for k, v in planted.items()}
    check("K14 classifier controls: planted determinate 1/2 -> SELECTS-1/2-CANDIDATE, planted xi row -> TRADE, planted menu -> MENU",
          pg == {"P-select": "SELECTS-1/2-CANDIDATE", "P-trade": "TRADE", "P-menu": "MENU"}, json.dumps(pg))

    # rho_crit readings (I6): determinate values only
    rc = {}
    for cid in ("N4", "N5", "N7", "N8"):
        rc[cid] = {k: (vv["kappa"] * math.sqrt(OmL) if vv["kappa"] else None) for k, vv in R[cid]["variants"].items()}
    print(f"\n  K6 (I6) rho_crit readings kappa_crit = kappa sqrt(Omega_L) (report only, never pooled): "
          + "; ".join(f"{cid} " + ", ".join(f"{v:.3f}" for v in d_.values() if v) for cid, d_ in rc.items()))
    OUT["rho_crit_readings"] = rc
    check("K6 (I6) rho_crit readings printed separately for every determinate value", all(rc[c_] for c_ in rc))

    # ------------------------------------------------------------------------------------------------------------- H MUTATE
    bites = {}
    if MUT:
        hdr("H. MUTATE: the four frozen controls (each must bite; exit 1 if all bite, 3 if any does not)")
        for P in MUTS:
            _, RM = analyse(P, verbose=False)
            if P["name"].startswith("M1"):
                k7b, k7m = R["N7"]["variants"]["n = 1"]["kappa2"], RM["N7"]["variants"]["n = 1"]["kappa2"]
                n0b = [v["kappa2"] for v in R["N0"]["natural"].values()]; n0m = [v["kappa2"] for v in RM["N0"]["natural"].values()]
                gbare_same = all(R[cid]["variants"] == RM[cid]["variants"] for cid in ("N1", "N2[V]", "N2[-p]", "N4", "N5", "N8"))
                ok = (sp.sympify(k7b) == sp.Rational(2, 3) and sp.sympify(k7m) == sp.Rational(1, 3) and n0b != n0m and gbare_same)
                bites[P["name"]] = {"bites": ok, "N7": [k7b, k7m], "N0_natural": [n0b, n0m], "G_bare_unchanged": gbare_same}
            elif P["name"].startswith("M2"):
                mb = {cid: R[cid]["unit_xi_kappa2"] for cid in R if "unit_xi_kappa2" in R[cid]}
                mm = {cid: RM[cid]["unit_xi_kappa2"] for cid in RM if "unit_xi_kappa2" in RM[cid]}
                n5b, n5m = R["N5"]["variants"]["N_d = d^2"]["kappa2"], RM["N5"]["variants"]["N_d = d^2"]["kappa2"]
                n8same = R["N8"]["variants"] == RM["N8"]["variants"]
                ok = (mb != mm and sp.sympify(n5m) == sp.Rational(37, 160) and n8same
                      and [sp.sympify(mm[k]) for k in ("N2[V]", "N2[-p]", "N2[X]", "N2[trace]", "N2[active]")]
                      == [sp.Rational(19, 20), sp.Rational(9, 10), sp.Rational(1, 20), sp.Rational(37, 10), sp.Rational(17, 10)])
                bites[P["name"]] = {"bites": ok, "unit_xi": [mb, mm], "N5": [n5b, n5m], "N8_unchanged": n8same}
            elif P["name"].startswith("M3"):
                n5m = RM["N5"]["variants"]["N_d = d^2"]["kappa2"]
                p7 = RM["N7"]["variants"]["n = 1"]["pi_weight"]; p8 = RM["N8"]["variants"]["(a) G Phi1/c [H_A]"]["pi_weight"]
                k8 = RM["N8"]["variants"]["(a) G Phi1/c [H_A]"]["kappa2"]
                n4same = R["N4"]["variants"] == RM["N4"]["variants"]
                ok = (sp.sympify(n5m) == sp.Rational(1, 5) and sp.sympify(p7) == sp.Rational(-1, 3) and sp.sympify(p8) == -1
                      and sp.simplify(S(k8) - 2 / (3 * PI)) == 0 and n4same)
                bites[P["name"]] = {"bites": ok, "N5": n5m, "N7_pi_weight": p7, "N8a": [k8, p8], "N4_unchanged": n4same}
            elif P["name"].startswith("M4"):
                rm = RM["N1*"]
                gm = grade_one("N1*", rm)["grade"]
                ok = (gm == "IDENTITY" and abs(rm["rename_two_fifths"]["xi from the law"] - 0.4) < 1e-12)
                bites[P["name"]] = {"bites": ok, "grade": gm, "rename": [rm["rename_half"], rm["rename_two_fifths"]]}
            print(f"  {P['name']:28s} bites: {bites[P['name']]['bites']}   {json.dumps({k: v for k, v in bites[P['name']].items() if k != 'bites'}, default=str)[:300]}")
        OUT["mutate_controls"] = bites

    # ------------------------------------------------------------------------------------------------------------- finish
    npass = sum(ch["pass"] for ch in CHECKS)
    OUT["checks"] = CHECKS
    OUT["n_checks"] = [npass, len(CHECKS)]
    print(f"\nchecks: {npass}/{len(CHECKS)} PASS")
    with open(os.path.join(HERE, f"cfg911_results{TAG}.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("kappa = 1/2 FITTED; HYPOTHESIS BUILDING (not a derivation); footings never pooled; not theory closed.")
    if MUT:
        allb = all(b["bites"] for b in bites.values())
        print(f"MUTATE: {'all controls bite -> exit 1 (by design)' if allb else 'a control did NOT bite -> exit 3'}")
        sys.exit(1 if allb else 3)
    fails = [ch for ch in CHECKS if not ch["pass"]]
    undisclosed = [ch["name"] for ch in fails if not ch["expectation_error"]]
    print(f"failures: {len(fails)} ({len(fails) - len(undisclosed)} disclosed frozen-expectation errors; undisclosed: {undisclosed or 'none'})")
    sys.exit(0 if not undisclosed else 2)


if __name__ == "__main__":
    main()
