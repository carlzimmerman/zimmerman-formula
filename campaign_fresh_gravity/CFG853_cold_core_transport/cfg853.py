"""CFG853 -- granular (fragment) dynamical-friction transport of the dSph cold core.
Criteria: FROZEN_CRITERIA.md (cbe934afe, committed alone before this script).
Run:  nice -n 19 python3 cfg853.py            -> cfg853.out, cfg853_results.json
      CFG853_MUTATE=1 nice -n 19 python3 cfg853.py  -> cfg853_MUTATE.out, cfg853_results_MUTATE.json
Units: pc, Msun, km/s (G in pc (km/s)^2 / Msun).  numpy/scipy/sympy, one core, seconds.
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, csv, json, math, sys
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG853_MUTATE") == "1"
OUT = []
def P_(s=""):
    print(s, flush=True); OUT.append(str(s))

G_SI, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
G = G_SI * MSUN / (PC * 1e6)                     # pc (km/s)^2 / Msun
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
PF = 64 / 125; SUP = 5.364; FRET = 0.1; STOCK = SUP / FRET
B1 = float(erf(1.0) - 2.0 * math.exp(-1.0) / math.sqrt(math.pi))   # Chandrasekhar B(X=1)
LN10, LN2 = math.log(10.0), math.log(2.0)
NAMES = ["Draco", "Sextans", "Fornax", "Leo I"]

# ---------------------------------------------------------------- inputs (I1-I5)
lvd = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv")))}
c827 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
c824 = json.load(open(os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824_results.json")))["rows"]
c822 = json.load(open(os.path.join(LANES, "CFG822_hex_dsph", "cfg822_results.json")))["rows"]
c861 = {s["name"]: s for s in json.load(open(os.path.join(LANES, "CFG861_classical_dsph_binaries", "cfg861_results.json")))["systems"]}
INP = {}
for n in NAMES:
    r = lvd[n]
    ups = c827[n]["ups"] if n in c827 else 2.0
    so, eso = (c824[n]["so"], c824[n]["eso"]) if n in c824 else (float(r["vlos_sigma"]), float(r["vlos_sigma_em"]))
    INP[n] = dict(MV=float(r["M_V"]), a=float(r["rhalf_sph_physical"]), ups=ups, ups_src="CFG827 SFH" if n in c827 else "assumed 2",
                  sig=so, esig=eso, sig_lvd=float(r["vlos_sigma"]), rta=1000.0 * c822[f"canonical|{n}"]["rta_kpc"],
                  delta861=c861[n]["delta"] if n in c861 else None)

def baseline(n, a0, sig=None, esig=None):
    d = INP[n]; sig = d["sig"] if sig is None else sig; esig = d["esig"] if esig is None else esig
    Ms = d["ups"] * 10 ** (0.4 * (4.83 - d["MV"])); a = d["a"]; R = 4.0 / 3.0 * a
    y = G_SI * PF * Ms * MSUN / (R * PC) ** 2 / a0
    s = min(PF * (math.sqrt(0.25 + 1.0 / y) - 0.5), SUP)
    sig_b = math.sqrt(G * Ms * (PF + s) / (3 * R))
    Mrem = (STOCK - s) * Ms
    need = lambda sg: Ms * (3 * R * sg ** 2 / (G * Ms) - PF - s)
    Mx, A, Mx_lo = need(sig), need(sig + 2 * esig), need(max(sig - 2 * esig, 0.0))
    return dict(name=n, Ms=Ms, a=a, R=R, s=s, y=y, sig_b=sig_b, Mrem=Mrem, Mx=Mx, A=A, Mx_lo=Mx_lo, F=Mx / Mrem,
                sig=sig, esig=esig, Vneed2=3 * sig ** 2, Mneed=3 * R * sig ** 2 / G)

# ---------------------------------------------------------------- model (M1-M4)
class Dw:
    def __init__(self, b, geom, phi, total_bg=False):
        self.b = b; self.Ms, self.a, self.R, self.s = b["Ms"], b["a"], b["R"], b["s"]
        self.rout = INP[b["name"]]["rta"] if geom == "G1" else 5.0 * self.R
        self.mu = b["Mrem"] / (self.rout - self.R); self.phi = phi; self.total_bg = total_bg
    def Mpl(self, r): return self.Ms * r ** 3 / (r * r + self.a ** 2) ** 1.5
    def rhopl(self, r): return 3 * self.Ms / (4 * math.pi * self.a ** 3) * (1 + (r / self.a) ** 2) ** -2.5
    def M(self, r):   # initial static model, r >= R
        return self.Mpl(r) + self.s * self.Ms + self.mu * (min(r, self.rout) - self.R)
    def V(self, r): return math.sqrt(G * self.M(r) / r)
    def rhotot(self, r): return self.rhopl(r) + (self.mu / (4 * math.pi * r * r) if r < self.rout else 0.0)
    def rhol(self, r):
        f = 1.0 if self.total_bg else (1.0 - self.phi)
        return self.rhopl(r) + (f * self.mu / (4 * math.pi * r * r) if r < self.rout else 0.0)
    def dI(self, r):
        V = self.V(r); drV = 0.5 * V + 2 * math.pi * G * r * r * self.rhotot(r) / V
        return drV * V * V / (4 * math.pi * r * self.rhol(r) * B1)
    def I(self, ri):
        if ri <= self.R: return 0.0
        pts = [x for x in (2 * self.R, 5 * self.R, 20 * self.R) if self.R < x < ri]
        return quad(self.dI, self.R, ri, limit=400, points=pts or None, epsrel=1e-9)[0]
    def rF(self, Mx): return self.R + Mx / (self.phi * self.mu)
    def deliver(self, Q):
        if self.I(self.rout) <= Q: rd = self.rout
        else: rd = brentq(lambda r: self.I(r) - Q, self.R, self.rout, xtol=1e-6, rtol=1e-12)
        return rd, self.phi * self.mu * (rd - self.R)
    # T1: quasi-static circular-orbit energy lost crossing [R, min(r,2R)]
    def deps(self, r, initial=False):
        rs = min(r, 2 * self.R); R = self.R; a = self.a
        C = self.s * self.Ms + (0.0 if initial else self.phi * self.mu * (r - R))
        k = self.mu if initial else (1 - self.phi) * self.mu
        Mq = lambda x: self.Mpl(x) + C + k * (x - R)
        pot = G * self.Ms * (1 / math.sqrt(R * R + a * a) - 1 / math.sqrt(rs * rs + a * a)) + G * C * (1 / R - 1 / rs) \
            + G * k * (math.log(rs / R) + R / rs - 1)
        return pot + 0.5 * (G * Mq(rs) / rs - G * Mq(R) / R)
    def dj(self, r):
        rs = min(r, 2 * self.R); R = self.R
        C = self.s * self.Ms + self.phi * self.mu * (r - R); k = (1 - self.phi) * self.mu
        Mq = lambda x: self.Mpl(x) + C + k * (x - R)
        return math.sqrt(G * Mq(rs) * rs) - math.sqrt(G * Mq(R) * R)
    def Esh(self, rF, initial=False):
        return self.phi * self.mu * quad(lambda r: self.deps(r, initial), self.R, rF, limit=400, points=[2 * self.R] if rF > 2 * self.R else None)[0]
    def Jsh(self, rF):
        return self.phi * self.mu * quad(self.dj, self.R, rF, limit=400, points=[2 * self.R] if rF > 2 * self.R else None)[0]
    def Mrecv(self, G0=False):
        light = (1 - self.phi) * self.b["Mrem"] if G0 else (1 - self.phi) * self.mu * (min(3 * self.R, self.rout) - self.R)
        return self.Mpl(3 * self.R) + self.s * self.Ms + light
    def R1_post(self, rF):
        IF = self.I(rF)
        integ = quad(lambda r: IF - self.I(r), self.R, rF, limit=200, epsrel=1e-7)[0]
        return 2 * math.sqrt(math.pi) * 3 * self.phi * self.mu / (4 * math.pi * self.R ** 3 * self.b["sig"]) * integ
    def W_init(self):   # stars truncated at R (p M*), settled M_s(r) = s M* r/R, reservoir mu (r-R) on [R, rout]
        R, Ms, s, a = self.R, self.Ms, self.s, self.a
        Min = lambda r: self.Mpl(r) + s * Ms * r / R
        dMin = lambda r: 4 * math.pi * r * r * self.rhopl(r) + s * Ms / R
        w1 = quad(lambda r: G * Min(r) * dMin(r) / r, 1e-9 * R, R, limit=200)[0]
        Mi = self.Mpl(R) + s * Ms
        w2 = quad(lambda r: G * (Mi + self.mu * (r - R)) * self.mu / r, R, self.rout, limit=200)[0]
        return -(w1 + w2)

# ---------------------------------------------------------------- core evaluation
def evaluate(a0, sigs=None, tol=LN10, phi_mode="common", total_bg=False, initial=False, G0=False, inject=None):
    sigs = sigs or {}
    B = {n: baseline(n, a0, *(sigs.get(n, (None, None)))) for n in NAMES}
    if inject is not None:   # MUTATE: injected dispersions (phi held fixed)
        for n, sg in inject["sig"].items(): B[n] = baseline(n, a0, sg, B[n]["esig"])
    phi = inject["phi"] if inject is not None else max(B["Draco"]["F"], B["Sextans"]["F"])
    res = dict(phi=phi, base={n: {k: B[n][k] for k in ("Ms", "R", "s", "sig", "sig_b", "Mrem", "Mx", "A", "Mx_lo", "F")} for n in NAMES}, geoms={})
    for g in ("G1", "G2"):
        D = {n: Dw(B[n], g, phi, total_bg) for n in NAMES}
        rF = {n: D[n].rF(B[n]["Mx"]) for n in NAMES}
        QD, QS = D["Draco"].I(rF["Draco"]), D["Sextans"].I(rF["Sextans"])
        Qs = max(QD, QS)
        t2 = {}
        for n in NAMES:
            rd, Md = D[n].deliver(Qs)
            t2[n] = dict(rd=rd, Mdel=Md, A=B[n]["A"], ratio=Md / B[n]["A"], ok=Md <= B[n]["A"] * (1 + 1e-9),
                         rVc2=D[n].R * D[n].V(D[n].R) ** 2, rout=D[n].rout, mu=D[n].mu)
        t2pass = all(t2[n]["ok"] for n in NAMES)
        # T2-D: Sextans-independent (phi = F_Draco, Q = Q_Draco, guards only)
        phD = B["Draco"]["F"]; DD = {n: Dw(B[n], g, phD, total_bg) for n in NAMES}
        QDD = DD["Draco"].I(DD["Draco"].rF(B["Draco"]["Mx"]))
        t2d = {}
        for n in ("Fornax", "Leo I"):
            rd, Md = DD[n].deliver(QDD); t2d[n] = dict(Mdel=Md, A=B[n]["A"], ratio=Md / B[n]["A"], ok=Md <= B[n]["A"])
        t2dfail = not all(t2d[n]["ok"] for n in t2d)
        # T1 (+ R1, R3) per dwarf
        t1 = {}
        for n in NAMES:
            ph = B[n]["F"] if phi_mode == "per" else phi
            d = Dw(B[n], g, ph, total_bg); rf = d.rF(B[n]["Mx"])
            if rf > d.rout * (1 + 1e-12): t1[n] = dict(undeliverable=True); continue
            E = d.Esh(rf, initial); Mr = d.Mrecv(G0); de = E / Mr; tl = B[n]["Vneed2"] * tol
            Jsh = d.Jsh(rf); lam = 0.5 * B[n]["sig"] * 1.5 * d.R * Mr / Jsh if Jsh > 0 else float("inf")
            post = d.R1_post(rf)
            t1[n] = dict(rF=rf, Esh=E, Mrecv=Mr, deps=de, tol=tl, ratio=de / tl, ok=de <= tl, lam_crit=lam,
                         R1_post=post, R1_ratio=post / (B[n]["Vneed2"] * LN10), deps_over_sig2=de / B[n]["sig"] ** 2)
        t1fail = any(not t1[n].get("ok", False) for n in ("Draco", "Sextans"))
        res["geoms"][g] = dict(Q_Draco=QD, Q_Sextans=QS, Qstar=Qs, T2=t2, T2_pass=t2pass, T2D=t2d, T2D_fail=t2dfail, T1=t1, T1_fail_DS=t1fail)
    G1, G2 = res["geoms"]["G1"], res["geoms"]["G2"]
    if not G1["T2_pass"] and not G2["T2_pass"]:
        cls = "EXCLUDED"
        sub1 = "and stars cannot be the receiver" if (G1["T1_fail_DS"] and G2["T1_fail_DS"]) else "stellar receiver not excluded"
        sub2 = "(Sextans-independent)" if (G1["T2D_fail"] and G2["T2D_fail"]) else "(via Sextans inputs)"
        label = f"{cls} {sub2}, {sub1}"
    elif not G1["T2_pass"] and G2["T2_pass"]:
        label = "CONDITIONAL (compact reservoir only)"
    else:
        label = "VIABLE CANDIDATE" + (", pre-stellar (gas-receiver) epoch only" if G1["T1_fail_DS"] else "")
    res["label"] = label
    return res

def relax_channel(a0, sigs=None):
    sigs = sigs or {}
    out = {}
    for g in ("G1", "G2"):
        for n in ("Draco", "Sextans"):
            b = baseline(n, a0, *(sigs.get(n, (None, None)))); d = Dw(b, g, 1.0)
            Ei = 0.5 * d.W_init()
            row = {}
            for prof, c in (("uniform", 0.6), ("SIS", 1.0)):
                Ef = -0.5 * c * G * b["Mneed"] ** 2 / b["R"]
                Mesc = b["Mrem"] - b["Mx"]
                ereq = (abs(Ef) - abs(Ei)) / Mesc if Mesc > 0 else float("inf")
                row[prof] = dict(Ef_over_Ei=abs(Ef) / abs(Ei), e_req=ereq, e_req_over_half_sig2=ereq / (0.5 * b["sig"] ** 2))
            out[f"{g}|{n}"] = row
    return out

# ---------------------------------------------------------------- controls
def controls():
    ok = True; rep = {}
    # K1 against CE-FM-084 saved results (full precision) and the handoff's printed numbers
    ref = {}
    try:
        rj = json.load(open(os.path.join(REPO, "sol61_push", "cold_final_mile_2026_10_13", "run_084", "results.json")))
        for c in rj["dwarf_cases"]: ref[c["name"]] = c["cases"]["primary"]
    except Exception as e:
        ref = {}
    hand = {"Draco": (4.334, 0.469303, 2.77236e7), "Fornax": (11.242, 0.0130695, 9.90289e8), "Leo I": (7.468, 0.0345131, 1.88437e8),
            "Sextans": (None, 0.988540, 2.53958e7)}
    k1 = {}
    for n in NAMES:
        b = baseline(n, A0["canonical"]); h = hand[n]
        e = dict(sig_b=b["sig_b"], F=b["F"], Mrem=b["Mrem"])
        chk = []
        if h[0] is not None: chk.append(abs(b["sig_b"] / h[0] - 1) <= 1e-4)
        chk.append(abs(b["F"] / h[1] - 1) <= 1e-4)
        chk.append(abs(b["Mrem"] / h[2] - 1) <= 1e-4)
        if n in ref:
            chk.append(abs(b["sig_b"] / ref[n]["baseline_sigma"] - 1) < 1e-9)
            chk.append(abs(b["F"] / ref[n]["additional_fraction_remaining"] - 1) < 1e-9)
            e["ref_sig_b"] = ref[n]["baseline_sigma"]; e["ref_F"] = ref[n]["additional_fraction_remaining"]
        e["pass"] = all(chk); k1[n] = e; ok &= e["pass"]
    rep["K1"] = k1
    # K2 Rosenbluth light-species heating
    import sympy as sp
    v, sg = sp.symbols("v sigma", positive=True); X = v / (sp.sqrt(2) * sg)
    h = sp.erf(X) / v
    expr = sp.simplify(2 * v * sp.diff(h, v) + 2 * h - 4 / sp.sqrt(sp.pi) * X * sp.exp(-X ** 2) / v)
    k2sym = expr == 0
    def h_num(vv, sL):   # Rosenbluth h for unit-density Maxwellian, direct radial quadrature
        f = lambda u: (2 * math.pi * sL ** 2) ** -1.5 * math.exp(-u * u / (2 * sL ** 2))
        a1 = quad(lambda u: f(u) * u * u, 0, vv)[0] / vv; a2 = quad(lambda u: f(u) * u, vv, np.inf)[0]
        return 4 * math.pi * (a1 + a2)
    k2num = []
    for sL, ss in ((1.0, 1.0), (1.0, 0.5), (2.0, 1.3), (0.7, 1.9)):
        dh = lambda vv: (h_num(vv * (1 + 1e-5), sL) - h_num(vv * (1 - 1e-5), sL)) / (2e-5 * vv)
        rate = lambda vv: 4 * math.pi * (2 * vv * dh(vv) + 2 * h_num(vv, sL))          # x G^2 m rho lnL
        fs = lambda vv: 4 * math.pi * vv * vv * (2 * math.pi * ss ** 2) ** -1.5 * math.exp(-vv * vv / (2 * ss ** 2))
        avg = quad(lambda vv: rate(vv) * fs(vv), 1e-6, 12 * max(ss, sL), limit=200, epsrel=1e-10)[0]
        closed = 8 * math.sqrt(2 * math.pi) * sL ** 2 / (sL ** 2 + ss ** 2) ** 1.5
        hcheck = abs(h_num(1.3, sL) - erf(1.3 / (math.sqrt(2) * sL)) / 1.3)
        k2num.append(dict(sL=sL, ss=ss, avg=avg, closed=closed, rel=abs(avg / closed - 1), h_err=hcheck))
    eq = 8 * math.sqrt(2 * math.pi) / 2 ** 1.5
    k2 = dict(sympy_identity=bool(k2sym), cases=k2num, equal_sigma_coeff=eq, four_sqrt_pi=4 * math.sqrt(math.pi),
              pass_=bool(k2sym) and all(c["rel"] < 1e-6 and c["h_err"] < 1e-8 for c in k2num) and abs(eq - 4 * math.sqrt(math.pi)) < 1e-12)
    ok &= k2["pass_"]; rep["K2"] = k2
    # K3 BT08 8.13 coefficient via the same I() machinery in a singular isothermal background
    class SIS(Dw):
        def __init__(self): self.V0 = 10.0; self.R = 100.0; self.total_bg = True; self.phi = 0.0
        def M(self, r): return self.V0 ** 2 * r / G
        def V(self, r): return self.V0
        def rhotot(self, r): return self.V0 ** 2 / (4 * math.pi * G * r * r)
        def rhol(self, r): return self.rhotot(r)
    sis = SIS(); ri = 1000.0
    coef = sis.I(ri) / (G ** 2) / ((ri ** 2 - sis.R ** 2) * sis.V0 / G)    # t G m lnL / ((r^2-R^2) V)
    k3 = dict(coef=coef, BT=1.17, pass_=abs(coef / 1.17 - 1) < 0.01); ok &= k3["pass_"]; rep["K3"] = k3
    # K4 Plummer fraction
    k4v = (4 / 3) ** 3 / ((4 / 3) ** 2 + 1) ** 1.5
    rep["K4"] = dict(frac=k4v, pass_=abs(k4v - 0.512) < 1e-12); ok &= rep["K4"]["pass_"]
    return ok, rep

# ---------------------------------------------------------------- run
def fmt(x, p=3): return f"{x:.{p}g}"
def print_eval(tag, R):
    P_(f"\n  [{tag}] common phi = {R['phi']:.6f}")
    for g in ("G1", "G2"):
        X = R["geoms"][g]
        P_(f"   {g}: Q*/Q_Dra = {X['Qstar'] / X['Q_Draco']:.3f}  (Q_Sex/Q_Dra = {X['Q_Sextans'] / X['Q_Draco']:.3f})")
        P_(f"     T2  {'dwarf':8s} {'r_out':>8s} {'r_d':>8s} {'M_del':>10s} {'A(+2s)':>10s} {'M_del/A':>8s}  ok   R*Vc(R)^2")
        for n in NAMES:
            t = X["T2"][n]
            P_(f"         {n:8s} {t['rout']:8.0f} {t['rd']:8.1f} {t['Mdel']:10.3e} {t['A']:10.3e} {t['ratio']:8.2f}  {'yes' if t['ok'] else 'NO '}  {t['rVc2']:9.0f}")
        P_(f"     T2 {'PASS' if X['T2_pass'] else 'FAIL'};  T2-D (Sextans-independent, phi=F_Dra): " +
           ", ".join(f"{n} M_del/A {X['T2D'][n]['ratio']:.2f}" for n in X["T2D"]) + f" -> {'FAIL' if X['T2D_fail'] else 'pass'}")
        P_(f"     T1  {'dwarf':8s} {'r_F/R':>6s} {'E_sh':>10s} {'M_recv':>10s} {'de*/sig2':>9s} {'de*/tol':>8s} ok   lam_crit  R1 post/tol")
        for n in NAMES:
            t = X["T1"][n]
            if t.get("undeliverable"): P_(f"         {n:8s} undeliverable"); continue
            rr = t["rF"] / R["base"][n]["R"]
            P_(f"         {n:8s} {rr:6.2f} {t['Esh']:10.3e} {t['Mrecv']:10.3e} {t['deps_over_sig2']:9.2f} {t['ratio']:8.2f}  {'yes' if t['ok'] else 'NO '}  {t['lam_crit']:8.3f}  {t['R1_ratio']:9.2f}")
    P_(f"   LABEL: {R['label']}")

P_("CFG853  granular (fragment) dynamical-friction transport of the dSph cold core" + ("   [MUTATE: injected dispersions]" if MUT else ""))
P_(f"  criteria cbe934afe; G = {G:.6e} pc (km/s)^2/Msun; B(1) = {B1:.6f}; stock 53.64 M*; kappa = 1/2 fitted")
okc, CTRL = controls()
P_("\n  CONTROLS")
for n in NAMES:
    k = CTRL["K1"][n]
    P_(f"   K1 {n:8s} sigma_b {k['sig_b']:.6f}  F {k['F']:.7f}  M_rem {k['Mrem']:.6e}" + (f"  (CE-FM-084 saved: {k['ref_sig_b']:.6f}, {k['ref_F']:.7f})" if 'ref_sig_b' in k else "") + f"  -> {'PASS' if k['pass'] else 'FAIL'}")
k2 = CTRL["K2"]
P_(f"   K2 sympy identity 2vh'+2h = (4/sqrt pi) X e^-X^2 / v: {k2['sympy_identity']}; equal-sigma coefficient {k2['equal_sigma_coeff']:.12f} = 4 sqrt(pi) {k2['four_sqrt_pi']:.12f}")
for c in k2["cases"]: P_(f"      sigma_L {c['sL']}, sigma_s {c['ss']}: quadrature {c['avg']:.10f} closed {c['closed']:.10f} rel {c['rel']:.1e}  (h err {c['h_err']:.1e})")
P_(f"   K2 -> {'PASS' if k2['pass_'] else 'FAIL'}")
P_(f"   K3 SIS friction coefficient {CTRL['K3']['coef']:.4f} vs BT08 1.17 -> {'PASS' if CTRL['K3']['pass_'] else 'FAIL'}")
P_(f"   K4 Plummer M(<4a/3)/M = {CTRL['K4']['frac']:.6f} -> {'PASS' if CTRL['K4']['pass_'] else 'FAIL'}")
P_(f"   controls: {'ALL PASS' if okc else 'FAILURE'}")

P_("\n  INPUTS (I1, I2; canonical)")
for n in NAMES:
    d = INP[n]; b = baseline(n, A0["canonical"])
    P_(f"   {n:8s} M_V {d['MV']:6.2f}  a {d['a']:6.1f} pc  R {b['R']:6.1f}  Ups {d['ups']:.5f} ({d['ups_src']})  sigma {d['sig']}+-{d['esig']}  M* {b['Ms']:.3e}  s {b['s']:.3f}  M_rem {b['Mrem']:.3e}  M_x {b['Mx']:.3e}  F {b['F']:.5f}  A {b['A']:.3e}  r_ta {d['rta']:.0f} pc  delta861 {d['delta861']}")

RES = dict(lane="CFG853", criteria_commit="cbe934afe", mutate=MUT, controls_pass=okc, controls=CTRL, footings={})
MAIN = {}
for fo, a0 in A0.items():
    P_(f"\n================ footing {fo} (a0 = {a0:.4e}) ================")
    R = evaluate(a0); MAIN[fo] = R; print_eval(f"{fo} PRIMARY", R)
    out = dict(primary=R, variants={}, relax=relax_channel(a0))
    # R4 variants
    S = INP["Sextans"]
    sig_bc = S["sig"] * 10 ** (S["delta861"] / 2)
    var = {
        "V1 Sextans binary-corrected": dict(sigs={"Sextans": (sig_bc, None)}),
        "V2 Sextans sigma-2err": dict(sigs={"Sextans": (S["sig"] - 2 * S["esig"], None)}),
        "V3 strict tolerance ln2": dict(tol=LN2),
        "V4 per-dwarf phi_i=F_i (T1)": dict(phi_mode="per"),
        "V5 total background (M4)": dict(total_bg=True),
        "V6 initial static potential (T1)": dict(initial=True),
        "V7 G0 receivers (T1)": dict(G0=True),
    }
    P_(f"\n  R4 VARIANTS ({fo})  [T1 D,S de*/tol; T2 status; max guard M_del/A]")
    for k, kw in var.items():
        Rv = evaluate(a0, **kw); out["variants"][k] = Rv
        line = []
        for g in ("G1", "G2"):
            X = Rv["geoms"][g]
            t1s = "/".join("undel" if X["T1"][n].get("undeliverable") else f"{X['T1'][n]['ratio']:.2f}" for n in ("Draco", "Sextans"))
            worst = max(NAMES, key=lambda n: X["T2"][n]["ratio"])
            r1s = "/".join("undel" if X["T1"][n].get("undeliverable") else f"{X['T1'][n]['R1_ratio']:.3g}" for n in ("Draco", "Sextans"))
            line.append(f"{g}: T1 {t1s}  R1 {r1s}  T2 {'PASS' if X['T2_pass'] else 'FAIL'} (worst {worst} {X['T2'][worst]['ratio']:.2f}; Fornax {X['T2']['Fornax']['ratio']:.2f}, Leo I {X['T2']['Leo I']['ratio']:.2f})")
        P_(f"   {k:34s} phi {Rv['phi']:.4f} | " + " | ".join(line) + f" | label: {Rv['label']}")
    # POST-HOC (added after the primary result was seen; reported only, cannot change the class):
    # does ANY common fragment fraction phi rescue T2 / T2-D?  An envelope over an unknown, not a fit.
    P_(f"\n  POST-HOC phi ENVELOPE ({fo}; added after the primary result; reported only)")
    Bp = {n: baseline(n, a0) for n in NAMES}; env = {}
    for g in ("G1", "G2"):
        for mode, lo in (("T2", max(Bp["Draco"]["F"], Bp["Sextans"]["F"])), ("T2-D", Bp["Draco"]["F"])):
            best = None
            for ph in np.linspace(lo, 0.999, 24):
                Dp = {n: Dw(Bp[n], g, ph) for n in NAMES}
                Qd = Dp["Draco"].I(Dp["Draco"].rF(Bp["Draco"]["Mx"]))
                Q = max(Qd, Dp["Sextans"].I(Dp["Sextans"].rF(Bp["Sextans"]["Mx"]))) if mode == "T2" else Qd
                who = NAMES if mode == "T2" else ["Fornax", "Leo I"]
                rat = {n: Dp[n].deliver(Q)[1] / Bp[n]["A"] for n in who}
                worst = max(rat.values()); gmin = min(rat[n] for n in ("Fornax", "Leo I"))
                if best is None or worst < best[1]: best = (float(ph), worst, rat)
            env[f"{g}|{mode}"] = dict(phi_range=[float(lo), 0.999], best_phi=best[0], min_worst_ratio=best[1], ratios_at_best=best[2])
            P_(f"   {g} {mode:5s} phi in [{lo:.4f}, 0.999]: smallest worst-case M_del/A = {best[1]:.2f} at phi {best[0]:.3f} ("
               + ", ".join(f"{n} {v:.2f}" for n, v in best[2].items()) + f") -> {'some phi passes' if best[1] <= 1 else 'no phi passes'}")
    out["posthoc_phi_envelope"] = env
    # R2 relaxation channel
    P_(f"\n  R2 RELAXATION (lump-lump) CHANNEL ({fo})")
    P_(f"   (a) stars gain 0.5*4 sqrt(pi)*0.34 = {0.5 * 4 * math.sqrt(math.pi) * 0.34:.3f} sigma^2 per lump relaxation time (m-independent);"
       f" tolerance reached after {3 * LN10 / (2 * math.sqrt(math.pi) * 0.34):.2f} (ln10) / {3 * LN2 / (2 * math.sqrt(math.pi) * 0.34):.2f} (ln2) relaxation times")
    for k, row in out["relax"].items():
        P_(f"   (b) {k:12s} |E_f|/|E_i| uniform {row['uniform']['Ef_over_Ei']:.2f} (escaper e_req/(sig^2/2) {row['uniform']['e_req_over_half_sig2']:.2f})"
           f"   SIS {row['SIS']['Ef_over_Ei']:.2f} ({row['SIS']['e_req_over_half_sig2']:.2f})")
    for vk in ("V1 Sextans binary-corrected", "V2 Sextans sigma-2err"):
        sg = sig_bc if vk.startswith("V1") else S["sig"] - 2 * S["esig"]
        rr = relax_channel(a0, {"Sextans": (sg, None)}); out[f"relax_{vk}"] = rr
        P_(f"   (b) {vk}: " + "; ".join(f"{k} uniform {rr[k]['uniform']['Ef_over_Ei']:.2f} ({rr[k]['uniform']['e_req_over_half_sig2']:.2f})" for k in rr if "Sextans" in k))
    # D1 diagnostic
    B = {n: baseline(n, a0) for n in NAMES}; order = sorted(NAMES, key=lambda n: B[n]["R"])
    viol = [(i, j, B[i]["Mx_lo"] / B[j]["A"]) for ii, i in enumerate(order) for j in order[ii + 1:] if B[i]["Mx_lo"] > B[j]["A"]]
    P_(f"\n  D1 needed extra (central [lo, allowed]) by R: " + "; ".join(f"{n} R {B[n]['R']:.0f}: {B[n]['Mx']:.2e} [{B[n]['Mx_lo']:.2e}, {B[n]['A']:.2e}]" for n in order))
    P_(f"     one non-decreasing M_x(r) possible: {'YES' if not viol else 'NO'}" + ("" if not viol else "  (violations: " + ", ".join(f"{i} lo > {j} allowed x{r:.2f}" for i, j, r in viol) + ")"))
    out["D1"] = dict(order=order, violations=viol, needs={n: dict(R=B[n]["R"], Mx=B[n]["Mx"], lo=B[n]["Mx_lo"], A=B[n]["A"]) for n in NAMES})
    RES["footings"][fo] = out

if MUT:
    P_("\n================ MUTATE: injected friction-consistent dispersions (phi held at the main-run value) ================")
    bites = {}
    for fo, a0 in A0.items():
        lab = {}
        for g in ("G1", "G2"):
            R0 = MAIN[fo]; phi = R0["phi"]; Bm = {n: baseline(n, a0) for n in NAMES}
            Dm = {n: Dw(Bm[n], g, phi) for n in NAMES}; QD = Dm["Draco"].I(Dm["Draco"].rF(Bm["Draco"]["Mx"]))
            inj = {n: math.sqrt(G * (Bm[n]["Ms"] * (PF + Bm[n]["s"]) + Dm[n].deliver(QD)[1]) / (3 * Bm[n]["R"])) for n in NAMES}
            Rm = evaluate(a0, inject=dict(sig=inj, phi=phi))
            X = Rm["geoms"][g]
            P_(f"   {fo} {g}: injected sigma " + ", ".join(f"{n} {inj[n]:.3f}" for n in NAMES) + f" -> T2 {'PASS' if X['T2_pass'] else 'FAIL'} (" +
               ", ".join(f"{n} {X['T2'][n]['ratio']:.2f}" for n in NAMES) + ")")
            lab[g] = dict(inj=inj, T2_pass=X["T2_pass"], ratios={n: X["T2"][n]["ratio"] for n in NAMES})
        bites[fo] = lab["G1"]["T2_pass"] or lab["G2"]["T2_pass"]
        RES.setdefault("mutate_detail", {})[fo] = lab
        P_(f"   {fo}: MUTATE {'BITES (T2 passes, class changes from EXCLUDED)' if bites[fo] else 'DOES NOT BITE'}")
    RES["mutate_bites"] = bites

P_("\n  SUMMARY")
for fo in A0:
    P_(f"   {fo}: {MAIN[fo]['label']}")
RES["labels"] = {fo: MAIN[fo]["label"] for fo in A0}
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg853_results{sfx}.json"), "w"), indent=1, default=float, sort_keys=True)
open(os.path.join(HERE, f"cfg853{sfx}.out"), "w").write("\n".join(OUT) + "\n")
if MUT: sys.exit(0 if all(RES["mutate_bites"].values()) else 1)
sys.exit(0 if okc else 1)
