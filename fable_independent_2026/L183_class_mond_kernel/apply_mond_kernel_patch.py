#!/usr/bin/env python3
"""L183 -- patch CLASS 3.3.4.0 (Newtonian gauge) with a MEAN-FIELD MOND KERNEL on the metric potentials.
Species and CMB sources see psi_eff = nu * psi_N, phi'_eff = nu * phi'_N, phi_eff = nu * phi_N, with nu = nu_RAR(g/a0),
g = (k/a) * A_env * sqrt(As (k/kp)^(ns-1)) * c^2/Mpc the physical rms acceleration of the mode (A_env = oscillator envelope of phi_N),
while phi_N itself keeps its GR evolution (momentum constraint). Active only for sub-horizon modes (k tau > 1) and z > mond_zmin;
nu capped at mond_numax. New inputs: mond_a0 [m/s^2] (0 = off, stock CLASS), mond_zmin, mond_As, mond_ns, mond_kpivot, mond_numax.
Every replacement is asserted EXACTLY ONCE. Usage: python3 apply_mond_kernel_patch.py <extracted-classy-3.3.4.0>"""
import sys, os, re
root = sys.argv[1]
def patch(path, reps, regex=False):
    s = open(path).read()
    for old, new in reps:
        n = len(re.findall(old, s)) if regex else s.count(old)
        assert n == 1, f"{os.path.basename(path)}: expected exactly one match, found {n}: {old[:60]!r}"
        s = re.sub(old, new, s) if regex else s.replace(old, new)
    open(path, "w").write(s)
H = os.path.join(root, "include/perturbations.h"); I = os.path.join(root, "source/input.c"); P = os.path.join(root, "source/perturbations.c")
patch(H, [("  enum possible_gauges gauge; /**< gauge in which to perform this calculation */",
           "  enum possible_gauges gauge; /**< gauge in which to perform this calculation */\n  double mond_a0; double mond_zmin; double mond_As; double mond_ns; double mond_kpivot; double mond_numax; /**< L183 mean-field MOND kernel */"),
          ("  int index_mt_phi_prime;     /**< (d phi/d conf.time) in longitudinal gauge */",
           "  int index_mt_phi_prime;     /**< (d phi/d conf.time) in longitudinal gauge */\n  double mond_nu;             /**< L183: current mean-field kernel factor */")])
patch(I, [("  ppt->has_perturbations = _FALSE_;\n",
           "  ppt->has_perturbations = _FALSE_;\n  ppt->mond_a0 = 0.; ppt->mond_zmin = 0.; ppt->mond_As = 2.1e-9; ppt->mond_ns = 0.9649; ppt->mond_kpivot = 0.05; ppt->mond_numax = 20.;\n"),
          (r'(\n\s*class_call\(parser_read_string\(pfc,"gauge",&string1,&flag1,errmsg\),)',
           r'\n  class_read_double("mond_a0",ppt->mond_a0); class_read_double("mond_zmin",ppt->mond_zmin); class_read_double("mond_As",ppt->mond_As); class_read_double("mond_ns",ppt->mond_ns); class_read_double("mond_kpivot",ppt->mond_kpivot); class_read_double("mond_numax",ppt->mond_numax);\1')], regex=True)
patch(P, [("      /* equation for phi' */\n      ppw->pvecmetric[ppw->index_mt_phi_prime] = -a_prime_over_a * ppw->pvecmetric[ppw->index_mt_psi] + 1.5 * (a2/k2) * ppw->rho_plus_p_theta;\n",
           "      /* equation for phi' */\n      ppw->pvecmetric[ppw->index_mt_phi_prime] = -a_prime_over_a * ppw->pvecmetric[ppw->index_mt_psi] + 1.5 * (a2/k2) * ppw->rho_plus_p_theta;\n"
           "      /* L183 mean-field MOND kernel: species and sources see nu * GR potentials; phi_N keeps GR evolution (see derivs) */\n"
           "      ppw->mond_nu = 1.;\n"
           "      if (ppt->mond_a0 > 0. && (1./sqrt(a2) - 1.) > ppt->mond_zmin && k*tau > 1.) {\n"
           "        double mphiN = y[ppw->pv->index_pt_phi]; double mphiNp = ppw->pvecmetric[ppw->index_mt_phi_prime];\n"
           "        double menv = sqrt(mphiN*mphiN + 3.*mphiNp*mphiNp/k2);\n"
           "        double mamp = sqrt(ppt->mond_As*pow(k/ppt->mond_kpivot, ppt->mond_ns-1.));\n"
           "        double mg = (k/sqrt(a2))*menv*mamp*8.98755e16/3.0857e22;\n"
           "        double mx = mg/ppt->mond_a0; if (mx < 1e-300) mx = 1e-300;\n"
           "        ppw->mond_nu = 1./(1.-exp(-sqrt(mx))); if (ppw->mond_nu > ppt->mond_numax) ppw->mond_nu = ppt->mond_numax;\n"
           "        ppw->pvecmetric[ppw->index_mt_psi] *= ppw->mond_nu;\n"
           "        ppw->pvecmetric[ppw->index_mt_phi_prime] *= ppw->mond_nu;\n"
           "      }\n"),
          ("      dy[pv->index_pt_phi] = pvecmetric[ppw->index_mt_phi_prime];", "      dy[pv->index_pt_phi] = pvecmetric[ppw->index_mt_phi_prime]/ppw->mond_nu; /* L183: GR evolution of phi_N */"),
          ("          metric_euler = k2*y[ppw->pv->index_pt_phi] - 4.5*a2*ppw->rho_plus_p_shear;", "          metric_euler = k2*ppw->mond_nu*y[ppw->pv->index_pt_phi] - 4.5*a2*ppw->rho_plus_p_shear; /* L183 */")])
# sources: phi_N -> nu*phi_N inside perturbations_sources only
s = open(P).read(); a = s.index("int perturbations_sources("); b = s.index("int perturbations_print_variables(")
seg = s[a:b]; n = len(re.findall(r"(?<!d)y\[ppw->pv->index_pt_phi\]", seg)); assert n == 6, f"sources: expected 6 uses of phi (excluding dy[phi]), found {n}"
seg = re.sub(r"(?<!d)y\[ppw->pv->index_pt_phi\]", "(ppw->mond_nu*y[ppw->pv->index_pt_phi])", seg)
s = s[:a] + seg + s[b:]
# initialise mond_nu = 1 at the top of perturbations_einstein (synchronous-gauge runs never set it)
old = "int perturbations_einstein("; i = s.index(old); j = s.index("{", i); s = s[:j+1] + "\n  ppw->mond_nu = 1.; /* L183 */" + s[j+1:]
open(P, "w").write(s); print("patched OK")
