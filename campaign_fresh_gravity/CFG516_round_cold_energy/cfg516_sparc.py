#!/usr/bin/env python3
"""CFG516 Parts 2 + 3: SPARC rotation curves under the round enclosed-mass rule (RM) vs the full QUMOND field (PD),
and the edge-on vertical-structure predictions (PD vs RM).

Frozen criteria: FROZEN_CRITERIA.md (committed alone first, b35642ca6).
Per galaxy (Q <= 2, Upsilon_disk 0.5, Upsilon_bul 0.7) one 3-D baryon model on CFG514's axisymmetric finite-volume grid
(scale-free; grid unit u = R_last/25):
  stars  Sigma = 0.5 SBdisk, exponential vertical h_z = 0.196 R_disk^0.633 kpc
  bulge  spherical, M(<r) = 0.7 r V_bul^2 / G
  gas    non-negative annulus inversion of V_gas|V_gas|, exponential vertical h_g = 0.1 kpc
Models at every data radius: ALG (algebraic law in the plane), PD (full QUMOND), RMphi (spherical cold energy carrying the
phantom's enclosed mass), RMv (spherical cold energy with M_law(<r) = r v_ALG^2/G).
Statistic (CFG476's): weighted rms of log g_obs - log g_model, weights (V/eV)^2.
kappa = 1/2 is FITTED (here a0 is also fitted, and kappa is reported on both footings); cold energy mass still required;
not theory closed.
Run: nice -n 15 python3 cfg516_sparc.py   (<= 4 threads; ~10-20 min)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "4"
import sys, json, math, time
import numpy as np
from scipy.optimize import nnls
from scipy.special import ellipk
from scipy.interpolate import RegularGridInterpolator

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data")
SRC514 = os.path.join(HERE, "..", "CFG514_directional_milky_way", "cfg514_directional.py")
src = open(SRC514).read()
head = src.split("# ------------------------------------------------------------------ build the framework / rival")[0]
ns = {"__file__": os.path.abspath(SRC514)}
exec(compile(head, "cfg514_head", "exec"), ns)
G, KPC_M, Grid, nu_mono = ns["G"], ns["KPC_M"], ns["Grid"], ns["nu_mono"]
A0_SI = {"canonical": 9.36e-11, "alt": 1.13e-10}
CONV = KPC_M / 1e6                      # m/s^2 -> (km/s)^2/kpc
A0 = {k: v * CONV for k, v in A0_SI.items()}
UPS_D, UPS_B = 0.5, 0.7
HG = 0.1
A0_GRID_SI = np.geomspace(5e-11, 2e-10, 31)
QUICK = os.environ.get("CFG516_QUICK", "0") == "1"
INNER = os.environ.get("CFG516_INNER", "const")      # post-run variant V2 ("exp"): stellar Sigma rises inward with R_disk inside R_1
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.append(s)


def check(cond, msg):
    CHECKS.append((bool(cond), msg)); P(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
    return bool(cond)


# ------------------------------------------------------------------ SPARC
def load():
    tab = {}
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
    for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        tok = line.split()
        if len(tok) != 19:
            continue
        try:
            vals = [float(t) for t in tok[1:18]]
        except ValueError:
            continue
        tab[tok[0]] = dict(zip(keys, vals))
    gal = []
    d_ = os.path.join(DATA, "sparc_data")
    for f in sorted(os.listdir(d_)):
        if not f.endswith("_rotmod.dat"):
            continue
        d = np.genfromtxt(os.path.join(d_, f), comments="#")
        if d.ndim != 2 or d.shape[1] < 8:
            continue
        name = f.replace("_rotmod.dat", "")
        m = tab.get(name)
        if m is None or int(m["Q"]) > 2:
            continue
        gal.append(dict(name=name, R=d[:, 0], V=d[:, 1], eV=d[:, 2], Vg=d[:, 3], Vd=d[:, 4], Vb=d[:, 5], SBd=d[:, 6], SBb=d[:, 7], meta=m))
    return gal


# ------------------------------------------------------------------ one grid, used scale-free
GR = Grid()
NG = GR.n
XR, XZ = GR.RR, GR.ZZ


def ring_phi(a, R, z):
    """potential of a unit-mass thin ring of radius a at (R, z)."""
    s2 = (R + a) ** 2 + z ** 2
    k2 = np.clip(4 * a * R / s2, 0, 1 - 1e-12)
    return -2 * G * ellipk(k2) / (math.pi * np.sqrt(s2))


def annulus_gR(r1, r2, R, zs, nsub=24):
    """inward radial field at (R, zs) of a uniform annulus r1..r2 of unit mass (sub-ring quadrature, z-softened)."""
    a = r1 + (np.arange(nsub) + 0.5) / nsub * (r2 - r1)
    w = a / a.sum()
    h = 1e-4 * np.maximum(R, 1e-3)
    out = np.zeros_like(R)
    for ai, wi in zip(a, w):
        out += wi * (ring_phi(ai, R + h, zs) - ring_phi(ai, R - h, zs)) / (2 * h)
    return out


def build_density(g, u):
    """3-D baryon density on the grid cells (physical Msun/kpc^3), for grid unit u (kpc)."""
    R, Rl = g["R"], g["R"][-1]
    Rd = g["meta"]["Rdisk"] if g["meta"]["Rdisk"] > 0 else Rl / 4
    hz = 0.196 * Rd ** 0.633
    Rc = XR * u; Zc = XZ * u
    # stars
    Sd = UPS_D * np.maximum(g["SBd"], 0) * 1e6
    Sig = np.interp(Rc, R, Sd, left=Sd[0], right=Sd[-1])
    Sig = np.where(Rc > Rl, Sd[-1] * np.exp(-(Rc - Rl) / Rd), Sig)
    if INNER == "exp":
        Sig = np.where(Rc < R[0], Sd[0] * np.exp((R[0] - Rc) / Rd), Sig)
    rho_s = Sig / (2 * hz) * np.exp(-np.abs(Zc) / hz)
    # bulge (spherical)
    rho_bu = np.zeros_like(Rc)
    if np.any(g["Vb"] > 0):
        Mb = np.maximum.accumulate(UPS_B * R * g["Vb"] ** 2 / G)
        rr = np.concatenate([[0.0], R]); MM = np.concatenate([[0.0], Mb])
        rq = np.sqrt(Rc ** 2 + Zc ** 2)
        dens = np.diff(MM) / (4 / 3 * math.pi * np.diff(rr ** 3))
        k = np.searchsorted(rr, rq) - 1
        rho_bu = np.where((k >= 0) & (k < len(dens)), dens[np.clip(k, 0, len(dens) - 1)], 0.0)
    # gas: annulus NNLS
    edges = np.concatenate([[0.0], 0.5 * (R[1:] + R[:-1]), [Rl + 0.5 * (R[-1] - R[-2]) if len(R) > 1 else 1.1 * Rl]])
    extra = np.linspace(edges[-1], 1.6 * Rl, 5)[1:]
    edges = np.concatenate([edges, extra])
    zs = HG
    A = np.stack([annulus_gR(edges[j], edges[j + 1], R, zs) * R for j in range(len(edges) - 1)], 1)   # V^2 per unit mass
    y = g["Vg"] * np.abs(g["Vg"])
    wts = 1.0 / np.maximum(np.abs(y), 0.05 * np.max(np.abs(y)) + 1e-6)
    mass, _ = nnls(A * wts[:, None], y * wts)
    area = math.pi * (edges[1:] ** 2 - edges[:-1] ** 2)
    Sg_ring = mass / area
    k = np.clip(np.searchsorted(edges, Rc) - 1, 0, len(Sg_ring) - 1)
    Sgas = np.where(Rc < edges[-1], Sg_ring[k], 0.0)
    rho_g = Sgas / (2 * HG) * np.exp(-np.abs(Zc) / HG)
    Vg_fit = np.sign(A @ mass) * np.sqrt(np.abs(A @ mass))
    return rho_s + rho_bu + rho_g, dict(hz=hz, Rd=Rd, Vg_fit=Vg_fit, Mgas=float(mass.sum()))


class GalField:
    def __init__(self, g):
        self.g = g
        self.u = g["R"][-1] / 25.0
        u = self.u
        self.rho, self.info = build_density(g, u)
        self.Mb = 2 * np.sum(2 * math.pi * self.rho * GR.VOL) * u ** 3
        self.rbR, self.rbZ = GR.rbR * u, GR.rbZ * u
        pR, pZ = -G * self.Mb / self.rbR, -G * self.Mb / self.rbZ
        self.PhiN = GR.poisson(self.rho * u ** 2, pR, pZ)
        self.pNR, self.pNZ = pR, pZ
        dR, dz = GR.grad(self.PhiN, pR, pZ)
        self.gN = (dR / u, dz / u)
        self.iN = self._interp(dR / u, dz / u)
        self.Rpts = g["R"]
        self.zmid = GR.zc[0] * u
        self.gNp = self.gRz(self.iN, self.Rpts, np.full_like(self.Rpts, self.zmid))[0]   # in-plane inward radial field
        self.MbR = self.flux_mass(self.iN, self.Rpts)

    def _interp(self, dR, dz):
        kw = dict(bounds_error=False, fill_value=None)
        return (RegularGridInterpolator((GR.Rc, GR.zc), dR, **kw), RegularGridInterpolator((GR.Rc, GR.zc), dz, **kw))

    def gRz(self, it, R, z):
        x = np.clip(np.asarray(R) / self.u, GR.Rc[0], GR.Rc[-1]); y = np.clip(np.abs(np.asarray(z)) / self.u, GR.zc[0], GR.zc[-1])
        pts = np.stack([x, y], -1)
        return it[0](pts), it[1](pts)

    def flux_mass(self, it, r, nth=120):
        mu = (np.arange(nth) + 0.5) / nth
        out = []
        for rr in np.atleast_1d(r):
            z = rr * mu; R = rr * np.sqrt(1 - mu ** 2)
            dR, dz = self.gRz(it, R, z)
            out.append(rr ** 2 * np.mean((dR * R + dz * z) / rr) / G)
        return np.array(out)

    def pd(self, a0):
        """full QUMOND; returns interpolators of the total field."""
        u = self.u
        nu_c = nu_mono(np.hypot(*self.gN) / a0)
        rho_ph_u2 = GR.phantom_source(self.PhiN, self.pNR, self.pNZ, nu_c)          # = u^2 rho_ph (x-units operator)
        pbR = ns["phi_qumond_sph"](self.Mb, a0, self.rbR); pbZ = ns["phi_qumond_sph"](self.Mb, a0, self.rbZ)
        Phi = GR.poisson(self.rho * u ** 2 + rho_ph_u2, pbR, pbZ)
        dR, dz = GR.grad(Phi, pbR, pbZ)
        return self._interp(dR / u, dz / u), rho_ph_u2 / u ** 2

    def models(self, a0, want_vertical=False):
        R = self.Rpts
        gN = self.gNp
        g_alg = nu_mono(np.abs(gN) / a0) * gN
        itP, rho_ph = self.pd(a0)
        g_pd = self.gRz(itP, R, np.full_like(R, self.zmid))[0]
        Mph = self.flux_mass(itP, R) - self.MbR
        g_phi = gN + G * Mph / R ** 2
        g_v = gN + g_alg - G * self.MbR / R ** 2
        out = dict(ALG=g_alg, PD=g_pd, RMphi=g_phi, RMv=g_v, Mph=Mph, rho_ph=rho_ph)
        if want_vertical:
            out["itP"] = itP
        return out


def wrms(res, w):
    return float(np.sqrt(np.sum(w * res ** 2) / np.sum(w)))


# ------------------------------------------------------------------ run
T0 = time.time()
P("=" * 110)
P("CFG516 Parts 2+3  SPARC: round enclosed-mass rule vs full QUMOND; edge-on vertical predictions")
P("=" * 110)
GALS = load()
if QUICK:
    GALS = GALS[::12]
P(f"  galaxies (Q <= 2): {len(GALS)}")

# S3: Plummer QUMOND in galaxy units (u = 0.4 kpc): scale-free use of the grid
P("\n--- controls")
u = 0.4; Mp, bp = 1e9, 1.0
rcell = np.sqrt((XR * u) ** 2 + (XZ * u) ** 2)
rho_pl = 3 * Mp / (4 * math.pi * bp ** 3) * (1 + rcell ** 2 / bp ** 2) ** -2.5
pR, pZ = -G * Mp / np.sqrt((GR.rbR * u) ** 2 + bp ** 2), -G * Mp / np.sqrt((GR.rbZ * u) ** 2 + bp ** 2)
PhiN = GR.poisson(rho_pl * u ** 2, pR, pZ)
dR, dz = GR.grad(PhiN, pR, pZ)
a0c = A0["canonical"]
nuc = nu_mono(np.hypot(dR / u, dz / u) / a0c)
rph = GR.phantom_source(PhiN, pR, pZ, nuc)
pbR = ns["phi_qumond_sph"](Mp, a0c, GR.rbR * u); pbZ = ns["phi_qumond_sph"](Mp, a0c, GR.rbZ * u)
Phi = GR.poisson(rho_pl * u ** 2 + rph, pbR, pbZ)
dR, dz = GR.grad(Phi, pbR, pbZ)
iR = RegularGridInterpolator((GR.Rc, GR.zc), np.hypot(dR, dz) / u)
rt = np.array([0.5, 1, 2, 5, 10, 20.0])
gnum = iR(np.stack([rt / u, np.full_like(rt, GR.zc[0])], -1))
gNa = G * Mp * rt / (rt ** 2 + bp ** 2) ** 1.5
dev = float(np.max(np.abs(gnum / (nu_mono(gNa / a0c) * gNa) - 1)))
check(dev < 0.02, f"S3 QUMOND Plummer (M 1e9, b 1 kpc) on the scale-free grid at u = 0.4 kpc, r = 0.5-20 kpc: max dev {dev:.2%} (< 2%)")

# S5 (informational, added after the QUICK smoke run): QUMOND vs the algebraic law in the plane of a near-Kuzmin
# Miyamoto-Nagai disc (M 3e10, a 3, b 0.1 kpc). For a razor-thin Kuzmin disc QUMOND equals nu(|g_N|) g_N with |g_N|
# including the vertical 2 pi G Sigma just above the plane, so the in-plane radial-only algebraic law over-predicts.
def mn_rho(R, z, M, a, b):
    zb = np.sqrt(z * z + b * b)
    return b * b * M / (4 * math.pi) * (a * R * R + (a + 3 * zb) * (a + zb) ** 2) / ((R * R + (a + zb) ** 2) ** 2.5 * zb ** 3)
Mmn = 3e10
rho_mn = mn_rho(XR, XZ, Mmn, 3.0, 0.1)
pR, pZ = -G * Mmn / GR.rbR, -G * Mmn / GR.rbZ
PhiN = GR.poisson(rho_mn, pR, pZ); dR, dz = GR.grad(PhiN, pR, pZ)
rph = GR.phantom_source(PhiN, pR, pZ, nu_mono(np.hypot(dR, dz) / a0c))
pbR = ns["phi_qumond_sph"](Mmn, a0c, GR.rbR); pbZ = ns["phi_qumond_sph"](Mmn, a0c, GR.rbZ)
Phi = GR.poisson(rho_mn + rph, pbR, pbZ); dR2, _ = GR.grad(Phi, pbR, pbZ)
Rt = np.array([1, 2, 4, 8, 15, 30.0]); pts = np.stack([Rt, np.full_like(Rt, GR.zc[0])], -1)
gNm = RegularGridInterpolator((GR.Rc, GR.zc), dR)(pts); gPm = RegularGridInterpolator((GR.Rc, GR.zc), dR2)(pts)
S5 = (gPm / (nu_mono(gNm / a0c) * gNm)).tolist()
P("  S5 (info) near-Kuzmin MN disc: QUMOND/algebraic in-plane at R = 1,2,4,8,15,30 kpc: " + " ".join(f"{x:.3f}" for x in S5))

rows = []
cache = {}
a0_list = [A0_GRID_SI * CONV][0]
gal_res = []
S1dev, S2data, S4dev = [], [], []
tick = time.time()
for i, g in enumerate(GALS):
    f = GalField(g)
    Vbar2 = g["Vg"] * np.abs(g["Vg"]) + UPS_D * g["Vd"] ** 2 + UPS_B * g["Vb"] ** 2
    vgrid = np.sqrt(np.maximum(f.gNp * g["R"], 0))
    vrot = np.sqrt(np.maximum(Vbar2, 0))
    ok = vrot > 5
    dv = float(np.sqrt(np.mean((vgrid[ok] / vrot[ok] - 1) ** 2))) if ok.sum() else float("nan")
    S1dev.append(dv)
    gobs = g["V"] ** 2 / g["R"]
    w = (g["V"] / np.maximum(g["eV"], 1e-3)) ** 2
    gbar_rot = Vbar2 / g["R"]
    # per-a0 model accelerations (grid); fixed footings evaluated directly as well
    per = {}
    for key, a0 in [("canonical", A0["canonical"]), ("alt", A0["alt"])] + [(f"g{j}", a) for j, a in enumerate(a0_list)]:
        m = f.models(a0, want_vertical=(key in ("canonical", "alt")))
        per[key] = m
    mask = (gobs > 0) & (f.gNp > 0) & (gbar_rot > 0)
    for key in per:
        for mn in ("ALG", "PD", "RMphi", "RMv"):
            mask &= per[key][mn] > 0
    rec = dict(name=g["name"], n=int(mask.sum()), S1=dv, Mb=f.Mb, Mgas=f.info["Mgas"], hz=f.info["hz"], Rd=f.info["Rd"],
               SBd_at_Rd=float(np.interp(f.info["Rd"], g["R"], g["SBd"])))
    rec["res"] = {}
    for key in per:
        rec["res"][key] = {mn: (np.log10(gobs[mask]) - np.log10(per[key][mn][mask])).tolist() for mn in ("ALG", "PD", "RMphi", "RMv")}
    rec["w"] = w[mask].tolist()
    vmatch = np.abs(vgrid / np.maximum(vrot, 1e-6) - 1) <= 0.05
    rec["match"] = vmatch[mask].tolist()
    a0f = A0["canonical"]
    rec["res_rotmod_ALG"] = {k: (np.log10(gobs[mask]) - np.log10(nu_mono(gbar_rot[mask] / A0[k]) * gbar_rot[mask])).tolist() for k in ("canonical", "alt")}
    rec["S2"] = {k: (np.log10(per[k]["ALG"][mask]) - np.log10(nu_mono(gbar_rot[mask] / A0[k]) * gbar_rot[mask])).tolist() for k in ("canonical", "alt")}
    # in-plane ratio PD vs RM (dimensionless shape effect), at the fixed footings
    rec["ratio"] = {k: dict(RMphi_over_PD=np.median(per[k]["RMphi"][mask] / per[k]["PD"][mask]) if mask.any() else float("nan"),
                            RMv_over_PD=np.median(per[k]["RMv"][mask] / per[k]["PD"][mask]) if mask.any() else float("nan"),
                            PD_over_ALG=np.median(per[k]["PD"][mask] / per[k]["ALG"][mask]) if mask.any() else float("nan"))
                    for k in ("canonical", "alt")}
    # ---- Part 3: vertical structure at R = 2 R_d and R_last (fixed footings)
    vert = {}
    for k in ("canonical", "alt"):
        m = per[k]; itP = m["itP"]
        vk = {}
        for lab, Rv in (("2Rd", min(2 * f.info["Rd"], g["R"][-1])), ("Rlast", g["R"][-1])):
            hz = f.info["hz"]
            zz = np.array([0.25 * hz, hz])
            Rq = np.full(2, Rv)
            Kpd = f.gRz(itP, Rq, zz)[1]
            KN = f.gRz(f.iN, Rq, zz)[1]
            r = np.sqrt(Rv ** 2 + zz ** 2)
            # RM cold masses at radius r
            Mph_r = f.flux_mass(itP, r) - f.flux_mass(f.iN, r)
            gN_r = f.gRz(f.iN, r, np.full_like(r, f.zmid))[0]
            Mv_r = r * r * nu_mono(np.abs(gN_r) / A0[k]) * np.abs(gN_r) / G - f.flux_mass(f.iN, r)
            Kphi = KN + G * Mph_r * zz / r ** 3
            Kv = KN + G * Mv_r * zz / r ** 3
            vk[lab] = dict(R=float(Rv), nuz2_PD=float(Kpd[0] / zz[0]), nuz2_RMphi=float(Kphi[0] / zz[0]), nuz2_RMv=float(Kv[0] / zz[0]),
                           Khz_PD=float(Kpd[1]), Khz_RMphi=float(Kphi[1]), Khz_RMv=float(Kv[1]), Khz_N=float(KN[1]))
        vert[k] = vk
    rec["vert"] = vert
    if i < 8:                                   # S4: phantom enclosed mass, Gauss flux vs cell sum (identity)
        m = per["canonical"]; rl = np.array([0.5 * g["R"][-1], g["R"][-1]])
        Mcell = GR.enclosed(m["rho_ph"], rl / f.u) * f.u ** 3
        Mflx = np.interp(rl, g["R"], m["Mph"])
        S4dev.append(float(np.max(np.abs(Mcell / Mflx - 1))))
    gal_res.append(rec)
    if (i + 1) % 10 == 0:
        P(f"  ... {i + 1}/{len(GALS)} galaxies ({time.time() - tick:.0f} s)")

# ------------------------------------------------------------------ controls S1, S2, S4
S1 = np.array([r["S1"] for r in gal_res])
s1med = float(np.nanmedian(S1))
check(s1med <= 0.05, f"S1 grid baryons vs rotmod V_bar: median per-galaxy rms |V_grid/V_bar - 1| = {s1med:.2%} (<= 5%); "
      f"90th pct {np.nanpercentile(S1, 90):.1%}, worst {gal_res[int(np.nanargmax(S1))]['name']} {np.nanmax(S1):.1%}")
W = np.concatenate([r["w"] for r in gal_res])
for k in ("canonical", "alt"):
    s2 = np.concatenate([r["S2"][k] for r in gal_res])
    v = wrms(s2, W)
    check(v <= 0.02, f"S2 [{k}] ALG on grid baryons vs ALG on rotmod V_bar: weighted rms difference {v:.4f} dex (<= 0.02)")

check(max(S4dev) < 0.03, f"S4 RM-phi identity: phantom enclosed mass by Gauss flux vs cell sum at R_last/2, R_last (first 8 galaxies): max dev {max(S4dev):.2%} (< 3%)")

# ------------------------------------------------------------------ statistics
P("\n" + "=" * 110 + "\nPART 2: weighted rms of log g_obs - log g_model (weights (V/eV)^2), all points of all galaxies\n" + "=" * 110)
NPTS = len(W)
P(f"  points used: {NPTS} in {len(gal_res)} galaxies (points with any non-positive model or g_bar dropped from ALL models alike)")
stat = {}
for k in ("canonical", "alt"):
    stat[k] = {}
    for mn in ("ALG", "PD", "RMphi", "RMv"):
        res = np.concatenate([r["res"][k][mn] for r in gal_res])
        stat[k][mn] = dict(rms=wrms(res, W), mean=float(np.sum(W * res) / np.sum(W)))
    resr = np.concatenate([r["res_rotmod_ALG"][k] for r in gal_res])
    stat[k]["ALG_rotmod"] = dict(rms=wrms(resr, W), mean=float(np.sum(W * resr) / np.sum(W)))
    P(f"  a0 = {A0_SI[k]:.3g} ({k}): " + "  ".join(f"{mn} {stat[k][mn]['rms']:.4f} (mean {stat[k][mn]['mean']:+.3f})" for mn in ("ALG_rotmod", "ALG", "PD", "RMphi", "RMv")))
# free a0
fit = {}
for mn in ("ALG", "PD", "RMphi", "RMv"):
    rmsv = np.array([wrms(np.concatenate([r["res"][f"g{j}"][mn] for r in gal_res]), W) for j in range(len(a0_list))])
    j = int(np.argmin(rmsv))
    la = np.log10(A0_GRID_SI)
    if 0 < j < len(la) - 1:
        c = np.polyfit(la[j - 1:j + 2], rmsv[j - 1:j + 2], 2)
        lbest = -c[1] / (2 * c[0]); rbest = float(np.polyval(c, lbest))
    else:
        lbest, rbest = la[j], float(rmsv[j])
    a0b = 10 ** lbest
    fit[mn] = dict(a0=a0b, rms=rbest, kappa_canonical=0.5 * a0b / A0_SI["canonical"], kappa_alt=0.5 * a0b / A0_SI["alt"],
                   edge=bool(j in (0, len(la) - 1)), rms_curve=rmsv.tolist())
    P(f"  a0 free  {mn:<6}: a0 = {a0b:.3e}  rms = {rbest:.4f}  kappa_canonical = {fit[mn]['kappa_canonical']:.3f}  kappa_alt = {fit[mn]['kappa_alt']:.3f}"
      + ("  [GRID EDGE]" if fit[mn]["edge"] else ""))

# ------------------------------------------------------------------ verdict clauses
P("\n  SPARC rule: rms(RM) <= rms(PD) + 0.02 dex at canonical, alt and a0 free")
spar = {}
for rm in ("RMphi", "RMv"):
    cl = dict(canonical=stat["canonical"][rm]["rms"] - stat["canonical"]["PD"]["rms"],
              alt=stat["alt"][rm]["rms"] - stat["alt"]["PD"]["rms"],
              free=fit[rm]["rms"] - fit["PD"]["rms"])
    passes = {k: bool(v <= 0.02) for k, v in cl.items()}
    dla = math.log10(fit[rm]["a0"] / fit["PD"]["a0"])
    spar[rm] = dict(delta_rms=cl, passes=passes, all_pass=all(passes.values()), dlog_a0_vs_PD=dla, kappa_moves=bool(abs(dla) > 0.05))
    P(f"  {rm}: d rms canonical {cl['canonical']:+.4f}  alt {cl['alt']:+.4f}  free {cl['free']:+.4f}  -> {'PASS' if spar[rm]['all_pass'] else 'FAIL'};"
      f"  dlog a0_fit vs PD {dla:+.3f} dex{'  KAPPA MOVES' if abs(dla) > 0.05 else ''}")

# post-run variant V1 (added after the QUICK smoke run showed S1 at the 5% line): only points where the grid baryons
# reproduce rotmod's V_bar within 5%
P("\n  V1 (post-run variant, disclosed): only points whose grid V_bar matches rotmod within 5%")
MM = np.concatenate([r["match"] for r in gal_res]).astype(bool)
P(f"  points kept: {MM.sum()} of {len(MM)}")
v1 = {}
for k in ("canonical", "alt"):
    v1[k] = {mn: wrms(np.concatenate([r["res"][k][mn] for r in gal_res])[MM], W[MM]) for mn in ("ALG", "PD", "RMphi", "RMv")}
    P(f"  {k}: " + "  ".join(f"{mn} {v1[k][mn]:.4f}" for mn in ("ALG", "PD", "RMphi", "RMv")))
for mn in ("ALG", "PD", "RMphi", "RMv"):
    rmsv = np.array([wrms(np.concatenate([r["res"][f"g{j}"][mn] for r in gal_res])[MM], W[MM]) for j in range(len(a0_list))])
    j = int(np.argmin(rmsv)); la = np.log10(A0_GRID_SI)
    c = np.polyfit(la[max(j - 1, 0):j + 2], rmsv[max(j - 1, 0):j + 2], 2) if 0 < j < len(la) - 1 else None
    lb = -c[1] / (2 * c[0]) if c is not None else la[j]
    v1.setdefault("free", {})[mn] = dict(a0=10 ** lb, rms=float(np.polyval(c, lb)) if c is not None else float(rmsv[j]))
    P(f"  a0 free {mn:<6}: a0 = {10 ** lb:.3e}, rms {v1['free'][mn]['rms']:.4f}, kappa_canonical {0.5 * 10 ** lb / A0_SI['canonical']:.3f}, kappa_alt {0.5 * 10 ** lb / A0_SI['alt']:.3f}")
for rm in ("RMphi", "RMv"):
    d = [v1["canonical"][rm] - v1["canonical"]["PD"], v1["alt"][rm] - v1["alt"]["PD"], v1["free"][rm]["rms"] - v1["free"]["PD"]["rms"]]
    P(f"  V1 {rm}: d rms canonical {d[0]:+.4f} alt {d[1]:+.4f} free {d[2]:+.4f} -> {'PASS' if max(d) <= 0.02 else 'FAIL'}")
    v1[f"rule_{rm}"] = dict(d=d, passes=bool(max(d) <= 0.02))

# in-plane ratios
P("\n  median per-galaxy in-plane acceleration ratios (fixed footings):")
ratio_sum = {}
for k in ("canonical", "alt"):
    ratio_sum[k] = {key: float(np.nanmedian([r["ratio"][k][key] for r in gal_res])) for key in ("RMphi_over_PD", "RMv_over_PD", "PD_over_ALG")}
    P(f"  {k}: RMphi/PD {ratio_sum[k]['RMphi_over_PD']:.4f}   RMv/PD {ratio_sum[k]['RMv_over_PD']:.4f}   PD/ALG {ratio_sum[k]['PD_over_ALG']:.4f}")

# ------------------------------------------------------------------ Part 3
P("\n" + "=" * 110 + "\nPART 3: edge-on vertical structure, PD (phantom disc) vs RM (round), prediction only\n" + "=" * 110)
P("  ratios PD/RM: nu_z^2 (midplane vertical frequency^2, from K_z at 0.25 h_z) and K_z(h_z);")
P("  stellar sigma_z at fixed scale height ~ sqrt(K_z) -> ratio sqrt; HI thickness at fixed sigma_HI ~ 1/nu_z -> ratio RM/PD of h_HI = sqrt(nu_z2_PD/nu_z2_RM)")
part3 = {}
for k in ("canonical", "alt"):
    part3[k] = {}
    for lab in ("2Rd", "Rlast"):
        for grp, sel in (("all", lambda r: True), ("HSB", lambda r: r["SBd_at_Rd"] >= 100), ("LSB", lambda r: r["SBd_at_Rd"] < 100)):
            sub = [r for r in gal_res if sel(r)]
            if not sub:
                continue
            d = {}
            for rm in ("RMphi", "RMv"):
                nz = np.array([r["vert"][k][lab]["nuz2_PD"] / r["vert"][k][lab][f"nuz2_{rm}"] for r in sub])
                kh = np.array([r["vert"][k][lab]["Khz_PD"] / r["vert"][k][lab][f"Khz_{rm}"] for r in sub])
                d[rm] = dict(n=len(sub), nuz2_ratio_med=float(np.nanmedian(nz)), nuz2_ratio_p16=float(np.nanpercentile(nz, 16)),
                             nuz2_ratio_p84=float(np.nanpercentile(nz, 84)), sigz_ratio_med=float(np.nanmedian(np.sqrt(kh))),
                             hHI_RM_over_PD_med=float(np.nanmedian(np.sqrt(nz))))
            part3[k][f"{lab}_{grp}"] = d
            P(f"  {k:<9} R={lab:<5} {grp:<3} (n={len(sub):>3}): "
              + "  ".join(f"{rm}: nu_z^2 PD/RM {d[rm]['nuz2_ratio_med']:.2f} [{d[rm]['nuz2_ratio_p16']:.2f}-{d[rm]['nuz2_ratio_p84']:.2f}], "
                          f"sigma_z PD/RM {d[rm]['sigz_ratio_med']:.3f}, h_HI RM/PD {d[rm]['hHI_RM_over_PD_med']:.2f}" for rm in ("RMphi", "RMv")))

RES = dict(S5_MN_PD_over_ALG=S5, inner=INNER, V1=v1, n_gal=len(gal_res), n_pts=NPTS, fixed=stat, free=fit, sparc_rule=spar, ratios=ratio_sum, part3=part3,
           S1=dict(median=s1med, per_gal={r["name"]: r["S1"] for r in gal_res}),
           per_gal={r["name"]: dict(n=r["n"], Mb=r["Mb"], Mgas=r["Mgas"], ratio=r["ratio"], vert=r["vert"]) for r in gal_res},
           checks=[dict(ok=o, msg=m) for o, m in CHECKS], quick=QUICK)
P(f"\nchecks: {sum(o for o, _ in CHECKS)}/{len(CHECKS)} pass; runtime {time.time() - T0:.0f} s")


def jc(o):
    if isinstance(o, dict):
        return {k: jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jc(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    return o


tag = ("_QUICK" if QUICK else "") + ("_INNEREXP" if INNER == "exp" else "")
json.dump(jc(RES), open(os.path.join(HERE, f"cfg516_sparc_results{tag}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg516_sparc{tag}.out"), "w").write("\n".join(OUT) + "\n")
