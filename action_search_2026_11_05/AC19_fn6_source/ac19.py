"""AC19: does v3s or AC2q supply FN6's mass-dependent screening length? Criteria FROZEN_CRITERIA.md (4b010d8f23).
Run from the repository root, one thread:
  OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC19_fn6_source/ac19.py [--mutate]
Outputs ac19.json / ac19.out (main) or ac19_MUTATE.json / ac19_MUTATE.out. Kappa = 1/2 FITTED; not theory closed."""
import json, sys
from pathlib import Path
import sympy as sp

MUTB = "--mutate-b" in sys.argv
MUT = "--mutate" in sys.argv or MUTB
D = Path(__file__).resolve().parent
tag = "_MUTATE_B" if MUTB else "_MUTATE" if MUT else ""
lines = []
def log(s=""):
    print(s); lines.append(s)

# symbols: all positive
M, G, a0, c, r, Ls, rhoX, lam = sp.symbols("M G a0 c r Lstar rho_X lambda", positive=True)
q = sp.Symbol("q")
rM = sp.sqrt(G * M / a0)
pexp = lambda L: sp.simplify(sp.diff(sp.log(L), M) * M)            # d ln L / d ln M

# framework-native rho_DE from a0 = kappa c sqrt(G rho_DE), kappa = 1/2
rho_DE = 4 * a0 ** 2 / (G * c ** 2)
s2 = 2 * rho_DE                                                      # bound s^2 <= 2 rho_DE, at equality

# phantom density D.P around a point mass in the two regimes
rho_ph_deep = sp.sqrt(G * M * a0) / (4 * sp.pi * G * r ** 2)
rho_ph_newt = 2 * a0 / (4 * sp.pi * G * r)

checks = {}
def check(name, ok, got, want):
    checks[name] = dict(ok=bool(ok), got=str(got), want=want)
    log(f"[{'PASS' if ok else 'FAIL'}] {name}: {got} (want {want})")

# ---- known answers
# KA1: AZ41's stiffness-to-source ratio for Fbar = lam d^q/q on p = a rM/r, at q = 2, lam = Lstar^2/2
a = sp.Symbol("a", positive=True)
R_az41 = 2 * lam * (q - 1) * a ** (q - 2) * rM.subs(a0, a) ** (q - 3) * r ** (3 - 2 * q)
R2 = sp.simplify(R_az41.subs({q: 2, lam: Ls ** 2 / 2}))
rc = sp.solve(sp.Eq(R2, 1), r)[0]
check("KA1_crossover", sp.simplify(rc - Ls ** 2 / rM.subs(a0, a)) == 0, rc, "Lstar^2/r_M")
pq = sp.simplify(sp.solve(sp.Eq(sp.diff(sp.log(R_az41.subs(r, sp.Symbol('rr'))), M) * 0, 0), q)) if False else None
# exponent formula: R = 1 -> r^(2q-3) propto rM^(q-3) propto M^((q-3)/2)
p_formula = sp.simplify((q - 3) / 2 / (2 * q - 3))
check("KA1_exponent", sp.simplify(p_formula.subs(q, 2) - pexp(rc)) == 0 and sp.simplify(p_formula - (q - 3) / (4 * q - 6)) == 0,
      f"{p_formula} -> {p_formula.subs(q, 2)}; direct {pexp(rc)}", "(q-3)/(4q-6) = -1/2 at q = 2")
# KA2: AZ41 high-field ratio at q = 2 is radius independent
R_hf = lam * (q - 1) * 2 ** (q - 1) * a ** (q - 2) * r ** (2 - q) / rM.subs(a0, a) ** 2
check("KA2_highfield", sp.diff(R_hf.subs(q, 2), r) == 0, sp.simplify(R_hf.subs({q: 2, lam: Ls ** 2 / 2})), "independent of r")
# KA3: numeric rho_DE
NUM = dict(G=6.67430e-11, c=2.99792458e8)
foot = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
ref = {"canonical": 5.8424e-27, "alt": 8.5328e-27}
ka3 = {f: float(rho_DE.subs({G: NUM["G"], c: NUM["c"], a0: v})) for f, v in foot.items()}
check("KA3_rhoDE", all(abs(ka3[f] / ref[f] - 1) < 1e-3 for f in foot), ka3, "AC6/AC7 values to 1e-3")

# ---- admissible lengths (rows)
PC, KPC, MSUN = 3.0856775814913673e16, 3.0856775814913673e19, 1.98847e30
M_MW = 6e10 * MSUN
Lstar_val = {"canonical": 21.7 * PC, "alt": 22.9 * PC}

rows = []
def add(name, action, L, regime_ok, note):
    rows.append(dict(name=name, action=action, L=L, regime=regime_ok, note=note))

add("Lstar (stiffness length; also D10's embedded scale)", "v3s, AC2q", Ls, None, "fixed constant")
add("r_M: source vs Newtonian balance (g_N = a0)", "v3s, AC2q", rM, None, "MOND radius")
add("stiffness vs source, deep MOND (AZ41 q = 2)", "v3s, AC2q", rc.subs(a, a0), "deep", "needs r >> r_M")
add("GM/c^2", "v3s, AC2q", G * M / c ** 2, None, "horizon scale, not a screen")
add("c^2/a0", "v3s, AC2q", c ** 2 / a0, None, "Hubble scale")
# AC2q charge offset vs phantom density
offset = rhoX if MUT else s2
rX_deep = sp.solve(sp.Eq(rho_ph_deep, offset), r)[0]
rX_newt = sp.solve(sp.Eq(rho_ph_newt, offset), r)[0]
add("AC2q charge offset s^2 vs D.P, deep MOND" if not MUT else ("PLANTED offset rho_X ~ M^-3/8 vs D.P, deep MOND" if MUTB else "PLANTED offset rho_X ~ M^-1/4 vs D.P, deep MOND"),
    "AC2q" if not MUT else "MUTATE", rX_deep, "deep", "needs r >> r_M")
add("AC2q charge offset s^2 vs D.P, Newtonian" if not MUT else ("PLANTED offset rho_X ~ M^-3/8 vs D.P, Newtonian" if MUTB else "PLANTED offset rho_X ~ M^-1/4 vs D.P, Newtonian"),
    "AC2q" if not MUT else "MUTATE", rX_newt, "newt", "needs r << r_M")
no_balance = ["stiffness vs source, Newtonian: ratio independent of r (KA2), no radius",
              "AC2q P-equation offset 2 gamma s^2 grad(phi) vs source grad(phi): ratio 2 gamma s^2 <= 2.2e-10, constant, no radius (AC8)",
              "v3s dust term mu_K: free constant, 0 in galaxies, mass independent"]

# MUTATE: rho_X = A M^(-1/4), normalized so the MW deep-MOND balance radius is 2 kpc on each footing
results, any_pass = [], False
for row in rows:
    out = dict(name=row["name"], action=row["action"], note=row["note"])
    L = row["L"]
    Asym = sp.Symbol("A", positive=True)
    if MUT and "PLANTED" in row["name"]:
        L = L.subs(rhoX, Asym * M ** (sp.Rational(-3, 8) if MUTB else sp.Rational(-1, 4)))
    p = sp.nsimplify(pexp(L))
    out["expression"] = str(L); out["p"] = str(p)
    out["p_in_window"] = bool(sp.Rational(30, 100) <= p <= sp.Rational(45, 100))
    sizes, reg = {}, {}
    for f, a0v in foot.items():
        sub = {G: NUM["G"], c: NUM["c"], a0: a0v, M: M_MW, Ls: Lstar_val[f]}
        Lv = L
        if MUT and "PLANTED" in row["name"]:
            # one normalization per footing: the planted deep-MOND balance radius is 2 kpc for the MW
            if MUTB:   # AMENDMENTS.md (post-result): rho_X ~ M^(-3/8), Newtonian balance radius 2 kpc (propto 1/A)
                Ln = rX_newt.subs(rhoX, Asym * M ** sp.Rational(-3, 8)).subs(sub)
                Aval = float(Ln.subs(Asym, 1)) / (2 * KPC)
            else:
                Ldeep = rX_deep.subs(rhoX, Asym * M ** sp.Rational(-1, 4)).subs(sub)
                Aval = (float(Ldeep.subs(Asym, 1)) / (2 * KPC)) ** 2          # L_deep propto A^(-1/2)
            Lv = L.subs(Asym, Aval)
        val = float(Lv.subs(sub))
        sizes[f] = val / KPC
        rmv = float(rM.subs(sub))
        reg[f] = (val > 3 * rmv) if row["regime"] == "deep" else (val < rmv / 3) if row["regime"] == "newt" else True
    out["MW_kpc"] = sizes; out["regime_consistent"] = reg
    out["size_ok"] = {f: 0.5 <= v <= 9.0 for f, v in sizes.items()}            # within x3 of 1.5-3 kpc
    out["passes"] = out["p_in_window"] and all(reg.values()) and all(out["size_ok"].values())
    any_pass |= out["passes"]
    results.append(out)
    log(f"- {row['name']} [{row['action']}]: L = {L}, p = {p}, MW = "
        + ", ".join(f"{f} {v:.4g} kpc" for f, v in sizes.items())
        + f", regime-consistent {reg}, window {out['p_in_window']}, passes {out['passes']}")
for nb in no_balance:
    log(f"- no balance radius: {nb}")

ka_ok = all(v["ok"] for v in checks.values())
if MUT:
    label = "control bites (planted window length graded PASS)" if any_pass and ka_ok else "control did NOT bite: no verdict"
else:
    label = ("NO VERDICT (known answer failed)" if not ka_ok else
             "PASS" if any_pass else "FAIL (no admissible length of v3s or AC2q in the window)")
log(f"LABEL: {label}")
log("kappa = 1/2 FITTED; not theory closed")
json.dump(dict(mutate=MUT, checks=checks, rows=results, no_balance=no_balance, label=label,
               note="kappa = 1/2 FITTED; not theory closed"), open(D / f"ac19{tag}.json", "w"), indent=1)
(D / f"ac19{tag}.out").write_text("\n".join(lines) + "\n")
sys.exit(0 if (ka_ok and (any_pass if MUT else True)) else 1)
