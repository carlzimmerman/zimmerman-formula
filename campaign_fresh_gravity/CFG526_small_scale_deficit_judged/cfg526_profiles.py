#!/usr/bin/env python3
"""CFG526 question A (FROZEN_CRITERIA.md): engine gravitating M(<r) vs candidate B's law profile M_b + phantom, built from the run's own baryons.
Stage 1 (`compute`, heavy, cached in _external_data/cfg526_work): for each run, load the saved z = 0 positions, call the engine's own `forces`
(diag = True, imported unchanged) once, capture the total potential exactly from the three acceleration transforms, build rho_grav, rho_p,
rho_b,ret, rho_b,all, rho_in (MIX-A filtered retained baryons), select halos, and store discrete-ball enclosed masses.
Stage 2 (default): K1-K3, R = M_grav/M_law, D ratios vs the matched S0, convergence, verdict per footing, MUTATE M1.
CFG526_MUTATE=1: M2 (cells within 1.5 cells of each scored centre emptied in the DC-can L50/L25 gravitating fields) -> _MUTATE outputs, exit 1 = detected.
Usage: python3 cfg526_profiles.py compute [run ...] ;  python3 cfg526_profiles.py ;  CFG526_MUTATE=1 python3 cfg526_profiles.py"""
import os, sys, json, math, time, importlib.util
NTH = 4
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = str(NTH)
import numpy as np
from scipy import fft as sfft, ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
WORK = os.path.join(EXT, "cfg526_work"); os.makedirs(WORK, exist_ok=True)
MUT = os.environ.get("CFG526_MUTATE", "0") == "1"
NP = 256; RPROF = [1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0]; NKEEP = 100; NCAND = 6000
G_SI = 6.674e-11; MSUN = 1.989e30; MPC = 3.0856775814913673e22

E521 = os.path.join(CFG, "CFG521_small_box_galaxy_regime", "cfg521_pm.py")
E524 = os.path.join(CFG, "CFG524_reservoir_only_draw", "cfg524_pm.py")
W521, W524, W518, W359 = (os.path.join(EXT, d) for d in ("cfg521_work", "cfg524_work", "cfg518_work", "cfg359_work"))

def t521(sw, L, foot="canonical", mode="census", nocomp=False):
    tag = f"{sw}_TA{'_NOCOMP' if nocomp else ''}_MIXA_MASSCONS_fret{mode}_FLAT_{foot}_N256" + (f"_L{L}" if L != 200 else "")
    return os.path.join(W521, f"cfg521_{tag}")
def t524(dr, L, foot="canonical", mode="census"):
    return os.path.join(W524, f"cfg524_RES_TA_MIXA_MASSCONS_fret{mode}_FLAT_{foot}_N256" + (f"_L{L}" if L != 200 else "") + f"_draw{dr}")

# name: (L, engine, env prefix, extra env, switch, foot, base path)
RUNS = {}
for L in (50, 25):
    RUNS[f"S0_L{L}"] = (L, E521, "CFG521", {}, "S0", "canonical", t521("S0", L))
    RUNS[f"DCcan_L{L}"] = (L, E521, "CFG521", {}, "RES", "canonical", t521("RES", L))
    RUNS[f"DCalt_L{L}"] = (L, E521, "CFG521", {}, "RES", "alt", t521("RES", L, "alt"))
    RUNS[f"K1_L{L}"] = (L, E521, "CFG521", {"FRET_MODE": "one"}, "RES", "canonical", t521("RES", L, mode="one"))
    RUNS[f"NOCOMP_L{L}"] = (L, E521, "CFG521", {"NOCOMP": "1"}, "RES", "canonical", t521("RES", L, nocomp=True))
    RUNS[f"R2can_L{L}"] = (L, E524, "CFG524", {"DRAW": "R2"}, "RES", "canonical", t524("R2", L))
    RUNS[f"R2alt_L{L}"] = (L, E524, "CFG524", {"DRAW": "R2"}, "RES", "alt", t524("R2", L, "alt"))
RUNS["S0_L100"] = (100, E521, "CFG521", {}, "S0", "canonical", t521("S0", 100))
RUNS["DCcan_L100"] = (100, E521, "CFG521", {}, "RES", "canonical", t521("RES", 100))
RUNS["S0_L200"] = (200, E521, "CFG521", {}, "S0", "canonical", os.path.join(W359, "cfg359_S0_FLAT_canonical_N256"))
RUNS["DCcan_L200"] = (200, E521, "CFG521", {}, "RES", "canonical", os.path.join(W518, "cfg518_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256"))
RUNS["DCalt_L200"] = (200, E521, "CFG521", {}, "RES", "alt", os.path.join(W518, "cfg518_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_alt_N256"))
ORDER = ["S0_L50", "DCcan_L50", "DCalt_L50", "K1_L50", "NOCOMP_L50", "R2can_L50", "R2alt_L50",
         "S0_L25", "DCcan_L25", "DCalt_L25", "K1_L25", "NOCOMP_L25", "R2can_L25", "R2alt_L25",
         "S0_L100", "DCcan_L100", "S0_L200", "DCcan_L200", "DCalt_L200"]

def load_engine(name):
    L, path, pre, extra, sw, foot, base = RUNS[name]
    env = {f"{pre}_L": f"{L:g}", f"{pre}_RMIN": str(2 * L / 256 if L != 200 else 1.56), f"{pre}_THREADS": str(NTH),
           f"{pre}_NSEED": "256", f"{pre}_FRET_MODE": "census", f"{pre}_NOCOMP": "0", f"{pre}_MUTATE": "0"}
    env.update({f"{pre}_{k}": v for k, v in extra.items()})
    for k in list(os.environ):
        if k.startswith(pre + "_"): del os.environ[k]
    os.environ.update(env)
    spec = importlib.util.spec_from_file_location(f"eng_{name}", path); mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.RC = 0.0; mod.MIX = "MIXA"; mod.NTH = NTH
    return mod

def ball(M, R):
    g = np.arange(M); g = np.minimum(g, M - g).astype(np.float32)
    b = ((g[:, None, None] ** 2 + g[None, :, None] ** 2 + g[None, None, :] ** 2) <= R * R + 1e-6).astype(np.float32)
    return b, int(b.sum())

def compute(name):
    out = os.path.join(WORK, f"cfg526_{name}.npz")
    if os.path.exists(out):
        print("cached", name); return
    t0 = time.time()
    L, path, pre, extra, sw, foot, base = RUNS[name]
    mod = load_engine(name)
    pos = np.load(base + "_z0.npz")["pos"].astype(np.float64)
    js = json.load(open(base + ".json"))["snap"]["z0"]
    mesh = mod.Mesh(NP); dta = mod.dta_table()
    delta = mesh.deposit(pos); npart = pos.shape[0]; del pos
    rec = []
    inv0 = mesh.inv
    def inv_rec(xk):
        rec.append(xk);  del rec[:-3]
        return inv0(xk)
    mesh.inv = inv_rec
    _, info = mod.forces(mesh, delta, 1.0, sw, "FLAT", foot, dta, diag=True)
    mesh.inv = inv0
    info.pop("_grids", None)
    num = sum(kv * x for kv, x in zip(mesh.kvec, rec)); del rec          # = 1j k^2 phik
    dgk = (-num / (1j * 1.5 * mod.Om)).astype(np.complex64); del num   # -k^2 phik a / (1.5 Om), a = 1
    dgk[0, 0, 0] = 0
    dgrav = mesh.inv(dgk); del dgk
    k2 = None
    # K checks
    K = {}
    shared = {}
    for k_, v in info.items():
        if k_ in js and isinstance(v, (int, float)) and not isinstance(v, bool) and k_ != "t":
            shared[k_] = [float(v), float(js[k_])]
    K["shared"] = shared
    K["s0_maxdiff_rel"] = float(np.abs(dgrav - delta).max() / (1.0 + float(delta.max())))
    K["mean_grav_minus_p"] = float((dgrav - delta).mean())
    kb, pb, s8 = mod.measure_pk(mesh, delta, npart)
    kg, pg, s8g = mod.measure_pk(mesh, dgrav, npart)
    K["pk_z0_check"] = float(np.max(np.abs(np.array(pb) / np.array(js["P"]) - 1)))
    rho_p = (1.0 + delta).astype(np.float32); rho_g = (1.0 + dgrav).astype(np.float32); del dgrav, delta
    fret = mod._INC.get("fret") if sw != "S0" else None
    if fret is None: fret = np.ones_like(rho_p)
    FB = mod.FB
    rbret = (fret * FB * rho_p).astype(np.float32)
    kk = mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2
    kJ = lambda T: math.sqrt(1.5 * mod.Om) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
    fc, fh, fs = mod.MIXES["MIXA"]
    Wk = (fc / (1.0 + kk / kJ(1e4) ** 2) + fh / (1.0 + kk / kJ(1e6) ** 2) + fs).astype(np.float32); del kk
    rin = mesh.inv(mesh.fwd(rbret) * Wk); del Wk
    dx = L / NP
    # peaks and r_ON
    mx = ndimage.maximum_filter(rho_p, size=3, mode="wrap"); pk = np.argwhere(rho_p == mx); del mx
    pk = pk[np.argsort(rho_p[pk[:, 0], pk[:, 1], pk[:, 2]])[::-1][:NCAND]]
    ii = (pk[:, 0], pk[:, 1], pk[:, 2])
    Rg = np.geomspace(dx, 8.0, 14)
    rpk = mesh.fwd(rho_p)
    ok = np.ones(len(pk), bool); ron = np.zeros(len(pk))
    for R in Rg:
        b, nb = ball(NP, R / dx)
        mean = mesh.inv(rpk * mesh.fwd(b))[ii] / nb
        ok &= mean >= js["Delta_ta"]; ron[ok] = R
    # profiles at candidate centres
    prof = {}
    nball = []
    fk = {"p": rpk, "g": mesh.fwd(rho_g), "bret": mesh.fwd(rbret), "in": mesh.fwd(rin)}
    for R in RPROF:
        b, nb = ball(NP, R); nball.append(nb); bk = mesh.fwd(b)
        for f, xk in fk.items():
            prof.setdefault(f, []).append(mesh.inv(xk * bk)[ii])
    prof = {f: np.array(v).T for f, v in prof.items()}            # (ncand, nR), units of mean-density cells
    # M2 mutation: emptied cores in the gravitating field (all candidates' top-100 scored set decided later; store per-candidate emptied sums
    # for the first 300 kept-candidate centres to cover the scored set)
    np.savez_compressed(out, pk=pk, ron=ron, rho_at=rho_p[ii], fret_at=fret[ii], nball=np.array(nball), dx=dx, L=L, Om=mod.Om, FB=FB,
                        Delta_ta=js["Delta_ta"], foot=foot, sw=sw, **{f"M_{f}": v for f, v in prof.items()},
                        K=json.dumps(K), info=json.dumps({k: v for k, v in info.items() if not isinstance(v, (dict, list))}),
                        kgrav=np.array(kg), pgrav=np.array(pg), ppart=np.array(pb), s8g=s8g, s8=s8)
    # keep the gravitating field and S0 field for later matched / mutated evaluations
    np.save(os.path.join(WORK, f"cfg526_{name}_rhog.npy"), rho_g.astype(np.float32))
    if sw == "S0":
        np.save(os.path.join(WORK, f"cfg526_{name}_rhop.npy"), rho_p.astype(np.float32))
    print(f"done {name} {time.time() - t0:.0f}s K={json.dumps({k: v for k, v in K.items() if k != 'shared'})}", flush=True)

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "compute":
    try: os.nice(10)
    except OSError: pass
    for n in (sys.argv[2:] or ORDER):
        compute(n)
    sys.exit(0)

# ============================================================== stage 2: analysis and verdict
LINES = []
def P(s=""):
    print(s); LINES.append(s)
_S0F = {}
def s0_fields(L):
    if L not in _S0F:
        rho = np.load(os.path.join(WORK, f"cfg526_S0_L{L}_rhop.npy"))
        rk = sfft.rfftn(rho, workers=NTH); fl = []
        for R in RPROF:
            b, _ = ball(NP, R); fl.append(sfft.irfftn(rk * sfft.rfftn(b, workers=NTH), s=rho.shape, workers=NTH).astype(np.float32))
        _S0F.clear(); _S0F[L] = (rho, fl)
    return _S0F[L]
def s0_match(L, pk):
    rho, fl = s0_fields(L); out = np.zeros((len(pk), len(RPROF)))
    off = np.array([(a, b, c) for a in range(-2, 3) for b in range(-2, 3) for c in range(-2, 3)])
    for n, p in enumerate(pk):
        cc = (p[None, :] + off) % NP; j = int(np.argmax(rho[cc[:, 0], cc[:, 1], cc[:, 2]])); c = cc[j]
        out[n] = [f[c[0], c[1], c[2]] for f in fl]
    return out
def emptied_grav(name, pk, dx):
    rho = np.load(os.path.join(WORK, f"cfg526_{name}_rhog.npy"))
    rr = np.arange(-2, 3)
    for p in pk:
        for a in rr:
            for b in rr:
                for c in rr:
                    if a * a + b * b + c * c <= 1.5 ** 2 + 1e-6:
                        rho[(p[0] + a) % NP, (p[1] + b) % NP, (p[2] + c) % NP] = 0.0
    rk = sfft.rfftn(rho, workers=NTH); out = []
    for R in RPROF:
        b, _ = ball(NP, R)
        f = sfft.irfftn(rk * sfft.rfftn(b, workers=NTH), s=rho.shape, workers=NTH)
        out.append(f[pk[:, 0], pk[:, 1], pk[:, 2]])
    return np.array(out).T

def analyse(name, mutate_core=False):
    L, path, pre, extra, sw, foot, base = RUNS[name]
    d = np.load(os.path.join(WORK, f"cfg526_{name}.npz"))
    mod = load_engine(name)
    dx = float(d["dx"]); Om = float(d["Om"]); FB = float(d["FB"]); Dta = float(d["Delta_ta"])
    Mcell = Om * 2.775e11 * dx ** 3                                   # Msun/h per mean-density cell
    a0 = mod.A0[foot]; rmin = 2 * L / 256 if L != 200 else 1.56
    pk, ron = d["pk"], d["ron"]
    keep = []; kept_xyz = []; kept_r = []
    for n in range(len(pk)):
        if ron[n] < rmin - 1e-9:
            continue
        x = pk[n] * dx
        if kept_xyz:
            dd = np.abs(np.array(kept_xyz) - x); dd = np.minimum(dd, L - dd); dist = np.sqrt((dd ** 2).sum(1))
            if np.any(dist < np.array(kept_r)):
                continue
        kept_xyz.append(x); kept_r.append(ron[n]); keep.append(n)
    hosts = np.array(keep)
    lM = np.array([math.log10(mod.M_ta(ron[n], Dta)) for n in hosts])
    re = np.array([mod.x_supply(ron[n], Dta, 1.0, "FLAT", foot) * ron[n] for n in hosts])
    sc = re >= 1.5 * dx
    sel = hosts[sc][:NKEEP]; lM = lM[sc][:NKEEP]; re = re[sc][:NKEEP]
    res = {"name": name, "L": L, "foot": foot, "n_hosts": int(len(hosts)), "n_scored_avail": int(sc.sum()), "n_scored": int(len(sel))}
    if len(sel) == 0:
        return res, None
    nb = d["nball"]; reff = (3 * nb / (4 * math.pi)) ** (1 / 3) * dx      # Mpc/h
    Mp = d["M_p"][sel] * Mcell; Mg = d["M_g"][sel] * Mcell; Mbr = d["M_bret"][sel] * Mcell; Min = d["M_in"][sel] * Mcell
    if mutate_core:
        Mg = emptied_grav(name, pk[sel], dx) * Mcell
    Mba = FB * Mp
    h = 0.6736
    def nu_of(Mb):
        g = G_SI * (Mb / h) * MSUN / ((reff[None, :] / h * MPC) ** 2)
        return mod.nu_mono(g / a0)
    Mlaw = Mba + (nu_of(Mbr) - 1.0) * Mbr
    Mlaw_noexp = nu_of(Mbr) * Mbr
    Mlaw_in = Mba + (nu_of(Min) - 1.0) * Min
    Ms0 = s0_match(L, pk[sel]) * Mcell
    scored = reff[None, :] <= re[:, None] + 1e-9
    # r_M from M_b,ret(<r_e) (log-log interpolation over the profile radii, clipped to the range)
    rM = np.zeros(len(sel))
    for i in range(len(sel)):
        Mbe = math.exp(np.interp(math.log(min(max(re[i], reff[0]), reff[-1])), np.log(reff), np.log(np.maximum(Mbr[i], 1e-30))))
        rM[i] = math.sqrt(G_SI * Mbe / h * MSUN / a0) / MPC * h            # Mpc/h
    R = Mg / Mlaw
    def med(a, m):
        v = a[m]; return [float(np.median(v)), float(np.percentile(v, 16)), float(np.percentile(v, 84))] if v.size else None
    per = []
    for j, Rc in enumerate(RPROF):
        m = scored[:, j]; ma = np.ones(len(sel), bool)
        per.append({"R_cells": Rc, "r_eff": float(reff[j]), "n": int(m.sum()),
                    "R": med(R[:, j], m), "R_noexp": med((Mg / Mlaw_noexp)[:, j], m), "R_in": med((Mg / Mlaw_in)[:, j], m),
                    "D_eng": med((Mg / Ms0)[:, j], m), "D_part": med((Mp / Ms0)[:, j], m), "D_law": med((Mlaw / Ms0)[:, j], m),
                    "r_over_rM": med(reff[j] / rM, m), "Mp_over_Mlaw": med((Mp / Mlaw)[:, j], m),
                    "all_R": med(R[:, j], ma), "all_D_eng": med((Mg / Ms0)[:, j], ma), "all_D_law": med((Mlaw / Ms0)[:, j], ma)})
    core = scored & (np.array(RPROF)[None, :] <= 2.0)
    res.update(per=per, lM_range=[float(lM.min()), float(lM.max())], re_cells_med=float(np.median(re / dx)),
               rM_med=float(np.median(rM)),
               core={"n": int(core.sum()), "R": med(R, core), "R_noexp": med(Mg / Mlaw_noexp, core), "R_in": med(Mg / Mlaw_in, core),
                     "D_eng": med(Mg / Ms0, core), "D_part": med(Mp / Ms0, core), "D_law": med(Mlaw / Ms0, core)})
    K = json.loads(str(d["K"]))
    res["K"] = K
    halos = {"lM": lM, "R": R, "scored": scored, "reff": reff}
    return res, halos

def kcheck(name, res):
    K = res["K"]; sh = K["shared"]; ok = True; why = []
    if RUNS[name][4] == "S0":
        ok = K["s0_maxdiff_rel"] <= 1e-4; why.append(f"K2 S0 maxdiff {K['s0_maxdiff_rel']:.2e}")
    else:
        for k_ in ("e_sum", "q_max"):
            if k_ in sh:
                a, b = sh[k_]; r_ = abs(a - b) / max(abs(b), 1e-30); ok &= r_ <= 1e-3; why.append(f"{k_} rel {r_:.1e}")
        if "n_catch" in sh:
            ok &= sh["n_catch"][0] == sh["n_catch"][1]; why.append(f"n_catch {sh['n_catch'][0]:.0f}/{sh['n_catch'][1]:.0f}")
        if "src_sum" in sh and "e_sum" in sh:
            dd = abs(sh["src_sum"][0] - sh["src_sum"][1]); ok &= dd <= 1e-6 * sh["e_sum"][1]; why.append(f"src_sum |d| {dd:.1e}")
        rest = [abs(a - b) / max(abs(b), 1e-12) for k_, (a, b) in sh.items() if k_ not in ("e_sum", "q_max", "n_catch", "src_sum")]
        mr = max(rest) if rest else 0.0; ok &= mr <= 1e-3; why.append(f"other shared diag max rel {mr:.1e} ({len(rest)} keys)")
    k3 = abs(K["mean_grav_minus_p"]) <= 1e-6; ok &= k3; why.append(f"K3 mean(grav-p) {K['mean_grav_minus_p']:.1e}")
    return bool(ok), "; ".join(why)

def conv_stat(h50, h25):
    out = []
    for j50, j25 in ((0, 2), (2, 4), (3, 5), (4, 6)):          # L50 1,2,3,4 cells  <->  L25 2,4,6,8 cells
        m50 = h50["scored"][:, j50] & (h50["lM"] >= 12.7) & (h50["lM"] <= 14.3)
        m25 = h25["scored"][:, j25] & (h25["lM"] >= 12.7) & (h25["lM"] <= 14.3)
        if m50.sum() >= 10 and m25.sum() >= 10:
            a = float(np.median(np.log10(h50["R"][m50, j50]))); b = float(np.median(np.log10(h25["R"][m25, j25])))
            out.append({"r_phys": float(h50["reff"][j50]), "n50": int(m50.sum()), "n25": int(m25.sum()), "logR50": a, "logR25": b, "d": b - a})
        else:
            out.append({"r_phys": float(h50["reff"][j50]), "n50": int(m50.sum()), "n25": int(m25.sum()), "skip": True})
    used = [c for c in out if not c.get("skip")]
    return out, (bool(used) and all(abs(c["d"]) <= 0.1 for c in used))

def verdict(r50, r25, k_ok, conv_ok):
    if not k_ok:
        return "NOT DIAGNOSTIC", "integrity check failed"
    if r50["n_scored"] < 20 and r25["n_scored"] < 20:
        return "NOT DIAGNOSTIC", "fewer than 20 scored halos in both boxes"
    c50, c25 = r50["core"], r25["core"]
    t = 10 ** -0.1
    if c50["R"][0] < t and c25["R"][0] < t:
        return "ENGINE ARTEFACT", f"core R {c50['R'][0]:.3f} / {c25['R'][0]:.3f} < 10^-0.1 in both boxes"
    if c50["D_law"][0] >= 1 and c25["D_law"][0] >= 1 and c50["D_eng"][0] < 10 ** -0.05 and c25["D_eng"][0] < 10 ** -0.05:
        return "ENGINE ARTEFACT", "law needs no central deficit vs S0 but the engine has one"
    match = all(abs(math.log10(p["R"][0])) <= 0.1 for r in (r50, r25) for p in r["per"] if p["R"] is not None)
    if match and conv_ok and c50["D_law"][0] < 1 and c25["D_law"][0] < 1:
        return "LAW-REQUIRED", "engine matches the law within 0.1 dex at every scored radius, converged, law less concentrated than S0"
    why = []
    if not match: why.append("engine departs from the law by > 0.1 dex at some scored radius")
    if not conv_ok: why.append("run-vs-law ratio not converged L50 -> L25")
    if not (c50["D_law"][0] < 1 and c25["D_law"][0] < 1): why.append("law core not below S0 in both boxes")
    return "MIXED", "; ".join(why)

def fmt(m):
    return "   -   " if m is None else f"{m[0]:.3f} [{m[1]:.2f},{m[2]:.2f}]"

def main():
    A = {}; H = {}; KOK = {}
    P("CFG526 A: engine gravitating M(<r) vs candidate B's law profile (M_b,all + (nu - 1) M_b,ret, nu_mono, own baryons), z = 0, 256^3 seed 359")
    P("kappa = 1/2 FITTED; footings never pooled; a0 flat; cold energy MASS still required; not theory closed.")
    P("R = M_grav/M_law (scored radii r_eff <= census edge r_e); D = M/M_S0 (matched S0 peak within +-2 cells); median [16, 84].")
    if MUT: P("*** MUTATE M2: gravitating field emptied within 1.5 cells of each scored centre (DC-can L50 / L25) ***")
    for name in ORDER:
        if not os.path.exists(os.path.join(WORK, f"cfg526_{name}.npz")):
            P(f"\n{name}: MISSING"); continue
        if RUNS[name][4] == "S0":
            d = np.load(os.path.join(WORK, f"cfg526_{name}.npz")); res = {"K": json.loads(str(d["K"])), "name": name}
            ok, why = kcheck(name, res); KOK[name] = ok; A[name] = {"K_ok": ok, "K": why}
            P(f"\n{name}: integrity {'PASS' if ok else 'FAIL'} ({why})"); continue
        mc = MUT and name in ("DCcan_L50", "DCcan_L25")
        res, h = analyse(name, mutate_core=mc)
        ok, why = kcheck(name, res); KOK[name] = ok; res["K_ok"] = ok; res["K_why"] = why
        A[name] = res; H[name] = h
        P(f"\n{name}  (L = {res['L']}, cell {res['L'] / NP:.3f} Mpc/h, {res['foot']})  integrity {'PASS' if ok else 'FAIL'}: {why}")
        P(f"  hosts {res['n_hosts']}, scored available {res['n_scored_avail']}, used {res['n_scored']}")
        if h is None: continue
        P(f"  log M_ta {res['lM_range'][0]:.2f}-{res['lM_range'][1]:.2f}; median census edge {res['re_cells_med']:.2f} cells; median r_M {res['rM_med']:.4f} Mpc/h")
        P("   R(cells) r_eff   n   R=Mgrav/Mlaw          R_noexp  R_in     D_eng   D_part  D_law   r/r_M    Mp/Mlaw")
        for p in res["per"]:
            if p["n"] == 0:
                P(f"   {p['R_cells']:4.1f} {p['r_eff']:.3f} {p['n']:4d}   (beyond edge; all-halo R {p['all_R'][0]:.3f}, D_eng {p['all_D_eng'][0]:.3f}, D_law {p['all_D_law'][0]:.3f})")
                continue
            P(f"   {p['R_cells']:4.1f} {p['r_eff']:.3f} {p['n']:4d}   {fmt(p['R'])}  {p['R_noexp'][0]:.3f}    {p['R_in'][0]:.3f}    "
              f"{p['D_eng'][0]:.3f}   {p['D_part'][0]:.3f}   {p['D_law'][0]:.3f}   {p['r_over_rM'][0]:6.1f}   {p['Mp_over_Mlaw'][0]:.2f}")
        c = res["core"]
        P(f"  CORE (scored, <= 2 cells, n = {c['n']}): R {fmt(c['R'])}; R_noexp {c['R_noexp'][0]:.3f}; R_in {c['R_in'][0]:.3f}; "
          f"D_eng {c['D_eng'][0]:.3f}; D_part {c['D_part'][0]:.3f}; D_law {c['D_law'][0]:.3f}")
    P("\nConvergence (median log10 R at shared physical radii, log M_ta 12.7-14.3):")
    V = {}
    for foot, tag in (("canonical", "DCcan"), ("alt", "DCalt")):
        n50, n25 = f"{tag}_L50", f"{tag}_L25"
        cs, cok = conv_stat(H[n50], H[n25])
        for c in cs:
            P(f"  {foot:9s} r = {c['r_phys']:.3f}: " + ("skipped (n50 %d, n25 %d)" % (c["n50"], c["n25"]) if c.get("skip")
              else f"L50 {c['logR50']:+.3f} (n {c['n50']})  L25 {c['logR25']:+.3f} (n {c['n25']})  diff {c['d']:+.3f}"))
        k_ok = KOK[n50] and KOK[n25] and KOK["S0_L50"] and KOK["S0_L25"]
        v, why = verdict(A[n50], A[n25], k_ok, cok)
        V[foot] = {"verdict": v, "why": why, "converged": cok, "conv": cs,
                   "core_R": [A[n50]["core"]["R"][0], A[n25]["core"]["R"][0]], "core_D_law": [A[n50]["core"]["D_law"][0], A[n25]["core"]["D_law"][0]],
                   "core_D_eng": [A[n50]["core"]["D_eng"][0], A[n25]["core"]["D_eng"][0]]}
    m1 = {}
    for L in (50, 25):
        m1[L] = [A[f"NOCOMP_L{L}"]["core"]["R"][0], A[f"DCcan_L{L}"]["core"]["R"][0]]
    m1_ok = all(a > b for a, b in m1.values())
    P(f"\nMUTATE M1 (NOCOMP core R must exceed DC-can core R): L50 {m1[50][0]:.3f} vs {m1[50][1]:.3f}; L25 {m1[25][0]:.3f} vs {m1[25][1]:.3f} -> "
      f"{'DETECTED (test has teeth)' if m1_ok else 'NOT DETECTED -> A downgraded to NOT DIAGNOSTIC'}")
    if not m1_ok and not MUT:
        for f in V: V[f]["verdict"] = "NOT DIAGNOSTIC"; V[f]["why"] += "; M1 not detected"
    P("")
    for f in V:
        P(f"VERDICT A [{f}]: {V[f]['verdict']} -- {V[f]['why']}")
    sfx = "_MUTATE" if MUT else ""
    open(os.path.join(HERE, f"cfg526_profiles{sfx}.out"), "w").write("\n".join(LINES) + "\n")
    json.dump({"runs": A, "verdict": V, "M1": {"L50": m1[50], "L25": m1[25], "detected": m1_ok}, "mutate_M2": MUT},
              open(os.path.join(HERE, f"cfg526_profiles{sfx}.json"), "w"), indent=1)
    if MUT:
        det = V["canonical"]["verdict"] == "ENGINE ARTEFACT"
        P(f"MUTATE M2: {'DETECTED' if det else 'NOT DETECTED'}")
        open(os.path.join(HERE, f"cfg526_profiles{sfx}.out"), "a").write(f"MUTATE M2: {'DETECTED' if det else 'NOT DETECTED'}\n")
        sys.exit(1 if det else 0)

if __name__ == "__main__":
    main()
