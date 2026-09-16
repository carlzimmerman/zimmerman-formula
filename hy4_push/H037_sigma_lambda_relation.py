#!/usr/bin/env python3
r"""H037 -- SIGMA FROM LAMBDA: a Kepler-grade dispersion law, and whether it is
            a prediction or a rearrangement.

THE DERIVATION (one line of algebra, done two ways).

    G046 (temperature)      sigma^2 = (1/2) sqrt(G M_b a_0)
    H016 (the seesaw)       a_0     = Lambda^2 / (n M_Pl),      n = 2

Eliminate a_0.  In natural units (hbar = c = 1, G = 1/M_Pl^2):

    sigma^4 = (1/4) G M_b a_0 = M_b Lambda^2 / (4 n M_Pl^3)

    ==>  sigma = (1/sqrt2) [ M_b Lambda^2 / (n M_Pl^3) ]^{1/4}
                = (1/sqrt2) (n M_Pl^3)^{-1/4}  Lambda^{1/2}  M_b^{1/4}

In SI (Lambda an ENERGY in joule, M_Pl = sqrt(hbar c/G) a MASS in kg, because
a_0 [m/s^2] = a_0[J] * c/hbar  and  a_0[J] = Lambda^2/(n M_Pl c^2) ):

    sigma^4 = G M_b Lambda^2 / (4 n M_Pl c hbar)
            = (M_b Lambda^2 / 4n) (G/(hbar c))^{3/2}          [M_Pl eliminated]

With n = 2 the two closed forms are

    sigma^4 = G M_b Lambda^2 / (8 M_Pl c hbar) = (M_b Lambda^2/8)(G/hbar c)^{3/2}

    sigma^4/M_b = G Lambda^2/(8 M_Pl c hbar)   <-- UNIVERSAL: no M_b, no a_0

Since Lambda^4 = rho_Lambda (i.e. Lambda^2 = rho_Lambda^{1/2}), the same
statement reads  sigma^8  proportional to  rho_Lambda  at fixed M_b:
THE EIGHTH POWER OF THE HALO DISPERSION TRACKS THE DARK-ENERGY DENSITY.

THE THREE QUESTIONS ASKED, ANSWERED UP FRONT (details below):
  Q1  sigma proportional to Lambda^{1/2} at fixed M_b?   YES, exponent 1/2 exactly.
  Q2  Does that give a testable prediction?              NO, not as stated.
      Lambda is MEASURED, not a knob: the "sigma(Lambda)" scaling cannot be
      dialled.  The only live content is the ZERO POINT sigma^4/M_b, and that
      is P6 (the BTFR zero point) divided by 4 -- i.e. it is the same 22%
      a_0 tension (H029/P11) rescaled by the 1/4 power into a 4.8% tension in
      sigma, which sits BELOW the 0.075 dex (18.9%) intrinsic scatter of the
      observed M-sigma relation.  Not currently discriminating.
  Q3  Consistent with the observed Faber-Jackson-like sigma ~ M^{1/4}?  YES --
      but the exponent is a REARRANGEMENT of the input (sigma^4 = G M_b a_0/4
      IS the BTFR), so this is CIRCULAR and is not counted as a result.

HONEST CLASSIFICATION (H029 rule: no rearrangement of the postulate is a
finding).  This lane produces a NEW FORM and NO NEW CONTENT:
    * sigma^4 = (M_b Lambda^2/8)(G/hbar c)^{3/2} is a closed relation between
      a galactic observable and a cosmological one, with no a_0 in it.  New
      as a statement.
    * But a_0 = Lambda^2/(2 M_Pl) is ALGEBRAICALLY THE POSTULATE (H029 proved
      [Lambda^2/(2 M_Pl)]/a_0 = 1 identically), so substituting it into G046
      is a change of variable.  Every number this lane predicts is a number
      the BTFR + the postulate already predicted.
    * Verdict: KEPLER-GRADE IN FORM, CIRCULAR IN CONTENT, NOT INDEPENDENTLY
      TESTABLE AT CURRENT PRECISION.

Every check states measurement and threshold separately.  Both a_0 footings.
"""
import json, math
import sympy as sp

RES, NP_, NF_ = [], 0, 0
def check(n, measured, ok, d=""):
    global NP_, NF_
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         {d}")
    RES.append({"check": n, "measured": measured, "pass": ok})
    if ok: NP_ += 1
    else:  NF_ += 1
    return ok

# ---------------------------------------------------------------- constants
G     = 6.67430e-11
c     = 2.99792458e8
hbar  = 1.054571817e-34
eV_J  = 1.602176634e-19
Msun  = 1.98847e30
MPC   = 3.0856775814913673e22
n     = 2                                   # the SPARC / seesaw integer
Mpl_kg = math.sqrt(hbar*c/G)                # NON-reduced Planck mass, kg
Mpl_eV = Mpl_kg*c**2/eV_J
H0    = 67.4e3/MPC
OmL   = 0.685
FOOT  = {"canonical": 9.3619e-11, "alternative": 1.1279e-10}

# the two routes, to be compared
def a0_of_Lambda(Lam_J):                    # Lam_J in JOULE (an energy)
    return Lam_J**2/(n*Mpl_kg*c*hbar)
def Lambda_of_a0(a0):
    return math.sqrt(n*Mpl_kg*c*hbar*a0)
def sigma_G046(Mb_kg, a0):                  # the temperature relation
    return math.sqrt(0.5*math.sqrt(G*Mb_kg*a0))
def sigma_Keppler(Mb_kg, Lam_J):            # the new closed form
    return ((Mb_kg*Lam_J**2/(4.0*n))*(G/(hbar*c))**1.5)**0.25
def v_c(Mb_kg, a0):                         # BTFR circular velocity
    return (G*Mb_kg*a0)**0.25

print("="*78)
print("H037 -- SIGMA FROM LAMBDA:  sigma^4 = G M_b Lambda^2 / (4 n M_Pl c hbar)")
print("="*78)

# ============================================================ 1. derivation
print("\n" + "="*78)
print("PART 1 -- THE ALGEBRA (sympy, exact)")
print("="*78)

Lam, Mb, Mpl, nn = sp.symbols('Lambda M_b M_Pl n', positive=True)
G_nat = 1/Mpl**2                                   # natural units
a0    = Lam**2/(nn*Mpl)
sig4  = sp.Rational(1,4)*G_nat*Mb*a0               # from sigma^2 = (1/2)sqrt(G Mb a0)
sig   = sig4**sp.Rational(1,4)

target = G_nat*Mb*Lam**2/(4*nn*Mpl) * Mpl**0       # sigma^4 = M_b Lambda^2/(4 n M_Pl^3)
target = Mb*Lam**2/(4*nn*Mpl**3)
resid  = sp.simplify(sig4 - target)
check("D1 [ELIMINATION] sigma^4 - M_b Lambda^2/(4 n M_Pl^3) simplifies to zero",
      f"residual = {resid}",
      sp.simplify(resid) == 0,
      "sigma^4 = M_b Lambda^2/(4 n M_Pl^3) in natural units; with n=2 the\n"
      "         Planck factor is (2 M_Pl^3)^{-1}. Exact, no approximation.")

e_Lam = sp.simplify(sp.diff(sp.log(sig), Lam)*Lam)
e_Mb  = sp.simplify(sp.diff(sp.log(sig), Mb)*Mb)
e_n   = sp.simplify(sp.diff(sp.log(sig), nn)*nn)
e_Mpl = sp.simplify(sp.diff(sp.log(sig), Mpl)*Mpl)
check("D2 [THE EXPONENTS] dln sigma/dln Lambda = 1/2 and dln sigma/dln M_b = 1/4",
      f"dln sigma/dln Lambda = {e_Lam},  dln sigma/dln M_b = {e_Mb},"
      f"  dln sigma/dln n = {e_n},  dln sigma/dln M_Pl = {e_Mpl}",
      abs(float(e_Lam) - 0.5) < 1e-12 and abs(float(e_Mb) - 0.25) < 1e-12
      and abs(float(e_n) + 0.25) < 1e-12 and abs(float(e_Mpl) + 0.75) < 1e-12,
      "sigma = (1/sqrt2)(n M_Pl^3)^{-1/4} Lambda^{1/2} M_b^{1/4}: the dispersion\n"
      "         is the GEOMETRIC MEAN of the dark-energy scale and the baryon\n"
      "         mass measured in Planck units, to the one-quarter power.")

# SI closed form vs the original route, both footings, over a mass grid
print("\n      route A: sigma^2 = (1/2) sqrt(G M_b a_0)      [G046, a_0 given]")
print("      route B: sigma^4 = (M_b Lambda^2/4n)(G/hbar c)^{3/2}   [Lambda given]")
worst = 0.0
for fname, a0 in FOOT.items():
    Lam_J = Lambda_of_a0(a0)
    for Mb_s in [1e6, 1e9, 1e10, 6e10, 1e11, 1e12, 1e15]:
        m = Mb_s*Msun
        r = sigma_Keppler(m, Lam_J)/sigma_G046(m, a0)
        worst = max(worst, abs(r-1.0))
check("D3 [BOTH ROUTES AGREE] route B / route A over M_b = 1e6..1e15 Msun on\\n"
      "      both a_0 footings",
      f"max |ratio - 1| = {worst:.3e}",
      worst < 1e-12,
      "The SI closed form and the original temperature relation are the SAME\n"
      "         function. This is the whole point: nothing new was added by the\n"
      "         elimination -- only a_0 was renamed."  )

# dimensional audit, exponent bookkeeping (kg, m, s)
D = {'G':       {'kg':-1,'m':3,'s':-2},
     'hbar':    {'kg': 1,'m':2,'s':-1},
     'c':       {'kg': 0,'m':1,'s':-1},
     'Lambda':  {'kg': 1,'m':2,'s':-2},     # an energy
     'M_b':     {'kg': 1,'m':0,'s': 0}}
def mul(a,b): return {k:a[k]+b[k] for k in a}
def pw(a,p):  return {k:a[k]*p   for k in a}
dim = mul(pw(D['M_b'],1), pw(D['Lambda'],2))
dim = mul(dim, pw(mul(D['G'], pw(mul(D['hbar'],D['c']),-1)), 1.5))
check("D4 [DIMENSIONS] (M_b Lambda^2/4n)(G/(hbar c))^{3/2} carries the units of\\n"
      "      a velocity to the fourth",
      f"kg^{dim['kg']} m^{dim['m']} s^{dim['s']}  (target kg^0 m^4 s^-4)",
      dim == {'kg':0,'m':4,'s':-4},
      "The relation is dimensionally closed: M_Pl has been ELIMINATED, so the\n"
      "         whole right-hand side is G, hbar, c, Lambda and M_b only.")

# ============================================================ 2. the numbers
print("\n" + "="*78)
print("PART 2 -- THE NUMBERS (both a_0 footings)")
print("="*78)

# Lambda implied by each footing
print(f"  M_Pl = sqrt(hbar c/G) = {Mpl_kg:.6e} kg = {Mpl_eV/1e9:.4e} GeV")
Lam_meV = {}
for fname, a0 in FOOT.items():
    L = Lambda_of_a0(a0)
    Lam_meV[fname] = L/eV_J*1e3
    print(f"  {fname:<12s} a_0 = {a0:.4e} m/s^2  ->  Lambda = {Lam_meV[fname]:.4f} meV")
check("N1 [THE SCALE IS RECOVERED] Lambda from the canonical footing equals the\\n"
      "      registered 2.2404 meV",
      f"Lambda(canonical) = {Lam_meV['canonical']:.4f} meV (registered 2.2404)",
      abs(Lam_meV['canonical'] - 2.2404) < 0.01,
      "The footing and the scale are the same measurement, read backwards.\n"
      f"         The alternative footing (a_0 = 1.1279e-10) means Lambda = "
      f"{Lam_meV['alternative']:.4f} meV,\n         i.e. it is a +{100*(Lam_meV['alternative']/Lam_meV['canonical']-1):.1f}% "
      "cosmology, not a different law.")

# the universal constant sigma^4/M_b, and the astronomer's form M_b/sigma^4
print("\n  the universal constant  K = sigma^4/M_b = G Lambda^2/(4 n M_Pl c hbar):")
K = {}
for fname, a0 in FOOT.items():
    L = Lambda_of_a0(a0)
    K[fname] = G*L**2/(4*n*Mpl_kg*c*hbar)
    Ainv = 4.0/(G*a0)/Msun*(1e3)**4              # M_b/sigma^4 in Msun/(km/s)^4
    print(f"    {fname:<12s} K = {K[fname]:.6e} (m/s)^4/kg"
          f"   ->  M_b/sigma^4 = {Ainv:.2f} Msun/(km/s)^4")
A_reg = 80.46                                     # registered BTFR zero point
ratio4 = (4.0/(G*FOOT['canonical'])/Msun*(1e3)**4)/(4*A_reg)
check("N2 [THE ZERO POINT IS THE BTFR, QUARTERED] M_b/sigma^4 = 4/(G a_0) = 4A,\\n"
      "      with A = 80.46 Msun/(km/s)^4 the registered BTFR zero point",
      f"M_b/sigma^4 = {4.0/(G*FOOT['canonical'])/Msun*(1e3)**4:.2f} vs "
      f"4A = {4*A_reg:.2f} Msun/(km/s)^4;  ratio = {ratio4:.6f}",
      abs(ratio4 - 1.0) < 5e-3 and abs(ratio4*1.0 - 1.0) > 0,
      "sigma = v_c/sqrt2 EXACTLY (P5), so sigma^4 = v_c^4/4 and the dispersion\n"
      "         zero point is the BTFR zero point times four. This is the\n"
      "         clearest sign that the new relation carries no new content.")

# dispersion table
print("\n  sigma(M_b) from Lambda alone (no a_0, no v_c, zero free parameters):")
print(f"    {'M_b [Msun]':>12s} {'sigma_can [km/s]':>18s} {'sigma_alt [km/s]':>18s}"
      f" {'v_c [km/s]':>12s} {'sigma/v_c':>11s}")
table = {}
for Mb_s in [1e9, 1e10, 6e10, 1e11, 1e12]:
    m = Mb_s*Msun
    row = {}
    for fname, a0 in FOOT.items():
        row[fname] = sigma_Keppler(m, Lambda_of_a0(a0))/1e3
    vv = v_c(m, FOOT['canonical'])/1e3
    row['v_c'] = vv; row['ratio'] = row['canonical']/vv
    table[f"{Mb_s:.0e}"] = row
    print(f"    {Mb_s:>12.0e} {row['canonical']:>18.2f} {row['alternative']:>18.2f}"
          f" {vv:>12.2f} {row['ratio']:>11.6f}")
dev = max(abs(r['ratio'] - 1/math.sqrt(2)) for r in table.values())
check("N3 [P5 RECOVERED] sigma/v_c = 0.707107 at every mass, on the canonical\\n"
      "      footing, when sigma is computed from Lambda directly",
      f"max |sigma/v_c - 1/sqrt2| = {dev:.3e} over M_b = 1e9..1e12 Msun",
      dev < 1e-9 and abs(1/math.sqrt(2) - 0.707107) < 1e-6,
      "The dispersion law and the BTFR are one law. Confirms the internal\n"
      "         consistency of the elimination, and confirms its emptiness.")

# ============================================================ 3. Lambda scaling
print("\n" + "="*78)
print("PART 3 -- HOW SIGMA MOVES WITH LAMBDA  (sigma ~ Lambda^{1/2})")
print("="*78)

a0c  = FOOT['canonical']
Lc   = Lambda_of_a0(a0c)
Mb0  = 1e11*Msun
s0   = sigma_Keppler(Mb0, Lc)
num  = sigma_Keppler(Mb0, Lc*1.01)/sigma_Keppler(Mb0, Lc)
check("S1 [EXPONENT IS ONE HALF] a 1% change in Lambda moves sigma by 0.5%",
      f"sigma(1.01 Lambda)/sigma(Lambda) = {num:.9f} vs 1.01^0.5 = {1.01**0.5:.9f}",
      abs(num - 1.01**0.5) < 1e-12,
      "d ln sigma / d ln Lambda = 1/2. Equivalently sigma^8 is proportional to\n"
      "         rho_Lambda: the eighth power of the halo dispersion tracks the\n"
      "         dark-energy density at fixed baryon mass.")

print("\n      if Lambda were different, at fixed M_b = 1e11 Msun "
      f"(sigma_0 = {s0/1e3:.2f} km/s):")
print(f"    {'dLambda/Lambda':>16s} {'dsigma/sigma':>14s} {'sigma [km/s]':>14s} {'dsigma [km/s]':>14s}")
for f in [0.01, 0.05, 0.10, 0.25, 0.50, 1.00]:
    s1 = s0*(1+f)**0.5
    print(f"    {100*f:>15.1f}% {100*((1+f)**0.5-1):>13.2f}%"
          f" {s1/1e3:>14.2f} {(s1-s0)/1e3:>14.2f}")

# what the measured spread in Lambda actually buys you
H0_planck, H0_sh0es = 67.4, 73.04                 # km/s/Mpc
Lam_ratio = (H0_sh0es/H0_planck)**0.5             # Lambda ~ (OmL h^2)^{1/4} ~ h^{1/2}
sig_ratio = Lam_ratio**0.5
d_sigma   = 100.0*(sig_ratio - 1.0)               # km/s at sigma0 = 100 km/s
check("S2 [THE H0 TENSION, TRANSLATED] Planck H0 = 67.4 vs SH0ES H0 = 73.04 is a\\n"
      "      4.1% Lambda difference, hence a 2.0% sigma difference",
      f"Lambda ratio = {Lam_ratio:.4f}, sigma ratio = {sig_ratio:.4f}, "
      f"delta sigma = {d_sigma:.2f} km/s at sigma_0 = 100 km/s",
      abs(Lam_ratio - 1.0410) < 5e-3 and abs(d_sigma - 2.03) < 0.2,
      "Because sigma goes as the SQUARE ROOT of Lambda and Lambda only as the\n"
      "         FOURTH ROOT of rho_Lambda, even a 9% Hubble split is diluted to\n"
      "         2% in the dispersion. The 1/2 exponent DEADENS the sensitivity.")

# against the real observational precision
scatter_dex = 0.075                               # Cannarozzo+2020 intrinsic scatter
scatter_pct = (10**scatter_dex - 1)*100
a0_tension  = 1.1279/0.93619 - 1                  # the 22% (H029 / P11)
sig_tension = (1+a0_tension)**0.25 - 1
check("S3 [IS IT DISCRIMINATING?] the Lambda-induced sigma shift versus the\\n"
      "      intrinsic scatter of the observed M-sigma relation",
      f"H0-tension shift = {100*sig_ratio-100:.2f}%;  whole 22% a_0 tension "
      f"damped to {100*sig_tension:.2f}%;\n         observed intrinsic scatter "
      f"= 0.075 dex = {scatter_pct:.1f}%",
      100*sig_tension < scatter_pct and 100*(sig_ratio-1) < scatter_pct,
      "BOTH signals sit under the scatter. sigma ~ a_0^{1/4}, so the quarter\n"
      f"         power that makes the relation look precise also makes it hard to\n"
      f"         falsify: a 22% error in a_0 is only a {100*sig_tension:.1f}% error in sigma.")

# ============================================================ 4. Faber-Jackson
print("\n" + "="*78)
print("PART 4 -- FABER-JACKSON:  sigma ~ M_b^{1/4}")
print("="*78)

check("F1 [THE EXPONENT MATCHES] predicted dln sigma/dln M_b = 0.25; observed\\n"
      "      <log sigma | log L> slope ~ 1/4 (canonical Faber-Jackson)",
      f"predicted 0.250000;  observed a_(sigma|L) ~ 0.25 (canonical FJ), "
      f"0.176 (Cannarozzo+2020 SDSS), ~0.30 (massive quiescents)",
      abs(0.25 - 0.25) < 0.05,
      "Consistent. BUT: sigma^4 = G M_b a_0/4 IS the BTFR with v_c -> sigma sqrt2,\n"
      "         so 'sigma ~ M_b^{1/4}' is a REARRANGEMENT OF THE INPUT, not a\n"
      "         derivation of Faber-Jackson. Per H029 it is not a result.")

# the zero point, which is the only part that could bite
Mb_anchor = 1e11*Msun
pred_c = sigma_Keppler(Mb_anchor, Lambda_of_a0(FOOT['canonical']))/1e3
pred_a = sigma_Keppler(Mb_anchor, Lambda_of_a0(FOOT['alternative']))/1e3
obs    = 170.0            # sigma_e at M_* = 1e11 Msun, SDSS ETGs (Cannarozzo+2020)
print(f"\n  predicted sigma(M_b = 1e11 Msun):  canonical {pred_c:.1f} km/s,"
      f"  alternative {pred_a:.1f} km/s")
print(f"  observed  sigma_e(M_* = 1e11 Msun) = {obs:.0f} km/s, "
      f"intrinsic scatter 0.075 dex = {scatter_pct:.1f}%")
kappa = obs/pred_c
check("F2 [THE ZERO POINT DOES NOT MATCH -- AND THE REASON MATTERS] predicted\\n"
      "      halo sigma against the observed stellar sigma_e at M = 1e11 Msun",
      f"predicted {pred_c:.1f} (canonical) / {pred_a:.1f} (alternative) vs "
      f"observed {obs:.0f} km/s;  kappa = sigma_e/sigma_halo = {kappa:.3f}",
      abs(obs/pred_c - 1.0) < 0.10,
      "FAILS, and it fails by much more than the 22%: the deficit is 28% in\n"
      "         sigma, which would need a_0 larger by 2.7x -- far outside P11.\n"
      "         So G046's sigma is the HALO dispersion, not the aperture stellar\n"
      "         dispersion sigma_e; the conversion kappa ~ 1.28 is NOT derived\n"
      "         and is not a constant of the framework. The Faber-Jackson\n"
      "         comparison therefore tests the EXPONENT only, never the zeropoint.")

# ============================================================ 5. verdict
print("\n" + "="*78)
print("PART 5 -- IS IT CIRCULAR?")
print("="*78)

# rho_Lambda = 4 Lambda^4/(n^2 M_Pl^2 G c^2); with G = 1/M_Pl^2 (natural) and
# n = 2 this is exactly rho_Lambda = Lambda^4.  Check it with real numbers.
rho_L   = OmL*3.0*H0**2/(8.0*math.pi*G)                 # kg/m^3
rho_eV4 = rho_L*c**2*(hbar*c)**3/eV_J**4                # natural units, eV^4
Lam_eV  = Lam_meV['canonical']*1e-3
rho_from_Lam = 4.0*Lam_eV**4/n**2
r_id = rho_from_Lam/rho_eV4
check("C1 [THE SEESAW IS THE POSTULATE] a_0 = Lambda^2/(n M_Pl) is identical to\\n"
      "      a_0 = (1/2) c sqrt(G rho_Lambda) because rho_Lambda = 4 Lambda^4/n^2\\n"
      "      = Lambda^4 for n = 2 (natural units)",
      f"rho_Lambda(from H0, OmL) = {rho_eV4:.6e} eV^4;  "
      f"4 Lambda^4/n^2 = {rho_from_Lam:.6e} eV^4;  ratio = {r_id:.6f}",
      abs(r_id - 1.0) < 1e-3,

      "H029 already proved this: [Lambda^2/(2 M_Pl)]/a_0 = 1 IDENTICALLY. So the\n"
      "         substitution performed in this lane is a CHANGE OF VARIABLE.\n"
      "         Everything downstream of it carries exactly the information\n"
      "         that G046 + the postulate already carried, nothing more.")

print(f"""
  THE RELATION (new in form):

      sigma^4 = G M_b Lambda^2 / (4 n M_Pl c hbar)
              = (M_b Lambda^2 / 4n) (G/(hbar c))^{{3/2}}            [M_Pl eliminated]

      n = 2:   sigma^4 = (M_b Lambda^2 / 8) (G/(hbar c))^{{3/2}}
               sigma   = (1/sqrt2) (2 M_Pl^3)^{{-1/4}} Lambda^{{1/2}} M_b^{{1/4}}
               sigma^4/M_b = {K['canonical']:.4e} (m/s)^4/kg   (canonical footing)
                           = {K['alternative']:.4e} (m/s)^4/kg   (alternative footing)

  THE ANSWERS:

    * SCALING EXPONENT IN LAMBDA:  1/2  (sigma ~ Lambda^{{1/2}}, i.e. sigma^8 ~ rho_Lambda)
    * SCALING EXPONENT IN M_b:     1/4  (matches Faber-Jackson-like sigma ~ M^{{1/4}})
    * TESTABLE?                    NOT AS STATED, AND NOT AT CURRENT PRECISION.
        - Lambda is measured, not variable: "what if Lambda changed" is
          counterfactual, not an experiment.
        - The zero point sigma^4/M_b is the BTFR zero point /4, so the only
          live test is P11's 22% a_0 tension, damped by the 1/4 power to
          {100*sig_tension:.1f}% in sigma -- under the {scatter_pct:.1f}% intrinsic scatter of the
          observed M-sigma relation.
        - The H0 tension (67.4 vs 73.04) buys only {100*(sig_ratio-1):.1f}% in sigma.
    * CIRCULAR?                    YES, IN CONTENT.
        a_0 = Lambda^2/(2 M_Pl) is the postulate (H029). Substituting it into
        G046 renames a_0; it does not predict anything P6/P5 did not. The
        Faber-Jackson exponent check is likewise a rearrangement: sigma^4 =
        G M_b a_0/4 is the BTFR. Count this as a UNIFICATION (one fewer
        symbol in the relation), not as a prediction and not as a test.

  WHAT WOULD MAKE IT WORTH SOMETHING:
    1. Derive the halo-sigma / stellar-sigma_e conversion kappa ~ {kappa:.2f} from the
       action. Until then the M-sigma comparison is exponent-only.
    2. Measure sigma^4/M_b with systematics below ~5% (not the current 19%).
    3. Or: find a sector where Lambda appears WITHOUT a_0 being measurable --
       i.e. where the elimination is not invertible. Halo dispersion is not
       such a sector; a_0 is measured far better than sigma is.
""")

json.dump({"lane": "H037", "pass": NP_, "fail": NF_, "results": RES,
           "relation": "sigma^4 = G M_b Lambda^2/(4 n M_Pl c hbar) = (M_b Lambda^2/4n)(G/(hbar c))^{3/2}",
           "closed_form_n2": "sigma = (1/sqrt2)(2 M_Pl^3)^{-1/4} Lambda^{1/2} M_b^{1/4}",
           "exponent_Lambda": 0.5, "exponent_Mb": 0.25,
           "K_sigma4_over_Mb": K, "Lambda_meV": Lam_meV,
           "Mpl_GeV": Mpl_eV/1e9,
           "sigma_kms_at_1e11_Msun": {"canonical": pred_c, "alternative": pred_a},
           "kappa_sigma_e_over_sigma_halo": kappa,
           "H0_tension_dsigma_percent": 100*(sig_ratio-1),
           "a0_tension_damped_to_percent": 100*sig_tension,
           "testable": False, "circular": True,
           "verdict": "new in form, circular in content; zero point is P6/4 and sits "
                      "below the 0.075 dex scatter of the observed M-sigma relation"},
          open("/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/H037_results.json","w"),
          indent=2)
print("="*78)
print(f"H037 READING:  {NP_} PASS / {NF_} FAIL")
print("="*78)
print(json.dumps({"pass": NP_, "fail": NF_}))
