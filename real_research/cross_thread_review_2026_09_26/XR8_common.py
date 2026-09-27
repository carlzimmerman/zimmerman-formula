#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR8_common -- shared, side-effect-free solvers for the XR8 lane ("what is the fluid?").

Everything here is a pure function.  The test problem, units, checkpoints, coarse-graining, misplaced-mass measure and
pass rule are L374's (real_research/condensate_dust_2026/L374_condensate_dust_shell_crossing.py, commit 4366a5625),
imported from that file where it has a pure function (Grid, v_init, S_init, condensate, schrodinger) and re-implemented
here only where XR8 needs something L374 does not provide (node detection, other completions, warm targets, Vlasov,
sticky particles).  L374's main is never run.  Code units: L = v0 = rho_bar = 1; t_sc = L / (2 pi v0).

L374's pre-declared pass rule, reused verbatim (L374 lines 41-44): a cell TRACKS the collisionless answer if it keeps
  M <= max(0.05, 2 x Schroedinger-Poisson's M at the same lambda and time) at every post-crossing checkpoint in BOTH
  tests, stays positive (min rho >= -0.01 rho_bar), conserves energy to 1% and does not break down.
"""
import os, sys, math, hashlib
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
L374_DIR = os.path.join(REPO, "real_research", "condensate_dust_2026")
L374_PATH = os.path.join(L374_DIR, "L374_condensate_dust_shell_crossing.py")
sys.path.insert(0, L374_DIR)
sys.dont_write_bytecode = True                              # write no bytecode cache into another lane's folder
import L374_condensate_dust_shell_crossing as L374          # noqa: E402  (module import only; its main is guarded)

L, V0, RHOB = L374.L, L374.V0, L374.RHOB
TSC = L374.TSC
GRAV = dict(L374.GRAV)
TCHK = {k: list(v) for k, v in L374.TCHK.items()}
M_TOL, POS_TOL, E_TOL = L374.M_TOL, L374.POS_TOL, L374.E_TOL
Grid, v_init, S_init = L374.Grid, L374.v_init, L374.S_init
TSC_GRAV_L374 = 0.1405                                        # L374's first stream crossing in the self-gravitating N-body


def l374_sha256():
    return hashlib.sha256(open(L374_PATH, "rb").read()).hexdigest()


def D_of(lam):
    """L374: de Broglie length lambda = 4 pi D / v0."""
    return lam * V0 / (4 * np.pi)


# ==================================================================================================== collisionless targets
def nbody_cold(test, nx, NP, nx_extra=None):
    """L374's collisionless answer (free: exact; gravity: exact-force sheets, Jeans swindle, periodic wrap as L374 l.160)."""
    return nbody_sheets(test, nx, q=(np.arange(NP) + 0.5) * L / NP, u=np.zeros(NP), nx_extra=nx_extra)


def nbody_warm(test, nx, NQ, NU, dv):
    """A warm WATER-BAG target: at each Lagrangian point q, velocities v_init(q) + u with u uniform on [-dv/2, dv/2]
    (a 1-D collisionless gas whose adiabatic index is 3; its sound speed at rho_bar is dv / 2)."""
    q = (np.arange(NQ) + 0.5) * L / NQ
    u = (np.arange(NU) + 0.5) * dv / NU - dv / 2
    Q, U = np.meshgrid(q, u, indexing="ij")
    return nbody_sheets(test, nx, q=Q.ravel(), u=U.ravel())


def nbody_sheets(test, nx, q, u, dt=2.5e-4, tchk=None, nx_extra=None):
    """Sheets with exact 1-D gravity (L374's algorithm).  nx_extra: also deposit on a second grid (key 'rs_extra')."""
    g = Grid(nx); NP = q.size; m = RHOB * L / NP
    g2 = Grid(nx_extra) if nx_extra else None
    tchk = TCHK[test] if tchk is None else tchk
    xp = q.copy(); vp = v_init(q) + u
    out, out2 = {}, {}
    if test == "free":
        for t in tchk:
            out[t] = g.smooth(g.cic(xp + vp * t, m))
            if g2 is not None:
                out2[t] = g2.smooth(g2.cic(xp + vp * t, m))
        return dict(rs=out, rs_extra=out2, tsc=TSC, vmax=float(np.abs(vp).max()))
    grav = GRAV[test]

    def acc(xp):
        order = np.argsort(xp, kind="stable")
        rank = np.empty(NP); rank[order] = np.arange(NP)
        a = -grav * (m * (rank + 0.5) - RHOB * xp)
        return a - a.mean()
    t, tsc, vmax = 0.0, None, 0.0
    a = acc(xp)
    for tc in tchk:
        n = int(round((tc - t) / dt))
        for _ in range(n):
            vp += 0.5 * dt * a; xp += dt * vp
            if tsc is None and np.all(u == 0) and np.any(np.diff(xp) < 0):
                tsc = t + dt
            xp %= L
            a = acc(xp); vp += 0.5 * dt * a
            t += dt
        vmax = max(vmax, float(np.abs(vp).max()))
        out[tc] = g.smooth(g.cic(xp, m))
        if g2 is not None:
            out2[tc] = g2.smooth(g2.cic(xp, m))
    return dict(rs=out, rs_extra=out2, tsc=tsc, vmax=vmax)


# ==================================================================================================== the wave field
def wave(test, lam, W, nx, gamma=2, dtm=None, node_every=1, tchk=None, psi0=None, record_min=True):
    """Schroedinger-Poisson (W = 0) or Gross-Pitaevskii-Poisson with a gamma = 2 (|psi|^4) or gamma = 3 (|psi|^6)
    self-interaction, the same Strang splitting and time step as L374's schrodinger(), plus a SPACE-TIME NODE DETECTOR:
    the phase winding of psi around every (dx, node_every * dt) plaquette.  A nonzero winding is a node event
    (psi = 0 at an isolated point of the x-t plane), where the phase is undefined and jumps.
    W = c_s^2(rho_bar) / v0^2 as in L374 (gamma = 2: h = eps rho; gamma = 3: h = (3/2) K rho^2 with 3 K rho_bar^2 = eps rho_bar)."""
    g = Grid(nx); D = D_of(lam); grav = GRAV[test]
    eps = W * V0 ** 2 / RHOB
    psi = np.sqrt(RHOB) * np.exp(1j * S_init(g.x) / (2 * D)) if psi0 is None else psi0.copy()
    dtm = 1e-5 * (8192 / nx) if dtm is None else dtm
    tchk = TCHK[test] if tchk is None else tchk

    def V(psi):
        rho = np.abs(psi) ** 2
        if eps > 0:                                              # enthalpy h(rho): gamma 2 -> eps rho; gamma 3 -> eps rho^2 / 2 rho_bar
            out = eps * rho if gamma == 2 else 0.5 * eps * rho ** 2 / RHOB
        else:
            out = np.zeros(nx)
        if grav > 0:
            out = out + np.fft.irfft(g.phi_k(np.fft.rfft(rho), grav), nx)
        return out / (2 * D)
    t, out, nodes_t, nodes_x, nodes_d, nodes_w, prev, nstep, rmin = 0.0, {}, [], [], [], [], psi.copy(), 0, []
    rho_max = float(np.max(np.abs(psi) ** 2))
    for tc in tchk:
        n = max(1, int(math.ceil((tc - t) / dtm))); dt = (tc - t) / n
        kin = np.exp(-1j * D * g.kf ** 2 * dt)
        for i_ in range(n):
            psi *= np.exp(-0.5j * dt * V(psi))
            psi = np.fft.ifft(kin * np.fft.fft(psi))
            psi *= np.exp(-0.5j * dt * V(psi))
            nstep += 1
            if nstep % 10 == 0:
                rho_max = max(rho_max, float(np.max(psi.real ** 2 + psi.imag ** 2)))
            if node_every and nstep % node_every == 0:
                nxt = np.roll(psi, -1); pnx = np.roll(prev, -1)
                wnd = (np.angle(pnx / prev) + np.angle(nxt / pnx) + np.angle(psi / nxt) + np.angle(prev / psi)) / (2 * np.pi)
                idx = np.nonzero(np.abs(wnd) > 0.5)[0]
                if idx.size:
                    tt = t + (i_ + 1) * dt
                    nodes_t.extend([tt] * idx.size); nodes_x.extend(g.x[idx].tolist())
                    corners = np.minimum(np.minimum(np.abs(prev[idx]) ** 2, np.abs(pnx[idx]) ** 2),
                                         np.minimum(np.abs(psi[idx]) ** 2, np.abs(nxt[idx]) ** 2))
                    nodes_d.extend((corners / RHOB).tolist()); nodes_w.extend(np.rint(wnd[idx]).astype(int).tolist())
                prev = psi.copy()
                if record_min:
                    rmin.append((t + (i_ + 1) * dt, float(np.min(np.abs(psi) ** 2))))
        t = tc
        out[tc] = g.smooth(np.abs(psi) ** 2)
    return dict(rs=out, nodes_t=np.array(nodes_t), nodes_x=np.array(nodes_x), nodes_depth=np.array(nodes_d),
                nodes_wind=np.array(nodes_w), psi=psi, rmin=rmin, rho_max=rho_max)


def wave_mixed(test, lam, us, nx, dtm=None, tchk=None):
    """A MIXED-STATE wave field: N incoherent wavefunctions psi_j = sqrt(rho_bar / N) exp(i (S_init + u_j x) / 2D),
    each with a velocity offset u_j (u_j x / 2D periodic: u_j a multiple of 4 pi D / L), evolved in their common
    Schroedinger-Poisson potential rho = sum_j |psi_j|^2 (Widrow & Kaiser 1993; Mocz et al. 2018).  Its Wigner function
    obeys the Vlasov equation up to O(hbar^2) (the Moyal correction)."""
    g = Grid(nx); D = D_of(lam); grav = GRAV[test]
    us = np.asarray(us, float); N = us.size
    quantum = 4 * np.pi * D / L
    assert np.allclose(us / quantum, np.rint(us / quantum)), "velocity offsets must keep psi_j periodic"
    psi = np.sqrt(RHOB / N) * np.exp(1j * (S_init(g.x)[None, :] + us[:, None] * g.x[None, :]) / (2 * D))
    dtm = 1e-5 * (8192 / nx) if dtm is None else dtm
    tchk = TCHK[test] if tchk is None else tchk

    def V(psi):
        rho = np.sum(np.abs(psi) ** 2, axis=0)
        if grav > 0:
            return (np.fft.irfft(g.phi_k(np.fft.rfft(rho), grav), nx) / (2 * D))[None, :]
        return np.zeros((1, nx))
    t, out = 0.0, {}
    for tc in tchk:
        n = max(1, int(math.ceil((tc - t) / dtm))); dt = (tc - t) / n
        kin = np.exp(-1j * D * g.kf ** 2 * dt)[None, :]
        for _ in range(n):
            if grav > 0:
                psi *= np.exp(-0.5j * dt * V(psi))
            psi = np.fft.ifft(kin * np.fft.fft(psi, axis=1), axis=1)
            if grav > 0:
                psi *= np.exp(-0.5j * dt * V(psi))
        t = tc
        out[tc] = g.smooth(np.sum(np.abs(psi) ** 2, axis=0))
    return dict(rs=out)


# ==================================================================================================== single-velocity fluids
def fluid(test, lam, W, nx, eos="g2", disp="k4", b_alpha=0.0, dtfac=1.0, tchk=None, pressureless=False):
    """L374's condensate generalised.  Variables rho and the velocity potential S (v = d_x S), Hamiltonian
        E = int [ rho v^2 / 2 + U(rho) + (beta/2)(1 + b (rho - rho_bar)/rho_bar)(d_x v)^2 + (gamma6/2)(d_x^2 v)^2
                  + (rho - rho_bar) Phi / 2 ],
    so d_t rho = -d_x(rho v) + d_x^2[beta (1 + b delta) d_x v] - gamma6 d_x^5 v and d_t S = -v^2/2 - Phi - U'(rho)
    - (beta b / 2 rho_bar)(d_x v)^2.  eos 'g2': U = eps rho^2 / 2 (L374); 'g3': U = K rho^3 / 2 with 3 K rho_bar^2 =
    eps rho_bar (the same c_s at rho_bar; a P ~ X^{3/2}-type index).  disp 'k4' (L374: beta = D^2 / eps), 'k4k6' (adds
    gamma6 = beta (lambda/2pi)^2), 'k6' (replaces: beta = 0, gamma6 = (D^2 / eps)(lambda/2pi)^2).  D and eps as in L374.
    Integrating-factor RK4 (Lawson) exactly as L374's condensate(), 2/3 dealiasing, the same time-step rules."""
    g = Grid(nx); grav = GRAV[test]
    tchk = TCHK[test] if tchk is None else tchk
    if pressureless:
        eps = beta = gam6 = 0.0; K = 0.0
    else:
        D = D_of(lam); eps = W * V0 ** 2 / RHOB
        beta0 = D ** 2 / eps; ell = lam / (2 * np.pi)
        beta = beta0 if disp in ("k4", "k4k6") else 0.0
        gam6 = beta0 * ell ** 2 if disp in ("k4k6", "k6") else 0.0
        K = eps / (3 * RHOB) if eos == "g3" else 0.0
    Lam = beta * g.k ** 4 + gam6 * g.k ** 6                      # linear exchange: rho_t = Lam S, S_t = -eps rho
    om = np.sqrt(eps * Lam)
    rk = np.fft.rfft(np.full(nx, RHOB)); sk = np.fft.rfft(S_init(g.x))
    dtm = 2e-5 * (8192 / nx) * dtfac
    kd = (2.0 / 3.0) * g.k[-1]

    def Eop(tau):
        c = np.cos(om * tau); s = np.sin(om * tau); safe = om > 1e-300
        B = np.where(safe, Lam * s / np.where(safe, om, 1.0), Lam * tau)
        C = np.where(safe, -eps * s / np.where(safe, om, 1.0), -eps * tau)
        return c, B, C

    def apply(E, r, s_):
        c, B, C = E
        return c * r + B * s_, C * r + c * s_

    def Nl(r, s_):
        r_d, s_d = r * g.deal, s_ * g.deal
        rho = np.fft.irfft(r_d, nx); v = np.fft.irfft(1j * g.k * s_d, nx)
        nr = -1j * g.k * np.fft.rfft(rho * v)
        ns = -0.5 * np.fft.rfft(v * v) - g.phi_k(r_d, grav)
        if K > 0:                                                # gamma = 3: U'(rho) - eps rho = (3/2) K (rho - rho_bar)^2 + const
            ns = ns - 1.5 * K * np.fft.rfft((rho - RHOB) ** 2)
        if b_alpha != 0.0:                                       # X-dependent k^4 coefficient (the delta (lap pi)^2 cubic)
            dv = np.fft.irfft(-(g.k ** 2) * s_d, nx)
            nr = nr - (g.k ** 2) * np.fft.rfft(beta * b_alpha * (rho - RHOB) / RHOB * dv)
            ns = ns - np.fft.rfft(0.5 * beta * b_alpha / RHOB * dv * dv)
        return nr * g.deal, ns * g.deal

    def energy(r, s_):
        rho = np.fft.irfft(r, nx); v = np.fft.irfft(1j * g.k * s_, nx)
        dv = np.fft.irfft(-(g.k ** 2) * s_, nx); d2v = np.fft.irfft(-1j * g.k ** 3 * s_, nx)
        ph = np.fft.irfft(g.phi_k(r, grav), nx)
        U = 0.5 * eps * rho ** 2 if K == 0 else 0.5 * K * rho ** 3
        return float(np.sum(0.5 * rho * v ** 2 + U + 0.5 * beta * (1 + b_alpha * (rho - RHOB) / RHOB) * dv ** 2
                            + 0.5 * gam6 * d2v ** 2 + 0.5 * (rho - RHOB) * ph) * g.dx)
    E0 = energy(rk, sk); EK0 = 0.25 * RHOB * V0 ** 2 * L
    t, out, min_rho, e_drift, t_break = 0.0, {}, RHOB, 0.0, None
    t_neg, e_pre, nstep = None, 0.0, 0
    for tc in tchk:
        while t < tc - 1e-14 and t_break is None:
            rho = np.fft.irfft(rk, nx); v = np.fft.irfft(1j * g.k * sk, nx)
            vmax = float(np.max(np.abs(v))) + 1e-12
            dt = min(dtm, 0.25 * dtfac * g.dx / vmax, tc - t)
            if eps > 0:
                cmax = math.sqrt(eps * max(float(np.max(np.abs(rho))), RHOB)) if K == 0 else \
                    math.sqrt(3 * K) * max(float(np.max(np.abs(rho))), RHOB)
                dt = min(dt, 0.5 * dtfac / (kd * cmax))
            if b_alpha != 0.0:
                stiff = math.sqrt(eps * beta * abs(b_alpha) * max(float(np.max(np.abs(rho - RHOB))), RHOB) / RHOB) * kd ** 2
                dt = min(dt, 0.5 * dtfac / max(stiff, 1e-30))
            if K > 0:                                            # the EOS remainder couples to the dispersion explicitly:
                lam_kd = beta * kd ** 4 + gam6 * kd ** 6         # omega ~ sqrt(eps |rho/rho_bar - 1| Lam(kd))
                stiff = math.sqrt(eps * max(float(np.max(np.abs(rho / RHOB - 1))), 1e-3) * lam_kd)
                dt = min(dt, 0.5 * dtfac / max(stiff, 1e-30))
            if grav > 0:
                dt = min(dt, 0.05 * dtfac / math.sqrt(grav * max(float(np.max(rho)), RHOB)))
            Eh, Eh2 = Eop(dt), Eop(0.5 * dt)
            k1 = Nl(rk, sk)
            a_ = apply(Eh2, rk + 0.5 * dt * k1[0], sk + 0.5 * dt * k1[1]); k2 = Nl(*a_)
            u2 = apply(Eh2, rk, sk); b_ = (u2[0] + 0.5 * dt * k2[0], u2[1] + 0.5 * dt * k2[1]); k3 = Nl(*b_)
            uh = apply(Eh, rk, sk); e3 = apply(Eh2, *k3)
            c_ = (uh[0] + dt * e3[0], uh[1] + dt * e3[1]); k4_ = Nl(*c_)
            e1 = apply(Eh, *k1); e23 = apply(Eh2, k2[0] + k3[0], k2[1] + k3[1])
            rk = uh[0] + dt / 6 * (e1[0] + 2 * e23[0] + k4_[0])
            sk = uh[1] + dt / 6 * (e1[1] + 2 * e23[1] + k4_[1])
            t += dt
            rho = np.fft.irfft(rk, nx)
            if not np.all(np.isfinite(rho)) or np.max(np.abs(rho)) > 1e4 * RHOB:
                t_break = t
                break
            min_rho = min(min_rho, float(rho.min())); nstep += 1
            if not pressureless and (nstep % 50 == 0 or (t_neg is None and rho.min() < POS_TOL)) and rho.min() >= -1.0:
                e_pre = max(e_pre, abs(energy(rk, sk) - E0) / EK0)
            if t_neg is None and rho.min() < POS_TOL:
                t_neg = t
        if t_break is not None:
            break
        out[tc] = g.smooth(np.fft.irfft(rk, nx))
        if not pressureless:
            e_drift = max(e_drift, abs(energy(rk, sk) - E0) / EK0)
    return dict(rs=out, min_rho=min_rho, e_drift=max(e_drift, e_pre), t_break=t_break, t_neg=t_neg)


def madelung(test, lam, W, nx, tchk=None, t_end=None, amin_frac=1e-5):
    """The Madelung FORM of the same wave field, solved as a fluid: a = sqrt(rho) and the phase S (v = d_x S),
        a_t = -S_x a_x - a S_xx / 2,     S_t = -S_x^2 / 2 - Phi - eps a^2 + 2 D^2 a_xx / a,
    explicit pseudo-spectral RK4 with 2/3 dealiasing.  Identical to the wave form while rho > 0 everywhere; singular at a
    node (a -> 0, where S jumps).  It stops ('breaks down') when min rho < amin_frac^2 rho_bar... i.e. min a < amin_frac,
    or on overflow, or when the adaptive step collapses."""
    g = Grid(nx); D = D_of(lam); grav = GRAV[test]; eps = W * V0 ** 2 / RHOB
    tchk = TCHK[test] if tchk is None else tchk
    kd = (2.0 / 3.0) * g.k[-1]
    a = np.full(nx, math.sqrt(RHOB)); S = S_init(g.x).copy()

    def d(f, n_):
        return np.fft.irfft(((1j * g.k) ** n_) * np.fft.rfft(f) * g.deal, nx)

    def rhs(a, S):
        ax, axx, Sx, Sxx = d(a, 1), d(a, 2), d(S, 1), d(S, 2)
        at = -Sx * ax - 0.5 * a * Sxx
        St = -0.5 * Sx ** 2 - eps * a ** 2 + 2 * D ** 2 * axx / a
        if grav > 0:
            St = St - np.fft.irfft(g.phi_k(np.fft.rfft(a * a), grav), nx)
        fa = np.fft.irfft(np.fft.rfft(at) * g.deal, nx); fS = np.fft.irfft(np.fft.rfft(St) * g.deal, nx)
        return fa, fS

    def energy(a, S):
        ph = np.fft.irfft(g.phi_k(np.fft.rfft(a * a), grav), nx)
        return float(np.sum(0.5 * a * a * d(S, 1) ** 2 + 2 * D ** 2 * d(a, 1) ** 2 + 0.5 * eps * a ** 4
                            + 0.5 * (a * a - RHOB) * ph) * g.dx)
    E0 = energy(a, S); EK0 = 0.25 * RHOB * V0 ** 2 * L
    t, out, t_break, why, e_drift, amin_hist = 0.0, {}, None, None, 0.0, []
    for tc in tchk:
        while t < tc - 1e-14 and t_break is None:
            vmax = float(np.max(np.abs(d(S, 1)))) + 1e-12
            dt = min(0.2 * g.dx / vmax, 1.6 / (D * kd ** 2), tc - t)
            if eps > 0:
                dt = min(dt, 0.5 / (kd * math.sqrt(eps * max(float(np.max(a * a)), RHOB))))
            if grav > 0:
                dt = min(dt, 0.05 / math.sqrt(grav * max(float(np.max(a * a)), RHOB)))
            if dt < 1e-9:
                t_break, why = t, "time step collapsed"; break
            k1 = rhs(a, S); k2 = rhs(a + 0.5 * dt * k1[0], S + 0.5 * dt * k1[1])
            k3 = rhs(a + 0.5 * dt * k2[0], S + 0.5 * dt * k2[1]); k4 = rhs(a + dt * k3[0], S + dt * k3[1])
            a = a + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); S = S + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            t += dt
            if not (np.all(np.isfinite(a)) and np.all(np.isfinite(S))):
                t_break, why = t, "overflow"; break
            am = float(np.min(a))
            amin_hist.append((t, am))
            if am < amin_frac * math.sqrt(RHOB):
                t_break, why = t, "a node reached (rho -> 0): the fluid form is singular there"; break
            if t_end is not None and t >= t_end:
                break
        if t_break is not None:
            break
        out[tc] = g.smooth(a * a)
        e_drift = max(e_drift, abs(energy(a, S) - E0) / EK0)
    return dict(rs=out, t_break=t_break, why=why, e_drift=e_drift, amin=amin_hist)


# ==================================================================================================== adhesion (sticky dust)
def sticky(test, nx, NP, dt=2.5e-4, tchk=None):
    """Adhesion / zero-viscosity Burgers dust as sticky sheets: when two sheets meet they merge, conserving mass and
    momentum (the nu -> 0 limit of the adhesion model; E, Rykov & Sinai 1996).  Well-posed, dissipative, single-stream."""
    g = Grid(nx); tchk = TCHK[test] if tchk is None else tchk
    x = (np.arange(NP) + 0.5) * L / NP; v = v_init(x); m = np.full(NP, RHOB * L / NP)
    grav = GRAV[test]
    E0 = None

    def acc(x, m):
        if grav == 0:
            return np.zeros_like(x)
        cm = np.cumsum(m) - 0.5 * m
        a = -grav * (cm - RHOB * x)
        return a - np.sum(a * m) / np.sum(m)

    def merge(x, v, m):
        while True:
            bad = np.nonzero(np.diff(x) < 0)[0]
            if bad.size == 0:
                return x, v, m
            keep = np.ones(x.size, bool)
            i_prev = -2
            for i in bad:                                          # merge i+1 into i (left to right, skip chained)
                if i == i_prev + 1 or not keep[i]:
                    continue
                mt = m[i] + m[i + 1]
                x[i] = (m[i] * x[i] + m[i + 1] * x[i + 1]) / mt
                v[i] = (m[i] * v[i] + m[i + 1] * v[i + 1]) / mt
                m[i] = mt; keep[i + 1] = False; i_prev = i
            x, v, m = x[keep], v[keep], m[keep]

    def kin(v, m):
        return float(0.5 * np.sum(m * v * v))
    t, out, K0 = 0.0, {}, kin(v, m)
    a = acc(x, m)
    for tc in tchk:
        n = int(round((tc - t) / dt))
        for _ in range(n):
            v = v + 0.5 * dt * a; x = x + dt * v
            x, v, m = merge(x, v, m)
            x %= L
            o = np.argsort(x, kind="stable"); x, v, m = x[o], v[o], m[o]
            a = acc(x, m); v = v + 0.5 * dt * a
            t += dt
        out[tc] = g.smooth(g.cic(x, m) / (L / NP) * (L / NP)) if False else g.smooth(cic_mass(g, x, m))
    return dict(rs=out, n_clusters=int(x.size), K_frac=kin(v, m) / K0 if K0 > 0 else None)


def cic_mass(g, xp, m):
    s = (xp % L) / g.dx; i0 = np.floor(s).astype(np.int64); f = s - i0
    rho = (np.bincount(i0 % g.nx, weights=(1 - f) * m, minlength=g.nx)
           + np.bincount((i0 + 1) % g.nx, weights=f * m, minlength=g.nx))
    return rho / g.dx


# ==================================================================================================== Vlasov continuum
def vlasov(test, sig, nx=512, nv=1024, vmax=3.5, dt=2e-3, tchk=None, bgk_nu=0.0, filt=True):
    """The collisionless phase-space continuum f(x, v, t) on an Eulerian (x, v) grid (no particles anywhere):
    d_t f + v d_x f - d_x Phi d_v f = 0, Strang-split semi-Lagrangian (Cheng & Knorr 1976) with exact FFT shifts in x
    and v and order-8 high-k filters in x and v (grid-scale coarse-graining of f, which acts as numerical warmth).  The cold beam is
    represented with a Gaussian velocity width sig.  bgk_nu > 0 (MUTATE) adds BGK collisions that relax f to the local
    Maxwellian at rate nu: the continuum then becomes a collisional fluid."""
    tchk = TCHK[test] if tchk is None else tchk
    x = np.arange(nx) * L / nx; dvv = 2 * vmax / nv; v = -vmax + (np.arange(nv) + 0.5) * dvv
    X, Vg = np.meshgrid(x, v, indexing="ij")
    f = RHOB * np.exp(-0.5 * ((Vg - v_init(X)) / sig) ** 2) / (math.sqrt(2 * math.pi) * sig)
    kx = 2 * np.pi * np.fft.rfftfreq(nx, L / nx); kv = 2 * np.pi * np.fft.rfftfreq(nv, dvv)
    grav = GRAV[test]
    filt_v = np.exp(-36 * (kv / kv[-1]) ** 8)[None, :] if filt else 1.0      # grid-scale coarse-graining of f
    filt_x = np.exp(-36 * (kx / kx[-1]) ** 8)[:, None] if filt else 1.0
    mass0 = f.sum() * dvv * L / nx

    def xshift(f, tau):
        fk = np.fft.rfft(f, axis=0); fk *= np.exp(-1j * np.outer(kx, v * tau)) * filt_x; return np.fft.irfft(fk, nx, axis=0)

    def vshift(f, a, tau):
        fk = np.fft.rfft(f, axis=1); fk *= np.exp(-1j * np.outer(a * tau, kv)); fk *= filt_v
        return np.fft.irfft(fk, nv, axis=1)

    def accel(f):
        rho = f.sum(axis=1) * dvv
        if grav == 0:
            return rho, np.zeros(nx)
        rk = np.fft.rfft(rho); phik = np.zeros_like(rk); phik[1:] = -grav * rk[1:] / kx[1:] ** 2
        return rho, -np.fft.irfft(1j * kx * phik, nx)

    def bgk(f, h):
        rho = f.sum(axis=1) * dvv
        u = (f * v[None, :]).sum(axis=1) * dvv / np.maximum(rho, 1e-12)
        T = np.maximum((f * (v[None, :] - u[:, None]) ** 2).sum(axis=1) * dvv / np.maximum(rho, 1e-12), (2 * dvv) ** 2)
        g_ = np.exp(-0.5 * (v[None, :] - u[:, None]) ** 2 / T[:, None])
        fM = rho[:, None] * g_ / np.maximum(g_.sum(axis=1, keepdims=True) * dvv, 1e-300)   # exact mass on the v-grid
        return fM + (f - fM) * math.exp(-bgk_nu * h)
    t, out = 0.0, {}
    for tc in tchk:
        if grav == 0 and bgk_nu == 0.0:
            ft = xshift(f, tc); out[tc] = ft.sum(axis=1) * dvv
            continue
        n = max(1, int(math.ceil((tc - t) / dt))); h = (tc - t) / n
        for _ in range(n):
            f = xshift(f, 0.5 * h)
            rho, a = accel(f)
            f = vshift(f, a, h)
            if bgk_nu > 0:
                f = bgk(f, h)
            f = xshift(f, 0.5 * h)
        t = tc; out[tc] = f.sum(axis=1) * dvv
    return dict(rho=out, x=x, fmin=float(f.min()), mass_err=abs(f.sum() * dvv * L / nx / mass0 - 1))


# ==================================================================================================== scoring
def misplaced(g, rs, ref):
    return g.misplaced(rs, ref)


def tracks(M_by_t, sp_by_t, post, min_rho=0.0, e_drift=0.0, t_break=None, check_energy=True):
    """L374's pass rule (lines 41-44 / 400-401) for one test."""
    return (t_break is None and min_rho >= POS_TOL and (not check_energy or e_drift <= E_TOL)
            and all(t in M_by_t and M_by_t[t] <= max(M_TOL, 2 * sp_by_t[t]) for t in post))
