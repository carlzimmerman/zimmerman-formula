#!/usr/bin/env python3
"""
LMC1 core module: the framework's Milky Way field, tracer sampling, the leapfrog integrator with and without
a rigid LMC, and the model observation. Imported by lmc1_design.py and lmc1.py (same folder).
Origins of copied code (copied, not imported; nothing outside this folder is executed):
  - baryon census M_parts / M_sph, nu_fw, g_model: closure_2026_11_12/RAW1_halo_stars_direct/raw1_model.py
    (itself copied from closure_2026_11_12/MWJ1_milky_way_joint_window/mwj1.py).
  - HEALPix ang2pix_ring: closure_2026_11_12/HOT1_hot_bin_localisation/hot1.py (general nside).
Units inside the integrator: kpc, Myr, kpc/Myr. 1 km/s = KMS kpc/Myr.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import math
import numpy as np
TRAPZ = getattr(np, "trapezoid", None) or np.trapz

# ------------------------------------------------------------------ constants (SI and integrator units)
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
MYR = 3.15576e13
KMS = 1.0e3 * MYR / KPC                     # km/s -> kpc/Myr  (1.02271e-3)
ACC = MYR ** 2 / KPC                         # m/s^2 -> kpc/Myr^2
G_INT = G * MSUN * MYR ** 2 / KPC ** 3       # kpc^3 / (Msun Myr^2)
PC = KPC / 1000.0; MSUN_PC2 = MSUN / PC ** 2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
MSTAR_CENSUS = 5.49e10
MSTAR_RC = {"canonical": 7.08e10, "alt": 6.42e10}

# ------------------------------------------------------------------ copied from raw1_model.py
MC = dict(thin =dict(S0=896.0*MSUN_PC2, Rd=2.50*KPC, zd=0.300*KPC, Rm=0.0, vert="exp"),
          thick=dict(S0=183.0*MSUN_PC2, Rd=3.02*KPC, zd=0.900*KPC, Rm=0.0, vert="exp"),
          HI   =dict(Sfid=10.0*MSUN_PC2, Rfid=8.33*KPC, Rd=7.00*KPC, zd=0.085*KPC, Rm=4.0*KPC,  vert="sech2"),
          H2   =dict(Sfid= 2.0*MSUN_PC2, Rfid=8.33*KPC, Rd=1.50*KPC, zd=0.045*KPC, Rm=12.0*KPC, vert="sech2"))
STARS = ("thin", "thick"); GAS = ("HI", "H2")
MBULGE, ABULGE = 9.23e9 * MSUN, 0.70 * KPC
def S0_of(c): return c["S0"] if "S0" in c else c["Sfid"] / math.exp(-c["Rm"] / c["Rfid"] - c["Rfid"] / c["Rd"])
def sigma_of_R(c, R):
    R = np.maximum(np.asarray(R, float), 1e-6 * KPC); return S0_of(c) * np.exp(-c.get("Rm", 0.0) / R - R / c["Rd"])
def zcum(c, n=1201):
    zg = np.linspace(-10 * c["zd"], 10 * c["zd"], n)
    zz = (np.exp(-np.abs(zg) / c["zd"]) / (2 * c["zd"]) if c["vert"] == "exp" else 1.0 / np.cosh(zg / (2 * c["zd"])) ** 2 / (4 * c["zd"]))
    cum = np.concatenate([[0.0], np.cumsum((zz[1:] + zz[:-1]) / 2 * np.diff(zg))]); return zg, cum / cum[-1]
_MS = {}
def M_parts(r_kpc):
    key = float(r_kpc)
    if key not in _MS:
        r = key * KPC; st = MBULGE * r ** 2 / (r + ABULGE) ** 2; gs = 0.0
        Rg = np.linspace(1e-4 * KPC, min(r, 60 * KPC), 4000); h = np.sqrt(np.maximum(r ** 2 - Rg ** 2, 0.0))
        for k, c in MC.items():
            zg, cum = zcum(c); m = float(TRAPZ(2 * np.pi * Rg * sigma_of_R(c, Rg) * np.interp(h, zg, cum), Rg))
            if k in STARS: st += m
            else: gs += m
        _MS[key] = (st, gs)
    return _MS[key]
def nu_fw(y): return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, float), 1e-14))))
RTAB = np.logspace(math.log10(0.5), math.log10(2.0e4), 700)
_TAB = None
def _tab():
    global _TAB
    if _TAB is None:
        st = np.array([M_parts(r)[0] if r <= 200 else np.nan for r in RTAB]); gs = np.array([M_parts(r)[1] if r <= 200 else np.nan for r in RTAB])
        last = np.where(RTAB <= 200)[0][-1]; st[last + 1:] = st[last]; gs[last + 1:] = gs[last]
        _TAB = (st, gs)
    return _TAB
def g_model(r_kpc, model, footing=None, a0_mult=1.0):
    """Radial acceleration (m/s^2). model in {'FW_census','FW_rc','N','flat200'} (raw1_model.g_model, NFW branch dropped)."""
    r = np.asarray(r_kpc, float); rm = r * KPC
    if model == "flat200": return (200e3) ** 2 / rm
    st, gs = _tab()
    Ms = np.interp(np.log(r), np.log(RTAB), st); Mg = np.interp(np.log(r), np.log(RTAB), gs)
    if model == "FW_rc": Ms = Ms * MSTAR_RC[footing] / MSTAR_CENSUS
    gb = G * (Ms + Mg) / rm ** 2
    if model == "N": return gb
    return nu_fw(gb / (A0[footing] * a0_mult)) * gb
def M_b(r_kpc):
    s, g = M_parts(r_kpc); return (s + g) / MSUN

# ------------------------------------------------------------------ fast field table (integrator units)
class Field:
    """Spherical field g(r) on a fine log grid; inside 0.5 kpc, g -> g(0.5) r / 0.5 (a harmonic core; the
    census bulge is not resolved below 0.5 kpc; the same core in every twin)."""
    def __init__(self, model, footing):
        self.model, self.footing = model, footing
        self.lr = np.linspace(math.log(0.5), math.log(2.0e4), 20001)
        self.g = g_model(np.exp(self.lr), model, footing) * ACC         # kpc/Myr^2
        self.lr0, self.dlr = self.lr[0], self.lr[1] - self.lr[0]
        # potential (for the energy check): Phi(r) = -int_r^Rmax g dr' (+ const)
        rr = np.exp(self.lr); seg = 0.5 * (self.g[1:] + self.g[:-1]) * np.diff(rr)
        self.phi = -np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    def g_of_r(self, r):
        lr = np.log(np.maximum(r, 0.5))
        out = np.interp(lr, self.lr, self.g)
        return np.where(r < 0.5, self.g[0] * r / 0.5, out)
    def phi_of_r(self, r):
        lr = np.log(np.maximum(r, 0.5))
        out = np.interp(lr, self.lr, self.phi)
        return np.where(r < 0.5, self.phi[0] - 0.5 * self.g[0] / 0.5 * (0.25 - r * r), out)
    def acc(self, x):
        r = np.sqrt(np.einsum("ij,ij->i", x, x))
        return -(self.g_of_r(r) / np.maximum(r, 1e-9))[:, None] * x

# ------------------------------------------------------------------ tracers
def tracer_n(r, a_in, a_out, rb):
    r = np.asarray(r, float); return np.where(r < rb, (r / rb) ** (-a_in), (r / rb) ** (-a_out))
def jeans_sr2(field, a_in, a_out, rb, beta, rgrid):
    """sigma_r^2 (kpc/Myr)^2 on rgrid for constant beta (spherical Jeans, outer boundary 2e4 kpc)."""
    rr = np.exp(field.lr); n = tracer_n(rr, a_in, a_out, rb); w = n * rr ** (2 * beta) * field.g
    seg = 0.5 * (w[1:] + w[:-1]) * np.diff(rr); cum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    s2 = cum / (n * rr ** (2 * beta))
    return np.interp(np.log(rgrid), field.lr, s2)
def sample_tracers(field, N, seed, a_in=2.0, a_out=5.0, rb=20.0, rmin=2.0, rmax=400.0, beta=0.6):
    rng = np.random.default_rng(seed)
    rg = np.logspace(math.log10(rmin), math.log10(rmax), 20001)
    pdf = tracer_n(rg, a_in, a_out, rb) * rg ** 2
    cdf = np.concatenate([[0.0], np.cumsum(0.5 * (pdf[1:] + pdf[:-1]) * np.diff(rg))]); cdf /= cdf[-1]
    r = np.interp(rng.random(N), cdf, rg)
    cth = rng.uniform(-1, 1, N); ph = rng.uniform(0, 2 * np.pi, N); sth = np.sqrt(1 - cth ** 2)
    rh = np.vstack([sth * np.cos(ph), sth * np.sin(ph), cth]).T
    th = np.vstack([cth * np.cos(ph), cth * np.sin(ph), -sth]).T; phh = np.vstack([-np.sin(ph), np.cos(ph), np.zeros(N)]).T
    sr = np.sqrt(jeans_sr2(field, a_in, a_out, rb, beta, r)); st = math.sqrt(1 - beta) * sr
    v = rng.normal(0, 1, N)[:, None] * sr[:, None] * rh + rng.normal(0, 1, N)[:, None] * st[:, None] * th \
        + rng.normal(0, 1, N)[:, None] * st[:, None] * phh
    return r[:, None] * rh, v

# ------------------------------------------------------------------ the LMC pull (rigid Plummer body, mass M_eff)
EPS_LMC = 5.0   # kpc, Plummer softening (frozen)
def lmc_pull(x, xl, M):
    """acceleration on points x from a Plummer body of mass M (Msun) at xl."""
    d = xl[None, :] - x; s2 = np.einsum("ij,ij->i", d, d) + EPS_LMC ** 2
    return (G_INT * M) * d / (s2 * np.sqrt(s2))[:, None]
def mw_reflex(xl, M):
    """the Milky Way centre's acceleration toward the LMC at xl (same Plummer law at the centre)."""
    s2 = float(xl @ xl) + EPS_LMC ** 2
    return (G_INT * M) * xl / (s2 * math.sqrt(s2))

def lmc_track(field, x0, v0, M, T, dt, nsub=20, friction=False):
    """Integrate the LMC (relative to the MW centre) backward from today for T Myr; return positions at
    t = -T, -T+dt, ..., 0 (array (nT+1, 3), index k <-> t = -T + k dt) and the velocities.
    Relative equation: d'' = -g_MW(|d|) d_hat - a_MW(d) (MW centre accelerates toward the LMC)."""
    nT = int(round(T / dt)); h = -dt / nsub
    x = np.array(x0, float); v = np.array(v0, float)
    def a(x): return field.acc(x[None])[0] - mw_reflex(x, M)
    X = [x.copy()]; V = [v.copy()]
    for k in range(nT):
        for _ in range(nsub):
            v = v + 0.5 * h * a(x); x = x + h * v; v = v + 0.5 * h * a(x)
        X.append(x.copy()); V.append(v.copy())
    return np.array(X[::-1]), np.array(V[::-1])

def integrate(field, x, v, dt, nsteps, track=None, M=0.0, k0=0, snaps=(), snap_fn=None):
    """Kick-drift-kick leapfrog in the MW-centred frame. With track: star acceleration
    = MW field + LMC pull - MW centre acceleration, LMC at track[k] at step k (k from k0).
    With track None: MW field only (a separate code path; the zero-mass twin uses the LMC path)."""
    x = x.copy(); v = v.copy(); out = {}
    def acc(x, k):
        a = field.acc(x)
        if track is not None:
            xl = track[k]; a = a + (lmc_pull(x, xl, M) - mw_reflex(xl, M)[None, :])
        return a
    a = acc(x, k0)
    for s in range(nsteps):
        if s in snaps and snap_fn is not None: out[s] = snap_fn(x, v)
        v = v + 0.5 * dt * a; x = x + dt * v
        a = acc(x, k0 + s + 1); v = v + 0.5 * dt * a
    if nsteps in snaps and snap_fn is not None: out[nsteps] = snap_fn(x, v)
    return x, v, out

# ------------------------------------------------------------------ observation
BINS = [(20.0, 30.0), (30.0, 40.0), (40.0, 55.0), (55.0, 80.0)]
def ang2pix_ring(nside, theta, phi):
    theta = np.asarray(theta, float); phi = np.mod(np.asarray(phi, float), 2 * np.pi)
    z = np.cos(theta); za = np.abs(z); tt = phi / (0.5 * np.pi)
    npix = 12 * nside * nside; ncap = 2 * nside * (nside - 1)
    pix = np.empty(z.shape, dtype=np.int64)
    eq = za <= 2.0 / 3.0
    t1 = nside * (0.5 + tt[eq]); t2 = nside * z[eq] * 0.75
    jp = np.floor(t1 - t2).astype(np.int64); jm = np.floor(t1 + t2).astype(np.int64)
    ir = nside + 1 + jp - jm; kshift = 1 - (ir & 1)
    ip = (jp + jm - nside + kshift + 1) // 2; ip = np.mod(ip, 4 * nside)
    pix[eq] = ncap + (ir - 1) * 4 * nside + ip
    po = ~eq
    tp = tt[po] - np.floor(tt[po]); tmp = nside * np.sqrt(3 * (1 - za[po]))
    jp = np.floor(tp * tmp).astype(np.int64); jm = np.floor((1 - tp) * tmp).astype(np.int64)
    ir = jp + jm + 1; ip = np.floor(tt[po] * ir).astype(np.int64); ip = np.mod(ip, 4 * ir)
    pix[po] = np.where(z[po] > 0, 2 * ir * (ir - 1) + ip, npix - 2 * ir * (ir + 1) + ip)
    return pix
def pix_of_dir(n, nside=4):
    """n: unit vectors from the Sun in Galactocentric axes (x toward the centre, y toward l = 90, z north)."""
    lon = np.arctan2(n[:, 1], n[:, 0]); lat = np.arcsin(np.clip(n[:, 2], -1, 1))
    return ang2pix_ring(nside, 0.5 * np.pi - lat, lon)
def observe(x, v, p0):
    """Galactocentric r, unit vector from the Sun, and v_gsr (velocity relative to the MW centre, projected)."""
    r = np.sqrt(np.einsum("ij,ij->i", x, x)); dd = x - p0[None, :]
    n = dd / np.sqrt(np.einsum("ij,ij->i", dd, dd))[:, None]
    return r, n, np.einsum("ij,ij->i", v, n) / KMS
def dipole_fit(vlos, n):
    A = np.hstack([np.ones((len(vlos), 1)), n]); co, *_ = np.linalg.lstsq(A, vlos, rcond=None)
    d = co[1:]; amp = float(np.linalg.norm(d))
    return dict(mono=float(co[0]), vec=d.tolist(), amp=amp, l=math.degrees(math.atan2(d[1], d[0])) % 360,
                b=math.degrees(math.asin(d[2] / amp)) if amp > 0 else 0.0)

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
