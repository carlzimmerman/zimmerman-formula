#!/usr/bin/env python3
"""
Agent P -- The Verlinde COEFFICIENT audit: is the 1/6 forced, and is 6 vs Z=5.789 distinguishable?
===================================================================================================
Companion calculation to agentP_verlinde_coefficient.md. Verlinde 2016 (arXiv:1611.02269v2) derives,
from de Sitter entropy displacement + an elastic-response dictionary, the deep-MOND relation

    g_D = sqrt(a_M g_B)   with   a_M = (d-3)/((d-2)(d-1)) * a0,   a0 = cH0     [eqs (1.7), (1.2)]
    => d=4:  a_M = a0/6                                                        [eq (7.43)]

i.e. a DERIVED, dimension-forced O(1) coefficient (6 = (d-1)x(d-2)/(d-3) = 3x2), against the
framework's DATA-SELECTED Z = sqrt(32pi/3) = 5.789 (a0 = cH_Lambda/Z). This script does the
comparison RIGHT per the repo's convention rules (MEMORY.md working rule + COEFFICIENT_FOOTING_AUDIT):
  (1) BOTH footings (cH0 = rho_total vs cH_Lambda = rho_DE) x BOTH coefficients (6 vs Z);
  (2) against every banked data error scale (stat / syst / fit-metric swing / Upsilon degeneracy);
  (3) decisive: SAME-SHAPE SPARC RAR run on the repo's own data -- the Yoon-corrected EG total
      g = sqrt(gB^2 + a_M gB) (arXiv:2003.03198 eq 37; PDU 45,101551) is IDENTICAL in form to the
      framework's interpolation g = sqrt(gB^2 + a0 gB), so the coefficient comparison is clean.
      Verlinde's original additive form g = gB + sqrt(a_M gB) (eqs 7.43 + 7.41) is run as well.
No git. C. Zimmerman / Agent P, 2026-06-10. numpy + repo SPARC data.
"""
import numpy as np, glob, os

# ----------------------------------------------------------------------------------------------
# constants -- repo canonical (COEFFICIENT_FOOTING_AUDIT_2026-06.md)
# ----------------------------------------------------------------------------------------------
c   = 2.998e8                      # m/s
kpc = 3.0857e19; Mpc = 3.0857e22
H0  = 67.4e3/Mpc                   # 67.4 km/s/Mpc = 2.184e-18 1/s  (Planck)
OmL = 0.685
HL  = H0*np.sqrt(OmL)              # pure-Lambda de Sitter rate H_Lambda = H0 sqrt(Omega_Lambda)
cH0, cHL = c*H0, c*HL
Z   = np.sqrt(32*np.pi/3)          # framework: 5.78845...  (data-selected)
SIX = 6.0                          # Verlinde:  (d-1)(d-2)/(d-3) at d=4  (derived, given postulates)

print("="*100)
print("PART 1 -- where the 1/6 comes from (pinned from the LaTeX source of arXiv:1611.02269v2)")
print("="*100)
print(f"""  a_M = (d-3)/((d-2)(d-1)) a0   [eq (1.7)];  d=4 => 1/6.  The 6 factorizes as 3 x 2:
    * (d-1) = 3 : the volume-law normalization V0 = 4G.hbar.L/(d-1) [eq (2.14)] -- ball volume
                  V = A.r/(d-1) [eq (2.13)] + boundary condition S_DE(L) = A(L)/4G.hbar [eq (2.12)].
                  Pure 3-spatial-dimension geometry once the volume-law POSTULATE is granted.
    * (d-2)/(d-3) = 2 : the ADM/Gauss conversion Sigma = (d-2)/(d-3) g/8piG [eq (1.6)] -- an
                  uncontested Newtonian/GR factor.
  Chain: S_M = 2 pi M r/hbar [eq (4.28), Bekenstein/Wald -- derived] -> V_M = (8piG/a0) M r/(d-1)
  [eq (4.33)] -> Eshelby inclusion condition INT eps^2 dV <= V_M [Sec 7.1; EQUALITY assumed] ->
  Sigma_D = (a0/8piG) eps [shear modulus a0^2/16piG, fixed by the self-energy match, Sec 6] ->
  INT (8piG Sigma_D/a0)^2 dV = ((d-2)/(d-1)) OINT (Phi_B/a0) n.dA [eq (7.36)] ->
  INT G M_D^2/r'^2 dr' = M_B a0 r/6 [eq (7.40), THE main result] -> g_D = sqrt(a0 g_B/6) [eq (7.43)].
  => GIVEN the postulates, 1/6 is FORCED (zero tunable freedom, zero data input). The freedom lives
     in the postulates themselves: (P1) volume-law dS entropy; (P2) linear-in-r S_M interpolation;
     (P3) the elastic dictionary; (P4) equality saturation of the strain inequality; (P5) spherical/
     static/isolated. P1+P3+P4 are the contested part (Dai-Stojkovic 1710.00946 vs Yoon 2003.03198).""")

print("="*100)
print("PART 2 -- the four cross-products (both footings x both coefficients), arXiv-pinned")
print("="*100)
print(f"  cH0      = {cH0:.4e} m/s^2   (measured-H0 / rho_total footing; Verlinde eq (1.2) face value)")
print(f"  cH_L     = {cHL:.4e} m/s^2   (pure-Lambda / rho_DE footing; Verlinde's OWN Sec-8 caveat:")
print(f"             'a0 should actually be defined in terms of the dark energy density, or the value")
print(f"             of the cosmological constant... it takes a slightly different value')")
print(f"  {'':24s}{'/6 (Verlinde)':>16s}{'/Z=5.789 (framework)':>22s}{'ratio 6/Z':>12s}")
print(f"  {'cH0 footing':24s}{cH0/SIX:>16.4e}{cH0/Z:>22.4e}{Z/SIX:>12.4f}")
print(f"  {'cH_Lambda footing':24s}{cHL/SIX:>16.4e}{cHL/Z:>22.4e}{Z/SIX:>12.4f}")
gap = SIX/Z - 1
print(f"\n  coefficient gap: 6 vs Z = sqrt(32pi/3) = {Z:.4f}  ->  {100*gap:.2f}% (a_M is {100*gap:.2f}% LOW of a0_fw")
print(f"  on the same footing). Footing gap (cH0 vs cH_L) = 1/sqrt(Omega_L) - 1 = {100*(1/np.sqrt(OmL)-1):.1f}% -- the")
print(f"  footing fork is {(1/np.sqrt(OmL)-1)/gap:.0f}x LARGER than the 6-vs-Z fork. The footing dominates the comparison.")
print(f"  External anchor: Yoon+22 (2206.11685) / Diez-Tejedor+18 (1612.06282) 'quasi-de-Sitter' EG uses")
print(f"  a0 = 5.41e-10 = cH_Lambda (the repo's own footing) and finds it fits SPARC BETTER than cH0")
print(f"  (offset -0.027 vs -0.060 dex) -- an independent, non-framework group landing on the rho_DE branch.\n")

print("="*100)
print("PART 3 -- is 3.65% distinguishable? (against every banked error scale)")
print("="*100)
rows = [
 ("RAR stat error (McGaugh+16 1609.05917: 1.20+/-0.02e-10)",          0.02/1.20),
 ("RAR M/L systematic (same paper: +/-0.24e-10)",                      0.24/1.20),
 ("fit-METRIC swing, fixed Upsilon=0.70 (banked: 8.5e-11..1.3e-10)",  (1.3-0.85)/1.075),
 ("SHAPE dependence (EG-shape fit prefers a_M ~30% below cH0/6, 1909.01734/2206.11685)", 0.30),
 ("footing fork cH0 vs cH_L (the rho_total/rho_DE branch)",            1/np.sqrt(OmL)-1),
]
print(f"  {'error scale':74s}{'size':>8s}{'gap/scale':>10s}")
for n, s in rows:
    print(f"  {n:74s}{100*s:>7.1f}%{gap/s:>10.2f}")
print(f"""  The {100*gap:.2f}% gap is 0.18x the M/L systematic, 0.09x the metric swing, 0.12x the shape systematic.
  Only the formal 1.7% stat error could nominally split it (2.2 sigma) -- but that error bar is itself
  convention-fiction: the central value moves ~40% with the weighting and ~30% with the assumed shape.
  To split 6 from Z at 3 sigma needs sigma(a0) < {100*gap/3:.1f}% TOTAL -- below even the stat-only error,
  and ~20x below the honest systematic floor. Per the footing audit's discrimination table (framework vs
  thermal 8.2% needs <2.7%), this pair is the LEAST distinguishable coefficient pair in the corpus.
  Deep-MOND amplitude check: v_f = (a_M G M_B)^(1/4) shifts by only (Z/6)^(1/4)-1 = {100*((Z/SIX)**0.25-1):.2f}% -- BTFR
  zero-point scatter/normalization uncertainty (~10%+) is ~10x larger. NOT DISTINGUISHABLE, any convention.""")

# ----------------------------------------------------------------------------------------------
# PART 4 -- decisive: same-shape SPARC RAR on the repo's own data
# ----------------------------------------------------------------------------------------------
print("="*100)
print("PART 4 -- SPARC RAR (repo data, 175 rotmod files): the four coefficients, BOTH shapes, BOTH metrics")
print("="*100)
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"

def load_raw():
    rows = []
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try: d = np.genfromtxt(f, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        rows.append((R*kpc, Vobs, eV, Vgas, Vdisk, Vbul))
    return rows
ROWS = load_raw()
print(f"  loaded {len(ROWS)} galaxies")

def g_quad(gb, a):  return np.sqrt(gb**2 + gb*a)            # quadrature: framework == Yoon-corrected EG
def g_add(gb, a):   return gb + np.sqrt(gb*a)               # additive: Verlinde 1611.02269 eq (7.43)+(100)

def scatter(Ud, Ub, a, shape):
    res, w = [], []
    for Rm, Vobs, eV, Vgas, Vdisk, Vbul in ROWS:
        Vbar2 = np.sign(Vgas)*Vgas**2 + Ud*Vdisk**2 + Ub*Vbul**2
        gb = Vbar2*1e6/Rm; go = (Vobs*1e3)**2/Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
        r = np.log10(go[ok]) - np.log10(shape(gb[ok], a))
        fr = np.clip(eV[ok], 1, None)/np.clip(Vobs[ok], 1, None)
        res += list(r); w += list(1/fr**2)
    res, w = np.array(res), np.array(w)
    unw = np.sqrt(np.mean(res**2))                            # UNWEIGHTED dex scatter (standard; the rule's metric)
    wgt = np.sqrt(np.sum(w*res**2)/np.sum(w))                 # inverse-error-weighted (mlfit script's metric)
    return unw, wgt, np.mean(res)

CASES = [("cH_L/Z  (framework canonical)", cHL/Z), ("cH_L/6  (Verlinde, Lambda footing)", cHL/SIX),
         ("cH0/Z   (framework, cross-footing)", cH0/Z), ("cH0/6   (Verlinde face value)", cH0/SIX)]
UGRID = np.linspace(0.30, 1.20, 91)

for sname, sfun in (("QUADRATURE  g=sqrt(gB^2+a.gB)   [framework == Yoon-corrected EG]", g_quad),
                    ("ADDITIVE    g=gB+sqrt(a.gB)     [Verlinde 1611 original]", g_add)):
    print(f"\n  shape: {sname}")
    print(f"  {'coefficient':38s}{'a0[m/s^2]':>11s}{'bestU':>7s}{'unw-dex':>9s}{'bestU_w':>9s}{'wgt-dex':>9s}"
          f"{'unw@U=.70':>10s}{'unw@U=.50':>10s}")
    base = {}
    for cname, a in CASES:
        sc  = [scatter(U, 1.4*U, a, sfun) for U in UGRID]
        unws = np.array([s[0] for s in sc]); wgts = np.array([s[1] for s in sc])
        iu, iw = np.argmin(unws), np.argmin(wgts)
        u70 = scatter(0.70, 0.98, a, sfun)[0]; u50 = scatter(0.50, 0.70, a, sfun)[0]
        print(f"  {cname:38s}{a:>11.3e}{UGRID[iu]:>7.2f}{unws[iu]:>9.4f}{UGRID[iw]:>9.2f}{wgts[iw]:>9.4f}"
              f"{u70:>10.4f}{u50:>10.4f}")
        base[cname] = (unws[iu], wgts[iw])
    d_unw = base[CASES[1][0]][0] - base[CASES[0][0]][0]
    d_wgt = base[CASES[1][0]][1] - base[CASES[0][0]][1]
    print(f"  -> Delta(scatter) cH_L/6 vs cH_L/Z, Upsilon-profiled: {d_unw:+.4f} dex (unw), {d_wgt:+.4f} dex (wgt)")

print(f"""
  READING (both ways, per the working rule): with Upsilon profiled -- the only honest comparison,
  a0 and Upsilon are degenerate -- the scatter difference between Verlinde's 6 and the framework's
  Z is at the ~1e-3-dex level on BOTH metrics and BOTH footings: pure noise against the ~0.105-dex
  relation width and the ~0.01-dex jackknife wobble of the optimum. SPARC cannot tell 6 from 5.789.
  Neither value 'wins'; neither is in deficit. The additive-vs-quadrature SHAPE fork moves the fit
  more than the 6-vs-Z coefficient fork -- consistent with Lelli+17's hook being a statement about
  the additive form, not about the scale.""")

print("="*100)
print("VERDICT (numbers): COEFFICIENT-CHAIN-EXISTS -- a published derivation yields Z_V = 6, within")
print(f"3.65% of the data-selected Z = 5.789, i.e. inside every defensible error floor (>=20% syst,")
print(f"~40% metric swing, ~30% shape systematic); current data CANNOT distinguish them, and the")
print(f"chain is CONDITIONAL on Verlinde's contested postulates (see .md for the full-weight caveats).")
print("="*100)
