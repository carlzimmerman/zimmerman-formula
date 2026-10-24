#!/usr/bin/env python3
"""PH1_two_phase_cold_energy: a two-phase cold energy (condensed = held khronon dust that sources the law; normal =
self-gravitating Xi-neutral dust) tested against the rows O1 left open.

Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (11270eef61, committed alone first).  kappa = 1/2 FITTED.  Footings
9.3603e-11 / 1.1312e-10 m/s^2, never pooled.  No dark-matter particle (classical field).  Not "theory closed".

Run:   OMP_NUM_THREADS=1 nice -n 15 python3 ph1_two_phase.py            -> .out, _results.json (exit 0 iff all checks pass)
       OMP_NUM_THREADS=1 nice -n 15 python3 ph1_two_phase.py --mutate   -> _MUTATE.* (normal phase given Xi-charge; D3, KG FAIL)
Other lanes are read only (functions extracted by ast from P4 and F3; Z2 / U1 csv files).  Nothing is downloaded.
"""
import os, sys, ast, csv, json, math, time, resource
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RB = os.path.join(REPO, "rebuild_2026_10_22")
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
T0 = time.time()
OUT, CHECKS = [], {}
RES = dict(lane="PH1_two_phase_cold_energy", criteria="11270eef61", mutate=MUT)


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(k, ok, val, thr):
    CHECKS[k] = dict(ok=bool(ok), value=str(val), threshold=thr)
    P(f"{k} {'PASS' if ok else 'FAIL'}  {val}   [{thr}]")


def rss_gb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e9 if sys.platform == "darwin" else r / 1e6


def extract(path, names, g):
    """exec only the named top-level functions of another lane's script (read-only reuse)."""
    src = open(path).read(); tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            exec(compile(ast.Module([node], []), path, "exec"), g)
    return g


G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
LSTAR = {"canonical": 21.68, "alt": 22.85}                  # pc, D10 floors (FITTED)


def g_from_gN(y):
    y = np.asarray(y, float); return 0.5 * (y + np.sqrt(y * y + 4.0 * y))   # g mu(g) = gN, mu = x/(1+x), a0 = 1


P("=" * 110)
P("PH1_two_phase_cold_energy" + ("   *** MUTATE: normal phase carries Xi-charge ***" if MUT else ""))
P("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled; not theory closed")
P("=" * 110)

# ============================================================== T1: action family and sympy derivations
P("\nT1  ACTION (classical complex scalar; condensed = coherent phase = khronon; normal = incoherent part)")
P("  S = (c^3/16piG) Int sqrt(-g) [R - 2Lambda - 2 J_x(Y[theta]) + 2 K(Q[theta])] + S_gammaL/switch[theta]")
P("      + Int sqrt(-g) [ -|d psi_n|^2 - mu^2 |psi_n|^2 ]_incoherent  + S_m[g]")
P("  psi = sqrt(rho_s) e^{i theta} (coherent, <psi> != 0)  +  psi_n (<psi_n> = 0, Wigner -> multi-stream dust)")
P("  The law sector J_x sees only theta (the coherent phase).  The normal part couples to g only.")
r, a0s, Gs, M, gN, g, C = sp.symbols("r a_0 G M g_N g C", positive=True)
y = sp.symbols("y", positive=True)
gsol = (y + sp.sqrt(y ** 2 + 4 * y)) / 2
D1 = sp.simplify(gsol * (gsol / (1 + gsol)) - y)
check("D1", D1 == 0, f"condensed static limit: g mu(g/a0) = g_N with g = a0 g_from_gN; residual {D1}; held dust = phantom of "
      "(rho_b + rho_n), Xi = Phi + C (U1 D2)", "residual 0")
sig, rr = sp.symbols("sigma r", positive=True)
rho_iso = sig ** 2 / (2 * sp.pi * Gs * rr ** 2)
Menc = sp.integrate(4 * sp.pi * rr ** 2 * rho_iso, (rr, 0, r))
jeans = sp.simplify(sp.diff(rho_iso * sig ** 2, rr) + rho_iso * Gs * Menc.subs(r, rr) / rr ** 2)
check("D2", jeans == 0, f"normal static limit: isothermal rho = sigma^2/(2 pi G r^2) solves Jeans + Poisson (residual {jeans}); "
      f"M_n(<r) = {sp.simplify(Menc)} = v_n^2 r/G", "residual 0")
Mb, Mn, Ms, gh = sp.symbols("M_b M_n M_s g_h", positive=True)
qn = 1 if MUT else 0                                        # Xi-charge of the normal phase (mutate: held like the condensate)
gradXi = gh                                                 # K5: held AQUAL host, |grad Xi_amb| = g_host
F = (Mb + Mn + Ms) * gh - (Ms + qn * Mn) * gradXi
acc_n = sp.simplify(gh - qn * gradXi)                       # acceleration of the normal share
eps_n = sp.simplify((gh - acc_n) / gh)                       # lag relative to free fall, in units of g_host
check("D3", eps_n == 0, f"composite weight F = {sp.simplify(F)}; normal share accelerates at {acc_n} -> eps_n = {eps_n} "
      f"(condensed share eps_s = 1)", "eps_n = 0")
k, cs, Ls, rhob = sp.symbols("k c_s L_star rhobar", positive=True)
omega = k * Ls * sp.sqrt(2 * sp.pi * Gs * rhob)
vc = sp.simplify(omega / k)
check("D4", sp.simplify(vc - Ls * sp.sqrt(2 * sp.pi * Gs * rhob)) == 0,
      f"Landau v_c = min_k omega/k = {vc} (held phase linear dispersion with the L* stiffness, O1 sec.3)", "derived")
A_, t_, q_ = sp.symbols("A t q", positive=True)
xq = q_ - A_ * t_ * sp.sin(q_)                               # Zel'dovich / free streaming of v = -A sin q
dxdq = sp.diff(xq, q_)
fold = sp.solve(sp.Eq(dxdq.subs(q_, 0), 0), t_)
ok5 = fold == [1 / A_] and sp.simplify(dxdq.subs(q_, 0).subs(t_, 2 / A_)) < 0
check("D5", ok5, f"fold first at t = {fold}; dx/dq(q=0) = {sp.simplify(dxdq.subs(q_, 0))} < 0 for every t > 1/A: once "
      "multi-stream the medium never returns to single-stream (no single-valued theta, so no condensate)", "fold persists")
RES["T1"] = dict(D3_eps_n=str(eps_n), vc=str(vc))

# Landau speeds from the allowed constants
def cs_kms(rho_msun_pc3, Lpc):
    Gp = 4.30091e-3                                          # pc (km/s)^2 / Msun
    return Lpc * math.sqrt(2 * math.pi * Gp * rho_msun_pc3)  # (km/s)  [pc * sqrt(pc^-2 (km/s)^2)]
VC = {f: {"satellite rho 0.1": cs_kms(0.1, LSTAR[f]), "disc halo rho 0.01": cs_kms(0.01, LSTAR[f]),
          "cluster core rho 0.003": cs_kms(3e-3, LSTAR[f])} for f in FOOTS}
P(f"  Landau v_c (km/s): {json.dumps({f: {k_: round(v, 3) for k_, v in VC[f].items()} for f in FOOTS})}")
RES["v_c_kms"] = VC

# ============================================================== T2: criterion menu
P("\nT2  CRITERION MENU (phase assigned per class; REQUIRED: disc C, satellite N, cluster core part-N, early N, TDG none, SS none)")
H0n = 67.578 * 1e3 / KPC / 1e3                               # s^-1 (background A)
rhoL = 3 * H0n ** 2 * 0.687 / (8 * math.pi * G) / (MSUN / PC ** 3)
STATE = {  # class: (g/a0, rho [Msun/pc^3], sigma [km/s], V_rel [km/s], streams)
    "isolated disc (R 8-30 kpc)": ("0.4-2", "1e-2", "150", "0.03 (O1)", "multi if built by dust growth"),
    "satellite (r_half)": ("0.01-0.3", "0.1", "3-10", "100-300", "single (held) before infall"),
    "cluster core (0.3-1 Mpc)": ("1-3", "3e-3", "1000", "members 1000", "multi"),
    "early universe z 1100-30": ("15.6 at z 1100 (LEDGER:705)", f">{1100**3*0.31*rhoL/0.69:.1e}->", "~0", "~0", "single"),
    "TDG / DF2-DF4": ("0.05-0.3", "-", "-", "100-200 at birth", "baryons only"),
    "Solar System / globulars": (">1e3", "-", "-", "36-220 (O1)", "-"),
}
MENU = {
    "C-g  |grad Phi| < a0 => condensed": dict(constants="0 new", disc="C (outer) / N (inner)", satellite="C  X", cluster="mixed", early="N to z~90, then C  X (Theorem G)", TDG="n/a", SS="N ok", admissible=False),
    "C-rho  rho < k rho_Lambda => condensed": dict(constants="0 new (+ O(1) k)", disc="N  X (rho ~ 1e5 rho_L)", satellite="N", cluster="N", early="N", TDG="n/a", SS="N", admissible=False),
    "C-rho' rho > k rho_Lambda => condensed": dict(constants="0 new (+ O(1) k)", disc="C", satellite="C  X", cluster="C  X", early="C  X", TDG="n/a", SS="C", admissible=False),
    "C-sigma  sigma < (G M a0)^1/4 => condensed": dict(constants="0 new", disc="C (ratio 0.71)", satellite="C  X (ratio 0.47 pre-infall, unchanged by infall)", cluster="C", early="C  X (sigma -> 0)", TDG="n/a", SS="-", admissible=False),
    "C-V  V_rel < c_s(L*, rho) => condensed (Landau)": dict(constants="0 new (L* FITTED, allowed)", disc="C ok (0.03 << ~1 km/s)", satellite="N ok (released at dv = v_c << sigma: bound)", cluster="members N; cluster khronon still holds => debris ADDED", early="C  X (no relative flow on FRW)", TDG="none ok", SS="none ok (O1 VS)", admissible=False),
    "C-SX  single-stream => condensed": dict(constants="0 new", disc="N  X (virialised)", satellite="N", cluster="N", early="C  X", TDG="n/a", SS="-", admissible=False),
    "C-lambda  c/(mu sigma) > size => condensed": dict(constants="+1 NEW (mu); mu = 1/L* gives m c^2 = 2.9e-25 eV", disc="C (66 kpc)", satellite="C  X (660 kpc)", cluster="N ok (6.6 kpc)", early="C  X (fuzzy, Jeans k ~ 0.3/Mpc)", TDG="n/a", SS="-", admissible=False),
}
for k_, v in STATE.items():
    P(f"  state  {k_:30s} g/a0 {v[0]:28s} rho {v[1]:10s} sigma {v[2]:6s} V_rel {v[3]:16s} {v[4]}")
for k_, v in MENU.items():
    P(f"  {k_:50s} [{v['constants']}]  disc {v['disc']} | sat {v['satellite']} | cl {v['cluster']} | early {v['early']} | TDG {v['TDG']} | SS {v['SS']}")
P("  => no criterion from {kappa, a0, G, c, Lambda, L*} is ADMISSIBLE; best = C-V (fails only 'early universe' as a phase rule).")
P("     Early-normal can only be an INITIAL CONDITION (branch EN), and D5 forbids normal -> condensed later.")
RES["T2"] = dict(state=STATE, menu=MENU, admissible=[k_ for k_, v in MENU.items() if v["admissible"]], rho_Lambda=rhoL)

# ============================================================== G: growth
P("\nG   GROWTH (three fluids: baryons, normal s = 1, condensed held s = 0; a_i = 1e-3; line ratio >= 0.95)")
F3P = os.path.join(RB, "F3_growth_audit", "f3_growth_audit.py")
gF3 = extract(F3P, {"make_E", "growth_ratio"}, dict(math=math, np=np, solve_ivp=solve_ivp))
WB, WC, HA = 0.022308, 0.120573, 0.67578
BGS = {"A_c2b": ((WB + WC) / HA ** 2, WB / HA ** 2, HA), "B_cfg886": (0.2976015949416498, WB / 0.6856426703851345 ** 2, 0.6856426703851345)}


def growth3(fn, Om, Ob, h, a_i=1e-3, qn_=0):
    Ek, Or = gF3["make_E"](Om, h, True); Oc = Om - Ob; On, Os = fn * Oc, (1 - fn) * Oc
    def rhs(x, s_):
        a = math.exp(x); E = Ek(a); e = 1e-6
        dlnE = (math.log(Ek(a * math.exp(e))) - math.log(Ek(a * math.exp(-e)))) / (2 * e)
        dens = 1.5 * a ** -3 / E ** 2
        db, gb, dn, gn, ds, gs = s_
        src_all = dens * (Ob * db + On * dn + Os * ds)
        src_held = dens * (Ob * db + On * dn * (1 - qn_))      # held: no self-force (s = 0); mutate: normal is held too
        src_n = src_held if qn_ else src_all
        return [gb, -(2 + dlnE) * gb + src_all, gn, -(2 + dlnE) * gn + src_n, gs, -(2 + dlnE) * gs + src_held]
    sol = solve_ivp(rhs, [math.log(a_i), 0.0], [a_i] * 6, method="DOP853", rtol=1e-8, atol=1e-13)
    y_ = sol.y[:, -1]
    return (Ob * y_[0] + On * y_[2] + Os * y_[4]) / Om


GRO = {}
for bg, (Om, Ob, h) in BGS.items():
    dust = growth3(1.0, Om, Ob, h)                          # pure dust reference (normal, uncharged)
    r0 = growth3(0.0, Om, Ob, h) / dust
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        (lo, hi) = (lo, mid) if growth3(mid, Om, Ob, h, qn_=qn) / dust >= 0.95 else (mid, hi)
    GRO[bg] = dict(Om=Om, Ob=Ob, h=h, ratio_EC_fn0=r0, fn_min=hi, ratio_fn1=growth3(1.0, Om, Ob, h, qn_=qn) / dust)
    P(f"  {bg}: Om {Om:.4f} Ob {Ob:.4f} h {h:.4f}: EC (f_n = 0) ratio {r0:.4f}; f_n,min = {hi:.4f} (line 0.95)")
# KG: my f_n = 0 vs F3's growth_ratio with its BSK2 kernel at mu -> 0 (s -> 0); f_n = 1 vs mu -> inf
Om, Ob, h = BGS["A_c2b"]
gF3r = float(gF3["growth_ratio"](np.array([0.1]), 1e-9, Om, Ob, h, kernel="bsk2")[0])
my0 = GRO["A_c2b"]["ratio_EC_fn0"]
r1 = GRO["A_c2b"]["ratio_fn1"]
okG = abs(gF3r - my0) < 1e-3 and r1 >= 0.95
check("KG", okG, f"F3 growth_ratio(mu->0, BSK2 kernel) {gF3r:.5f} vs mine f_n=0 {my0:.5f}; f_n = 1 with the run's charge "
      f"assignment (Xi-charge {qn}): {r1:.4f}", "|diff| < 1e-3 and f_n = 1 meets 0.95")
RES["G"] = GRO

# ============================================================== P4: isolated RAR double counting
P("\nP4  ISOLATED RAR + DOUBLE COUNTING (P4 statistic: weighted rms <= 0.110 and median Upsilon in [0.50, 0.80])")
P4P = os.path.join(RB, "P4_v3_galaxy_tiles", "p4_v3_galaxy_tiles.py")
KPC_S = 3.0857e19
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
gP4 = extract(P4P, {"load_sparc_own", "gal_arrays", "chi2_offset", "fit_sample", "pooled"},
              dict(os=os, np=np, math=math, CHI2=CHI2, DATA=os.path.join(REPO, "real_research", "data"), KPC_S=KPC_S, UPS=UPS,
                   LN10=math.log(10.0)))
GALS = gP4["load_sparc_own"]()
P4J = json.load(open(os.path.join(RB, "P4_v3_galaxy_tiles", "p4_v3_galaxy_tiles_results.json")))["tiles"]["T1"]["footings"]


def lgp_for(a0, mode=None, par=0.0, H0=None, fn=None):
    out = {}
    for q in GALS:
        GB, GO, OK, W = gP4["gal_arrays"](q, UPS)
        R = (q["R"] * KPC_S)[:, None]
        gNn = 0.0
        if mode == "EC":
            gNn = par * (a0 * g_from_gN(np.abs(GB) / a0) - np.abs(GB))
        elif mode == "EN":
            Mb = np.maximum(GB[-1] * R[-1] ** 2, 0.0) / G                 # kg, per Upsilon column (last point); A1 fix
            Mt = par * fn * (WC / WB) * Mb
            vn = (10.0 * G * H0 * Mt) ** (1.0 / 3.0)
            Rv = vn / (10.0 * H0)
            gNn = np.where(R <= Rv[None, :], vn[None, :] ** 2 / R, G * Mt[None, :] / R ** 2)
        out[q["name"]] = np.log10(np.maximum(a0 * g_from_gN(np.maximum(GB + gNn, 1e-300) / a0), 1e-300))
    return out


def stat(a0, **kw):
    st = gP4["pooled"](gP4["fit_sample"](GALS, lgp_for(a0, **kw)))
    return dict(rms=st["rms"], U_median=st["U_median"], frac_p_ok=st["frac_p_ok"], line=bool(st["rms"] <= 0.110 and 0.50 <= st["U_median"] <= 0.80))


P4R = {}
okP = True
for f in FOOTS:
    base = stat(A0[f])
    ref = P4J[f]["iso_perUps"]
    okP &= abs(base["rms"] - ref["rms"]) <= 1e-4 and base["U_median"] == ref["U_median"]
    row = dict(control=base, P4_ref=dict(rms=ref["rms"], U_median=ref["U_median"]))
    for bg, gr in GRO.items():
        H0 = gr["h"] * 100e3 / KPC / 1e3
        row[f"EN_{bg}"] = stat(A0[f], mode="EN", par=1.0, H0=H0, fn=gr["fn_min"])
    # tolerances (diagnostics)
    lam_max = 0.0
    for lam in np.round(np.arange(0.05, 2.0001, 0.05), 2):
        if stat(A0[f], mode="EC", par=lam)["line"]:
            lam_max = float(lam)
        else:
            break
    gr = GRO["A_c2b"]; H0 = gr["h"] * 100e3 / KPC / 1e3
    m_max = 0.0
    for m in np.round(np.arange(0.05, 5.0001, 0.05), 2):
        if stat(A0[f], mode="EN", par=m, H0=H0, fn=gr["fn_min"])["line"]:
            m_max = float(m)
        else:
            break
    row["EC_lambda_max"] = lam_max; row["EC_at_lambda_max_plus"] = stat(A0[f], mode="EC", par=lam_max + 0.05)
    row["EN_m_max"] = m_max
    row["EC_lambda_0.5"] = stat(A0[f], mode="EC", par=0.5); row["EC_lambda_1"] = stat(A0[f], mode="EC", par=1.0)
    P4R[f] = row
    P(f"  {f}: control rms {base['rms']:.4f} U {base['U_median']:.2f} (P4 {ref['rms']:.4f} / {ref['U_median']:.2f})")
    for bg in GRO:
        e = row[f"EN_{bg}"]
        P(f"     EN {bg}: rms {e['rms']:.4f}  U_med {e['U_median']:.2f}  line {'PASS' if e['line'] else 'FAIL'}   "
          f"double count: d rms {e['rms']-base['rms']:+.4f}, d U {e['U_median']-base['U_median']:+.2f}")
    P(f"     EC merger debris: lambda_max {lam_max:.2f} of own phantom (lambda 0.5: rms {row['EC_lambda_0.5']['rms']:.4f} "
      f"U {row['EC_lambda_0.5']['U_median']:.2f}; lambda 1: rms {row['EC_lambda_1']['rms']:.4f} U {row['EC_lambda_1']['U_median']:.2f}); "
      f"EN m_max {m_max:.2f} x fair share at f_n,min")
check("KP", okP, "control reproduces P4 iso_perUps rms and median Upsilon on both footings", "|d rms| <= 1e-4, U equal")
RES["P4"] = P4R

# ============================================================== Z2: satellites
P("\nZ2  SATELLITES (Z2 per-system Delta_ISO; C2-C4 subset; EC freeze-out radial collapse; EN normal subhalo)")
Z2 = list(csv.DictReader(open(os.path.join(RB, "Z2_satellite_systematics", "z2_per_system.csv"))))
U1 = {(r_["footing"], r_["name"]): r_ for r_ in csv.DictReader(open(os.path.join(RB, "U1_v3_dust_content", "u1_satellites_per_system.csv")))}
LVD = {}
for fn_ in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r_ in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", fn_))):
        def fl(x):
            try:
                v = float(x); return v if math.isfinite(v) else None
            except Exception:
                return None
        LVD[r_["name"]] = fl(r_.get("rhalf_sph_physical")) or fl(r_.get("rhalf_physical"))


# ---- 1D spherical shell code (G = M_b = r12 = 1)
def plummer_M(rr_, a):
    return rr_ ** 3 / (rr_ ** 2 + a ** 2) ** 1.5


def collapse(y12, Rj, Nd=1500, Ns=500, eps=0.03, tmult=6.0, seed=0):
    """released phantom (radial, at rest) + stars (circular shells) of an isolated deep-AQUAL Plummer satellite, truncated
    at Rj (units r12).  Returns boost B = g_tot(r12_f)/g_iso(r12_f) and contraction c = r12_f / r12_i."""
    a0p = 1.0 / y12; ap = 1.0 / 1.305
    rg = np.geomspace(1e-3, Rj, 4000)
    Mb_ = plummer_M(rg, ap) / plummer_M(1e9, ap)
    gl = a0p * g_from_gN(Mb_ / rg ** 2 / a0p)
    Mph = np.maximum.accumulate(np.maximum(rg ** 2 * gl - Mb_, 0.0))
    Mtot_i = Mph[-1]
    u = (np.arange(Nd) + 0.5) / Nd
    rd = np.interp(u * Mtot_i, Mph, rg); md = np.full(Nd, Mtot_i / Nd)
    Mbmax = Mb_[-1]
    us = (np.arange(Ns) + 0.5) / Ns
    rs = np.interp(us * Mbmax, Mb_, rg); ms_ = np.full(Ns, Mbmax / Ns)
    Mtot_r = lambda x: np.interp(x, rg, Mb_ + Mph)
    js2 = rs ** 3 * (Mtot_r(rs) / rs ** 2)
    rpos = np.concatenate([rd, rs]); v = np.zeros(Nd + Ns); m = np.concatenate([md, ms_])
    j2 = np.concatenate([np.zeros(Nd), js2]); isd = np.arange(Nd + Ns) < Nd
    tJ = 0.5 * math.pi * math.sqrt(Rj ** 3 / (2 * (Mbmax + Mtot_i)))
    vmax = math.sqrt(2 * (Mbmax + Mtot_i) / Rj * (1 + math.log(Rj / eps))) * 1.5
    t_orb1 = 2 * math.pi / math.sqrt(max(Mtot_r(1.0), 1e-9))
    dt = min(0.25 * eps / vmax, 0.01 * t_orb1)
    nstep = int(tmult * tJ / dt) + 1
    def acc(rp):
        o = np.argsort(rp); cm = np.cumsum(m[o]) - 0.5 * m[o]
        Min = np.empty_like(cm); Min[o] = cm
        return -Min * rp / (rp ** 2 + eps ** 2) ** 1.5 + j2 / np.maximum(rp, 1e-6) ** 3
    lgr = np.linspace(math.log(0.05), math.log(Rj * 2), 120); rgrid = np.exp(lgr)
    Macc = np.zeros(len(rgrid)); r12acc = 0.0; nacc = 0
    a_ = acc(rpos)
    t_start = 3.0 * tJ
    for it in range(nstep):
        v += 0.5 * dt * a_; rpos += dt * v
        neg = rpos < 0; rpos[neg] = -rpos[neg]; v[neg] = -v[neg]
        a_ = acc(rpos); v += 0.5 * dt * a_
        if it * dt >= t_start and it % 20 == 0:
            srt = np.sort(rpos); cms = np.cumsum(m[np.argsort(rpos)])
            Macc += np.interp(rgrid, srt, cms); r12acc += np.median(rpos[~isd]); nacc += 1
    Mf = Macc / nacc; r12f = r12acc / nacc
    gt = np.interp(r12f, rgrid, Mf) / r12f ** 2
    giso = a0p * g_from_gN(0.5 * Mbmax / r12f ** 2 / a0p)
    return dict(B=float(gt / giso), c=float(r12f), nstep=nstep, tJ=tJ, Mph_over_Mb=float(Mtot_i / Mbmax))


def collapse_ad(y12, Rj, Nd=4000, eps=0.03, tmult=6.0):
    """AMENDMENT A1 (post-result): the released phantom collapses radially from rest (dust shells, softened, Plummer baryons
    in the force); the stars respond in the adiabatic limit of the same circular shells (r M(<r) conserved for the stellar
    half-mass shell).  Returns B = g_tot(r12_f)/g_iso(r12_f) and c = r12_f / r12_i."""
    a0p = 1.0 / y12; ap = 1.0 / 1.305
    rg = np.geomspace(1e-3, Rj, 4000)
    Mb_ = plummer_M(rg, ap) / plummer_M(1e9, ap)
    gl = a0p * g_from_gN(Mb_ / rg ** 2 / a0p)
    Mph = np.maximum.accumulate(np.maximum(rg ** 2 * gl - Mb_, 0.0))
    Mtot_i = Mph[-1]; Mbmax = Mb_[-1]
    u = (np.arange(Nd) + 0.5) / Nd
    rpos = np.interp(u * Mtot_i, Mph, rg); v = np.zeros(Nd); m = np.full(Nd, Mtot_i / Nd)
    tJ = 0.5 * math.pi * math.sqrt(Rj ** 3 / (2 * (Mbmax + Mtot_i)))
    vmax = math.sqrt(2 * (Mbmax + Mtot_i) / Rj * (1 + math.log(Rj / eps))) * 1.5
    dt = 0.25 * eps / vmax
    nstep = int(tmult * tJ / dt) + 1
    Mb_at = lambda x: plummer_M(x, ap) / plummer_M(1e9, ap)
    def acc(rp):
        o = np.argsort(rp); cm = np.cumsum(m[o]) - 0.5 * m[o]
        Min = np.empty_like(cm); Min[o] = cm
        return -(Min + Mb_at(rp)) * rp / (rp ** 2 + eps ** 2) ** 1.5
    rgrid = np.exp(np.linspace(math.log(0.02), math.log(Rj * 2), 160))
    Macc = np.zeros(len(rgrid)); nacc = 0
    a_ = acc(rpos)
    for it in range(nstep):
        v += 0.5 * dt * a_; rpos += dt * v
        neg = rpos < 0; rpos[neg] = -rpos[neg]; v[neg] = -v[neg]
        a_ = acc(rpos); v += 0.5 * dt * a_
        if it * dt >= 3.0 * tJ and it % 20 == 0:
            srt = np.sort(rpos); Macc += np.interp(rgrid, srt, np.cumsum(m)); nacc += 1
    Mdf = Macc / nacc
    Mdi1 = float(np.interp(1.0, rg, Mph)); inv = 1.0 * (0.5 + Mdi1)
    lo, hi = 0.02, 5.0
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        (lo, hi) = (lo, mid) if mid * (0.5 + np.interp(mid, rgrid, Mdf)) > inv else (mid, hi)
    rf = math.sqrt(lo * hi)
    gt = (0.5 + np.interp(rf, rgrid, Mdf)) / rf ** 2
    giso = a0p * g_from_gN(0.5 / rf ** 2 / a0p)
    return dict(B=float(gt / giso), c=float(rf), nstep=nstep, tJ=tJ, Mph_over_Mb=float(Mtot_i / Mbmax),
                Md_in_1_ratio=float(np.interp(1.0, rgrid, Mdf) / Mdi1))


# KS1: cold uniform sphere collapse energy check (no stars), before shell crossing
def ks1():
    N = 2000; rr_ = ((np.arange(N) + 0.5) / N) ** (1 / 3); m_ = np.full(N, 1.0 / N)
    vv = np.zeros(N); dt = 1e-4; tff = math.pi / 2 * math.sqrt(1 / 2)
    def acc(rp):
        o = np.argsort(rp); cm = np.cumsum(m_[o]) - 0.5 * m_[o]; Mi = np.empty_like(cm); Mi[o] = cm
        return -Mi / rp ** 2
    def energy(rp, vp):
        o = np.argsort(rp); cm = np.cumsum(m_[o]) - 0.5 * m_[o]; Mi = np.empty_like(cm); Mi[o] = cm
        return np.sum(0.5 * m_ * vp ** 2) - np.sum(m_ * Mi / rp)
    E0 = energy(rr_, vv); a_ = acc(rr_)
    for _ in range(int(0.9 * tff / dt)):
        vv += 0.5 * dt * a_; rr_ += dt * vv; a_ = acc(rr_); vv += 0.5 * dt * a_
    return abs(energy(rr_, vv) / E0 - 1), float(np.max(rr_))
e1, rmax_ = ks1()
check("KS1", e1 < 0.01, f"cold uniform sphere to 0.9 t_ff: |dE/E| {e1:.2e}; outer radius {rmax_:.3f}", "< 1 %")

# system table
SYS = {f: [] for f in FOOTS}
for r_ in Z2:
    f = r_["footing"]; nm = r_["name"]
    rh = LVD.get(nm)
    yv = float(U1[(f, nm)]["y"]); y12 = yv / (4 / 3) ** 2
    r12 = 4 / 3 * rh * PC
    Dm = float(r_["D_host_kpc"]) * KPC
    xe = float(r_["x_e"])
    rp = float(r_["r_peri_kpc"]) * KPC if r_["r_peri_kpc"] not in ("", "nan") else float("nan")
    def Rj_of(D):
        if not math.isfinite(D):
            return float("nan")
        Dp = D / r12; Meff = xe * (1.0 / y12) * Dp ** 2
        R_ = 5.0
        for _ in range(200):
            M_ = R_ ** 1 / math.sqrt(y12) + 1.0                  # deep isolated M(<R) (units M_b), R >> a
            R_ = Dp * (M_ / (2 * Meff)) ** (1 / 3)
        return R_
    SYS[f].append(dict(name=nm, host=r_["host"], MV=float(r_["M_V"]), xe=xe, y12=y12, r12=r12, Dkpc=float(r_["D_host_kpc"]),
                       Rj=Rj_of(Dm), Rj_peri=Rj_of(rp), dISO=float(r_["Delta_ISO"]), lb0=float(r_["lb0"]),
                       sub=(r_["ell_flag"] == "False" and r_["grad_flag"] == "False" and float(r_["N_q"]) >= 10)))
allR = [s["Rj"] for f in FOOTS for s in SYS[f]] + [s["Rj_peri"] for f in FOOTS for s in SYS[f] if math.isfinite(s["Rj_peri"])]
ally = [s["y12"] for f in FOOTS for s in SYS[f]]
P(f"  R_J/r12 range {min(allR):.2f}-{max(allR):.1f}; y12 range {min(ally):.2e}-{max(ally):.2e}")

# grid of collapse runs (cached stage file; deterministic)
STG = os.path.join(HERE, "ph1_collapse_grid_A1.json")
LY = [-4.0, -3.25, -2.5, -1.75]
LR = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75]
if os.path.exists(STG):                                     # the grid does not depend on --mutate
    GRID = json.load(open(STG))
else:
    GRID = {}
    for ly in LY:
        for lr in LR:
            t1 = time.time()
            GRID[f"{ly},{lr}"] = collapse_ad(10 ** ly, 10 ** lr)
            P(f"   grid y12 1e{ly} R_J 10^{lr}: B {GRID[f'{ly},{lr}']['B']:.3f} c {GRID[f'{ly},{lr}']['c']:.3f} "
              f"({time.time()-t1:.0f} s, {GRID[f'{ly},{lr}']['nstep']} steps)")
    if not MUT:
        json.dump(GRID, open(STG, "w"), indent=1)
# KS2: convergence at a central node
cA = GRID["-2.5,1.0"]["B"]
cB = collapse_ad(10 ** -2.5, 10 ** 1.0, Nd=8000, eps=0.015)["B"]
cC = collapse_ad(10 ** -2.5, 10 ** 1.0, Nd=2000, eps=0.06)["B"]
dconv = max(abs(math.log10(cB / cA)), abs(math.log10(cC / cA)))
check("KS2", dconv <= 0.02, f"(A1 method) B at (1e-2.5, 10): {cA:.3f}; 2x N, eps/2: {cB:.3f}; N/2, 2 eps: {cC:.3f}; max |d log B| {dconv:.3f}", "<= 0.02 dex")
cA2 = GRID["-2.5,1.5"]["B"]
cB2 = collapse_ad(10 ** -2.5, 10 ** 1.5, Nd=8000, eps=0.015)["B"]
cC2 = collapse_ad(10 ** -2.5, 10 ** 1.5, Nd=2000, eps=0.06)["B"]
dconv2 = max(abs(math.log10(cB2 / cA2)), abs(math.log10(cC2 / cA2)))
check("KS2b", dconv2 <= 0.02, f"(A1, largest R_J node) B at (1e-2.5, 31.6): {cA2:.3f}; fine {cB2:.3f}; coarse {cC2:.3f}; max |d log B| {dconv2:.3f}", "<= 0.02 dex")
RES["collapse_grid"] = GRID; RES["KS2"] = dict(B=cA, B_fine=cB, B_coarse=cC, B2=cA2, B2_fine=cB2, B2_coarse=cC2)

lyA = np.array(LY); lrA = np.array(LR)
TB = np.array([[math.log10(GRID[f"{ly},{lr}"]["B"]) for lr in LR] for ly in LY])
TC = np.array([[math.log10(GRID[f"{ly},{lr}"]["c"]) for lr in LR] for ly in LY])


def bilin(T, ly, lr):
    ly = min(max(ly, lyA[0]), lyA[-1]); lr = min(max(lr, lrA[0]), lrA[-1])
    i = min(np.searchsorted(lyA, ly) - 1, len(lyA) - 2); i = max(i, 0)
    j = min(np.searchsorted(lrA, lr) - 1, len(lrA) - 2); j = max(j, 0)
    u_ = (ly - lyA[i]) / (lyA[i + 1] - lyA[i]); w_ = (lr - lrA[j]) / (lrA[j + 1] - lrA[j])
    return (1 - u_) * (1 - w_) * T[i, j] + u_ * (1 - w_) * T[i + 1, j] + (1 - u_) * w_ * T[i, j + 1] + u_ * w_ * T[i + 1, j + 1]


def logB_obs(s, Rkey="Rj"):
    """map observed (final) y12, R_J/r12 to the initial grid coordinates by fixed point on the contraction c."""
    ly_f, lr_f = math.log10(s["y12"]), math.log10(s[Rkey])
    ly_i, lr_i = ly_f, lr_f
    for _ in range(30):
        lc = bilin(TC, ly_i, lr_i)                           # r12_f = c r12_i  => y_f = y_i c^-2, R_f = R_i / c
        ly_i, lr_i = ly_f + 2 * lc, lr_f + lc
    return bilin(TB, ly_i, lr_i), bilin(TC, ly_i, lr_i)


rng = np.random.default_rng(20261024)


def boot_med(x, nb=4000):
    x = np.asarray(x, float); idx = rng.integers(0, len(x), (nb, len(x)))
    b = np.median(x[idx], axis=1); return float(np.median(x)), float(np.std(b))


def ols_slope(res, lx, mv, nb=4000):
    X = np.column_stack([np.ones(len(res)), lx, mv]); res = np.asarray(res)
    beta = np.linalg.lstsq(X, res, rcond=None)[0]
    bs = []
    for _ in range(nb):
        i = rng.integers(0, len(res), len(res))
        bs.append(np.linalg.lstsq(X[i], res[i], rcond=None)[0][1])
    return float(beta[1]), float(np.std(bs))


Z2R = {}
okKZ = True
Z2REF = {"canonical": 0.450, "alt": 0.409}
for f in FOOTS:
    S_ = SYS[f]; sub = [s for s in S_ if s["sub"]]
    for s in S_:
        s["logB"], s["logc"] = logB_obs(s)
        s["logB_peri"] = logB_obs(s, "Rj_peri")[0] if math.isfinite(s["Rj_peri"]) else float("nan")
        # EN normal subhalo, Newtonian, on the present stellar mass, truncated at R_J
        Ms_kg = s["y12"] * A0[f] * s["r12"] ** 2 / G
        gr = GRO["A_c2b"]; H0 = gr["h"] * 100e3 / KPC / 1e3
        Mt = gr["fn_min"] * (WC / WB) * Ms_kg; vn = (10 * G * H0 * Mt) ** (1 / 3)
        gNn = vn ** 2 / s["r12"]
        gNb = 0.5 * s["y12"] * A0[f]
        lgobs = s["lb0"] + math.log10(gNb)
        s["res_EN"] = lgobs - math.log10(gNb + gNn)
        s["res_EC"] = s["dISO"] - s["logB"]
        s["res_EC_peri"] = s["dISO"] - s["logB_peri"] if math.isfinite(s["logB_peri"]) else float("nan")
    nsub = len(sub)
    mISO = boot_med([s["dISO"] for s in sub])
    okKZ &= nsub == 19 and abs(mISO[0] - Z2REF[f]) <= 0.05
    row = dict(N_sub=nsub, ISO=mISO, EC=boot_med([s["res_EC"] for s in sub]),
               EC_peri=boot_med([s["res_EC_peri"] for s in sub if math.isfinite(s["res_EC_peri"])]),
               EN=boot_med([s["res_EN"] for s in sub]),
               EC_all_MW_M31=boot_med([s["res_EC"] for s in S_ if s["host"] in ("MW", "M31")]),
               ISO_all_MW_M31=boot_med([s["dISO"] for s in S_ if s["host"] in ("MW", "M31")]),
               logB_sub_median=float(np.median([s["logB"] for s in sub])),
               logc_sub_median=float(np.median([s["logc"] for s in sub])))
    hosted = [s for s in S_ if s["host"] in ("MW", "M31")]
    row["slope_EC"] = ols_slope([s["res_EC"] for s in hosted], [math.log10(s["xe"]) for s in hosted], [s["MV"] for s in hosted])
    row["slope_ISO"] = ols_slope([s["dISO"] for s in hosted], [math.log10(s["xe"]) for s in hosted], [s["MV"] for s in hosted])
    def cls(m):
        return "CONSISTENT" if abs(m[0]) <= 2 * m[1] else ("ABOVE" if m[0] > 0 else "BELOW")
    row["class_EC"] = cls(row["EC"]); row["class_EN"] = cls(row["EN"]); row["class_ISO"] = cls(row["ISO"])
    row["class_EC_peri"] = cls(row["EC_peri"])
    row["slope_EC_ok"] = abs(row["slope_EC"][0]) <= 2 * row["slope_EC"][1]
    Z2R[f] = row
    P(f"  {f}: C2-C4 N {nsub}: ISO {mISO[0]:+.3f} +- {mISO[1]:.3f} ({row['class_ISO']}); median log B {row['logB_sub_median']:+.3f}, "
      f"stellar contraction log c {row['logc_sub_median']:+.3f}")
    P(f"     EC freeze-out (radial collapse, present D): residual {row['EC'][0]:+.3f} +- {row['EC'][1]:.3f} -> {row['class_EC']}; "
      f"pericentre R_J: {row['EC_peri'][0]:+.3f} +- {row['EC_peri'][1]:.3f} -> {row['class_EC_peri']}")
    P(f"     EC host-field slope at fixed M_V (MW+M31, N {len(hosted)}): {row['slope_EC'][0]:+.3f} +- {row['slope_EC'][1]:.3f} "
      f"(ISO's {row['slope_ISO'][0]:+.3f} +- {row['slope_ISO'][1]:.3f})  -> {'flat OK' if row['slope_EC_ok'] else 'NOT flat'}")
    P(f"     EN normal subhalo (fair share of present stars, f_n,min): residual {row['EN'][0]:+.3f} +- {row['EN'][1]:.3f} -> {row['class_EN']}")
check("KZ", okKZ, f"C2-C4 N {[Z2R[f]['N_sub'] for f in FOOTS]}; median Delta_ISO {[round(Z2R[f]['ISO'][0],3) for f in FOOTS]} "
      f"vs Z2 {list(Z2REF.values())}", "N 19, |d| <= 0.05")
RES["Z2"] = Z2R
RES["Z2_systems"] = {f: [{k_: v for k_, v in s.items()} for s in SYS[f]] for f in FOOTS}

# ============================================================== verdicts
P("\nROW VERDICTS")
V = {}
gA = GRO["A_c2b"]; gB = GRO["B_cfg886"]
V["F3 growth"] = dict(EC=f"FAIL: ratio {gA['ratio_EC_fn0']:.3f} / {gB['ratio_EC_fn0']:.3f} (line 0.95)",
                      EN=f"PASS only as an INITIAL CONDITION f_n >= {gA['fn_min']:.3f} / {gB['fn_min']:.3f} (+1 IC)")
for bg in GRO:
    pass
enp = all(P4R[f][f"EN_{bg}"]["line"] for f in FOOTS for bg in GRO)
V["P4 isolated RAR"] = dict(EC="PASS if no merger debris (control); lambda_max " + " / ".join(f"{P4R[f]['EC_lambda_max']:.2f}" for f in FOOTS),
                            EN=("PASS" if enp else "FAIL") + ": " + "; ".join(
                                f"{f} rms {P4R[f]['EN_A_c2b']['rms']:.3f} U {P4R[f]['EN_A_c2b']['U_median']:.2f}" for f in FOOTS))
ecz = [Z2R[f]["class_EC"] for f in FOOTS]
V["Z2 satellites"] = dict(EC=("PASS" if all(c == "CONSISTENT" for c in ecz) and all(Z2R[f]["slope_EC_ok"] for f in FOOTS)
                              else ("FAIL" if all(c == "ABOVE" for c in ecz) else "MIXED")) + f": {ecz}",
                          EN=f"{[Z2R[f]['class_EN'] for f in FOOTS]}")
V["F1 cluster cores"] = dict(EC="FAIL (REUSED X2): members' released debris is ADDED to the cluster law (khronon still holds); X2: added overshoots",
                             EN="FAIL (REUSED X2/X6): fair-share normal mass sources the law like baryons (X6 C1b 'CDM under another name'); X2 added form fails")
V["U1 TDGs / DF2-DF4"] = dict(EC="PASS (REUSED U1 B0 +0.055 +- 0.114): born at V_rel >> v_c, no condensate", EN="PASS for TDGs (gas-born); DF2/DF4 history-dependent")
V["Solar System / globulars"] = dict(EC="PASS (REUSED O1 VS)", EN="PASS for the condensate; an ambient normal component is CDM-like (Y1: ambient gate ratio 7.4e-4)")
for k_, v in V.items():
    P(f"  {k_:26s} EC: {v['EC']}\n  {'':26s} EN: {v['EN']}")
RES["verdicts"] = V
P("\nCONSTANT COUNT: EC adds none (v_c from L*, FITTED but allowed) but has no early-normal phase (growth FAIL);")
P("  EN needs +1 initial condition (f_n) and, for a field-level normal phase on dwarf scales, a wave scale mu^-1 <= ~3e-3 pc (NEW).")

check("RSS", rss_gb() < 1.0, f"peak RSS {rss_gb():.3f} GB", "< 1 GB")
RES["checks"] = CHECKS; RES["runtime_s"] = time.time() - T0; RES["peak_rss_gb"] = rss_gb()
P(f"\nchecks {sum(c['ok'] for c in CHECKS.values())}/{len(CHECKS)} pass; runtime {time.time()-T0:.0f} s")
json.dump(RES, open(os.path.join(HERE, f"ph1_two_phase_results{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"ph1_two_phase{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
sys.exit(0 if all(c["ok"] for c in CHECKS.values()) else 1)
