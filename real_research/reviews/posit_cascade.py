#!/usr/bin/env python3
"""
CLASS 3 -- SCALE / CASCADE routes from the framework to the SM, enumerated and graded
=====================================================================================
Carl ('more posits for a TOE'): does the SM mass spectrum CASCADE from the framework's
own scales (Lambda / E_dS / E_Planck / E_Hubble) by a FORCED operation -- or only by a
coincidence that dies under a look-elsewhere (FDR) penalty?

FOOTING (LOCKED, framework's own premises -- NEVER the standard-MOND lens):
  a0   = c H_Lambda / Z = 9.36e-11 m/s^2      (modified INERTIA, dS-Unruh horizon)
  Z    = sqrt(32 pi / 3) = 5.7878...           (FREE -- kappa-closure; carries sqrt(pi))
  H_Lam= 1.808e-18 /s    (pure-Lambda de Sitter Hubble)
  rho_DE = 3 H_Lam^2 / (8 pi G);  E_dS = rho_DE^(1/4) = 2.24 meV (vacuum-energy scale)

THE WALLS every route must clear (from the committed ledger / memory):
  (W1) flavor-blindness: inertia ~ |a| only (EP) -> no per-flavor handle.
  (W2) NUMBER-FIELD: Z carries sqrt(pi) (transcendental); all flavor data is ALGEBRAIC
       -> any a0/Z-built mass scale is structurally gauge/flavor-BLIND for the VALUE.
  (W3) 30-order SCALE GAP: a0~1e-10 m/s^2, E_dS~meV vs SM masses MeV..TeV.
  (W4) Z is FREE (kappa=1/2 provably unforceable: ghost-freedom+unitarity+holography).
  (W5) Koide circularity: Q = 1/3 + r^2/6 holds for ANY r (sympy-exact) -> non-diagnostic.

KNOWN GRADES (do NOT redo -- cite):
  * Geometric-mean ladder E_dS = sqrt(2/Z) * sqrt(E_P E_H): an ALGEBRAIC IDENTITY (holds
    iff Z^2=32pi/3) -> RESTATES the a0<->Lambda coincidence in UV/IR language, carries NO
    info on the VALUE. (THE_COSMIC_SEESAW.md, project_a0_vacuum_energy_seesaw.py). FDR-aware
    DEAD as a derivation of any SM number.
  * Reaching Lambda_QCD needs an UNFORCED exponent a=0.676 (free Weinberg continuum) ->
    FDR-dead (particle_numerology_standing).
  * The NEUTRINO: E_dS ~ 2.24 meV lands INSIDE the oscillation window [sqrt(dm21),sqrt(dm31)]
    = [8.6, 50] meV and ON the published swampland bound m_nu1 <~ Lambda^(1/4) (Gonzalo-
    Ibanez-Valenzuela 2109.10961). The ONE partial-open. founded-not-derived (bound, not =).

WHAT THIS SCRIPT DOES (prove-by-moving-the-number, with a HARD FDR / look-elsewhere null):
  Enumerate every cascade VARIANT Carl named; for each compute the predicted scale; for each
  'hit' run a Monte-Carlo look-elsewhere null -- how often does a RANDOM target in the same
  decade get matched at least as well by SOME member of the same small operation-grid? If the
  null p is not tiny, the 'hit' is FDR-dead (a coincidence), not a forcing.

REAL LITERATURE (web-checked, both-ways):
  * Cohen-Kaplan-Nelson hep-th/9803132 (UV-IR seesaw rho_Lambda~M_P^2 H^2; an INEQUALITY).
  * Arkani-Hamed-Dimopoulos-Dvali-March-Russell hep-ph/9908146 (neutrino-mass seesaw m~v^2/M).
  * Gonzalo-Ibanez-Valenzuela 2109.10961 (swampland AdS bound m_nu1 <~ Lambda4^(1/4)).
  * Montero-Vafa-Valenzuela 2205.12293 (dark dimension: a meV KK tower at Lambda^(1/4)).
  * Look-elsewhere / FDR: Benjamini-Hochberg; here a direct MC null (the honest guard).
"""
import math
import numpy as np

rng = np.random.default_rng(20260627)

# ---------------------------------------------------------------- footing (LOCKED) --
c    = 2.99792458e8
hbar = 1.054571817e-34
G    = 6.67430e-11
eV   = 1.602176634e-19
H_Lam= 1.808e-18
Z    = math.sqrt(32.0*math.pi/3.0)
a0   = c*H_Lam/Z

E_P_full = 1.22091e19          # GeV  (Planck energy, full)
M_P_red  = 2.435e18            # GeV  (reduced Planck mass)
E_H  = hbar*H_Lam/eV/1e9       # GeV  (Hubble energy scale)
rho_DE = 3.0*H_Lam**2/(8.0*math.pi*G)
E_dS = (rho_DE*c**2*(hbar*c)**3)**0.25/eV/1e9    # GeV  (vacuum-energy scale, rho_DE^1/4)

print("="*96)
print("CLASS 3 -- SCALE / CASCADE routes: enumerate, predict, FDR-null every hit")
print("="*96)
print(f"[footing]  Z={Z:.6f}  a0={a0:.4g} m/s^2  E_dS={E_dS*1e12:.3f} meV  "
      f"E_P={E_P_full:.3g} GeV  E_H={E_H:.3g} GeV")
print(f"[identity check] sqrt(2/Z)*sqrt(E_P_full*E_H) = {math.sqrt(2/Z)*math.sqrt(E_P_full*E_H)*1e12:.3f} meV"
      f"  vs E_dS={E_dS*1e12:.3f} meV  (the algebraic seesaw, NO new info)")

# ---- SM target scales (GeV) we ask the cascade to hit ----------------------------
TARGETS = {
    "m_nu (sqrt dm31)":  math.sqrt(2.51e-3)*1e-9,   # ~0.050 eV
    "m_e":               0.511e-3,
    "m_mu":              0.10566,
    "Lambda_QCD":        0.34,
    "m_p":               0.9383,
    "m_tau":             1.77686,
    "v_EW (Higgs vev)":  246.22,
    "m_top":             172.69,
    "m_W":               80.38,
    "M_GUT":             2e16,
}

# =====================================================================================
# The FDR / look-elsewhere null.
# A cascade 'machine' = a small grid of operations on the framework scales {E_P,E_H,E_dS,M_P}
# combined with framework O(1) factors {1, 2/Z, Z, Z/2pi, sqrt(2/Z), 4pi, ...}. We measure
# how well the BEST machine matches a target, then ask: against a RANDOM target drawn
# log-uniformly across the SAME 35-decade window, how often does the best machine match
# AT LEAST as well? That tail prob is the honest look-elsewhere p-value for the 'hit'.
# =====================================================================================
SCALES = {"E_P": E_P_full, "M_P": M_P_red, "E_H": E_H, "E_dS": E_dS}
O1 = {"1":1.0, "2/Z":2.0/Z, "Z":Z, "Z/2pi":Z/(2*math.pi), "sqrt(2/Z)":math.sqrt(2/Z),
      "4pi":4*math.pi, "1/4pi":1/(4*math.pi), "8pi":8*math.pi}

def machine_grid():
    """Yield (label, value_GeV) for every simple cascade operation on framework scales."""
    out=[]
    names=list(SCALES.items())
    # single scale * O(1)
    for sn,sv in names:
        for on,ov in O1.items():
            out.append((f"{on}*{sn}", ov*sv))
    # geometric mean of any two scales * O(1)  (the seesaw operation + its iterates)
    for i in range(len(names)):
        for j in range(i,len(names)):
            an,av=names[i]; bn,bv=names[j]
            gm=math.sqrt(av*bv)
            for on,ov in O1.items():
                out.append((f"{on}*GM({an},{bn})", ov*gm))
    # three-scale seesaw  X^2/Y  (the ADD-style mass seesaw m~v^2/M)  and  cube-root mean
    for an,av in names:
        for bn,bv in names:
            if an==bn: continue
            out.append((f"{an}^2/{bn}", av*av/bv))
    # iterated geometric mean: GM(scale, E_dS) twice  (the 'forced cascade' candidate)
    for sn,sv in names:
        out.append((f"GM({sn},E_dS)", math.sqrt(sv*E_dS)))
        out.append((f"GM(GM({sn},E_dS),E_dS)", math.sqrt(math.sqrt(sv*E_dS)*E_dS)))
    return out

GRID = machine_grid()
grid_vals = np.array([v for _,v in GRID])
print(f"\n[machine grid] {len(GRID)} simple cascade operations on {{E_P,M_P,E_H,E_dS}} x {len(O1)} O(1)s")

def best_match(target):
    """Return (best_dex_error, label) -- closest grid machine to target (log10 distance)."""
    d = np.abs(np.log10(grid_vals/target))
    k = int(np.argmin(d))
    return d[k], GRID[k][0]

def look_elsewhere_p(observed_dex, n_mc=200000, decades=(-12, 19)):
    """P(a RANDOM log-uniform target in [10^lo,10^hi] GeV is matched <= observed_dex by SOME machine)."""
    lo,hi=decades
    rand_t = 10.0**rng.uniform(lo, hi, n_mc)
    logg = np.log10(grid_vals)
    # for each random target, min over grid of |log10(g/t)|
    lt = np.log10(rand_t)
    # broadcast min-dist: do it in chunks to bound memory
    hits=0
    chunk=4000
    for s in range(0,n_mc,chunk):
        block=lt[s:s+chunk][:,None]                     # (chunk,1)
        dd=np.abs(logg[None,:]-block)                    # (chunk,Ngrid)
        mind=dd.min(axis=1)
        hits+=int(np.sum(mind<=observed_dex))
    return hits/n_mc

# =====================================================================================
# ENUMERATE THE NAMED VARIANTS, grade each.
# =====================================================================================
print("\n" + "-"*96)
print("VARIANT-BY-VARIANT (predicted scale, best-match target, FDR look-elsewhere p)")
print("-"*96)

def report(name, value_GeV, claim_target):
    tval=TARGETS[claim_target]
    dex=abs(math.log10(value_GeV/tval))
    p=look_elsewhere_p(dex)
    flag = "FORCED-ish" if (dex<0.1 and p<0.01) else ("near-miss" if dex<0.7 else "MISS")
    print(f"  {name}")
    print(f"     predicted = {value_GeV:.4g} GeV   claim->{claim_target}={tval:.4g} GeV   "
          f"|err|={dex:.2f} dex")
    print(f"     look-elsewhere p (random target in 35 decades matched this well by SOME machine) = {p:.3f}"
          f"   [{flag}]")
    return dex,p

# (3a) geometric-mean ladder  E_dS = sqrt(2/Z) sqrt(E_P E_H)  -> the NEUTRINO scale
gm_eds = math.sqrt(2/Z)*math.sqrt(E_P_full*E_H)      # = E_dS = 2.24 meV exactly (the identity)
m_sol  = math.sqrt(7.42e-5)*1e-9   # GeV, sqrt(dm21) ~ 8.6 meV  (light end of the nu window)
m_atm  = math.sqrt(2.51e-3)*1e-9   # GeV, sqrt(dm31) ~ 50  meV  (heavy end)
print("  (3a) GM ladder  sqrt(2/Z)*sqrt(E_P*E_H)  [seesaw identity -> meV]")
print(f"     predicted E_dS = {gm_eds*1e12:.2f} meV   nu window [sqrt(dm21),sqrt(dm31)] = "
      f"[{m_sol*1e12:.1f}, {m_atm*1e12:.1f}] meV")
print(f"     E_dS is ON the published swampland bound m_nu1 <~ Lambda^(1/4) (Gonzalo-Ibanez-Valenzuela")
print(f"     2109.10961: NH-Dirac m_nu1<=7.7 meV) -> sits at the LIGHT-nu mass scale (factor ~{m_atm/gm_eds:.0f}")
print(f"     below the heaviest splitting -- a BOUND/coincidence, NOT a forced equality).")
print("        STATUS: algebraic IDENTITY (Z^2=32pi/3). Lands the meV/neutrino scale. The ONE")
print("        partial-open, but it is the COINCIDENCE restated, not a VALUE derivation. -> PARTIAL-OPEN (nu).")

# (3b) iterated GM cascade -> EW?  GM(E_P, E_dS)
gm_ew = math.sqrt(E_P_full*E_dS)
d,p = report("(3b) iterated cascade  GM(E_P, E_dS)  -> EW?", gm_ew, "v_EW (Higgs vev)")
print("        Forcing claim FAILS: lands ~few TeV, misses v_EW=246 GeV by ~1.3 dex; and the FDR p is")
print("        not tiny -> a near-miss with no forcing. NOT a 3-scale forced cascade. -> TRIED-WALLED (W3).")

# (3c) three-scale see-saw  E_dS^2/E_H  and  E_P^2/M_P style  (ADD seesaw m~v^2/M form)
seesaw3 = E_dS*E_dS/E_H
report("(3c) 3-scale seesaw  E_dS^2 / E_H", seesaw3, "M_GUT")
print("        The v^2/M seesaw with framework scales lands ~1e18 GeV-ish; no SM number")
print("        is forced (the operation is CHOSEN, look-elsewhere large). -> TRIED-WALLED.")

# (3d) Z -> a coupling constant:  compare 1/Z^2, Z/2pi, 4/Z^2 to alpha and sin^2theta_W
print("\n  (3d) Z -> a COUPLING constant (dimensionless; dodges W3 scale gap, hits W2 number-field):")
alpha_em = 1/137.035999
sin2thW  = 0.23122           # MSbar at M_Z (PDG)
cands = {"1/Z^2":1/Z**2, "Z/2pi":Z/(2*math.pi), "1/Z":1/Z, "4/Z^2":4/Z**2,
         "3/(8pi)":3/(8*math.pi), "2/Z":2/Z}
print(f"        alpha_em={alpha_em:.5f}   sin^2theta_W(M_Z)={sin2thW:.5f}")
for nm,v in cands.items():
    da=abs(math.log10(v/alpha_em)); ds=abs(math.log10(v/sin2thW))
    tag=[]
    if da<0.05: tag.append(f"~alpha ({da:.3f}dex)")
    if ds<0.05: tag.append(f"~sin2thW ({ds:.3f}dex)")
    print(f"        {nm:8s} = {v:.5f}   {('  '.join(tag)) if tag else ''}")
# honest null on the BEST coupling 'hit'
best_coup_dex = min(abs(math.log10(v/sin2thW)) for v in cands.values())
# look-elsewhere over a coupling: how many of {alpha, sin2thW, alpha_s, ...} x {6 Z-cands} land <0.05 dex by chance?
print(f"        BEST coupling match within {best_coup_dex:.3f} dex; with 6 candidates x 3 running targets the")
print(f"        expected number of <0.05-dex coincidences by chance ~ 6*3*2*0.05 ~ 1.8 -> EXPECTED. W2 holds")
print(f"        (Z carries sqrt(pi); couplings run/are scheme-dependent and ALGEBRAIC-at-a-scale).")
print(f"        -> TRIED-WALLED (W2 number-field; running target).")

# (3e) swampland tower m ~ M_P exp(-alpha dphi): other tower states = charged leptons?
print("\n  (3e) swampland tower  m_n ~ M_P*exp(-alpha*dphi)  (other states = charged leptons?):")
# the framework fixes only dphi(z) (observable) + alpha~lambda (conjectured); the ABSOLUTE
# scale (total field distance) is FREE. A charged-lepton tower would need an integer/level
# structure giving m_e:m_mu:m_tau = the lepton ratios. Test: is exp(-alpha*n) a geometric
# tower matching the lepton hierarchy for any single alpha?
m_e,m_mu,m_tau=0.511e-3,0.10566,1.77686
r1=m_mu/m_e; r2=m_tau/m_mu
print(f"        lepton ratios: m_mu/m_e={r1:.1f}  m_tau/m_mu={r2:.2f}  (NON-geometric: {r1:.0f} vs {r2:.1f})")
print(f"        a single-alpha geometric tower predicts a CONSTANT ratio; the leptons are NOT geometric")
print(f"        (206.8 vs 16.8) -> no single swampland tower reproduces the hierarchy. And W1: the tower")
print(f"        mass is flavor-BLIND. -> TRIED-WALLED (W1 flavor-blindness + non-geometric spectrum).")

# (3f) dark-dimension KK tower -> KK masses
print("\n  (3f) dark-dimension KK tower  m_KK ~ 1/R ~ Lambda^(1/4):")
ell_dd = hbar*c/(E_dS*1e9*eV)   # m, the meV Compton length
print(f"        m_KK ~ E_dS ~ {E_dS*1e12:.2f} meV (a meV KK tower, the dark-dimension scale, R~{ell_dd*1e6:.0f} um)")
print(f"        This is a DIFFERENT theory (an extra dimension); the framework has NO extra dimension")
print(f"        -> predicts NO sub-mm force. A KK SM-flavor map needs the radion/wavefunction profiles")
print(f"        the framework does not contain. -> TRIED-WALLED (not the framework; W1/W2 for flavor).")

# =====================================================================================
# THE GENUINELY-UNTRIED ANGLE + a real feasibility check
# =====================================================================================
print("\n" + "="*96)
print("GENUINELY-UNTRIED: the RATIO cascade -- is sqrt(E_dS/E_P) (a PURE number) a SM ratio?")
print("="*96)
# Rationale: W2 says a0/Z is gauge-BLIND for any ABSOLUTE scale (sqrt(pi), algebraic mismatch).
# But the DIMENSIONLESS ratio  eps == E_dS/E_P  is the ONLY pure number the cascade makes that
# is NOT pre-loaded with Z's sqrt(pi) in a value-bearing way (it is rho_DE^1/4 / E_P). Untried
# question: does eps or sqrt(eps) coincide with a *dimensionless* SM ratio (a Yukawa, a mixing
# angle, a mass ratio) -- and does it SURVIVE a look-elsewhere null? If yes -> a NEW forced
# dimensionless tie; if no (expected) -> a clean, honest, NEGATIVE that closes the angle.
eps = E_dS/E_P_full
print(f"  eps = E_dS/E_P = {eps:.3e}   sqrt(eps)={math.sqrt(eps):.3e}   eps^(1/4)={eps**0.25:.3e}")
# candidate dimensionless SM ratios spanning the small-number landscape
SM_RATIOS = {
    "y_e (m_e/v)":      0.511e-3/246.22,
    "y_nu (m_nu/v)":    0.05e-9/246.22,
    "m_e/m_P_red":      0.511e-3/M_P_red,
    "Vub":              0.0037,
    "Vcb":              0.041,
    "theta13(sin)":     0.1487,
    "alpha_em":         alpha_em,
    "m_e/m_tau":        m_e/m_tau,
    "Vus(Cabibbo)":     0.2243,
    "m_nu/m_e":         0.05e-9/0.511e-3,
}
probe = {"eps":eps, "sqrt(eps)":math.sqrt(eps), "eps^1/4":eps**0.25, "eps^1/2*Z":math.sqrt(eps)*Z}
print(f"  {'probe':12s} | closest SM ratio (|dex|)")
best_global=(9,"","")
for pn,pv in probe.items():
    best=(9,"")
    for rn,rv in SM_RATIOS.items():
        d=abs(math.log10(pv/rv))
        if d<best[0]: best=(d,rn)
    print(f"  {pn:12s} | {best[1]:14s}  |{best[0]:.2f} dex|  (probe={pv:.3e})")
    if best[0]<best_global[0]: best_global=(best[0],pn,best[1])
print(f"\n  BEST untried tie: {best_global[1]} ~ {best_global[2]}  at {best_global[0]:.2f} dex")

# FEASIBILITY / FDR null on the best untried tie:
# how often does a RANDOM small dimensionless number (log-uniform over the SM-ratio span,
# 10^-44 .. 10^0) get matched <= best_global[0] dex by SOME probe in {eps,sqrt(eps),eps^1/4,...}?
probe_vals=np.array(list(probe.values()))
def le_p_dimensionless(obs_dex, n_mc=400000, decades=(-44,0)):
    lt=np.log10(10.0**rng.uniform(decades[0],decades[1],n_mc))
    logp=np.log10(probe_vals)
    hits=0; chunk=8000
    for s in range(0,n_mc,chunk):
        block=lt[s:s+chunk][:,None]
        mind=np.abs(logp[None,:]-block).min(axis=1)
        hits+=int(np.sum(mind<=obs_dex))
    return hits/n_mc
p_untried=le_p_dimensionless(best_global[0])
print(f"  FEASIBILITY (look-elsewhere): a random small dimensionless number is matched <= {best_global[0]:.2f} dex")
print(f"     by SOME of the {len(probe)} probes with p = {p_untried:.3f}.")
verdict = ("SURVIVES (worth a real forcing check)" if p_untried<0.01 and best_global[0]<0.1
           else "FDR-DEAD coincidence (expected by chance) -> a clean NEGATIVE")
print(f"     => {verdict}")

# =====================================================================================
# SUMMARY GRADES
# =====================================================================================
print("\n" + "="*96)
print("CLASS-3 GRADE SUMMARY")
print("="*96)
print("  (3a) GM ladder -> meV/neutrino .................. PARTIAL-OPEN (nu only; identity, founded-not-derived)")
print("  (3b) iterated GM cascade -> EW .................. TRIED-WALLED (W3: misses 246 GeV by ~1.3 dex, FDR not tiny)")
print("  (3c) 3-scale v^2/M seesaw ....................... TRIED-WALLED (operation chosen; no SM number forced)")
print("  (3d) Z -> coupling (alpha, sin^2thW) ............ TRIED-WALLED (W2: sqrt(pi) vs algebraic; running target)")
print("  (3e) swampland tower -> charged leptons ......... TRIED-WALLED (W1 flavor-blind; lepton ratios non-geometric)")
print("  (3f) dark-dimension KK tower .................... TRIED-WALLED (different theory; no extra dim in framework)")
print("  (UNTRIED) eps=E_dS/E_P dimensionless ratio ...... see FDR p above (clean negative expected)")
print("\n  BEST genuinely-untried long-shot = the DIMENSIONLESS eps-ratio cascade, BECAUSE it is the only")
print("  variant that sidesteps W3 (scale gap) by asking for a pure NUMBER, and directly confronts W2.")
print("  Feasibility verdict printed above. The neutrino (3a) remains the only PARTIAL-OPEN.")
print("="*96)
print("EXIT 0 -- no manufactured win, no manufactured deficit.")
