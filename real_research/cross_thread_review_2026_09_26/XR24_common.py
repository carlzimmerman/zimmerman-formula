#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR24_common.py -- the machinery of review lane XR24 (the Local Group's Hubble flow in 3-D, in the chain's law).  A library:
it writes nothing and prints nothing.  Everything committed that it reuses is exec'd or imported read-only:
  * FP11's module (its main() is not run): FP6's band-passed phantom(), FP9's yield hook, the two-body interaction integral
    dg_body, the force table / Acc / shooter / branch finder, the LG cosmology, the UNGC reader;
  * FP13's code (its module header and the state block of its main(), exec'd): the H_S tables L(z), y_th(z);
  * FP12's module (its main() is not run): k02's UNGC group baryons.
New here: the 3-D interaction field of N point masses (direct integral of the band-passed dipole kernel; a spherical-harmonic
finite-volume solver), the N-body system with FP11's exact pair tables live and the rest of the interaction as a Picard-
iterated history, Newton shooting for the numerical-action boundary conditions, the test-particle machinery (3-D R0 rays,
the observed dwarfs' solutions), the Local Volume bodies and the flow sample.
"""
# ============================================================================================================== part: lib
import os, sys, io, json, math, time, textwrap, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from scipy.special import ive, sph_harm, erf
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DC = os.path.join(REPO, "real_research", "derivation_chain_2026")
sys.path.insert(0, DC); sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
with contextlib.redirect_stdout(io.StringIO()):
    import FP11_local_group_flyby as F11                     # noqa: E402  (main() not run)

G, MSUN, MPC, KPC, GYR = F11.G, F11.MSUN, F11.MPC, F11.KPC, F11.GYR
M6 = F11.M6
phantom, RG, x_P2, Efac, gfrac = F11.phantom, F11.RG, F11.x_P2, F11.Efac, F11.gfrac
YIELD = F11.YIELD
A0 = F11.A0
LG_H0, LG_OM, LG_OL = F11.LG_H0, F11.LG_OM, F11.LG_OL
L_OL_H02 = F11.L_OL_H02
EPS = F11.EPS


def Xvec(gx, gy, gz, a0, yth):
    gm = np.sqrt(gx * gx + gy * gy + gz * gz)
    x = x_P2(gm / a0 - (yth or 0.0))
    f = np.where(gm > 0, a0 * x / np.maximum(gm, 1e-300), 0.0)
    return f * gx, f * gy, f * gz


def W_field(P, bodies, a0, Lm, yth):
    """W = X(sum g_bp,j) - sum X(g_bp,j) at points P (..., 3) [m]; bodies: list of (m_kg, (x, y, z) [m])."""
    sx = np.zeros(P.shape[:-1]); sy = np.zeros_like(sx); sz = np.zeros_like(sx)
    wx = np.zeros_like(sx); wy = np.zeros_like(sx); wz = np.zeros_like(sx)
    for (m, xb) in bodies:
        dx = P[..., 0] - xb[0]; dy = P[..., 1] - xb[1]; dz = P[..., 2] - xb[2]
        r = np.sqrt(dx * dx + dy * dy + dz * dz); r = np.maximum(r, 1e-6 * KPC)
        fac = -G * m * Efac(r, Lm) / r ** 3
        gx, gy, gz = fac * dx, fac * dy, fac * dz
        sx += gx; sy += gy; sz += gz
        X1, X2, X3 = Xvec(gx, gy, gz, a0, yth)
        wx -= X1; wy -= X2; wz -= X3
    X1, X2, X3 = Xvec(sx, sy, sz, a0, yth)
    return wx + X1, wy + X2, wz + X3


def _ylm_theta(l, m, th):
    """fully normalised Y_lm(theta, phi = 0) (Condon-Shortley), real."""
    return np.real(sph_harm(m, l, 0.0, th))


class Grid3:
    """spherical (r, theta, phi) finite-volume grid about a centre: divergence of W by face fluxes, spherical-harmonic
    projection with exact cell integrals, the Gaussian's exact multipole kernel for S_L, Poisson recursion (FP11's)."""
    def __init__(self, rmin_kpc=2.0, rmax_kpc=40000.0, nr=180, nth=64, nph=128, lmax=48, lsm=None, nsub=8):
        self.re = np.geomspace(rmin_kpc, rmax_kpc, nr + 1) * KPC; self.rc = np.sqrt(self.re[1:] * self.re[:-1]); self.nr = nr
        self.te = np.linspace(0.0, math.pi, nth + 1); self.tc = 0.5 * (self.te[1:] + self.te[:-1]); self.nth = nth
        self.dph = 2 * math.pi / nph; self.pe = np.arange(nph) * self.dph; self.pc = self.pe + 0.5 * self.dph; self.nph = nph
        self.lmax = lmax; self.lsm = lmax if lsm is None else lsm
        self.dmu = np.cos(self.te[:-1]) - np.cos(self.te[1:]); self.dth = self.te[1:] - self.te[:-1]
        self.vol = (self.re[1:] ** 3 - self.re[:-1] ** 3) / 3.0; self.a2 = (self.re[1:] ** 2 - self.re[:-1] ** 2) / 2.0
        xg, wg = np.polynomial.legendre.leggauss(nsub)
        L1 = lmax + 1
        self.Pint = np.zeros((L1, L1, nth)); self.Yc = np.zeros((L1, L1, nth)); self.dYc = np.zeros((L1, L1, nth))
        tq = (0.5 * (self.te[1:] - self.te[:-1]))[:, None] * xg[None, :] + self.tc[:, None]          # (nth, nsub)
        wq = (0.5 * (self.te[1:] - self.te[:-1]))[:, None] * wg[None, :] * np.sin(tq)
        dt = 1e-6
        for l in range(L1):
            for m in range(l + 1):
                self.Pint[l, m] = (_ylm_theta(l, m, tq) * wq).sum(axis=1)
                self.Yc[l, m] = _ylm_theta(l, m, self.tc)
                self.dYc[l, m] = (_ylm_theta(l, m, self.tc + dt) - _ylm_theta(l, m, self.tc - dt)) / (2 * dt)
        self.lvec = np.arange(L1)
        ms = np.arange(L1)
        # phi-cell integral factor for the analysis: Int_cell e^{-i m phi} dphi = dph sinc(m dph/2) e^{-i m phi_k}
        self.phfac = self.dph * np.sinc(ms * self.dph / 2 / math.pi) * np.exp(-1j * ms * self.dph / 2)
        R, T, PH = np.meshgrid(self.rc, self.tc, self.pc, indexing="ij")
        self.st, self.ct = np.sin(T), np.cos(T); self.sp, self.cp = np.sin(PH), np.cos(PH)
        self._faces()

    def _faces(self):
        """face-centre points (unit-free directions; positions formed on demand) and the local unit vectors there."""
        def sph(r, t, p):
            R, T, PH = np.meshgrid(r, t, p, indexing="ij")
            return R, T, PH
        self.F_r = sph(self.re, self.tc, self.pc)
        self.F_t = sph(self.rc, self.te, self.pc)
        self.F_p = sph(self.rc, self.tc, self.pe)

    @staticmethod
    def _cart(R, T, PH):
        st, ct, sp, cp = np.sin(T), np.cos(T), np.sin(PH), np.cos(PH)
        return np.stack([R * st * cp, R * st * sp, R * ct], axis=-1), (st, ct, sp, cp)

    def divergence(self, Wfun, centre, rot):
        """q = div W (cell averages) by face fluxes.  Wfun(P) -> (wx, wy, wz) in the WORLD frame; the grid frame is
        world = centre + rot @ local."""
        def at(F):
            Pl, (st, ct, sp, cp) = self._cart(*F)
            Pw = centre[None, None, None, :] + Pl @ rot.T
            wx, wy, wz = Wfun(Pw)
            W = np.stack([wx, wy, wz], axis=-1) @ rot                      # back to the local frame
            er = np.stack([st * cp, st * sp, ct], axis=-1)
            et = np.stack([ct * cp, ct * sp, -st], axis=-1)
            ep = np.stack([-sp, cp, np.zeros_like(sp)], axis=-1)
            return (W * er).sum(-1), (W * et).sum(-1), (W * ep).sum(-1)
        Wr, _, _ = at(self.F_r); fr = (self.re[:, None, None] ** 2) * Wr * self.dmu[None, :, None] * self.dph
        _, Wt, _ = at(self.F_t); ft = np.sin(self.te)[None, :, None] * Wt * self.a2[:, None, None] * self.dph
        _, _, Wp = at(self.F_p); fp = Wp * self.a2[:, None, None] * self.dth[None, :, None]
        fpn = np.roll(fp, -1, axis=2)
        num = (fr[1:] - fr[:-1]) + (ft[:, 1:] - ft[:, :-1]) + (fpn - fp)
        return num / (self.vol[:, None, None] * self.dmu[None, :, None] * self.dph)

    def analyse(self, q):
        Q = np.fft.rfft(q, axis=2)                                            # sum_k q_k e^{-2 pi i m k/n}
        L1 = self.lmax + 1; out = np.zeros((self.nr, L1, L1), complex)
        for m in range(L1):
            Qm = Q[:, :, m] * self.phfac[m]
            out[:, m:, m] = Qm @ self.Pint[m:, m, :].T
        return out

    def smooth(self, qlm, Lm):
        """(S_L q)_lm with the Gaussian's exact multipole kernel (FP11's smooth, per l for all m); unresolved rows: identity."""
        if Lm is None:
            return np.zeros_like(qlm)
        r = self.rc; dr = self.re[1:] - self.re[:-1]; unres = Lm < 2.0 * dr
        Zs = np.maximum(np.outer(r, r) / Lm ** 2, 1e-300)
        lnG2 = -(r[:, None] - r[None, :]) ** 2 / (2 * Lm ** 2)
        lnpref = -1.5 * math.log(2 * math.pi * Lm ** 2) + math.log(4 * math.pi) + np.log(r ** 2 * dr)[None, :]
        out = np.zeros_like(qlm)
        for l in range(min(self.lsm, self.lmax) + 1):
            with np.errstate(all="ignore"):
                lniel = 0.5 * np.log(math.pi / (2 * Zs)) + np.log(np.maximum(ive(l + 0.5, Zs), 1e-300))
                K = np.exp(np.minimum(lnpref + lnG2 + lniel, 700.0))
            K[unres, :] = 0.0
            out[:, l, :] = K @ qlm[:, l, :]
            out[unres, l, :] = qlm[unres, l, :]
        if self.lsm < self.lmax:
            out[unres, self.lsm + 1:, :] = qlm[unres, self.lsm + 1:, :]
        return out

    def poisson(self, qlm):
        """FP11's recursion per l, vectorised over m: Psi_lm and dPsi_lm/dr at the cell centres."""
        nr, L1 = self.nr, self.lmax + 1; l = np.arange(L1).astype(float)[:, None]; re, rc = self.re, self.rc
        I = np.zeros((nr, L1, L1), complex); acc = np.zeros((L1, L1), complex)
        for i in range(nr):
            a = re[i] / rc[i]; I[i] = acc * a ** (l + 1) + qlm[i] * rc[i] ** 2 * (1 - a ** (l + 3)) / (l + 3)
            b = re[i] / re[i + 1]; acc = acc * b ** (l + 1) + qlm[i] * re[i + 1] ** 2 * (1 - b ** (l + 3)) / (l + 3)
        O = np.zeros((nr, L1, L1), complex); acc = np.zeros((L1, L1), complex)
        for i in range(nr - 1, -1, -1):
            a = rc[i] / re[i + 1]; b = re[i] / re[i + 1]
            with np.errstate(all="ignore"):
                half = np.where(l == 2, rc[i] ** 2 * np.log(re[i + 1] / rc[i]), rc[i] ** 2 * (a ** (l - 2) - 1) / (2 - l))
                full = np.where(l == 2, re[i] ** 2 * np.log(re[i + 1] / re[i]), re[i] ** 2 * (b ** (l - 2) - 1) / (2 - l))
            O[i] = acc * a ** l + qlm[i] * half; acc = acc * b ** l + qlm[i] * full
        c = 1.0 / (2 * l + 1)
        Psi = -c[None] * (I + O)
        dPsi = -c[None] * (-(l[None] + 1) * I / rc[:, None, None] + l[None] * O / rc[:, None, None])
        return Psi, dPsi

    def synth(self, flm, kind="Y"):
        """sum_lm f_lm Y_lm (kind 'Y'), sum f_lm dY/dtheta ('dY'), sum f_lm i m Y ('imY') at the cell centres (real field)."""
        L1 = self.lmax + 1; out = np.zeros((self.nr, self.nth, self.nph // 2 + 1), complex)
        for m in range(L1):
            B = self.Yc if kind in ("Y", "imY") else self.dYc
            A = flm[:, m:, m] @ B[m:, m, :]                                   # (nr, nth)
            if kind == "imY":
                A = A * (1j * m)
            out[:, :, m] = A * (1.0 if m == 0 else 2.0)
        # value = Re sum_m out_m e^{i m phi_k}; phi_k = (k + 1/2) dph
        ms = np.arange(self.nph // 2 + 1)
        out = out * np.exp(1j * ms * self.dph / 2)[None, None, :]
        # irfft computes (1/n) [X_0 + 2 Re sum X_m e^{2 pi i m k/n}] for hermitian input; we built 2x already -> use real part directly
        vals = np.real(np.fft.ifft(np.concatenate([out, np.zeros((self.nr, self.nth, self.nph - out.shape[2]), complex)], axis=2), axis=2)) * self.nph
        return vals

    def field(self, q, Lm):
        qlm = self.analyse(q)
        Psi, dPsi = self.poisson(qlm - self.smooth(qlm, Lm))
        gr = self.synth(dPsi, "Y")
        gt = self.synth(Psi, "dY") / self.rc[:, None, None]
        gp = self.synth(Psi, "imY") / (self.rc[:, None, None] * self.st)
        # local Cartesian
        gx = gr * self.st * self.cp + gt * self.ct * self.cp - gp * self.sp
        gy = gr * self.st * self.sp + gt * self.ct * self.sp + gp * self.cp
        gz = gr * self.ct - gt * self.st
        return np.stack([gx, gy, gz], axis=-1)

    def interp(self, F, Pl):
        """trilinear in (ln r, theta, phi) of a local-frame Cartesian field F (nr, nth, nph, 3) at local points Pl (..., 3)."""
        r = np.sqrt((Pl ** 2).sum(-1)); th = np.arccos(np.clip(Pl[..., 2] / np.maximum(r, 1e-300), -1, 1))
        ph = np.mod(np.arctan2(Pl[..., 1], Pl[..., 0]), 2 * math.pi)
        lr = np.log(self.rc); dl = lr[1] - lr[0]
        ir = np.clip((np.log(np.maximum(r, self.rc[0])) - lr[0]) / dl, 0, self.nr - 1.000001)
        it = np.clip((th - self.tc[0]) / (self.tc[1] - self.tc[0]), 0, self.nth - 1.000001)
        ip = (ph - self.pc[0]) / self.dph; ip = np.mod(ip, self.nph)
        i0 = ir.astype(int); j0 = it.astype(int); k0 = np.floor(ip).astype(int) % self.nph; k1 = (k0 + 1) % self.nph
        fr = ir - i0; ft = it - j0; fp = ip - np.floor(ip)
        out = 0.0
        for di, wi in ((0, 1 - fr), (1, fr)):
            for dj, wj in ((0, 1 - ft), (1, ft)):
                for kk, wk in ((k0, 1 - fp), (k1, fp)):
                    out = out + (wi * wj * wk)[..., None] * F[i0 + di, j0 + dj, kk]
        out = np.where((r > self.re[-1])[..., None], 0.0, out)
        return out


def rot_to(zdir):
    """rotation matrix whose third column is zdir (world = rot @ local)."""
    z = np.asarray(zdir, float); z = z / np.linalg.norm(z)
    t = np.array([1.0, 0, 0]) if abs(z[0]) < 0.9 else np.array([0, 1.0, 0])
    x = t - (t @ z) * z; x /= np.linalg.norm(x); y = np.cross(z, x)
    return np.stack([x, y, z], axis=1)


def direct_W_at(bodies, iA, a0, Lm, yth, ns=200, nmu=96, nphi=96, smin_fac=1e-4, smax=None):
    """the interaction field P(1 - S_L) W at body iA by the direct 3-D integral of the band-passed dipole kernel:
    g = W(A)/3 + Int ds/s dOmega/(4 pi) [A'(u) n (n.W) + E(u) W],  A' = -(3E + sqrt(2/pi) u^3 e^{-u^2/2})."""
    xA = np.asarray(bodies[iA][1], float)
    dmin = min(np.linalg.norm(np.asarray(b[1]) - xA) for j, b in enumerate(bodies) if j != iA)
    dmax = max(np.linalg.norm(np.asarray(b[1]) - xA) for j, b in enumerate(bodies) if j != iA)
    if smax is None:
        smax = (1e4 * dmax) if Lm is None else max(60 * Lm, 60 * dmax)
    s = np.geomspace(smin_fac * dmin, smax, ns)
    mu, wmu = np.polynomial.legendre.leggauss(nmu); phi = (np.arange(nphi) + 0.5) * 2 * math.pi / nphi
    st = np.sqrt(1 - mu ** 2)
    nx = st[:, None] * np.cos(phi)[None, :]; ny = st[:, None] * np.sin(phi)[None, :]; nz = mu[:, None] * np.ones_like(phi)[None, :]
    n = np.stack([nx, ny, nz], axis=-1)                                         # (nmu, nphi, 3)
    wang = (wmu[:, None] * np.ones(nphi)[None, :]) * (2 * math.pi / nphi) / (4 * math.pi)
    # W at the body itself: X(g_A + g_rest) - X(g_A) -> 0 (X saturates), so W(A) = -sum_{j != A} X(g_bp,j(A))
    WA = np.zeros(3)
    for j, (m, xb) in enumerate(bodies):
        if j == iA:
            continue
        dv = xA - np.asarray(xb, float); r = float(np.linalg.norm(dv)); fac = -G * m * float(Efac(np.array([r]), Lm)[0]) / r ** 3
        WA -= np.array(Xvec(np.array([fac * dv[0]]), np.array([fac * dv[1]]), np.array([fac * dv[2]]), a0, yth)).ravel()
    acc = np.zeros(3)
    rows = []
    for si in s:
        P = xA[None, None, :] + si * n
        wx, wy, wz = W_field(P, bodies, a0, Lm, yth)
        W = np.stack([wx, wy, wz], axis=-1)
        if Lm is None:
            E, Ap = 1.0, -3.0
        else:
            u = si / Lm; E = float(Efac(np.array([si]), Lm)[0]); Ap = -(3 * E + math.sqrt(2 / math.pi) * u ** 3 * math.exp(-u * u / 2))
        integ = (Ap * n * (n * W).sum(-1)[..., None] + E * W)
        rows.append((integ * wang[..., None]).sum(axis=(0, 1)))
    rows = np.array(rows)
    acc = np.trapz(rows, np.log(s), axis=0)
    return WA / 3.0 + acc

# ============================================================================================================== part: core
warnings.filterwarnings("ignore")


LNAT = F11.LNAT                                                              # FP11's 49 epochs, ln 0.02 .. 0
DGRID = F11.DGRID                                                            # FP11's 64 separations, 2 kpc .. 8 Mpc


# ================================================================================================= the laws
_HS = {}


def hs_tables():
    """FP13's headline state separator (H_S): L at delta_c on the nonlinear field, y_th = band-passed web rms x max(0, 2q);
    FP13's own code exec'd read-only (module header + the state block of its main()), nothing edited."""
    if not _HS:
        p = os.path.join(DC, "FP13_separator_from_state.py"); src = open(p).read()
        head = src[:src.index("def main():")]
        m1 = "    # " + "-" * 93 + " names from the machinery"
        m2 = "    # " + "-" * 93 + " the general separator model + gates"
        body = textwrap.dedent(src[src.index(m1):src.index(m2)])
        ns = {"__file__": p, "__name__": "fp13_machinery"}
        old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(head, p, "exec"), ns)
                ns["P"] = lambda *a, **k: None
                exec(compile(body, p, "exec"), ns)
                LH = ns["L_table"](ns["DELTA_C"], "NL")
                yh, yt, rms = ns["yth_state"](LH, "NL", "ramp", 1.0)
        finally:
            if old is None: os.environ.pop("MUTATE", None)
            else: os.environ["MUTATE"] = old
        _HS.update(lna=np.array(ns["LNA"]), LH=np.array(LH), yth={f: np.array(yt[f]) for f in ("canonical", "alt")},
                   z_q0=float(ns["Z_Q0"]), fun_of=ns["fun_of"])
    return _HS


class Law:
    """kind: 'HS' (FP13's state separator, the chain's current law), 'HY' (FP9's separator, FP11's scored law), 'P2' (FP7's
    plain root, no separator: the MUTATE law), 'NEWTON' (the LCDM control's gravity: no MOND sector)."""
    def __init__(self, kind, foot):
        self.kind, self.foot = kind, foot
        self.a0 = A0[foot]
        self.mond = kind != "NEWTON"
        if kind == "HS":
            t = hs_tables(); self._lna = t["lna"]; self._lL = np.log(t["LH"]); self._y = t["yth"][foot]

    def L(self, a):
        if self.kind == "HS":
            return float(np.exp(np.interp(math.log(a), self._lna, self._lL))) * MPC          # FP13's hook11, verbatim in effect
        if self.kind == "HY":
            return F11.L_LAMBDA * F11.LG_OmL(a) ** (F11.HEAD["n"] / 2.0) * MPC               # FP11's L_of_a
        return None

    def yth(self, a):
        if self.kind == "HS":
            return max(float(np.interp(math.log(a), self._lna, self._y)), 0.0)
        if self.kind == "HY":
            return F11.HEAD["y25"] * (F11.LG_OmL(1 / 1.25) / F11.LG_OmL(a)) ** F11.HEAD["pp"]
        return None

    @property
    def epoch_dependent(self):
        return self.kind in ("HS", "HY")


def iso_table(m_kg, law, lna=LNAT):
    """enclosed isolated phantom of a point mass on FP6's grid RG at the epochs lna (FP11's PairField rows)."""
    out = np.zeros((len(lna), len(RG)))
    if not law.mond:
        return out
    rows = range(len(lna)) if law.epoch_dependent else [len(lna) - 1]
    for e in rows:
        a = math.exp(lna[e]); L = law.L(a); yt = law.yth(a)
        out[e] = phantom(m_kg, law.a0, L, yt, YIELD if yt else 4)
    if not law.epoch_dependent:
        out[:] = out[-1]
    return out


def pair_table(mA, mB, law, isoB, lna=LNAT, dgrid=DGRID):
    """A's MOND acceleration toward B (B's isolated phantom at A + the interaction field at A, FP11's dg_body), times d^2 --
    exactly FP11's force_table split per body (Acc interpolates the relative sum of the two)."""
    T = np.zeros((len(lna), len(dgrid)))
    if not law.mond:
        return T
    rows = range(len(lna)) if law.epoch_dependent else [len(lna) - 1]
    for e in rows:
        a = math.exp(lna[e]); L = law.L(a); yt = law.yth(a)
        gMB = G * np.interp(dgrid, RG, isoB[e]) / dgrid ** 2
        for k, d in enumerate(dgrid):
            T[e, k] = (gMB[k] - F11.dg_body(mA, mB, d, law.a0, L, yt)) * d ** 2
    if not law.epoch_dependent:
        T[:] = T[-1]
    return T


def interp_TM(TM, lna, ld, d0, l, d):
    """FP11's Acc.mond, verbatim in effect: bilinear in (ln a, ln d) of the table x d^2, linear below the first separation."""
    j = (l - lna[0]) / (lna[1] - lna[0]); j0 = int(min(max(math.floor(j), 0), len(lna) - 2))
    fj = min(max(j - j0, 0.0), 1.0); row = (1 - fj) * TM[j0] + fj * TM[j0 + 1]
    dd = np.maximum(d, d0); m = np.interp(np.log(dd), ld, row) / dd ** 2
    return np.where(d < d0, m * d / d0, m)


def H_of(a):
    return LG_H0 * math.sqrt(LG_OM / a ** 3 + LG_OL)


# ================================================================================================= the N-body system
class System:
    """bodies (masses [kg]) under a law: live forces = softened Newton + isolated phantoms (all pairs) + FP11's exact two-body
    interaction tables for the listed 'live pairs'; the rest of the interaction field enters as a frozen history Delta_i(ln a)
    from the 3-D field solve (updated by Picard iteration)."""
    def __init__(self, masses, law, live_pairs=(), soft=EPS, conv="A", lna=LNAT, pair_tabs=None, iso_tabs=None):
        self.m = np.asarray(masses, float); self.N = len(self.m); self.law = law; self.soft = soft; self.conv = conv
        self.lna = np.asarray(lna); self.lRG = np.log(RG)
        self.iso = iso_tabs if iso_tabs is not None else [iso_table(mi, law, self.lna) for mi in self.m]
        self.live = list(live_pairs)
        self.TM = {}
        for (A, B) in self.live:
            if pair_tabs is not None and (A, B) in pair_tabs:
                self.TM[(A, B)] = pair_tabs[(A, B)]; self.TM[(B, A)] = pair_tabs[(B, A)]
            else:
                self.TM[(A, B)] = pair_table(self.m[A], self.m[B], law, self.iso[B], self.lna)
                self.TM[(B, A)] = pair_table(self.m[B], self.m[A], law, self.iso[A], self.lna)
        self.ld = np.log(DGRID); self.d0 = DGRID[0]
        self.livemask = np.zeros((self.N, self.N), bool)
        for (A, B) in self.live:
            self.livemask[A, B] = self.livemask[B, A] = True
        self.hist_lna = None; self.hist_D = None                              # frozen Delta history (ne, N, 3)
        self.gscale = 1.0                                                     # homotopy multiplier on every mass-sourced force
        self.a_start = 0.02                                                   # the growing-mode epoch (FP11's convention: a = 0.02)

    def set_history(self, lna_h, D):
        self.hist_lna = None if lna_h is None else np.asarray(lna_h); self.hist_D = None if D is None else np.asarray(D)

    def delta(self, l):
        if self.hist_lna is None:
            return 0.0
        h = self.hist_lna
        if l <= h[0]:
            return self.hist_D[0] * 0.0 if l < h[0] - 1e-12 else self.hist_D[0]
        j = int(min(np.searchsorted(h, l) - 1, len(h) - 2)); f = (l - h[j]) / (h[j + 1] - h[j]); f = min(max(f, 0.0), 1.0)
        return (1 - f) * self.hist_D[j] + f * self.hist_D[j + 1]

    def iso_prof(self, l):
        ne = len(self.lna); j = int(min(max(np.searchsorted(self.lna, l) - 1, 0), ne - 2))
        f = min(max((l - self.lna[j]) / (self.lna[j + 1] - self.lna[j]), 0.0), 1.0)
        return [(1 - f) * T[j] + f * T[j + 1] for T in self.iso]

    def accel(self, l, X):
        """X (S, N, 3) physical positions [m] -> accelerations (S, N, 3) [m/s^2] (without Delta)."""
        a = math.exp(l); S = X.shape[0]
        dX = X[:, None, :, :] - X[:, :, None, :]                                # (S, i, j, 3): x_j - x_i
        d = np.sqrt((dX ** 2).sum(-1)); np.fill_diagonal_ = None
        eye = np.eye(self.N, dtype=bool)
        dsafe = np.where(eye[None], 1.0, d)
        newt = G * self.m[None, None, :] / (dsafe ** 2 + self.soft ** 2) ** 1.5    # coefficient of dX
        coef = np.where(eye[None], 0.0, newt)
        if self.law.mond:
            profs = self.iso_prof(l)
            for j in range(self.N):
                col = np.maximum(dsafe[:, :, j], RG[0])
                mond = G * np.interp(np.log(col), self.lRG, profs[j]) / np.maximum(dsafe[:, :, j], 1e-30) ** 3
                mond = np.where(dsafe[:, :, j] < self.soft, mond * dsafe[:, :, j] / self.soft, mond)
                live_i = self.livemask[:, j][None, :]
                coef[:, :, j] += np.where(eye[None, :, j] | live_i, 0.0, mond)
            for (A0_, B0_) in self.live:
                for (A, B) in ((A0_, B0_), (B0_, A0_)):
                    dAB = d[:, A, B]
                    # A's MOND acceleration toward B (magnitude) from the exact two-body table; unit vector dX[:, A, B]/d
                    mA = interp_TM(self.TM[(A, B)], self.lna, self.ld, self.d0, l, dAB)
                    coef[:, A, B] += mA / np.maximum(dAB, 1e-30)
        acc = (coef[..., None] * dX).sum(axis=2)
        if self.gscale != 1.0:
            acc *= self.gscale
        acc += L_OL_H02 * X
        if self.conv == "B":
            acc -= 0.5 * LG_OM * LG_H0 ** 2 / a ** 3 * X
        return acc

    def integrate(self, Q, a_start=None, nstep=8000, store=False, extra=None):
        """Q (S, N, 3) comoving Lagrangian positions [m]: start on the Hubble flow at a_start; RK4 in ln a.  Returns X, V today
        (and the stored trajectory X(ln a) on the step grid if asked).  extra: optional callable (l, X) -> acceleration
        added (used by the test-particle integrator to share the step grid)."""
        a_start = self.a_start if a_start is None else a_start
        X = a_start * np.asarray(Q, float); V = H_of(a_start) * X
        lna = np.linspace(math.log(a_start), 0.0, nstep + 1); h = lna[1] - lna[0]
        traj = [X.copy()] if store else None; vtraj = [V.copy()] if store else None

        def f(l, X_, V_):
            H = H_of(math.exp(l)); ac = self.accel(l, X_) + self.gscale * self.delta(l)
            return V_ / H, ac / H
        for i in range(nstep):
            l = lna[i]
            k1x, k1v = f(l, X, V); k2x, k2v = f(l + h / 2, X + h * k1x / 2, V + h * k1v / 2)
            k3x, k3v = f(l + h / 2, X + h * k2x / 2, V + h * k2v / 2); k4x, k4v = f(l + h, X + h * k3x, V + h * k3v)
            X = X + h * (k1x + 2 * k2x + 2 * k3x + k4x) / 6; V = V + h * (k1v + 2 * k2v + 2 * k3v + k4v) / 6
            if store:
                traj.append(X.copy()); vtraj.append(V.copy())
        if store:
            return X, V, lna, np.array(traj), np.array(vtraj)
        return X, V


# ================================================================================================= the boundary-value problem
def solve_bvp(sysm, Xobs, Q0, nstep=4000, tol=1e-6 * MPC, maxit=30, J=None, hfd=1e-3 * MPC, verbose=False):
    """Peebles' numerical-action boundary conditions (positions today; the growing mode = zero peculiar velocity at a = 0.02),
    solved by Newton shooting on the comoving initial positions Q: finite-difference Jacobian, Broyden updates, backtracking
    line search on max|residual|; the Jacobian is recomputed when a step fails."""
    N = sysm.N; n = 3 * N; Q = np.array(Q0, float).copy(); Xobs = np.asarray(Xobs, float)
    nint = [0]

    def fdjac(Q):
        Qs = np.repeat(Q[None], n + 1, axis=0)
        for k in range(n):
            Qs[k + 1].reshape(-1)[k] += hfd
        X, V = sysm.integrate(Qs, nstep=nstep); nint[0] += n + 1
        Jm = (X[1:].reshape(n, n) - X[0].reshape(1, n)).T / hfd
        return X[0], V[0], Jm

    def one(Q):
        X, V = sysm.integrate(Q[None], nstep=nstep); nint[0] += 1
        return X[0], V[0]
    if J is None:
        X0, V0, J = fdjac(Q)
    else:
        X0, V0 = one(Q)
    R = (X0 - Xobs).ravel(); hist = [float(np.abs(R).max() / MPC)]; fresh = J is not None
    for it in range(maxit):
        if np.abs(R).max() < tol:
            break
        dQ = np.linalg.solve(J, -R); lam = 1.0; ok = False
        for _ in range(6):
            Qn = Q + lam * dQ.reshape(N, 3); Xn, Vn = one(Qn); Rn = (Xn - Xobs).ravel()
            if np.abs(Rn).max() < np.abs(R).max():
                ok = True; break
            lam *= 0.5
        if not ok:
            X0, V0, J = fdjac(Q); R = (X0 - Xobs).ravel(); hist.append(float(np.abs(R).max() / MPC))
            if len(hist) > 9 and hist[-1] > 0.5 * hist[-9]:
                break
            continue
        s_ = lam * dQ
        J = J + np.outer(Rn - R - J @ s_, s_) / (s_ @ s_)                     # Broyden
        Q, R, X0, V0 = Qn, Rn, Xn, Vn
        hist.append(float(np.abs(R).max() / MPC))
        if len(hist) > 9 and hist[-1] > 0.5 * hist[-9]:                        # stagnation: stop (reported by the caller)
            break
    if verbose:
        print("      bvp residual history [Mpc]:", ", ".join(f"{h:.1e}" for h in hist), f"({nint[0]} integrations)")
    return dict(Q=Q, X=X0, V=V0, J=J, res=float(np.abs(R).max() / MPC), nint=nint[0], it=len(hist) - 1)


def pair_seed(sysm, A, B, d_today_m, nstep=8000):
    """the two-body first-approach (k = 0) branch of the live pair (A, B) at today's separation, from FP11's own branch finder
    on the pair's exact force table: the initial PHYSICAL separation at a = 0.02 [m], or None."""
    TMr = (sysm.TM[(A, B)] + sysm.TM[(B, A)]) if (A, B) in sysm.TM else np.zeros((len(sysm.lna), len(DGRID)))   # Newton: no MOND part
    mA, mB = sysm.m[A], sysm.m[B]
    # rebuild an FP11 Acc object with this table (T = G M/d^2 + TM/d^2)
    T = G * (mA + mB) / DGRID[None, :] ** 2 + TMr / DGRID[None, :] ** 2
    acc = F11.Acc(DGRID, sysm.lna, T, mA + mB, soft=sysm.soft)
    a_s = sysm.a_start
    br = [b for b in F11.branches(acc, D0=d_today_m, bg=(sysm.conv == "B"), nstep=nstep, a_start=a_s, lo=0.05 * a_s / 0.02,
                                  hi=600.0 * a_s / 0.02) if b["k"] == 0 and b["vr"] < 0]
    return (br[0]["ri_kpc"] * KPC, br[0]) if br else (None, None)


# ================================================================================================= the field history
def traj_at(lna_s, T, l):
    """linear interpolation of a stored trajectory T (nsteps+1, ...) on the step grid lna_s at ln a = l."""
    j = int(min(max(np.searchsorted(lna_s, l) - 1, 0), len(lna_s) - 2)); f = (l - lna_s[j]) / (lna_s[j + 1] - lna_s[j])
    return (1 - f) * T[j] + f * T[j + 1]


def body_delta_history(sysm, lna_s, Xs, lna_h, dres=(120, 48, 48)):
    """Delta_i(ln a) = the interaction field P(1 - S_L)W of ALL bodies at body i (direct 3-D integral of the band-passed dipole
    kernel) minus the interaction of each live pair at its actual separation (FP11's dg_body): the part the live tables miss."""
    law = sysm.law; N = sysm.N; D = np.zeros((len(lna_h), N, 3))
    if not law.mond:
        return D
    for e, l in enumerate(lna_h):
        X = traj_at(lna_s, Xs, l); a = math.exp(l); L = law.L(a); yt = law.yth(a)
        bodies = [(sysm.m[i], X[i]) for i in range(N)]
        for i in range(N):
            g = direct_W_at(bodies, i, law.a0, L, yt, ns=dres[0], nmu=dres[1], nphi=dres[2])
            for (A0_, B0_) in sysm.live:
                for (A, B) in ((A0_, B0_), (B0_, A0_)):
                    if A != i:
                        continue
                    dv = X[B] - X[A]; d = float(np.linalg.norm(dv))
                    g = g - (-F11.dg_body(sysm.m[A], sysm.m[B], d, law.a0, L, yt)) * dv / d
            D[e, i] = g
    return D


def solve_bodies(sysm, Xobs, Q0, lna_h, nstep=4000, maxpicard=6, tolv=0.05e3, verbose=False, dres=(120, 48, 48), J=None):
    """the Picard iteration: solve the BVP with the frozen Delta history, recompute the history along the new orbits, repeat
    until every body's predicted velocity moves by < tolv."""
    sysm.set_history(None, None); Q = np.array(Q0, float); Vprev = None; log = []
    for it in range(maxpicard):
        sol = solve_bvp(sysm, Xobs, Q, nstep=nstep, J=J, verbose=verbose); Q, J = sol["Q"], sol["J"]
        X, V, lna_s, Xs, Vs = sysm.integrate(Q[None], nstep=nstep, store=True)
        dv = None if Vprev is None else float(np.abs(V[0] - Vprev).max())
        log.append(dict(it=it, res=sol["res"], nint=sol["nint"], dv_kms=None if dv is None else dv / 1e3))
        if verbose:
            print(f"    picard {it}: BVP residual {sol['res']:.1e} Mpc, {sol['nint']} integrations, max dv {('%.3f' % (dv / 1e3)) if dv is not None else '-'} km/s")
        if dv is not None and dv < tolv:
            break
        Vprev = V[0].copy()
        if not sysm.law.mond:
            break
        D = body_delta_history(sysm, lna_s, Xs[:, 0], lna_h, dres=dres); sysm.set_history(lna_h, D)
    return dict(Q=Q, X=X[0], V=V[0], lna_s=lna_s, Xs=Xs[:, 0], Vs=Vs[:, 0], J=J, log=log, sol=sol)


# ================================================================================================= the test particles
def grid_tables(sysm, lna_s, Xs, lna_g, grid, rot, lg=(0, 1)):
    """the interaction field P(1 - S_L)W of all bodies on the 3-D grid (centred on the LG barycentre, axes rot) at the
    epochs lna_g, from the converged body trajectory."""
    law = sysm.law; F = np.zeros((len(lna_g), grid.nr, grid.nth, grid.nph, 3), np.float32); C = np.zeros((len(lna_g), 3))
    lg = list(lg)
    for e, l in enumerate(lna_g):
        X = traj_at(lna_s, Xs, l); a = math.exp(l); L = law.L(a); yt = law.yth(a)
        c = (sysm.m[lg, None] * X[lg]).sum(0) / sysm.m[lg].sum(); C[e] = c
        if not law.mond:
            continue
        bodies = [(sysm.m[i], X[i]) for i in range(sysm.N)]
        q = grid.divergence(lambda P: W_field(P, bodies, law.a0, L, yt), c, rot)
        F[e] = grid.field(q, L)
    return F, C


class Tracers:
    """test particles in the bodies' field: softened Newton + isolated phantoms (live, FP11's PairField rule) + the tabulated
    interaction field (trilinear on the 3-D grid, linear in ln a between epochs; zero before the first epoch)."""
    def __init__(self, sysm, grid, rot, lna_g, F, C):
        self.s = sysm; self.g = grid; self.rot = rot; self.lna_g = np.asarray(lna_g); self.F = F; self.C = C

    def accel(self, l, Xb, Y):
        s = self.s; acc = np.zeros_like(Y); a = math.exp(l)
        profs = s.iso_prof(l) if s.law.mond else None
        for j in range(s.N):
            d = Y - Xb[j]; r = np.sqrt((d * d).sum(-1))
            newt = G * s.m[j] / (r * r + s.soft * s.soft) ** 1.5
            if s.law.mond:
                mond = G * np.interp(np.log(np.maximum(r, RG[0])), s.lRG, profs[j]) / np.maximum(r, 1e-30) ** 3
                mond = np.where(r < s.soft, mond * r / s.soft, mond)
                newt = newt + mond
            acc -= newt[:, None] * d
        if s.law.mond and self.F is not None:
            h = self.lna_g
            if l >= h[0]:
                j = int(min(max(np.searchsorted(h, l) - 1, 0), len(h) - 2)); f = min(max((l - h[j]) / (h[j + 1] - h[j]), 0.0), 1.0)
                g0 = self.g.interp(self.F[j], (Y - self.C[j]) @ self.rot); g1 = self.g.interp(self.F[j + 1], (Y - self.C[j + 1]) @ self.rot)
                acc += ((1 - f) * g0 + f * g1) @ self.rot.T
        acc += L_OL_H02 * Y
        if s.conv == "B":
            acc -= 0.5 * LG_OM * LG_H0 ** 2 / a ** 3 * Y
        return acc

    def run(self, Qb, Qt, a_start=None, nstep=3000):
        """bodies (their converged Q) and tracers (comoving Lagrangian positions Qt (P, 3)) integrated together from the Hubble
        flow at a_start; returns bodies' X, V and tracers' Y, U today."""
        s = self.s; a_start = s.a_start if a_start is None else a_start
        X = a_start * np.asarray(Qb, float); V = H_of(a_start) * X
        Y = a_start * np.asarray(Qt, float); U_ = H_of(a_start) * Y
        lna = np.linspace(math.log(a_start), 0.0, nstep + 1); hh = lna[1] - lna[0]

        def f(l, X_, V_, Y_, U2):
            H = H_of(math.exp(l)); ab = s.accel(l, X_[None])[0] + s.delta(l); at = self.accel(l, X_, Y_)
            return V_ / H, ab / H, U2 / H, at / H
        for i in range(nstep):
            l = lna[i]
            k1 = f(l, X, V, Y, U_)
            k2 = f(l + hh / 2, X + hh * k1[0] / 2, V + hh * k1[1] / 2, Y + hh * k1[2] / 2, U_ + hh * k1[3] / 2)
            k3 = f(l + hh / 2, X + hh * k2[0] / 2, V + hh * k2[1] / 2, Y + hh * k2[2] / 2, U_ + hh * k2[3] / 2)
            k4 = f(l + hh, X + hh * k3[0], V + hh * k3[1], Y + hh * k3[2], U_ + hh * k3[3])
            X = X + hh * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6; V = V + hh * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
            Y = Y + hh * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) / 6; U_ = U_ + hh * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]) / 6
        return X, V, Y, U_


def lg_frame(M, X, V, lg=(0, 1)):
    lg = list(lg); w = M[lg] / M[lg].sum()
    return (w[:, None] * X[lg]).sum(0), (w[:, None] * V[lg]).sum(0)


def R0_rays_3d(tr, Qb, M, dirs, rho_lo=0.1 * MPC, rho_hi=4.0 * MPC, n0=40, npass=6, nins=8, rpair=0.6, nstep=3000, lg=(0, 1)):
    """FP11's R0_rays in 3-D: tracers on rays from the LG's Lagrangian barycentre; today's LG-centric radius and radial velocity
    (relative to the LG barycentre); adaptive insertion; the outermost - -> + crossing of v_r beyond rpair [Mpc] with a
    continuous bracket.  dirs: (nd, 3) unit vectors.  Returns R0 per direction [Mpc] and every tracer."""
    lg = list(lg); qc = (M[lg, None] * Qb[lg]).sum(0) / M[lg].sum(); nd = len(dirs)
    RHO = np.geomspace(rho_lo, rho_hi, n0)
    data = [dict(rho=RHO.copy(), R=None, v=None, Y=None, U=None) for _ in range(nd)]

    def evaluate(dir_idx, rhos):
        Qt = qc[None, :] + rhos[:, None] * dirs[dir_idx]
        X, V, Y, U_ = tr.run(Qb, Qt, nstep=nstep)
        c, vc = lg_frame(M, X, V, lg); d = Y - c; R = np.sqrt((d * d).sum(-1)); vr = ((U_ - vc) * d).sum(-1) / np.maximum(R, 1e-30)
        return R, vr, Y, U_, X, V
    R, vr, Y, U_, Xb, Vb = evaluate(np.repeat(np.arange(nd), n0), np.tile(RHO, nd))
    for k in range(nd):
        s_ = slice(k * n0, (k + 1) * n0); data[k].update(R=R[s_], v=vr[s_], Y=Y[s_], U=U_[s_])
    for _ in range(npass):
        own, rr = [], []
        for k in range(nd):
            dk = data[k]; o = np.argsort(dk["rho"]); rh, R_, v_ = dk["rho"][o], dk["R"][o], dk["v"][o]
            for j in range(len(rh) - 1):
                if max(R_[j], R_[j + 1]) > 0.2 * MPC and (R_[j + 1] / max(R_[j], 1e-30) > 1.25 or R_[j] / max(R_[j + 1], 1e-30) > 1.25
                                                         or ((v_[j] < 0 < v_[j + 1]) and abs(R_[j + 1] / R_[j] - 1) >= 0.05)):
                    ins = np.geomspace(rh[j], rh[j + 1], nins + 2)[1:-1]; own += [k] * nins; rr += list(ins)
        if not rr:
            break
        own, rr = np.array(own), np.array(rr)
        R, vr, Y, U_, _, _ = evaluate(own, rr)
        for k in range(nd):
            s_ = own == k
            if s_.any():
                for key, val in (("rho", rr[s_]), ("R", R[s_]), ("v", vr[s_]), ("Y", Y[s_]), ("U", U_[s_])):
                    data[k][key] = np.concatenate([data[k][key], val])
    R0 = np.full(nd, np.nan)
    for k in range(nd):
        dk = data[k]; o = np.argsort(dk["rho"]); R_, v_ = dk["R"][o], dk["v"][o]
        idx_ = [j for j in range(len(R_) - 1) if v_[j] < 0 < v_[j + 1] and R_[j + 1] > rpair * MPC and abs(R_[j + 1] / R_[j] - 1) < 0.05]
        if idx_:
            j = idx_[-1]; fr_ = -v_[j] / (v_[j + 1] - v_[j]); R0[k] = (R_[j] + fr_ * (R_[j + 1] - R_[j])) / MPC
    return R0, data, (Xb, Vb)


def fib_dirs(n):
    i = np.arange(n) + 0.5; phi = math.pi * (1 + 5 ** 0.5) * i; z = 1 - 2 * i / n; r = np.sqrt(1 - z * z)
    return np.stack([r * np.cos(phi), r * np.sin(phi), z], axis=1)


def nam_tracers(tr, Qb, M, Xobs_t, seeds_q, nstep=3000, tol=1e-4 * MPC, maxit=12, hfd=2e-3 * MPC, lg=(0, 1, 2), maxstep=0.6 * MPC):
    """Newton shooting for test particles: for each target position (today) and each seed Lagrangian position, find q with
    y(q) = x_target.  seeds_q: list over targets of arrays (k, 3).  Batched: every candidate and its 3 finite-difference
    partners in one joint integration per iteration.  Returns per target the list of converged solutions (q, y, v, dv/dx)."""
    cand = [(t, np.array(q, float)) for t, qs in enumerate(seeds_q) for q in qs]
    if not cand:
        return [[] for _ in seeds_q], None
    T_ = np.array([c[0] for c in cand]); Qc = np.array([c[1] for c in cand]); nc = len(cand)
    alive = np.ones(nc, bool); conv = np.zeros(nc, bool); resn = np.full(nc, np.inf)
    last = None
    for it in range(maxit):
        idx_ = np.where(alive & ~conv)[0]
        if len(idx_) == 0:
            break
        Qs = np.concatenate([Qc[idx_]] + [Qc[idx_] + hfd * np.eye(3)[k][None, :] for k in range(3)])
        X, V, Y, U_ = tr.run(Qb, Qs, nstep=nstep)
        n_ = len(idx_); Y0, U0 = Y[:n_], U_[:n_]
        Jc = np.stack([(Y[(k + 1) * n_:(k + 2) * n_] - Y0) / hfd for k in range(3)], axis=-1)       # (n, 3, 3): dY/dq
        Jv = np.stack([(U_[(k + 1) * n_:(k + 2) * n_] - U0) / hfd for k in range(3)], axis=-1)      # dU/dq
        R = Y0 - Xobs_t[T_[idx_]]; rn = np.sqrt((R * R).sum(-1))
        for m_, i in enumerate(idx_):
            resn[i] = rn[m_]
            if rn[m_] < tol:
                conv[i] = True
                try:
                    dvdx = Jv[m_] @ np.linalg.inv(Jc[m_])
                except np.linalg.LinAlgError:
                    dvdx = np.full((3, 3), np.nan)
                cand[i] = cand[i] + (Y0[m_].copy(), U0[m_].copy(), dvdx) if len(cand[i]) == 2 else (cand[i][0], cand[i][1], Y0[m_].copy(), U0[m_].copy(), dvdx)
                continue
            try:
                dq = -np.linalg.solve(Jc[m_], R[m_])
            except np.linalg.LinAlgError:
                alive[i] = False; continue
            nq = np.linalg.norm(dq)
            if nq > maxstep:
                dq *= maxstep / nq
            Qc[i] = Qc[i] + dq
        last = (X, V)
    # the final converged set, deduplicated per target by Lagrangian position (10 kpc comoving)
    out = [[] for _ in seeds_q]
    for i in np.where(conv)[0]:
        t = T_[i]; q = Qc[i]; y, u, dvdx = cand[i][2], cand[i][3], cand[i][4]
        if all(np.linalg.norm(q - s["q"]) > 0.01 * MPC for s in out[t]):
            out[t].append(dict(q=q.copy(), y=y, u=u, dvdx=dvdx))
    return out, last


def free_beta(conv, a_start=0.02, nstep=4000):
    """a free particle's expansion today relative to comoving (x = beta a q) under the convention: A (point masses + Lambda:
    no background matter, the region coasts) or B (the smooth background decelerates it: beta = 1)."""
    s = System([1e-30 * MSUN], Law("NEWTON", "canonical"), conv=conv)
    X, V = s.integrate(np.array([[[1.0 * MPC, 0, 0]]]), a_start=a_start, nstep=nstep)
    return float(X[0, 0, 0] / MPC)


def seed_bodies(sysm, Xobs, pair=(0, 1), sat=(), host=1):
    """initial guesses: every body on its free expansion (Q = X/beta); the MW-M31 pair's separation from FP11's two-body
    first-approach branch about its own free-expansion barycentre; satellites (M33) at their host's seed + offset/beta."""
    beta = free_beta(sysm.conv, a_start=sysm.a_start); Q0 = Xobs / beta
    A, B = pair; M = sysm.m
    d0 = float(np.linalg.norm(Xobs[B] - Xobs[A])); ri, br = pair_seed(sysm, A, B, d0)
    if ri is not None:
        c = (M[A] * Xobs[A] + M[B] * Xobs[B]) / (M[A] + M[B]) / beta; u = (Xobs[B] - Xobs[A]) / d0
        Q0[A] = c - M[B] / (M[A] + M[B]) * (ri / sysm.a_start) * u; Q0[B] = c + M[A] / (M[A] + M[B]) * (ri / sysm.a_start) * u
    for s_ in sat:
        Q0[s_] = Q0[host] + (Xobs[s_] - Xobs[host]) / beta
    return Q0, br, beta


def homotopy_bodies(sysm, Xobs, Q0, mus=(0.0, 0.05, 0.12, 0.25, 0.4, 0.55, 0.7, 0.85, 1.0), nstep=4000, verbose=False):
    """continuation in the gravity strength: at mu = 0 every body coasts (Q = X/beta exactly); the first-approach solution is
    tracked to mu = 1 (Broyden with the previous Jacobian; a fresh finite-difference Jacobian where a step fails)."""
    Q = np.array(Q0, float); J = None; log = []
    for mu in mus:
        sysm.gscale = mu
        sol = solve_bvp(sysm, Xobs, Q, nstep=nstep, J=J, verbose=verbose)
        if sol["res"] > 1e-4:                                                  # retry from scratch at this mu
            sol = solve_bvp(sysm, Xobs, Q, nstep=nstep, J=None, verbose=verbose)
        Q, J = sol["Q"], sol["J"]; log.append((mu, sol["res"], sol["nint"]))
    sysm.gscale = 1.0
    return Q, J, log

# ============================================================================================================== part: data
import os, sys, io, math, contextlib

with contextlib.redirect_stdout(io.StringIO()):
    import FP12_local_volume_groups_r0 as F12                                   # noqa: E402 (main() not run)
HL = F11.HL

# ---- frames: vdM+2012's solar parameters (R0 = 8.29 kpc, V0 = 239 km/s, (U, V, W)pec = (11.1, 12.24, 7.25) km/s)
R_SUN = 8.29 * KPC
V_SUN_GAL = np.array([11.1, 12.24 + 239.0, 7.25]) * 1e3                           # Galactic Cartesian (toward GC, rotation, NGP)
T_ICRS2GAL = np.array([[-0.0548755604, -0.8734370902, -0.4838350155],
                       [+0.4941094279, -0.4448296300, +0.7469822445],
                       [-0.8676661490, -0.1980763734, +0.4559837762]])
V_SUN_EQ = T_ICRS2GAL.T @ V_SUN_GAL


def unit(ra, de):
    ra, de = np.radians(ra), np.radians(de)
    return np.stack([np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)], axis=-1)


rows = HL.vizier_tsv("ungc_karachentsev2013.tsv")
U = dict(name=np.array([r_["Name"].strip() for r_ in rows]), MD=np.array([r_["MD"].strip() for r_ in rows]),
         ra=np.array([HL._f(r_["_RAJ2000"]) for r_ in rows]), de=np.array([HL._f(r_["_DEJ2000"]) for r_ in rows]),
         D=np.array([HL._f(r_["Dist"]) for r_ in rows]), Vh=np.array([HL._f(r_["HRV"]) for r_ in rows]),
         Vlg=np.array([HL._f(r_["Vlg"]) for r_ in rows]), fD=np.array([r_["f_Dist"].strip() for r_ in rows]),
         Ti=np.array([HL._f(r_["Ti1"]) for r_ in rows]), lK=np.array([HL._f(r_["KLum"]) for r_ in rows]),
         lH=np.array([HL._f(r_["MHI"]) for r_ in rows]))
U["n"] = unit(U["ra"], U["de"])


def idx(name):
    return int(np.where(U["name"] == name)[0][0])


N_GC = U["n"][idx("Milky Way")]                                                   # the UNGC's Milky Way entry = Sgr A* direction
X_GC_HELIO = R_SUN * N_GC                                                        # GC position, heliocentric equatorial [m]


def pos_gc(i, D_mpc=None):
    """heliocentric -> Galactocentric-origin equatorial position [m]."""
    D = U["D"][i] if D_mpc is None else D_mpc
    return D * MPC * U["n"][i] - X_GC_HELIO


def vgsr(i):
    return (U["Vh"][i] * 1e3 + V_SUN_EQ @ U["n"][i])                              # [m/s]


# ---- the bodies
MW_STARS, M31_STARS, M33_STARS = 6.08e10, 10.3e10, 4.8e9                        # Licquia & Newman 2015; Sick+2015; Corbelli+2014
GAS = lambda nm: 1.33 * 10 ** U["lH"][idx(nm)]


def k02_mass(anchor, rcut, ups=0.6):
    i_c = F12.uidx(anchor); R, Vr, ok = F12.group_frame(i_c); ms, mg = F12.baryons(R, ok, rcut, i_c, anchor, ups); return ms + mg


def body_list(verbose=False, merge_m33=True):
    """(name, anchor, M_b [Msun], position [m], v_GSR obs [m/s] or None, kind)"""
    B = []
    # the Local Group: M31's heliocentric distance scaled so that the MW-M31 separation is FP11's 0.78 Mpc
    i31 = idx("MESSIER031"); n31 = U["n"][i31]
    # solve |D n31 - X_GC| = 0.78 Mpc for D
    b_ = n31 @ X_GC_HELIO; c_ = X_GC_HELIO @ X_GC_HELIO - (0.78 * MPC) ** 2; D31 = b_ + math.sqrt(b_ * b_ - c_)
    B.append(("MW", "Milky Way", MW_STARS + GAS("Milky Way"), np.zeros(3), 0.0, "LG"))
    B.append(("M31", "MESSIER031", M31_STARS + GAS("MESSIER031"), D31 * n31 - X_GC_HELIO, vgsr(i31), "LG"))
    if merge_m33:                                                             # M33 (a satellite 0.2 Mpc from M31) merged into M31
        n_, m_, x_, v_, k_ = B[1][0], B[1][2], B[1][3], B[1][4], B[1][5]
        B[1] = ("M31+M33", "MESSIER031", m_ + M33_STARS + GAS("MESSIER033"), x_, v_, k_)
    else:
        i33 = idx("MESSIER033")
        B.append(("M33", "MESSIER033", M33_STARS + GAS("MESSIER033"), pos_gc(i33), vgsr(i33), "LG"))
    for nm, anchor, key in (("M81 group", "MESSIER081", "M81"), ("Cen A group", "NGC5128", "CenA"), ("M83 group", "NGC5236", "M83"),
                            ("IC 342 group", "IC0342", "IC342")):
        R0k = F12.K02_OUT[key][0]
        m = k02_mass(anchor, R0k)
        i = idx(anchor); B.append((nm, anchor, m, pos_gc(i), vgsr(i), "nb"))
    for nm, anchor in (("NGC 253 group", "NGC0253"), ("NGC 4736 group", "NGC4736"), ("NGC 4826 group", "NGC4826"), ("Circinus", "CIRCINUS")):
        m = k02_mass(anchor, 0.7)
        i = idx(anchor); B.append((nm, anchor, m, pos_gc(i), vgsr(i), "nb"))
    return B


# ---- the flow sample: FP11's section-D selection (UNGC, barycentre at 0.63 of the way to M31, accurate distances,
#      0.7 < R < 3 Mpc, other groups' members excluded)
def flow_sample(f31=0.63, lo=0.7, hi=3.0):
    dd = F11.ungc_hubble(f31)
    sel = np.isfinite(dd["R"]) & np.isfinite(dd["Vr"]) & (dd["R"] > lo) & (dd["R"] < hi) & np.isin(dd["fD"], F11.ACC_DIST) \
        & ~(np.isin(dd["MD"], F11.OTHER_GROUPS) & (dd["Ti"] > 0))
    names = list(dd["name"][sel])
    out = []
    for nm in names:
        i = idx(nm)
        out.append(dict(name=nm, i=i, D=U["D"][i], x=pos_gc(i), vgsr=vgsr(i), n=U["n"][i], Vlg=U["Vlg"][i], fD=U["fD"][i]))
    return out, dd, sel

# ============================================================================================================== part: run
import os, sys, time, math, json


SIG_TH, SIG_OBS, SIG_DREL, H_REF = 25e3, 5e3, 0.05, 70.0 * 1e3 / MPC          # km/s-level choices (stated)
VR_LG, EVR_LG = -109.3e3, 4.4e3


def build(cfg):
    """cfg: dict(law, foot, s_lg, nb (bool), nb_scale, conv, f_halo (LCDM: mass multiplier), live)"""
    law = Law(cfg["law"], cfg["foot"])
    B = body_list()
    if not cfg.get("nb", True):
        B = [b for b in B if b[5] == "LG"]                                   # the pair alone (the same machinery)
    names = [b[0] for b in B]; M = np.array([b[2] for b in B]) * MSUN
    M[:2] *= cfg.get("s_lg", 1.0)
    if len(M) > 2:
        M[2:] *= cfg.get("nb_scale", 1.0)
    if cfg["law"] == "NEWTON":
        M[:2] *= cfg.get("f_lg", 1.0); M[2:] *= cfg.get("f_nb", 1.0)
    X = np.array([b[3] for b in B]); cm = (M[:, None] * X).sum(0) / M.sum(); Xobs = X - cm
    return law, B, names, M, Xobs, cm


def run_config(cfg, do_tracers=True, verbose=False, nstep_b=4000, nstep_t=3000, grid_kw=None, lna_g=None):
    t_start = time.time(); out = dict(cfg=cfg)
    law, B, names, M, Xobs, cm = build(cfg)
    live = [(0, 1)] if law.mond else []
    sysm = System(M, law, live_pairs=live, conv=cfg.get("conv", "B")); sysm.a_start = cfg.get("a_start", 0.02)
    Q0, br0, beta = seed_bodies(sysm, Xobs)                                  # the pair on its two-body first-approach branch
    sol0 = solve_bvp(sysm, Xobs, Q0, nstep=nstep_b, maxit=40, verbose=verbose); Q, J = sol0["Q"], sol0["J"]
    out["bvp_res_Mpc"] = sol0["res"]
    if sol0["res"] > 1e-4 and cfg.get("allow_homotopy", True):              # fall back on continuation in the gravity strength
        Q, J, hl = homotopy_bodies(sysm, Xobs, Xobs / beta, nstep=nstep_b, verbose=verbose); out["homotopy"] = hl
    elif sol0["res"] > 1e-3:                                                 # not converged and no fallback allowed: report, stop
        out["not_converged"] = True; return out
    out["seed_pair"] = br0
    zmax_h = cfg.get("zmax_hist", 3.0 if law.kind in ("HS", "HY") else 49.0)
    lna_h = LNAT[LNAT >= math.log(1.0 / (1.0 + zmax_h)) - 1e-9]
    res = solve_bodies(sysm, Xobs, Q, lna_h, nstep=nstep_b, maxpicard=8, verbose=verbose, J=J)
    out["picard"] = res["log"]
    Xf, Vf, Qb = res["X"], res["V"], res["Q"]
    dx = Xf[1] - Xf[0]; dv = Vf[1] - Vf[0]; d = float(np.linalg.norm(dx)); vr = float(dx @ dv / d)
    vt = float(np.linalg.norm(dv - vr * dx / d))
    # the MW-M31 orbit: separation history, extrema, pericentres
    sep = np.linalg.norm(res["Xs"][:, 1] - res["Xs"][:, 0], axis=1); lna_s = res["lna_s"]
    imax = int(np.argmax(sep)); mins = [i for i in range(1, len(sep) - 1) if sep[i] < sep[i - 1] and sep[i] < sep[i + 1]]
    out["pair"] = dict(vr=vr / 1e3, vt=vt / 1e3, d=d / MPC, dmax=float(sep[imax] / MPC), z_dmax=float(math.exp(-lna_s[imax]) - 1),
                       t_dmax_lookback=float((F11.T0_AGE - F11.t_of_a(math.exp(lna_s[imax]))) / GYR),
                       peri=[(float(math.exp(-lna_s[i]) - 1), float(sep[i] / KPC)) for i in mins], d_ai_kpc=float(sep[0] / KPC),
                       Qrel=float(np.linalg.norm(Qb[1] - Qb[0]) / MPC))
    # every body's predicted Galactocentric velocity (relative to the MW, along the observed line of sight)
    bv = []
    for i in range(len(M)):
        if i == 0:
            bv.append(None); continue
        n_ = B[i][3] + X_GC_HELIO; n_ = n_ / np.linalg.norm(n_)                 # the heliocentric line of sight
        bv.append(dict(name=names[i], pred=float((Vf[i] - Vf[0]) @ n_ / 1e3), obs=(None if B[i][4] is None else float(B[i][4] / 1e3)),
                       displacement_Mpc=float(np.linalg.norm(Qb[i] * beta - Xobs[i]) / MPC)))
    out["bodies"] = bv
    out["t_bodies"] = time.time() - t_start
    if verbose:
        print(f"  [{cfg.get('tag', '')}] bodies: v_r {vr/1e3:.3f} v_t {vt/1e3:.2f} km/s; d_max {out['pair']['dmax']:.3f} Mpc at z {out['pair']['z_dmax']:.2f}; "
              f"{out['t_bodies']:.0f}s", flush=True)
    if not do_tracers:
        return out
    # ---- the grid tables (the interaction field for the test particles)
    t1 = time.time()
    gk = dict(rmin_kpc=2.0, rmax_kpc=40000.0, nr=180, nth=64, nph=96, lmax=40); gk.update(grid_kw or {})
    grid = Grid3(**gk); rot = rot_to(Xobs[1] - Xobs[0])
    if lna_g is None:
        lna_g = LNAT if law.kind not in ("HS",) else LNAT[LNAT >= math.log(1.0 / (1.0 + cfg.get("zmax_grid", 49.0))) - 1e-9]
    F, C = grid_tables(sysm, res["lna_s"], res["Xs"], lna_g, grid, rot) if law.mond else (None, None)
    tr = Tracers(sysm, grid, rot, lna_g, F, C)
    out["t_grid"] = time.time() - t1
    # ---- R0 rays (8 GL in cos theta about the MW->M31 axis x 8 in phi)
    t1 = time.time()
    cs, ws = np.polynomial.legendre.leggauss(8); th = np.arccos(cs); nphi = cfg.get("nphi_rays", 8)
    ph = (np.arange(nphi) + 0.5) * 2 * math.pi / nphi
    dirs = np.array([[math.sin(t) * math.cos(p), math.sin(t) * math.sin(p), math.cos(t)] for t in th for p in ph]) @ rot.T
    R0, data, _ = R0_rays_3d(tr, Qb, M, dirs, n0=40, nins=8, nstep=nstep_t,
                             rho_hi=(4.0 if sysm.conv == "A" and sysm.a_start <= 0.02 else 12.5) * MPC)   # FP11: 80 / 250 kpc at a = 0.02
    R0m = R0.reshape(8, nphi); ok = np.isfinite(R0m)
    per_th = np.array([np.nanmean(R0m[k]) if ok[k].any() else np.nan for k in range(8)])
    wt = ws[:, None] * np.ones(nphi)[None, :] / nphi
    mean = float(np.nansum(wt * np.nan_to_num(R0m)) / np.sum(wt * ok))
    val = (np.abs(cs) <= 0.9)[:, None] & ok
    mean_val = float(np.sum(wt * np.nan_to_num(R0m) * val) / np.sum(wt * val))
    out["R0"] = dict(mean=mean, mean_valid=mean_val, per_theta=per_th.tolist(), per_dir=R0.tolist(), cos=cs.tolist(), n_ok=int(ok.sum()),
                     spread_phi=float(np.nanmax(np.nanstd(R0m, axis=1))), min=float(np.nanmin(R0)), max=float(np.nanmax(R0)))
    out["t_rays"] = time.time() - t1
    if verbose:
        print(f"  [{cfg.get('tag', '')}] R0 mean {mean:.4f} (|cos|<=0.9: {mean_val:.4f}); per theta {np.round(per_th, 3)}; {out['t_rays']:.0f}s", flush=True)
    # ---- the dwarfs: the numerical action for each observed galaxy (Newton shooting from Lagrangian seeds)
    t1 = time.time()
    fs, dd, sel = flow_sample()
    Xt = np.array([g["x"] for g in fs]) - cm
    # the Lagrangian sample: every ray tracer + a Fibonacci sample around the LG's Lagrangian barycentre
    qc = (M[:2, None] * Qb[:2]).sum(0) / M[:2].sum()
    Ys, Qs_ = [], []
    lgdir = [dirs[k] for k in range(len(dirs))]
    for k in range(len(dirs)):
        Ys.append(data[k]["Y"]); Qs_.append(qc[None, :] + data[k]["rho"][:, None] * dirs[k][None, :])
    fd = fib_dirs(cfg.get("nfib", 300)); rho = np.geomspace(0.05, 7.0 / beta, 24) * MPC
    Qf = (qc[None, None, :] + rho[None, :, None] * fd[:, None, :]).reshape(-1, 3)
    _, _, Yf, Uf = tr.run(Qb, Qf, nstep=nstep_t)
    Ys.append(Yf); Qs_.append(Qf)
    Ys = np.concatenate(Ys); Qs_ = np.concatenate(Qs_)
    seeds = []
    for t in range(len(fs)):
        dist = np.linalg.norm(Ys - Xt[t], axis=1); o = np.argsort(dist)
        chosen = []
        for j in o[:400]:
            if dist[j] > 0.6 * MPC and chosen:
                break
            if all(np.linalg.norm(Qs_[j] - Qs_[c]) > 0.08 * MPC for c in chosen):
                chosen.append(j)
            if len(chosen) >= 4:
                break
        seeds.append(Qs_[chosen])
    sols, last = nam_tracers(tr, Qb, M, Xt, seeds, nstep=nstep_t)
    # frames: the model's MW and LG barycentre today
    V_MW = Vf[0]; cLG, vLG = lg_frame(M, Xf, Vf)
    rows = []
    for t, g in enumerate(fs):
        n_ = g["n"]; vobs = g["vgsr"]
        cand = []
        for s_ in sols[t]:
            vg = float((s_["u"] - V_MW) @ n_)
            dvdD = float(n_ @ s_["dvdx"] @ n_) if np.all(np.isfinite(s_["dvdx"])) else float("nan")
            cand.append(dict(vgsr=vg / 1e3, dvdD=dvdD * MPC / 1e3, q=(s_["q"] - qc).tolist()))
        best = min(cand, key=lambda c_: abs(c_["vgsr"] - vobs / 1e3)) if cand else None
        rows.append(dict(name=g["name"], D=g["D"], vobs=vobs / 1e3, n_sol=len(cand), sols=cand, best=best,
                         vlg_shift=float((V_MW - vLG) @ n_ / 1e3)))
    out["dwarfs"] = rows
    out["t_dwarfs"] = time.time() - t1
    out["t_total"] = time.time() - t_start
    if verbose:
        nsol = [r["n_sol"] for r in rows]
        print(f"  [{cfg.get('tag', '')}] dwarfs: solved {sum(1 for n in nsol if n > 0)}/{len(nsol)}, multi {sum(1 for n in nsol if n > 1)}; "
              f"{out['t_dwarfs']:.0f}s; total {out['t_total']:.0f}s", flush=True)
    return out


def chi2_flow(out, sig_th=SIG_TH, dist_term="ref"):
    """the flow chi^2 over the dwarfs (best branch per galaxy) and the MW-M31 timing term."""
    c2, n, res = 0.0, 0, []
    for r in out["dwarfs"]:
        if r["best"] is None:
            continue
        dv = (r["best"]["vgsr"] - r["vobs"]) * 1e3
        if dist_term == "ref":
            sD = H_REF * SIG_DREL * r["D"] * MPC
        else:
            sD = abs(r["best"]["dvdD"]) * 1e3 / MPC * SIG_DREL * r["D"] * MPC if np.isfinite(r["best"]["dvdD"]) else H_REF * SIG_DREL * r["D"] * MPC
        s2 = sig_th ** 2 + SIG_OBS ** 2 + sD ** 2
        c2 += dv * dv / s2; n += 1; res.append(dv / 1e3)
    ct = ((out["pair"]["vr"] * 1e3 - VR_LG) / EVR_LG) ** 2
    res = np.array(res)
    return dict(chi2_flow=c2, n=n, chi2_timing=ct, mean_res=float(res.mean()) if n else float("nan"),
                rms_res=float(np.sqrt((res ** 2).mean())) if n else float("nan"))
