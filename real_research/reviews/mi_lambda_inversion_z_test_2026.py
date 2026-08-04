#!/usr/bin/env python3
r"""mi_lambda_inversion_z_test_2026.py -- DOOR 2: does the Lambda-inversion ever TEST Z?

A0LINE_LAMBDA_2026.md inverts a galactically measured a0 through Lambda = 3 Z^2 a0^2/c^4 and
recovers Planck's Lambda to a factor ~2, then disclaims: "not a test of the postulated
normalization Z, which appears on both sides."  This file decides whether that disclaimer is a
THEOREM or a FRAMING ARTEFACT, and prices the door either way.

  S1  the algebra, in sympy: kappa is an INVERTIBLE function of (a0, Lambda) alone
  S2  the circularity question, settled by injectivity + by reproducing the paper's own identity
  S3  the H0 CONSISTENCY AUDIT on real SPARC -- the one place cosmology DOES enter the galactic side
  S4  "the squaring helps" -- tested, and it is FALSE (reparametrisation invariance)
  S5  what the cosmological side actually costs, and the sigma(a0) a 3-sigma kappa test needs
  S6  the w0-wa complication, three separate effects, priced
  S7  the footing fork: is the kappa question even well posed?  and is the 4-way ladder identified?
  S8  the assembled budget and the verdict

NOT redone here (read those files instead): the shape systematic and the 14.2% N-independent floor
(mi_routeA_shape_invariant_a0_2026.py), the BTFR finite-radius Q x Gamma pricing (ibid. S9), the
one-sided H0=73 distance-scale systematic (ibid. S10d).  This file consumes those numbers and adds
the two-sided, correlated treatment that the Lambda inversion specifically requires.

a0 is an INPUT on both footings.  Nothing here is fitted to improve a framework prediction.
"""
import math
import os
import sys
import csv
import glob
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)                      # .../real_research
if HERE not in sys.path:
    sys.path.insert(0, HERE)
# constants imported, not re-declared, so the round-trip against the committed A0_CANON is exact
from mi_route_a_kernel import (A0_CANON, A0_ALT, A0_M20, Z_FW,  # noqa: E402
                              C_L, G_N, H0 as H0_SI, OM_L as OMEGA_L_P)

KPC = 3.0857e19
TWO_PI = 2.0 * math.pi

_nchk = [0, 0]


def check(cond, msg):
    _nchk[1] += 1
    if cond:
        _nchk[0] += 1
        print(f"  [OK] {msg}")
    else:
        print(f"  [FAIL] {msg}")
        print(f"\n  {_nchk[0]}/{_nchk[1]} checks held -- FAILING.")
        sys.exit(1)


def banner(t):
    print("\n" + "=" * 110 + f"\n  {t}\n" + "=" * 110)


# ----------------------------------------------------------------------------------------------
banner("S1  THE ALGEBRA -- kappa is a function of (a0, Lambda) ALONE")

a0s, lam, kap, c_, G_ = sp.symbols("a0 Lambda kappa c G", positive=True)
# framework premise: a0 = kappa c sqrt(G rho_Lambda),  rho_Lambda = Lambda c^2/(8 pi G)
rho_of_lam = lam * c_**2 / (8 * sp.pi * G_)
a0_fwd = kap * c_ * sp.sqrt(G_ * rho_of_lam)                      # = kappa c^2 sqrt(Lambda/(8 pi))
kap_inv = sp.solve(sp.Eq(a0s, a0_fwd), kap)[0]                    # kappa = ...
lam_inv = sp.solve(sp.Eq(a0s, a0_fwd), lam)[0]                    # Lambda = ...
resid_k = sp.simplify(kap_inv - a0s * sp.sqrt(8 * sp.pi / lam) / c_**2)
resid_l = sp.simplify(lam_inv - 8 * sp.pi * a0s**2 / (kap**2 * c_**4))
resid_Z = sp.simplify(lam_inv.subs(kap, sp.sqrt(8 * sp.pi / 3) / sp.Symbol("Zsym", positive=True))
                      - 3 * sp.Symbol("Zsym", positive=True)**2 * a0s**2 / c_**4)
print("  premise      a0 = kappa c sqrt(G rho_Lambda),   rho_Lambda = Lambda c^2/(8 pi G)")
print(f"  inverted     kappa  = (a0/c^2) sqrt(8 pi / Lambda)        [residual {resid_k}]")
print(f"               Lambda = 8 pi a0^2/(kappa^2 c^4) = 3 Z^2 a0^2/c^4,  Z = sqrt(8pi/3)/kappa")
check(resid_k == 0 and resid_l == 0 and resid_Z == 0,
      "S1a the inversion is exact and Z-free in form: kappa = (a0/c^2) sqrt(8 pi/Lambda) contains NO "
      "assumed normalisation -- Z enters only as a RELABELLING of kappa, Z = sqrt(8pi/3)/kappa")

Z_canon = 2.0 * math.sqrt(8 * math.pi / 3.0)
kap_canon, kap_M20 = 0.5, math.sqrt(8 * math.pi / 3.0) / TWO_PI
# the COSMOLOGICAL side, built from cosmology only (Planck 2018 LCDM), never from a0
H0_P, OMEGA_M_P = 67.36, 0.315
LAM_PLANCK = 3.0 * OMEGA_L_P * H0_SI**2 / C_L**2
print(f"  Z(kappa=1/2) = {Z_canon:.6f} = Z_FW {Z_FW:.6f};   Milgrom's Z = 2pi = {TWO_PI:.6f}")
print(f"  Lambda(Planck LCDM, cosmology only) = {LAM_PLANCK:.4e} m^-2  (published 1.089e-52)")
print(f"  ** LABEL WARNING for the lane brief. Three conventions name the SAME two hypotheses:")
print(f"     a0 = kappa c sqrt(G rho_L) : canonical kappa = {kap_canon:.5f}, Milgrom {kap_M20:.5f}")
print(f"     a0 = k' c H_Lambda         : canonical k' = {1/Z_FW:.5f}, Milgrom 1/(2pi) = {1/TWO_PI:.5f}")
print(f"     a0 = c H_Lambda / Z        : canonical Z = {Z_FW:.5f}, Milgrom 2pi = {TWO_PI:.5f}")
print(f"     '1/2' and '1/2pi' are from DIFFERENT columns; the ratio is 1/Z either way, so the a0 gap")
print(f"     is the same {100*(1-A0_M20/A0_CANON):.2f}% and a0(Milgrom) = {A0_M20:.4e}.")
GAP_LOG = math.log(A0_CANON / A0_M20)
need3_naive = GAP_LOG / 3.0
check(abs(Z_canon - Z_FW) < 1e-12 and abs(A0_M20 / A0_CANON - Z_FW / TWO_PI) < 1e-12
      and abs(GAP_LOG - 0.08195) < 1e-4,
      f"S1b the hypothesis gap is exactly Z_FW/(2pi): {100*(1-A0_M20/A0_CANON):.3f}% of canonical, "
      f"{100*GAP_LOG:.3f}% in the log -- H0- and Omega_Lambda-free")


# ----------------------------------------------------------------------------------------------
banner("S2  IS THE DISCLAIMER A THEOREM OR A FRAMING ARTEFACT?")


def kappa_of(a0_hat, lam_obs):
    """kappa from a galactic a0 and a cosmological Lambda.  No Z, no footing, no kernel."""
    return a0_hat * math.sqrt(8 * math.pi / lam_obs) / C_L**2


# INJECTIVITY: hold the cosmological Lambda fixed, vary the TRUE kappa, recover it.
inj = []
for k_true in (0.10, 0.1592, 0.2588, 0.35, 0.50, 0.75, 1.00):
    a0_true = k_true * C_L * math.sqrt(G_N * LAM_PLANCK * C_L**2 / (8 * math.pi * G_N))
    inj.append(abs(kappa_of(a0_true, LAM_PLANCK) / k_true - 1.0))
print(f"  injectivity at FIXED Lambda over kappa in [0.10, 1.00]: max |recovered/true - 1| = {max(inj):.2e}")
check(max(inj) < 1e-12,
      "S2a the map (a0, Lambda) -> kappa is INJECTIVE at fixed Lambda: different kappa give different a0, "
      "so a galactic a0 confronted with a cosmological Lambda DOES determine kappa. The comparison is not "
      "vacuous, and 'Z appears on both sides' cannot be a theorem")

# the paper's own identity, and what it really is
a0_hat_demo = 1.181e-10                                        # the paper's full-gas GLS central
ratio_lam = (8 * math.pi * a0_hat_demo**2 / (kap_canon**2 * C_L**4)) / LAM_PLANCK
r1 = abs(ratio_lam - (a0_hat_demo / A0_CANON)**2)
r2 = abs(ratio_lam - (kappa_of(a0_hat_demo, LAM_PLANCK) / kap_canon)**2)
print(f"  Lambda_pred/Lambda_Planck = {ratio_lam:.4f};  (a0_hat/a0_canon)^2 residual {r1:.2e};  "
      f"(kappa_hat/0.5)^2 residual {r2:.2e}")
print(f"  kappa_hat from the SAME two numbers = {kappa_of(a0_hat_demo, LAM_PLANCK):.4f}  "
      f"(canonical 0.5, Milgrom {kap_M20:.4f})")
check(r1 < 1e-10 and r2 < 1e-12,
      "S2b the paper's ratio Lambda_pred/Lambda_Planck IS the kappa measurement, squared and relabelled: it "
      "equals (kappa_hat/kappa_canon)^2 identically. So the disclaimer is a FRAMING ARTEFACT of writing the "
      "answer as a Lambda ratio -- the SAME arithmetic read as kappa_hat is a genuine, non-circular "
      "determination of the normalisation. VERDICT: the limitation is NOT fatal")


# ----------------------------------------------------------------------------------------------
banner("S3  THE H0 CONSISTENCY AUDIT -- where cosmology really does enter the galactic side")

_meta = {}
with open(os.path.join(REPO, "data", "sparc_master_clean.csv")) as fh:
    for r_ in csv.DictReader(fh):
        _meta[r_["name"]] = dict(Q=int(r_["Q"]), inc=float(r_["inc"]), fD=int(r_["fD"]),
                                 D=float(r_["D_Mpc"]))
UD, UB = 0.7, 0.98
GAL = []
for f in sorted(glob.glob(os.path.join(REPO, "data", "sparc_data", "*_rotmod.dat"))):
    nm = os.path.basename(f).replace("_rotmod.dat", "")
    m = _meta.get(nm)
    if m is None or m["Q"] > 2 or m["inc"] < 30:
        continue
    d = np.genfromtxt(f, comments="#")
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
    ok = (R > 0) & (Vo > 0) & (eV / Vo < 0.10)
    if ok.sum() == 0:
        continue
    GAL.append(dict(name=nm, fD=m["fD"], R=R[ok], Vo=Vo[ok], eV=eV[ok],
                    Vg=Vg[ok], Vd=Vd[ok], Vb=Vb[ok]))


def sample(scale_fd1=1.0, only=None):
    """Gas-dominated point sample; scale_fd1 rescales fD=1 (Hubble-flow) distances by that factor.
    Under D -> sD:  R -> sR, V_bar -> sqrt(s) V_bar (M ~ D^2, R ~ D), V_obs unchanged."""
    gb, go, rel = [], [], []
    for g in GAL:
        if only is not None and g["fD"] not in only:
            continue
        s = scale_fd1 if g["fD"] == 1 else 1.0
        R, Vg, Vd, Vb = g["R"] * s, g["Vg"] * math.sqrt(s), g["Vd"] * math.sqrt(s), g["Vb"] * math.sqrt(s)
        gstar = (UD * Vd**2 + UB * Vb**2) * 1e6 / (R * KPC)
        ggas = np.sign(Vg) * Vg**2 * 1e6 / (R * KPC)
        m = Vg**2 > (UD * Vd**2 + UB * Vb**2)
        gb.append((ggas + gstar)[m]); go.append(((g["Vo"] * 1e3)**2 / (R * KPC))[m])
        rel.append((g["eV"] / g["Vo"])[m])
    return (np.concatenate(gb), np.concatenate(go), np.concatenate(rel))


def a0_line_gls(gb, go, rel, niter=8):
    """the paper's iterated GLS slope of E = g_obs^2 - g_bar^2 on g_bar, model-based weights."""
    E = go**2 - gb**2
    a0 = A0_CANON
    for _ in range(niter):
        gm = np.sqrt(gb**2 + a0 * gb)
        sE = 2 * gm * (2 * rel * gm)
        w = 1.0 / np.maximum(sE, 1e-30)**2
        a0 = float(np.sum(w * E * gb) / np.sum(w * gb**2))
    return a0


gb0, go0, rel0 = sample(1.0)
gb1, _, _ = sample(1.10)
print(f"  gas-dominated points {len(gb0)} drawn from {len(GAL)} quality galaxies; "
      f"g_bar invariance under D -> 1.10 D: max |dlog| = {np.max(np.abs(np.log(gb1/gb0))):.2e}")
check(np.max(np.abs(np.log(gb1 / gb0))) < 1e-12,
      "S3a g_bar is EXACTLY distance-independent on the real data (the paper's g_bar ~ D^0), so all H0 "
      "dependence enters through g_obs alone -- this is the premise the exponent below rests on")

EPS = 0.02
exps = {}
for lab, only in (("full gas-dom", None), ("Hubble-flow only (fD=1)", {1}), ("TRGB/Cepheid only (fD=2,3)", {2, 3})):
    # H0 -> H0(1+e) makes Hubble-flow D -> D/(1+e); a0_hat exponent = d ln a0_hat / d ln H0
    hi = a0_line_gls(*sample(1.0 / (1 + EPS), only))
    lo = a0_line_gls(*sample(1.0 / (1 - EPS), only))
    mid = a0_line_gls(*sample(1.0, only))
    exps[lab] = (math.log(hi / lo) / math.log((1 + EPS) / (1 - EPS)), mid)
    print(f"  {lab:<26s} a0_hat = {mid:.4e}   d ln a0_hat/d ln H0 = {exps[lab][0]:+.3f}   "
          f"-> d ln kappa_hat/d ln H0 = {exps[lab][0]-1:+.3f}")
e_full, e_hf, e_cl = (exps[k][0] for k in exps)
f_share = e_full / e_hf
check(abs(e_cl) < 1e-9 and 1.8 < e_hf < 2.3,
      f"S3b the galactic side is NOT cosmology-free where it uses Hubble-flow distances: a0_hat ~ H0^"
      f"{e_hf:.2f} there (2 in the deep limit since E ~ g_obs^2 ~ D^-2, slightly above 2 because the g_bar^2 "
      f"subtraction amplifies it), while the TRGB/Cepheid subsample is EXACTLY H0-independent. Hubble-flow "
      f"weight share of the gas-dominated sample f = {f_share:.2f}. The corpus' clean-distance column is the "
      f"only STRICTLY cosmology-free one, and the paper's 'no cosmological input whatsoever' holds only there")

h0_ten = math.log(73.0 / 67.36)
# d ln sqrt(Lambda) / d ln H0: 1 at fixed Omega_L; larger at fixed omega_m = Omega_m h^2 (CMB-realistic)
dlnL_fixOmL = 1.0
dlnL_fixwm = 1.0 / OMEGA_L_P     # Lambda ~ H0^2 - 1e4 omega_m => dln sqrt(Lambda)/dln H0 = 1/Omega_L
ek = [abs(e_full - dlnL_fixOmL), abs(e_full - dlnL_fixwm)]
print(f"  the SH0ES-vs-Planck H0 offset is {100*h0_ten:.2f}% in ln H0 = {h0_ten/GAP_LOG:.2f}x the kappa gap")
print(f"  d ln sqrt(Lambda)/d ln H0 = {dlnL_fixOmL:.3f} at fixed Omega_L, {dlnL_fixwm:.3f} at fixed omega_m")
print(f"  one-sided charge on a0_hat  (= corpus S10d's treatment): {100*abs(e_full)*h0_ten:.2f}%")
print(f"  two-sided charge on kappa_hat                          : {100*ek[0]:.2f}-{100*ek[1]:.2f}% "
      f"x {100*h0_ten:.1f}% -> {100*max(ek)*h0_ten:.2f}%  (worst case kept)")
check(max(ek) < abs(e_full),
      f"S3c *** THE INVERSION PARTLY SELF-CANCELS IN H0, AND THE CORPUS'S TREATMENT IS INCONSISTENT. *** "
      f"kappa_hat ~ H0^(2f - dlnsqrtLam) so SPARC's f = {f_share:.2f} leaves exponent "
      f"{e_full-dlnL_fixwm:+.2f} to {e_full-dlnL_fixOmL:+.2f} instead of {e_full:+.2f}. Recomputing SPARC's "
      f"Hubble-flow distances at the SAME H0 that Planck's Lambda uses is mandatory, and doing it costs the "
      f"kappa test {100*max(ek)*h0_ten:.1f}% (worst case) rather than the {100*abs(e_full)*h0_ten:.1f}% a "
      f"one-sided treatment charges -- a {abs(e_full)/max(ek):.1f}x reduction. FAVOURABLE, and it is the one "
      f"thing this door buys that a0-alone does not. It also reproduces S10d's -8.7% one-sided number")


# ----------------------------------------------------------------------------------------------
banner('S4  "THE SQUARING HELPS" -- tested, and it is FALSE')

print(f"  the lane brief's hope: Lambda ~ a0^2, so the {100*(1-A0_M20/A0_CANON):.2f}% a0 gap becomes a "
      f"{100*(1-(A0_M20/A0_CANON)**2):.1f}% Lambda gap ({100*2*GAP_LOG:.2f}% in the log)")
# generalised: compare hypotheses in X = a0^p for any p.  Gaussian-in-log errors.
SIG_LN = 0.142                                                    # the corpus' N-independent floor
rows = []
for p in (0.5, 1.0, 2.0, 3.0, -1.0):
    gap_p, sig_p = abs(p) * GAP_LOG, abs(p) * SIG_LN
    rows.append((p, gap_p, sig_p, gap_p / sig_p))
print(f"  {'power p':>8}{'gap(ln)':>10}{'sigma(ln)':>11}{'S/N':>8}")
for p, g, s, sn in rows:
    print(f"  {p:>8.1f}{100*g:>9.2f}%{100*s:>10.2f}%{sn:>8.4f}")
sn_spread = max(r[3] for r in rows) - min(r[3] for r in rows)
check(sn_spread < 1e-12,
      f"S4a REPARAMETRISATION INVARIANCE: the S/N is {rows[1][3]:.4f} for EVERY power p, to {sn_spread:.1e}. "
      f"Squaring doubles the gap and doubles the error; a monotone relabelling of one number cannot create "
      f"information. The 'squaring helps' premise is FALSE")

# likelihood-ratio form: the Jacobian cancels, so the evidence is identical in either space
rng = np.random.default_rng(20260803)
draws = np.exp(rng.normal(math.log(A0_CANON), SIG_LN, 40000))


def dlnL(x, h1, h2, s):
    return (-0.5 * ((np.log(x) - math.log(h1)) / s)**2) - (-0.5 * ((np.log(x) - math.log(h2)) / s)**2)


d_a0 = dlnL(draws, A0_CANON, A0_M20, SIG_LN)
lam_of = lambda a: 8 * math.pi * a**2 / (kap_canon**2 * C_L**4)
d_lam = dlnL(lam_of(draws), lam_of(A0_CANON), lam_of(A0_M20), 2 * SIG_LN)
print(f"  40k-draw log-likelihood ratio canonical-vs-Milgrom: max |dlnL(a0) - dlnL(Lambda)| = "
      f"{np.max(np.abs(d_a0-d_lam)):.2e}   mean dlnL = {np.mean(d_a0):+.4f}")
check(np.max(np.abs(d_a0 - d_lam)) < 1e-9,
      "S4b the same conclusion in likelihood form: the evidence for canonical over Milgrom is IDENTICAL "
      "sample-by-sample whether you work in a0 or in Lambda. The inversion adds no discriminating power")

# the trap that makes people believe otherwise
naive = (1 + A0_M20 / A0_CANON) / 2.0
print(f"  the LINEAR-space trap: (Lambda_c - Lambda_M)/(2 a0_c sigma_a0) = {naive:.4f} x the a0-space S/N, "
      f"i.e. naive linear propagation LOSES {100*(1-naive):.1f}%, it does not gain")
check(naive < 1.0,
      f"S4c and where the two spaces differ at all -- naive LINEAR error propagation rather than log -- the "
      f"squared variable is {100*(1-naive):.1f}% WORSE, not better. The sign of the effect is opposite to the "
      f"hoped-for one")


# ----------------------------------------------------------------------------------------------
banner("S5  WHAT THE COSMOLOGICAL SIDE COSTS, AND THE sigma(a0) A 3-SIGMA kappa TEST NEEDS")

# Lambda = 3 H0^2 (1-Omega_m)/c^2; propagate with the Omega_m-H0 correlation SCANNED, not assumed
sOm, sH = 0.007, 0.54 / H0_P
dOm = 1.0 / (1 - OMEGA_M_P)
cands = []
for rho_c in (-1.0, -0.5, 0.0, 0.5, 0.93, 1.0):
    v = (dOm * sOm)**2 + (2 * sH)**2 + 2 * rho_c * (dOm * sOm) * (2 * sH)
    cands.append(math.sqrt(max(v, 0.0)))
SIG_LNLAM_PL, SIG_LNLAM_TIGHT = max(cands), min(cands)
SIG_LNLAM_DESI = 1.30e-2                              # DESI DR2 BAO+CMB LCDM class, illustrative
print(f"  Planck-class sigma(ln Lambda) over the full correlation scan: {100*SIG_LNLAM_TIGHT:.2f}% to "
      f"{100*SIG_LNLAM_PL:.2f}%  (loose end adopted, per the no-truncation rule)")
print(f"  in a0-equivalent (half of it): {100*SIG_LNLAM_PL/2:.2f}% (Planck) / {100*SIG_LNLAM_DESI/2:.2f}% (DESI-class)")
sig_needed = [math.sqrt(max(need3_naive**2 - (s / 2)**2, 0.0)) for s in (SIG_LNLAM_DESI, SIG_LNLAM_PL)]
print(f"  3-sigma budget on the LOG gap                       : sigma(ln a0) <= {100*need3_naive:.3f}%")
print(f"  ... after paying the cosmological side              : {100*min(sig_needed):.3f}% to "
      f"{100*max(sig_needed):.3f}%   (TIGHTER, not looser)")
print(f"  cosmology-only ceiling (a perfect galactic a0)       : {GAP_LOG/(SIG_LNLAM_PL/2):.1f} to "
      f"{GAP_LOG/(SIG_LNLAM_DESI/2):.1f} sigma")
check(max(sig_needed) < need3_naive and min(sig_needed) > 0,
      f"S5a THE ANSWER TO (b) IS NO. The required sigma(a0) is not materially looser than the 2.73% the "
      f"corpus already has -- it is {100*min(sig_needed):.2f}-{100*max(sig_needed):.2f}%, i.e. 3-12% TIGHTER, "
      f"because the cosmological error adds in quadrature rather than relaxing anything")
check(GAP_LOG / (SIG_LNLAM_PL / 2) > 3.0,
      f"S5b the one genuinely favourable finding: the cosmological side is NOT the binding constraint. On a "
      f"CMB+BAO LCDM Lambda it alone would support a {GAP_LOG/(SIG_LNLAM_PL/2):.1f}-sigma kappa test, so the "
      f"door is entirely galactic-side-limited")

# and the model-choice systematic the corpus has never charged on the COSMOLOGICAL side
lam_ratio_h0 = ((73.0 / 100) ** 2 - OMEGA_M_P * (H0_P / 100) ** 2) / \
               ((H0_P / 100) ** 2 - OMEGA_M_P * (H0_P / 100) ** 2)
s_h0_cosmo = 0.5 * math.log(lam_ratio_h0)
print(f"  AGAINST INTEREST: if the H0 tension is physical, Lambda at h = 0.73 (fixed omega_m) is "
      f"{lam_ratio_h0:.3f}x Planck's = {100*s_h0_cosmo:.1f}% in a0-equivalent = {s_h0_cosmo/GAP_LOG:.2f}x the gap")
check(s_h0_cosmo > GAP_LOG,
      f"S5c so S5b's favourable reading is CONDITIONAL on committing to a CMB+BAO LCDM Lambda. Allow the H0 "
      f"tension to be physical and the cosmological side alone costs {100*s_h0_cosmo:.1f}% in a0-equivalent, "
      f"{s_h0_cosmo/GAP_LOG:.2f}x the whole kappa gap, and the door closes on the COSMOLOGICAL side too. "
      f"Both readings are stated; the corpus currently carries neither")


# ----------------------------------------------------------------------------------------------
banner("S6  THE w0-wa COMPLICATION -- three separate effects, priced separately")

# EFFECT A -- the fitted (Omega_m, H0) move when you allow w != -1, so the number you call "Lambda" moves
def lam_eff(om, h):
    return 3.0 * (1.0 - om) * (h * 1e5 / 3.0857e22) ** 2 / C_L ** 2


boxes = {"LCDM-to-w0waCDM (fiducial)": ((0.300, 0.340), (0.665, 0.690)),
         "widened": ((0.295, 0.360), (0.660, 0.695))}
effA = {}
for lab, (omr, hr) in boxes.items():
    vals = [lam_eff(om, h) for om in omr for h in hr]
    effA[lab] = 0.5 * 0.5 * math.log(max(vals) / min(vals))     # half-range, then a0-equivalent (half of ln)
    print(f"  Effect A {lab:<28s} Omega_m {omr}  h {hr}  ->  {100*effA[lab]:.2f}% in a0-equivalent")
eA = max(effA.values())
check(eA < GAP_LOG and eA > need3_naive,
      f"S6a EFFECT A (which number you call Lambda) is {100*eA:.2f}% in a0-equivalent: it does NOT swamp the "
      f"{100*GAP_LOG:.2f}% gap, but it DOES exceed the entire {100*need3_naive:.2f}% 3-sigma budget by "
      f"{eA/need3_naive:.1f}x. So allowing evolving dark energy alone disqualifies the cosmological side from "
      f"being treated as a 1% anchor")

# EFFECT B -- the framework's own a0(z) over the actual SPARC redshifts (bump-then-decline law)
gasgals = {}
for g in GAL:
    R, Vg, Vd, Vb = g["R"], g["Vg"], g["Vd"], g["Vb"]
    n = int(np.sum(Vg ** 2 > (UD * Vd ** 2 + UB * Vb ** 2)))
    if n:
        gasgals[g["name"]] = (_meta[g["name"]]["D"], n)
zs = np.array([73.0 * d / 299792.458 for d, _ in gasgals.values()])
wts = np.array([n for _, n in gasgals.values()], float)


def a0z(z, w0, wa):
    return (1 + z) ** (1.5 * (1 + w0 + wa)) * math.exp(-1.5 * wa * z / (1 + z))


for w0, wa in ((-0.75, -0.86), (-0.42, -1.75)):
    sh = np.array([a0z(z, w0, wa) for z in zs])
    eB = abs(math.log(float(np.average(sh, weights=wts))))
    print(f"  Effect B (w0,wa)=({w0:+.2f},{wa:+.2f}): SPARC gas galaxies z_med {np.median(zs):.4f} "
          f"z_max {zs.max():.4f} -> point-weighted a0(z) shift {100*eB:.2f}%, worst galaxy "
          f"{100*abs(math.log(sh.max())):.2f}%")
eB_worst = max(abs(math.log(max(a0z(z, w0, wa) for z in zs)))
               for w0, wa in ((-0.75, -0.86), (-0.42, -1.75)))
check(eB_worst < GAP_LOG,
      f"S6b EFFECT B (the framework's own a0(z) across the sample's own redshifts) is at most "
      f"{100*eB_worst:.2f}% even on the most aggressive DESI-class (w0,wa) and at the most distant galaxy -- "
      f"below the gap. SPARC is local enough that the bump-then-decline law does not reach this door")

# EFFECT C -- the de Sitter premise itself.  epsilon = -Hdot/H^2 measures how non-static the horizon is.
eps = {"canonical footing, LCDM (pure Lambda)": 0.0,
       "ALT footing, LCDM (total H at z=0)": 1.5 * OMEGA_M_P,
       "pure-DE with w0 = -0.84": 1.5 * (1 - 0.84),
       "pure-DE with w0 = -0.75": 1.5 * (1 - 0.75),
       "pure-DE with w0 = -0.42": 1.5 * (1 - 0.42)}
for k, v in eps.items():
    print(f"  Effect C  epsilon = -Hdot/H^2  {k:<38s} {v:.3f}   ({v/GAP_LOG:.1f}x the gap)")
check(eps["canonical footing, LCDM (pure Lambda)"] == 0.0
      and min(v for k, v in eps.items() if "w0" in k) > GAP_LOG,
      f"S6c EFFECT C is the one that matters and it is STRUCTURAL, not numerical: the Gibbons-Hawking "
      f"temperature the framework's a0 is built on assumes a static horizon, exact only when epsilon = 0, "
      f"which holds for the canonical pure-Lambda footing in LCDM and for NOTHING else here. Any DESI-class "
      f"w0 puts epsilon at {min(v for k,v in eps.items() if 'w0' in k):.2f}-"
      f"{max(v for k,v in eps.items() if 'w0' in k):.2f}, i.e. 3-11x the gap the door is trying to resolve. "
      f"This is an order-of-magnitude adiabaticity estimate, NOT a computed correction to T_dS -- but its size "
      f"means w != -1 damages the DERIVATION far more than it shifts the NUMBER")


# ----------------------------------------------------------------------------------------------
banner("S7  THE FOOTING FORK -- is the kappa question even well posed?")

HYP = {"canonical (cH_Lambda), Z = 2sqrt(8pi/3)": A0_CANON,
       "canonical (cH_Lambda), Z = 2pi": A0_M20,
       "ALT (cH0), Z = 2sqrt(8pi/3)": A0_ALT,
       "ALT (cH0), Z = 2pi": A0_ALT * Z_FW / TWO_PI}
for k, v in HYP.items():
    print(f"  {k:<40s} a0 = {v:.4e}")
keys = list(HYP)
gaps = sorted(abs(math.log(HYP[a] / HYP[b])) for i, a in enumerate(keys) for b in keys[i + 1:])
FOOT_LOG = abs(math.log(A0_ALT / A0_CANON))
print(f"  6 pairwise log separations: " + ", ".join(f"{100*g:.2f}%" for g in gaps))
print(f"  footing fork {100*FOOT_LOG:.2f}%  vs  Z fork {100*GAP_LOG:.2f}%  ->  ratio {FOOT_LOG/GAP_LOG:.2f}")
print(f"  a 3-sigma 4-WAY separation needs sigma(ln a0) <= {100*gaps[0]/3:.2f}% (set by the smallest gap, "
      f"which IS the Z gap)")
check(FOOT_LOG > GAP_LOG and abs(gaps[0] - GAP_LOG) < 1e-12,
      f"S7a THE ANSWER TO (d) IS YES, THE FORK MUST BE RESOLVED FIRST. The footing choice moves the predicted "
      f"a0 by {100*FOOT_LOG:.2f}%, {FOOT_LOG/GAP_LOG:.2f}x the {100*GAP_LOG:.2f}% Z signal, so with the footing "
      f"left open as a discrete nuisance the Z inference is not identified: a Z shift and a footing shift are "
      f"the same kind of multiplicative move on one number. Either commit to a footing on independent grounds "
      f"or report the 4-way ladder, never a 2-way kappa verdict")

# are any two of the four hypotheses DEGENERATE?  (canon, Z_FW) == (ALT, 2pi) would need a special Omega_L
om_needed = (Z_FW / TWO_PI) ** 2
om_meas, om_err = (A0_CANON / A0_ALT) ** 2, 2 * 0.007       # sqrt(Omega_L) = H_Lambda/H0 = a0_canon/a0_ALT
nsig_alias = abs(om_needed - om_meas) / om_err
print(f"  aliasing test: (canon,Z_FW) would coincide with (ALT,2pi) iff Omega_L = (Z_FW/2pi)^2 = "
      f"{om_needed:.4f}; measured {om_meas:.4f} +- {om_err:.3f}  ->  {nsig_alias:.1f} sigma away")
check(nsig_alias > 5.0,
      f"S7b FAVOURABLE: the two forks are not DEGENERATE with each other, only unresolved. Exact aliasing "
      f"would require Omega_Lambda = 8/(3pi) = {om_needed:.4f}, excluded at {nsig_alias:.0f} sigma. So the "
      f"4-way ladder is identifiable in principle -- one measurement at {100*gaps[0]/3:.1f}% would settle "
      f"footing AND Z together")
print(f"  a theory-side lever on the fork, from S6c and NOT from data: epsilon = 0 exactly on the canonical "
      f"pure-Lambda footing and {1.5*OMEGA_M_P:.2f} on ALT, so only canonical has a static-horizon limit at all")
print(f"  AGAINST INTEREST: the corpus' own ledger records theory favouring Z = 2pi (both natural constants "
      f"in the a0 box are 2pi) while data lean Z = 2sqrt(8pi/3). The two theory arguments point OPPOSITE ways.")


# ----------------------------------------------------------------------------------------------
banner("S8  THE ASSEMBLED BUDGET AND THE VERDICT")

S_GAL_TODAY, S_GAL_FLOOR = 0.175, 0.142           # mi_routeA_shape_invariant_a0_2026.py S7/S8
S_COSMO = SIG_LNLAM_PL / 2
S_H0CONS = max(ek) * h0_ten
budget = {
    "today, best shape-invariant galactic a0": [S_GAL_TODAY, S_COSMO, S_H0CONS],
    "N -> inf, LCDM-committed cosmology": [S_GAL_FLOOR, S_COSMO, S_H0CONS],
    "  + evolving dark energy allowed (Effect A)": [S_GAL_FLOOR, S_COSMO, S_H0CONS, eA],
    "  + H0 tension taken as physical": [S_GAL_FLOOR, S_COSMO, S_H0CONS, eA, s_h0_cosmo],
}
best = 9e9
for lab, terms in budget.items():
    tot = math.sqrt(sum(t * t for t in terms))
    best = min(best, tot)
    print(f"  {lab:<44s} sigma(ln a0_eff) = {100*tot:5.2f}%   kappa separation {GAP_LOG/tot:.2f} sigma")
req = max(sig_needed)
print(f"  required for 3 sigma: {100*min(sig_needed):.2f}-{100*req:.2f}%   ->  shortfall "
      f"{best/req:.1f}x to {best/min(sig_needed):.1f}x")
check(GAP_LOG / best < 3.0 and best > req,
      f"S8a *** THE DOOR IS GENUINE BUT IT DOES NOT REACH. *** The Lambda inversion IS a real, non-circular "
      f"measurement of the normalisation (S1, S2), kappa enters it at leading order and no transition shape "
      f"enters the inversion ITSELF -- but it consumes a galactic a0 whose shape systematic it inherits whole, "
      f"so the best available total is {100*best:.2f}% against the {100*req:.2f}% needed: "
      f"{GAP_LOG/best:.2f} sigma, {best/req:.1f}x short. reaches_3pct = NO")

kap_hat = kappa_of(8.5573e-11, LAM_PLANCK)          # the sibling lane's shape-invariant central
print(f"  read as a NORMALISATION MEASUREMENT, the sharpest shape-invariant galactic a0 gives "
      f"kappa_hat = {kap_hat:.4f} +- {100*best:.1f}% (canonical 0.5000, Milgrom {kap_M20:.4f})")
print(f"    -> {abs(kap_hat-kap_canon)/(kap_canon*best):.2f} sigma from canonical, "
      f"{abs(kap_hat-kap_M20)/(kap_M20*best):.2f} sigma from Milgrom: consistent with BOTH, discriminating "
      f"NEITHER, and it does not lean kappa = 1/2")
check(abs(kap_hat - kap_canon) / (kap_canon * best) < 3
      and abs(kap_hat - kap_M20) / (kap_M20 * best) < 3,
      "S8b stated as plainly as a win would be: this door does not currently favour Carl's normalisation. It "
      "is consistent with both candidates, and the small residual lean is toward Milgrom's, not away from it")

banner("SCOPE -- what is and is not established here")
print("""  ESTABLISHED:
   * A0LINE_LAMBDA_2026's disclaimer is a FRAMING ARTEFACT, not a theorem. kappa = (a0/c^2)sqrt(8pi/Lambda)
     needs no assumed Z; the paper's Lambda ratio IS (kappa_hat/kappa_canon)^2, identically (S1, S2).
   * The precision hope fails: S/N is invariant under a0 -> a0^p, so the 16.4% Lambda gap buys NOTHING over
     the 8.20% a0 gap, and the required sigma(a0) is 2.40-2.65%, TIGHTER than 2.73% (S4, S5).
   * The galactic side is not cosmology-free where it uses Hubble-flow distances (a0_hat ~ H0^2.09 there),
     but the inversion PARTLY SELF-CANCELS in H0 -- kappa_hat carries only H0^(-0.30..+0.15) (S3).
   * w != -1 costs 5.0% in a0-equivalent numerically (Effect A) and O(0.24-0.87) STRUCTURALLY (Effect C) (S6).
   * The footing fork (18.8%) is larger than the Z signal (8.20%), so a 2-way kappa verdict is not well posed;
     but the forks are not degenerate -- exact aliasing needs Omega_L = 8/(3pi) = 0.849, excluded even on a
     DOUBLED Planck error bar -- so ONE measurement at 2.73% would settle footing and Z together (S7).
  NOT CLAIMED:
   * NOT that the framework fails, and NOT that kappa = 1/2 is wrong. It is unmeasured at useful significance.
   * NOT a new a0 measurement. Every galactic number here is the sibling lane's, consumed not refitted.
   * Effect C is an adiabaticity SCALE, not a computed correction to the de Sitter-Unruh temperature.
   * a0 is an INPUT on both footings throughout; nothing was fitted to it.
   * No file outside this one was written. This is not a claim that the door is closed -- the identified
     openings are a kernel/shape determination, a gas-mass calibration, and y ~ 1 dynamic range.""")
print(f"\n  {_nchk[0]}/{_nchk[1]} checks held.")
print("  Exit 0: the Lambda inversion is a legitimate normalisation test whose precision the squaring does "
      "not improve.")
