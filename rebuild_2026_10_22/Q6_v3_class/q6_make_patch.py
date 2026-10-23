#!/usr/bin/env python3
"""Q6_v3_class step P: the Khronon (v3) variant of C7's AeST-patched CLASS v3.3.4 (FROZEN_CRITERIA section 5 + A2).

Usage:  python3 -I q6_make_patch.py PRISTINE_DIR TARGET_DIR [--mutate]
  PRISTINE_DIR = ../_external_data/class_public_v3.3.4_2026_10_22/class_public-3.3.4 (never modified)
  TARGET_DIR   = a new directory (must not exist).
Steps: copy the pristine tree; apply C7's aest.patch (covariant_push_2026_10_22/C7_aest_class/aest.patch) with
`patch -p1` (must apply cleanly); replace ONLY the bodies of C7's two isolated functions background_aest_K() and
perturbations_aest_rhs(), plus (AMENDMENT A2.2, the frozen fallback when IC_C7 fails) the sector's IC lines; write the
unified diff pristine -> Khronon tree (source/include) to khronon.patch (khronon_MUTATE.patch with --mutate, which flips
the sign of the metric-source term of the khronon delta' equation, FROZEN_CRITERIA V4).

Parameter semantics in the Khronon tree (C7's input names kept, re-labelled here; no input.c edit):
  aest_K_type 0 DUST (K'' -> inf), 3 LIT (literal quadratic K), 4 LOB (dust background + literal c_s^2);
  aest_K2 = mu_K^2 [Mpc^-2]; aest_Q0 = 1 (Q dimensionless); aest_lambda_c = j1 = J'(0) (-1 for v3's J_x);
  aest_K_B = 1 and aest_g = 1 (unused / derived g = 1).  Equations: q6_derive.py (D2_fluid, D9_cform, IC_fld).
"""
import difflib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
C7PATCH = os.path.join(REPO, "covariant_push_2026_10_22", "C7_aest_class", "aest.patch")
pristine, target = sys.argv[1], sys.argv[2]
MUT = "--mutate" in sys.argv
assert os.path.isdir(pristine) and not os.path.exists(target)
shutil.copytree(pristine, target)
r = subprocess.run(["patch", "-p1", "--forward", "--no-backup-if-mismatch", "-d", target, "-i", C7PATCH],
                   capture_output=True, text=True)
print(r.stdout.strip())
assert r.returncode == 0 and "FAILED" not in r.stdout and "offset" not in r.stdout.lower(), r.stdout + r.stderr


def replace_between(path, start, end, new, keep_end=True):
    fp = os.path.join(target, path)
    s = open(fp).read()
    assert s.count(start) == 1, f"start anchor x{s.count(start)} in {path}: {start[:70]!r}"
    i = s.index(start)
    j = s.index(end, i)
    assert s.count(end) >= 1
    s = s[:i] + new + (s[j:] if keep_end else s[j + len(end):])
    open(fp, "w").write(s)


# ------------------------------------------------------------------ 1. background_aest_K()
BG_NEW = r"""/**
 * Q6_v3_class: Khronon (v3) variant of C7's background_aest_K(). BS24 Eq. 7: K(Q) = mu_K^2 (Q-1)^2, Q dimensionless
 * (aest_Q0 = 1), aest_K2 = mu_K^2 [Mpc^-2]. K'(Qbar) = I0/a^3 (khronon shift charge, FITTED via Omega_aest).
 * aest_K_type: 0 DUST (K'' -> infinity); 3 LIT (literal: Qbar = 1 + I0/(2 mu^2 a^3), K = mu^2 (Qbar-1)^2);
 * 4 LOB (dust background Qbar = 1, K = 0; perturbations use the literal c_s^2, see perturbations_aest_rhs()).
 * Returns Qbar, K, K' and the background c_a^2 = K'/(Q K'') (0 for DUST and LOB).
 * Derivation: rebuild_2026_10_22/Q6_v3_class/q6_derive.py (D1, D8, D10).
 */
int background_aest_K(
                      struct background * pba,
                      double a,
                      double * Q,
                      double * Kz,
                      double * Kp,
                      double * ca2
                      ) {
  double I0 = pba->aest_I0, mu2 = pba->aest_K2;
  double kp = I0/(a*a*a);

  *Kp = kp;
  switch (pba->aest_K_type) {
  case 0: /* DUST: K'' -> infinity at fixed I0 */
  case 4: /* LOB: dust background (the a^-6 partner and all O(Qbar-1) background terms dropped) */
    *Q = 1.;
    *Kz = 0.;
    *ca2 = 0.;
    break;
  case 3: /* LIT: literal quadratic K */
    *Q = 1. + kp/(2.*mu2);
    *Kz = kp*kp/(4.*mu2);
    *ca2 = kp/((*Q)*2.*mu2);
    break;
  default:
    class_stop(pba->error_message,"Khronon (Q6): aest_K_type = %d not coded (0 DUST, 3 LIT, 4 LOB)",pba->aest_K_type);
  }
  return _SUCCESS_;
}

"""
replace_between("source/background.c", "/**\n * C7_aest_class: background of the AeST extra sector",
                "/**\n * C7_aest_class: solve the shift charge I0", BG_NEW)

# ------------------------------------------------------------------ 2. perturbations_aest_rhs()
cont = "(theta - metric_continuity)" if MUT else "(theta + metric_continuity)"
PT_NEW = r"""/**
 * Q6_v3_class: Khronon (v3) variant of C7's perturbations_aest_rhs(). Derived from BS24's action with J only through
 * J(0) and j1 = J'(0) (q6_derive.py D0-D10): the khronon sector is a fluid with no shear and rest-frame sound speed
 *   cs2 = Q K'/(Q^2 K'' - 2 j1 k^2/a^2),  K'' = 2 mu_K^2  (LIT: background Q; LOB: literal Q = 1 + K'/(2 mu^2); DUST: 0)
 *   dp/rho = cs2 (delta + 3H(1+w) theta/k^2) - 3H ca2 (1+w) theta/k^2
 *   delta' = -(1+w)(theta + metric_continuity) - 3H(dp/rho - w delta)
 *   theta' = -H(1-3ca2) theta + k^2 (dp/rho)/(1+w) + metric_euler
 * y[0..1] = (delta, theta); C7's slots y[2..3] are dormant (0). j1 is read from aest_lambda_c (v3: -1).
 */
static int perturbations_aest_rhs(
                                  struct background * pba,
                                  double k,
                                  double * pvecback,
                                  double metric_continuity,
                                  double metric_euler,
                                  double * y,
                                  double * dy,
                                  double * dp_over_rho
                                  ) {
  double a = pvecback[pba->index_bg_a];
  double H = pvecback[pba->index_bg_H]*a;
  double Q = pvecback[pba->index_bg_Q_aest];
  double Kz = pvecback[pba->index_bg_Kz_aest];
  double Kp = pvecback[pba->index_bg_Kp_aest];
  double ca2 = pvecback[pba->index_bg_ca2_aest];
  double mu2 = pba->aest_K2;
  double j1 = pba->aest_lambda_c;
  double rho_hat = Q*Kp - Kz;
  double w = Kz/rho_hat;
  double k2 = k*k;
  double delta = y[0], theta = y[1];
  double cs2 = 0., Ql, Pi;

  switch (pba->aest_K_type) {
  case 3: /* LIT */
    cs2 = Q*Kp/(Q*Q*2.*mu2 - 2.*j1*k2/a/a);
    break;
  case 4: /* LOB: literal Qbar on a dust background */
    Ql = 1. + Kp/(2.*mu2);
    cs2 = Ql*Kp/(Ql*Ql*2.*mu2 - 2.*j1*k2/a/a);
    break;
  default: /* DUST */
    cs2 = 0.;
  }
  Pi = cs2*(delta + 3.*H*(1.+w)*theta/k2) - 3.*H*ca2*(1.+w)*theta/k2;

  *dp_over_rho = Pi;
  if (dy != NULL) {
    dy[0] = -(1.+w)*""" + cont + r""" - 3.*H*(Pi - w*delta);
    dy[1] = -H*(1.-3.*ca2)*theta + k2*Pi/(1.+w) + metric_euler;
    dy[2] = 0.;
    dy[3] = 0.;
  }
  return _SUCCESS_;
}

"""
fp = os.path.join(target, "source/perturbations.c")
s = open(fp).read()
st = "/**\n * C7_aest_class: the AeST extra sector's linear equations"
i = s.index(st)
assert s.count(st) == 1
j = s.index("  return _SUCCESS_;\n}\n", i) + len("  return _SUCCESS_;\n}\n")
s = s[:i] + PT_NEW.rstrip("\n") + "\n" + s[j:]
open(fp, "w").write(s)

# ------------------------------------------------------------------ 3. the sector's IC lines (AMENDMENT A2.2)
IC_NEW = r"""      /* Q6_v3_class (AMENDMENT A2.2): khronon-sector adiabatic IC = CLASS's fluid formula (1004.5509, as for fld) with
         w from the background and the rest-frame c_s^2(k, tau_ini) from perturbations_aest_rhs() (dp/rho at delta = 1,
         theta = 0). q6_derive.py IC1-IC3, IC_fld. C7's slots E, chi are dormant (0). */
      if (pba->has_aest == _TRUE_) {
        double Qa = ppw->pvecback[pba->index_bg_Q_aest];
        double Kpa = ppw->pvecback[pba->index_bg_Kp_aest];
        double Kza = ppw->pvecback[pba->index_bg_Kz_aest];
        double w_a = Kza/(Qa*Kpa - Kza);
        double yu_a[4] = {1., 0., 0., 0.};
        double cs2_a;
        perturbations_aest_rhs(pba,k,ppw->pvecback,0.,0.,yu_a,NULL,&cs2_a);
        ppw->pv->y[ppw->pv->index_pt_delta_aest] = 3./4.*ppw->pv->y[ppw->pv->index_pt_delta_g]*(1.+w_a)*(4.-3.*cs2_a)/(4.-6.*w_a+3.*cs2_a);
        ppw->pv->y[ppw->pv->index_pt_theta_aest] = - k*ktau_three/4.*cs2_a/(4.-6.*w_a+3.*cs2_a) * ppr->curvature_ini * s2_squared;
        ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;
        ppw->pv->y[ppw->pv->index_pt_chi_aest] = 0.;
      }
"""
s = open(fp).read()
st = "      /* AeST extra sector (C7): adiabatic IC"
i = s.index(st)
assert s.count(st) == 1
endm = "        ppw->pv->y[ppw->pv->index_pt_chi_aest] = a*Qa*th_a/k/k + qal_a;\n      }\n"
j = s.index(endm, i) + len(endm)
s = s[:i] + IC_NEW + s[j:]
open(fp, "w").write(s)
print(f"Khronon edits applied to {target}{' (MUTATE)' if MUT else ''}")

# ------------------------------------------------------------------ diff pristine -> Khronon tree
out = []
for sub in ("include", "source"):
    for fn in sorted(os.listdir(os.path.join(pristine, sub))):
        a_ = open(os.path.join(pristine, sub, fn)).read().splitlines(keepends=True)
        b_ = open(os.path.join(target, sub, fn)).read().splitlines(keepends=True)
        if a_ != b_:
            out.extend(difflib.unified_diff(a_, b_, fromfile=f"a/{sub}/{fn}", tofile=f"b/{sub}/{fn}"))
pname = os.path.join(HERE, "khronon_MUTATE.patch" if MUT else "khronon.patch")
open(pname, "w").write("".join(out))
print(f"wrote {os.path.basename(pname)}: {sum(1 for l in out if l.startswith('+') and not l.startswith('+++'))} added, "
      f"{sum(1 for l in out if l.startswith('-') and not l.startswith('---'))} removed lines")
