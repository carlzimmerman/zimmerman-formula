#!/usr/bin/env python3
"""CFG937 -- two-floor primordial halos (H-CF2): the atomic-cooling floor (CFG934) for systems quenched at reionization and a
post-reionization filtering floor for systems that kept forming stars.
Criteria: FROZEN_CRITERIA.md (73144fddb, committed alone before this script existed).

H-CF2: a quenched system (Weisz+14 tau90 at the 12.59-Gyr first node) sits in at least M_cool(z_f), the halo with T_vir = 1e4 K
(CFG934); a late former (tau90 below the node; SPARC; every CFG934 group default) sits in at least max(M_cool, M_filt), where
M_filt is the halo whose virial velocity reaches V_th = sqrt(2) c_s(T_IGM), mu 0.59 (CFG782's retention condition T_vir >= T_IGM),
T_IGM in {1, 1.5, 2} x 1e4 K.  Everything else is CFG934's, reused by exec'ing cfg934.py read-only up to its K section.
Corners mu x tau x C x T_IGM = 36 per footing and reading; readings (S) sum [primary] and (M) max [alternative].

Run (one core, one process):  CFG937_MODE=K|MUTATE_EQ|MUTATE_T10|SEAL|main OMP_NUM_THREADS=1 nice -n 10 python3 cfg937.py
K must pass first (MUTATE / SEAL / main read cfg937_results_K.json).  Each mode writes its own outputs.  RSS guard 900 MB.
kappa = 1/2 FITTED; the footings are never pooled; cold energy, not a particle; not theory closed."""
import os, sys, io, math, json, time, contextlib, builtins, resource, hashlib
import numpy as np
import scipy.integrate, scipy.optimize                                # imported before the read-only exec (no import-time writes)
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MODE = os.environ.get("CFG937_MODE", "main"); assert MODE in ("K", "MUTATE_EQ", "MUTATE_T10", "SEAL", "main"), MODE
SUF = {"K": "_K", "MUTATE_EQ": "_MUTATE_EQ", "MUTATE_T10": "_MUTATE_T10", "SEAL": "_SEAL", "main": ""}[MODE]
TRUE_OPEN = builtins.open
OUT = []; CHECKS = []; T0W = time.time(); RSS_CAP_MB = 900.0


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss_mb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e6 if sys.platform == "darwin" else r / 1e3


def guard(tag=""):
    if rss_mb() > RSS_CAP_MB:
        P(f"  RSS GUARD: peak {rss_mb():.0f} MB > {RSS_CAP_MB:.0f} MB at {tag}; aborting (no outputs written)")
        sys.exit(3)


def check(name, ok, detail):
    CHECKS.append(dict(name=name, ok=bool(ok), detail=detail)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}"); return bool(ok)


def sha256(path):
    return hashlib.sha256(TRUE_OPEN(path, "rb").read()).hexdigest()


def ro_open(file, mode="r", *a, **k):
    if any(ch in mode for ch in "wax+"):
        raise PermissionError(f"CFG937: write refused inside exec'd code ({os.path.basename(str(file))})")
    return TRUE_OPEN(file, mode, *a, **k)


# =====================================================================================================================  CFG934 definitions (read-only exec)
SRC934 = os.path.join(LANES, "CFG934_cooling_floor_halos", "cfg934.py")
MARK934 = "# =====================================================================================================================  K\n"
os.environ["CFG934_MODE"] = "main"
_src = TRUE_OPEN(SRC934).read()
g = {"__file__": SRC934, "__name__": "cfg934_defs"}
builtins.open = ro_open
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(_src[:_src.index(MARK934)], "cfg934", "exec"), g)
finally:
    builtins.open = TRUE_OPEN
assert g["TFAC"] == 1.0 and g["TV"] == 1.0e4
P(__doc__.split("Run (one core")[0].strip())
P(f"\n  MODE {MODE}; CFG934 definitions exec'd read-only (cfg934.py sha256 {sha256(SRC934)[:16]}...); {time.time() - T0W:.1f} s, {rss_mb():.0f} MB")

for _k in ("tau_of", "zf_of_tau", "get_halo", "mcool", "KB", "MP", "GS", "MSUN_C", "KPC_M", "T0", "t_of_z", "z_of_t", "Z_ONSET",
           "all_classes", "verdict", "lab", "lab_S", "CLASSES", "SEV", "FOOTS", "A0X", "A0H", "FBN", "FB42", "SAMPLES", "UL", "I874",
           "SAMP880", "PRE880", "WZT", "GDEF", "LDEF", "GRP_MEM", "R24", "R42", "R45", "U_stat", "CL_stat", "halo_K", "sparc_rows",
           "S_stat", "halo_mass", "nfw_DM", "L_parts", "ephan", "ns880", "R933", "fnum", "grp_of_host", "jclean", "fmt_cls", "J",
           "G880", "MS880", "PC880", "nu880", "read_tsv", "NAMEMAP", "T6", "WZ", "norm", "delta_vir", "rhom"):
    globals()[_k] = g[_k]

R934 = J("CFG934_cooling_floor_halos", "cfg934_results.json")
CAP = 10 ** 10.1 / 1e9                                                # the Weisz+14 first node (12.589 Gyr)
T_COOL = 1.0e4
MU_F = 0.59
TIGM = (1.0e4, 1.5e4, 2.0e4)
MUS, TKS, CS = (0.59, 1.22), ("t50", "t90"), (1500, 3000, 6000)
CK36 = [(mu, tk, C, T) for mu in MUS for tk in TKS for C in CS for T in TIGM]


def ck36(c):
    return f"mu{c[0]}|{c[1]}|C{c[2]}|T{c[3]:.1e}"


def ck12(c):
    return f"mu{c[0]}|{c[1]}|C{c[2]}"


# =====================================================================================================================  H-CF2: selector + floor (criteria 2.2-2.4)
def has_gas(kind, obj):
    if kind == "sat":
        return obj["MHI"] > 0
    if kind == "iso":
        return obj["lHI"] is not None
    if kind == "lvd":
        return PRE880[obj["name"]]["lHI"] is not None
    return True


def status_of(nm, MV, grp, kind, obj, sel, deflt):
    """'Q' quenched at reionization / 'L' kept forming stars after it (criteria 2.3; variants V7 t50, V8 own, V11 all)."""
    if sel == "off":
        return "Q"
    if kind == "sparc" or sel == "all":
        return "L"
    t50, t90, src = tau_of(nm, MV, grp, deflt)
    if sel == "t90":
        return "Q" if t90 >= CAP - 1e-9 else "L"
    if sel == "t50":
        return "Q" if t50 >= CAP - 1e-9 else "L"
    if sel == "own":
        if src == "Weisz+14" and t90 < CAP - 1e-9:
            return "L"
        return "L" if has_gas(kind, obj) else "Q"
    raise ValueError(sel)


def floor_halo(zf, mu, C, st, Tigm, m2=2, eds=False, zcoll=None, eq=False):
    """Q: M_cool(z_f; 1e4 K, mu).  L: max(M_cool, M_filt) with V_th^2 = m2 k T_IGM/(0.59 m_p) = 2 k T_eff/(0.59 m_p).
    eq (MUTATE_EQ): the filtering floor's parameters are replaced by the cooling floor's (T 1e4 K, the corner's mu)."""
    Hc = get_halo(zf, mu, C, T_COOL, eds, zcoll)
    if st == "Q":
        return Hc
    muf, Teff = (mu, T_COOL) if eq else (MU_F, m2 * Tigm / 2.0)
    Hf = get_halo(zf, muf, C, Teff, eds, zcoll)
    return Hf if Hf.M > Hc.M else Hc


ONSET = g["Z_ONSET"]


def hcf2(mu, tk, C, Tigm, sel="t90", m2=2, eds=False, onset=False, deflt="group", eq=False):
    zc = ONSET if onset else None

    def for_obj(nm, MV, grp, kind, obj):
        t50, t90, _ = tau_of(nm, MV, grp, deflt)
        zf = zf_of_tau(t50 if tk == "t50" else t90)
        H = floor_halo(zf, mu, C, status_of(nm, MV, grp, kind, obj, sel, deflt), Tigm, m2, eds, zc, eq)
        return H.M, H.enc

    def sparc(_Ms):
        H = floor_halo(0.0, mu, C, status_of("", 0.0, "field", "sparc", None, sel, deflt), Tigm, m2, eds, zc, eq)
        return H.M, H.enc
    return dict(sat=lambda d: for_obj(d["name"], d["MV"], "sat", "sat", d),
                iso=lambda r: for_obj(r["name"], r["MV"], grp_of_host(r.get("host")), "iso", r),
                lvd=lambda d: for_obj(d["name"], d["MV"], grp_of_host(d.get("host")), "lvd", d),
                sparc=sparc)


def run_grid(readings=("S", "M"), corners=CK36, tfac=1.0, tag="", **kw):
    G = {}
    for reading in readings:
        G[reading] = {}
        for foot in FOOTS:
            G[reading][foot] = {}
            for c in corners:
                t1 = time.time()
                H = hcf2(c[0], c[1], c[2], c[3] * tfac, **kw)
                key = ck36((c[0], c[1], c[2], c[3] * tfac))
                G[reading][foot][key] = all_classes(foot, reading, H)
                guard(f"{tag} {reading} {foot} {key}")
                if tag:
                    P(f"  ({reading}) {foot:9s} {key:26s}: " + fmt_cls(G[reading][foot][key]) + f"  [{time.time() - t1:.1f} s, {rss_mb():.0f} MB]")
    return G


def cmp(a, b, path="", tol=1e-12, out=None):
    """recursive comparison of a (this lane, jclean'd) against b (committed JSON)."""
    out = out if out is not None else {"max": 0.0, "bad": [], "n": 0}
    if isinstance(b, dict):
        if not isinstance(a, dict) or set(a) != set(b):
            out["bad"].append(f"{path}: keys differ"); return out
        for k in b:
            cmp(a[k], b[k], f"{path}/{k}", tol, out)
    elif isinstance(b, list):
        if not isinstance(a, list) or len(a) != len(b):
            out["bad"].append(f"{path}: length differs"); return out
        for i, (x, y) in enumerate(zip(a, b)):
            cmp(x, y, f"{path}[{i}]", tol, out)
    elif b is None or isinstance(b, (bool, str)):
        if a != b:
            out["bad"].append(f"{path}: {a!r} vs {b!r}")
    else:
        if isinstance(a, bool) or not isinstance(a, (int, float)):
            out["bad"].append(f"{path}: type {type(a).__name__}"); return out
        d = abs(a - b); out["max"] = max(out["max"], d); out["n"] += 1
        if d > tol:
            out["bad"].append(f"{path}: {a!r} vs {b!r}")
    return out


def bare_law():
    NOH = dict(sat=None, iso=None, lvd=None, sparc=lambda Ms: (1.0, lambda r: 0.0))
    B = {}
    for foot in FOOTS:
        B[foot] = all_classes(foot, "L", NOH)
        B[foot]["S"] = S_stat(sparc_rows(foot, A0X[foot], "S", lambda Ms: (1e-30, lambda r: 0.0), FBN))
        B[foot]["S"]["label"] = lab_S(B[foot]["S"]["frac"])
    return B


def variant_grid(base, Hfun, corners, ups_IL=2.0, reuse_sat=False):
    grid = {}
    for f in FOOTS:
        grid[f] = {}
        for c in corners:
            k = c[0]
            grid[f][k] = all_classes(f, "S", Hfun(c[1]), ups_IL=ups_IL, skip_sat=(base[f][k] if reuse_sat else None))
            guard(f"variant {f} {k}")
    return grid


def v4_grid(base, lo, hi):
    g4 = {}
    for f in FOOTS:
        g4[f] = {}
        for k in base[f]:
            res = dict(base[f][k])
            for c in ("I", "L"):
                fl = 0.5 * abs(hi[f][k][c]["stat"] - lo[f][k][c]["stat"]); e = math.sqrt(base[f][k][c]["err"] ** 2 + fl ** 2)
                res[c] = dict(base[f][k][c], err=e, z=base[f][k][c]["stat"] / e, ups_floor=fl); res[c]["label"] = lab(res[c]["z"])
            g4[f][k] = res
    return g4


def E_syn(MV, r12_pc, Mg, lHI, foot, reading, halo_tuple, ups=2.0):
    """CFG880's L estimator for one (possibly synthetic) dwarf: returns (boost = 0.5 ln(sigma_pred^2/sigma_law^2), f_ex)."""
    a0 = A0X[foot]; fb = FBN
    r12 = r12_pc * PC880; Ms = ups * 10 ** (0.4 * (4.83 - MV))
    gN = G880 * (Ms / 2 + Mg) * MS880 / r12 ** 2
    sN2 = gN * r12 / 3 / 1e6; sl2 = float(gN * nu880(gN / a0)) * r12 / 3 / 1e6
    Mc, enc = halo_tuple; fex = 0.0
    add = G880 * (1 - fb) * float(enc(r12_pc / 1000.0)) * MS880 / (3 * r12) / 1e6
    if reading == "S":
        Mb_e = Ms + (1.33 * 10 ** lHI if lHI is not None else 0.0)
        fex = max(0.0, 1.0 - ephan(Mb_e, foot) / ((1 - fb) * Mc)); s2 = sl2 + fex * add
    else:
        s2 = sN2 + max(sl2 - sN2, add)
    return 0.5 * math.log(s2 / sl2), fex


RES = dict(lane="CFG937", criteria="73144fddb", mode=MODE, cfg934_sha256=sha256(SRC934), T_IGM=list(TIGM), m2=2, mu_f=MU_F, cap_Gyr=CAP)


def finish(code, json_name=None):
    RES["checks"] = CHECKS; RES["runtime_s"] = time.time() - T0W; RES["peak_rss_mb"] = rss_mb(); RES["exit_code"] = code
    P(f"\n  runtime {RES['runtime_s']:.0f} s, peak RSS {RES['peak_rss_mb']:.0f} MB, exit {code}")
    jn = json_name or f"cfg937_results{SUF}.json"
    with TRUE_OPEN(os.path.join(HERE, jn), "w") as fh:
        json.dump(jclean(RES), fh, indent=1)
    with TRUE_OPEN(os.path.join(HERE, f"cfg937{SUF}.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    sys.exit(code)


# =====================================================================================================================  K
if MODE == "K":
    P("\n" + "=" * 118 + "\nK TESTS (criteria section 5)\n" + "=" * 118)
    KOK = []
    # ---- K0
    k0 = json.load(TRUE_OPEN(os.path.join(LANES, "CFG934_cooling_floor_halos", "cfg934_results_K.json")))
    KOK.append(check("K0 CFG934's committed K passed; cfg934.py sha256 printed", k0.get("K_all") is True,
                     f"cfg934_results_K.json K_all {k0.get('K_all')}; cfg934.py sha256 {sha256(SRC934)}"))
    # ---- K1 / K1b: CFG42 and CFG45 (CFG934's K1 / K1b replayed through the inherited estimator)
    dmax = 0.0; nk = 0; t1 = time.time()
    for foot in FOOTS:
        a0 = A0H[foot]
        for rule in (False, True):
            u = U_stat(foot, a0, "S" if rule else "L", halo_K(), FB42, floors=rule); ref = R42["UF"][f"{foot}|{'rule' if rule else 'law'}"]
            for k in ("km", "err", "f_ups", "f_mh", "tot", "z"):
                dmax = max(dmax, abs(u[k] - ref[k])); nk += 1
            for key in ("cls", "col", "m31"):
                c = CL_stat(key, foot, a0, "S" if rule else "L", halo_K(), FB42, floors=rule); ref = R42["CL"][f"{key}|{foot}|{'rule' if rule else 'law'}"]
                for k in ("med", "tot", "z"):
                    dmax = max(dmax, abs(c[k] - ref[k])); nk += 1
    h4 = S_stat(sparc_rows("canonical", A0H["canonical"], "S", lambda Ms: (float(halo_mass(Ms)), lambda r, M=float(halo_mass(Ms)): float(nfw_DM(M, r))), FB42))
    h4d = max(abs(h4["n"] - R42["H4"]["n"]), abs(h4["nfex"] - R42["H4"]["nfex"]), abs(h4["frac"] - R42["H4"]["frac"]), abs(h4["max"] - R42["H4"]["max"]))
    KOK.append(check("K1 CFG42 H1/H2/H4 reproduced through the inherited estimator with CFG42's own inputs (1e-9)", dmax <= 1e-9 and h4d <= 1e-9,
                     f"{nk} UF/CL numbers, max |d| {dmax:.1e}; H4 n {h4['n']} nfex {h4['nfex']} frac {h4['frac']:.3f} max {h4['max']:.3f} (|d| {h4d:.1e}) [{time.time() - t1:.0f} s]"))
    dmax = 0.0; nk = 0
    for foot in FOOTS:
        a0 = A0H[foot]
        u = U_stat(foot, a0, "M", halo_K(), FB42, floors=True); ref = R45["UF"][f"{foot}|M"]
        for k in ("km", "z"):
            dmax = max(dmax, abs(u[k] - ref[k])); nk += 1
        for key in ("cls", "col", "m31"):
            c = CL_stat(key, foot, a0, "M", halo_K(), FB42, floors=True); ref = R45["CL"][f"{key}|{foot}|M"]
            for k in ("med", "z"):
                dmax = max(dmax, abs(c[k] - ref[k])); nk += 1
    sm = S_stat(sparc_rows("canonical", A0X["canonical"], "M", lambda Ms: (float(halo_mass(Ms)), lambda r, M=float(halo_mass(Ms)): float(nfw_DM(M, r))), FB42))
    refm = R45["SPARC"]["dwarf|M"]; smd = max(abs(sm["frac"] - refm["frac_lt003"]), abs(sm["max"] - refm["max"]))
    KOK.append(check("K1b CFG45 (M) reading reproduced (UF km/z, CL med/z, SPARC dwarf|M frac/max) (1e-6)", dmax <= 1e-6 and smd <= 1e-6,
                     f"{nk} UF/CL numbers max |d| {dmax:.1e}; SPARC M frac {sm['frac']:.4f} max {sm['max']:.4f} (|d| {smd:.1e})"))
    # ---- K2: CFG934 with the second floor switched off
    t1 = time.time()
    C12 = [(mu, tk, C, 1.0e4) for mu in MUS for tk in TKS for C in CS]
    OFF = run_grid(corners=C12, sel="off")
    nb = 0; mx = 0.0; bad = []
    for reading in ("S", "M"):
        for foot in FOOTS:
            for c in C12:
                o = cmp(jclean(OFF[reading][foot][ck36(c)]), R934["corners"][reading][foot][ck12(c)])
                mx = max(mx, o["max"]); nb += o["n"]; bad += [f"{reading}|{foot}|{ck12(c)}{b}" for b in o["bad"]]
    BARE = bare_law(); ob = cmp(jclean(BARE), R934["bare_law"]); mx = max(mx, ob["max"]); nb += ob["n"]; bad += ob["bad"]
    vS = verdict({f: {ck12(c): OFF["S"][f][ck36(c)] for c in C12} for f in FOOTS})[0]
    vM = verdict({f: {ck12(c): OFF["M"][f][ck36(c)] for c in C12} for f in FOOTS})[0]
    # CFG934's six variants with the second floor off
    base = {f: {ck12(c): OFF["S"][f][ck36(c)] for c in C12} for f in FOOTS}
    CL12 = [(ck12(c), c) for c in C12]
    vg = {}
    vg["V1 Delta_vir = 18 pi^2"] = variant_grid(base, lambda c: hcf2(c[0], c[1], c[2], c[3], sel="off", eds=True), CL12)
    vg["V2 onset z_coll (13.3 Gyr)"] = variant_grid(base, lambda c: hcf2(c[0], c[1], c[2], c[3], sel="off", onset=True), CL12)
    vg["V3 Upsilon_V 1 for I and L"] = variant_grid(base, lambda c: hcf2(c[0], c[1], c[2], c[3], sel="off"), CL12, ups_IL=1.0, reuse_sat=True)
    vg["V3 Upsilon_V 4 for I and L"] = variant_grid(base, lambda c: hcf2(c[0], c[1], c[2], c[3], sel="off"), CL12, ups_IL=4.0, reuse_sat=True)
    vg["V4 uniform recipe (Ups floor on I, L)"] = v4_grid(base, vg["V3 Upsilon_V 1 for I and L"], vg["V3 Upsilon_V 4 for I and L"])
    vg["V5 Upsilon_SFH (CFG827) for I and L"] = variant_grid(base, lambda c: hcf2(c[0], c[1], c[2], c[3], sel="off"), CL12, ups_IL="SFH", reuse_sat=True)
    vg["V6 luminosity-class tau default"] = variant_grid(base, lambda c: hcf2(c[0], c[1], c[2], c[3], sel="off", deflt="lum"), CL12)
    vbad = []; vmx = 0.0
    for name, grd in vg.items():
        ref = R934["variants"][name]
        if verdict(grd)[0] != ref["verdict"]:
            vbad.append(f"{name}: {verdict(grd)[0]} vs {ref['verdict']}")
        st = {f: {k: {c: [grd[f][k][c].get("stat"), grd[f][k][c].get("z")] for c in CLASSES if c != "S"} for k in grd[f]} for f in FOOTS}
        o = cmp(jclean(st), ref["stats"]); vmx = max(vmx, o["max"]); vbad += [f"{name}{b}" for b in o["bad"]]
    KOK.append(check("K2 CFG934 reproduced with the second floor switched off: corners (S, M) + bare law to 1e-12, labels, verdicts, six variants",
                     not bad and mx <= 1e-12 and vS == R934["verdict_S"] and vM == R934["verdict_M"] and not vbad and vmx <= 1e-12,
                     f"{nb} numbers, max |d| {mx:.1e}, {len(bad)} mismatches{(': ' + '; '.join(bad[:4])) if bad else ''}; verdicts S '{vS}' / M '{vM}' "
                     f"(CFG934 '{R934['verdict_S']}' / '{R934['verdict_M']}'); variants max |d| {vmx:.1e}, {len(vbad)} mismatches "
                     f"[{time.time() - t1:.0f} s]"))
    # ---- K3: record IGM quantities (CFG782)
    KB782, MP782 = 1.380649e-23, 1.6726e-27
    vth = {T: math.sqrt(2 * KB * T / (MU_F * MP)) / 1e3 for T in TIGM}
    v782 = {T: math.sqrt(2) * math.sqrt(KB782 * T / (0.59 * MP782)) / 1e3 for T in TIGM}
    printed = {1.0e4: 16.73, 1.5e4: 20.49, 2.0e4: 23.66}
    r1 = max(abs(vth[T] / v782[T] - 1) for T in TIGM); r2 = max(abs(vth[T] - printed[T]) for T in TIGM)
    ex = max(abs(get_halo(z, MU_F, 3000, 1.0e4).M - mcool(z, 0.59, T_COOL)[0]) for z in (0.0, 1.0, 3.0, 5.0))
    vv = []
    for z in (0.0, 2.0, 4.96):
        for T in TIGM:
            M_, r_, _ = mcool(z, MU_F, 2 * T / 2.0)
            vv.append(abs(math.sqrt(GS * M_ * MSUN_C / (r_ * KPC_M)) / 1e3 / vth[T] - 1))
    KOK.append(check("K3 V_th = sqrt(2) c_s(T_IGM) vs CFG782 (formula 1e-5 rel; printed 0.005 km/s); M_filt(1e4) == M_cool(mu 0.59); V_vir(M_filt) = V_th (1e-10)",
                     r1 <= 1e-5 and r2 <= 0.005 and ex == 0.0 and max(vv) <= 1e-10,
                     f"V_th " + " / ".join(f"{vth[T]:.4f}" for T in TIGM) + f" km/s; vs CFG782 formula max rel {r1:.1e}; vs printed max {r2:.4f}; "
                     f"M_filt-M_cool max |d| {ex:.1e}; V_vir identity {max(vv):.1e}"))
    # ---- K4: selector inputs
    dt = 0.0; nt = 0
    for nm, r in R24.items():
        if nm in WZT:
            dt = max(dt, abs(WZT[nm][1] - r["tau90"])); nt += 1
    F1 = {}
    for r in read_tsv(os.path.join(WZ, "table5.tsv")):
        nm = r["ID"]; key = NAMEMAP.get(nm, nm)
        if key in F1:
            continue
        F1[key] = fnum(T6.get(nm, r)["f10.1"])
    mism = [k for k in WZT if (WZT[k][1] >= CAP - 1e-9) != (F1[k] is not None and F1[k] >= 0.9)]
    lb6, lb8 = T0 - t_of_z(6.0), T0 - t_of_z(8.0)
    KOK.append(check("K4 selector tau90 = CFG824's (1e-12); 'tau90 at node' <=> f(12.59 Gyr) >= 0.9 for every Weisz object; lookback(z 6, 8) > 12.589 Gyr",
                     dt <= 1e-12 and nt == len(R24) and not mism and lb6 > CAP and lb8 > CAP,
                     f"{nt}/{len(R24)} CFG824 objects, max |d tau90| {dt:.1e}; {len(WZT)} Weisz objects, mismatches {mism}; lookback z6 {lb6:.3f}, z8 {lb8:.3f} Gyr "
                     f"vs node {CAP:.3f} (z_reion inert)"))
    # ---- K5: synthetic estimator == L_parts
    k5 = 0.0
    for reading in ("S", "M"):
        for foot in FOOTS:
            Hl = hcf2(0.59, "t50", 3000, 1.5e4)["lvd"]
            _, _, fx, boost, _ = L_parts(foot, A0X[foot], reading, Hl, FBN)
            for i, d in enumerate(SAMP880):
                q = PRE880[d["name"]]
                b, f_ = E_syn(q["MV"], q["r12"], q["Mg"], q["lHI"], foot, reading, Hl(d))
                k5 = max(k5, abs(b - boost[i]), abs(f_ - fx[i]))
    KOK.append(check("K5 the seal's synthetic estimator equals the L class estimator (boost, f_ex) for the real 83 (1e-12), both readings and footings",
                     k5 <= 1e-12, f"max |d| {k5:.1e}"))
    RES["K_all"] = all(KOK)
    P(f"\n  K-stage {'ALL PASS' if RES['K_all'] else 'FAILED'}")
    finish(0 if RES["K_all"] else 2)

# =====================================================================================================================  MUTATE / SEAL / main need K
KJ = os.path.join(HERE, "cfg937_results_K.json")
if not (os.path.exists(KJ) and json.load(TRUE_OPEN(KJ)).get("K_all") is True):
    P("  K has not passed (cfg937_results_K.json): per criteria section 5 the lane stops; no class is reported."); RES["class"] = None; finish(2)

# =====================================================================================================================  MUTATE
if MODE.startswith("MUTATE"):
    P("\n" + "=" * 118 + f"\nMUTATE {MODE} (criteria section 5)\n" + "=" * 118)
    if MODE == "MUTATE_EQ":
        GR = run_grid(tag="EQ", eq=True)
        mx = 0.0; bad = []; nb = 0
        for reading in ("S", "M"):
            for foot in FOOTS:
                for c in CK36:
                    o = cmp(jclean(GR[reading][foot][ck36(c)]), R934["corners"][reading][foot][ck12(c)])
                    mx = max(mx, o["max"]); nb += o["n"]; bad += [f"{reading}|{foot}|{ck36(c)}{b}" for b in o["bad"]]
        ok = check("MUTATE_EQ: filtering floor := cooling floor reproduces CFG934 at all 36 corners (every class number 1e-12, labels), both readings and footings",
                   not bad and mx <= 1e-12, f"{nb} numbers, max |d| {mx:.1e}, {len(bad)} mismatches{(': ' + '; '.join(bad[:6])) if bad else ''}")
    else:
        GR = run_grid(tag="T10", readings=("S",), tfac=10.0)
        bad = []; signonly = []
        for f in FOOTS:
            for ck, res in GR["S"][f].items():
                cells = [(c, res[c]) for c in ("U", "C", "I", "L")] + [(f"M-{s}", res["M"][s]) for s in ("collins", "lvd")]
                for c, r in cells:
                    if not (r["stat"] < 0 and r["z"] <= -2):
                        bad.append(f"{f} {ck} {c} {r['stat']:+.3f} ({r['z']:+.2f})")
                        if r["stat"] < 0:
                            signonly.append(f"{f} {ck} {c}")
                if res["S"]["label"] == "CONSISTENT":
                    bad.append(f"{f} {ck} S frac {res['S']['frac']:.2f}")
        ok = check("MUTATE_T10: T_IGM x 10 over-predicts every class at every corner on both footings (U, C, M both, I, L: stat < 0 and z <= -2; S not CONSISTENT)",
                   not bad, f"{len(bad)} failing cells of {len(GR['S']['canonical']) * 2 * 7}; of these, {len(signonly)} have the right sign (stat < 0) but z > -2"
                   + (": " + "; ".join(bad[:14]) if bad else ""))
        RES["T10_failing_cells"] = bad
        byc = {}
        for b in bad:
            c = b.split()[2]; byc[c] = byc.get(c, 0) + 1
        P(f"  failing cells by class: {byc}")
        RES["T10_failing_by_class"] = byc
    RES["corners"] = GR; RES["mutate_ok"] = ok
    vS = verdict(GR["S"])[0]; RES["verdict_S"] = vS
    P(f"\n  (MUTATE run, no verdict weight) H-CF2 (S) verdict as computed: {vS}")
    finish(0 if ok else 1)

# =====================================================================================================================  SEAL (criteria section 6)
if MODE == "SEAL":
    P("\n" + "=" * 118 + "\nSEALED PREDICTION P937 (model only; synthetic grid; no sigma data read for this class)\n" + "=" * 118)
    late = [(nm, t50, t90) for ms in GRP_MEM.values() for (nm, t50, t90) in ms if t50 < CAP - 1e-9]
    T50L, T90L = float(np.median([m[1] for m in late])), float(np.median([m[2] for m in late]))
    zQ = zf_of_tau(CAP); zL = {"t50": zf_of_tau(T50L), "t90": zf_of_tau(T90L)}
    P(f"  templates: Q tau50 = tau90 = {CAP:.3f} Gyr (z_f {zQ:.3f}); Lm tau50 {T50L:.3f} / tau90 {T90L:.3f} Gyr (z_f {zL['t50']:.3f} / {zL['t90']:.3f}), "
      f"medians over {len(late)} Weisz+14 objects with an LVD row and tau50 < node")
    MVG = [-5.0, -6.0, -7.0, -8.0, -9.0, -10.0, -11.0]; RHG = [100.0, 200.0, 300.0, 500.0]
    BINS = {"M_V > -7.7": [-5.0, -6.0, -7.0], "-10 < M_V <= -7.7": [-8.0, -9.0], "M_V <= -10": [-10.0, -11.0]}
    SEALT = {}
    for foot in FOOTS:
        for reading in ("S", "M"):
            per_corner = {}
            for c in CK36:
                mu, tk, C, T = c
                HQ = floor_halo(zQ, mu, C, "Q", T); HL = floor_halo(zL[tk], mu, C, "L", T)
                cell = {}
                for MV in MVG:
                    for rh in RHG:
                        eq_, fq = E_syn(MV, 4.0 / 3.0 * rh, 0.0, None, foot, reading, (HQ.M, HQ.enc))
                        el_, fl = E_syn(MV, 4.0 / 3.0 * rh, 0.0, None, foot, reading, (HL.M, HL.enc))
                        cell[f"{MV:+.0f}|{rh:.0f}"] = dict(E_Q=eq_, E_L=el_, dE=el_ - eq_, fex_Q=fq, fex_L=fl)
                per_corner[ck36(c)] = dict(M_floor_Q=HQ.M, M_floor_L=HL.M, grid=cell,
                                           bins={b: float(np.mean([cell[f"{MV:+.0f}|{rh:.0f}"]["dE"] for MV in mvs for rh in RHG])) for b, mvs in BINS.items()})
            rng = {}
            for MV in MVG:
                for rh in RHG:
                    v = [per_corner[k]["grid"][f"{MV:+.0f}|{rh:.0f}"]["dE"] for k in per_corner]
                    rng[f"{MV:+.0f}|{rh:.0f}"] = [float(min(v)), float(max(v))]
            brng = {b: [float(min(per_corner[k]["bins"][b] for k in per_corner)), float(max(per_corner[k]["bins"][b] for k in per_corner))] for b in BINS}
            SEALT[f"{foot}|{reading}"] = dict(range_dE=rng, bins_dE=brng, per_corner=per_corner)
            P(f"  [{foot} {reading}] Delta E_pred (Lm - Q) range over 36 corners: " + "; ".join(f"{b}: {v[0]:+.3f} to {v[1]:+.3f} ln" for b, v in brng.items()))
            for MV in (-6.0, -8.0, -9.0):
                P(f"      M_V {MV:+.0f}: " + ", ".join(f"r_h {rh:.0f} pc {rng[f'{MV:+.0f}|{rh:.0f}'][0]:+.3f}..{rng[f'{MV:+.0f}|{rh:.0f}'][1]:+.3f}" for rh in RHG))
    SEAL = dict(lane="CFG937", criteria="73144fddb", what="SEALED PREDICTION P937 (criteria section 6)", script_sha256=sha256(os.path.abspath(__file__)),
                cfg934_sha256=sha256(SRC934),
                cls="gas-free dSphs with a resolved CMD SFH and stellar sigma, in no sample used by the record (CFG42, CFG874, CFG880/LVD-83, CFG933, CFG936)",
                split="Q: f(12.59 Gyr) >= 0.9; Lm: tau50 < 12.589 Gyr", quantity="Delta E = <ln(sigma_obs/sigma_law)>_Lm - <...>_Q at matched M_V and r_h; sigma_law CFG880 (Ups_V 2, nu_e)",
                templates=dict(Q=dict(tau50=CAP, tau90=CAP, z_f=zQ), Lm=dict(tau50=T50L, tau90=T90L, z_f50=zL["t50"], z_f90=zL["t90"], N=len(late))),
                grid=dict(M_V=MVG, r_h_pc=RHG, bins=BINS), corners=[ck36(c) for c in CK36],
                kill_line="with >= 5 per group matched within 0.5 mag and 0.15 dex in r_h: excluded on a footing if the observed Delta E lies outside "
                          "[min - 2 se, max + 2 se] of the (S) prediction (sealed function at the sample's own M_V, r_h, SFHs; the template table when only the split is known)",
                prediction=SEALT, settings="kappa = 1/2 FITTED; footings never pooled; cold energy, not a particle; not theory closed")
    sp = os.path.join(HERE, "cfg937_SEALED_P937.json")
    with TRUE_OPEN(sp, "w") as fh:
        json.dump(jclean(SEAL), fh, indent=1)
    P(f"\n  sealed file cfg937_SEALED_P937.json sha256 {sha256(sp)}")
    RES["sealed_sha256"] = sha256(sp)
    RES["bins"] = {k: v["bins_dE"] for k, v in SEALT.items()}
    finish(0)

# =====================================================================================================================  main
P("\n" + "=" * 118 + "\nFLOOR MASSES (native Delta_vir): M_cool(1e4 K, mu) and M_filt(T_IGM, mu 0.59); r_vir\n" + "=" * 118)
MTAB = []
for z in (0.0, 0.5, 1.0, 2.0, 3.0, 5.0):
    row = dict(z=z, Mcool_059=mcool(z, 0.59, T_COOL)[0], Mcool_122=mcool(z, 1.22, T_COOL)[0],
               Mfilt={f"{T:.1e}": mcool(z, MU_F, T)[0] for T in TIGM}, rvir_filt_kpc={f"{T:.1e}": mcool(z, MU_F, T)[1] for T in TIGM})
    MTAB.append(row)
    P(f"  z {z:3.1f}: M_cool {row['Mcool_059']:.3e} (mu .59) / {row['Mcool_122']:.3e} (mu 1.22); M_filt " +
      " / ".join(f"{row['Mfilt'][f'{T:.1e}']:.3e}" for T in TIGM) + " (T_IGM 1/1.5/2e4); r_vir " + " / ".join(f"{row['rvir_filt_kpc'][f'{T:.1e}']:.2f}" for T in TIGM) + " kpc")
VTH = {f"{T:.1e}": math.sqrt(2 * KB * T / (MU_F * MP)) / 1e3 for T in TIGM}
P("  V_th = sqrt(2) c_s: " + ", ".join(f"T {k}: {v:.2f} km/s" for k, v in VTH.items()) + "; V_cool 16.73 (mu .59) / 11.63 (mu 1.22) km/s")
RES["floor_table"] = MTAB; RES["V_th"] = VTH

# ---- selector membership and per-object table
P("\n" + "=" * 118 + "\nSELECTOR MEMBERSHIP (criteria 2.3; variants V7 t50, V8 own evidence)\n" + "=" * 118)
OBJ = dict(U=[("sat", d) for d in SAMPLES["ufd"]] + [("sat", d) for d in UL], C=[("sat", d) for d in SAMPLES["cls"]],
           M_col=[("sat", d) for d in SAMPLES["col"]], M_lvd=[("sat", d) for d in SAMPLES["m31"]], I=[("iso", r) for r in I874], L=[("lvd", d) for d in SAMP880])
MEMB = {}; PEROBJ = {}
for cls_, lst in OBJ.items():
    MEMB[cls_] = {}
    for sel in ("t90", "t50", "own"):
        sts = []
        for kind, o in lst:
            grp = "sat" if kind == "sat" else grp_of_host(o.get("host"))
            sts.append((o["name"], status_of(o["name"], o["MV"], grp, kind, o, sel, "group")))
        MEMB[cls_][sel] = dict(N=len(sts), nQ=sum(1 for s in sts if s[1] == "Q"), Q=[s[0] for s in sts if s[1] == "Q"])
    P(f"  {cls_:6s} N {MEMB[cls_]['t90']['N']:3d}: primary Q {MEMB[cls_]['t90']['nQ']} {MEMB[cls_]['t90']['Q']}; V7 (t50) Q {MEMB[cls_]['t50']['nQ']}; "
      f"V8 (own evidence) Q {MEMB[cls_]['own']['nQ']}")
    for kind, o in lst:
        grp = "sat" if kind == "sat" else grp_of_host(o.get("host"))
        t50, t90, src = tau_of(o["name"], o["MV"], grp)
        st = status_of(o["name"], o["MV"], grp, kind, o, "t90", "group")
        fl = {}
        for tk, tau in (("t50", t50), ("t90", t90)):
            zf = zf_of_tau(tau)
            for mu in MUS:
                for T in TIGM:
                    fl[f"{tk}|mu{mu}|T{T:.1e}"] = floor_halo(zf, mu, 3000, st, T).M
        PEROBJ[f"{cls_}:{o['name']}"] = dict(status=st, tau50=t50, tau90=t90, z50=zf_of_tau(t50), z90=zf_of_tau(t90), src=src, M_floor=fl)
RES["membership"] = MEMB; RES["per_object"] = PEROBJ

# ---- bare law and the 36-corner grid
P("\n" + "=" * 118 + "\nBARE LAW (reference)\n" + "=" * 118)
BARE = bare_law()
for foot in FOOTS:
    P(f"  {foot:9s}: " + fmt_cls(BARE[foot]))
RES["bare_law"] = BARE
GRID = {}
for reading in ("S", "M"):
    P("\n" + "=" * 118 + f"\nH-CF2, reading ({reading}) {'[PRIMARY]' if reading == 'S' else '[ALTERNATIVE]'}: 36 corners x 2 footings\n" + "=" * 118)
    GRID.update(run_grid(readings=(reading,), tag="main"))
RES["corners"] = GRID

# ---- verdicts
UP = [c for c in CK36 if c[3] > 1.0e4]


def sub(grid, cs):
    return {f: {ck36(c): grid[f][ck36(c)] for c in cs} for f in FOOTS}


P("\n" + "=" * 118 + "\nVERDICT (criteria 4.1 headline over 36 corners; 4.2 upper bracket T_IGM 1.5-2e4, 24 corners)\n" + "=" * 118)
VER = {}
for reading in ("S", "M"):
    vh, labh = verdict(GRID[reading]); vu, labu = verdict(sub(GRID[reading], UP))
    VER[reading] = dict(headline=vh, upper=vu.replace("SURVIVES", "SURVIVES-UPPER").replace("FAILS", "FAILS-UPPER").replace("PARTIAL", "PARTIAL-UPPER"))
    for f in FOOTS:
        for c in CLASSES:
            cnt = {k: sum(1 for ck in labh[f] if labh[f][ck][c] == k) for k in SEV}
            perT = {f"{T:.1e}": "/".join(str(sum(1 for cc in CK36 if cc[3] == T and labh[f][ck36(cc)][c] == k)) for k in SEV) for T in TIGM}
            P(f"  ({reading}) {f:9s} {c}: CONSISTENT {cnt['CONSISTENT']:2d} / TENSION {cnt['TENSION']:2d} / CONTRADICTED {cnt['CONTRADICTED']:2d} of 36   "
              f"per T_IGM (C/T/X of 12): " + ", ".join(f"{k}: {v}" for k, v in perT.items()))
    allc = {f: [ck for ck in labh[f] if all(labh[f][ck][c] == "CONSISTENT" for c in CLASSES)] for f in FOOTS}
    both = [ck for ck in allc["canonical"] if ck in allc["alt"]]
    VER[reading]["all_consistent"] = dict(canonical=allc["canonical"], alt=allc["alt"], both=both)
    VER[reading]["labels"] = labh
    P(f"  ({reading}) all six CONSISTENT: canonical {len(allc['canonical'])}/36, alt {len(allc['alt'])}/36, both footings {len(both)}: {both}")
    P(f"  ({reading}) headline: {vh};  upper bracket: {VER[reading]['upper']}\n")
RES["verdict"] = VER
vS, vSu = VER["S"]["headline"], VER["S"]["upper"]

# ---- change vs CFG934 at the same (mu, tau, C)
DEL = {}
for reading in ("S", "M"):
    for f in FOOTS:
        for c in CK36:
            r = GRID[reading][f][ck36(c)]; r0 = R934["corners"][reading][f][ck12(c)]
            DEL[f"{reading}|{f}|{ck36(c)}"] = {k: (r[k]["stat"] - r0[k]["stat"]) for k in CLASSES}
RES["delta_vs_cfg934"] = DEL
for reading in ("S", "M"):
    for f in FOOTS:
        P(f"  ({reading}) {f:9s} change vs CFG934 at the upper corners (min..max): " +
          ", ".join(f"{k} {min(DEL[f'{reading}|{f}|{ck36(c)}'][k] for c in UP):+.3f}..{max(DEL[f'{reading}|{f}|{ck36(c)}'][k] for c in UP):+.3f}" for k in CLASSES))

# ---- variants (reading S)
P("\n" + "=" * 118 + "\nVARIANTS (reading S; a variant that changes the headline or the upper-bracket verdict marks it FRAGILE)\n" + "=" * 118)
CL36 = [(ck36(c), c) for c in CK36]
BASE = GRID["S"]; VAR = {}


def vrec(name, grd):
    vh = verdict(grd)[0]; vu = verdict(sub(grd, UP))[0]
    vu = vu.replace("SURVIVES", "SURVIVES-UPPER").replace("FAILS", "FAILS-UPPER").replace("PARTIAL", "PARTIAL-UPPER")
    labs = {f: {ck: {c: grd[f][ck][c]["label"] for c in CLASSES} for ck in grd[f]} for f in FOOTS}
    nall = {f: sum(1 for ck in labs[f] if all(v == "CONSISTENT" for v in labs[f][ck].values())) for f in FOOTS}
    VAR[name] = dict(headline=vh, upper=vu, labels=labs, n_all_consistent=nall,
                     stats={f: {ck: {c: (grd[f][ck][c].get("stat"), grd[f][ck][c].get("z")) for c in CLASSES if c != "S"} for ck in grd[f]} for f in FOOTS})
    flag = []
    if vh != vS:
        flag.append("headline")
    if vu != vSu:
        flag.append("upper")
    P(f"  {name:40s}: headline {vh:28s} upper {vu:34s} all-CONSISTENT corners can {nall['canonical']:2d} / alt {nall['alt']:2d}" + (f"   <-- changes {' + '.join(flag)}" if flag else ""))
    return grd


v3lo = vrec("V3 Upsilon_V 1 for I and L", variant_grid(BASE, lambda c: hcf2(*c), CL36, ups_IL=1.0, reuse_sat=True))
v3hi = vrec("V3 Upsilon_V 4 for I and L", variant_grid(BASE, lambda c: hcf2(*c), CL36, ups_IL=4.0, reuse_sat=True))
vrec("V1 Delta_vir = 18 pi^2", variant_grid(BASE, lambda c: hcf2(*c, eds=True), CL36))
vrec("V2 onset z_coll (13.3 Gyr)", variant_grid(BASE, lambda c: hcf2(*c, onset=True), CL36))
vrec("V4 uniform recipe (Ups floor on I, L)", v4_grid(BASE, v3lo, v3hi))
vrec("V5 Upsilon_SFH (CFG827) for I and L", variant_grid(BASE, lambda c: hcf2(*c), CL36, ups_IL="SFH", reuse_sat=True))
vrec("V6 luminosity-class tau default", variant_grid(BASE, lambda c: hcf2(*c, deflt="lum"), CL36))
vrec("V7 selector by tau50", variant_grid(BASE, lambda c: hcf2(*c, sel="t50"), CL36))
vrec("V8 own-evidence selector (own SFH or HI)", variant_grid(BASE, lambda c: hcf2(*c, sel="own"), CL36))
vrec("V9 m = 1 (V_th = c_s)", variant_grid(BASE, lambda c: hcf2(*c, m2=1), CL36))
vrec("V10 m = 2 (V_th = 2 c_s)", variant_grid(BASE, lambda c: hcf2(*c, m2=4), CL36))
vrec("V11 onset mapping: every dwarf late", variant_grid(BASE, lambda c: hcf2(*c, sel="all"), CL36))
FRAG = [k for k, v in VAR.items() if v["headline"] != vS or v["upper"] != vSu]
P(f"\n  FRAGILE: {'YES (' + ', '.join(FRAG) + ')' if FRAG else 'no'}")
RES["variants"] = VAR; RES["fragile"] = FRAG

# =====================================================================================================================  ungraded (criteria section 7)
P("\n" + "=" * 118 + "\nUNGRADED REPORTS (criteria section 7)\n" + "=" * 118)
UNG = {}
MVa = np.array([PRE880[d["name"]]["MV"] for d in SAMP880]); NAMES = [d["name"] for d in SAMP880]
BINS = (("M_V <= -10", MVa <= -10), ("-10 < M_V <= -7.7", (MVa > -10) & (MVa <= -7.7)), ("M_V > -7.7", MVa > -7.7))
LUM = {}
for f in FOOTS:
    Eb = L_parts(f, A0X[f], "L", None, FBN)[0]
    LUM[f"{f}|bare"] = {b: dict(N=int(m.sum()), E=float(Eb[m].mean())) for b, m in BINS}
    for reading in ("S", "M"):
        for c in CK36:
            E, eps, fx, boost, _ = L_parts(f, A0X[f], reading, hcf2(*c)["lvd"], FBN); act = boost > 1e-6
            LUM[f"{f}|{reading}|{ck36(c)}"] = {b: dict(N=int(m.sum()), E=float(E[m].mean()), n_act=int((act & m).sum()), n_fex=int(((fx > 0) & m).sum())) for b, m in BINS}
    for reading in ("S", "M"):
        P(f"  LVD-83 by luminosity [{f}] ({reading}) bare: " + "; ".join(f"{b} {v['E']:+.3f} (N {v['N']})" for b, v in LUM[f"{f}|bare"].items()))
        for T in TIGM:
            ks = [ck36(c) for c in CK36 if c[3] == T]
            P(f"     T_IGM {T:.1e}: " + "; ".join(f"{b} {min(LUM[f'{f}|{reading}|{k}'][b]['E'] for k in ks):+.3f}..{max(LUM[f'{f}|{reading}|{k}'][b]['E'] for k in ks):+.3f} "
                                              f"(acts in {min(LUM[f'{f}|{reading}|{k}'][b]['n_act'] for k in ks)}-{max(LUM[f'{f}|{reading}|{k}'][b]['n_act'] for k in ks)})" for b, _ in BINS))
UNG["lvd_by_luminosity"] = LUM
# named dwarfs: edge phantom vs cold floor
NAMED = {}
for f in FOOTS:
    for n in ("Draco", "Andromeda IX", "Andromeda V", "Bootes I", "Segue 1"):
        i = NAMES.index(n); q = PRE880[n]; d = SAMP880[i]
        Mb = 2.0 * 10 ** (0.4 * (4.83 - q["MV"])) + (1.33 * 10 ** q["lHI"] if q["lHI"] is not None else 0.0); ep = ephan(Mb, f)
        row = dict(M_V=q["MV"], M_b=Mb, edge_phantom=ep)
        for tk in TKS:
            for T in TIGM:
                Mc = hcf2(0.59, tk, 6000, T)["lvd"](d)[0]; cold = (1 - FBN) * Mc
                row[f"{tk}|T{T:.1e}"] = dict(cold_floor=cold, fex=max(0.0, 1 - ep / cold))
        NAMED[f"{f}|{n}"] = row
        if f == "canonical":
            P(f"  {n:13s} M_V {q['MV']:6.2f} M_b {Mb:.2e} edge phantom {ep:.2e}; cold floor / f_ex (mu .59): " +
              "; ".join(f"{tk} T{T:.0e} {row[f'{tk}|T{T:.1e}']['cold_floor']:.2e}/{row[f'{tk}|T{T:.1e}']['fex']:.2f}" for tk in TKS for T in TIGM))
UNG["named_dwarfs"] = NAMED


def sint_ml(E, eps):                                                  # CFG934's, verbatim
    S = np.concatenate([[0.0], np.geomspace(1e-3, 3.0, 600)]); ll = []
    for s in S:
        w = 1.0 / (eps ** 2 + s ** 2); m = np.sum(w * E) / np.sum(w); ll.append(-0.5 * np.sum(w * (E - m) ** 2) + 0.5 * np.sum(np.log(w)))
    ll = np.array(ll); k = int(np.argmax(ll)); d = 2 * (ll[k] - ll); ok = S[d <= 3.84]
    return dict(s_int=float(S[k]), lo95=float(ok.min()), hi95=float(ok.max()))


D3 = {}
for f in FOOTS:
    a0 = A0X[f]; Eb, epsb, _, _, _ = L_parts(f, a0, "L", None, FBN); SX = ns880["SREF"][f]
    Ec = L_parts(f, a0, "L", None, FBN, extra2=lambda d, r12: float(ns880["clump2"](r12, SX, a0)))[0]
    D3[f] = dict(bare=sint_ml(Eb, epsb), clump877=dict(sint_ml(Ec, epsb), sigma_x=SX, mean=float(np.mean(Ec))), hcf2={})
    for reading in ("S", "M"):
        for c in CK36:
            E, eps, fx, boost, _ = L_parts(f, a0, reading, hcf2(*c)["lvd"], FBN)
            rho = spearmanr(boost, Eb).correlation if np.ptp(boost) > 0 else float("nan")
            D3[f]["hcf2"][f"{reading}|{ck36(c)}"] = dict(sint_ml(E, eps), mean=float(np.mean(E)), rho_boost_vs_obs=float(rho), n_boosted=int(np.sum(boost > 1e-6)))
        guard("D3")
    for reading in ("S", "M"):
        hs = [v for k, v in D3[f]["hcf2"].items() if k.startswith(reading + "|")]
        P(f"  D3 [{f}] ({reading}) LVD-83 s_int: bare {D3[f]['bare']['s_int']:.3f}; clump877 {D3[f]['clump877']['s_int']:.3f}; H-CF2 {min(v['s_int'] for v in hs):.3f}-"
          f"{max(v['s_int'] for v in hs):.3f}; Spearman rho(boost, observed excess) {np.nanmin([v['rho_boost_vs_obs'] for v in hs]):+.2f} to "
          f"{np.nanmax([v['rho_boost_vs_obs'] for v in hs]):+.2f}; boosted {min(v['n_boosted'] for v in hs)}-{max(v['n_boosted'] for v in hs)} of 83")
UNG["D3_scatter"] = D3

# Coma UDGs and DF2/DF4 (CFG933's per-galaxy sigma_law)
D67 = {}
for f in FOOTS:
    pg = R933["byfoot"][f]["per_galaxy"]
    for zf in (0.0, 0.5, 1.0, 2.0, 3.0, 5.0):
        for st, pars in (("Q", [(mu, None) for mu in MUS]), ("L", [(0.59, T) for T in TIGM])):
            for mu, T in pars:
                for C in CS:
                    H = floor_halo(zf, mu, C, st, T if T else 1.0e4); rec = {}
                    for gx in pg:
                        r12_kpc = 4.0 / 3.0 * gx["Re"]; r12 = r12_kpc * 3.0857e19; sl2 = gx["sigma_law"] ** 2
                        gN = 6.674e-11 * (gx["Ms"] / 2) * 1.989e30 / r12 ** 2; sN2 = gN * r12 / 3 / 1e6
                        add = 6.674e-11 * (1 - FBN) * H.enc(r12_kpc) * 1.989e30 / (3 * r12) / 1e6
                        fex = max(0.0, 1 - ephan(gx["Ms"], f) / ((1 - FBN) * H.M))
                        rec[gx["name"]] = dict(pop=gx["pop"], E_obs=gx["E_obs"], E_pred_S=0.5 * math.log((sl2 + fex * add) / sl2),
                                               E_pred_M=0.5 * math.log((sN2 + max(sl2 - sN2, add)) / sl2), fex=fex)
                    coma = [v for v in rec.values() if v["pop"] == "Coma"]
                    D67[f"{f}|zf{zf}|{st}|mu{mu}|T{T}|C{C}"] = dict(per=rec, coma_E_obs=float(np.mean([v["E_obs"] for v in coma])),
                                                                    coma_E_pred_S=float(np.mean([v["E_pred_S"] for v in coma])),
                                                                    coma_E_pred_M=float(np.mean([v["E_pred_M"] for v in coma])), coma_fex_gt0=int(sum(v["fex"] > 0 for v in coma)))
for f in FOOTS:
    rows_ = [v for k, v in D67.items() if k.startswith(f + "|")]
    P(f"  D7 Coma UDGs [{f}] <E_obs> {rows_[0]['coma_E_obs']:+.3f} ln; H-CF2 <E_pred> (S) {min(v['coma_E_pred_S'] for v in rows_):+.3f} to {max(v['coma_E_pred_S'] for v in rows_):+.3f} "
      f"(f_ex > 0 in at most {max(v['coma_fex_gt0'] for v in rows_)}/9), (M) {min(v['coma_E_pred_M'] for v in rows_):+.3f} to {max(v['coma_E_pred_M'] for v in rows_):+.3f} "
      f"over z_f 0-5, both statuses, every mu / T_IGM / C")
    dfn = [n for n, v in rows_[0]["per"].items() if v["pop"] != "Coma"]
    P(f"  D6 DF2/DF4 [{f}] E_obs " + ", ".join(f"{n} {rows_[0]['per'][n]['E_obs']:+.2f}" for n in dfn) +
      "; H-CF2 (no primordial halo): E_pred = 0; with a floor halo (any z_f 0-5, either status): (S) up to " +
      f"{max(v['per'][n]['E_pred_S'] for v in rows_ for n in dfn):+.3f}, (M) up to {max(v['per'][n]['E_pred_M'] for v in rows_ for n in dfn):+.3f}")
UNG["D67_cfg933"] = {k: {kk: vv for kk, vv in v.items() if kk != "per"} for k, v in D67.items()}
UNG["D67_dfs_max"] = {f: dict(S=max(v["per"][n]["E_pred_S"] for k, v in D67.items() if k.startswith(f + "|") for n in v["per"] if v["per"][n]["pop"] != "Coma"),
                             M=max(v["per"][n]["E_pred_M"] for k, v in D67.items() if k.startswith(f + "|") for n in v["per"] if v["per"][n]["pop"] != "Coma")) for f in FOOTS}
R936 = J("CFG936_below_law_systems", "cfg936_results.json")
UNG["TDG_cfg936"] = {f: dict(mean_dex=R936["S1"][f]["mean"], se_dex=R936["S1"][f]["se"], cls=R936["S1"][f]["cls"]) for f in FOOTS}
P("  TDGs (CFG936 S1): " + "; ".join(f"{f} mean {R936['S1'][f]['mean']:+.3f} +- {R936['S1'][f]['se']:.3f} dex ({R936['S1'][f]['cls']})" for f in FOOTS) +
  "; H-CF2 assigns no primordial halo -> E_pred = 0 (no excess), not a deficit")
RES["ungraded"] = UNG

# ---- headline ranges
P("\n" + "=" * 118 + "\nHEADLINE: class statistic range over the 36 corners (and the 24 upper corners)\n" + "=" * 118)
HL = {}
for reading in ("S", "M"):
    for f in FOOTS:
        for c in CLASSES:
            for nm_, cs in (("all", CK36), ("upper", UP)):
                vals = [GRID[reading][f][ck36(k)][c]["stat"] for k in cs]
                zs = [GRID[reading][f][ck36(k)][c].get("z", float("nan")) for k in cs]
                HL[f"{reading}|{f}|{c}|{nm_}"] = dict(min=float(min(vals)), max=float(max(vals)), zmin=(float(np.nanmin(zs)) if c != "S" else None),
                                                      zmax=(float(np.nanmax(zs)) if c != "S" else None), bare=BARE[f][c]["stat"], bare_z=BARE[f][c].get("z"))
            h, u = HL[f"{reading}|{f}|{c}|all"], HL[f"{reading}|{f}|{c}|upper"]
            P(f"  ({reading}) {f:9s} {c}: bare {h['bare']:+.3f}" + (f" ({h['bare_z']:+.2f})" if c != "S" else "") + f" -> all {h['min']:+.3f}..{h['max']:+.3f}" +
              (f" (z {h['zmin']:+.2f}..{h['zmax']:+.2f})" if c != "S" else "") + f"; upper {u['min']:+.3f}..{u['max']:+.3f}" + (f" (z {u['zmin']:+.2f}..{u['zmax']:+.2f})" if c != "S" else ""))
RES["headline"] = HL
P(f"\n  H-CF2 (S) headline {vS}; upper bracket {vSu}; (M) headline {VER['M']['headline']}; upper {VER['M']['upper']}; FRAGILE {'YES' if FRAG else 'no'}.")
P("  kappa = 1/2 FITTED; footings never pooled; cold energy, not a particle; not theory closed.")
finish(0)
