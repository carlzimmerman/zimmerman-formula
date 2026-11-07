#!/usr/bin/env python3
"""FA2 (FROZEN_CRITERIA.md, origin 614f4404cb): grade the top three local-action candidates of IDEAS.md.
    nice -n 15 python3 fa2.py            -> fa2.json / fa2.out
    nice -n 15 python3 fa2.py --mutate   -> fa2_MUTATE.json / fa2_MUTATE.out
C1 profile-length key (any F of the local field length ell), C2 Yukawa-screened phantom (range L2), C3 two-branch
balance (S-shaped h = mu x). Read-only reuse: GB1 battery source (up to its main block), QX5 lensing loader, SV5 web
functions and JSON, WL1 stage-2 output, QX7 iter_4 baseline. One thread, < 1 GB, preemptible.
kappa = 1/2 FITTED; not theory closed; footings never pooled. Adopts nothing."""
import os, sys, json, math, io, re, contextlib, signal
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
import sympy as sp

signal.signal(signal.SIGTERM, lambda *a: sys.exit(143))
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL = os.path.join(REPO, "closure_2026_11_06"); C7 = os.path.join(REPO, "closure_2026_11_07")
MUT = "--mutate" in sys.argv; TAG = "fa2_MUTATE" if MUT else "fa2"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

# ------------------------------------------------------------- GB1 battery source up to its main block (read-only)
GB = os.path.join(CL, "GB1_all_gates_battery", "gb1.py"); src = open(GB).read()
cut = src.index("# ------------------------------------------------------------------ main")
NS = {"__file__": GB, "__name__": "gb1_lib"}; argv0 = sys.argv; sys.argv = [GB]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], GB, "exec"), NS)
sys.argv = argv0
_i, _j = src.index("def short(g, r):"), src.index("for cn, mk in CANDS.items():")
exec(compile(src[_i:_j], GB, "exec"), NS)
G, MS, PC, KPC, A0 = NS["G"], NS["MS"], NS["PC"], NS["KPC"], NS["A0"]
MPC = 1e6 * PC
LE = NS["NS"]["lensing"]()                                       # QX5's 59 KiDS isolated-lens points
GB1J = json.load(open(os.path.join(CL, "GB1_all_gates_battery", "gb1.json")))
SV1 = json.load(open(os.path.join(CL, "SV5_growth_mechanism", "iter_1_law_on_web", "sv5_iter1.json")))
Q7 = json.load(open(os.path.join(CL, "QX7_unified_cold_switch", "iter_4_late_evaporation", "qx7_iter4.json")))
WL1OUT = open(os.path.join(C7, "WL1_web_law_switch", "wl1.out")).read()
def glaw(g, a0): return 0.5 * g + np.sqrt(0.25 * g * g + a0 * np.maximum(g, 0.0))
def nu(x): return 0.5 + math.sqrt(0.25 + 1.0 / x)
RES = dict(lane="FA2", criteria="614f4404cb (origin) + A1", tag=TAG, note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, sympy={}, C1={}, C2={}, C3={})
P(f"FA2 {'MUTATE' if MUT else 'MAIN'}: local-action candidates C1 / C2 / C3. kappa = 1/2 FITTED; not theory closed.")

# ============================================================= sympy statements
x, a0s, Gs, rho, m, L2s, beta, V, r = sp.symbols("x a0 G rho m L2 beta V r", positive=True)
Phi, psi = sp.Function("Phi"), sp.Function("psi")
nuf = sp.Function("nu")
class Q(sp.Function):            # QUMOND potential: Q'(z) = nu(sqrt z)
    def fdiff(self, argindex=1): return nuf(sp.sqrt(self.args[0]))
# (C2) massive QUMOND, 1D reduction of the same structure: L = -rho Phi - (1/8piG)[2 Phi' psi' - a0^2 Q(psi'^2/a0^2) - m^2 (Phi-psi)^2]
Lag = -rho * Phi(x) - (2 * Phi(x).diff(x) * psi(x).diff(x) - a0s ** 2 * Q(psi(x).diff(x) ** 2 / a0s ** 2) - m ** 2 * (Phi(x) - psi(x)) ** 2) / (8 * sp.pi * Gs)
from sympy.calculus.euler import euler_equations
eqs = euler_equations(Lag, [Phi(x), psi(x)], x)
eP = sp.simplify(eqs[0].lhs.doit()); eS = sp.simplify(eqs[1].lhs.doit())
psi2 = sp.solve(eP, psi(x).diff(x, 2))[0]                          # psi'' from varying Phi
Phi2 = sp.solve(eS, Phi(x).diff(x, 2))[0]                          # Phi'' from varying psi
nuexpr = nuf(sp.sqrt(psi(x).diff(x) ** 2 / a0s ** 2))
target = 4 * sp.pi * Gs * rho + sp.diff((nuexpr - 1) * psi(x).diff(x), x)
resid = sp.simplify((Phi2 - target).subs(psi(x).diff(x, 2), psi2).doit().subs(psi(x).diff(x, 2), psi2))
psi_rel = sp.simplify(psi2 - (4 * sp.pi * Gs * rho - m ** 2 * (Phi(x) - psi(x))))
c2_ok = (resid == 0) and (psi_rel == 0)
RES["sympy"]["C2_natural_massive_qumond"] = dict(Phi_identity_residual=str(resid), psi_eq_residual=str(psi_rel), no_screening=bool(c2_ok))
P(f"SYMPY C2: massive QUMOND -> Phi'' = 4piG rho + [(nu-1) psi']' residual {resid}; psi'' = 4piG rho - m^2 (Phi - psi) residual {psi_rel} "
  f"-> {'NATURAL FORM DOES NOT SCREEN' if c2_ok else 'IDENTITY NOT REPRODUCED'}")
# (C3) linearised AQUAL flux mu(|g|/a0) g_i: eigenvalues along g and across it
g1, g2, g3 = sp.symbols("g1 g2 g3", real=True); mu = sp.Function("mu")
gv = sp.Matrix([g1, g2, g3]); gn = sp.sqrt(g1 ** 2 + g2 ** 2 + g3 ** 2)
flux = gv * mu(gn / a0s); Jm = flux.jacobian(gv).subs({g2: 0, g3: 0})
lam_r = sp.simplify(Jm[0, 0].subs(g1, a0s * x)); lam_t = sp.simplify(Jm[1, 1].subs(g1, a0s * x))
h = mu(x) * x; c3_ok = sp.simplify(lam_r - sp.diff(h, x)) == 0 and sp.simplify(lam_t - h / x) == 0
# explicit S-shaped member as a witness: h(x) = x^2/(1+x) + c x exp(-k ln(x/xc)^2) has a falling segment
xs = np.geomspace(1e-3, 1e3, 200001); hS = xs ** 2 / (1 + xs) + 1.0 * xs * np.exp(-4 * np.log(xs) ** 2)
dh = np.gradient(hS, xs); fall = xs[dh < 0]
RES["sympy"]["C3_flux_eigenvalues"] = dict(radial=str(lam_r), transverse=str(lam_t), radial_is_hprime=bool(c3_ok),
                                           witness_falling_segment=[float(fall.min()), float(fall.max())] if len(fall) else None)
P(f"SYMPY C3: flux Jacobian eigenvalues radial = h'(x), transverse = h/x -> {'CONFIRMED' if c3_ok else 'NOT CONFIRMED'}; "
  f"S-shaped witness falls on x in [{fall.min():.3g}, {fall.max():.3g}] (radial coefficient < 0: non-elliptic, WP FAIL by Rolle for every two-branch h)")
# (C4) polynomial (div A)^2 L2^2 term on a flat curve: d/dr(lap psi) = -2 g / r^2 -> correction ~ (L2/r)^2
psir = V ** 2 * sp.log(r); lap = sp.diff(r ** 2 * sp.diff(psir, r), r) / r ** 2
c4 = sp.simplify(sp.diff(lap, r) / (sp.diff(psir, r) / r ** 2))
RES["sympy"]["C4_flat_curve"] = dict(dlap_over_g_over_r2=str(c4), ok=bool(c4 == -2))
P(f"SYMPY C4: flat curve d(lap psi)/dr = {c4} g/r^2 -> correction -2 beta L2^2/r^2 falls outward (UV class, Lstar's kind): {'CONFIRMED' if c4 == -2 else 'NO'}")

# ============================================================= battery + features
def ell_pm(xv, rr, a0):
    """point-mass law: ell = r / |d ln g_law / d ln r|, g_N ~ r^-2."""
    gN = xv * a0; e = 1e-4; s = -2 * (math.log(glaw(gN * (1 + e), a0)) - math.log(glaw(gN * (1 - e), a0))) / (math.log(1 + e) - math.log(1 - e))
    return rr / abs(s)
def ell_profile(rr, gN, a0):
    gl = glaw(np.asarray(gN), a0); s = np.gradient(np.log(gl), np.log(np.asarray(rr)))
    return np.asarray(rr) / np.maximum(np.abs(s), 1e-3)
def ell_efe(ft):
    xe, xi0, rh = ft["xe"], ft["x"], ft["r"]
    if xe is None or xi0 is None or rh is None: return None
    xi = xi0 * nu(xe)
    return rh * math.sqrt(xe ** 2 + xi ** 2) / (2 * xi)

def battery(f, a0):
    S, E, X = NS["build"](f, a0); GRp = {0: NS["groups_pts"](a0, 0.0), 1: NS["groups_pts"](a0, 1.0)}
    U = NS["udgs"](f, a0); D = NS["dsphs"](f, a0); K = NS["kids"](a0)
    st = NS["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=U, D=D, K=K, sigU=sigU); B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S])))
    # --- ell + observed D on every feature
    k = 0
    for gx in NS["SP"]:
        n = len(gx["R"]); rr = gx["R"]; gN = gx["vb2"] / rr
        el = ell_profile(rr, gN, a0) if n > 1 else [ell_pm(gN[0] / a0, rr[0], a0)]
        for i in range(n): S[k + i]["feat"]["ell"] = float(el[i]); S[k + i]["feat"]["Dobs"] = S[k + i]["D"]
        k += n
    assert k == len(S)
    for j, e in enumerate(NS["EL"]):
        for q, mm in enumerate((2, 4, 8)):
            p = E[3 * j + q]; rk = mm * e["Re"]; rr = np.array([rk * (1 - 1e-3), rk * (1 + 1e-3)])
            gN = np.array([G * e["Mbar"](t) * MS / (t * KPC) ** 2 for t in rr]); p["feat"]["ell"] = float(ell_profile(rr * KPC, gN, a0).mean()); p["feat"]["Dobs"] = p["D"]
    names = [z["name"] for z in NS["XC"]]
    for nm in sorted(set(names)):
        ids = [i for i, z in enumerate(NS["XC"]) if z["name"] == nm]; rr = np.array([NS["XC"][i]["r_kpc"] * KPC for i in ids])
        gN = np.array([G * NS["XC"][i]["M_b"] * MS / rr[q] ** 2 for q, i in enumerate(ids)]); el = ell_profile(rr, gN, a0)
        for q, i in enumerate(ids): X[i]["feat"]["ell"] = float(el[q]); X[i]["feat"]["Dobs"] = X[i]["D"]; X[i]["cl"] = nm
    for fs in (0, 1):
        for gp in GRp[fs]:
            rr = np.array([p["feat"]["r"] for p in gp["pts"]]); gN = np.array([p["feat"]["x"] * a0 for p in gp["pts"]])
            el = ell_profile(rr, gN, a0) if len(rr) > 1 else [ell_pm(gp["pts"][0]["feat"]["x"], rr[0], a0)]
            for q, p in enumerate(gp["pts"]): p["feat"]["ell"] = float(el[q]); p["feat"]["Dobs"] = p["D"]
    for p in U: p["feat"]["ell"] = ell_efe(p["feat"]); p["feat"]["Dobs"] = p["D"]
    for cls, pts in D.items():
        for p in pts:
            ft = p["feat"]; e_ = ell_efe(ft) if ft.get("xe") else None
            ft["ell"] = e_ if e_ is not None else (ell_pm(ft["x"], ft["r"], a0) if ft["x"] and ft["r"] else None); ft["Dobs"] = p["D"]
    Ee, Ll = K
    for q, i in enumerate(NS["K1"]):
        for ft, arr in ((Ee[q], NS["Ek"]), (Ll[q], NS["Lk"])):
            ft["ell"] = ell_pm(ft["x"], ft["r"], a0); ft["Dobs"] = math.log10(4 * NS["GPC"] * arr[i] * PC / glaw(NS["gk"][i], a0))
    kp = []
    for p in LE:
        R = math.sqrt(G * p["Mb"] / p["gbar"]); kp.append(dict(R=R, Mb=p["Mb"], gbar=p["gbar"], gobs=p["gobs"], ell=ell_pm(p["gbar"] / a0, R, a0),
                                                             Dobs=math.log10(p["gobs"] / glaw(p["gbar"], a0))))
    B["KP"] = kp
    return B

def gb1_rows(cand, B, a0):
    row = {}
    for gname, fn, fills in NS["GATES"]:
        row[gname] = NS["run_gate"](fn, cand, B, a0, fills)
    return row
def kg6(B, a0, gfun):
    """mean log10(g_cand / g_base) over the 59 KiDS points, pointwise; gfun(point) -> g_cand."""
    d = [math.log10(gfun(p) / glaw(p["gbar"], a0)) for p in B["KP"]]
    return float(np.mean(d))
def lab(rows):
    fails = sorted({g for f in rows for g, v in rows[f].items() if v == "FAIL"}); nv = sorted({g for f in rows for g, v in rows[f].items() if v == "NO VERDICT"})
    if fails: return "FAIL (" + ", ".join(fails) + ")" + (f"; NO VERDICT ({', '.join(nv)})" if nv else "")
    if nv: return "NO VERDICT (" + ", ".join(nv) + ")"
    return "SURVIVES (" + ", ".join(sorted({g for f in rows for g in rows[f]})) + ")"

# ============================================================= known answers
BATT = {}; kaok = True
for f, a0 in A0.items():
    B = battery(f, a0); BATT[f] = B
    cm = dict(X=np.mean([p["D"] for p in B["X"]]), E=np.mean([p["D"] for p in B["E"]]), S=np.mean([p["D"] for p in B["S"]]),
              G0=np.mean([p["D"] for g in B["GR"][0] for p in g["pts"]]), G1=np.mean([p["D"] for g in B["GR"][1] for p in g["pts"]]))
    ref = GB1J["KA"][f]["KA1"]["class_means"]; d1 = max(abs(cm[k] - ref[k]) for k in cm)
    L0 = NS["L0"](f, a0); rows0 = gb1_rows(L0, B, a0); st0 = {g: v["status"] for g, v in rows0.items()}
    stref = {g: GB1J["cands"]["L0"][f][g]["status"] for g in st0}
    base = float(np.mean([p["Dobs"] for p in B["KP"]])); dk = abs(base - Q7["baselines"][f]["L"])
    ln = ell_pm(1e4, 1.0, a0); ld = ell_pm(1e-8, 1.0, a0)                      # A1: deep check at y 1e-8
    gN4 = 1e-4 * a0; gl4 = glaw(gN4, a0); dg4 = 0.5 + (0.25 * gN4 + 0.5 * a0) / math.sqrt(0.25 * gN4 ** 2 + a0 * gN4)
    l4 = ell_pm(1e-4, 1.0, a0); l4a = 1.0 / (2 * gN4 * dg4 / gl4)                 # A1: analytic law-S match at y 1e-4
    ka = dict(GB1_means_maxdiff=float(d1), GB1_status_equal=bool(st0 == stref), KIDS_base=base, KIDS_diff=dk,
              ell_newton=ln, ell_deep_1e8=ld, ell_1e4=l4, ell_1e4_analytic=l4a,
              ok=bool(d1 <= 1e-9 and st0 == stref and dk <= 1e-9 and abs(ln - 0.5) <= 1e-3 and abs(ld - 1.0) <= 1e-3 and abs(l4 - l4a) <= 1e-6))
    B["L0rows"] = rows0; RES["KA"][f] = ka; kaok &= ka["ok"]
    P(f"[{f}] KA-GB1 L0 means max|d| {d1:.1e}, statuses equal {st0 == stref}; KA-K KiDS base {base:.6f} vs QX7 {Q7['baselines'][f]['L']:.6f} |d| {dk:.1e}; "
      f"KA-ell point mass r/2 -> {ln:.4f}, deep (y 1e-8) r -> {ld:.5f}, y 1e-4 {l4:.6f} vs analytic {l4a:.6f} => {'PASS' if ka['ok'] else 'FAIL'}")
rp = {f: float(re.search(rf"\[{f}\] stage 2 z 1\.0: .*?r_pop ([0-9.]+)", WL1OUT).group(1)) for f in A0}
rsv = {f: SV1["foot"][f]["proj"]["r"] for f in A0}
ka_w = bool(round(rsv["canonical"], 4) == 74.7424 and round(rsv["alt"], 1) == 89.4 and rp["canonical"] == 3.75 and rp["alt"] == 4.32)
RES["KA"]["SV5_WL1"] = dict(r_sv5=rsv, r_pop=rp, ok=ka_w); kaok &= ka_w
P(f"KA-SV5 r {rsv['canonical']:.4f} / {rsv['alt']:.4f}; KA-WL1 r_pop(z 1) {rp['canonical']} / {rp['alt']} -> {'PASS' if ka_w else 'FAIL'}")
if not kaok:
    P("KA FAIL: stop; nothing graded."); RES["graded"] = False
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float); open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(2)
RES["graded"] = True
def binof(v): return int(math.floor(math.log10(v) / 0.2))      # dimensionless (y)
def binl(e): return int(math.floor(math.log10(e / KPC) / 0.2))  # ell in kpc

# ============================================================= C1: any F of the local field length ell
def Freq(D, xv, a0):
    gN = xv * a0; gl = glaw(gN, a0); return (10 ** D * gl - gN) / (gl - gN)
def c1_oracle(B, a0, xdata):
    byb = {}
    for p, D in zip(B["X"], xdata): byb.setdefault(binl(p["feat"]["ell"]), []).append(Freq(D, p["feat"]["x"], a0))
    Fb = {b: float(np.median(v)) for b, v in byb.items()}
    def Fgen(t): return {b: 1 + t * (v - 1) for b, v in Fb.items()}
    def xmean(t):
        Ft = Fgen(t); res = []
        for p, D in zip(B["X"], xdata):
            gN = p["feat"]["x"] * a0; gl = glaw(gN, a0); res.append(D - math.log10((gN + Ft[binl(p["feat"]["ell"])] * (gl - gN)) / gl))
        return float(np.mean(res))
    if xmean(1.0) > 0.05: t = 1.0
    elif xmean(0.0) <= 0.05: t = 0.0
    else:
        lo, hi = 0.0, 1.0
        for _ in range(60):
            md = 0.5 * (lo + hi); (hi, lo) = (md, lo) if xmean(md) <= 0.05 else (hi, md)
        t = hi
    return Fb, t, Fgen(t)
def c1_cand(Ft):
    def c(ft):
        e = ft.get("ell")
        if e is None: e = ell_pm(ft["x"], ft["r"], 1.0) if ft.get("x") and ft.get("r") else None   # Solar System (ratio x only)
        return dict(b=1.0, F=float(Ft.get(binl(e), 1.0)) if e else 1.0, T=0.0)
    return c
def run_c1(xmode="data"):
    out = {}; rows = {}
    for f, a0 in A0.items():
        B = BATT[f]; xd = [p["D"] for p in B["X"]] if xmode == "data" else [0.0] * len(B["X"])
        Fb, t, Ft = c1_oracle(B, a0, xd); c = c1_cand(Ft) if xmode != "newton" else NS["NEWTON"](f, a0)
        rw = gb1_rows(c, B, a0)
        def gk(p, Ft=Ft):
            Fv = Ft.get(binl(p["ell"]), 1.0) if xmode != "newton" else 0.0
            gl = glaw(p["gbar"], a0); return p["gbar"] + Fv * (gl - p["gbar"])
        sh = kg6(B, a0, gk); kpass = abs(sh) <= 0.05
        xb = sorted(Fb); share = {}
        for b in xb:
            kk = [p for p in B["KP"] if binl(p["ell"]) == b]; gg = [q for g_ in B["GR"][0] for q in g_["pts"] if binl(q["feat"]["ell"]) == b]
            share[f"{10**(0.2*b):.0f}-{10**(0.2*b+0.2):.0f} kpc"] = dict(F_bin=Fb[b], F_gen=Ft[b], kids_pts=len(kk), kids_meanD=float(np.mean([p["Dobs"] for p in kk])) if kk else None,
                                                                              group_pts=len(gg), group_meanD=float(np.mean([p["D"] for p in gg])) if gg else None)
        W = "FAIL"; out[f] = dict(t=t, bins=share, gb1={g: dict(status=v["status"], num=v["num"]) for g, v in rw.items()}, K_G6=dict(shift=sh, pass_=kpass),
                                  web=dict(r_lower_bound=min(rsv[f], rp[f]), r_L0=rsv[f], r_pop=rp[f], status=W),
                                  ell_kpc={c_: [float(np.min(v)), float(np.max(v))] for c_, v in (("SPARC", [p["feat"]["ell"] / KPC for p in B["S"]]), ("X-COP", [p["feat"]["ell"] / KPC for p in B["X"]]),
                                           ("groups", [p["feat"]["ell"] / KPC for g in B["GR"][0] for p in g["pts"]]), ("KiDS59", [p["ell"] / KPC for p in B["KP"]]),
                                           ("UDG", [p["feat"]["ell"] / KPC for p in B["U"]]), ("ellipticals", [p["feat"]["ell"] / KPC for p in B["E"]]))})
        rows[f] = {g: v["status"] for g, v in rw.items()}; rows[f]["K-G6"] = "PASS" if kpass else "FAIL"; rows[f]["W web"] = W
        if xmode == "data":
            P(f"[{f}] C1 ell ranges (kpc): " + "; ".join(f"{k_} {v[0]:.3g}-{v[1]:.3g}" for k_, v in out[f]["ell_kpc"].items()))
            P(f"[{f}] C1 oracle: X-COP bins {len(Fb)}, generous scaling t {t:.3f}; per bin (F_bin -> F_gen | KiDS pts, mean D | group pts f*0, mean D):")
            for k_, v in share.items():
                P(f"      {k_:>12s}: F {v['F_bin']:.2f} -> {v['F_gen']:.2f} | KiDS {v['kids_pts']:2d} {('%+.3f' % v['kids_meanD']) if v['kids_meanD'] is not None else '  -   '} | groups {v['group_pts']:2d} {('%+.3f' % v['group_meanD']) if v['group_meanD'] is not None else '  -  '}")
        P(f"[{f}] C1{'' if xmode == 'data' else ' MUTATE ' + xmode} K-G6 shift {sh:+.4f} (line |.| <= 0.05) -> {'PASS' if kpass else 'FAIL'} (margin {0.05 - abs(sh):+.4f})")
        for g, v in rw.items(): P(f"[{f}] C1{'' if xmode == 'data' else ' ' + xmode} {g:17s} {v['status']:10s} {NS['short'](g, v)}")
        P(f"[{f}] C1 W web: F = 1 on web scales -> r = L0 {rsv[f]:.1f}; any variant keeping F >= 1 inside R_ms -> r >= r_pop {rp[f]} (line 1.072) -> FAIL")
    return out, rows

# ============================================================= C2: Yukawa-screened phantom
def yuk_force(r, s, dm, L):
    """inward force at radius r from Yukawa shells (radius s, mass dm), range L (G factored out)."""
    if not np.isfinite(L): return float(np.sum(dm[s < r]) / r ** 2)
    out = 0.0; a = s < r; b = ~a
    sa, da = s[a], dm[a]
    out += np.sum(da * (L / (2 * sa)) * (np.exp((sa - r) / L) - np.exp(-(sa + r) / L)) * (1 + r / L)) / r ** 2
    sb, db = s[b], dm[b]
    ch = (np.exp((r - sb) / L) + np.exp(-(r + sb) / L)) / 2; sh = (np.exp((r - sb) / L) - np.exp(-(r + sb) / L)) / 2
    out += np.sum(db * (L / sb) * (sh / r ** 2 - ch / (L * r)))
    return float(out)
def phantom_shells(Mb_of_r, rmax, a0, n=6000, rmin=1e-3 * KPC):
    e = np.geomspace(rmin, rmax, n + 1); sm = np.sqrt(e[1:] * e[:-1])
    def Mph(rr):
        M = Mb_of_r(rr); gN = G * M * MS / rr ** 2; return rr ** 2 * (glaw(gN, a0) - gN) / G / MS
    Me = Mph(e); return sm, np.diff(Me), Mph
def F_chi(r, Mb_of_r, L, a0):
    rmax = r + 30 * L if np.isfinite(L) else 2 * r
    s, dm, Mph = phantom_shells(Mb_of_r, max(rmax, 2 * r), a0)
    return yuk_force(r, s, dm, L) / (Mph(r) / r ** 2)
def web_ladder(Ls):
    sys.path.insert(0, os.path.join(CL, "SV5_growth_mechanism"))
    argv0, sys.argv = sys.argv, [os.path.join(CL, "SV5_growth_mechanism", "sv5_web.py")]
    with contextlib.redirect_stdout(io.StringIO()): import sv5_web as SW
    sys.argv = argv0
    W, dV = SW.realise(5); outr = {}
    for f, a0 in A0.items():
        Bz = {L: [] for L in Ls}; ymax = []
        for z in SW.ZG:
            dk, _ = SW.delta_k(W, dV, z); a = 1 / (1 + z); kSI = 1.0 / SW.MPC
            phik = -1.5 * SW.H0s ** 2 * SW.Om * dk / (a * SW.K2 * kSI ** 2); phik[0, 0, 0] = 0
            gc = [np.real(np.fft.ifftn(-1j * Kc * kSI * phik)) / a for Kc in (SW.KX, SW.KY, SW.KZ)]
            gn = np.sqrt(gc[0] ** 2 + gc[1] ** 2 + gc[2] ** 2); n1 = SW.nu(gn / a0) - 1; ymax.append(float(gn.max() / a0))
            Nk = [np.fft.fftn(c) for c in gc]; divN = SW.KX * Nk[0] + SW.KY * Nk[1] + SW.KZ * Nk[2]; del Nk
            Wk = [np.fft.fftn(n1 * c) for c in gc]; divW = SW.KX * Wk[0] + SW.KY * Wk[1] + SW.KZ * Wk[2]; del Wk, gc
            den = SW.shell_mean(np.abs(divN) ** 2); KK2 = SW.KK ** 2
            for L in Ls:
                S = np.ones_like(KK2) if not np.isfinite(L) else (KK2 / (KK2 + 1.0 / L ** 2) if L > 0 else np.zeros_like(KK2))
                Bz[L].append(SW.shell_mean(np.abs(divN + S * divW) ** 2) / den)
            del divN, divW
        outr[f] = {("inf" if not np.isfinite(L) else str(L)): SW.project(Bz[L]) for L in Ls}
    return outr
def run_c2():
    Ls = [math.inf, 30.0, 10.0, 3.0, 1.0, 0.3, 0.1, 0.03, 0.0]
    WR = web_ladder(Ls); out = {}; rows = {}
    keys = [("inf" if not np.isfinite(L) else str(L)) for L in Ls]
    rr = {f: [WR[f][k]["r"] for k in keys] for f in A0}
    kaw = all(abs(rr[f][0] / rsv[f] - 1) <= 1e-6 for f in A0); mono = all(np.all(np.diff(rr[f][:-1]) <= 1e-9) for f in A0)
    mut0 = all(abs(rr[f][-1] - 1) <= 1e-9 for f in A0)
    RES["KA"]["C2_web_inf"] = dict(r=[rr[f][0] for f in A0], ok=bool(kaw))
    for f in A0: P(f"[{f}] C2 web ladder L2 (Mpc) -> r: " + ", ".join(f"{k}: {v:.4g}" for k, v in zip(keys, rr[f])))
    P(f"C2 KA web L2 = inf reproduces SV5 r to 1e-6: {'PASS' if kaw else 'FAIL'}; r monotone in L2: {mono}; L2 = 0 gives r = 1: {mut0}")
    okL = [L for L, k in zip(Ls, keys) if 0 < L and all(WR[f][k]["r"] <= 1.072 for f in A0)]
    Lmax = max(okL) if okL else None
    P(f"C2 L_max (largest listed L2 with r <= 1.072 on both footings) = {Lmax} Mpc")
    for f, a0 in A0.items():
        B = BATT[f]; o = dict(web=dict(zip(keys, rr[f])), L_max_Mpc=Lmax)
        def kids_at(L):
            vals = []; Fs = []
            for p in B["KP"]:
                Mb = p["Mb"] / MS; Fv = F_chi(p["R"], lambda t, Mb=Mb: np.full_like(np.asarray(t, float), Mb), L * MPC, a0) if np.isfinite(L) and L > 0 else (1.0 if not np.isfinite(L) else 0.0)
                Fs.append(Fv); gl = glaw(p["gbar"], a0); vals.append(math.log10((p["gbar"] + Fv * (gl - p["gbar"])) / gl))
            return float(np.mean(vals)), float(max(Fs)), float(min(Fs))
        if MUT:
            s0, _, _ = kids_at(0.0); si, _, _ = kids_at(math.inf)
            o["MUT"] = dict(K_G6_L0=s0, K_G6_inf=si); P(f"[{f}] C2 MUTATE K-G6 at L2 = 0: {s0:+.4f} ({'FAIL' if abs(s0) > 0.05 else 'PASS'}), at L2 = inf: {si:+.4f}")
            out[f] = o; continue
        # check: shell code at L = 1e6 Mpc reproduces the unscreened phantom force
        chk = F_chi(0.3 * MPC, lambda t: np.full_like(np.asarray(t, float), 10 ** 10.5), 1e6 * MPC, a0); o["shell_check_F_at_1e6Mpc"] = chk
        sh, fmax, fmin = kids_at(Lmax) if Lmax else (None, None, None)
        kp = sh is not None and abs(sh) <= 0.05
        # SPARC at L_max: spherical-equivalent phantom per galaxy
        k = 0; fmaxS = 0.0
        for gx in NS["SP"]:
            Rr = gx["R"]; Mpts = gx["vb2"] * Rr / G / MS
            def Mb_of(t, Rr=Rr, Mpts=Mpts): return np.interp(t, np.concatenate([[0.0], Rr]), np.concatenate([[0.0], Mpts]))
            for i in range(len(Rr)):
                Fv = F_chi(Rr[i], Mb_of, Lmax * MPC, a0) if Lmax else 1.0; B["S"][k + i]["feat"]["F_c2"] = Fv; fmaxS = max(fmaxS, Fv)
            k += len(Rr)
        cS = lambda ft: dict(b=1.0, F=ft.get("F_c2", 1.0), T=0.0)
        g1 = NS["run_gate"](NS["g_sparc"], cS, B, a0, [])
        rw = {"G1 SPARC": g1["status"]}
        for g in ("G2 X-COP", "G3 groups", "G4 ellipticals", "G5 Coma UDGs", "G6 dSph classes", "G7 KiDS split"):
            rw[g] = "FAIL" if B["L0rows"][g]["status"] == "FAIL" else "NOT COMPUTED"
        rw["G8 Solar System"] = "PASS"; rw["K-G6"] = "PASS" if kp else "FAIL"; rw["W web"] = "PASS" if Lmax else "FAIL"
        o.update(K_G6=dict(shift=sh, pass_=kp, F_max=fmax, F_min=fmin), G1=g1["num"], F_max_SPARC=fmaxS, rows=rw)
        P(f"[{f}] C2 shell check (L2 1e6 Mpc, R 0.3 Mpc): F {chk:.5f}")
        P(f"[{f}] C2 at L_max {Lmax} Mpc: K-G6 shift {sh:+.4f} (line 0.05) -> {rw['K-G6']} (KiDS F range {fmin:.3f}-{fmax:.3f}); G1 SPARC {g1['status']} {NS['short']('G1 SPARC', g1)} (max F {fmaxS:.3f}); "
          f"G2-G7 L0 FAIL rows stay FAIL (F <= 1 lowers the phantom); G8 PASS")
        out[f] = o; rows[f] = rw
    return out, rows

# ============================================================= C3: two-branch balance
def c3_oracle(B, a0, gr_override=None):
    hot = [(p["feat"]["x"], p["D"], 0.10) for p in B["X"]] + [(p["feat"]["x"], p["D"], 0.15) for p in B["E"]] + [(p["feat"]["x"], p["D"], B["sigU"]) for p in B["U"]]
    for fs in (0, 1):
        for gp in B["GR"][fs]:
            for p in gp["pts"]: hot.append((p["feat"]["x"], p["D"] if gr_override is None else gr_override(p), p["sl"]))
    byb = {}
    for xv, D, s in hot: byb.setdefault(binof(xv), []).append((D, s))
    grid = np.arange(0.0, 1.5001, 0.01); up = {}
    for b, v in byb.items():
        Dv = np.array([d for d, _ in v]); sv = np.array([s for _, s in v])
        cost = [np.sum(np.minimum(Dv ** 2, (Dv - dlt) ** 2) / sv ** 2) for dlt in grid]; up[b] = float(grid[int(np.argmin(cost))])
    return up
def c3_cand(up, newton=False, a0=None):
    def c(ft):
        if newton: return dict(b=1.0, F=0.0, T=0.0)
        du = up.get(binof(ft["x"]), 0.0) if ft.get("x") else 0.0; D = ft.get("Dobs")
        if D is None: return dict(delta=0.0)
        return dict(delta=du if abs(D - du) < abs(D) else 0.0)
    return c
def run_c3(mode="data"):
    out = {}; rows = {}
    for f, a0 in A0.items():
        B = BATT[f]
        if mode == "plant":
            up0 = c3_oracle(B, a0); saved = []
            for fs in (0, 1):
                for gp in B["GR"][fs]:
                    for p in gp["pts"]: saved.append((p, p["D"], p["feat"]["Dobs"])); v = up0.get(binof(p["feat"]["x"]), 0.0); p["D"] = v; p["feat"]["Dobs"] = v
            up = up0
        else: up = c3_oracle(B, a0)
        c = c3_cand(up, newton=(mode == "newton"))
        rw = gb1_rows(c, B, a0)
        def gk(p):
            if mode == "newton": return p["gbar"]
            du = up.get(binof(p["gbar"] / a0), 0.0); dl = du if abs(p["Dobs"] - du) < abs(p["Dobs"]) else 0.0
            return glaw(p["gbar"], a0) * 10 ** dl
        sh = kg6(B, a0, gk); kp = abs(sh) <= 0.05
        rows[f] = {g: v["status"] for g, v in rw.items()}; rows[f]["K-G6"] = "PASS" if kp else "FAIL"; rows[f]["WP"] = "FAIL"; rows[f]["W web"] = "FAIL"
        out[f] = dict(Delta_up={f"{10**(0.2*b):.3g}-{10**(0.2*b+0.2):.3g}": v for b, v in sorted(up.items())}, gb1={g: dict(status=v["status"], num=v["num"]) for g, v in rw.items()},
                      K_G6=dict(shift=sh, pass_=kp), WP="FAIL (radial coefficient h' < 0 on the falling segment; Rolle)", web=dict(r_L0=rsv[f], r_pop=rp[f], status="FAIL"))
        tag = "" if mode == "data" else f" MUTATE {mode}"
        if mode == "data": P(f"[{f}] C3 Delta_up by y bin: " + ", ".join(f"{k_}: {v:.2f}" for k_, v in out[f]["Delta_up"].items()))
        for g, v in rw.items(): P(f"[{f}] C3{tag} {g:17s} {v['status']:10s} {NS['short'](g, v)}")
        P(f"[{f}] C3{tag} K-G6 shift {sh:+.4f} -> {'PASS' if kp else 'FAIL'}; WP FAIL (non-elliptic falling segment); W web lower branch = law r {rsv[f]:.1f} >= r_pop {rp[f]} -> FAIL")
        if mode == "plant":
            for p, d, dd in saved: p["D"] = d; p["feat"]["Dobs"] = dd
    return out, rows

# ============================================================= run
if not MUT:
    RES["C1"]["by_footing"], r1 = run_c1("data"); RES["C1"]["label"] = lab(r1); P(f"LABEL C1: {RES['C1']['label']}")
    RES["C2"]["by_footing"], r2 = run_c2(); r2["sympy"] = {"natural form": "FAIL" if c2_ok else "NO VERDICT"}
    RES["C2"]["label"] = lab(r2) + ("; natural massive-QUMOND form does not screen (sympy)" if c2_ok else ""); P(f"LABEL C2: {RES['C2']['label']}")
    RES["C3"]["by_footing"], r3 = run_c3("data"); RES["C3"]["label"] = lab(r3); P(f"LABEL C3: {RES['C3']['label']}")
    RES["lane_label"] = dict(C1=RES["C1"]["label"], C2=RES["C2"]["label"], C3=RES["C3"]["label"])
else:
    m1, r1 = run_c1("zero"); m2, r1n = run_c1("newton")
    b1 = all(r1[f]["K-G6"] == "PASS" for f in A0) and all(r1n[f]["G1 SPARC"] == "FAIL" for f in A0)
    RES["C1"] = dict(M1=m1, M2=m2, bites=bool(b1)); P(f"C1 MUTATE: M1 (X-COP need 0) K-G6 PASS both footings and M2 Newton G1 FAIL -> {'BITES' if b1 else 'NO BITE'}")
    c2o, _ = run_c2(); b2 = all(abs(c2o[f]["MUT"]["K_G6_L0"]) > 0.05 and abs(c2o[f]["MUT"]["K_G6_inf"]) <= 1e-12 for f in A0)
    RES["C2"] = dict(out=c2o, bites=bool(b2)); P(f"C2 MUTATE: L2 = 0 K-G6 FAIL, L2 = inf shift 0 -> {'BITES' if b2 else 'NO BITE'}")
    p3, r3 = run_c3("plant"); n3, r3n = run_c3("newton")
    b3 = all(r3[f]["G3 groups"] == "PASS" for f in A0) and all(r3n[f]["G1 SPARC"] == "FAIL" for f in A0)
    RES["C3"] = dict(M1=p3, M2=n3, bites=bool(b3)); P(f"C3 MUTATE: M1 planted two-valued groups G3 PASS and M2 Newton G1 FAIL -> {'BITES' if b3 else 'NO BITE'}")
    RES["MUTATE_bites"] = bool(b1 and b2 and b3)
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
