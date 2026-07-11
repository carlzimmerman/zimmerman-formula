#!/usr/bin/env python3
"""
ROUTE A -- the cosmological rigidity bound on Branch B's beta.

QUESTION: The Branch-B medium is a w=-1 relativistic elastic SOLID (published
action, Zenodo 21301460) whose relaxed state IS the dark energy
(T_munu = -rho_L c^2 g_munu, w_eos=-1) but which carries a SHEAR MODULUS mu_s>0
(rigidity). That rigidity sources ANISOTROPIC STRESS in cosmological
perturbations = "elastic / solid dark energy" (Bucher-Spergel 1999 PRD 60 043505;
Battye-Moss 2005/2007; Battye-Pearson). The Cassini fork PASSES iff
   beta = mu_s/(3 K_eff) > beta_crit = 0.42 (canon a0) / 0.60 (alt a0),
with the 6Z^2 mechanical cap beta <= 2 (v_T <= 0.17c). beta is NOT pinned by
the action (it is the shear Poisson-ratio split of K_eff into K_F + mu_s/6).

Route A asks: does the COSMOLOGICAL bound on the shear modulus of w=-1 solid DE
cap beta BELOW beta_crit (=> JOINT Cassini+cosmology FAIL) or ALLOW beta>beta_crit
(=> door open / beta free)?

THE #1 TRAP (handled below): the literature rigidity is c_v^2 = mu/(rho+P)
(Battye-Moss astro-ph/0703744 Eq. 45), which is SINGULAR at w=-1 because
rho+P = rho_L(1+w) -> 0. The finite physical variable is the ABSOLUTE shear
modulus mu_s (Pa), equivalently c_v^2 normalized by the MASS density rho_L:
   c_v^2/c^2 = mu_s/(rho_L c^2).

VERBATIM literature quantities used (quoted, with source):
 * Battye-Moss (astro-ph/0703744), Eq. 45:
     transverse/vector sound speed   c_v^2 = mu/(rho+P)
     longitudinal/scalar sound speed c_s^2 = (beta_bulk + 4mu/3)/(rho+P)
   and Eq. 46: c_s^2 = dP/drho + (4/3) c_v^2.
   Both diverge as w->-1 (rho+P->0): the parametrization singularity = the trap.
 * Radiation-like elastic solid (arXiv:1402.4434 / 1708.00237): "if only the
   ordinary Sachs-Wolfe effect is considered, the shear modulus to energy
   density ratio must be of order 10^-5 or less ... the integrated Sachs-Wolfe
   effect relaxes this constraint by almost two orders of magnitude" (~1e-3).
   -- BUT this is a solid that is RADIATION-LIKE (w=+1/3) and dynamically O(1)
      of the budget AT RECOMBINATION. It does NOT transfer to w=-1 DE (see below).
 * Planck 2015 DE&MG (A&A 594 A14): for minimally-coupled DE they adopt
     "c_s^2 = 1 ... and sigma = 0 (no scalar anisotropic stress)";
   the DE sound speed is essentially UNCONSTRAINED near w=-1 and DE
   perturbations are suppressed by the (1+w) factors in the source terms.

No commits, no Zenodo. Exit 0.
"""
import math

# ---------------------------------------------------------------------------
# constants
G   = 6.674e-11          # m^3 kg^-1 s^-2
c   = 2.99792458e8       # m/s
c2  = c*c
Z   = math.sqrt(32.0*math.pi/3.0)   # 5.78876...
Z2  = Z*Z                            # 33.510... ; 6 Z^2 = 201.06
kappa_t = 0.5            # PINNED bulk tangent stiffness (footing-independent)

def K_eff(a0):           # = a0^2 / (16 pi G)   [Pa]
    return a0*a0/(16.0*math.pi*G)

def rhoL_c2(a0):         # dark-energy rest-energy density = 3(Z a0)^2/(8 pi G) [Pa]
    return 3.0*(Z*a0)**2/(8.0*math.pi*G)

def beta_crit(w_pass_ratio):
    # beta_crit = kappa_t (Q2_scalar/Q2_cassini - 1)/4  -> supplied per footing
    return w_pass_ratio

# ---------------------------------------------------------------------------
# the two footings
FOOT = {
    "canonical  a0=9.36e-11 (rho_DE/cH_Lambda)": dict(a0=9.36e-11, bcrit=0.42),
    "alt        a0=1.13e-10 (rho_tot/cH0)":      dict(a0=1.13e-10, bcrit=0.60),
}

BETA_CAP     = 2.0        # 6 Z^2 mechanical cap (v_T = sqrt(mu_s/rho_L) <= 0.17c)
BETA_NATURAL = 2.0/7.0    # natural-elasticity Poisson value (marginally FAILS Cassini)

# cosmological anchors
MU_OVER_RHO_SW   = 1e-5   # radiation-solid, Sachs-Wolfe-only bound (WRONG epoch for DE)
MU_OVER_RHO_ISW  = 1e-3   # radiation-solid, ISW-relaxed bound     (WRONG epoch for DE)
OMEGA_DE         = 0.69   # DE density fraction today
Z_REC            = 1100.0
OMEGA_M          = 0.31
SLIP_SENS        = 0.10   # current gravitational-slip / E_G sensitivity ~10% (Planck+lensing+RSD, DES/KiDS)

print("="*82)
print("ROUTE A -- cosmological rigidity (shear-modulus) bound on Branch-B beta")
print("="*82)
print(f"Z = sqrt(32pi/3) = {Z:.5f},  Z^2 = {Z2:.4f},  6 Z^2 = {6*Z2:.3f}")
print(f"kappa_t (PINNED) = {kappa_t}")
print()
print("STEP 1 -- the w->-1 singularity of the LITERATURE rigidity (the trap)")
print("-"*82)
print(" Battye-Moss Eq.45:  c_v^2 = mu/(rho+P),  rho+P = rho_L (1+w).")
print(" At w=-1 exactly, rho+P=0  =>  c_v^2 -> INFINITY for any mu>0.")
print(" => mu/(rho+P) is NOT a usable variable here. Use the ABSOLUTE mu_s (Pa),")
print("    i.e. normalize by the MASS density rho_L:   c_v^2/c^2 = mu_s/(rho_L c^2).")
print(" This stays finite and is what the framework's c_v = sqrt(mu_s/rho_L) uses.")
print()

for name, f in FOOT.items():
    a0    = f["a0"]
    bcrit = f["bcrit"]
    Keff  = K_eff(a0)
    rLc2  = rhoL_c2(a0)
    ratio = rLc2/Keff                      # should be 6 Z^2 = 201
    # mu_s(beta) = 3 beta K_eff ;  c_v^2/c^2 = mu_s/(rho_L c^2) = 3 beta/ (6Z^2) = beta/(2Z^2)
    def cv2_over_c2(beta): return 3.0*beta*Keff/rLc2
    inv = ratio/3.0                        # beta/67 :  1/inv = 3/ratio
    print("="*82)
    print(f"FOOTING: {name}")
    print("-"*82)
    print(f" a0            = {a0:.3e} m/s^2")
    print(f" K_eff=a0^2/16piG = {Keff:.4e} Pa")
    print(f" rho_L c^2     = {rLc2:.4e} Pa")
    print(f" rho_L c^2/K_eff = {ratio:.3f}   (must equal 6 Z^2 = {6*Z2:.3f})  [check: {abs(ratio-6*Z2)<1e-6}]")
    print(f" => c_v^2/c^2 = mu_s/(rho_L c^2) = beta/{inv:.2f}   (framework's 'beta/67')")
    print()
    print(f" beta_crit (Cassini pass boundary) = {bcrit}")
    cv2c = cv2_over_c2(bcrit)
    print(f"   at beta_crit:  c_v^2/c^2 = {cv2c:.4e},  c_v/c = {math.sqrt(cv2c):.4f}")
    print(f"   mu_s(beta_crit) = 3*{bcrit}*K_eff = {3*bcrit*Keff:.4e} Pa")
    cv2cap = cv2_over_c2(BETA_CAP)
    print(f" mechanical cap beta=2: c_v^2/c^2 = {cv2cap:.4e}, c_v/c = {math.sqrt(cv2cap):.4f} (=0.17c)")
    cv2nat = cv2_over_c2(BETA_NATURAL)
    print(f" natural beta=2/7={BETA_NATURAL:.3f}: c_v^2/c^2 = {cv2nat:.4e}, c_v/c = {math.sqrt(cv2nat):.4f}")
    print()

    print(" STEP 2 -- adversarial check: NAIVE transfer of the radiation-solid bound")
    print(" "+"-"*70)
    # naive: demand mu_s/(rho_L c^2) <= mu/rho bound  ->  beta <= inv * bound
    beta_max_sw  = inv*MU_OVER_RHO_SW
    beta_max_isw = inv*MU_OVER_RHO_ISW
    print(f"  IF one naively imposes mu_s/(rho_L c^2) <= {MU_OVER_RHO_SW:.0e} (SW):")
    print(f"     beta <= {beta_max_sw:.4f}  << beta_crit={bcrit}  => Cassini FAILS by x{bcrit/beta_max_sw:.0f}")
    print(f"  IF one naively imposes <= {MU_OVER_RHO_ISW:.0e} (ISW-relaxed):")
    print(f"     beta <= {beta_max_isw:.4f}  << beta_crit={bcrit}  => Cassini FAILS by x{bcrit/beta_max_isw:.1f}")
    print("  ==> a NAIVE transfer would CLOSE the door (joint FAIL). But it is ILLEGITIMATE:")
    frac_rec = OMEGA_DE/(OMEGA_DE + OMEGA_M*(1+Z_REC)**3)
    print(f"     that bound is for a RADIATION-LIKE (w=+1/3) solid that is O(1) of the")
    print(f"     energy budget AT RECOMBINATION. A w=-1 DE solid is rho_DE/rho_tot")
    print(f"     = {frac_rec:.2e} of the budget at z={Z_REC:.0f} -> its shear has ~0 effect on")
    print(f"     the primary CMB. The Sachs-Wolfe/early channel simply does not apply.")
    print()

    print(" STEP 3 -- the FAIR (late-time-only) bound: DE shear -> gravitational slip")
    print(" "+"-"*70)
    # the honest observable: DE anisotropic stress modifies the slip eta=Phi/Psi
    # amplitude ~ Omega_DE * mu_s/(rho_L c^2) = Omega_DE * beta/inv  (order of magnitude)
    for label, beta in [("beta_crit", bcrit), ("natural 2/7", BETA_NATURAL), ("cap 2", BETA_CAP)]:
        slip = OMEGA_DE*cv2_over_c2(beta)
        verdict = "BELOW" if slip < SLIP_SENS else "ABOVE"
        print(f"   beta={beta:.3f} ({label:11s}): induced slip ~ Omega_DE*beta/{inv:.0f} = {slip:.3e}"
              f"  -> {verdict} ~{SLIP_SENS:.0%} sensitivity  (x{SLIP_SENS/slip:.0f} margin)")
    # what beta would the fair slip bound actually permit?
    beta_slip_max = SLIP_SENS/OMEGA_DE*inv
    print(f"   => fair slip bound permits beta up to ~{beta_slip_max:.1f}  >> mechanical cap 2")
    print(f"      i.e. the ENTIRE mechanically-allowed window beta in (0,2] is cosmologically OK.")
    print(f"      Planck moreover ADOPTS sigma=0, c_s^2=1 for DE and finds the DE sound speed")
    print(f"      UNCONSTRAINED near w=-1 (perturbations (1+w)-suppressed): no tighter handle.")
    print()

    door = "OPEN" if beta_slip_max > bcrit else "SHUT"
    print(f" VERDICT (this footing): fair cosmological cap on beta ~{beta_slip_max:.1f} > beta_crit={bcrit}")
    print(f"   => Cassini door stays {door}. Cosmology does NOT pin beta, does NOT cap it")
    print(f"      below beta_crit. beta remains a FREE material parameter (shear Poisson ratio).")
    print()

print("="*82)
print("FOOTING-INDEPENDENCE NOTE")
print("-"*82)
print(" The constraining ratio mu_s/(rho_L c^2) = beta/(2Z^2) = beta/67 is IDENTICAL")
print(" on both footings: K_eff ~ a0^2 AND rho_L c^2 ~ a0^2, so a0 cancels. The")
print(" cosmological viability is thus footing-independent; only beta_crit moves")
print(" (0.42 canon -> 0.60 alt), and both sit far below the fair cosmological cap.")
print()
print("="*82)
print("ROUTE A BOTTOM LINE")
print("-"*82)
print(" * The literature rigidity c_v^2=mu/(rho+P) is SINGULAR at w=-1 (the trap);")
print("   the finite physical variable is mu_s/(rho_L c^2) = beta/67.")
print(" * The ONE tight published shear bound (mu/rho<=1e-5..1e-3) is for a")
print("   RADIATION-like solid at recombination and does NOT transfer to w=-1 DE")
print("   (DE is ~1e-9 of the budget then).")
print(" * The FAIR late-time channel (DE anisotropic stress -> gravitational slip)")
print("   gives induced slip ~ 0.4% (beta_crit) to ~2% (cap), all BELOW ~10% current")
print("   sensitivity; Planck leaves the DE sound speed/anisotropic stress")
print("   unconstrained near w=-1.")
print(" * => Route A does NOT pin beta and does NOT cap it below beta_crit.")
print("   Cosmology leaves beta FREE across the whole mechanical window (0,2].")
print("   The Cassini verdict stays HOSTAGE to the unpinned shear Poisson ratio")
print("   (natural beta=2/7=0.286 still marginally FAILS; cosmology neither rescues")
print("   nor kills it). Door OPEN, both footings.")
print("="*82)
