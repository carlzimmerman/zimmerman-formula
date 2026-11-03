#!/usr/bin/env python3
"""CZ1: the KT dwarf lanes' external field, Newtonian instead of MOND inside QUMOND's nu. Criteria 90c548c6cf.
Part A form check, B 24 dwarfs (E0 reproduction of KT27, E1 MW Newtonian, E2 MW + M31 vector sum), C Cassini with the
Newtonian Galactic field, D IC 1613 (stated). KT27's model code copied verbatim; only the external-field value changes.
OMP_NUM_THREADS=1 python3 -I cz1.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import csv, json, math, os, resource, sys
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.special import erf
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); RB = os.path.join(REPO, "rebuild_2026_10_22")
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
def P(s): print(s, flush=True); OUT.append(s)
KAP = 0.5; A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; Gk = 4.30091e-6; CONV = 3.0857e19 / 1e6; XCLIP = 200.0
nu_s = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
nu = (lambda y: np.ones_like(np.asarray(y, float))) if MUT else nu_s
M_MW = 7.0e10  # KT15's frozen MW baryonic mass
P(f"CZ1 (criteria 90c548c6cf){'  [MUTATE]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")

# ---------- Part A: form check ----------
P("\nPart A: boost in the external-field limit (y_int -> 0)")
A = {}
for y in (0.003, 0.01, 0.03):
    corr = float(nu_s(y)); ge = corr * y; mm = 1 / ge; kt = float(nu_s(ge))
    A[y] = dict(corrected=corr, mcgaugh_milgrom=mm, kt_form=kt, kt_over_mm=kt / mm, corr_over_mm=corr / mm)
    P(f"  y_Ne {y}: corrected nu(y_Ne) {corr:.3f}; McGaugh-Milgrom a0/g_e {mm:.3f}; KT form nu(g_e/a0) {kt:.3f}; KT/MM {kt / mm:.3f}; corrected/MM {corr / mm:.3f}")
labA = "DEFECT CONFIRMED" if abs(A[0.01]["kt_over_mm"] - 1) > 0.30 and abs(A[0.01]["corr_over_mm"] - 1) <= 0.10 else "NO DEFECT"
RES["partA"] = dict(rows={str(k): v for k, v in A.items()}, label=labA); P(f"LABEL A: {labA}")

# ---------- KT27's model, copied verbatim ----------
def xi_loc(r, gm, gs, clip):
    dg = np.abs(np.gradient(gm, r)); return np.minimum(gm * gm / np.maximum(dg * gs, 1e-300), clip)
GMs = 6.6743e-11 * 1.98892e30; GEXT, CEIL = 2.32e-10, 5.2e-27
def gh_pt(r, xi):
    xi = np.broadcast_to(xi, r.shape); x = r / xi; out = np.empty_like(r); s = x < 1e-3
    out[~s] = (erf(x[~s] / math.sqrt(2)) - math.sqrt(2 / math.pi) * x[~s] * np.exp(-x[~s] ** 2 / 2)) / r[~s] ** 2; out[s] = math.sqrt(2 / math.pi) / 3 * r[s] / xi[s] ** 3; return out
def qcas(eta, xi, nr=20000, nm=200):
    u = np.linspace(math.log(1e-7), math.log(1e5), nr); r = np.exp(u); mu, w = np.polynomial.legendre.leggauss(nm)
    X = xi(r) if callable(xi) else xi; g = gh_pt(r, X)[:, None]; M = mu[None, :]
    A_ = nu(np.sqrt(eta * eta + g * g + 2 * eta * g * M)) - 1; return abs(1.5 * float(np.trapz(((A_ * (eta * (3 * M - 5 * M ** 3) + g * (1 - 3 * M * M))) @ w) / r, u))), X
def cas_xi(eta):
    def f(x):
        gq = np.sqrt(x ** -4.0 + eta * eta); gm = nu(gq) * gq; return xi_loc(x, gm, 1 / KAP, 1e4)
    return f
UPS = np.linspace(1, 3, 41)
def rgrid(a, xi, n=2000): return np.geomspace(1e-4 * a, 60 * a + 8 * xi, n)
def plummer(r, M, a): return 3 * M / (4 * math.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5
def smooth_rows(r, rho, s, mask_small=False):
    s = np.broadcast_to(np.asarray(s, float), r.shape); R, Rp, S = r[:, None], r[None, :], s[:, None]
    K = (Rp / (math.sqrt(2 * math.pi) * S * R)) * (np.exp(-(R - Rp) ** 2 / (2 * S * S)) - np.exp(-(R + Rp) ** 2 / (2 * S * S))); out = np.trapz(K * rho[None, :], r, axis=1)
    if mask_small:
        dr = np.gradient(r); m = s < 3 * dr; out[m] = rho[m]
    return out
def menc(r, rho):
    f = 4 * math.pi * r * r * rho; return np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(r))]) + 4 * math.pi * rho[0] * r[0] ** 3 / 3
def sig_los(M, a, mode, a0, ge, xi0=0.0):
    if mode == "local" or mode == "at_a":
        r = rgrid(a, XCLIP); rho = plummer(r, M, a); gN = Gk * menc(r, rho) / r ** 2; gq = np.sqrt(gN * gN + ge * ge); X = xi_loc(r, nu(gq / a0) * gq, a0 / KAP, XCLIP)
        if mode == "at_a": X = float(np.interp(a, r, X))
    else:
        X = xi0; r = rgrid(a, X); rho = plummer(r, M, a); gN = Gk * menc(r, rho) / r ** 2
    gh = gN if mode == "plain" else Gk * menc(r, smooth_rows(r, rho, X, mode == "local")) / r ** 2
    g = gN + (nu(np.sqrt(ge * ge + gh * gh) / a0) - 1) * gh; return math.sqrt(np.trapz(rho * r * g * 4 * math.pi * r * r, r) / (3 * M)), X, r

# ---------- positions (UNGC, astropy galactocentric) ----------
from astropy.coordinates import SkyCoord, Galactocentric
import astropy.units as u
U = {}; hdr = None
for l in open(os.path.join(REPO, "real_research", "data", "ungc_karachentsev2013.tsv")):
    if l.startswith("#") or not l.strip(): continue
    p = [x.strip() for x in l.rstrip("\n").split("\t")]
    if hdr is None: hdr = p; continue
    if p[1] == "deg" or set(p[0]) <= {"-"}: continue
    U[p[0]] = dict(zip(hdr, p))
def gc_vec(row):
    c = SkyCoord(ra=float(row["_RAJ2000"]) * u.deg, dec=float(row["_DEJ2000"]) * u.deg, distance=float(row["Dist"]) * u.Mpc)
    g = c.transform_to(Galactocentric(galcen_distance=8.178 * u.kpc)); return np.array([g.x.to(u.kpc).value, g.y.to(u.kpc).value, g.z.to(u.kpc).value])
m31 = U["MESSIER031"]; X31 = gc_vec(m31); M_M31 = 0.6 * 10 ** float(m31["KLum"]) + 1.33 * 10 ** float(m31["MHI"])
P(f"\nM31 (UNGC): galactocentric distance {np.linalg.norm(X31):.1f} kpc; M_b = 0.6 L_K + 1.33 M_HI = {M_M31:.3e} Msun; MW M_b {M_MW:.2e} (KT15)")
UMAP = {"Draco": "Draco", "Ursa Minor": "UMin", "Sculptor": "Sculptor", "Sextans (I)": "SexDSph", "Carina": "Carina", "Fornax": "Fornax", "Canes Venatici (I)": "CVnI",
        "Leo II": "LeoII", "Leo I": "LeoI", "Andromeda IX": "And IX", "Andromeda I": "And I", "Andromeda III": "And III", "Andromeda V": "And V", "Andromeda XIV": "And XIV",
        "Andromeda XV": "And XV", "Andromeda II": "And II", "Andromeda VII": "Cas dSph", "LGS 3 (Local Group Suspect 3)": "LGS 3", "Andromeda VI": "Peg dSph", "Cetus": "Cetus",
        "Leo T": "LeoT", "WLM (Wolf-Lundmark-Melotte)": "WLM", "Leo A": "LeoA", "Tucana": "Tucana"}
def gNe_two(x):
    g = -Gk * M_MW * x / np.linalg.norm(x) ** 3; d = x - X31; g = g - Gk * M_M31 * d / np.linalg.norm(d) ** 3; return float(np.linalg.norm(g))

# ---------- Part B: dwarfs ----------
DATA = os.path.join(REPO, "real_research/data/dsph/mcconnachie2012_dsph.csv"); rows = []
for d in csv.DictReader(open(DATA)):
    if not d["e_sigma*"] or float(d["VMag"]) > -8 or d["Name"].startswith(("M32", "NGC", "Sagittarius")): continue
    rows.append(dict(name=d["Name"], sub=d["SubG"], D=float(d["D"]), L=10 ** (-0.4 * (float(d["VMag"]) - 4.83)), a=float(d["R2"]) / 1e3, s=float(d["sigma*"]), e=float(d["e_sigma*"]), MHI=float(d["M.HI"]) * 1e6 if d["M.HI"] else 0.0))
nomatch = []
for d in rows:
    k = UMAP.get(d["name"]); d["gNe_E1"] = Gk * M_MW / d["D"] ** 2 if d["sub"] == "MW" else 0.0
    if k in U: x = gc_vec(U[k]); d["gNe_E2"] = gNe_two(x); d["d_MW"] = float(np.linalg.norm(x)); d["d_M31"] = float(np.linalg.norm(x - X31))
    else: nomatch.append(d["name"]); d["gNe_E2"] = d["gNe_E1"]; d["d_MW"] = d["D"]; d["d_M31"] = float("nan")
P(f"dwarfs {len(rows)}; no UNGC match (E2 keeps E1): {nomatch or 'none'}")
P("K2 (reported): law's MOND field nu(y_Ne) g_Ne vs 200^2/D [(km/s)^2/kpc], alt: " + ", ".join(
    f"D {D}: {float(nu_s(Gk * M_MW / D ** 2 / (A0SI['alt'] * CONV))) * Gk * M_MW / D ** 2:.0f} vs {200.0 ** 2 / D:.0f}" for D in (76, 147, 250)))
GEV = {"E0": lambda d: (200.0 ** 2 / d["D"]) if d["sub"] == "MW" else 0.0, "E1": lambda d: d["gNe_E1"], "E2": lambda d: d["gNe_E2"]}
MODES = [("plain", 0.0), ("const", 0.5), ("const055", 0.55), ("local", 0.0), ("at_a", 0.0)]
KT27REF = {"plain": 15, "const": 15, "local": 14}; FORN27 = {"canonical": 5.0, "alt": 5.1}
fi = [r_["name"] for r_ in rows].index("Fornax")
for foot, a0s in A0SI.items():
    a0 = a0s * CONV
    for ev, gef in GEV.items():
        cnt = {}
        for mode, eps in MODES:
            n = 0; det = []; m = "const" if mode == "const055" else mode
            for d in rows:
                ge = gef(d); sp = []
                for u_ in UPS:
                    M = u_ * d["L"] + 1.33 * d["MHI"]; s, X, r = sig_los(M, d["a"], m, a0, ge, eps * math.sqrt(Gk * M / a0)); sp.append(s)
                sp = np.array(sp); ok = bool((np.abs(sp - d["s"]) <= 2 * d["e"]).any()); n += ok
                det.append(dict(name=d["name"], obs=d["s"], e=d["e"], pred_U1=float(sp[0]), pred_U2=float(sp[20]), pred_U3=float(sp[-1]), ge_over_a0=ge / a0, passed=ok))
            cnt[mode] = n; RES[f"dwarf|{foot}|{ev}|{mode}"] = dict(n_pass=n, rows=det)
        P(f"\n[{foot} {ev}] " + ", ".join(f"{k} {v}/24" for k, v in cnt.items()) + f"; Fornax local pred {RES[f'dwarf|{foot}|{ev}|local']['rows'][fi]['pred_U2']:.2f} (obs 11.7)")
        if ev == "E0":
            ok = MUT or (all(cnt[k] == v for k, v in KT27REF.items()) and abs(round(RES[f"dwarf|{foot}|E0|local"]["rows"][fi]["pred_U2"], 1) - FORN27[foot]) < 1e-9)
            fail += not ok; P(f"K1 [{foot}] E0 reproduces KT27 (plain 15, const 15, local 14, Fornax {FORN27[foot]}): {'PASS' if ok else 'FAIL'}")
        else:
            for mode, _ in MODES:
                ch = [(x["name"].split(" (")[0], x["passed"]) for x, y in zip(RES[f"dwarf|{foot}|{ev}|{mode}"]["rows"], RES[f"dwarf|{foot}|E0|{mode}"]["rows"]) if x["passed"] != y["passed"]]
                if ch: P(f"    {mode}: changed vs E0: " + ", ".join(f"{nm} {'now PASS' if p else 'now fail'}" for nm, p in ch))
    for ev in ("E1", "E2"):
        c = {k: RES[f"dwarf|{foot}|{ev}|{k}"]["n_pass"] for k, _ in MODES}; fo = RES[f"dwarf|{foot}|{ev}|local"]["rows"][fi]["passed"]
        lab = dict(reference="REFERENCE CHANGES" if c["plain"] != 15 else "REFERENCE STANDS",
                   kt25=("HOLDS" if c["const"] >= c["plain"] - 1 else "FALLS"), kt17=("HOLDS" if c["const055"] >= c["plain"] - 1 else "FALLS"))
        if foot == "alt": lab["kt27"] = "KT27 DWARF FAIL IS AN ARTEFACT" if (c["local"] >= 15 and c["local"] >= c["plain"] - 1 and fo) else "KT27 DWARF FAIL STANDS"
        RES[f"label|{foot}|{ev}"] = dict(counts=c, fornax_local_pass=fo, **lab)
        P(f"LABEL B [{foot} {ev}]: {lab['reference']} (plain {c['plain']}/24); KT25 r_M/2 {lab['kt25']} ({c['const']}); KT17 0.55 r_M {lab['kt17']} ({c['const055']})" + (f"; {lab['kt27']} (local {c['local']}, Fornax {'pass' if fo else 'fail'})" if foot == "alt" else f"; local {c['local']}"))

# ---------- Part C: Cassini ----------
P("\nPart C: Cassini, observed Galactic field (E0) vs its Newtonian part (law inverted)")
R1REF = {"canonical": 0.481, "alt": 1.06}
for foot, a0 in A0SI.items():
    rM = math.sqrt(GMs / a0); qp = CEIL / (1.5 * a0 / rM); eta0 = GEXT / a0
    etaN = brentq(lambda y: float(nu_s(y)) * y - eta0, 1e-6, eta0)
    out = {}
    for lab_, eta in (("E0", eta0), ("N", etaN)):
        for arm, xi in (("const 0.5 r_M", 0.5), ("const 0.55 r_M", 0.55), ("local", cas_xi(eta))):
            q, _ = qcas(eta, xi); out[f"{lab_}|{arm}"] = dict(eta=eta, x_ceiling=q / qp, ok=bool(q <= qp))
    ok = MUT or abs(round(out["E0|const 0.5 r_M"]["x_ceiling"], 3 if foot == "canonical" else 2) - R1REF[foot]) < 1e-9; fail += not ok
    P(f"K3 [{foot}] E0 const 0.5 r_M {out['E0|const 0.5 r_M']['x_ceiling']:.4g} x ceiling (KT27 {R1REF[foot]}): {'PASS' if ok else 'FAIL'}; eta {eta0:.4f} -> Newtonian {etaN:.4f}")
    for arm in ("const 0.5 r_M", "const 0.55 r_M", "local"):
        a_, b_ = out[f"E0|{arm}"], out[f"N|{arm}"]
        P(f"  [{foot}] {arm:15s}: E0 {a_['x_ceiling']:.4g} x ({'PASS' if a_['ok'] else 'FAIL'})  ->  Newtonian {b_['x_ceiling']:.4g} x ({'PASS' if b_['ok'] else 'FAIL'})")
    RES[f"cassini|{foot}"] = out

# ---------- Part D: IC 1613 (stated) ----------
P("\nPart D: IC 1613, FD1 PRIMARY inputs (stated, not graded)")
x = gc_vec(U["IC1613"]); PC, MSUN, G = 3.0856775814913673e16, 1.98847e30, 6.67430e-11
fd = json.load(open(os.path.join(RB, "FD1_field_dwarf_audit", "fd1_field_dwarf_audit_results.json")))
x1 = {r["footing"]: r for r in csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv"))) if r["name"] == "IC 1613"}
for foot, a0 in A0SI.items():
    row = [r_ for r_ in fd["footings"][foot]["runs"]["PRIMARY M+G+K"]["rows"] if r_["name"] == "IC 1613"][0]
    r12 = 4 / 3 * float(x1[foot]["rh_pc"]) * PC; mb = 10 ** row["logMb"]; gobs = (3 * row["sigma_b"] ** 2 + row["vrot"] ** 2) * 1e6 / r12; gN = G * (mb / 2) * MSUN / r12 ** 2
    E0 = math.log10(gobs) - math.log10(float(nu_s(gN / a0)) * gN); ok = MUT or abs(E0 - row["E"]) < 1e-4; fail += not ok
    gNe = gNe_two(x) / CONV; yNe = gNe / a0; E1 = math.log10(gobs) - math.log10(float(nu_s(math.hypot(gN, gNe) / a0)) * gN)
    RES[f"ic1613|{foot}"] = dict(E_FD1=row["E"], E_repro=E0, yN_int=gN / a0, yN_ext=yNe, E_with_LG_field=E1, shift=E1 - E0, Z_with=E1 / row["s"], d_MW=float(np.linalg.norm(x)), d_M31=float(np.linalg.norm(x - X31)))
    P(f"  [{foot}] reproduce FD1 E {row['E']:+.4f}: {E0:+.4f} {'PASS' if ok else 'FAIL'}; d_MW {np.linalg.norm(x):.0f}, d_M31 {np.linalg.norm(x - X31):.0f} kpc; y_N int {gN / a0:.4f}, LG Newtonian ext {yNe:.2e}; E {E0:+.4f} -> {E1:+.4f} (shift {E1 - E0:+.5f} dex, Z {E1 / row['s']:+.2f})")

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30; RES["peak_rss_GB"] = rss; RES["fail"] = fail
P(f"\npeak RSS {rss:.2f} GB; failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"cz1{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"cz1{sfx}.json"), "w"), indent=1)
sys.exit(1 if (MUT or fail) else 0)
