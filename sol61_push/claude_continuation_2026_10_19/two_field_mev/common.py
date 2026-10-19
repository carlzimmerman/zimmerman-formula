"""Shared constants for CL-2F-2026-10-19-01 (two-field condensate, MeV continuation).

Units: m = lambda_tot = 1 (fields in m/sqrt(lambda_tot), r in 1/m). The only free
parameter is Gamma = G m^2 / lambda_tot. u_star and r_lambda are held fixed.
"""
import json, math, os, resource, time

U_STAR = 0.02
R_LAMBDA = 2.0
LAM = 1.0
M2 = 4.0 * (1.0 + U_STAR ** 2)            # (M/m)^2
MX = math.sqrt(M2)
DELTA = M2 - 4.0                           # Delta/m^2 = 4 u*^2
G_HAT = math.sqrt(DELTA / (1.0 + R_LAMBDA))  # g/(m sqrt(lambda_tot))
LAM_REP = LAM - G_HAT ** 2 / DELTA          # = 2/3
ZETA = U_STAR ** 2 * R_LAMBDA / (1.0 + R_LAMBDA)
FC_BENCH = 0.009888264649460883            # central f of mixed_G1em8_x04 (branch label)

# Documented physical constants (CODATA/PDG values, natural units)
HBARC_MEV_CM = 1.97326980e-11              # MeV cm
G_PER_MEV = 1.0 / 5.60958860e26            # g per MeV/c^2
G_NEWTON_GEV = 6.70883e-39                 # GeV^-2 (hbar c / (c^2 M_Pl^2))
HBAR_MEV_S = 6.58211957e-22                # MeV s
M_SUN_KG = 1.98841e30
KG_PER_MEV = 1.78266192e-30


def physical_benchmark(m_mev=1.0, sigma_over_m_cm2_g=0.3, u_star=U_STAR, r_lambda=R_LAMBDA):
    """Recompute lambda_tot, g, Gamma_phys from the MASTER document's definitions:
    sigma_0 = lambda_rep^2/(8 pi m^2), lambda_min = g^2/Delta, r_lambda = lambda_rep/lambda_min,
    Delta = 4 m^2 u*^2."""
    cm = 1.0 / HBARC_MEV_CM                # 1 cm in MeV^-1
    gram = 1.0 / G_PER_MEV                 # 1 g in MeV
    sig_m = sigma_over_m_cm2_g * cm ** 2 / gram   # MeV^-3
    lam_rep = math.sqrt(8 * math.pi * m_mev ** 3 * sig_m)
    lam_min = lam_rep / r_lambda
    lam_tot = lam_rep + lam_min
    delta = 4 * m_mev ** 2 * u_star ** 2
    g = math.sqrt(lam_min * delta)         # MeV
    gm2 = G_NEWTON_GEV * (m_mev * 1e-3) ** 2
    gamma = gm2 / lam_tot
    return dict(m_MeV=m_mev, sigma0_over_m_cm2_g=sigma_over_m_cm2_g, lambda_rep=lam_rep,
                lambda_min=lam_min, lambda_tot=lam_tot, g_MeV=g, g_eV=g * 1e6,
                g_hat=g / (m_mev * math.sqrt(lam_tot)), M_over_m=2 * math.sqrt(1 + u_star ** 2),
                G_m2=gm2, Gamma_phys=gamma, four_pi_Gamma=4 * math.pi * gamma)


def tf_point(x):
    """Algebraic two-field TF state at chemical fraction x (d = Omega^2-1 = zeta x).
    Returns d, f^2 (=n), h, charge density/(2 Omega) S=f^2+4h^2."""
    d = ZETA * x
    D = DELTA - 4 * d
    A = LAM * D - G_HAT ** 2
    n = d * D / (2 * A)
    h = G_HAT * n / D
    return d, n, h, n + 4 * h * h


def peak_rss_mb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 2 ** 20 if r > 1e7 else r / 1024.0   # macOS bytes, Linux kB


class Timer:
    def __init__(self):
        self.t0 = time.monotonic()

    def __call__(self):
        return time.monotonic() - self.t0


def dump(path, obj):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w') as fh:
        json.dump(obj, fh, indent=2, default=float)
        fh.write('\n')
