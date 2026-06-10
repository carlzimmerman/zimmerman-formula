#!/usr/bin/env python3
"""
PROBLEM 1 / APPROACH B (DECISIVE) -- Rahman-Susskind CONFINEMENT route to the deep-MOND SIGN.
=============================================================================================
GOAL (from the orchestrator): for a finite-mass backreacting dS probe (conical deficit alpha=m/M_dS),
using the closed q-form (Berkooz 1811.02584 / Lin 2208.07032 / Okuyama diagonal chord op), does the
matter-chord spectral weight ESCAPE to E=0 (CENTER -> p=1/2 -> deep-MOND ENHANCEMENT) or stay
CONFINED at the band edge (-> p<1/2 -> anti-MOND)? Is a galaxy an O(N)-singlet (escapes) or a generic
operator (confined)?

SELF-AUDIT (Fable): watch whether 'the singlet escapes to the center' SMUGGLES the spectral placement
(assumes center=MOND) rather than deriving it. If deconfinement can be answered WITHOUT pre-assuming
where dS sits -> genuine internal closure. If not -> CONTESTED-TERMINAL.

VERBATIM PRIMARY-SOURCE GROUNDING (fetched 2026-06-09 from ar5iv):
 [Rahman-Susskind 2401.08555 'Many Temperatures of de Sitter']
   - "Generic cord operators create collections of unbound Fermions which are confined to the
      stretched horizon region. They do not propagate into the bulk of the static patch."
   - "the multi-Fermion operators which create string-like cords which are able to escape the near
      horizon region and propagate deep into the bulk are very special 'singlet' operators."
   - "singlet operators are very rare in the space of all cord operators."
   - DYNAMICAL framing: T_cord ~ J0 is "hot enough to 'melt' cords to their constituent Fermions";
      "Similar things would be true for ... quarks and gluons in a hot QCD plasma."
   - **CRITICAL (the smoking gun for the self-audit):** the paper makes NO statement about WHERE in
      the ENERGY spectrum (E=0 center vs edge) the escaped singlets sit, and NO connection between
      deconfinement and the spectral center. 'Bulk center / pode' is a SPATIAL location in the static
      patch; 'spectral center E=0' is an ENERGY location. They are NOT the same object.

 [Rahman-Susskind 2312.04097 'conical defects']
   - (1 - alpha/2pi) = sqrt(1 - 8 G M)   [eq A.133];  small M: alpha ~ 8 pi G M.
   - pi v = pi - 2 theta  [eq 5.85];  v ~ p*alpha for small alpha  [eq 7.108]; p = locality parameter,
      ell_string/ell_cosmic ~ 1/p  [eq 3.32].  p ~ sqrt(lambda N) -> infinity in the double-scaled limit.
   - "states with finite backreaction migrate toward v=1, i.e., towards the EDGE of the energy
      spectrum, likely into the non-Gaussian tails."

The discriminator p (freezing exponent) is ALREADY SETTLED in the repo and reproduced here:
   spectral CENTER (flat DOS, local power s=0) -> p=1/2 -> g_obs=sqrt(g_bar a0) -> deep-MOND ENHANCEMENT.
   spectral EDGE   (sqrt DOS, s=1/2)           -> p=2/5 -> sub-linear -> anti-MOND.
So the SIGN reduces entirely to: does a finite-mass backreacting probe land its spectral weight at
E=0 or at the edge? That is what this script computes, two ways, on its own terms.
"""
import numpy as np
import sympy as sp

# --------------------------------------------------------------------------- physical constants
c = 2.998e8; G = 6.674e-11; Msun = 1.989e30
H0 = 67.0e3 / 3.086e22; OmegaL = 0.685
H_Lambda = H0 * np.sqrt(OmegaL)              # de Sitter rate c sqrt(Lambda/3)
M_dS = c**2 / (G * H_Lambda) / Msun          # de Sitter mass in Msun
a0 = 9.36e-11; Z = np.sqrt(32 * np.pi / 3)

NPOCH = 800
def qpoch(a, q, N=NPOCH):
    a = np.asarray(a, dtype=complex); out = np.ones(a.shape, dtype=complex); qk = 1.0
    for _ in range(N):
        out *= (1 - a * qk); qk *= q
    return out

def mu_qg(theta, q):
    qq = qpoch(q, q).real; e2 = np.exp(2j * theta)
    return qq * (qpoch(e2, q) * qpoch(np.conj(e2), q)).real / (2 * np.pi)

def G_amp(th1, th2, Delta, q):
    num = qpoch(q ** (2 * Delta), q)
    th1 = np.asarray(th1, float); th2 = np.asarray(th2, float)
    shape = np.broadcast(th1, th2).shape; den = np.ones(shape, complex)
    for s1 in (1, -1):
        for s2 in (1, -1):
            den *= qpoch(q ** Delta * np.exp(1j * (s1 * th1 + s2 * th2)), q)
    return num / den

def spectral_weight(theta_E, theta_vac, Delta, q):
    return mu_qg(theta_E, q) * np.abs(G_amp(theta_E, theta_vac, Delta, q)) ** 2


# ===========================================================================================
# STEP 0 -- the deficit->energy placement map (2312.04097), exact, with the p blueshift sting
# ===========================================================================================
def step0_placement():
    print("="*100)
    print("STEP 0 -- conical-deficit ENERGY placement v = p*alpha (Rahman-Susskind 2312.04097)")
    print("="*100)
    M, GG = sp.symbols('M G', positive=True)
    alpha_exact = 2*sp.pi*(1 - sp.sqrt(1 - 8*GG*M))
    alpha_small = sp.series(alpha_exact, M, 0, 2).removeO()
    print(f"  alpha(M) = {alpha_exact};  small-M: alpha ~ {alpha_small}  (= 8 pi G M) [matches eq 7.105]")
    print(f"  M_dS = c^2/(G H_Lambda) = {M_dS:.3e} Msun.  alpha/2pi = M/M_dS (small M).")
    print(f"  E/E0 = cos(theta) = sin((pi/2) v),  v = p*alpha.  CENTER: v->0 (E=0); EDGE: v->1.\n")
    print(f"  {'object':>13}{'M(Msun)':>10}{'alpha=2pi M/M_dS':>18}{'v(p=1)':>10}{'E/E0(p=1)':>11}"
          f"{'v(p=1e6)':>11}{'E/E0(p=1e6)':>13}")
    rows = [("dwarf",1e7),("spiral",3e10),("MW",1e11),("massive gal",1e12),
            ("group",1e13),("cluster",1e15)]
    out = {}
    for nm, Mv in rows:
        alpha = 2*np.pi*(Mv/Msun if False else Mv)/M_dS   # Mv already in Msun, M_dS in Msun
        alpha = 2*np.pi*Mv/M_dS
        def EoE0(p):
            v = min(p*alpha, 1.0); return np.sin(0.5*np.pi*v)
        out[nm] = (alpha, EoE0(1.0), EoE0(1e6))
        print(f"  {nm:>13}{Mv:>10.0e}{alpha:>18.3e}{min(alpha,1):>10.3e}{EoE0(1.0):>11.3e}"
              f"{min(1e6*alpha,1):>11.3e}{EoE0(1e6):>13.3e}")
    print("""
  READ: at p=1 (semiclassical book-keeping, NO double-scale blueshift) galaxies sit at E/E0 ~ 1e-6..1e-3
  -> CENTER -> MOND. But the PHYSICAL de Sitter limit IS the double-scaled limit, p ~ sqrt(lambda N) -> inf,
  and 2312.04097 says explicitly 'states with finite backreaction migrate toward v=1 ... the EDGE.' At p=1e6
  even a galaxy is blueshifted to the edge. SO STEP 0 ALONE IS p-DEPENDENT AND DOES NOT DECIDE.""")
    return out


# ===========================================================================================
# STEP 1 -- the diagonal kernel TRANSPORTS but does NOT pick the placement (reproduce + sharpen)
# ===========================================================================================
def step1_kernel_transports():
    print("="*100)
    print("STEP 1 -- the matter chord (diagonal q^{Delta N}) keeps weight at its SOURCE; reproduce")
    print("="*100)
    th = np.linspace(1e-4, np.pi-1e-4, 200001)
    print(f"  {'q':>5}{'Delta':>6} | {'CENTER-src frac|E|<.05':>23}{'meanE':>8} | "
          f"{'EDGE-src frac|E|>.95':>21}{'meanE':>8}")
    for q in (0.5, 0.7, 0.9, 0.95):
        for Delta in (0.5, 1.0):
            Wc = spectral_weight(th, np.pi/2, Delta, q)        # center source
            We = spectral_weight(th, np.pi-1e-3, Delta, q)     # edge source
            E = np.cos(th)
            def frac(W, mask):
                tot = np.trapz(W, th); return np.trapz(W*mask, th)/tot, np.trapz(W*np.abs(E),th)/tot
            fc, mc = frac(Wc, np.abs(E)<0.05)
            fe, me = frac(We, np.abs(E)>0.95)
            print(f"  {q:>5.2f}{Delta:>6.2f} | {fc:>23.3f}{mc:>8.3f} | {fe:>21.3f}{me:>8.3f}")
    print("""  READ: a center-sourced probe keeps weight at E=0; an edge-sourced probe keeps weight at the
  edge. The kernel is diagonal-dominant (semiclassical q): it TRANSPORTS the source, it does NOT pick
  the source. -> the SIGN rides entirely on the SOURCE PLACEMENT (Step 0), which the algebra abstains on.""")


# ===========================================================================================
# STEP 2 -- THE SELF-AUDIT: does 'singlet escapes to the center' smuggle the spectral placement?
#           Disambiguate SPATIAL bulk (deconfinement) from SPECTRAL center (E=0).
# ===========================================================================================
def step2_spatial_vs_spectral():
    print("="*100)
    print("STEP 2 -- SELF-AUDIT: spatial 'bulk center/pode' (deconfinement) vs spectral 'center E=0'")
    print("="*100)
    print("""  Rahman-Susskind 2401.08555 (confinement) says: GENERIC cords are CONFINED to the stretched
  horizon; only O(N)-SINGLETS ESCAPE to the BULK (the pode = the SPATIAL center of the static patch).
  This is a DYNAMICAL statement (T_cord melting, QCD-plasma analogy) -- GOOD, it is not a placement choice.

  BUT: 'escape to the bulk (pode)' is a statement about the SPATIAL/geodesic position in the static patch.
  The deep-MOND SIGN needs the ENERGY (spectral) position E=0. These are DIFFERENT axes:
     - chord number n ~ geodesic LENGTH ~ DEPTH into the bulk (spatial).
     - energy E = (2/sqrt(1-q)) cos(theta) ~ position in the SPECTRUM (energy).
  The bulk pode (deepest geodesic, n LARGE) is NOT the spectral center (E=0). In fact:""")

    # Demonstrate: a DEEP bulk chord (large n) is NOT spectrally central. Build chord-number n states'
    # spectral weight w(E)=|<E|n>|^2 and show where each n lives in energy.
    from scipy.linalg import eigh_tridiagonal
    print(f"\n  Spectral location of a chord-number-n state (n ~ bulk depth): peak |E/E0| of |<E|n>|^2")
    print(f"  {'q':>5} | " + "".join(f"n={n:<6}" for n in (0,1,2,5,10,20,40)))
    for q in (0.7, 0.9, 0.95):
        Nm = 3000
        ns = np.arange(1, Nm)
        b = np.sqrt((1-q**ns)/(1-q))
        E, V = eigh_tridiagonal(np.zeros(Nm), b)
        E0 = 2/np.sqrt(1-q); x = E/E0
        row = f"  {q:>5.2f} | "
        for n in (0,1,2,5,10,20,40):
            w = V[n,:]**2
            peak = abs(x[np.argmax(w)])
            row += f"{peak:<8.3f}"
        print(row)
    print("""  READ: n=0 (zero-length chord = AT the horizon, NOT the bulk pode) peaks at the spectral CENTER
  (|E/E0|~0). As n grows (deeper geodesic into the bulk), the peak MOVES TOWARD THE EDGE (|E/E0|->1).
  ==> THE SPATIAL BULK CENTER (large n, the pode) IS THE SPECTRAL EDGE. The horizon (n=0) IS the
  spectral center. These two 'centers' are OPPOSITE ENDS of both axes.

  THEREFORE the claim 'an O(N)-singlet escapes to the bulk center, hence sits at the spectral center E=0,
  hence deep-MOND' is a NON-SEQUITUR: escaping to the spatial bulk pode (large geodesic depth) places the
  excitation at the spectral EDGE, NOT E=0. The deep-MOND sign needs E=0, which corresponds to the
  near-HORIZON (n~0) limit -- exactly the strict empty-ensemble / Unruh-floor limit, NOT a propagating
  bulk particle. The confinement result does NOT deliver the spectral center for a bulk-propagating probe.""")


# ===========================================================================================
# STEP 3 -- can the DECONFINEMENT (escape) question be answered WITHOUT assuming the placement?
#           A dynamical melting/escape criterion (T_cord vs probe energy), independent of E-placement.
# ===========================================================================================
def step3_dynamical_deconfinement():
    print("="*100)
    print("STEP 3 -- DYNAMICAL deconfinement: is a galaxy a SINGLET that escapes? (no placement assumed)")
    print("="*100)
    print("""  R-S melting criterion: a cord survives as a coherent bulk excitation (escapes confinement) iff it
  is an O(N)-SINGLET; generic cords melt in the T_cord ~ J0 plasma. The escape condition is a SYMMETRY
  (singlet) condition, evaluated WITHOUT reference to where the cord sits in the spectrum. So we CAN ask
  'is a galaxy a singlet?' independent of placement -- this is the part that is genuinely a dynamical
  (deconfinement) question, exactly as the orchestrator hoped.

  IS A GALAXY A SINGLET?  -- both ways, and the singlet RARITY quantified.""")
    # Singlet fraction: degree-k cord operators ~ C(N,k); O(N)-singlet subspace dim is O(1) for fixed k.
    print(f"  {'N':>6}{'#bilinear ops ~C(N,2)':>22}{'#singlets O(1)':>16}{'singlet fraction':>18}")
    for Nf in (64, 256, 1024, 4096):
        n_ops = Nf*(Nf-1)//2 + Nf; n_sing = 1
        print(f"  {Nf:>6}{n_ops:>22}{n_sing:>16}{n_sing/n_ops:>18.2e}")
    print("""    => singlet fraction -> 0 as 1/N^2. A GENERICALLY constructed cord is NON-singlet -> melts -> confined.

  TWO PHYSICAL READINGS, GENUINELY DIFFERENT (this is where the deconfinement question lives):
    (R1) 'a galaxy = the literal matter CHORD the kernel inserts (q^{Delta N})':  a single matter-cord
         crossing is a GENERIC (non-singlet) operator -> CONFINED to the stretched horizon -> melts.
         R-S: generic cords 'do not propagate into the bulk.'  This reading -> the probe never even
         becomes a coherent bulk object.  [framework's ENEMY at the deconfinement step itself]
    (R2) 'a galaxy = a bulk-propagating, gauge-invariant lump of matter we OBSERVE freely-falling':
         by definition a thing that propagates in the bulk = the O(N)-SINGLET sector that escapes.
         A real galaxy demonstrably propagates -> it IS (in this dictionary) a singlet -> escapes.
         [framework's FRIEND at the deconfinement step] -- BUT see Step 2: escaping to the spatial bulk
         (pode, large n) puts it at the spectral EDGE, not E=0. So even R2 does NOT yield deep-MOND
         unless we ALSO assume the probe sits at E=0 -- which re-imports the placement (the smuggle).

  ==> The deconfinement (singlet/escape) question CAN be posed independently (R1 vs R2 is a real,
  symmetry-level fork). But NEITHER branch delivers the deep-MOND sign by itself:
     - R1 (generic chord): confined -> not even a bulk particle -> the deep-MOND derivation has no probe.
     - R2 (singlet, escapes to spatial bulk pode): lands at the spectral EDGE (Step 2) -> p<1/2 -> anti-MOND,
       UNLESS one separately asserts the probe sits at E=0 (the strict near-horizon n~0 limit), which is the
       SAME placement posit the confinement route was supposed to REPLACE.""")


def main():
    print("#"*100)
    print("# APPROACH B DECISIVE -- Rahman-Susskind confinement route to the deep-MOND sign")
    print(f"#   a0={a0:.3e}  Z={Z:.4f}  H_Lambda={H_Lambda:.3e}/s  M_dS={M_dS:.3e} Msun")
    print("#"*100 + "\n")
    step0_placement()
    print()
    step1_kernel_transports()
    print()
    step2_spatial_vs_spectral()
    print()
    step3_dynamical_deconfinement()
    print("\n" + "="*100)
    print("VERDICT (both ways, self-audited)")
    print("="*100)
    print("""  The orchestrator's hope: deconfinement is a DYNAMICAL question, so it might answer center-vs-edge
  WITHOUT pre-assuming where dS sits. RESULT: the deconfinement (singlet/escape) question IS genuinely
  dynamical and CAN be posed without placement -- BUT it does not close the sign, for two compounding reasons:

  1. SMUGGLE CAUGHT (Fable self-audit fires). 'Singlet escapes to the CENTER' conflates the SPATIAL bulk
     center (pode, the deepest geodesic, chord number n LARGE) with the SPECTRAL center (E=0). Step 2 shows
     these are OPPOSITE: the spatial bulk pode maps to the spectral EDGE; the spectral center E=0 is the
     near-HORIZON n~0 limit. So 'escapes to the bulk' does NOT mean 'sits at E=0'. The statement that would
     give deep-MOND ('the escaped singlet sits at the spectral center') is NOT in Rahman-Susskind and is a
     non-sequitur -- it re-assumes center=MOND rather than deriving it.

  2. EVEN GRANTING ESCAPE, the placement is re-imported. The only way to land the escaped probe at E=0 is
     the strict near-horizon / vanishing-backreaction / empty-Unruh-floor limit -- which is the same
     placement POSIT (de Sitter = spectral center) the confinement route was meant to derive from below.
     2312.04097's own blueshift (v=p*alpha, p->inf) pushes any FINITE backreaction to the EDGE.

  CONCLUSION: APPROACH B does NOT yield a genuine internal closure. The deconfinement question is real and
  dynamical, but it decides SPATIAL escape, not SPECTRAL placement; the deep-MOND sign needs the spectral
  center E=0, and reaching it still requires the contested de-Sitter-=-center placement (or the strict
  horizon limit). On the literal-chord reading the probe is CONFINED (anti-MOND or no-probe); on the
  observed-galaxy reading it escapes to the spatial bulk = spectral EDGE (anti-MOND) unless the placement
  posit is re-added. => CONTESTED-TERMINAL: undecidable within DSSYK without the external dS-placement
  dictionary. LEANING: against a free internal closure (the favorable route requires re-smuggling center=MOND).""")


if __name__ == "__main__":
    main()
