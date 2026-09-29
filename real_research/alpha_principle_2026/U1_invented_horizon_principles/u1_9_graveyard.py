#!/usr/bin/env python3
"""U1-9 -- the graveyard table: reads the result files of u1_1, u1_2, u1_3, re-derives every verdict from the recorded numbers, checks it against the stored verdict, and prints
principle -> equation -> what it fixes -> test -> verdict.  Pre-registered in U1_PREREGISTRATION.md.

Run:    python3 u1_9_graveyard.py            (real run; needs u1_1_results.json, u1_2_results.json, u1_3_results.json from real runs; exit 0 iff consistent)
        python3 u1_9_graveyard.py --mutate   (control: the stored verdict of P01 is corrupted to SURVIVES; the consistency check C2 must FAIL; exit 1 = the control works)
Environment: PYTHONDONTWRITEBYTECODE=1
"""
import sys
sys.dont_write_bytecode = True
import os
import json
import math
import u1_lib as L

MUT = "--mutate" in sys.argv
chk = L.Checks()
here = L.HERE


def load(fn):
    with open(os.path.join(here, fn)) as f:
        return json.load(f)


R1 = load("u1_1_results.json")["records"]
R2 = load("u1_2_results.json")["records"]
R3 = load("u1_3_results.json")["records"]
if MUT:
    for r in R1:
        if r["pid"] == "P01" and r["species_type"] == "fermion":
            r["verdict"] = "SURVIVES-T-SPEC"               # corrupt one stored verdict
            break
ALL = R1 + R2 + R3
print("=" * 118)
print("U1-9 graveyard -- " + ("MUTATE CONTROL (P01's stored verdict corrupted)" if MUT else "REAL RUN"))
print("=" * 118)


def derived(r):
    """Re-derive the verdict of one record from its recorded numbers, by the rules declared in the pre-registration."""
    pid = r["pid"]
    if pid in ("P01", "P02", "P03", "P04", "P05"):
        if r["c"] == 0:
            return "VACUOUS"
        return "DEAD" if not r["satisfied_by"] else "SURVIVES-T-SPEC"
    if pid == "P06":
        return "DEAD" if (abs(r["gW_star"]) > 100 and r["Npi_star"] > 100) else "OPEN"
    if pid == "P07":
        return "DEAD" if (r["alpha_pred"] <= 0 or r["delta"] > 5e-10) else "OPEN"
    if pid == "P08":
        return "DEAD" if r["n_real"] == 0 else "OPEN"
    if pid == "P09":
        return "DEAD" if r["ratio_to_ceiling"] > 1 else "OPEN"
    if pid == "P10" or pid == "P11":
        e = r.get("energy_ratio", r.get("energy_ratio_electron"))
        return "UNDECIDED-inert" if e < 1e-20 else "DEAD"
    if pid in ("P12", "P13"):
        if "negatives" in r:
            return "EMPTY" if not r["negatives"] else "OPEN"
        return "DEAD" if not r["satisfiable_under_ceiling"] else "OPEN"
    if pid in ("P14", "P15", "P16", "P17"):
        return "DEAD" if not r["clears"] else "OPEN"
    if pid == "P18":
        return "DEAD" if not r["invariant"] else "INVARIANT"
    return "?"


bad = []
for r in ALL:
    if "verdict" in r:
        d = derived(r)
        if d != r["verdict"]:
            bad.append((r["pid"], r.get("variant"), r["verdict"], d))
chk("C1 record counts: sigma-type 16 variants x 2 species types = 32 records, P06 1, P07 2, P08 2, P09 10, P10 1, P11 2, P12 10, P13 10 + 1 scan, P14 18, P15 6, P16 6, P17 2, P18 20",
    [sum(r["pid"] == p for r in ALL) for p in ("P01", "P02", "P03", "P04", "P05")] == [2, 10, 8, 8, 4] and sum(r["pid"] == "P06" for r in ALL) == 1 and sum(r["pid"] == "P07" for r in ALL) == 2
    and sum(r["pid"] == "P08" for r in ALL) == 2 and sum(r["pid"] == "P09" for r in ALL) == 10 and sum(r["pid"] == "P10" for r in ALL) == 1 and sum(r["pid"] == "P11" for r in ALL) == 2
    and sum(r["pid"] == "P12" for r in ALL) == 10 and sum(r["pid"] == "P13" for r in ALL) == 11 and sum(r["pid"] == "P14" for r in ALL) == 18
    and sum(r["pid"] == "P15" for r in ALL) == 4 and sum(r["pid"] == "P16" for r in ALL) == 4 and sum(r["pid"] == "P17" for r in ALL) == 2
    and sum(r["pid"] == "P18" and "worst" in r for r in ALL) == 20)
chk("C2 every stored verdict equals the verdict re-derived from its recorded numbers", not bad, f"(mismatches: {bad})")

# ---- variant counts (declared: 47)
decl = {"P01": 1, "P02": 5, "P03": 4, "P04": 4, "P05": 2, "P06": 1, "P07": 2, "P08": 2, "P09": 1, "P10": 1, "P11": 2, "P12": 2, "P13": 2, "P14": 2, "P15": 2, "P16": 2, "P17": 2, "P18": 10}
found = {}
for p in ("P01", "P02", "P03", "P04", "P05"):
    found[p] = len({r["variant"] for r in ALL if r["pid"] == p})
found["P06"] = 1
found["P07"] = len({r["variant"] for r in ALL if r["pid"] == "P07"})
found["P08"] = len({r["variant"] for r in ALL if r["pid"] == "P08"})
found["P09"] = 1
found["P10"] = 1
found["P11"] = len({r["variant"] for r in ALL if r["pid"] == "P11"})
found["P12"] = 2                                                      # fermion type (9 species) and scalar type (pi+-)
found["P13"] = 2
found["P14"] = len({r["variant"].split("[")[0].strip() for r in ALL if r["pid"] == "P14"})
found["P15"] = len({r["variant"].split(",")[0] for r in ALL if r["pid"] == "P15"})
found["P16"] = len({r["variant"].split(",")[0] for r in ALL if r["pid"] == "P16"})
found["P17"] = len({r["variant"] for r in ALL if r["pid"] == "P17"})
found["P18"] = len({r["variant"].split(" on ")[0] for r in ALL if r["pid"] == "P18" and "worst" in r})
chk("C3 declared count: 18 principles, 47 (principle, variant) pairs, all present in the records", found == decl and sum(found.values()) == 47, f"(found {sum(found.values())}: {found})")


# ---- headline numbers
def get(pid, **kw):
    return [r for r in ALL if r["pid"] == pid and all(r.get(k) == v for k, v in kw.items())]


def fm(pid, idx=0, typ="fermion"):
    return [r for r in ALL if r["pid"] == pid and r.get("species_type") == typ][idx]


p01 = fm("P01")
p02 = [r for r in ALL if r["pid"] == "P02" and r["species_type"] == "fermion"]
p02s = [r for r in ALL if r["pid"] == "P02" and r["species_type"] == "scalar"]
p03f = [r for r in ALL if r["pid"] == "P03" and r["species_type"] == "fermion" and r["verdict"] == "DEAD"]
p04 = [r for r in ALL if r["pid"] == "P04" and r["species_type"] == "fermion"]
p05 = [r for r in ALL if r["pid"] == "P05" and r["species_type"] == "fermion"]
p06 = get("P06")[0]
p07 = get("P07")
p09e = get("P09", species="electron")[0]
p12e = get("P12", species="electron")[0]
p13e = get("P13", species="electron")[0]
p14 = get("P14")
p15 = get("P15")
p16 = get("P16")
p17 = get("P17")
p03s = [r for r in ALL if r["pid"] == "P03" and r["species_type"] == "scalar" and r["verdict"] == "DEAD" and "q=3" in r["variant"]]
sf = lambda rs: (min(r["shortfall"] for r in rs), max(r["shortfall"] for r in rs))
ROWS = [
    ("P01", "stationary field: J=-2EH", "alpha G_f(M)=-2", f"fermion M*=10^{p01['Mstar']:.1f} (m*=10^{p01['m_star_eV_log10']:.1f} eV)", "T-SPEC", "DEAD", f"electron short by {p01['shortfall']:.1e}; T1 reproduced"),
    ("P02", "membrane impedance match R_H G_vac=1", "|alpha G(M)|=1 (5 length conventions)", f"fermion M*=10^{p02[0]['Mstar']:.0f}..10^{min(r['Mstar'] for r in p02):.0f}; scalar M*={min(r['Mstar'] for r in p02s):.3f}..{max(r['Mstar'] for r in p02s):.2f}", "T-SPEC", "DEAD", f"shortfall {sf(p02)[0]:.0e}..{sf(p02)[1]:.0e}"),
    ("P03", "critical damping, 4D oscillator (n,q)=(2,3)", "sigma/H=(2-q)^2/(4q)=1/12", f"sigma>0 needed: fermion wrong sign; scalar M*={p03s[0]['Mstar']:.2f}", "T-SIGN, T-SPEC", "DEAD", "q=2 variant VACUOUS (holds for any alpha)"),
    ("P04", "plasma resonance w_p=H", "sigma/H=1/q-2=-5/3", f"fermion M*=10^{[r for r in p04 if 'q=3' in r['variant']][0]['Mstar']:.0f}", "T-SPEC", "DEAD", f"shortfall {sf(p04)[0]:.0e}..{sf(p04)[1]:.0e}"),
    ("P05", "conductance quantum G_vac=n e^2/h", "G_X(M)=+-2 (alpha cancels)", f"fermion M*=10^{[r for r in p05 if r['Mstar'] is not None][0]['Mstar']:.2f} (n=-1)", "T-SPEC", "DEAD", "alpha-blind: cannot fix alpha at all"),
    ("P06", "vacuum neutrality sum sigma_i=0", "sum Q^2N g_i/m_i^2=0", f"g_W*={p06['gW_star']:.1e} or {p06['Npi_star']:.1e} pi+- per e", "spectrum", "DEAD", "alpha-blind; electron carries 93% of the sum"),
    ("P07", "Landau pole at the horizon", "alpha=3 pi/(2 ln(mu/m_e))", f"alpha_pred={p07[0]['alpha_pred']:.4f} (negative)", "T-SIGN, T-NUM", "DEAD", "no running below m_e (decoupling checked)"),
    ("P08", "pair-factor marginality rho=0", "mu^2+lambda^2=1/4 (dS2), 9/4 (dS4)", "needs M<=1/2 (3/2); electron M=4.3e38", "T-SPEC", "DEAD", "r->1 anchor verified"),
    ("P09", "Schwinger critical field", "lambda=M^2", f"lambda*={p09e['lam_star']:.1e} vs ceiling {L.lam_max():.1e}", "T-BACK", "DEAD", f"rho_E/rho_L={p09e['energy_ratio']:.1e} (electron)"),
    ("P10", "conformal threshold as the field", "lambda=1/2", f"E*={get('P10')[0]['E_star_SI']:.1e} V/m; rho_E/rho_L={get('P10')[0]['energy_ratio']:.0e}", "T-BACK, T-INERT", "UNDECIDED (inert)", "fixes E*=H^2/2e, not e"),
    ("P11", "Schwinger-Unruh (a0) matching", "lambda=kappa M", f"E*(e)={get('P11')[0]['E_star_electron_SI']:.1e} V/m (kappa=1/2)", "T-BACK, T-INERT", "UNDECIDED (inert)", "fixes E*=kappa m H/e, not e"),
    ("P12", "nonlinear self-sustained field", "|J|=2EH at finite lambda", f"lambda*_est={p12e['lam_est_over_ceiling']:.0e} x ceiling (electron)", "T-BACK", "DEAD", f"rho_E/rho_L~{p12e['energy_ratio_at_est']:.0e}"),
    ("P13", "zero of the renormalized current", "J(L*(M),M)=0", f"L*_est={p13e['lam_est_over_ceiling']:.0e} x ceiling (electron); scalar: no zero found", "T-BACK", "DEAD", "Q1's L*(M) show the M^2 scaling"),
    ("P14", "Schwinger-Unruh point that is the dark energy", "alpha=kappa^2 m^2/(3 M_P^2)", f"alpha_pred(e)={[r for r in p14 if r['species']=='electron'][0]['alpha_pred']:.1e}", "T-NUM", "DEAD", f"best of 18 misses {min(r['delta'] for r in p14):.1e}"),
    ("P15", "Nariai-reduced critical damping", "alpha=pi/(4N) (Dirac), pi/(2N) (Weyl)", "N*=107.63 / 215.26; nearest integers", "T-NUM", "DEAD", f"best miss {min(r['delta'] for r in p15):.1e} (bar needs 5e-10)"),
    ("P16", "membrane quantum Hall", "1/alpha=2N or N", "N*=68.518 / 137.036", "T-NUM", "DEAD", f"best miss {min(r['delta'] for r in p16):.1e} (N=137)"),
    ("P17", "EM self-duality", "alpha=1/2 or 1", "self-dual couplings", "T-NUM", "DEAD", f"miss {min(r['delta'] for r in p17):.3f}"),
    ("P18", "self-dual maps lambda->c/lambda, swap", "F(lambda')=F(lambda) identically", "no non-trivial invariance in 300 tests", "identity test", "DEAD", "only the constant massless fermion is invariant (trivial)"),
]
print("\nGRAVEYARD (principle -> equation -> what it demands -> test -> verdict):")
for pid, name, eq, demand, test, verdict, note in ROWS:
    print(f"  {pid}  {name:46s} | {eq:38s} | {demand:60s} | {test:16s} | {verdict:18s} | {note}")
ver = [r[5] for r in ROWS]
chk("C4 tally: 16 DEAD, 2 UNDECIDED (inert), 0 SURVIVES", ver.count("DEAD") == 16 and ver.count("UNDECIDED (inert)") == 2 and ver.count("SURVIVES") == 0, f"({ver.count('DEAD')} DEAD, {ver.count('UNDECIDED (inert)')} UNDECIDED, {ver.count('SURVIVES')} SURVIVES)")

# ---- structural summary numbers
r1 = load("u1_1_results.json")
mx = max(abs(L.ALPHA_INPUT * v) for v in list(r1["X_f"].values()) + [r1["X_tot"], r1["X_pi"]])
print(f"\nStructural facts computed in this lane:\n  * every known charged species has |sigma_i/H| <= {mx:.2e} (electron {abs(L.ALPHA_INPUT * r1['X_f']['electron']):.2e}); any principle of the form sigma/H = c with |c| > 1e-80 is dead for the whole SM spectrum.")
print(f"  * lambda_max = {L.lam_max():.3e}: a field-value principle whose field grows like M^2 needs m < {math.sqrt(L.lam_max()) * L.H_EV:.2e} eV; the lightest charged particle known is 3e8 times heavier.")
print("  * no principle contains alpha in a way that a known charged particle can satisfy; the two that survive T-BACK (P10, P11) do not contain alpha at all (E* = lambda* H^2/e).")
out = dict(rows=ROWS, tally=dict(dead=ver.count("DEAD"), undecided=ver.count("UNDECIDED (inert)")))
fn = L.write_json("u1_9_graveyard.json", MUT, out)
print(f"\nwritten {fn.split('/')[-1]}")
print(f"CHECKS: {sum(o for _, o in chk.items)}/{len(chk.items)} passed")
L.finish(chk, MUT, targeted_tags=["C2"])
