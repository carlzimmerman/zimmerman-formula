#!/usr/bin/env python3
"""
AS263 -- Tier-0b: derive the time-dependent projector commutator [d_tau, P_h]Z
=============================================================================
Framing (FINAL_ACTION.md eq. (10), occupied/RESULT.md): the varied intrinsic
(volume) mean is <A>_h = (int sqrt(h) A)/(int sqrt(h))  -- NOT lapse-weighted --
and the mean-zero projector is P_h A = A - <A>_h with int sqrt(h) P_h A = 0.

Normal convention (adopted): foliation time derivative along the future unit
normal flow, d/dtau = N n (zero shift).  Volume-element transport:
d(sqrt h)/dtau = N K sqrt(h).

Claims under test (derived in derivation.md):

    d<Z>_h/dtau = <N (n Z + K z)>_h,    z := P_h Z = Z - <Z>_h            (E1)
    [d_tau, P_h] Z = -<N K z>_h = -Cov_h(N K, Z)                          (C1)

C1 follows from E1 by differentiating numerator and denominator of the mean;
the commutator is a leaf-constant function with value -<NKz>_h.

Checks run on TWO sectors: exact-homogeneous (N=1, K=3H0 const, sqrt(h0)=1)
and small inhomogeneous lapse/expansion perturbation on the 3-torus with the
analytic transport constraint d sqrt(h)/dtau = N K sqrt(h).
"""

import json, math, time, signal, sys
import numpy as np

# ---------------------------------------------------------------- bounds ----
class BoundKill(Exception):
    pass

def _alarm(sig, frm):
    raise BoundKill("wall-time alarm fired")

signal.signal(signal.SIGALRM, _alarm)
signal.alarm(118)                # declared bound: <= 120 s wall, hard stop 118 s

t_start = time.time()

# ------------------------------------------------------------ constants ----
G   = 6.67430e-11        # m^3 kg^-1 s^-2 (SI, mandated)
c   = 299792458.0        # m/s
M_S = 1.98847e30         # kg
PC  = 3.085677581491367e16  # m
A0_CAN = 9.3619e-11      # m/s^2 canonical footing
A0_ALT = 1.1279e-10      # m/s^2 alternative footing

def rho_lambda(a0):
    return 4.0 * a0 ** 2 / (G * c ** 2)   # kg/m^3, a0 = kappa c sqrt(G rho), kappa=1/2

RHO_CAN = rho_lambda(A0_CAN)
RHO_ALT = rho_lambda(A0_ALT)
KAPPA_EFF_FIXED_RHO = A0_ALT / (c * math.sqrt(G * RHO_CAN))

def r_M(Mb):
    return math.sqrt(G * Mb / A0_CAN), math.sqrt(G * Mb / A0_ALT)

# ------------------------------------------------------------ domain data ----
NX = 24                      # 24^3 torus grid (13824 points)
x1 = np.arange(NX) * 2.0 * math.pi / NX
X1, X2, X3 = np.meshgrid(x1, x1, x1, indexing='ij')

H0 = 0.70                    # homogeneous expansion (code units; identity dimensionless)
T0 = 0.37                    # evaluation time

# analytic leaf data (band-limited trig; smooth on T^3)
def dNf(X1, X2, X3):
    return 0.02 * np.cos(3 * X1 - X2) * np.sin(2 * X3) + 0.01 * np.sin(4 * X1 + X3)

def dKf(X1, X2, X3):
    return 0.10 * np.cos(2 * X1) * np.cos(X2) * np.sin(X3) + 0.05 * np.sin(5 * X2 - X1)

def dvf(X1, X2, X3):
    return 0.03 * np.cos(2 * X1 + 3 * X2) * np.sin(X3)

# field with explicit time dependence (d_tau Z = N n Z under the normal convention)
def Zf(t, X1, X2, X3):
    return (np.cos(2 * X1 + 0.30 * t)
            + 0.40 * np.sin(3 * X2 - 0.10 * t) * np.cos(X3 + 0.20 * t)
            + 0.20 * np.cos(t) * np.cos(4 * X1 - 2 * X3))

def dZf(t, X1, X2, X3):      # d Z / d tau
    return (-0.30 * np.sin(2 * X1 + 0.30 * t)
            - 0.40 * 0.10 * np.cos(3 * X2 - 0.10 * t) * np.cos(X3 + 0.20 * t)
            - 0.40 * np.sin(3 * X2 - 0.10 * t) * 0.20 * np.sin(X3 + 0.20 * t)
            - 0.20 * np.sin(t) * np.cos(4 * X1 - 2 * X3))

def leaf_density(sqrt_h0, N, K, tau):
    """exact transport solution of d/dtau sqrt(h) = N*K*sqrt(h)."""
    return sqrt_h0 * np.exp(N * K * tau)

def means(sqrt_h, f):
    """varied intrinsic (volume) mean <f>_h = sum sqrt(h) f / sum sqrt(h)."""
    return np.sum(sqrt_h * f) / np.sum(sqrt_h)

def cov_h(sqrt_h, a, b):
    return means(sqrt_h, a * b) - means(sqrt_h, a) * means(sqrt_h, b)

# ------------------------------------------------------------------ checks ----
def run_checks():
    out = {}
    # ---- the two sectors ----
    N_h = np.ones_like(X1);          K_h = (3.0 * H0) * np.ones_like(X1)
    sh0_h = np.ones_like(X1);        sh_h = lambda t: leaf_density(sh0_h, N_h, K_h, t)

    N_p = 1.0 + dNf(X1, X2, X3);     K_p = 3.0 * H0 + dKf(X1, X2, X3)
    sh0_p = 1.0 + dvf(X1, X2, X3);   sh_p = lambda t: leaf_density(sh0_p, N_p, K_p, t)

    eps_list = [1e-3, 1e-4, 1e-5]

    # ---- C0: volume-element transport (base foliation datum) ----
    c0 = {}
    for tag, shf, Nf_, Kf_ in (("hom", sh_h, N_h, K_h), ("pert", sh_p, N_p, K_p)):
        e = 1e-5
        fd = (shf(T0 + e) - shf(T0 - e)) / (2 * e)
        ex = Nf_ * Kf_ * shf(T0)
        c0[tag] = {"rel_residual": float(np.max(np.abs(fd - ex) / np.abs(ex)))}
    out["C0_volume_transport"] = c0

    entries = {}
    for tag, shf, Nf_, Kf_ in (("hom", sh_h, N_h, K_h), ("pert", sh_p, N_p, K_p)):
        Zt0  = Zf(T0, X1, X2, X3)
        dZt0 = dZf(T0, X1, X2, X3)
        sht0 = shf(T0)
        mZ = means(sht0, Zt0)
        z  = Zt0 - mZ
        nZ = dZt0 / Nf_                     # normal derivative: n Z = N^-1 d_tau Z
        NK = Nf_ * Kf_

        # ---- C1: mean-derivative identity (E1); LHS: central FD of <Z> ----
        res_e1 = []
        for e in eps_list:
            lhs = (means(shf(T0 + e), Zf(T0 + e, X1, X2, X3))
                   - means(shf(T0 - e), Zf(T0 - e, X1, X2, X3))) / (2 * e)
            rhs = means(sht0, Nf_ * (nZ + Kf_ * z))
            res_e1.append(float(abs(lhs - rhs)))

        # ---- C2: quotient rule directly on numerator / denominator ----
        I = lambda t: np.sum(shf(t) * Zf(t, X1, X2, X3))
        W = lambda t: np.sum(shf(t))
        e2 = 1e-5
        Ip = (I(T0 + e2) - I(T0 - e2)) / (2 * e2)
        Wp = (W(T0 + e2) - W(T0 - e2)) / (2 * e2)
        quot_rule = (Ip * W(T0) - I(T0) * Wp) / W(T0) ** 2
        rhs2 = means(sht0, Nf_ * (nZ + Kf_ * z))

        # ---- C3: commutator (C1); FD commutation vs closed form ----
        PZ = lambda t: Zf(t, X1, X2, X3) - means(shf(t), Zf(t, X1, X2, X3))
        PdZ = dZt0 - means(sht0, dZt0)
        res_comm = []
        comm_cf = -means(sht0, NK * z)
        for e in eps_list:
            dPZ = (PZ(T0 + e) - PZ(T0 - e)) / (2 * e)
            comm_fd = dPZ - PdZ            # [d_tau, P_h] Z by direct commutation
            comm_cf = -means(sht0, NK * z)  # closed-form C1 (leaf-constant)
            res_comm.append(float(np.max(np.abs(comm_fd - comm_cf))))
        dPZf = (PZ(T0 + eps_list[0]) - PZ(T0 - eps_list[0])) / (2 * eps_list[0])
        comm_fd_full = dPZf - PdZ

        entries[tag] = {
            "E1_residual_FD_central": res_e1,
            "C2_quotient_rule_residual": float(abs(quot_rule - rhs2)),
            "C3_commutator_residual_FD_central": res_comm,
            "C3_commutator_is_leaf_constant": float(
                np.std(comm_fd_full) / (np.max(np.abs(comm_fd_full)) + 1e-30)),
            "C3_covariance_form_match": float(
                abs(means(sht0, NK * z) - cov_h(sht0, NK, Zt0))),
            "C3_commutator_value": float(-means(sht0, NK * z)),
            # ---- C6: negative control -- naive freeze (commute = 0) vs formula ----
            "C6_naive_freeze_residual": float(np.max(np.abs(comm_fd_full))),
            "C6_formula_residual": float(np.max(np.abs(comm_fd_full - comm_cf))),
            # ---- C7: covariance decomposition (terms surviving beyond homogeneity) ----
            "C7_cov_decomp_residual": float(abs(
                cov_h(sht0, NK, Zt0)
                - (3.0 * H0 * cov_h(sht0, Nf_ - 1.0, Zt0)
                   + cov_h(sht0, Kf_ - 3.0 * H0, Zt0)
                   + cov_h(sht0, (Nf_ - 1.0) * (Kf_ - 3.0 * H0), Zt0)))),
        }
    out["C1_C2_C3_C6_C7"] = entries

    # ---- C4: spatially constant test field Z = 7.3 ----
    C4 = {}
    for tag, shf, Nf_, Kf_ in (("hom", sh_h, N_h, K_h), ("pert", sh_p, N_p, K_p)):
        C = 7.3
        e = 1e-5
        PZc = lambda t: C - means(shf(t), C * np.ones_like(X1))
        dPZc = (PZc(T0 + e) - PZc(T0 - e)) / (2 * e)
        C4[tag] = {
            "commutator_FD_maxabs": float(np.max(np.abs(dPZc))),
            "closed_form": float(-means(shf(T0), Nf_ * Kf_ * (C - C))),
        }
    out["C4_constant_field"] = C4

    # ---- C5: exact-homogeneity sector; mean-zero AND mean-nonzero test fields ----
    C5 = {}
    for mz, name in ((0.0, "mean_zero"), (5.0, "mean_nonzero")):
        def Zz(t, X1=X1, X2=X2, X3=X3, mz=mz):
            return (mz + np.cos(2 * X1 + 0.3 * t) * np.sin(3 * X2 - 0.1 * t)
                    + 0.2 * np.cos(4 * X1 - 2 * X3 + 0.5 * t))
        def dZz(t):
            return (-0.3 * np.sin(2 * X1 + 0.3 * t) * np.sin(3 * X2 - 0.1 * t)
                    - 0.1 * np.cos(2 * X1 + 0.3 * t) * np.cos(3 * X2 - 0.1 * t)
                    - 0.1 * np.sin(4 * X1 - 2 * X3 + 0.5 * t))
        e = 1e-5
        PZz = lambda t: Zz(t) - means(sh_h(t), Zz(t))
        dPZz = (PZz(T0 + e) - PZz(T0 - e)) / (2 * e)
        PdZz = dZz(T0) - means(sh_h(T0), dZz(T0))
        comm = dPZz - PdZz
        zz = Zz(T0) - means(sh_h(T0), Zz(T0))
        C5[name] = {
            "commutator_maxabs_FD": float(np.max(np.abs(comm))),
            "closed_form": float(-means(sh_h(T0), N_h * K_h * zz)),
        }
    out["C5_exact_homogeneity"] = C5

    # ---- C8: auxiliary time-stepper -- the mean-preserving correction term ----
    ev = {}
    for tag, shf, Nf_, Kf_ in (("pert", sh_p, N_p, K_p),):
        Nsteps, dt = 200, 2e-3
        drift = 0.0
        zk = Zf(T0, X1, X2, X3) - means(shf(T0), Zf(T0, X1, X2, X3))
        zk_naive = zk.copy()
        mean_ev, mean_naive = [], []
        for k in range(Nsteps):
            t = T0 + k * dt
            st = shf(t)
            Zt = Zf(t, X1, X2, X3)
            dZt = dZf(t, X1, X2, X3)
            PnZ = dZt - means(st, dZt)                # P_h(d_tau Z) on the current leaf
            cfl = -means(st, Nf_ * Kf_ * zk)          # commutator term -<NK z>
            zk = zk + dt * (PnZ + cfl)                # corrected update (from C1)
            zk_naive = zk_naive + dt * PnZ            # naive (term omitted)
            mean_ev.append(float(means(st, zk)))
            mean_naive.append(float(means(st, zk_naive)))
            drift += dt * means(st, Nf_ * Kf_ * (Zt - means(st, Zt)))
        ev[tag] = {
            "final_mean_corrected": mean_ev[-1],
            "final_mean_naive": mean_naive[-1],
            "max_abs_mean_corrected": float(max(map(abs, mean_ev))),
            "naive_drift_expectation": float(-drift),
        }
    out["C8_mean_preserving_solver"] = ev
    return out

def run_symbolic():
    """Exact (symbolic) verification of E1 and C1 on a 1D circle with trig data.

    Strategy: the transport solution of d(sqrt h)/dtau = N K sqrt(h) with
    (N,K) tau-independent is sqrt(h)(tau) = sq * exp(N K tau).  The identities
    E1/C1 are pointwise in tau; evaluating at tau = 0 the volume data reduce to
    sqrt(h)(0) = sq and d sqrt(h)/dtau |_0 = N K sq, so every integral is an
    elementary trig product and the check is EXACT (no truncation in the
    perturbation amplitudes eN, eK, eZ; residual must simplify to 0).
    """
    import sympy as sp
    tau, x, H, eN, eK, eZ = sp.symbols("tau x H eN eK eZ", positive=True)
    N = 1 + eN * sp.sin(3 * x)
    K = 3 * H + eK * sp.cos(2 * x)
    sq = 1 + sp.Rational(1, 20) * sp.cos(2 * x)        # sqrt(h)(0,x)
    Z = sp.cos(2 * x + eZ * tau) + sp.Rational(3, 10) * sp.sin(3 * x) * sp.cos(tau)
    dZdtau = sp.simplify(sp.diff(Z, tau))

    def mean(f):
        """<f>_h at tau=0: (int sq f)/(int sq), all on the circle."""
        I = sp.integrate(sp.expand(sq * f), (x, 0, 2 * sp.pi))
        W = sp.integrate(sq, (x, 0, 2 * sp.pi))
        return sp.simplify(I / W)

    Z0 = sp.simplify(Z.subs(tau, 0))
    Zp = sp.simplify(dZdtau.subs(tau, 0))
    mZ = mean(Z0)                                  # <Z>(0)
    z = sp.simplify(Z0 - mZ)                       # z = P_h Z at tau=0
    # E1 at tau=0:  d<Z>/dtau = <N(nZ+Kz)> = <Zp + N*K*z>   (uses d(sqrt h)/dtau = NK sqrt h)
    dmd = sp.simplify(mean(Zp + N * K * z))
    # independent side: differentiate numerator I(tau)=int sqrt(h)(tau) Z(tau)
    # and denominator W(tau) at tau = 0:  I'(0) = int(NK sq Z0 + sq Zp), W'(0) = int(NK sq)
    I0 = sp.integrate(sp.expand(sq * Z0), (x, 0, 2 * sp.pi))
    W0 = sp.integrate(sq, (x, 0, 2 * sp.pi))
    Ip = sp.integrate(sp.expand((N * K * sq) * Z0 + sq * Zp), (x, 0, 2 * sp.pi))
    Wp = sp.integrate(sp.expand(N * K * sq), (x, 0, 2 * sp.pi))
    quot = sp.simplify((Ip * W0 - I0 * Wp) / W0 ** 2)
    E1 = sp.simplify(quot - dmd)
    # C1: [d_tau, P_h]Z = d(PZ)/dtau - P(dZ/dt) at tau=0
    PZ = sp.simplify(Z0 - mZ)                      # P_h Z(0) -- the projector at tau=0
    # d(P_h Z)/dtau |_0 = Zp - dmd   (projector depends on tau through h)
    dPZ = sp.simplify(Zp - dmd)
    PdZp = sp.simplify(Zp - mean(Zp))
    comm = sp.simplify(dPZ - PdZp)
    C1 = sp.simplify(comm + mean(N * K * z))
    return {
        "E1_symbolic_residual": str(E1),
        "C1_symbolic_residual": str(C1),
        "commutator_symbolic": sp.sstr(comm),
        "method": "exact trig integration on the circle at tau=0; "
                  "d(sqrt h)/dtau = N*K*sq used, no exp(), no truncation",
    }

def main():
    results = run_checks()
    results["symbolic"] = run_symbolic()
    results["footings"] = {
        "a0_canonical_m_s2": A0_CAN,
        "a0_alternative_m_s2": A0_ALT,
        "rho_Lambda_canonical_kg_m3": RHO_CAN,
        "rho_Lambda_alternative_kg_m3": RHO_ALT,
        "kappa_eff_at_fixed_rho_canonical": KAPPA_EFF_FIXED_RHO,
        "r_M_canonical_1e11Msun_m": r_M(1e11 * M_S)[0],
        "r_M_alternative_1e11Msun_m": r_M(1e11 * M_S)[1],
        "note": "kappa=1/2 ADOPTED; the two footings do not share (rho_Lambda, kappa); "
                "identity (C1) is kinematic/dimensionless and applies under both footings "
                "unchanged; footings enter only through the branch background K = 3H(tau).",
    }
    results["runtime_s"] = time.time() - t_start
    results["bounds"] = {"wall_alarm_s": 118, "memory_cap_MB": 512, "threads": 1}
    try:
        import resource
        results["peak_rss_kb_self"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except Exception:
        results["peak_rss_kb_self"] = None
    print(json.dumps(results, indent=1, default=str))

if __name__ == "__main__":
    try:
        main()
    except BoundKill:
        print(json.dumps({"FATAL": "wall-time alarm fired (118 s)"}))
        sys.exit(2)