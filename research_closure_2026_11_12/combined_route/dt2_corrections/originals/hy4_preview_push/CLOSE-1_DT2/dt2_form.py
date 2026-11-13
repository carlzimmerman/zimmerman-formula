#!/usr/bin/env python3
"""CLOSE-1 / DT2 check 3: does a halo that starts from dust reach the static state, or fold?

Spherical Lagrangian staggered scheme on the reduced system of COL1 Part 1, generalised
from the quadratic to any kinetic function (FROZEN_CRITERIA S0):

    vdot_j = - G [ M_b(<r_j) + M_d(<r_j) + M_pol(<r_j) ] / r_j^2  +  s_j
    s_j    = -(dh/dr)_j                                 the specific pressure force
    h_j    = c^2 x(rho_d,j)                             the DT2 enthalpy
    M_pol(<r) = (a0 r^2 / G) u/(1+u),   u = s/a0        Gauss on P; exact

The faces F_j are the primary variables, so a uniform state and homologous motion are
exact.  Both limits are reproduced by construction:
  * s << a0 :  M_pol -> r^2 s / G, so g_pol = s and the polarization's gravity cancels the
    pressure force term by term  ->  pressureless infall (COL1's finding for the quadratic);
  * s >> a0 :  M_pol saturates at a0 r^2/G, the pressure force survives -> a normal fluid
    with sound speed c_ad = c sqrt(n/n').

Initial condition is COL1's: cold dust in Hubble flow at z_i at the background density,
a baryon point mass (Plummer-softened over 1 kpc) ramped on over 1 Gyr.

Stated bracket: the conserved charge is N = rho_d + div P; this code advects rho_d.  That
is exact in the strong-gradient limit and is the pressure-favouring side of the bracket, so
a fold found here is a fold.
"""
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import cumulative_trapezoid
import dt2_function as D

KPC_M = D.KPC
OM_M, H0_S = 0.31, 70.0e3 / D.MPC
YR = 3.1557e7


def build_eos():
    xg = np.unique(np.concatenate([np.geomspace(1.0e-13, 1.0e-7, 4000),
                                   np.linspace(1.0e-7, D.L_JUMP, 20000),
                                   np.geomspace(D.L_JUMP, 1.0e-2, 20000)]))
    QnV = (1.0 + xg) * D.n_of_x(xg) - D.V_of_x(xg)
    rho = np.maximum(QnV, 1e-300) / D.MPC ** 2 * D.C_SI ** 2 / D.K_SI
    lr = np.log(rho)
    keep = np.concatenate([[True], np.diff(lr) > 0])
    return lr[keep], xg[keep]


_LR, _XG = build_eos()
_LR0, _LR1 = _LR[0], _LR[-1]


def x_of_rho(rho):
    lr = np.clip(np.log(np.maximum(np.asarray(rho, dtype=float), 1e-300)), _LR0, _LR1)
    return np.interp(lr, _LR, _XG)


def H_of_a(a):
    return H0_S * np.sqrt(OM_M * a ** -3 + (1 - OM_M))


_AG = np.geomspace(1.0 / 21.0, 1.0, 6000)
_TG = cumulative_trapezoid(1.0 / (_AG * H_of_a(_AG)), np.log(_AG), initial=0.0)
_TG -= _TG[0]
A_OF_T = interp1d(_TG, _AG, kind='cubic', bounds_error=False, fill_value=(_AG[0], 1.0))
T_OF_A = interp1d(_AG, _TG, kind='cubic')


def run(lm, a0, z_i=10.0, N=260, r_in=1.0 * KPC_M, r_out=2.0 * D.MPC,
        ramp_Gyr=1.0, soften_kpc=1.0, max_steps=400000, cfl=0.15,
        r_floor=None, absorb=True, verbose=False):
    """Collapse run.  Shells that reach r_floor are absorbed into a central mass (the
    completion FLD1 used: 'each crossed shell's trajectory after its first crossing'),
    so the run continues past the first central fold and the settled reach can be measured."""
    M_b = 10.0 ** lm * D.MSUN
    a_i = 1.0 / (1.0 + z_i)
    rho_bg_i = D.RHO_C0 * a_i ** -3
    if r_floor is None:
        r_floor = 0.5 * r_in

    F = np.exp(np.linspace(np.log(r_in), np.log(r_out), N + 1))
    dm = rho_bg_i * (4.0 * np.pi / 3.0) * (F[1:] ** 3 - F[:-1] ** 3)
    rj = 0.75 * (F[1:] ** 4 - F[:-1] ** 4) / (F[1:] ** 3 - F[:-1] ** 3)
    v = H_of_a(a_i) * rj
    soft = soften_kpc * KPC_M
    F0 = F.copy()
    M_cen = 0.0
    turned = np.zeros(len(dm), dtype=bool)
    first_fold = None
    folded_mass = 0.0

    def state(F, dmv, Mbon, Mcen):
        V = (4.0 * np.pi / 3.0) * np.maximum(F[1:] ** 3 - F[:-1] ** 3, 1e-300)
        rho = dmv / V
        x = x_of_rho(rho)
        h = D.C_SI ** 2 * x
        rj = 0.75 * (F[1:] ** 4 - F[:-1] ** 4) / np.maximum(F[1:] ** 3 - F[:-1] ** 3, 1e-300)
        s = -np.gradient(h, rj)
        u = np.maximum(s, 0.0) / a0
        Mpol = (a0 * rj ** 2 / D.G_SI) * u / (1.0 + u) * np.where(s > 0, 1.0, -1.0)
        Mb_of_r = Mbon * rj ** 3 / (rj ** 2 + soft ** 2) ** 1.5
        Md_in = np.cumsum(dmv) - 0.5 * dmv + Mcen
        g = D.G_SI * (Mb_of_r + Md_in + Mpol) / rj ** 2
        cad = np.sqrt(np.maximum(D.C_SI ** 2 * D.n_of_x(x) / D.nprime_of_x(x), 1.0))
        return -g + s, rj, rho, h, s, Mpol, cad

    t = float(T_OF_A(a_i))
    t_ramp = ramp_Gyr * 1.0e9 * YR
    T0 = float(T_OF_A(1.0))
    snaps, it = [], 0
    next_out = t
    while t < T0 and it < max_steps and len(dm) > 12:
        a = float(A_OF_T(t))
        Mbon = M_b * min(1.0, max(0.0, (t - float(T_OF_A(a_i))) / t_ramp))
        acc, rj, rho, h, s, Mpol, cad = state(F, dm, Mbon, M_cen)
        dt_cfl = cfl * np.min(np.abs(np.diff(rj)) / np.maximum(cad[:-1], 1.0))
        dt_acc = 0.05 * np.sqrt(np.min(np.abs(rj)) / max(np.max(np.abs(acc)), 1e-30))
        dt = min(dt_cfl, dt_acc, (T0 - t) * 0.5, 2.0e15)
        dt = max(dt, 1.0e10)
        v_half = v + 0.5 * acc * dt
        n = len(v_half)
        Fv = np.empty(n + 1)
        Fv[1:-1] = v_half[:-1] + (F[1:-1] - rj[:-1]) / (rj[1:] - rj[:-1]) * (v_half[1:] - v_half[:-1])
        Fv[0] = v_half[0]
        Fv[-1] = v_half[-1] + (F[-1] - rj[-1]) / (rj[-1] - rj[-2]) * (v_half[-1] - v_half[-2])
        F_new = F + Fv * dt
        turned[:n] |= (v_half < 0.0)
        hit = F_new[0] <= r_floor
        if hit and first_fold is None:
            first_fold = t
        if hit or np.any(F_new[1:] <= F_new[:-1]):
            if not absorb:
                break
            # absorb the innermost shell(s) into the central mass
            nabs = 1
            while nabs < n - 12 and F_new[nabs] <= r_floor:
                nabs += 1
            M_cen += float(np.sum(dm[:nabs]))
            folded_mass += float(np.sum(dm[:nabs]))
            dm = dm[nabs:]
            F = F[nabs:]
            F[0] = r_floor
            v = v[nabs:]
            turned = turned[nabs:]
            continue
        acc2, rj2, rho2, h2, s2, Mpol2, cad2 = state(F_new, dm, Mbon, M_cen)
        v = v_half + 0.5 * acc2 * dt
        F = F_new
        t += dt
        it += 1
        if t >= next_out:
            snaps.append((t, a, F.copy(), v.copy(), s2.copy(), rj2.copy(), M_cen, dm.copy()))
            next_out = t + (T0 - float(T_OF_A(a_i))) / 60.0
    acc, rj, rho, h, s, Mpol, cad = state(F, dm, M_b, M_cen)
    snaps.append((t, float(A_OF_T(t)), F.copy(), v.copy(), s.copy(), rj.copy(), M_cen, dm.copy()))
    return dict(first_fold=first_fold, snaps=snaps, F=F, r=rj, v=v, dm=dm, M_b=M_b,
                F0=F0, turned=turned, t_end=t, iters=it, T0=T0, M_cen=M_cen,
                folded_mass=folded_mass, rho=rho, s=s, Mpol=Mpol, h=h,
                r_in=r_in, rho_bg_i=rho_bg_i, a_i=a_i, r_floor=r_floor)


# ----------------------------------------------------------------- diagnostics
def settled_radius(res, a0, frac=0.30):
    """Largest radius inside which every shell is slow compared with its circular speed."""
    t, a, F, v, s, rj, Mcen, dm = res['snaps'][-1]
    Md_in = np.cumsum(dm) - 0.5 * dm + Mcen
    Mpol = (a0 * rj ** 2 / D.G_SI) * (np.maximum(s, 0) / a0) / (1 + np.maximum(s, 0) / a0)
    g = D.G_SI * (res['M_b'] + Md_in + Mpol) / rj ** 2
    vcirc = np.sqrt(g * rj)
    slow = np.abs(v) < frac * vcirc
    R = 0.0
    for j in range(len(rj)):
        if slow[j]:
            R = rj[j]
        else:
            break
    return R, rj, v, vcirc, slow


if __name__ == "__main__":
    import sys, time
    lm = float(sys.argv[1]) if len(sys.argv) > 1 else 10.45
    for a0, lab in [(D.A0_CANON, 'canonical'), (D.A0_ALT, 'alt')]:
        t0 = time.time()
        res = run(lm, a0, verbose=True)
        R, rj, v, vcirc, slow = settled_radius(res, a0)
        t, a, F, v2, s, rj2, Mcen, dm = res['snaps'][-1]
        ff = res['first_fold']
        print(f"{lab}: iters={res['iters']} wall={time.time()-t0:.1f}s end z={1/a-1:.3f} "
              f"first fold={'%.4f Gyr' % ((ff-float(T_OF_A(1/11)))/1e9/YR) if ff else 'NONE'} "
              f"M_cen/M_b={res['M_cen']/res['M_b']:.4f}")
        print(f"   R_set(0) = {R/KPC_M:.1f} kpc ;  n shells left {len(rj)}")

