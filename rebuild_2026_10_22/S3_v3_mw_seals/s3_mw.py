"""S3_v3_mw_seals: the Milky Way under v3 (shared by Part A and Part C).  Criteria FROZEN_CRITERIA.md (8f6c6587e1, A1, A2).

McMillan 2017 (Table 3) baryons transcribed from CFG514's formulae (checked identical to CFG514/516's functions in Part A);
B2 / B2b / B3 transcribed from CFG516.  Axisymmetric AQUAL solves (isolated; EFE along the disc axis) and the 3-D FFT ratio
for the record's external field at gamma = 57 deg.  Units kpc, km/s, Msun.  Cached in _cache/ (not committed).
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os
import json
import math
import hashlib
import numpy as np
import s3_aqual as S

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = S.CACHE
G = S.G
R0 = 8.122                                    # model frame (CFG514/516/553)
MSTAR_CENSUS, MSTAR_ERR = 5.43e10, 0.57e10
SM, SP = 1 - 0.57 / 5.43, 1 + 0.57 / 5.43
S_SEAL = [SM, 0.5 * (SM + 1), 1.0, 0.5 * (1 + SP), SP]
S_GRID = sorted(set([0.25, 0.5, 0.75, 1.3, 1.6, 2.0, 3.0, 4.0] + S_SEAL))
# the record's MW external field (hunt h81: LSS + M31 + LMC vector sum; Newtonian e_N per footing; toward (l, b))
EN_H81 = {"canonical": 0.01273, "alt": 0.01054}
DIR_LB = (268.5, 33.0)
GAMMA_DEG = 57.0
MU_K_HMPC, H_LITTLE = 14.8, 0.674
LSTARS_PC = (21.7, 22.9, 24.0, 90.0)

# ------------------------------------------------------------------ McMillan 2017 (as CFG514)
PC2, PC3 = 1e6, 1e9
S0_THIN, RD_THIN, ZD_THIN = 896.0 * PC2, 2.50, 0.300
S0_THICK, RD_THICK, ZD_THICK = 183.0 * PC2, 3.02, 0.900
RHO0_B, ALPHA_B, R0_B, RCUT_B, Q_B = 98.4 * PC3, 1.8, 0.075, 2.1, 0.5
R_FID = 8.33
S0_HI = 10.0 * PC2 / math.exp(-4.0 / R_FID - R_FID / 7.0)
S0_H2 = 2.0 * PC2 / math.exp(-12.0 / R_FID - R_FID / 1.5)


def rho_stars(R, z):
    z = np.abs(z)
    thin = (S0_THIN / (2 * ZD_THIN)) * np.exp(-z / ZD_THIN - R / RD_THIN)
    thick = (S0_THICK / (2 * ZD_THICK)) * np.exp(-z / ZD_THICK - R / RD_THICK)
    rp = np.maximum(np.sqrt(R * R + (z / Q_B) ** 2), 1e-7)
    bulge = RHO0_B / (1 + rp / R0_B) ** ALPHA_B * np.exp(-(rp / RCUT_B) ** 2)
    return thin + thick + bulge


def rho_gas(R, z):
    z = np.abs(z)
    Rs = np.maximum(R, 1e-6)
    hi = (S0_HI * np.exp(-4.0 / Rs - Rs / 7.0) / (4 * 0.085)) / np.cosh(z / (2 * 0.085)) ** 2
    h2 = (S0_H2 * np.exp(-12.0 / Rs - Rs / 1.5) / (4 * 0.045)) / np.cosh(z / (2 * 0.045)) ** 2
    return hi + h2


def rho_mcm(R, z):
    return rho_stars(R, z) + rho_gas(R, z)


def rho_b2(R, z, Mtot=6.0e10):                 # CFG516 (L172 shapes)
    s = Mtot / 6.0e10
    Mbul, abul = 0.90e10 * s, 0.7
    Md, Rd, hd = 4.03e10 * s, 2.6, 0.3
    Mg, Rg, hg = 1.08e10 * s, 6.0, 0.1
    z = np.abs(z); r = np.maximum(np.sqrt(R * R + z * z), 1e-7)
    bul = Mbul * abul / (2 * math.pi * r * (r + abul) ** 3)
    disc = Md / (4 * math.pi * Rd ** 2 * hd) * np.exp(-R / Rd - z / hd)
    gas = Mg / (4 * math.pi * Rg ** 2 * hg) * np.exp(-R / Rg - z / hg)
    return bul + disc + gas


RD_SHORT = 2.15


def rho_b3(R, z):                              # CFG516 (short disc, each disc's Sigma(R0) kept)
    zz = np.abs(z)
    old_thin = (S0_THIN / (2 * ZD_THIN)) * np.exp(-zz / ZD_THIN - R / RD_THIN)
    old_thick = (S0_THICK / (2 * ZD_THICK)) * np.exp(-zz / ZD_THICK - R / RD_THICK)
    s_thin = S0_THIN * math.exp(-R0 / RD_THIN + R0 / RD_SHORT)
    s_thick = S0_THICK * math.exp(-R0 / RD_THICK + R0 / RD_SHORT)
    new_thin = (s_thin / (2 * ZD_THIN)) * np.exp(-zz / ZD_THIN - R / RD_SHORT)
    new_thick = (s_thick / (2 * ZD_THICK)) * np.exp(-zz / ZD_THICK - R / RD_SHORT)
    return rho_mcm(R, z) - old_thin - old_thick + new_thin + new_thick


VARIANTS = {"B2_6.0e10": lambda R, z: rho_b2(R, z, 6.0e10), "B2b_7.3e10": lambda R, z: rho_b2(R, z, 7.3e10),
            "B3_short_disc": rho_b3}

GRID_MAIN = (0.02, 1.045, 3000.0, 0.01, 1.06, 3000.0)
GRID_FINE = (0.0133, 1.03, 3000.0, 0.0067, 1.04, 3000.0)


def ext_unit():
    """unit vector of the external acceleration in a galactocentric frame: x from the Sun to the GC (l = 0), y toward
    l = 90 (rotation at the Sun), z = NGP.  Directions are frame-independent, so (l, b) is used directly."""
    l, b = map(math.radians, DIR_LB)
    return np.array([math.cos(b) * math.cos(l), math.cos(b) * math.sin(l), math.sin(b)])


class MW:
    def __init__(self, grid=GRID_MAIN, tag="main"):
        self.g = S.Grid(*grid)
        self.tag = tag + S.TAG
        self._mem = {}
        g = self.g
        self.rs = rho_stars(g.RR, g.ZZ)
        self.rg = rho_gas(g.RR, g.ZZ)
        self.Ms, self.Mg = S.total_mass(g, self.rs), S.total_mass(g, self.rg)
        PBs = S.bc_newton(g, self.Ms); PBg = S.bc_newton(g, self.Mg)
        self.PhiN_s, self.PhiN_g = g.newton(self.rs, PBs), g.newton(self.rg, PBg)
        self.PBN_s, self.PBN_g = PBs, PBg

    def rho(self, s):
        return s * self.rs + self.rg

    def phiN(self, s):
        PB = {k: s * self.PBN_s[k] + self.PBN_g[k] for k in self.PBN_s}
        return s * self.PhiN_s + self.PhiN_g, PB

    def gN_plane(self, s, R):
        return s * self.g.gR_plane(self.PhiN_s, R) + self.g.gR_plane(self.PhiN_g, R)

    def solve(self, foot, s, eN=0.0, rho=None, key_extra=""):
        """AQUAL solve; eN > 0: external field along +z (gamma = 0).  Cached."""
        a0 = S.A0[foot]
        key = f"{self.tag}|{foot}|s{s:.6f}|eN{eN:.6f}|{key_extra}"
        if key in self._mem:
            self._mem[key] = self._mem.pop(key)          # LRU touch
            return self._mem[key]
        fn = os.path.join(CACHE, "mw_" + hashlib.sha1(key.encode()).hexdigest()[:16] + ".npz")
        if os.path.exists(fn):
            z = np.load(fn)
            out = (z["Phi"], json.loads(str(z["info"])), {k: z["PB_" + k] for k in ("R", "B", "T")}, float(z["ge"]))
            self._remember(key, out)
            return out
        g = self.g
        if rho is None:
            rho = self.rho(s); PhiN, PBN = self.phiN(s)
        else:
            PBN = S.bc_newton(g, S.total_mass(g, rho)); PhiN = g.newton(rho, PBN)
        M = S.total_mass(g, rho)
        if eN > 0:
            PB, ge = S.bc_aqual_efe_z(g, M, a0, eN)
            Phi, info = g.aqual(rho, a0, PB, Phi_init_N=PhiN, PB_N=PBN, ge=ge, ye_a0=eN * a0)
        else:
            PB, ge = S.bc_aqual_iso(g, M, a0), 0.0
            Phi, info = g.aqual(rho, a0, PB, Phi_init_N=PhiN, PB_N=PBN)
        info = dict(iters=info["iters"], residual=info["residual"], floor=info["floor"])
        np.savez(fn, Phi=Phi, info=json.dumps(info), ge=ge, **{"PB_" + k: v for k, v in PB.items()})
        self._remember(key, (Phi, info, PB, ge))
        return Phi, info, PB, ge

    def _remember(self, key, val, cap=6):
        self._mem[key] = val
        while len(self._mem) > cap:
            self._mem.pop(next(iter(self._mem)))

    def vc2(self, foot, s, R, eN=0.0):
        Phi, info, PB, ge = self.solve(foot, s, eN)
        return self.g.vc2(Phi, R), info


def newton_field_func(mw, s=1.0):
    """F_N = grad Phi_N (outward for attraction) as a Cartesian function from the axisymmetric Newtonian solve."""
    from scipy.interpolate import RegularGridInterpolator
    Phi, PB = mw.phiN(s)
    dPR, dPz = mw.g.cell_derivs(Phi, PB)
    iR = RegularGridInterpolator((mw.g.Rc, mw.g.zc), dPR, bounds_error=False, fill_value=None)
    iZ = RegularGridInterpolator((mw.g.Rc, mw.g.zc), dPz, bounds_error=False, fill_value=None)

    def F(X, Y, Z):
        R = np.sqrt(X * X + Y * Y)
        pts = np.stack([R.ravel(), Z.ravel()], -1)
        fR = iR(pts).reshape(R.shape); fz = iZ(pts).reshape(R.shape)
        Rs = np.maximum(R, 1e-12)
        return fR * X / Rs, fR * Y / Rs, fz
    return F


R3D = np.array([5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 35.0, 40.0, 50.0, 60.0])
PH3D = np.radians(np.arange(0.0, 360.0, 5.0))


def anticentre_mask(ph):
    """galactocentric azimuth phi measured from +x (Sun -> GC direction); the anticentre side of the GC is phi = 180 deg."""
    d = np.degrees(np.angle(np.exp(1j * (ph - math.pi))))
    return np.abs(d) <= 30.0


def run_3d(mw, foot, eN, gamma_deg, N, Lbox=640.0, s=1.0):
    """3-D EFE solve; returns the in-plane radial field (dPhi/dR, internal = total minus the uniform part) on R3D x PH3D,
    and sphere-averaged radial fields for Gauss masses at R3D.  Cached as JSON."""
    a0 = S.A0[foot]
    key = f"3d|{mw.tag}|{foot}|eN{eN:.6f}|g{gamma_deg:.3f}|N{N}|L{Lbox}|s{s:.6f}"
    fn = os.path.join(CACHE, "mw3d_" + hashlib.sha1(key.encode()).hexdigest()[:16] + ".json")
    if os.path.exists(fn):
        return json.load(open(fn))
    if not os.environ.get("S3_CHILD"):
        import subprocess, sys as _sys
        env = dict(os.environ, S3_CHILD="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
        code = ("import sys; sys.path.insert(0, %r); import s3_mw as M; mw = M.MW(M.GRID_MAIN if %r == 'main' else M.GRID_FINE, tag=%r); "
                "M.run_3d(mw, %r, %r, %r, %r, %r, %r)" % (HERE, mw.tag.replace(S.TAG, ''), mw.tag.replace(S.TAG, ''), foot, eN, gamma_deg, N, Lbox, s))
        subprocess.run([_sys.executable, "-c", code] + (["--mutate"] if S.MUTATE else []), env=env, check=True)
        return json.load(open(fn))
    xe = S.gtot_from_newton(eN) if not S.MUTATE else eN
    if gamma_deg == 0.0:
        e = np.array([0.0, 0.0, 1.0])
    else:
        e = ext_unit()
        assert abs(math.degrees(math.acos(e[2])) - gamma_deg) < 0.05, (math.degrees(math.acos(e[2])), gamma_deg)
    FN = newton_field_func(mw, s)
    E = S.EFE3D(N, Lbox, FN, xe * a0 * e, a0)
    phs = np.radians(np.arange(0.0, 360.0, 45.0))

    def probe(E):
        out = []
        for R in (15.0, 27.5, 60.0):
            P = np.stack([R * np.cos(phs), R * np.sin(phs), 0 * phs], 1)
            d = E.d_at(P); fx, fy, fz = FN(P[:, 0], P[:, 1], P[:, 2])
            out.append((fx + d[:, 0]) * np.cos(phs) + (fy + d[:, 1]) * np.sin(phs))
        return np.concatenate(out)
    info = E.solve(probe=probe)
    FR = np.zeros((len(R3D), len(PH3D)))
    for i, R in enumerate(R3D):
        P = np.stack([R * np.cos(PH3D), R * np.sin(PH3D), 0 * PH3D], 1)
        d = E.d_at(P); fx, fy, fz = FN(P[:, 0], P[:, 1], P[:, 2])
        FR[i] = (fx + d[:, 0]) * np.cos(PH3D) + (fy + d[:, 1]) * np.sin(PH3D)
    # sphere averages of the radial internal field (Fibonacci points)
    n = 2000
    k = np.arange(n) + 0.5
    th = np.arccos(1 - 2 * k / n); ph = math.pi * (1 + 5 ** 0.5) * k
    U = np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)], 1)
    Fsph = []
    for R in R3D:
        P = R * U
        d = E.d_at(P); fx, fy, fz = FN(P[:, 0], P[:, 1], P[:, 2])
        Fsph.append(float(np.mean(((fx + d[:, 0]) * U[:, 0] + (fy + d[:, 1]) * U[:, 1] + (fz + d[:, 2]) * U[:, 2]))))
    out = dict(foot=foot, eN=eN, gamma=gamma_deg, N=N, L=Lbox, s=s, iters=info["iters"], converged=info["converged"],
               last_change=info["last_change"], R=R3D.tolist(), ph_deg=np.degrees(PH3D).tolist(), FR=FR.tolist(), Fsph=Fsph)
    del E
    json.dump(out, open(fn, "w"))
    return out


def l_g_pc(Lstar_pc, r_M_kpc):
    """screening length l_g = L*^2 / (2 r_M) in pc."""
    return (Lstar_pc ** 2) / (2 * r_M_kpc * 1e3)


_MWS = {}


def job_mw_solve(grid, tag, foot, s, eN):
    """child job: one cached AQUAL solve (writes the npz); returns its info."""
    k = (tuple(grid), tag)
    if k not in _MWS:
        _MWS[k] = MW(tuple(grid), tag=tag)
    Phi, info, PB, ge = _MWS[k].solve(foot, s, eN)
    return dict(info=info)


def presolve(mw, grid, tag, cells, batch=4):
    """run the listed (foot, s, eN) solves in child processes unless already cached."""
    todo = []
    for foot, s, eN in cells:
        key = f"{tag + S.TAG}|{foot}|s{s:.6f}|eN{eN:.6f}|"
        fn = os.path.join(CACHE, "mw_" + hashlib.sha1(key.encode()).hexdigest()[:16] + ".npz")
        if not os.path.exists(fn):
            todo.append(dict(grid=list(grid), tag=tag, foot=foot, s=s, eN=eN))
    if not todo:
        return 0, 0.0
    res, peak = S.run_batch("s3_mw", "job_mw_solve", todo, batch=batch)
    return len(todo), peak


def job_mw_variant(grid, tag, foot, variant, eN):
    """child job: AQUAL solve for a declared baryon variant (B2 / B2b / B3) at census (cached via key_extra)."""
    k = (tuple(grid), tag)
    if k not in _MWS:
        _MWS[k] = MW(tuple(grid), tag=tag)
    m = _MWS[k]
    rho = VARIANTS[variant](m.g.RR, m.g.ZZ)
    Phi, info, PB, ge = m.solve(foot, 1.0, eN, rho=rho, key_extra=variant)
    return dict(info=info)


def job_plummer_check(foot, eN, gamma_deg=57.0, N=160, Lbox=640.0, M=6.6e10, b=3.0):
    """child job (AMENDMENT A3, check C5): exact tilted-field reference vs the pointwise 3-D estimator for a Plummer sphere.
    Exact: axisymmetric solve with the field along its own axis, evaluated in a plane tilted by gamma."""
    from scipy.interpolate import RegularGridInterpolator
    a0 = S.A0[foot]
    xe = S.gtot_from_newton(eN)
    g = S.Grid(*GRID_MAIN)
    rho = (3 * M / (4 * math.pi * b ** 3)) * (1 + (g.RR ** 2 + g.ZZ ** 2) / b ** 2) ** -2.5
    Mt = S.total_mass(g, rho); PBN = S.bc_newton(g, Mt); PhiN = g.newton(rho, PBN)
    PB, ge = S.bc_aqual_efe_z(g, Mt, a0, eN)
    Phi, info = g.aqual(rho, a0, PB, Phi_init_N=PhiN, PB_N=PBN, ge=ge, ye_a0=eN * a0)
    dPR, dPz = g.cell_derivs(Phi, PB)
    iR = RegularGridInterpolator((g.Rc, g.zc), dPR); iZ = RegularGridInterpolator((g.Rc, g.zc), dPz)
    dNR, dNz = g.cell_derivs(PhiN, PBN)
    nR = RegularGridInterpolator((g.Rc, g.zc), dNR); nZ = RegularGridInterpolator((g.Rc, g.zc), dNz)

    def F_exact(P, e):
        zp = P @ e; perp = P - np.outer(zp, e); Rp = np.linalg.norm(perp, axis=1)
        fR = iR(np.stack([Rp, zp], 1)); fz = iZ(np.stack([Rp, zp], 1))
        return fR[:, None] * perp / np.maximum(Rp, 1e-12)[:, None] + fz[:, None] * e[None, :]

    def FN(X, Y, Z):
        R = np.sqrt(X * X + Y * Y); pts = np.stack([R.ravel(), Z.ravel()], -1)
        fR = nR(pts).reshape(R.shape); fz = nZ(pts).reshape(R.shape); Rs = np.maximum(R, 1e-12)
        return fR * X / Rs, fR * Y / Rs, fz
    gam = math.radians(gamma_deg)
    e57 = np.array([0.0, -math.sin(gam), math.cos(gam)]); e0 = np.array([0.0, 0.0, 1.0])
    Rs = np.array([15.0, 20.0, 27.5, 40.0, 60.0]); ph = PH3D
    out = {}
    F3 = {}
    for tagd, e in (("57", e57), ("0", e0)):
        E = S.EFE3D(N, Lbox, FN, xe * a0 * e, a0)
        phs = np.radians(np.arange(0.0, 360.0, 45.0))

        def probe(E):
            o = []
            for R in (15.0, 27.5, 60.0):
                P = np.stack([R * np.cos(phs), R * np.sin(phs), 0 * phs], 1)
                d = E.d_at(P); fx, fy, fz = FN(P[:, 0], P[:, 1], P[:, 2])
                o.append((fx + d[:, 0]) * np.cos(phs) + (fy + d[:, 1]) * np.sin(phs))
            return np.concatenate(o)
        E.solve(probe=probe)
        arr = np.zeros((len(Rs), len(ph)))
        for i, R in enumerate(Rs):
            P = np.stack([R * np.cos(ph), R * np.sin(ph), 0 * ph], 1)
            d = E.d_at(P); fx, fy, fz = FN(P[:, 0], P[:, 1], P[:, 2])
            arr[i] = (fx + d[:, 0]) * np.cos(ph) + (fy + d[:, 1]) * np.sin(ph)
        F3[tagd] = arr
        del E
    ex57 = np.zeros((len(Rs), len(ph))); ex0 = np.zeros((len(Rs), len(ph)))
    for i, R in enumerate(Rs):
        P = np.stack([R * np.cos(ph), R * np.sin(ph), 0 * ph], 1)
        ex57[i] = (F_exact(P, e57) * P).sum(1) / R
        ex0[i] = (F_exact(P, e0) * P).sum(1) / R
    est = ex0 * F3["57"] / F3["0"]                 # pointwise estimator: exact gamma-0 x 3-D ratio
    err = np.abs(est / ex57 - 1)
    p2p_est = (est.max(1) - est.min(1)) / est.mean(1); p2p_ex = (ex57.max(1) - ex57.min(1)) / ex57.mean(1)
    return dict(R=Rs.tolist(), max_rel_err=float(err.max()), p2p_est=p2p_est.tolist(), p2p_exact=p2p_ex.tolist(),
                p2p_absdiff=float(np.max(np.abs(p2p_est - p2p_ex))), axi_residual=info["residual"])


def job_A4(which):
    """child job: Part A's solver controls A4(i)-(iii) with the true mu (they validate the code, not the mutate)."""
    if which in ("plummer_iso", "plummer_efe"):
        a0c = 1.0; Mc = 1.0 / S.G; b = 0.01
        gp = S.Grid(0.0005, 1.04, 300.0, 0.0005, 1.04, 300.0)
        rhoP = (3 * Mc / (4 * math.pi * b ** 3)) * (1 + (gp.RR ** 2 + gp.ZZ ** 2) / b ** 2) ** -2.5
        MP = S.total_mass(gp, rhoP); PBN = S.bc_newton(gp, MP); PhiNP = gp.newton(rhoP, PBN)
        if which == "plummer_iso":
            PhiP, info = gp.aqual(rhoP, a0c, S.bc_aqual_iso(gp, MP, a0c), Phi_init_N=PhiNP, PB_N=PBN, mufun=S.mu_true)
            Rr = np.geomspace(0.3 * b, 30 * b, 15)
            gNx = S.G * MP * Rr / (Rr ** 2 + b ** 2) ** 1.5
            return dict(err=float(np.max(np.abs(gp.gR_plane(PhiP, Rr) / (S.nu1(gNx / a0c) * gNx) - 1))), grid=gp.describe(), residual=info["residual"])
        xe = float(S.nu1(0.1) * 0.1); ge = xe * a0c
        L0 = 1.0 / (1 + xe); mue = xe / (1 + xe)
        PBe = {}
        for k, (R, z) in gp.bpoints().items():
            PBe[k] = -S.G * MP / (mue * math.sqrt(1 + L0) * np.sqrt(R ** 2 + z ** 2 / (1 + L0)))
        PhiE, info = gp.aqual(rhoP, a0c, PBe, Phi_init_N=PhiNP, PB_N=PBN, ge=ge, ye_a0=0.1, mufun=S.mu_true)
        import importlib.util
        spec = importlib.util.spec_from_file_location("aqual_axi", os.path.join(HERE, "..", "..", "doors_push_2026_10_22", "E2_field_equation", "aqual_axi.py"))
        E2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(E2)
        sol = E2.AxiSolver(E2.law_canonical(), 0.1, mode="AQUAL"); sol.solve(tol=1e-11)
        rr = np.array([0.5, 1.0, 2.0, 4.0])
        drr, _ = sol.field_at(rr, np.full_like(rr, np.pi / 2))
        return dict(err=float(np.max(np.abs(gp.gR_plane(PhiE, rr) / (1 / rr ** 2 + drr) - 1))), residual=info["residual"])
    if which == "kuzmin":
        gk = S.Grid(0.01, 1.04, 3000.0, 0.001, 1.05, 3000.0)
        ak, Mk, a0k = 1.0, 1e10, S.A0["canonical"]
        rhoK = np.zeros((gk.nR, gk.nz))
        MencK = Mk * (1 - ak / np.sqrt(gk.Re ** 2 + ak ** 2))
        rhoK[:, gk.jc] = np.diff(MencK) / (math.pi * (gk.Re[1:] ** 2 - gk.Re[:-1] ** 2)) / gk.dz[gk.jc]
        MK = S.total_mass(gk, rhoK); PBN = S.bc_newton(gk, MK); PhiNK = gk.newton(rhoK, PBN)
        PBK = S.bc_aqual_iso(gk, MK, a0k) if not S.MUTATE else None
        if S.MUTATE:          # true-mu boundary for the control
            rref = float(gk.Re[-1]); PBK = {}
            for k, (R, z) in gk.bpoints().items():
                r = np.hypot(R, z); lr = np.linspace(np.log(r.min()) - 1e-9, np.log(max(r.max(), rref)) + 1e-9, 20001); x = np.exp(lr)
                gN = S.G * MK / x ** 2; gg = S.nu1(gN / a0k) * gN
                cum = np.concatenate([[0.0], np.cumsum(0.5 * (gg[1:] * x[1:] + gg[:-1] * x[:-1]) * np.diff(lr))])
                PBK[k] = np.interp(np.log(r), lr, cum) - np.interp(np.log(rref), lr, cum)
        PhiK, info = gk.aqual(rhoK, a0k, PBK, Phi_init_N=PhiNK, PB_N=PBN, mufun=S.mu_true)
        Rr = np.geomspace(0.3, 20, 15)
        gNR = S.G * MK * Rr / (Rr ** 2 + ak ** 2) ** 1.5; gNm = S.G * MK / (Rr ** 2 + ak ** 2)
        eK = float(np.max(np.abs(gk.gR_plane(PhiK, Rr) / (S.nu1(gNm / a0k) * gNR) - 1)))
        dPR, dPz = gk.cell_derivs(PhiK, PBK)
        Ro = np.array([0.5, 1.0, 2.0, 5.0, 10.0]); zo = 0.5 * ak
        mag = np.hypot(gk.interp2(dPR, Ro, np.full_like(Ro, zo)), gk.interp2(dPz, Ro, np.full_like(Ro, zo)))
        gn = S.G * MK / (Ro ** 2 + (zo + ak) ** 2)
        eK2 = float(np.max(np.abs(mag / (S.nu1(gn / a0k) * gn) - 1)))
        alg_ratio = float(gk.gR_plane(PhiK, np.array([0.3]))[0] / (S.nu1(gNR[0] / a0k) * gNR[0]) - 1)
        return dict(eK=eK, eK2=eK2, alg_ratio=alg_ratio, residual=info["residual"])
    raise ValueError(which)


def job_A4iv():
    """child job: main vs fine grid V(15-27.5 kpc) and slope at s = 1 (cached solves)."""
    def slope_w(R, V):
        return float(np.polyfit(np.log(R), np.log(V), 1)[0])
    out = dict(dv=0.0, dsl=0.0)
    mwm = MW(GRID_MAIN, tag="main"); mwf = MW(GRID_FINE, tag="fine")
    Rr = np.linspace(15, 27.5, 26)
    for foot in S.FOOTS:
        for eN in (0.0, EN_H81[foot]):
            Pm, _, _, _ = mwm.solve(foot, 1.0, eN); Pf, _, _, _ = mwf.solve(foot, 1.0, eN)
            va, vb = np.sqrt(mwm.g.vc2(Pm, Rr)), np.sqrt(mwf.g.vc2(Pf, Rr))
            out["dv"] = max(out["dv"], float(np.max(np.abs(va / vb - 1))))
            out["dsl"] = max(out["dsl"], abs(slope_w(Rr, va) - slope_w(Rr, vb)))
    out["fine"] = mwf.g.describe()
    return out
