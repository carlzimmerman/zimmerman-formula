#!/usr/bin/env python3
"""L184 -- second patch on top of L183: the CONSISTENT metric derivative for the mean-field kernel (astra's L183 review, 2026-09-11).
With phi_eff = nu * phi_N one has phi_eff' = nu * phi_N' + nu' * phi_N; L183 dropped nu' * phi_N. New input mond_nuprime (0 = L183
behaviour, 1 = add nu' phi_N). nu' by the chain rule on x = K(k) * env / a: d ln x / dtau = -aH + phi phi' / env^2 (the phi'' term of the
envelope is dropped; it matters only where nu = 1), and x dnu/dx = -(nu/2) u/(e^u - 1), u = sqrt(x) (Lean: mean_field_isw_rate_identity).
nu' = 0 on the cap. The GR phi_N' is stored so dy[phi] no longer divides by nu (identical when mond_nuprime = 0).
Every replacement is asserted EXACTLY ONCE. Usage: python3 apply_nuprime_patch.py <L183-patched classy-3.3.4.0>"""
import sys, os
root = sys.argv[1]
def patch(path, reps):
    s = open(path).read()
    for old, new in reps:
        n = s.count(old); assert n == 1, f"{os.path.basename(path)}: expected exactly one match, found {n}: {old[:70]!r}"
        s = s.replace(old, new)
    open(path, "w").write(s)
H = os.path.join(root, "include/perturbations.h"); I = os.path.join(root, "source/input.c"); P = os.path.join(root, "source/perturbations.c")
patch(H, [("double mond_numax; /**< L183 mean-field MOND kernel */", "double mond_numax; double mond_nuprime; /**< L183 mean-field MOND kernel; L184 consistent derivative switch */"),
          ("  double mond_nu;             /**< L183: current mean-field kernel factor */",
           "  double mond_nu;             /**< L183: current mean-field kernel factor */\n  double mond_phiN_prime;     /**< L184: GR phi_N' (stored so phi_N keeps its GR evolution) */")])
patch(I, [("ppt->mond_numax = 20.;\n", "ppt->mond_numax = 20.; ppt->mond_nuprime = 0.;\n"),
          ('class_read_double("mond_numax",ppt->mond_numax);', 'class_read_double("mond_numax",ppt->mond_numax); class_read_double("mond_nuprime",ppt->mond_nuprime);')])
patch(P, [("      ppw->mond_nu = 1.;\n      if (ppt->mond_a0 > 0.",
           "      ppw->mond_nu = 1.; ppw->mond_phiN_prime = ppw->pvecmetric[ppw->index_mt_phi_prime]; /* L184 */\n      if (ppt->mond_a0 > 0."),
          ("        ppw->pvecmetric[ppw->index_mt_psi] *= ppw->mond_nu;\n        ppw->pvecmetric[ppw->index_mt_phi_prime] *= ppw->mond_nu;\n",
           "        double mnup = 0.; /* L184: nu' = -(nu/2) [u/(e^u-1)] d ln x/dtau, zero on the cap */\n"
           "        if (ppt->mond_nuprime > 0. && ppw->mond_nu < ppt->mond_numax) {\n"
           "          double mu = sqrt(mx); double mfac = (mu < 1e-8) ? 1. : mu/(exp(mu)-1.);\n"
           "          double mdlnx = -a_prime_over_a + mphiN*mphiNp/(menv*menv);\n"
           "          mnup = -0.5*ppw->mond_nu*mfac*mdlnx;\n"
           "        }\n"
           "        ppw->pvecmetric[ppw->index_mt_psi] *= ppw->mond_nu;\n"
           "        ppw->pvecmetric[ppw->index_mt_phi_prime] = ppw->mond_nu*mphiNp + mnup*mphiN; /* L184: (nu phi_N)' */\n"),
          ("      dy[pv->index_pt_phi] = pvecmetric[ppw->index_mt_phi_prime]/ppw->mond_nu; /* L183: GR evolution of phi_N */",
           "      dy[pv->index_pt_phi] = ppw->mond_phiN_prime; /* L183/L184: GR evolution of phi_N */")])
print("nuprime patch OK")
