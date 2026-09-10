#!/usr/bin/env python3
"""
L152 -- patch CLASS 3.3.4.0 so the fluid ('fld') rest-frame sound speed can RUN with the scale factor:

    cs2_fld(a) = min( cs2_fld_max ,  cs2_fld * (a / cs2_fld_astar)^cs2_fld_p )

New input parameters (all optional; defaults reproduce stock CLASS exactly):
    cs2_fld_p      (default 0  -> constant cs2_fld, i.e. stock behaviour)
    cs2_fld_astar  (default 1  -> cs2_fld is the value TODAY)
    cs2_fld_max    (default 1  -> causal cap)

The four places where CLASS uses pba->cs2_fld are replaced by cs2_fld_of_a(pba, a):
  (1)(2) adiabatic initial conditions of the fluid, (3) the rest-frame -> gauge pressure transformation in
  perturbations_total_stress_energy, (4) the fluid equations of motion in perturbations_derivs.
(The PPF branch also gets the running value for consistency, but the L152 runs use use_ppf = no.)

Every replacement is asserted to occur EXACTLY ONCE, so a CLASS version drift cannot silently produce a
half-patched build.  Usage:  python3 apply_running_cs2_patch.py <path-to-extracted-classy-3.3.4.0>
"""
import sys, os, re

root = sys.argv[1]
def patch(path, replacements):
    s = open(path).read()
    for old, new in replacements:
        n = s.count(old)
        assert n == 1, f"{path}: expected exactly 1 occurrence of {old[:60]!r}, found {n}"
        s = s.replace(old, new)
    open(path, 'w').write(s)
    print(f"  patched {os.path.relpath(path, root)} ({len(replacements)} edits)")

# ---- background.h: three new struct members ------------------------------------------------------------
patch(os.path.join(root, 'include', 'background.h'), [
    ("  double cs2_fld;",
     "  double cs2_fld;\n"
     "  double cs2_fld_p;     /**< L152: running index, cs2_fld(a) = cs2_fld (a/cs2_fld_astar)^cs2_fld_p (0 = stock) */\n"
     "  double cs2_fld_astar; /**< L152: pivot scale factor of the running sound speed */\n"
     "  double cs2_fld_max;   /**< L152: cap on the running sound speed */"),
])

# ---- input.c: defaults + reading -------------------------------------------------------------------------
patch(os.path.join(root, 'source', 'input.c'), [
    ("  pba->cs2_fld = 1.;",
     "  pba->cs2_fld = 1.;\n  pba->cs2_fld_p = 0.;\n  pba->cs2_fld_astar = 1.;\n  pba->cs2_fld_max = 1.;"),
    ("      class_read_double(\"wa_fld\",pba->wa_fld);\n      class_read_double(\"cs2_fld\",pba->cs2_fld);",
     "      class_read_double(\"wa_fld\",pba->wa_fld);\n      class_read_double(\"cs2_fld\",pba->cs2_fld);\n"
     "      class_read_double(\"cs2_fld_p\",pba->cs2_fld_p);\n"
     "      class_read_double(\"cs2_fld_astar\",pba->cs2_fld_astar);\n"
     "      class_read_double(\"cs2_fld_max\",pba->cs2_fld_max);"),
])

# ---- perturbations.c: helper + four call sites -----------------------------------------------------------
helper = '''
/* L152: fluid rest-frame sound speed as a function of the scale factor (p = 0 restores stock CLASS) */
static double cs2_fld_of_a(struct background * pba, double a) {
  double cs2;
  if (pba->cs2_fld_p == 0.) return pba->cs2_fld;
  cs2 = pba->cs2_fld * pow(a/pba->cs2_fld_astar, pba->cs2_fld_p);
  if (cs2 > pba->cs2_fld_max) cs2 = pba->cs2_fld_max;
  return cs2;
}
'''
pc = os.path.join(root, 'source', 'perturbations.c')
s = open(pc).read()
# insert helper after the last #include line at the top of the file
m = list(re.finditer(r'^#include .*$', s, flags=re.M))[-1]
s = s[:m.end()] + "\n" + helper + s[m.end():]
open(pc, 'w').write(s)
patch(pc, [
    ("          ppw->pv->y[ppw->pv->index_pt_delta_fld] = - ktau_two/4.*(1.+w_fld)*(4.-3.*pba->cs2_fld)/(4.-6.*w_fld+3.*pba->cs2_fld) * ppr->curvature_ini * s2_squared;",
     "          ppw->pv->y[ppw->pv->index_pt_delta_fld] = - ktau_two/4.*(1.+w_fld)*(4.-3.*cs2_fld_of_a(pba,a))/(4.-6.*w_fld+3.*cs2_fld_of_a(pba,a)) * ppr->curvature_ini * s2_squared;"),
    ("          ppw->pv->y[ppw->pv->index_pt_theta_fld] = - k*ktau_three/4.*pba->cs2_fld/(4.-6.*w_fld+3.*pba->cs2_fld) * ppr->curvature_ini * s2_squared;",
     "          ppw->pv->y[ppw->pv->index_pt_theta_fld] = - k*ktau_three/4.*cs2_fld_of_a(pba,a)/(4.-6.*w_fld+3.*cs2_fld_of_a(pba,a)) * ppr->curvature_ini * s2_squared;"),
    ("        ppw->delta_p_fld = pba->cs2_fld * ppw->delta_rho_fld + (pba->cs2_fld-ca2_fld)*(3*a_prime_over_a*ppw->rho_plus_p_theta_fld/k/k);",
     "        ppw->delta_p_fld = cs2_fld_of_a(pba,a) * ppw->delta_rho_fld + (cs2_fld_of_a(pba,a)-ca2_fld)*(3*a_prime_over_a*ppw->rho_plus_p_theta_fld/k/k);"),
    ("        c_gamma_k_H_square = pow(pba->c_gamma_over_c_fld*k/a_prime_over_a,2)*pba->cs2_fld;",
     "        c_gamma_k_H_square = pow(pba->c_gamma_over_c_fld*k/a_prime_over_a,2)*cs2_fld_of_a(pba,a);"),
    ("        cs2 = pba->cs2_fld;",
     "        cs2 = cs2_fld_of_a(pba,a);"),
])
# no stray uses may remain
s = open(pc).read()
left = [l for l in s.splitlines() if 'pba->cs2_fld' in l and 'cs2_fld_of_a' not in l and 'cs2_fld_p' not in l
        and 'cs2_fld_astar' not in l and 'cs2_fld_max' not in l]
assert not left, f"unpatched uses of pba->cs2_fld remain: {left}"
print("  all pba->cs2_fld uses in perturbations.c now go through cs2_fld_of_a(pba,a)")
print("PATCH OK")
