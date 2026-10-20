"""CFG903 shared definitions (criteria: FROZEN_CRITERIA.md, bb665cf4f).  kappa = 1/2 FITTED; not theory closed.

Paths, the resource watchdog, CFG502's verbatim distance and patch helpers, CFG902's declared catchment fixed point, and the
histogram binning shared by the pair stage and the score stage.
"""
import math, os, resource, sys, threading, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg903_work")

# ---------------------------------------------------------------- watchdog (criteria: < 1.5 GB, < 15 min per process)
LIM_RSS, LIM_T = 1.45e9, 14.5 * 60
T0 = time.time()
def rss():                             # peak (includes file-backed FITS pages while a file is open), reported only
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == "darwin" else 1024)
def cur_rss():                         # current resident set (bytes), what the watchdog enforces
    import subprocess
    try:
        return float(subprocess.check_output(["ps", "-o", "rss=", "-p", str(os.getpid())]).decode().strip()) * 1024
    except Exception:
        return 0.0
PEAK_CUR = [0.0]
def start_watchdog(tag):
    def run():
        while True:
            c = cur_rss(); PEAK_CUR[0] = max(PEAK_CUR[0], c)
            if c > LIM_RSS or time.time() - T0 > LIM_T:
                sys.stderr.write(f"{tag} WATCHDOG: rss {c / 1e6:.0f} MB, t {time.time() - T0:.0f} s -> STOP\n"); os._exit(3)
            time.sleep(0.5)
    threading.Thread(target=run, daemon=True).start()

# ---------------------------------------------------------------- CFG502 verbatim helpers
c_SI = 2.998e8; Mpc_m = 3.0857e22; H0_SI = 70 * 1e3 / Mpc_m
def DC(z, n=2048):                     # lr_esd_remeasure.py / agentK / CFG502 verbatim (flat, Om 0.3, H0 70; comoving Mpc)
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_SI / H0_SI) / Mpc_m
    return np.interp(z, zz, chi)

NPATCH = 50
def patch_edges(ra, dec, npatch=NPATCH):   # agentK's assign_patches, returning its quantile edges
    south = dec < -15.0
    ra_u = np.where(south, (ra + 180.0) % 360.0, ra)
    edges = []
    for m in (~south, south):
        npr = npatch // 2
        q = np.quantile(ra_u[m], np.linspace(0, 1, npr + 1)); q[0] -= 1e-6; q[-1] += 1e-6
        edges.append(q)
    return edges
def apply_patches(ra, dec, edges, npatch=NPATCH):
    south = dec < -15.0
    ra_u = np.where(south, (ra + 180.0) % 360.0, ra)
    patch = np.zeros(len(ra), dtype=np.int64); off = 0
    for m, q in zip((~south, south), edges):
        npr = npatch // 2
        patch[m] = off + np.clip(np.searchsorted(q, ra_u[m], side='right') - 1, 0, npr - 1)
        off += npr
    return patch

def unitvec(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]

def fcold(logMs):                      # the record's cold-gas recipe (agentK / CFG502)
    return 10 ** (-0.69 * logMs + 6.63)

# ---------------------------------------------------------------- framework: CFG804 / CFG902 declared catchment
SUP = 5.364; FB = 1 / (1 + SUP); Gpc = 4.30091e-3
SHIFT_DEX = math.log10(0.674)          # CFG902 R1 (CFG416's declared Msun/h ramp)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
def a0_kms2pc(foot):
    return A0[foot] * 3.0857e16 / 1e6
def fret_of(lM):                       # CFG416 / CFG556 verbatim (as in cfg804.py)
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)
def N_of_declared(logMb):              # cfg804.py N_of with CFG902's R1 replacement
    f = 0.10
    for _ in range(200):
        lMta = logMb - math.log10(f * FB) + SHIFT_DEX; fn = fret_of(lMta)
        if abs(fn - f) < 1e-12: break
        f = 0.5 * (f + fn)
    return 1 / f
edge_of = lambda N: math.sqrt(((2 * SUP * N + 1) ** 2 - 1) / 4)
NGRID = np.round(np.concatenate([[1.0], np.arange(2.0, 10.01, 0.25)]), 2)          # cfg804.py
NGRID_NB = np.unique(np.concatenate([NGRID, [1.25, 1.5, 1.75]]))                  # criteria: neighbour shapes

# ---------------------------------------------------------------- histogram binning (criteria)
# d bins: index 0 = [0, 0.003) Mpc; index i = 1..239 = [0.03*10^((i-76)/75), 0.03*10^((i-75)/75)) Mpc; B21 edges at i = 76 + 10k
ND = 240
D_EDGES = np.concatenate([[0.0], 0.03 * 10 ** ((np.arange(1, ND + 1) - 76) / 75.0)])   # len ND+1; D_EDGES[1] = 0.003
D_MAX = float(D_EDGES[-1])                                                             # 4.61 Mpc
B21_EDGES = 0.03 * 10 ** (np.arange(16) * 2 / 15.0)
assert np.allclose(D_EDGES[76 + 10 * np.arange(16)], B21_EDGES)
def dbin_of(d):
    jj = np.floor(np.log10(np.maximum(d, 1e-12) / 0.03) * 75.0).astype(np.int64)
    return np.where(d < D_EDGES[1], 0, jj + 76)
NM, M_LO, M_DL = 120, 7.0, 0.05        # log M_b cells 7.00-13.00
M_CEN = M_LO + M_DL * (np.arange(NM) + 0.5)
def mbin_of(logMb):
    return np.clip(np.floor((logMb - M_LO) / M_DL).astype(np.int64), 0, NM - 1)
WEDGES = np.array([100.0, 200.0, 300.0, 500.0, 1000.0])  # |dchi| bins: [0,100) [100,200) [200,300) [300,500) [500,1000)
NW = 5
NCELL = ND * NM * 2 * NW * 2           # (d, m, flag less-massive, w, masked)
NCELL_JK = ND * NM * 2                  # jackknife: (d, m, flag) for |dchi| < 500, unmasked
VARIANTS = ["v0_primary_I0_B21_C1p", "v1_C0", "v2_C2p", "v3_uniform", "v4_I1", "v5_I2", "v6_I5", "v7_z017_diag"]
