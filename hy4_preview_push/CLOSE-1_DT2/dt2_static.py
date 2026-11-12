#!/usr/bin/env python3
"""CLOSE-1 / DT2 check 2: the static clock state on three baryon profiles.

Spherical, static, today's background (q = 1, so x_bar_inf = x(1) = 0 and h = Phi_d = |Phi|).

    h(r)  = Phi_d(r)                                   specific enthalpy, m^2/s^2
    x(r)  = h/c^2
    rho_d = (Q n - V) c^2 / K                           exact clock stress-energy
    g_N'(r) = G [ M_b(<r) + M_d(<r) ] / r^2             baryons + the clock's dust
    g(r)  = [ g_N' + sqrt(g_N'^2 + 4 a0 g_N') ] / 2     the law, solved exactly at each r
    M_pol(<r) = (a0 r^2/G) u/(1+u),  u = g/a0           (Gauss on P; exact)
    Phi_d(r)  = int_r^{R_ref} g dr'

The inner solve for g is the exact algebraic form-B root, so the only iteration is on the
dust density (which enters through Phi_d).  Damped Picard on rho_d; divergence
(COL1 Part 0's "n = 1 Jeans core") is detected as a non-contracting / runaway iteration.

Known answer KA1: with the dust switched off and a point mass, M_pol(<r) must equal
form B's M_b X(r/r_M) exactly.
"""
import numpy as np
import dt2_function as D

R_REF_DEFAULT = 3.0 * D.MPC
KPC_M = D.KPC


def R_d_Shen(M_b_Msun):
    """Shen et al. 2003 late types, as used by SCS2 / DCN1 / SCS3 / EFN1 in this repo."""
    R50 = 0.10 * KPC_M * M_b_Msun ** 0.14 * (1.0 + M_b_Msun / 3.98e10) ** 0.25
    return R50 / 1.678


class Baryons:
    def __init__(self, kind, M_b, a):
        self.kind, self.M_b, self.a = kind, M_b, a

    def Menc(self, r):
        M, a = self.M_b, self.a
        if self.kind in ("point", "plummer"):
            return M * r ** 3 / (r ** 2 + a ** 2) ** 1.5
        if self.kind == "hernquist":
            return M * r ** 2 / (r + a) ** 2
        raise ValueError(self.kind)


def rho_dust_of_x(x):
    """(Q n - V) c^2 / K  in kg/m^3, from the tabulated kinetic function."""
    x = np.asarray(x, dtype=float)
    Qn_V = (1.0 + x) * D.n_of_x(x) - D.V_of_x(x)          # Mpc^-2
    return np.maximum(Qn_V, 0.0) / D.MPC ** 2 * D.C_SI ** 2 / D.K_SI


def solve_static(bary, a0, R_ref=R_REF_DEFAULT, N=1200, r_min=0.02 * KPC_M,
                 iters=250, damp=0.4, tol=1e-9, with_dust=True):
    r = np.exp(np.linspace(np.log(r_min), np.log(R_ref), N))
    Mb = bary.Menc(r)

    def g_of(gNp):
        return 0.5 * (gNp + np.sqrt(gNp ** 2 + 4.0 * a0 * gNp))

    def Phi_d_of(g):
        out = np.zeros(N)
        for i in range(N - 2, -1, -1):
            out[i] = out[i + 1] + 0.5 * (g[i] + g[i + 1]) * (r[i + 1] - r[i])
        return out

    Md = np.zeros(N)
    rho_d = np.zeros(N)
    hist = []
    converged = False
    it = 0
    for it in range(iters):
        gNp = D.G_SI * (Mb + Md) / r ** 2
        g = g_of(gNp)
        Phid = Phi_d_of(g)
        x = Phid / D.C_SI ** 2
        if with_dust:
            rho_new = rho_dust_of_x(x)
        else:
            rho_new = np.zeros(N)
        integ = 4.0 * np.pi * r ** 2 * rho_new
        Md_new = np.zeros(N)
        for i in range(1, N):
            Md_new[i] = Md_new[i - 1] + 0.5 * (integ[i] + integ[i - 1]) * (r[i] - r[i - 1])

        denom = np.maximum(Md_new[-1], 1e-30)
        step = np.max(np.abs(Md_new - Md)) / denom
        hist.append(step)
        rho_d = rho_d + damp * (rho_new - rho_d)
        Md = Md + damp * (Md_new - Md)
        if step < tol:
            converged = True
            break
        if len(hist) > 30 and np.median(hist[-10:]) >= 0.95 * np.median(hist[-30:-10]):
            converged = False
            break
    gNp = D.G_SI * (Mb + Md) / r ** 2
    g = g_of(gNp)
    Phid = Phi_d_of(g)
    u = g / a0
    Mpol = (a0 * r ** 2 / D.G_SI) * u / (1.0 + u)
    return dict(converged=converged, r=r, g=g, Md=Md, Mpol=Mpol, Phid=Phid,
                rho_d=rho_dust_of_x(Phid / D.C_SI ** 2) if with_dust else np.zeros(N),
                iters=it, step=hist[-1], hist=hist, Mb=Mb)


def _at(sol, arr, rq):
    return np.interp(rq, sol['r'], arr)


def main():
    print("=" * 118)
    print("DT2 STATIC CHECK: point mass / Plummer / Hernquist, 4 masses, both footings   (K2)")
    print("=" * 118)
    masses = [9.4, 10.45, 10.7, 10.9]
    rows = []
    for a0, lab in [(D.A0_CANON, "canonical"), (D.A0_ALT, "alt")]:
        line = 0.33 if lab == "canonical" else 0.19
        print(f"\n--- footing {lab}: a0 = {a0:.4e} m/s^2 ; KD1 line M_d(<4R_d)/M_b <= {line} ---")
        print(f"{'log M_b':>7} {'profile':>10} {'conv':>6} {'it':>4} "
              f"{'M_d/M_b@10':>11} {'@30':>10} {'@100':>10} {'@300':>10} "
              f"{'M_d(<4Rd)/M_b':>14} {'verdict':>9}")
        print("-" * 118)
        for lm in masses:
            M_b = 10.0 ** lm * D.MSUN
            Rd = R_d_Shen(10.0 ** lm)
            for kind in ("point", "plummer", "hernquist"):
                if kind == "point":
                    a = 1.0 * KPC_M
                elif kind == "plummer":
                    a = Rd
                else:
                    a = Rd / 1.815
                sol = solve_static(Baryons(kind, M_b, a), a0)
                Md = sol['Md']
                vals = [_at(sol, Md, q * KPC_M) / M_b for q in (10, 30, 100, 300)]
                M4 = _at(sol, Md, 4.0 * Rd) / M_b
                ok = "PASS" if (sol['converged'] and M4 <= line) else "FAIL"
                print(f"{lm:7.2f} {kind:>10} {str(sol['converged']):>6} {sol['iters']:4d} "
                      f"{vals[0]:11.3e} {vals[1]:10.3e} {vals[2]:10.3e} {vals[3]:10.3e} "
                      f"{M4:14.3e} {ok:>9}")
                rows.append((lab, lm, kind, sol['converged'], M4, vals))
    return rows


if __name__ == "__main__":
    main()
