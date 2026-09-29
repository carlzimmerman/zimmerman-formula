#!/usr/bin/env python3
"""Q1-1 -- Dirac fermion in dS_4 (planar patch, constant-energy-density electric field): structure, modes, adiabatic series.

Pre-registered in Q1_PREREGISTRATION.md (with Amendment 1; written before this script was run).  Units H = 1, tau = -1 (a = 1).

Checks: D1 curved-space Dirac equation -> flat system (tetrad + spin connection, sympy) and the 4x4 -> 2x2 block split; D2 the squared equation, the Whittaker index,
and that (e, E, m, H) enter only through (L, M); M1 the Whittaker modes solve the first-order system (both s = +-1, proportional); M2 the modes equal a far-past ODE integration
(Bunch-Davies, both k_perp signs, negative r); M3 the full 4x4 Dirac-sea trace equals the block sum; A1 the Bloch-vector adiabatic series (residual orders, unit norm, error scaling).

Run:     python3 q1_1_dirac_modes_ds4.py            (real run; exit 0 iff every check passes)
         python3 q1_1_dirac_modes_ds4.py --mutate   (control: the Whittaker index loses the spin-1/2 shift, nu = -i s r0 instead of 1/2 - i s r0; M1 must FAIL;
                                                     exit 1 if the targeted check FAILS as required, exit 3 if it does NOT fail = the control has no power)
"""
import sys
sys.dont_write_bytecode = True
import math
import numpy as np
import mpmath as mp
import sympy as sp
from scipy.integrate import solve_ivp
from q1_lib import (PI, SX, SY, SZ, ID2, h_matrix, B_matrix, mode_spinor, sz_from_spinor, build_adiabatic, ad_pair, sz_pair)

MUTATE = "--mutate" in sys.argv
CHECKS = {}
mp.mp.dps = 25


def check(tag, ok, detail=""):
    CHECKS[tag.split()[0]] = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


rng = np.random.default_rng(20260928)

if __name__ == "__main__":
    print("=" * 110)
    print("Q1-1 Dirac fermion in dS_4: modes and structure -- mode: " + ("MUTATE CONTROL (spin-1/2 index shift removed)" if MUTATE else "REAL RUN"))
    print("=" * 110, flush=True)

    if not MUTATE:
        # ------------------------------------------------------------------ D1: curved-space Dirac eq -> flat system
        print("\nD1. Dirac equation in dS_4 (tetrad e^a_mu = a delta, spin connection from the tetrad) reduces to the flat system for Xi = a^{3/2} psi")
        tau, x, y, z = sp.symbols("tau x y z", real=True)
        Hs, q, m = sp.symbols("H q m", positive=True)
        X = [tau, x, y, z]
        a = -1 / (Hs * tau)
        # chiral (Weyl) matrices, signature (+,-,-,-)
        s0 = sp.eye(2)
        sx_, sy_, sz_ = sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.Matrix([[1, 0], [0, -1]])

        def blk(A, B_, C, D):
            return sp.Matrix(sp.BlockMatrix([[A, B_], [C, D]]))
        Z2 = sp.zeros(2)
        g0 = blk(Z2, s0, s0, Z2)
        gs = [blk(Z2, sig, -sig, Z2) for sig in (sx_, sy_, sz_)]
        gam = [g0] + gs                                    # flat gamma^a, {g^a, g^b} = 2 eta^{ab}, eta = diag(1,-1,-1,-1)
        eta = sp.diag(1, -1, -1, -1)
        for i in range(4):
            for j in range(4):
                assert sp.simplify(gam[i] * gam[j] + gam[j] * gam[i] - 2 * eta[i, j] * sp.eye(4)) == sp.zeros(4)
        gmet = a ** 2 * eta
        ginv = gmet.inv()
        Gam = [[[sum(ginv[i, l] * (sp.diff(gmet[l, j], X[k]) + sp.diff(gmet[l, k], X[j]) - sp.diff(gmet[j, k], X[l])) / 2 for l in range(4)) for k in range(4)] for j in range(4)] for i in range(4)]
        e_low = a * sp.eye(4)                                # e^a_mu
        e_up = sp.eye(4) / a                                 # e_a^mu  (row a, col mu)
        # omega_mu^a_b = e^a_nu (d_mu e_b^nu + Gamma^nu_{mu lam} e_b^lam)
        def omega(mu_, a_, b_):
            return sum(e_low[a_, n] * (sp.diff(e_up[b_, n], X[mu_]) + sum(Gam[n][mu_][l] * e_up[b_, l] for l in range(4))) for n in range(4))
        # Gamma_mu = c (1/8) omega_mu^{ab}[gam_a, gam_b]  with omega^{ab} = eta^{bc} omega^a_c ; sign c fixed by covariant constancy of gamma^nu(x)
        def spin_conn(c):
            out = []
            for mu_ in range(4):
                Sm = sp.zeros(4)
                for a_ in range(4):
                    for b_ in range(4):
                        oab = omega(mu_, a_, b_) * eta[b_, b_]          # omega_mu^{a b}
                        # gamma_a = eta_{aa} gamma^a
                        ga, gb = eta[a_, a_] * gam[a_], eta[b_, b_] * gam[b_]
                        Sm += oab * (ga * gb - gb * ga) / 8 * 1
                out.append(c * sp.simplify(Sm))
            return out
        chosen = None
        for c in (1, -1):
            Gm = spin_conn(c)
            ok = True
            for mu_ in range(4):
                for nu_ in range(4):
                    gnu = sum((e_up[aa, nu_] * gam[aa] for aa in range(4)), sp.zeros(4))
                    res = sp.diff(gnu, X[mu_]) + sum((Gam[nu_][mu_][l] * sum((e_up[aa, l] * gam[aa] for aa in range(4)), sp.zeros(4)) for l in range(4)), sp.zeros(4)) + Gm[mu_] * gnu - gnu * Gm[mu_]
                    if sp.simplify(res) != sp.zeros(4):
                        ok = False
            if ok:
                chosen = (c, Gm)
                break
        d1a = chosen is not None
        check("D1a spin connection from the tetrad makes gamma^mu(x) covariantly constant (the sign is FOUND by this test)", d1a, f"(sign c = {chosen[0] if chosen else None})")
        Gm = chosen[1]
        # curved Dirac operator on psi = a^{-3/2} Xi with A_z = L/(q tau) (q A_z = L/tau, H=1 units restored below)
        Xi = sp.Matrix([sp.Function(f"Xi{i}")(tau, x, y, z) for i in range(4)])
        psi = a ** sp.Rational(-3, 2) * Xi
        Az = sp.Symbol("Lq", real=True) / (q * tau) * 0 + sp.Function("Az")(tau)      # generic A_z(tau)
        Dpsi = sp.zeros(4, 1)
        for mu_ in range(4):
            Amu = Az if mu_ == 3 else 0
            gmu = sum((e_up[aa, mu_] * gam[aa] for aa in range(4)), sp.zeros(4))
            Dpsi += sp.I * gmu * (sp.diff(psi, X[mu_]) + Gm[mu_] * psi + sp.I * q * Amu * psi)
        curved = Dpsi - m * psi
        flatXi = sp.zeros(4, 1)
        for mu_ in range(4):
            Amu = Az if mu_ == 3 else 0
            flatXi += sp.I * gam[mu_] * (sp.diff(Xi, X[mu_]) + sp.I * q * Amu * Xi)
        flat = flatXi - m * a * Xi
        resid = sp.simplify(curved - a ** sp.Rational(-5, 2) * flat)
        check("D1b curved Dirac operator on a^{-3/2} Xi = a^{-5/2} x (flat operator with mass m a(tau) and potential A_z(tau))  [residual identically 0]", resid == sp.zeros(4, 1), "")
        # Hamiltonian form: i Xi_tau = [ alpha . (k + qA) + gamma0 m a ] Xi  (plane wave e^{i k x}, alpha_j = gamma0 gamma^j); verify by residual
        kx, ky, kz = sp.symbols("k_x k_y k_z", real=True)
        Hh = sp.zeros(4)
        for j, kj in enumerate((kx, ky, kz)):
            Hh += g0 * gs[j] * (kj + (q * Az if j == 2 else 0))
        Hh += g0 * m * a
        xi_t = sp.Matrix([sp.Function(f"X{i}")(tau) for i in range(4)])
        plane = sp.exp(sp.I * (kx * x + ky * y + kz * z))
        Xi_pw = xi_t * plane
        opflat = sp.zeros(4, 1)
        for mu_ in range(4):
            Amu = Az if mu_ == 3 else 0
            opflat += sp.I * gam[mu_] * (sp.diff(Xi_pw, X[mu_]) + sp.I * q * Amu * Xi_pw)
        opflat = (opflat - m * a * Xi_pw) / plane
        # gamma^0 x (flat operator on a plane wave) = i Xi' + gamma0 gamma^j (i k_j + i q A_j) Xi - gamma0 m a Xi = i Xi' - alpha.(k + qA) Xi - beta m a Xi
        target = sp.I * xi_t.diff(tau) - sum((g0 * gs[j] * (kj + (q * Az if j == 2 else 0)) for j, kj in enumerate((kx, ky, kz))), sp.zeros(4)) * xi_t - g0 * m * a * xi_t
        d1c = sp.simplify(g0 * opflat - target) == sp.zeros(4, 1)
        check("D1c plane waves: gamma^0 x (flat operator) = i Xi' - alpha.(k + qA) Xi - beta m a Xi, i.e. i Xi' = h Xi with h = alpha.p + beta m a, p = k + qA (q A_z = L/tau)", d1c, "")

        # 4x4 -> 2x2 blocks
        def rand_case():
            return rng.uniform(0.2, 3.0), rng.uniform(-0.95, 0.95), rng.uniform(0.1, 2.0), rng.uniform(0.2, 2.5), -rng.uniform(0.3, 2.0)
        a_z = np.array(sp.lambdify((), g0 * gs[2])(), dtype=complex)
        a_x = np.array(sp.lambdify((), g0 * gs[0])(), dtype=complex)
        b_ = np.array(sp.lambdify((), g0)(), dtype=complex)
        Q = a_z @ a_x @ b_
        evq, vq = np.linalg.eig(Q)
        # central element: Q commutes with all three; eigenvalues +-i
        comm = max(np.abs(Q @ g - g @ Q).max() for g in (a_z, a_x, b_))
        blocks = []
        Ucols = []
        for qv in (evq[0], [e for e in evq if abs(e - evq[0]) > 1e-9][0]):
            Pq = (Q - (-qv) * np.eye(4)) / (2 * qv)
            Pq = Pq @ Pq * 0 + (np.eye(4) + Q / qv) / 2
            # basis of the q-subspace: v1 = P_q (eigenvector of alpha_z with +1), v2 = alpha_x v1
            Pz = (np.eye(4) + a_z) / 2
            Msub = Pq @ Pz
            u_, s_, vh_ = np.linalg.svd(Msub)
            v1 = u_[:, 0]
            v2 = a_x @ v1
            Ucols += [v1, v2]
            Rb = np.array([v1, v2]).T
            beta_blk = Rb.conj().T @ b_ @ Rb
            blocks.append(beta_blk)
        U = np.array(Ucols).T
        unit = np.abs(U.conj().T @ U - np.eye(4)).max()
        # In the (v1, v2) basis alpha_z = sigma_z, alpha_x = sigma_x, beta = eps sigma_y
        eps = []
        ok_blk = True
        for bb in blocks:
            e1 = np.abs(bb - SY).max()
            e2 = np.abs(bb + SY).max()
            eps.append(+1 if e1 < e2 else -1)
            ok_blk = ok_blk and min(e1, e2) < 1e-12
        UazU = U.conj().T @ a_z @ U
        UaxU = U.conj().T @ a_x @ U
        Ubu = U.conj().T @ b_ @ U
        target_az = np.kron(np.eye(2), SZ) * 0
        # blocks ordering: block 0 = (v1,v2) of q0 (cols 0,1), block 1 = cols (2,3)
        def diag2(A, B2):
            M4 = np.zeros((4, 4), dtype=complex)
            M4[:2, :2] = A
            M4[2:, 2:] = B2
            return M4
        err = max(np.abs(UazU - diag2(SZ, SZ)).max(), np.abs(UaxU - diag2(SX, SX)).max(),
                  np.abs(Ubu - diag2(eps[0] * SY, eps[1] * SY)).max(), unit, comm)
        check("D1d explicit unitary maps (alpha_z, alpha_x, beta) to diag(sigma_z, sigma_z), diag(sigma_x, sigma_x), diag(+sigma_y, -sigma_y): the 4x4 problem = two 2x2 blocks h = sigma_z p + sigma_x kp +- sigma_y M a", err < 1e-12 and sorted(eps) == [-1, 1],
              f"(max error {err:.1e}; signs {eps})")

        # ------------------------------------------------------------------ D2: squared equation
        print("\nD2. squared equation, Whittaker index, dimensional bookkeeping")
        t_, k_, r_, L_, M_ = sp.symbols("t k r L M", real=True)
        kp_ = k_ * sp.sqrt(1 - r_ ** 2)
        hs = (k_ * r_ + L_ / t_) * sp.Matrix([[1, 0], [0, -1]]) + kp_ * sp.Matrix([[0, 1], [1, 0]]) + (-M_ / t_) * sp.Matrix([[0, -sp.I], [sp.I, 0]])
        hp = hs.diff(t_)
        lhs_ = sp.simplify(hs * hs - sp.I * hp)
        r0 = sp.sqrt(L_ ** 2 + M_ ** 2)
        Bs = (L_ * sp.Matrix([[1, 0], [0, -1]]) - M_ * sp.Matrix([[0, -sp.I], [sp.I, 0]])) / r0
        rhs_ = (k_ ** 2 + 2 * L_ * k_ * r_ / t_ + r0 ** 2 / t_ ** 2) * sp.eye(2) + sp.I * r0 * Bs / t_ ** 2
        d2a = sp.simplify(lhs_ - rhs_) == sp.zeros(2)
        check("D2a h^2 - i h' = [k^2 + 2 L k_z/tau + r0^2/tau^2] 1 + i r0 B/tau^2, B = (L sigma_z - M sigma_y)/r0, B^2 = 1 (identically)", d2a and sp.simplify(Bs * Bs - sp.eye(2)) == sp.zeros(2), "")
        # Whittaker: phi = W_{kappa,nu}(2 i k tau) solves phi'' + [k^2 + 2 i k kappa/tau + (1/4 - nu^2)/tau^2] phi = 0 ; match (1/4 - nu^2) = r0^2 + i s r0 with nu = 1/2 - i s r0 and 2 i k kappa = 2 L k r
        s_ = sp.Symbol("s", real=True)
        nu_ = sp.Rational(1, 2) - sp.I * s_ * r0
        kap = -sp.I * L_ * r_
        chk = sp.simplify(sp.expand(sp.Rational(1, 4) - nu_ ** 2 - (r0 ** 2 + sp.I * s_ * r0)).subs(s_ ** 2, 1)) == 0
        chk2 = sp.simplify(2 * sp.I * k_ * kap - 2 * L_ * k_ * r_) == 0
        d2b = chk and chk2
        # numerical confirmation of the ODE for phi with mpmath (mp.diff)
        okn = True
        for (kk, rr, LL, MM, ss) in [(1.3, 0.4, 0.5, 1.0, 1), (0.8, -0.7, 1.2, 0.6, -1), (2.5, 0.1, 0.3, 2.0, 1)]:
            rr0 = math.hypot(LL, MM)
            nu = mp.mpf(1) / 2 - 1j * ss * rr0
            kappa = -1j * mp.mpf(LL) * mp.mpf(rr)
            f = lambda t: mp.whitw(kappa, nu, 2j * kk * t)
            for tt in (-1.0, -2.3):
                lhsn = mp.diff(f, tt, 2) + (kk ** 2 + 2 * LL * kk * rr / tt + (rr0 ** 2 + 1j * ss * rr0) / tt ** 2) * f(tt)
                okn = okn and abs(lhsn) / (abs(mp.diff(f, tt, 2)) + 1e-30) < 1e-10
        check("D2b Whittaker index nu = 1/2 - i s r0, kappa = -i L r reproduces the scalar equation (algebraic identity) and solves it numerically (mp.diff, 6 points)", d2b and okn, "")
        # (e, E, m, H, k) only through (L, M, k/H)
        e_, E_, m_, H_, kd, tt2 = sp.symbols("e E m H k_d tau_d", positive=True)
        kzd = kd * sp.Symbol("rr", real=True)
        # dimensionful: tau = tau_d/H (conformal time), k = H kappa, q A_z = e E/(H^2 tau) ; h = alpha_z (k_z + eE/(H^2 tau)) + ... + beta m (-1/(H tau))
        tau_phys = tt2 / H_
        h_dimful = (H_ * kzd + e_ * E_ / (H_ ** 2 * tau_phys)) * sp.Symbol("az") - (m_ / (H_ * tau_phys)) * sp.Symbol("by")
        h_dimless = H_ * ((kzd + (e_ * E_ / H_ ** 2) / tt2) * sp.Symbol("az") - ((m_ / H_) / tt2) * sp.Symbol("by"))
        check("D2c (e, E, m, H, k) enter h only through L = eE/H^2, M = m/H and k/H: h_dimful = H x h(L, M; k/H)  (and i d/dtau = H i d/dtau_d)", sp.simplify(h_dimful - h_dimless) == 0, "")

    # ------------------------------------------------------------------ M1: Whittaker modes solve the first-order system
    print("\nM1. Whittaker modes Xi = (i d_tau + h)(W w_s): residual of i Xi' - h Xi, and Xi_{+} proportional to Xi_{-}")
    pts = [(1.3, 0.4, 0.5, 1.0, -1.0), (0.7, -0.6, 0.3, 1.5, -1.0), (2.2, 0.9, 1.1, 0.7, -0.8), (0.4, 0.1, 0.2, 0.4, -1.5),
           (3.1, -0.3, 0.8, 2.0, -1.2), (1.0, 0.0, 0.6, 1.0, -2.0), (0.6, 0.7, 0.9, 0.3, -0.6), (1.8, -0.9, 0.4, 1.2, -1.0)]
    worst_res, worst_prop = 0.0, 0.0
    for (kk, rr, LL, MM, tt) in pts:
        for s in (+1, -1):
            for sperp in (+1, -1):
                def xi_at(t, s=s, sperp=sperp):
                    return np.array(mode_spinor(kk, rr, LL, MM, t, s, sperp, index_shift=not MUTATE), dtype=complex)
                # derivative by mpmath-free central difference with tiny step (Richardson) on the complex spinor
                hstep = 1e-4
                d = (8 * (xi_at(tt + hstep) - xi_at(tt - hstep)) - (xi_at(tt + 2 * hstep) - xi_at(tt - 2 * hstep))) / (12 * hstep)
                lhs = 1j * d
                rhs = h_matrix(tt, kk, rr, LL, MM, sperp) @ xi_at(tt)
                res = np.linalg.norm(lhs - rhs) / (np.linalg.norm(rhs) + 1e-300)
                worst_res = max(worst_res, res)
        for sperp in (+1, -1):
            v_p = np.array(mode_spinor(kk, rr, LL, MM, tt, +1, sperp, index_shift=not MUTATE), dtype=complex)
            v_m = np.array(mode_spinor(kk, rr, LL, MM, tt, -1, sperp, index_shift=not MUTATE), dtype=complex)
            cross = abs(v_p[0] * v_m[1] - v_p[1] * v_m[0]) / (np.linalg.norm(v_p) * np.linalg.norm(v_m))
            worst_prop = max(worst_prop, cross)
    check("M1 residual of the first-order system <= 1e-8 (finite-difference derivative; 8 points x 2 s x 2 k_perp signs) and Xi_{s=+} parallel to Xi_{s=-} to <= 1e-8", worst_res <= 1e-8 and worst_prop <= 1e-8,
          f"(worst residual {worst_res:.1e}; worst |cross| {worst_prop:.1e})")

    if MUTATE:
        failed = not CHECKS["M1"]
        print("\nMUTATE CONTROL: the spin-1/2 shift of the Whittaker index was removed.")
        print(f"  M1 {'FAILED as required -- the control works' if failed else 'DID NOT FAIL -- the check has no power'}")
        sys.exit(1 if failed else 3)

    # ------------------------------------------------------------------ M2: ODE (Bunch-Davies)
    print("\nM2. Whittaker s_z = far-past ODE integration (first-order adiabatic eigenvector at tau_0 = -4000/k), both k_perp signs, negative r included")

    def ode_sz(k, r, L, M, sperp, T=4000.0):
        tau0 = -T / k

        def rhs(t, yv):
            return -1j * (h_matrix(t, k, r, L, M, sperp) @ yv)
        ev, evec = np.linalg.eigh(h_matrix(tau0, k, r, L, M, sperp))
        u = evec[:, 1].astype(complex)
        sol = solve_ivp(rhs, (tau0, -1.0), u, method="DOP853", rtol=1e-11, atol=1e-13)
        return sz_from_spinor(sol.y[:, -1])
    cases = [(1.3, 0.4, 0.5, 1.0), (0.7, -0.6, 0.3, 1.5), (2.2, 0.9, 1.1, 0.7), (0.4, 0.1, 0.2, 0.4), (3.1, -0.3, 0.8, 2.0), (1.0, -0.9, 0.6, 1.0), (0.5, 0.5, 1.5, 0.5), (2.0, -0.2, 0.3, 3.0)]
    worst = 0.0
    print("     k      r      L     M    sperp   Whittaker s_z    ODE s_z       |diff|")
    for (kk, rr, LL, MM) in cases:
        for sperp in (+1, -1):
            sw = sz_from_spinor(mode_spinor(kk, rr, LL, MM, -1.0, +1, sperp))
            so = ode_sz(kk, rr, LL, MM, sperp)
            worst = max(worst, abs(sw - so))
            print(f"     {kk:4.1f}  {rr:+.1f}  {LL:4.2f}  {MM:4.2f}   {sperp:+d}    {sw:+.8f}   {so:+.8f}   {abs(sw - so):.1e}")
    check("M2 Whittaker construction = far-past ODE integration to <= 1e-4 (absolute) at 8 points, both k_perp signs (validates Bunch-Davies and the negative-r / k_perp mapping)", worst <= 1e-4, f"(worst {worst:.1e})")

    # ------------------------------------------------------------------ M3: full 4x4 sea
    print("\nM3. full 4x4 Dirac sea (two negative-energy in-modes, explicit chiral gamma matrices) vs 2x2 block sum")
    g0n = np.block([[np.zeros((2, 2)), np.eye(2)], [np.eye(2), np.zeros((2, 2))]]).astype(complex)
    gsn = [np.block([[np.zeros((2, 2)), sg], [-sg, np.zeros((2, 2))]]) for sg in (SX, SY, SZ)]
    alx, aly, alz = [g0n @ g for g in gsn]

    def h4(t, k, r, L, M):
        p = k * r + L / t
        kp = k * math.sqrt(1 - r * r)
        return alz * p + alx * kp + g0n * (-M / t)

    def sea_trace(k, r, L, M, T=3000.0):
        tau0 = -T / k
        ev, evec = np.linalg.eigh(h4(tau0, k, r, L, M))
        neg = evec[:, :2]                                  # the two negative-energy eigenvectors = the Dirac sea in the far past

        def rhs(t, yv):
            Y = yv.reshape(4, 2)
            return (-1j * (h4(t, k, r, L, M) @ Y)).reshape(-1)
        sol = solve_ivp(rhs, (tau0, -1.0), neg.astype(complex).reshape(-1), method="DOP853", rtol=1e-11, atol=1e-13)
        Y = sol.y[:, -1].reshape(4, 2)
        return np.trace(alz @ (Y @ Y.conj().T)).real           # Tr[alpha_z P_sea]

    worst3 = 0.0
    for (kk, rr, LL, MM) in [(1.3, 0.4, 0.5, 1.0), (0.7, -0.6, 0.3, 1.5), (2.2, 0.9, 1.1, 0.7)]:
        tr = sea_trace(kk, rr, LL, MM)
        blk = -sum(sz_from_spinor(mode_spinor(kk, rr, LL, MM, -1.0, +1, sp_)) for sp_ in (+1, -1))
        worst3 = max(worst3, abs(tr - blk))
        print(f"     (k, r, L, M) = ({kk}, {rr}, {LL}, {MM}):  4x4  Tr[alpha_z P_sea] = {tr:+.8f}   blocks  -(s_z(+) + s_z(-)) = {blk:+.8f}")
    check("M3 4x4 sea trace = -(s_z(k_perp) + s_z(-k_perp)) from the 2x2 blocks to <= 1e-6 at 3 points", worst3 <= 1e-6, f"(worst {worst3:.1e})")

    # ------------------------------------------------------------------ A1: adiabatic series
    print("\nA1. Bloch-vector adiabatic series s_0 + s_1 + s_2 (derivative counting eps)")
    t_, k_, r_, L_, M_, eps_ = sp.symbols("t k r L M eps", real=True)
    kp = k_ * sp.sqrt(1 - r_ ** 2)
    n = sp.Matrix([kp, -M_ / t_, k_ * r_ + L_ / t_])
    om = sp.sqrt((n.T * n)[0])
    nh = n / om
    s0 = nh
    s1 = -nh.cross(nh.diff(t_)) / (2 * om)
    s2 = -((s1.T * s1)[0]) * nh / 2 - nh.cross(s1.diff(t_)) / (2 * om)
    res1 = s0.diff(t_) - 2 * n.cross(s1)
    res2 = s1.diff(t_) - 2 * n.cross(s2)
    res0 = n.cross(s0)
    norm_o1 = (s0.T * s1)[0]
    norm_o2 = ((s1.T * s1)[0] + 2 * (s0.T * s2)[0])
    fs = sp.lambdify((t_, k_, r_, L_, M_), [res0, res1, res2, norm_o1, norm_o2], modules="numpy")
    worstA = 0.0
    for _ in range(6):
        tt = -rng.uniform(0.5, 2.0); kk = rng.uniform(0.3, 3.0); rr = rng.uniform(-0.9, 0.9); LL = rng.uniform(0.1, 1.5); MM = rng.uniform(0.2, 2.0)
        out = fs(tt, kk, rr, LL, MM)
        worstA = max(worstA, max(float(np.max(np.abs(np.array(o, dtype=float)))) for o in out))
    check("A1a residuals of n x s_0 = 0, s_0' = 2 n x s_1, s_1' = 2 n x s_2 and of the unit-norm conditions at orders 1, 2 vanish (6 random points, <= 1e-10)", worstA <= 1e-10, f"(worst {worstA:.1e})")

    # error scaling against the exact (Whittaker) mode
    print("     error of s_z after order 0 / order 2 against the exact Whittaker mode, (r, L, M) = (0.3, 0.5, 1.0); single k_perp sign and pair sum")
    fz = {o: build_adiabatic(o) for o in (0, 2)}
    rows = []
    for kk in (40.0, 80.0, 160.0):
        ex = [sz_from_spinor(mode_spinor(kk, 0.3, 0.5, 1.0, -1.0, +1, sp_)) for sp_ in (+1, -1)]
        e0 = [abs(ex[i] - float(fz[0](-1.0, kk, 0.3, 0.5, 1.0, sg))) for i, sg in enumerate((+1, -1))]
        e2 = [abs(ex[i] - float(fz[2](-1.0, kk, 0.3, 0.5, 1.0, sg))) for i, sg in enumerate((+1, -1))]
        e0p = abs(sum(ex) - sum(float(fz[0](-1.0, kk, 0.3, 0.5, 1.0, sg)) for sg in (+1, -1)))
        e2p = abs(sum(ex) - sum(float(fz[2](-1.0, kk, 0.3, 0.5, 1.0, sg)) for sg in (+1, -1)))
        rows.append((kk, e0[0], e2[0], e0p, e2p))
        print(f"     k = {kk:6.1f}   single: order0 {e0[0]:.3e}  order2 {e2[0]:.3e}    pair: order0 {e0p:.3e}  order2 {e2p:.3e}")
    sl = lambda i: (math.log(rows[2][i]) - math.log(rows[0][i])) / (math.log(160.0) - math.log(40.0))
    s_single0, s_single2, s_pair0, s_pair2 = sl(1), sl(2), sl(3), sl(4)
    print(f"     slopes (log-log, k = 40 -> 160): single order0 {s_single0:.2f}, single order2 {s_single2:.2f}, pair order0 {s_pair0:.2f}, pair order2 {s_pair2:.2f}")
    okA = (-2.4 <= s_single0 <= -1.6) and (-4.4 <= s_single2 <= -3.6) and (-3.4 <= s_pair0 <= -2.6) and (-5.4 <= s_pair2 <= -4.6)
    check("A1b error scaling (Amendment 2 windows, set AFTER the first run -- post-hoc): single block order 0 ~ k^-2, order 2 ~ k^-4; pair sum order 0 ~ k^-3, order 2 ~ k^-5", okA, "")

    print("\n" + "=" * 110)
    passed = sum(CHECKS.values())
    print(f"CHECKS: {passed}/{len(CHECKS)} passed")
    print("Scope: one Dirac fermion, minimal coupling, dS_4 planar patch, in-vacuum, constant-energy-density electric field; tau = -1.")
    sys.exit(0 if passed == len(CHECKS) else 1)
