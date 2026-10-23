#!/usr/bin/env python3
"""C7_aest_class step P: build the AeST-patched CLASS v3.3.4 tree from the pristine tree and write aest.patch.

Usage:  python3 -I c7_make_patch.py PRISTINE_DIR TARGET_DIR [--mutate]
  PRISTINE_DIR = .../_external_data/class_public_v3.3.4_2026_10_22/class_public-3.3.4 (never modified)
  TARGET_DIR   = a new directory (must not exist); the patched tree is copied there and edited.
Without --mutate the unified diff (pristine -> patched, source/include only) is written to aest.patch next to this
script. With --mutate one sign is flipped (the metric-source term of the extra-sector density equation,
FROZEN_CRITERIA V4) and the diff goes to aest_MUTATE.patch.

Every edit is an exact-anchor string edit that must match exactly once. The extra sector's linear equations live in
one C function, perturbations_aest_rhs(), and its background in background_aest_K(); a Khronon-dust variant replaces
those two functions. Equations: c7_derive.py (checks D2-D6), compact forms D5/D6, ICs IC_cform.
"""
import difflib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pristine, target = sys.argv[1], sys.argv[2]
MUT = "--mutate" in sys.argv
assert os.path.isdir(pristine) and not os.path.exists(target)
shutil.copytree(pristine, target)

EDITS = []


def edit(path, anchor, new, mode="after"):
    EDITS.append((path, anchor, new, mode))


# ------------------------------------------------------------------------------------------------ background.h
edit("include/background.h",
     "  double Omega0_cdm;      /**< \\f$ \\Omega_{0 cdm} \\f$: cold dark matter */\n",
     """  /* C7_aest_class: AeST extra sector (Skordis & Zlosnik, arXiv:2007.00082) */
  double Omega0_aest;     /**< present density of the AeST sector (set by the shift charge I0: FITTED initial condition) */
  int aest_K_type;        /**< 0 exact dust limit (K2 -> infinity), 1 Cosh, 2 Exp, 3 quadratic */
  double aest_K_B;        /**< K_B (vector kinetic coefficient) */
  double aest_Q0;         /**< Q0 in Mpc^-1 */
  double aest_K2;         /**< K2 (dimensionless) */
  double aest_Z0;         /**< Z0 in Mpc^-1 (Cosh, Exp) */
  double aest_lambda_c;   /**< F_Y/(2-K_B) at Y = 0 on FRW (premise P-F: 0 in all runs) */
  double aest_g;          /**< G_cosmo/G_N (premise P-g; 1 = paper convention) */
  double aest_I0;         /**< shift charge a^3 K'(Q) in Mpc^-1, solved from Omega0_aest */
""")
edit("include/background.h", "  int index_bg_rho_cdm;       /**< cdm density */\n",
     """  int index_bg_rho_aest;      /**< AeST sector density (units 8piG/3) */
  int index_bg_p_aest;        /**< AeST sector pressure */
  int index_bg_Q_aest;        /**< Qbar = A^mu d_mu phi (Mpc^-1) */
  int index_bg_Kz_aest;       /**< K(Qbar) (Mpc^-2), constant -2 Lambda moved to Omega_Lambda */
  int index_bg_Kp_aest;       /**< K'(Qbar) = I0/a^3 (Mpc^-1) */
  int index_bg_ca2_aest;      /**< adiabatic sound speed K'/(Q K'') */
""")
edit("include/background.h", "  short has_cdm;       /**< presence of cold dark matter? */\n",
     "  short has_aest;      /**< presence of the AeST extra sector? */\n")
edit("include/background.h", "  int background_w_fld(",
     """  int background_aest_K(struct background * pba, double a, double * Q, double * Kz, double * Kp, double * ca2);

  int background_aest_solve_I0(struct background * pba);

""", mode="before")

# ------------------------------------------------------------------------------------------------ background.c
edit("source/background.c",
     "    rho_m += pvecback[pba->index_bg_rho_cdm];\n  }\n",
     """
  /* AeST extra sector (C7): 8piG~ rho = Q K' - K, 8piG~ p = K (SZ21); CLASS stores 8piG rho/3 */
  if (pba->has_aest == _TRUE_) {
    double Qa, Kza, Kpa, ca2a;
    class_call(background_aest_K(pba,a,&Qa,&Kza,&Kpa,&ca2a),
               pba->error_message,
               pba->error_message);
    pvecback[pba->index_bg_Q_aest] = Qa;
    pvecback[pba->index_bg_Kz_aest] = Kza;
    pvecback[pba->index_bg_Kp_aest] = Kpa;
    pvecback[pba->index_bg_ca2_aest] = ca2a;
    pvecback[pba->index_bg_rho_aest] = (Qa*Kpa - Kza)/3.;
    pvecback[pba->index_bg_p_aest] = Kza/3.;
    rho_tot += pvecback[pba->index_bg_rho_aest];
    p_tot += pvecback[pba->index_bg_p_aest];
    dp_dloga += -ca2a*Qa*Kpa;   /* dK/dlna = K' dQ/dlna = -3 ca2 Q K' ; p = K/3 */
    rho_m += pvecback[pba->index_bg_rho_aest];
  }
""")
edit("source/background.c", "  class_define_index(pba->index_bg_rho_cdm,pba->has_cdm,index_bg,1);\n",
     """  class_define_index(pba->index_bg_rho_aest,pba->has_aest,index_bg,1);
  class_define_index(pba->index_bg_p_aest,pba->has_aest,index_bg,1);
  class_define_index(pba->index_bg_Q_aest,pba->has_aest,index_bg,1);
  class_define_index(pba->index_bg_Kz_aest,pba->has_aest,index_bg,1);
  class_define_index(pba->index_bg_Kp_aest,pba->has_aest,index_bg,1);
  class_define_index(pba->index_bg_ca2_aest,pba->has_aest,index_bg,1);
""")
edit("source/background.c", "  if (pba->Omega0_cdm != 0.)\n    pba->has_cdm = _TRUE_;\n",
     """
  pba->has_aest = _FALSE_;
  if (pba->Omega0_aest != 0.)
    pba->has_aest = _TRUE_;
""")
edit("source/background.c",
     "  /** - check that input parameters make sense and write additional information about them */\n",
     """  /** - AeST extra sector: solve the shift charge I0 from Omega0_aest (C7) */
  class_call(background_aest_solve_I0(pba),
             pba->error_message,
             pba->error_message);

""", mode="before")
edit("source/background.c", "    pba->Omega0_nfsm += pba->Omega0_cdm;\n",
     "  if (pba->has_aest == _TRUE_)\n    pba->Omega0_nfsm += pba->Omega0_aest;\n")
edit("source/background.c",
     "      class_print_species(\"Decaying Cold Dark Matter\",dcdm);\n      budget_matter+=pba->Omega0_dcdm;\n    }\n",
     """    if (pba->has_aest == _TRUE_) {
      class_print_species("AeST sector (C7)",aest);
      budget_matter+=pba->Omega0_aest;
    }
""")
edit("source/background.c", "int background_w_fld(\n", r"""/**
 * C7_aest_class: background of the AeST extra sector (SZ21, arXiv:2007.00082). Single place where K(Q) lives.
 * K'(Qbar) = I0/a^3 (shift charge, an initial condition). Returns Qbar, K, K' and c_ad^2 = K'/(Q K'').
 * A Khronon-dust variant would replace this function (and perturbations_aest_rhs()).
 */
int background_aest_K(
                      struct background * pba,
                      double a,
                      double * Q,
                      double * Kz,
                      double * Kp,
                      double * ca2
                      ) {
  double I0 = pba->aest_I0, Q0 = pba->aest_Q0, K2 = pba->aest_K2, Z0 = pba->aest_Z0;
  double kp = I0/(a*a*a), s, Z, y, lny, g, gp, dZ;
  int it;

  *Kp = kp;
  switch (pba->aest_K_type) {
  case 0: /* exact dust limit: K2 -> infinity at fixed Q0, I0 */
    *Q = Q0;
    *Kz = 0.;
    *ca2 = 0.;
    break;
  case 1: /* Cosh: K = 2 K2 Z0^2 [cosh(Z) - 1], Z = (Q-Q0)/Z0; K' = 2 K2 Z0 sinh Z */
    s = kp/(2.*K2*Z0);
    Z = asinh(s);
    *Q = Q0 + Z0*Z;
    *Kz = 2.*K2*Z0*Z0*s*s/(sqrt(1.+s*s)+1.);
    *ca2 = kp/((*Q)*2.*K2*sqrt(1.+s*s));
    break;
  case 2: /* Exp: K = 2 K2 Z0^2 [exp(Z^2) - 1]; K' = 4 K2 Z0 Z exp(Z^2); K'' = 4 K2 (1+2Z^2) exp(Z^2) */
    y = kp/(4.*K2*Z0);
    if (y < 1.) {
      Z = y;
      for (it=0; it<100; it++) {
        g = Z*exp(Z*Z) - y;
        gp = exp(Z*Z)*(1.+2.*Z*Z);
        dZ = g/gp;
        Z -= dZ;
        if (fabs(dZ) < 1.e-15*fabs(Z)) break;
      }
    }
    else {
      lny = log(y);
      Z = sqrt(lny) > 0.5 ? sqrt(lny) : 0.5;
      for (it=0; it<100; it++) {
        g = Z*Z + log(Z) - lny;
        gp = 2.*Z + 1./Z;
        dZ = g/gp;
        Z -= dZ;
        if (fabs(dZ) < 1.e-15*fabs(Z)) break;
      }
    }
    *Q = Q0 + Z0*Z;
    *Kz = 2.*K2*Z0*Z0*expm1(Z*Z);
    *ca2 = Z0*Z/((*Q)*(1.+2.*Z*Z));
    break;
  case 3: /* quadratic: K = K2 (Q-Q0)^2 */
    *Q = Q0 + kp/(2.*K2);
    *Kz = kp*kp/(4.*K2);
    *ca2 = kp/((*Q)*2.*K2);
    break;
  default:
    class_stop(pba->error_message,"aest_K_type = %d not coded (0 dust, 1 cosh, 2 exp, 3 quadratic)",pba->aest_K_type);
  }
  return _SUCCESS_;
}

/**
 * C7_aest_class: solve the shift charge I0 so that 8piG~ rho_aest(a=1) = 3 Omega0_aest H0^2 (Omega0_aest is FITTED).
 * d(Q K' - K)/dI0 = Q at a = 1, so Newton converges from the dust guess I0 = 3 Omega H0^2 / Q0.
 */
int background_aest_solve_I0(
                             struct background * pba
                             ) {
  double target, I0, Q, Kz, Kp, ca2, f = 0.;
  int it;

  if (pba->has_aest == _FALSE_)
    return _SUCCESS_;

  class_test((pba->aest_K_B <= 0.) || (pba->aest_K_B >= 2.),
             pba->error_message,
             "AeST needs 0 < K_B < 2 (SZ21 vector stability); got %e",pba->aest_K_B);
  class_test(pba->aest_Q0 <= 0.,pba->error_message,"AeST needs Q0 > 0");
  class_test((pba->aest_K_type != 0) && (pba->aest_K2 <= 0.),pba->error_message,"AeST needs K2 > 0");
  class_test(((pba->aest_K_type == 1) || (pba->aest_K_type == 2)) && (pba->aest_Z0 <= 0.),
             pba->error_message,"AeST Cosh/Exp need Z0 > 0");

  target = 3.*pba->Omega0_aest*pba->H0*pba->H0;
  I0 = target/pba->aest_Q0;
  for (it=0; it<200; it++) {
    pba->aest_I0 = I0;
    class_call(background_aest_K(pba,1.,&Q,&Kz,&Kp,&ca2),
               pba->error_message,
               pba->error_message);
    f = Q*Kp - Kz - target;
    if (fabs(f) < 1.e-15*target) break;
    I0 -= f/Q;
  }
  class_test(fabs(f) > 1.e-12*target,
             pba->error_message,
             "could not solve for the AeST shift charge I0 (residual %e)",f/target);
  pba->aest_I0 = I0;
  if (pba->background_verbose > 1)
    printf(" -> AeST: K_type=%d, I0 = %.10e Mpc^-1, Q(1) = %.10e, ca2(1) = %e\n",pba->aest_K_type,I0,Q,ca2);
  return _SUCCESS_;
}

""", mode="before")

# ------------------------------------------------------------------------------------------------ input.c
edit("source/input.c", "  /** 1) Omega_0_g (photons) and T_cmb */\n",
     """  /** 0) AeST extra sector (C7_aest_class); read first because aest_g rescales Omega0_g (premise P-g) */
  class_read_double("aest_g",pba->aest_g);
  class_read_double("aest_K_B",pba->aest_K_B);
  class_read_double("aest_Q0",pba->aest_Q0);
  class_read_double("aest_K2",pba->aest_K2);
  class_read_double("aest_Z0",pba->aest_Z0);
  class_read_double("aest_lambda_c",pba->aest_lambda_c);
  class_read_int("aest_K_type",pba->aest_K_type);
  class_test(pba->aest_g <= 0.,errmsg,"aest_g = G_cosmo/G_N must be > 0");

""", mode="before")
edit("source/input.c",
     "  if (class_none_of_three(flag1,flag2,flag3)){\n    pba->Omega0_g = (4.*sigma_B/_c_*pow(pba->T_cmb,4.))/",
     "  if (class_none_of_three(flag1,flag2,flag3)){\n    pba->Omega0_g = pba->aest_g*(4.*sigma_B/_c_*pow(pba->T_cmb,4.))/",
     mode="replace")
edit("source/input.c",
     "      pba->Omega0_g = (4.*sigma_B/_c_*pow(param1,4.))/",
     "      pba->Omega0_g = pba->aest_g*(4.*sigma_B/_c_*pow(param1,4.))/", mode="replace")
edit("source/input.c",
     "  class_test(pba->Omega0_cdm<0,errmsg, \"You cannot set the cold dark matter density to negative values.\");\n",
     """
  /** 3b) AeST extra sector density (C7): Omega_aest or omega_aest (FITTED initial condition I0) */
  class_call(parser_read_double(pfc,"Omega_aest",&param1,&flag1,errmsg),
             errmsg,
             errmsg);
  class_call(parser_read_double(pfc,"omega_aest",&param2,&flag2,errmsg),
             errmsg,
             errmsg);
  class_test(((flag1 == _TRUE_) && (flag2 == _TRUE_)),
             errmsg,
             "You can only enter one of 'Omega_aest' or 'omega_aest'.");
  if (flag1 == _TRUE_)
    pba->Omega0_aest = param1;
  if (flag2 == _TRUE_)
    pba->Omega0_aest = param2/pba->h/pba->h;
  class_test(pba->Omega0_aest<0,errmsg,"Omega_aest must be >= 0");
""")
edit("source/input.c", "  Omega_tot += pba->Omega0_cdm;\n", "  Omega_tot += pba->Omega0_aest;\n")
edit("source/input.c", "  pba->Omega0_dcdmdr = 0.0;\n",
     """  /* AeST extra sector (C7): off by default */
  pba->Omega0_aest = 0.;
  pba->aest_K_type = 0;
  pba->aest_K_B = 0.5;
  pba->aest_Q0 = 0.1;
  pba->aest_K2 = 1.;
  pba->aest_Z0 = 1.e-9;
  pba->aest_lambda_c = 0.;
  pba->aest_g = 1.;
  pba->aest_I0 = 0.;
""")

# ------------------------------------------------------------------------------------------------ thermodynamics.c
edit("source/thermodynamics.c",
     "pth->n_e = 3.*pow(pba->H0 * _c_ / _Mpc_over_m_,2)*pba->Omega0_b/(8.*_PI_*_G_*_m_H_)*(1.-pth->YHe);",
     "pth->n_e = 3.*pow(pba->H0 * _c_ / _Mpc_over_m_,2)*pba->Omega0_b/(8.*_PI_*_G_*pba->aest_g*_m_H_)*(1.-pth->YHe);",
     mode="replace")
edit("source/thermodynamics.c",
     "ptw->SIunit_nH0 = 3.*ptw->SIunit_H0*ptw->SIunit_H0*pba->Omega0_b/(8.*_PI_*_G_*_m_H_)*(1.-ptw->YHe);",
     "ptw->SIunit_nH0 = 3.*ptw->SIunit_H0*ptw->SIunit_H0*pba->Omega0_b/(8.*_PI_*_G_*pba->aest_g*_m_H_)*(1.-ptw->YHe);",
     mode="replace")
edit("source/thermodynamics.c", "  DeltaNeff = Neff_bbn - 3.046;\n",
     "  DeltaNeff = Neff_bbn - 3.046 + 43./7.*(pba->aest_g - 1.); /* C7 premise P-g: H_BBN^2 scales with g, g* = 10.75 */\n",
     mode="replace")
edit("source/thermodynamics.c", "  omega_b=pba->Omega0_b*pba->h*pba->h;\n",
     "  omega_b=pba->Omega0_b*pba->h*pba->h/pba->aest_g; /* C7 premise P-g: baryon number in G_N units */\n",
     mode="replace")

# ------------------------------------------------------------------------------------------------ perturbations.h
edit("include/perturbations.h", "  int index_pt_theta_dcdm; /**< dcdm velocity */\n",
     """  int index_pt_delta_aest; /**< AeST sector density contrast (C7) */
  int index_pt_theta_aest; /**< AeST sector velocity divergence */
  int index_pt_E_aest;     /**< AeST vector E = F_0x/a (gauge-invariant) */
  int index_pt_chi_aest;   /**< AeST chi = phi + Q alpha (gauge-invariant) */
""")

# ------------------------------------------------------------------------------------------------ perturbations.c
cont = "(theta - metric_continuity)" if MUT else "(theta + metric_continuity)"
edit("source/perturbations.c", '#include "parallel.h"\n', r"""
/**
 * C7_aest_class: the AeST extra sector's linear equations (SZ21, arXiv:2007.00082), derived from the covariant
 * action in covariant_push_2026_10_22/C7_aest_class/c7_derive.py (checks D2-D6). Single place where they live;
 * a Khronon-dust variant would replace this function and background_aest_K().
 * y[0..3] = (delta, theta, E, chi); E = F_0x/a and chi = phi + Q alpha are gauge-invariant.
 * gam = ca2 (rho_hat delta + (k/a)^2 [K_B E + (2-K_B) chi]) / K' ;  dp/rho = K' gam / rho_hat
 * delta' = -(1+w)(theta + metric_continuity) - 3H(dp/rho - w delta)
 * theta' = -H(1-3ca2) theta + k^2 (dp/rho)/(1+w) + metric_euler
 * E'     = -H E + (a/K_B){K' chi - (2-K_B)[gam + (H/a + (1+lambda_c) Q) chi - 3 ca2 (H/a) Q alpha]}
 * chi'   = a (gam + Q E) - 3 H ca2 Q alpha,     Q alpha = chi - a Q theta / k^2
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
  double KB = pba->aest_K_B;
  double lc = pba->aest_lambda_c;
  double rho_hat = Q*Kp - Kz;
  double w = Kz/rho_hat;
  double k2 = k*k;
  double delta = y[0], theta = y[1], E = y[2], chi = y[3];
  double qa = chi - a*Q*theta/k2;
  double gam = ca2*(rho_hat*delta + k2/a/a*(KB*E + (2.-KB)*chi))/Kp;
  double Pi = Kp*gam/rho_hat;

  *dp_over_rho = Pi;
  if (dy != NULL) {
    dy[0] = -(1.+w)*""" + cont + r""" - 3.*H*(Pi - w*delta);
    dy[1] = -H*(1.-3.*ca2)*theta + k2*Pi/(1.+w) + metric_euler;
    dy[2] = -H*E + a/KB*(Kp*chi - (2.-KB)*(gam + (H/a + (1.+lc)*Q)*chi - 3.*ca2*H/a*qa));
    dy[3] = a*(gam + Q*E) - 3.*H*ca2*qa;
  }
  return _SUCCESS_;
}

""")
edit("source/perturbations.c",
     "    class_define_index(ppv->index_pt_theta_dcdm,pba->has_dcdm,index_pt,1); /* dcdm velocity */\n",
     """
    /* AeST extra sector (C7): four contiguous variables */
    class_define_index(ppv->index_pt_delta_aest,pba->has_aest,index_pt,1);
    class_define_index(ppv->index_pt_theta_aest,pba->has_aest,index_pt,1);
    class_define_index(ppv->index_pt_E_aest,pba->has_aest,index_pt,1);
    class_define_index(ppv->index_pt_chi_aest,pba->has_aest,index_pt,1);
""")
edit("source/perturbations.c",
     "        ppv->y[ppv->index_pt_theta_dcdm] =\n          ppw->pv->y[ppw->pv->index_pt_theta_dcdm];\n      }\n",
     """
      if (pba->has_aest == _TRUE_) {
        ppv->y[ppv->index_pt_delta_aest] = ppw->pv->y[ppw->pv->index_pt_delta_aest];
        ppv->y[ppv->index_pt_theta_aest] = ppw->pv->y[ppw->pv->index_pt_theta_aest];
        ppv->y[ppv->index_pt_E_aest] = ppw->pv->y[ppw->pv->index_pt_E_aest];
        ppv->y[ppv->index_pt_chi_aest] = ppw->pv->y[ppw->pv->index_pt_chi_aest];
      }
""")
edit("source/perturbations.c",
     "  if (pba->has_dcdm == _TRUE_) {\n    rho_m += ppw->pvecback[pba->index_bg_rho_dcdm];\n  }\n",
     """
  if (pba->has_aest == _TRUE_) {
    rho_m += ppw->pvecback[pba->index_bg_rho_aest];
  }
""")
edit("source/perturbations.c",
     "        /* dcdm velocity velocity vanishes initially in the synchronous gauge */\n\n      }\n",
     """
      /* AeST extra sector (C7): adiabatic IC, c7_derive.py IC1-IC3/IC_cform. Radiation era, leading order,
         w, ca2, Qbar frozen at tau_ini; h = Cn (k tau)^2 with Cn = curvature_ini/2. delta carries CLASS's
         (1 - om tau/5) factor through delta_g, as CDM does; dust limit = CDM IC exactly. */
      if (pba->has_aest == _TRUE_) {
        double Qa = ppw->pvecback[pba->index_bg_Q_aest];
        double Kpa = ppw->pvecback[pba->index_bg_Kp_aest];
        double Kza = ppw->pvecback[pba->index_bg_Kz_aest];
        double c_a = ppw->pvecback[pba->index_bg_ca2_aest];
        double w_a = Kza/(Qa*Kpa - Kza);
        double den_a = 2.+3.*c_a-3.*w_a;
        double Cn = ppr->curvature_ini*s2_squared/2.;
        double th_a = -c_a*Cn*k*ktau_three/((4.-3.*c_a)*den_a);
        double E_a = -Cn*c_a*Qa*Kpa*a*a*k*k*pow(tau,4)/(4.*pba->aest_K_B*(4.-3.*c_a)*den_a);
        double qal_a = -Qa*Cn*c_a*Qa*Kpa*a*a*a*k*k*pow(tau,5)/(20.*pba->aest_K_B*(4.-3.*c_a)*den_a);
        ppw->pv->y[ppw->pv->index_pt_delta_aest] = 3./4.*ppw->pv->y[ppw->pv->index_pt_delta_g]*(1.+w_a)*2./den_a;
        ppw->pv->y[ppw->pv->index_pt_theta_aest] = th_a;
        ppw->pv->y[ppw->pv->index_pt_E_aest] = E_a;
        ppw->pv->y[ppw->pv->index_pt_chi_aest] = a*Qa*th_a/k/k + qal_a;
      }
""")
edit("source/perturbations.c",
     "      if (pba->has_dcdm == _TRUE_){\n        delta_cdm += ppw->pvecback[pba->index_bg_rho_dcdm] * ppw->pv->y[ppw->pv->index_pt_delta_dcdm];\n        rho_cdm += ppw->pvecback[pba->index_bg_rho_dcdm];\n      }\n",
     """      if (pba->has_aest == _TRUE_){
        delta_cdm += ppw->pvecback[pba->index_bg_rho_aest] * ppw->pv->y[ppw->pv->index_pt_delta_aest];
        rho_cdm += ppw->pvecback[pba->index_bg_rho_aest];
      }
""")
edit("source/perturbations.c",
     "      alpha = (eta + 3./2.*a_prime_over_a*a_prime_over_a/k/k/s2_squared*(delta_tot + 3.*a_prime_over_a/k/k*velocity_tot))/a_prime_over_a;\n",
     """      if (pba->has_aest == _TRUE_) {
        velocity_tot += (ppw->pvecback[pba->index_bg_rho_aest]+ppw->pvecback[pba->index_bg_p_aest])/rho_r
          *ppw->pv->y[ppw->pv->index_pt_theta_aest]/(1.+rho_m_over_rho_r);
      }

""", mode="before")
edit("source/perturbations.c",
     "        ppw->pv->y[ppw->pv->index_pt_theta_dcdm] = k*k*alpha;\n      }\n",
     """
      /* AeST (C7): D3 map; E and chi are gauge-invariant */
      if (pba->has_aest == _TRUE_) {
        ppw->pv->y[ppw->pv->index_pt_delta_aest] -= 3.*(1.+ppw->pvecback[pba->index_bg_p_aest]/ppw->pvecback[pba->index_bg_rho_aest])*a_prime_over_a*alpha;
        ppw->pv->y[ppw->pv->index_pt_theta_aest] += k*k*alpha;
      }
""")
edit("source/perturbations.c",
     "        rho_plus_p_theta_m += ppw->pvecback[pba->index_bg_rho_dcdm]*y[ppw->pv->index_pt_theta_dcdm]; // contribution to [(rho+p)theta]_matter\n        rho_plus_p_m += ppw->pvecback[pba->index_bg_rho_dcdm];\n      }\n    }\n",
     """
    /* AeST extra sector contribution (C7) */
    if (pba->has_aest == _TRUE_) {
      double rho_a = ppw->pvecback[pba->index_bg_rho_aest];
      double rpp_a = rho_a + ppw->pvecback[pba->index_bg_p_aest];
      double dpr_a;
      perturbations_aest_rhs(pba,k,ppw->pvecback,0.,0.,&(y[ppw->pv->index_pt_delta_aest]),NULL,&dpr_a);
      ppw->delta_rho += rho_a*y[ppw->pv->index_pt_delta_aest];
      ppw->rho_plus_p_theta += rpp_a*y[ppw->pv->index_pt_theta_aest];
      ppw->delta_p += rho_a*dpr_a;
      ppw->rho_plus_p_tot += rpp_a;

      if (ppt->has_source_delta_m == _TRUE_) {
        delta_rho_m += rho_a*y[ppw->pv->index_pt_delta_aest];
        rho_m += rho_a;
      }
      if ((ppt->has_source_delta_m == _TRUE_) || (ppt->has_source_theta_m == _TRUE_)) {
        rho_plus_p_theta_m += rpp_a*y[ppw->pv->index_pt_theta_aest];
        rho_plus_p_m += rpp_a;
      }
    }
""")
edit("source/perturbations.c", "    /** - ---> interacting dark radiation */\n    if (pba->has_idr == _TRUE_){\n",
     """    /** - ---> AeST extra sector (C7) */
    if (pba->has_aest == _TRUE_) {
      double dpr_a;
      perturbations_aest_rhs(pba,k,pvecback,metric_continuity,metric_euler,
                             &(y[pv->index_pt_delta_aest]),&(dy[pv->index_pt_delta_aest]),&dpr_a);
    }

""", mode="before")
edit("source/perturbations.c",
     "      Nnow = 3.*H0*H0*pba->Omega0_b*(1.-pth->YHe)/(8.*_PI_*_G_*_m_H_);",
     "      Nnow = 3.*H0*H0*pba->Omega0_b*(1.-pth->YHe)/(8.*_PI_*_G_*pba->aest_g*_m_H_);", mode="replace")

# ------------------------------------------------------------------------------------------------ apply
for path, anchor, new, mode in EDITS:
    fp = os.path.join(target, path)
    s = open(fp).read()
    n = s.count(anchor)
    assert n == 1, f"anchor matched {n} times in {path}: {anchor[:80]!r}"
    if mode == "after":
        s = s.replace(anchor, anchor + new)
    elif mode == "before":
        s = s.replace(anchor, new + anchor)
    elif mode == "replace":
        s = s.replace(anchor, new)
    open(fp, "w").write(s)
print(f"applied {len(EDITS)} edits to {target}{' (MUTATE)' if MUT else ''}")

# ------------------------------------------------------------------------------------------------ diff
out = []
for sub in ("include", "source"):
    for fn in sorted(os.listdir(os.path.join(pristine, sub))):
        a_ = open(os.path.join(pristine, sub, fn)).read().splitlines(keepends=True)
        b_ = open(os.path.join(target, sub, fn)).read().splitlines(keepends=True)
        if a_ != b_:
            out.extend(difflib.unified_diff(a_, b_, fromfile=f"a/{sub}/{fn}", tofile=f"b/{sub}/{fn}"))
pname = os.path.join(HERE, "aest_MUTATE.patch" if MUT else "aest.patch")
open(pname, "w").write("".join(out))
print(f"wrote {pname}: {sum(1 for l in out if l.startswith('+') and not l.startswith('+++'))} added lines, "
      f"{sum(1 for l in out if l.startswith('-') and not l.startswith('---'))} removed lines")
