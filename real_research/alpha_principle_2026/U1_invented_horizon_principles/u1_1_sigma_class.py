#!/usr/bin/env python3
"""U1-1 -- linear-response (sigma-type) invented principles P01-P07, tested against the known charged spectrum.
Pre-registered in U1_PREREGISTRATION.md (written before this script was run; see its Amendment 1).

Equation for every sigma-type variant:  alpha * Q^2 N_c * G_X(M) = c   (X = Dirac fermion or complex scalar; P05: G_X(M) = 2n, alpha cancels).

Run:    python3 u1_1_sigma_class.py            (real run; exit 0 iff every check passes)
        python3 u1_1_sigma_class.py --mutate   (control: P01's requirement is flipped to sigma = +2H as in T1; check B1 must FAIL; exit 1 = the control works)
Environment: PYTHONDONTWRITEBYTECODE=1
"""
import sys
sys.dont_write_bytecode = True
import math
import mpmath as mp
import u1_lib as L

MUT = "--mutate" in sys.argv
chk = L.Checks()
PI = math.pi
A = L.ALPHA_INPUT
print("=" * 118)
print("U1-1 sigma-type principles P01-P07 -- " + ("MUTATE CONTROL (P01 requirement flipped to +2)" if MUT else "REAL RUN"))
print("=" * 118)

# --------------------------------------------------------------------------- known spectrum
FERM = [(nm, mev, w, L.Mof(mev)) for nm, mev, w in L.species_fermions()]
M_PI = L.Mof(L.M_PION_MEV)
M_W = L.Mof(L.M_W_MEV)
X_f = {nm: w * float(L.Gf(Mv)) for nm, mev, w, Mv in FERM}       # Q^2 N_c G_f(M): sigma_i/H = alpha X_i
X_tot = sum(X_f.values())
X_pi = L.Gs(M_PI)                                                # pi^+- as a point complex scalar (EFT sense; flagged)
print(f"\nKnown spectrum with H = H_Lambda = {L.H_EV:.4e} eV:  M_e = {FERM[0][3]:.4e},  M_pi = {M_PI:.3e},  M_W = {M_W:.3e},  M_t = {FERM[-1][3]:.3e}")
print("  sigma_i/H = alpha Q^2 N_c G_f(M_i):")
for nm, mev, w, Mv in FERM:
    print(f"    {nm:9s} M = {Mv:10.4e}   alpha Q2N G_f = {A * X_f[nm]:+.4e}")
print(f"    total fermions:      alpha sum = {A * X_tot:+.4e}      pi^+- (scalar, heavy form): alpha G_s = {A * X_pi:+.4e}")
max_abs = max(abs(A * v) for v in list(X_f.values()) + [X_tot, X_pi])
chk("E1 (pre-registered expectation) every known species and the fermion total have |sigma/H| < 1e-70", max_abs < 1e-70, f"(max |sigma_i/H| = {max_abs:.3e})")

# --------------------------------------------------------------------------- variants
TWO_PI = 2 * PI
FOUR_PI = 4 * PI
V = []
V.append(dict(pid="P01", var="sigma/H = -2 (stationary field, T1)", kind="sigma", targets={"fermion": (2.0 if MUT else -2.0), "scalar": (2.0 if MUT else -2.0)}))
for cv, lab in [(1.0, "1"), (TWO_PI, "2 pi"), (1 / TWO_PI, "1/(2 pi)"), (FOUR_PI, "4 pi"), (1 / FOUR_PI, "1/(4 pi)")]:
    V.append(dict(pid="P02", var=f"|sigma/H| = {lab}", kind="sigma", targets={"fermion": -cv, "scalar": +cv}))
for qq in (1, 2, 3, 4):
    V.append(dict(pid="P03", var=f"q={qq}: sigma/H = (2-q)^2/(4q) = {(2 - qq) ** 2 / (4 * qq):.4g}", kind="sigma", targets={"fermion": (2 - qq) ** 2 / (4 * qq), "scalar": (2 - qq) ** 2 / (4 * qq)}, q=qq))
for qq in (1, 2, 3, 4):
    V.append(dict(pid="P04", var=f"q={qq}: sigma/H = 1/q - 2 = {1 / qq - 2:.4g}", kind="sigma", targets={"fermion": 1 / qq - 2, "scalar": 1 / qq - 2}, q=qq))
for nn in (+1, -1):
    V.append(dict(pid="P05", var=f"n={nn:+d}: G_X(M) = {2 * nn} (alpha-blind)", kind="G", targets={"fermion": 2.0 * nn, "scalar": 2.0 * nn}))
chk("C0 declared variant count: P01 1, P02 5, P03 4, P04 4, P05 2 = 16", len(V) == 16, f"({len(V)})")

REC = []
n_eval = 0
print("\nsigma-type variants (target t for X = Q^2 N_c G_X:  t = c/alpha; P05: t = G directly).  Columns: M* (mass in horizon units that solves it), m* in eV, electron ratio X_e/t, best shortfall factor, verdict")
for v in V:
    for typ in ("fermion", "scalar"):
        c = v["targets"][typ]
        t = c if v["kind"] == "G" else c / A
        rec = dict(pid=v["pid"], variant=v["var"], species_type=typ, c=c, t=t)
        # ---- solve for the mass that satisfies it (inverse map, not a test)
        if typ == "fermion":
            if t < 0:
                lnM = L.Gf_small_lnM(t)
                with mp.workdps(60):                                   # Amendment 2: refine the small-M identity with the exact G_f (O(M^2) correction matters only when M* ~ 1e-2)
                    lnM = mp.findroot(lambda x: L.Gf(mp.exp(x)) - t, lnM)
                Mstar = mp.exp(lnM)
                resid = abs(L.Gf(Mstar) / t - 1)
                rec.update(Mstar=float(mp.log10(Mstar)), Mstar_is_log10=True, resid=float(resid), note="small-M identity + exact G_f residual")
                m_eV = float(mp.log10(Mstar)) + math.log10(L.H_EV)
                rec["m_star_eV_log10"] = m_eV
                ok_res = resid < 1e-6
                sol = f"M* = 10^{float(mp.log10(Mstar)):.3f}, m* = 10^{m_eV:.2f} eV"
            elif t == 0:
                rec.update(Mstar=None, note="c = 0: satisfied by any heavy fermion to 1e-81 (vacuous); no mass is selected")
                ok_res, sol = True, "no mass selected (c = 0)"
            else:
                rec.update(Mstar=None, note="no solution: G_f < 0 at every M (T-SIGN)")
                ok_res, sol = True, "NO SOLUTION (G_f<0, wrong sign)"
            X_list = [(nm, X_f[nm]) for nm, *_ in FERM] + [("total", X_tot)]
        else:
            if t > 0:
                Ms, note = L.solve_Gs(t)
                rec.update(Mstar=Ms, note=note)
                ok_res = Ms is not None
                sol = (f"M* = {Ms:.4g}, m* = {Ms * L.H_EV:.3e} eV" if Ms else "no solution")
            elif t == 0:
                rec.update(Mstar=None, note="c = 0 (vacuous)")
                ok_res, sol = True, "no mass selected (c = 0)"
            else:
                rec.update(Mstar=None, note="no solution: G_s > 0 at every M (T-SIGN)")
                ok_res, sol = True, "NO SOLUTION (G_s>0, wrong sign)"
            X_list = [("pi+-", X_pi)]
        # ---- T-SPEC / T-SIGN on the known species
        sat = []
        best = None
        for nm, X in X_list:
            n_eval += 1
            if t == 0:
                sat_i = None
            else:
                ratio = X / t
                sat_i = (X * t > 0) and (0.5 <= abs(ratio) <= 2.0)
                if best is None or abs(ratio) > abs(best[1]):
                    best = (nm, ratio)
            sat.append((nm, sat_i))
        vacuous = (t == 0) and max(abs(A * X) for _, X in X_list) < 1e-30
        if t == 0:
            verdict = "VACUOUS" if vacuous else "DEAD"
            short = None
        else:
            satisfied = any(s for _, s in sat if s)
            verdict = "SURVIVES-T-SPEC" if satisfied else "DEAD"
            short = abs(t) / max(abs(X) for _, X in X_list)
            wrong_sign = all((X * t) < 0 for _, X in X_list)
            rec["wrong_sign_for_all_known"] = wrong_sign
        rec.update(verdict=verdict, shortfall=short, best=best, satisfied_by=[nm for nm, s in sat if s])
        REC.append(rec)
        if typ == "fermion" or True:
            print(f"  {v['pid']} {v['var'][:44]:44s} {typ:8s} {sol:46s} " + (f"electron/target ratio = {best[1]:+.2e}; shortfall {short:.2e}" if best else "c = 0") + f"  -> {verdict}")
chk("C1 n_evaluations: 16 variants x (9 fermions + total + pi) counted per species type = 16 x (10 + 1)", n_eval == 16 * 11, f"({n_eval})")

# --------------------------------------------------------------------------- B: the solved masses really solve their equations
p01f = [r for r in REC if r["pid"] == "P01" and r["species_type"] == "fermion"][0]
chk("B1 P01 (T1 reproduced): the fermion mass M* with alpha G_f(M*) = -2 exists and solves it (residual < 1e-6)",
    p01f.get("Mstar") is not None and p01f["resid"] < 1e-6, f"(M* = 10^{p01f.get('Mstar')}; T1: 2.337e-281 -> log10 = -280.63)")
if not MUT:
    chk("B2 P01 M* agrees with T1's 2.33714e-281 (M* is H-independent)", abs(p01f["Mstar"] - math.log10(2.33714e-281)) < 1e-3, f"(log10 M* = {p01f['Mstar']:.4f} vs {math.log10(2.33714e-281):.4f})")
    ferm_solved = [r for r in REC if r["species_type"] == "fermion" and r.get("Mstar") is not None]
    chk("B3 every solvable fermion M* satisfies its equation to 1e-6 with the exact G_f (250 digits)", all(r["resid"] < 1e-6 for r in ferm_solved), f"({len(ferm_solved)} solved)")
    # scalar solutions re-evaluated
    bad = 0
    for r in REC:
        if r["species_type"] == "scalar" and r.get("Mstar") and r["note"] == "bisection":
            if abs(L.Gs(r["Mstar"]) / r["t"] - 1) > 1e-6:
                bad += 1
    chk("B4 every scalar M* from the bisection reproduces its target G_s to 1e-6", bad == 0)

# --------------------------------------------------------------------------- E: pre-registered expectations
nonvac = [r for r in REC if r["verdict"] != "VACUOUS"]
chk("E2 every non-vacuous (variant, species type) is DEAD on the known spectrum", all(r["verdict"] == "DEAD" for r in nonvac), f"({sum(r['verdict'] == 'DEAD' for r in nonvac)}/{len(nonvac)} DEAD)")
chk("E3 the only VACUOUS entries are the q=2 variant of P03 (c = 0), for both species types", [ (r['pid'], r['variant'][:4], r['species_type']) for r in REC if r['verdict'] == 'VACUOUS'] ==
    [("P03", "q=2:", "fermion"), ("P03", "q=2:", "scalar")], f"({[(r['pid'], r['variant'][:4], r['species_type']) for r in REC if r['verdict'] == 'VACUOUS']})")
fer = [r for r in nonvac if r["species_type"] == "fermion"]
chk("E4 largest shortfall factor over the fermion entries is > 1e70 and the smallest is > 1e70 too (every c is O(1) or c/alpha O(1)-O(1e3))",
    min(r["shortfall"] for r in fer) > 1e70, f"(min {min(r['shortfall'] for r in fer):.3e}, max {max(r['shortfall'] for r in fer):.3e})")
sc = [r for r in nonvac if r["species_type"] == "scalar"]
chk("E5 the same for the pi^+- scalar entries (shortfall > 1e70)", min(r["shortfall"] for r in sc) > 1e70, f"(min {min(r['shortfall'] for r in sc):.3e})")
# sign kills: fermion entries needing sigma > 0
pos = [r for r in fer if r["c"] > 0]
chk("E6 every fermion entry with c > 0 (P02 sign +, P03, P05 n=+1) is killed by T-SIGN alone (the fermion sigma is negative)",
    all(r.get("wrong_sign_for_all_known") for r in pos) and len(pos) >= 1, f"({len(pos)} entries)")

# --------------------------------------------------------------------------- P03 scan over q, and P04 scan
print("\nP03 scan: (n-q)^2/(4q) for q in [1e-3, 1e3]:  the fermion sigma is negative, the required value is >= 0 for every q>0")
qs = [10 ** (-3 + 6 * i / 600) for i in range(601)] + [2.0]
c_of_q = lambda qq: (2 - qq) ** 2 / (4 * qq)
Se = A * X_f["electron"]
min_c = min(c_of_q(qq) for qq in qs)
chk("S1 P03: (2-q)^2/(4q) >= 0 for all scanned q, so a fermion (sigma < 0) can never be critically damped, at any q > 0", min_c >= 0 and Se < 0, f"(min over scan {min_c:.3g}; sigma_e/H = {Se:.3e})")
Spi = A * X_pi
dq = math.sqrt(8 * Spi)
print(f"    scalar pi^+-: sigma/H = {Spi:.3e}; c(q) = (q-2)^2/(4q) ~ (q-2)^2/8 near q = 2 equals it only for |q-2| ~ {dq:.2e} (a vacuous window: q must equal 2 to 40 digits)")
chk("S2 P03: the pi^+- can be critically damped only inside |q - 2| < 1e-30 (window width sqrt(8 sigma/H))", dq < 1e-30, f"(window {dq:.2e})")
res_min = min(abs(1 / qq - 2) for qq in qs)
print(f"    P04: resonance sigma/H = 1/q - 2 is zero only at q = 1/2 (scanned min |1/q - 2| = {res_min:.3g}); for the fermion sigma_e/H = {Se:.3e} it is met only within |q - 1/2| ~ {abs(Se) / 4:.2e}")

# --------------------------------------------------------------------------- P06 vacuum neutrality (heavy-limit sum rule)
print("\nP06 vacuum neutrality: sum_i sigma_i = 0 in the heavy limit sigma_i/H = alpha Q^2 N g_i / M_i^2 (alpha factors out)")
gf, gs = -1.0 / (9 * PI), 7.0 / (18 * PI)
T_f = gf * sum(w / mev ** 2 for _, mev, w, _ in FERM)          # MeV^-2
T_pi = gs / L.M_PION_MEV ** 2
T_W1 = 1.0 / L.M_W_MEV ** 2                                     # g_W = 1
gW_star = -(T_f + T_pi) / T_W1
Npi_star = abs(T_f) / T_pi
share = {nm: gf * w / mev ** 2 / T_f for nm, mev, w, _ in FERM}
print(f"    T_f = {T_f:.4e} MeV^-2 (electron share {share['electron']:.4f}); T_pi = {T_pi:.4e}; T_W(g_W=1) = {T_W1:.4e}")
print(f"    cancellation needs g_W* = {gW_star:.4e} (record's largest heavy |g| is 0.124), or N_pi* = {Npi_star:.4e} pi^+--like scalars per electron")
p06_dead = abs(gW_star) > 100 and Npi_star > 100
chk("P06 T-SPEC-type test: needs |g_W| > 100 AND more than 100 pi^+--like scalars (either route unreachable) -> DEAD (reading of the pre-registered 'or': the principle needs ONE route, so it is DEAD iff both are unreachable)", p06_dead)
REC.append(dict(pid="P06", variant="sum_i sigma_i = 0", species_type="spectrum", verdict="DEAD" if p06_dead else "OPEN", gW_star=gW_star, Npi_star=Npi_star, electron_share=share["electron"]))

# --------------------------------------------------------------------------- P07 Landau pole at the horizon
print("\nP07 Landau pole at the horizon: 1/alpha_eff(mu) = 1/alpha - (2/(3 pi)) ln(mu/m) = 0  ->  alpha = 3 pi/(2 ln(mu/m))")
me_eV = 0.51099895e6
runs = []
for lab, mu_eV in [("mu = H", L.H_EV), ("mu = H/(2 pi) (Gibbons-Hawking T)", L.H_EV / (2 * PI))]:
    lnr = math.log(mu_eV / me_eV)
    a_pred = 3 * PI / (2 * lnr)
    inv = 1 / a_pred
    delta = abs(abs(inv) / L.INV_ALPHA - 1)
    bar = L.bar_assess(delta, math.log2(2))
    print(f"    {lab:36s} ln(mu/m_e) = {lnr:+.4f}  alpha_pred = {a_pred:+.5f} (1/alpha_pred = {inv:+.3f});  |1/alpha| miss = {delta:.3f};  bar clears: {bar['clears']}")
    runs.append(dict(var=lab, ln=lnr, alpha_pred=a_pred, inv=inv, delta=delta, clears=bool(bar["clears"])))
    REC.append(dict(pid="P07", variant=lab, species_type="fermion", verdict="DEAD" if (a_pred <= 0 or not bar["clears"]) else "OPEN", alpha_pred=a_pred, inv_alpha_pred=inv, delta=delta))
chk("E7 P07: alpha_pred < 0 for both scale choices (H < m_e so ln(mu/m) < 0), and the bar is not cleared", all(r["ln"] < 0 and not r["clears"] for r in runs))
mp.mp.dps = 250
Me_mp = mp.mpf(FERM[0][3])
run_term = mp.log(Me_mp) - mp.re(mp.digamma(1j * Me_mp))
print(f"    decoupling: ln M_e = {float(mp.log(Me_mp)):.4f} but ln M_e - Re psi(iM_e) = {mp.nstr(run_term, 6)} (= -1/(12 M_e^2) = {mp.nstr(-1 / (12 * Me_mp ** 2), 6)}): below m_e the coupling does not run.")
chk("E8 P07 structural: the running log is cancelled to 1e-70 at M_e (no running below the lightest charged mass, so 1/alpha(H) = 1/alpha(0) is finite for every alpha)", abs(run_term) < mp.mpf("1e-70"))

# --------------------------------------------------------------------------- summary lines
print("\nWhat each sigma-type principle demands of the spectrum (fermion column: lightest fermion mass in horizon units that would satisfy it):")
for r in REC:
    if r["pid"] in ("P01", "P02", "P03", "P04", "P05") and r["species_type"] == "fermion":
        s = ("no solution (sign)" if r.get("Mstar") is None and r["c"] != 0 else "(any heavy fermion; c = 0)" if r["c"] == 0 else f"M* = 10^{r['Mstar']:.2f}, m* = 10^{r['m_star_eV_log10']:.1f} eV")
        print(f"    {r['pid']} {r['variant'][:46]:46s} {s:40s} shortfall of the electron {r['shortfall'] if r['shortfall'] else float('nan'):.2e}")
fn = L.write_json("u1_1_results.json", MUT, dict(records=REC, X_f=X_f, X_tot=X_tot, X_pi=X_pi, H_eV=L.H_EV, n_eval=n_eval))
print(f"\nrecords written to {fn.split('/')[-1]}")
print(f"CHECKS: {sum(o for _, o in chk.items)}/{len(chk.items)} passed")
print("VERDICT: every sigma-type variant is DEAD on the known spectrum (|sigma_e/H| ~ 2e-81); q = 2 in P03 is VACUOUS (holds for any alpha). alpha stays an INPUT; kappa = 1/2 FITTED.")
L.finish(chk, MUT, targeted_tags=["B1"])
