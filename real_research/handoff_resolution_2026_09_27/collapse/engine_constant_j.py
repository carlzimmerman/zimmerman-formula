#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG5_collapse_engine -- a spherical shell collapse with cooling baryons and the vacuum stress trigger (lane CFG5).

Physical coordinates, a flat LCDM background (Lambda enters as + H0^2 Omega_L r), units kpc, km/s, kpc/(km/s) = 0.9778 Gyr.
  * INITIAL PROFILE (the record's FP16 recipe, re-implemented): Lagrangian shells from 0.02 to 3 Lagrangian radii of the z = 0
    host.  Inside, each shell collapses when the host's main progenitor reaches its mass on a 2015 EPS mass-accretion history
    (the form FP16 uses: M(z) = M0 (1+z)^alpha e^(-beta z), from sigma(M) of CLASS's P(k)); outside, the constrained mean
    profile delta_L(<q) = 1.686 sigma^2(q, R_f)/sigma^2(R_f).  Growing-mode (Zel'dovich) start at z = 50.
  * ORBITS: each shell gets a tangential velocity lambda_j v_c at its turnaround (lambda_j uniform in 0.15-0.35, FP16's choice),
    which sets the pericentres; forces from the sorted enclosed mass (exact for spheres), softening 0.2 kpc.
  * BARYONS: a baryon shell follows its dark shell until its own first pericentre; there a fraction f_gal cools into the
    central galaxy (placed as static parcels at f_R r_ta; f_gal from the declared stellar-to-halo relation x 2 for gas,
    f_R = 0.02), the rest stays a hot collisionless tracer.  'dark-only' runs keep every baryon hot (no condensation).
  * THE TRIGGER (the principle): the dark stress at a dark shell, P_d = sum m [(v_r - <v_r>)^2 + v_t^2]/(3 V) over its 2 x 24
    radial neighbours (dark shells and daughters), is compared with P_c = a0^2/(8 pi G).  Only COHERENT dark shells convert:
    from their turnaround until their first apocentre after the first pericentre (the coherence clause).  A converting shell
    becomes daughters kicked isotropically at v_k: the escaping part (sampled over 64 directions against the shell's own
    potential) leaves; the bound part stays, carrying the mean bound kinetic energy (a daughter shell, never converts again).
  * OUTPUT: time-averaged (a > 0.85) enclosed dark, baryonic and daughter masses; conversion and escape budgets.
Declared modelling choices are listed in the lane's ledger.  Nothing here is a result; CFG5_2 runs it.
"""
import math, time
import numpy as np
import CFG5_common as C

GK = C.GK
H0 = 0.1 * C.H_LITTLE                     # km/s/kpc
OM, OL = C.OMEGA_M, C.OMEGA_L
RHOM0 = OM * 3 * H0 ** 2 / (8 * math.pi * GK)          # Msun/kpc^3
PA_TO_INT = C.KPC ** 3 / C.MSUN / 1e6     # Pa -> Msun (km/s)^2 / kpc^3
TU_GYR = C.KPC / 1e3 / (3.15576e16)       # kpc/(km/s) in Gyr


def E(a):
    return np.sqrt(OM / a ** 3 + OL)


def Hof(a):
    return H0 * E(a)


_ag = np.geomspace(1e-3, 1.0, 5000)
_I = np.concatenate([[0.0], np.cumsum(0.5 * (1 / (_ag[1:] * E(_ag[1:])) ** 3 + 1 / (_ag[:-1] * E(_ag[:-1])) ** 3) * np.diff(_ag))])
_I += _ag[0] ** 2.5 / (2.5 * OM ** 1.5)
_D = E(_ag) * _I
_D /= _D[-1]
_F = np.gradient(np.log(_D), np.log(_ag))
_t = np.concatenate([[0.0], np.cumsum(0.5 * (1 / (_ag[1:] * Hof(_ag[1:])) + 1 / (_ag[:-1] * Hof(_ag[:-1]))) * np.diff(_ag))])
_t += (2 / 3) / (H0 * math.sqrt(OM)) * _ag[0] ** 1.5


def Dof(a):
    return np.interp(np.log(a), np.log(_ag), _D)


def fof(a):
    return np.interp(np.log(a), np.log(_ag), _F)


def t_of_a(a):
    return np.interp(np.log(a), np.log(_ag), _t)


def a_of_t(t):
    return np.exp(np.interp(t, _t, np.log(_ag)))


class Sigma:
    """sigma^2 cross-terms of top-hats from CLASS's linear P(k) at z = 0 (kpc units)."""

    def __init__(self):
        cl = C.classy_background(z_max_pk=0.5, kmax=200.0)
        h = C.H_LITTLE
        KH = np.geomspace(1e-4, 190, 3000)
        self.k = KH * h / 1e3
        self.Pk = np.array([cl.pk_lin(kk * h, 0.0) for kk in KH]) * 1e9          # Mpc^3 -> kpc^3
        self.sigma8 = cl.sigma8()

    @staticmethod
    def W(x):
        return np.where(x > 1e-4, 3 * (np.sin(x) - x * np.cos(x)) / np.maximum(x, 1e-4) ** 3, 1.0)

    def cross(self, q, R):
        q = np.atleast_1d(q)
        return C._trap(self.k[None, :] ** 2 * self.Pk[None, :] * self.W(np.outer(q, self.k)) * self.W(self.k * R)[None, :],
                       self.k, axis=1) / (2 * math.pi ** 2)

    def S_of_M(self, M):
        R = (3 * float(M) / (4 * math.pi * RHOM0)) ** (1 / 3)
        return float(self.cross(np.array([R]), R)[0])


def eps_mah(SIG, M0):
    lm = math.log10(M0)
    zf = -0.0064 * lm ** 2 + 0.0237 * lm + 1.8837
    qq = 4.137 * zf ** (-0.9476)
    fM = 1.0 / math.sqrt(max(SIG.S_of_M(M0 / qq) - SIG.S_of_M(M0), 1e-6))
    dDdz = (Dof(1 / 1.01) - Dof(1.0)) / 0.01
    alpha = (1.686 * math.sqrt(2 / math.pi) * dDdz + 1) * fM
    return lambda z: M0 * (1 + np.asarray(z, float)) ** alpha * np.exp(-fM * np.asarray(z, float))


def initial_profile(SIG, M0, Nc, qmin_frac=0.02, qmax_fac=3.0):
    Rf = (3 * M0 / (4 * math.pi * RHOM0)) ** (1 / 3)
    qe = np.geomspace(qmin_frac * Rf, qmax_fac * Rf, Nc + 1)
    qm = ((qe[1:] ** 3 + qe[:-1] ** 3) / 2) ** (1 / 3)
    Mq = 4 * math.pi / 3 * RHOM0 * qm ** 3
    mah = eps_mah(SIG, M0)
    zz = np.linspace(0.0, 60.0, 6000); Mz = mah(zz)
    dL = np.zeros(Nc); inner = qm <= Rf
    zc = np.interp(np.log(Mq[inner]), np.log(Mz[::-1]), zz[::-1], left=60.0, right=0.0)
    dL[inner] = 1.686 / Dof(1 / (1 + zc))
    s_ff = SIG.cross(np.array([Rf]), Rf)[0]
    dL[~inner] = 1.686 * SIG.cross(qm[~inner], Rf) / s_ff
    m = 4 * math.pi / 3 * RHOM0 * (qe[1:] ** 3 - qe[:-1] ** 3)
    return qm, dL, m, Rf


def run(SIG, M0, a0_cap, trigger=True, cooling=True, vk=600.0, Nc=600, fR=0.02, seed=1, eta=0.03, rsoft=0.2, nb=24,
        fgal=None):
    """one collapse; a0_cap is the a0 inside the cap (0 -> P_c = 0: every coherent crossing converts)."""
    rng = np.random.default_rng(seed)
    qm, dL, m, Rf = initial_profile(SIG, M0, Nc)
    fb = C.F_B
    ai = 1 / 51.0
    di = dL * Dof(ai)
    r = ai * qm * (1 - di / 3); v = Hof(ai) * r * (1 - fof(ai) * di / 3)
    N = 2 * Nc
    R = np.concatenate([r, r.copy()]); V = np.concatenate([v, v.copy()])
    M = np.concatenate([(1 - fb) * m, fb * m])
    kind = np.concatenate([np.zeros(Nc, int), np.ones(Nc, int)])   # 0 dark, 1 baryon (not yet cooled), 2 daughter, 3 hot baryon
    J = np.zeros(N)
    phase = np.zeros(N, int)            # 0 expanding, 1 infall, 2 out after first pericentre, 3 phase-mixed
    lamj = np.full(N, 0.25)  # numerical benchmark: identical constant angular momentum field
    r_ta = np.full(N, np.nan)
    gal_R, gal_M = [], []
    if fgal is None:
        fgal = min(max(C.ms_of_mh(M0) * 2.0 / (fb * M0), 0.02), 1.0)
    if not cooling:
        fgal = 0.0
    Pc = C.P_cap(a0_cap) * PA_TO_INT
    t = float(t_of_a(ai)); t0 = float(t_of_a(1.0))
    alive = np.ones(N, bool)
    budget = dict(converted=0.0, escaped=0.0, recaptured=0.0, fired_shells=0)
    dark_init = float(np.sum((1 - fb) * m))
    snaps = []
    nstep = 0
    T0 = time.time()

    def enclosed():
        ia = np.where(alive)[0]
        o = np.argsort(R[ia]); ids = ia[o]
        Ms = M[ids]
        Menc_s = np.cumsum(Ms) - 0.5 * Ms
        if gal_R:
            gR = np.asarray(gal_R); gM = np.asarray(gal_M)
            og = np.argsort(gR); cg = np.cumsum(gM[og]); gRs = gR[og]
            Mg = np.interp(R[ids], gRs, cg, left=0.0)
            Mg = np.where(R[ids] < gRs[0], cg[0] * (R[ids] / gRs[0]) ** 3, Mg)
        else:
            Mg = np.zeros(len(ids))
        Menc = np.zeros(N); Menc[ids] = Menc_s + Mg
        # potential: -G Menc/r - G sum_{outer} m/r (galaxy parcels are inside every relevant shell)
        inv = Ms / R[ids]
        outer = np.concatenate([np.cumsum(inv[::-1])[::-1][1:], [0.0]])
        phi = np.zeros(N); phi[ids] = -GK * (Menc_s + Mg) / R[ids] - GK * outer
        return Menc, phi, ids

    def accel(Menc):
        re2 = R ** 2 + rsoft ** 2
        return np.where(alive, -GK * Menc * R / re2 ** 1.5 + J ** 2 / np.maximum(R, 1e-6) ** 3 + H0 ** 2 * OL * R, 0.0)

    Menc, phi, ids = enclosed()
    A = accel(Menc)
    while t < t0:
        live = alive & (M > 0)
        tdyn = float(np.min(np.sqrt(np.maximum(R[live], rsoft) ** 3 / (GK * np.maximum(Menc[live], 1.0)))))
        dt = min(eta * tdyn, 0.05 / H0 * 0.01)
        if t + dt > t0:
            dt = t0 - t
        V += 0.5 * dt * A
        R += dt * V
        np.maximum(R, 1e-3, out=R)
        t += dt
        Menc, phi, ids = enclosed()
        A = accel(Menc)
        V += 0.5 * dt * A
        nstep += 1
        turn = alive & (phase == 0) & (V < 0)
        if turn.any():
            vc = np.sqrt(GK * Menc[turn] / R[turn])
            J[turn] = lamj[turn] * R[turn] * vc
            phase[turn] = 1; r_ta[turn] = R[turn]
        phase[alive & (phase == 1) & (V > 0)] = 2
        phase[alive & (phase == 2) & (V < 0)] = 3
        cool_now = alive & (kind == 1) & (phase >= 2)
        if cool_now.any():
            for i in np.where(cool_now)[0]:
                mc = fgal * M[i]
                if mc > 0:
                    gal_R.append(max(fR * r_ta[i], rsoft)); gal_M.append(mc)
                M[i] -= mc
                kind[i] = 3
        if trigger and nstep % 5 == 0:
            dk = np.where(alive & ((kind == 0) | (kind == 2)))[0]
            o = np.argsort(R[dk]); di_ = dk[o]
            Rs = R[di_]; Ms = M[di_]; Vs = V[di_]; Vt2 = (J[di_] / Rs) ** 2
            n = len(di_)
            cm = np.concatenate([[0.0], np.cumsum(Ms)]); cmv = np.concatenate([[0.0], np.cumsum(Ms * Vs)])
            cmv2 = np.concatenate([[0.0], np.cumsum(Ms * (Vs ** 2 + Vt2))])
            lo = np.clip(np.arange(n) - nb, 0, n - 1); hi = np.clip(np.arange(n) + nb, 0, n - 1)
            mm = cm[hi + 1] - cm[lo]; mv = cmv[hi + 1] - cmv[lo]; mv2 = cmv2[hi + 1] - cmv2[lo]
            vol = 4 * math.pi / 3 * np.maximum(Rs[hi] ** 3 - Rs[lo] ** 3, 1e-9)
            Pd = (mv2 - mv ** 2 / np.maximum(mm, 1e-30)) / (3 * vol)
            coh = (kind[di_] == 0) & ((phase[di_] == 1) | (phase[di_] == 2))
            fire = di_[coh & (Pd > Pc)]
            if len(fire):
                nh = rng.normal(size=(len(fire), 64, 3)); nh /= np.linalg.norm(nh, axis=2)[:, :, None]
                vt = J[fire] / R[fire]
                vvec = np.stack([V[fire], vt, np.zeros(len(fire))], 1)
                w = vvec[:, None, :] + vk * nh
                Ek = 0.5 * np.sum(w ** 2, axis=2) + phi[fire][:, None]
                esc = Ek > 0
                fe = esc.mean(1)
                bound = ~esc
                nbnd = np.maximum(bound.sum(1), 1)
                vr2 = np.where(bound, w[:, :, 0] ** 2, 0).sum(1) / nbnd
                vt2 = np.where(bound, w[:, :, 1] ** 2 + w[:, :, 2] ** 2, 0).sum(1) / nbnd
                budget["converted"] += float(M[fire].sum()); budget["escaped"] += float((fe * M[fire]).sum())
                budget["recaptured"] += float(((1 - fe) * M[fire]).sum()); budget["fired_shells"] += len(fire)
                M[fire] *= (1 - fe)
                V[fire] = np.where(fe < 1, np.sign(V[fire]) * np.sqrt(vr2), V[fire])
                J[fire] = np.where(fe < 1, np.sqrt(vt2) * R[fire], J[fire])
                kind[fire] = 2
                alive[fire[M[fire] <= 0]] = False
        if float(a_of_t(t)) > 0.85 and (not snaps or t - snaps[-1][0] > 0.1):
            snaps.append((t, R.copy(), M.copy(), kind.copy(), np.asarray(gal_R, float), np.asarray(gal_M, float)))
    return dict(snaps=snaps, budget=budget, dark_init=dark_init, M0=M0, Rf=Rf, nstep=nstep, runtime=time.time() - T0,
                galaxy=float(np.sum(gal_M)), fgal=fgal)


def profiles(res, rgrid):
    """time-averaged enclosed dark (survivors + bound daughters), daughters alone, baryons (galaxy + hot) on rgrid [kpc]."""
    Md, Mdau, Mb = [], [], []
    for (t, R, M, kind, gR, gM) in res["snaps"]:
        def cum(sel):
            if not sel.any():
                return np.zeros_like(rgrid)
            o = np.argsort(R[sel])
            return np.interp(rgrid, R[sel][o], np.cumsum(M[sel][o]), left=0.0)
        Md.append(cum((kind == 0) | (kind == 2)))
        Mdau.append(cum(kind == 2))
        mb = cum((kind == 3) | (kind == 1))
        if len(gR):
            og = np.argsort(gR)
            mb = mb + np.interp(rgrid, gR[og], np.cumsum(gM[og]), left=0.0)
        Mb.append(mb)
    return np.mean(Md, 0), np.mean(Mdau, 0), np.mean(Mb, 0)


def r200_of(rgrid, Mtot):
    rho_mean = Mtot / (4 * math.pi / 3 * rgrid ** 3)
    target = 200 * 3 * H0 ** 2 / (8 * math.pi * GK)
    k = np.where(rho_mean >= target)[0]                     # the OUTERMOST radius still above 200 rho_crit (hollow centres)
    return float(rgrid[k[-1]]) if len(k) else float(rgrid[0])
