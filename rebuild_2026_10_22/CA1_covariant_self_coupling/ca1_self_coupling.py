"""CA1_covariant_self_coupling -- frozen criteria FROZEN_CRITERIA.md (7926bab64c).

Is there a covariant self-coupling of the cold dark energy that gives the core law's s(sigma) ~ sigma^-n with LN2's
normalisation, with a0 / Lambda fixing its scales?  Candidates C0 (contact), C1a (Yukawa, a0/Lambda-tied range), C1b (free
Yukawa: Born, classical, Hulthen reported only), C2 (Hubble-range pair exchange, V = C_p/r^p), C3 (condensate).
MUTATE=1: target n -> n + 0.6 (separate outputs).  kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os, sys, json, math, resource
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import loggamma
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE") == "1"; TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

G, MSUN, PC, YR = 6.674e-11, 1.989e30, 3.0857e16, 3.156e7
C, HBAR, EV = 2.99792458e8, 1.054571817e-34, 1.602176634e-19
KAPPA = 0.5
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
NREC = {"canonical": 0.784, "alt": 0.496}
if MUTATE: NREC = {f: n + 0.6 for f, n in NREC.items()}
SREF = 70.50e3; T_AGE = 13.8e9 * YR; DN = 0.10
SPAN_A, SPAN_B = (20e3, 200e3), (400e3, 1300e3)
KN_SIG = (5e3, 10e3, 20e3, 70.5e3, 1000e3)
V_MERGE, MERGE_MAX = 4700e3, 0.0708          # m/s ; m^2/kg (0.708 cm^2/g, CFG725)
CM2G = 0.1                                   # 1 cm^2/g = 0.1 m^2/kg
E_PL = math.sqrt(HBAR * C**5 / G)
RES = dict(frozen="7926bab64c", mutate=MUTATE, footings={}, checks={})

P(f"CA1_covariant_self_coupling  {'MUTATE run (n -> n + 0.6)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy = field paired with dark energy (scattering = its excitations on")
P("the mass shell, CFG723); not theory closed; nothing here says the data favour the framework or LCDM")

# ---------------------------------------------------------------- thermal average over Maxwellian relative speeds
XG = np.linspace(1e-4, 9.0, 6001)                   # x = v_rel / (2 sigma); weight for <sigma_T v>: x^3 e^-x^2
WG = XG**3 * np.exp(-XG**2)
def s_eff(sigT, sig):
    """s(sigma) = <sigma_T v>/<v> (per mass if sigT is per mass); sigT is a vectorised function of v_rel [m/s]."""
    v = 2 * sig * XG
    return np.trapz(sigT(v) * WG, XG) / np.trapz(WG, XG)
def n_sec(sigT, span):
    a, b = span
    return -math.log(s_eff(sigT, b) / s_eff(sigT, a)) / math.log(b / a)

def target(f, n):
    SA = A0[f] / (2 * math.pi * G)
    K = 9 * SREF**(1 + n) / (4 * math.pi * G * T_AGE * SA**2)
    return K, (lambda sig: math.sqrt(math.pi) / 4 * K * sig**(-n))
def kn(s, sig):
    v = 4 * sig / math.sqrt(math.pi)
    return math.sqrt(4 * math.pi * G * v * T_AGE / s) / sig

# ---------------------------------------------------------------- checks K1-K3
K1 = {}
for f in A0:
    n = NREC[f]; K, st = target(f, n)
    knr = 4 / (3 * math.sqrt(math.pi)) * 2 * A0[f] * T_AGE / SREF
    K1[f] = abs(kn(st(SREF), SREF) / knr - 1)
k2 = max(abs(n_sec(lambda v, k=k: v**(-k), sp_) - k) for k in (0.0, 0.5, 0.8, 4 / 7, 4.0) for sp_ in (SPAN_A, SPAN_B))
def born_shape(v, vst):                       # sigma_T * v^4 / const ; R = v / v*
    R2 = (v / vst)**2
    return (np.log1p(R2) - R2 / (1 + R2)) / v**4
n_lo = n_sec(lambda v: born_shape(v, 1e9), SPAN_A); n_hi = n_sec(lambda v: born_shape(v, 1.0), SPAN_A)
RES["checks"] = dict(K1=max(K1.values()) < 1e-6, K2=k2 < 1e-6, K3=(abs(n_lo) < 0.01 and abs(n_hi - 4) < 0.3))
P(f"K1 Kn(s*(sigma_ref)) vs LN2 closed form: max rel dev {max(K1.values()):.1e} -> {'PASS' if RES['checks']['K1'] else 'FAIL'}")
P(f"K2 thermal average of v^-k returns n_eff = k: max dev {k2:.1e} -> {'PASS' if RES['checks']['K2'] else 'FAIL'}")
P(f"K3 Born Yukawa limits: n_eff(v << v*) {n_lo:.4f}, n_eff(v >> v*) {n_hi:.3f} -> {'PASS' if RES['checks']['K3'] else 'FAIL'}")

# ---------------------------------------------------------------- sympy: exact slopes of C0, C1a (Coulomb), C2
v_, k_, p_, A_, C_, mu_ = sp.symbols("v k p A C mu", positive=True)
slope = lambda expr: sp.simplify(-sp.diff(sp.log(expr), v_) * v_)
sym = dict(C0=slope(A_ + 0 * v_), C2=slope(A_ * (C_ / (mu_ * v_**2 / 2))**(2 / p_)), rutherford=slope(A_ / v_**4))
P(f"sympy slopes -dln(sigma_T)/dln v: contact {sym['C0']}, Coulomb/Rutherford {sym['rutherford']}, power-law V = C/r^p: {sym['C2']}")
# velocity monomial G^a c^b a0^d rho^e t^f with dimension L/T
a, b, d, e, ff = sp.symbols("a b d e f")
sol = sp.solve([-a + e, 3 * a + b + d - 3 * e - 1, -2 * a - b - 2 * d + ff + 1], [b, e, ff], dict=True)[0]
P(f"sympy velocity monomials from (G, c, a0, rho_L, t): b = {sol[b]}, e = {sol[e]}, f = {sol[ff]}  =>  v = c (a0 t/c)^d (G rho_L t^2)^a")
RES["sympy"] = {k: str(v) for k, v in sym.items()} | dict(velocity_monomial={str(k): str(v) for k, v in sol.items()})

# ---------------------------------------------------------------- classical A_p for V = 1/y^p (repulsive), E = 1
def chi_rep(bb, p):
    g = lambda u: 1 - bb**2 * u**2 - u**p
    u0 = brentq(g, 0, 1.0, xtol=1e-15)
    integ = lambda w: 2 * u0 * w * bb / math.sqrt(max(g(u0 * (1 - w * w)), 1e-300))
    I, _ = quad(integ, 0, 1, limit=200, epsabs=1e-12, epsrel=1e-10)
    return math.pi - 2 * I
def A_p(p):
    f = lambda bb: (1 - math.cos(chi_rep(bb, p))) * bb * 2 * math.pi
    I1, _ = quad(f, 1e-9, 3, limit=400); I2, _ = quad(f, 3, 60, limit=400)
    return I1 + I2
AP = {p: A_p(p) for p in (3, 5, 6, 7, 40)}
P("classical momentum-transfer coefficient A_p (sigma_T = A_p (C/E)^(2/p), repulsive): " +
  ", ".join(f"p={p}: {AP[p]:.4f}" for p in AP) + f"  (p -> inf tends to the hard sphere pi = {math.pi:.4f})")
RES["A_p"] = AP

# ---------------------------------------------------------------- per footing
def fmt(x): return f"{x:.3g}"
for f in A0:
    n = NREC[f]; K, st = target(f, n); a0 = A0[f]
    rhoL = a0**2 / (KAPPA**2 * C**2 * G)
    E_L = (rhoL * C**2 * (HBAR * C)**3)**0.25
    sref = st(SREF)
    R = dict(n=n, s_target_ref_m2kg=sref, s_target_ref_cm2g=sref / CM2G, E_Lambda_eV=E_L / EV, cand={})
    P(f"\n=== [{f}] a0 {a0:.4e}; target n {n:.3f}; s*(sigma_ref) = {sref/CM2G:.4f} cm^2/g; E_Lambda = {E_L/EV*1e3:.3f} meV")
    knt = {s: kn(st(s), s) for s in KN_SIG}
    P("  target Kn at 5/10/20/70.5/1000 km/s: " + " / ".join(f"{v:.0f}" for v in knt.values()))
    # micro sigma_T/m giving exactly s*(sigma) for a pure power law k: sigma_T/m = B v^-k
    def micro_pl(k):
        B = sref / s_eff(lambda v: v**(-k), SREF)
        return lambda v: B * v**(-k)

    def grade_shape(name, sigT_m, extra=None, note=""):
        nA, nB = n_sec(sigT_m, SPAN_A), n_sec(sigT_m, SPAN_B)
        g1 = abs(nA - n) <= DN and abs(nB - n) <= DN
        knv = {s: kn(s_eff(sigT_m, s), s) for s in KN_SIG}
        g4 = min(knv.values()) > 1
        merge = float(sigT_m(np.array([V_MERGE]))[0])
        g5 = merge <= MERGE_MAX
        row = dict(nA=nA, nB=nB, G1=g1, Kn=knv, G4=g4, merge_cm2g=merge / CM2G, G5=g5)
        if extra: row.update(extra)
        P(f"  {name:<34} n_eff SPARC {nA:+.3f} clusters {nB:+.3f} -> G1 {'PASS' if g1 else 'FAIL'}; Kn min {min(knv.values()):.0f} "
          f"G4 {'PASS' if g4 else 'FAIL'}; merger {merge/CM2G:.3g} cm^2/g G5 {'PASS' if g5 else 'FAIL'} {note}")
        return row

    # C0 contact
    R["cand"]["C0"] = grade_shape("C0 contact lambda|chi|^4", micro_pl(0.0))
    R["cand"]["C0"].update(G2="solvable (lambda^2/m^3 free)", G3=False, G6=True)

    # C1a Yukawa with a0- or Lambda-tied range
    c1a = {}
    for lab, lam in (("c^2/a0", C**2 / a0), ("c/sqrt(G rho_L)", C / math.sqrt(G * rhoL))):
        rows = []
        for mchi_eV in (1.28e-20, 1e-3, 1.0, 1e9, 1e12, 1e28):
            m = mchi_eV * EV / C**2; vst = HBAR / (m * lam)
            nA, nB = n_sec(lambda v: born_shape(v, vst), SPAN_A), n_sec(lambda v: born_shape(v, vst), SPAN_B)
            # classical large-beta branch: sigma_T >= pi lam^2 (log beta)^2 >~ pi lam^2 ; per mass at the lightest allowed m
            rows.append(dict(m_eV=mchi_eV, v_star=vst, nA=nA, nB=nB, sigT_classical_min_over_m_cm2g=math.pi * lam**2 / m / CM2G))
        nmin = min(min(r["nA"], r["nB"]) for r in rows)
        clsmin = min(r["sigT_classical_min_over_m_cm2g"] for r in rows)
        c1a[lab] = dict(rows=rows, n_eff_min=nmin, classical_branch_min_cm2g=clsmin)
        P(f"  C1a Yukawa range {lab:<16} ({lam:.2e} m): Born/small-beta n_eff >= {nmin:.3f} for m_chi 1.3e-20 eV .. 1e28 eV "
          f"(Coulomb limit) -> G1 FAIL; large-beta branch sigma_T/m >= pi lambda^2/m = {clsmin:.1e} cm^2/g -> G2/G5 FAIL")
    R["cand"]["C1a"] = dict(c1a, G1=False, G2=False, G5=False, G3=False)

    # C1b free Yukawa: shape solves
    vgrid = np.logspace(3, 8, 101)               # v* in m/s
    born_ok = []
    for vst in vgrid:
        sh = lambda v, vst=vst: born_shape(v, vst)
        nA, nB = n_sec(sh, SPAN_A), n_sec(sh, SPAN_B)
        if abs(nA - n) <= DN and abs(nB - n) <= DN: born_ok.append(vst)
    bgrid = np.logspace(-3, 9, 121)              # beta at v_rel = sigma_ref
    def cls_attr(beta):
        beta = np.asarray(beta, float); out = np.empty_like(beta)
        lo, hi = beta < 0.1, beta > 1e3; mid = ~lo & ~hi
        out[lo] = 2 * beta[lo]**2 * np.log1p(beta[lo]**-2)
        bm = beta[mid]
        out[mid] = 7 * (bm**1.8 + 280 * (bm / 10)**10.3) / (1 + 1.4 * bm + 0.006 * bm**4 + 160 * (bm / 10)**10)
        Lb = np.log(beta[hi]); out[hi] = 0.81 * (1 + Lb - 1 / Lb)**2
        return out
    def cls_rep(beta):
        beta = np.asarray(beta, float); out = np.empty_like(beta)
        lo = beta < 1; hi = ~lo
        out[lo] = 2 * beta[lo]**2 * np.log1p(beta[lo]**-2)
        L2 = np.log(2 * beta[hi]); out[hi] = (L2 - np.log(L2))**2
        return out
    cls_ok = {"attractive": [], "repulsive": []}; cls_n = {"attractive": [], "repulsive": []}
    for br in bgrid:
        for lab, fn in (("attractive", cls_attr), ("repulsive", cls_rep)):
            sh = lambda v, fn=fn, br=br: fn(br * (SREF / v)**2)
            nA, nB = n_sec(sh, SPAN_A), n_sec(sh, SPAN_B)
            cls_n[lab].append((br, nA, nB))
            if abs(nA - n) <= DN and abs(nB - n) <= DN: cls_ok[lab].append(br)
    def rng(xs): return [float(min(xs)), float(max(xs))] if xs else None
    P(f"  C1b Born shape: v* meeting G1 on both spans: {('%.3g-%.3g km/s' % (min(born_ok)/1e3, max(born_ok)/1e3)) if born_ok else 'NONE'} "
      f"(v* = m_phi c / m_chi scanned 1-1e5 km/s)")
    for lab in cls_ok:
        best = min(cls_n[lab], key=lambda r: abs(r[1] - n) + abs(r[2] - n))
        P(f"  C1b classical {lab:<10}: beta(sigma_ref) meeting G1: {('%.3g-%.3g' % tuple(rng(cls_ok[lab]))) if cls_ok[lab] else 'NONE'}; "
          f"closest beta {best[0]:.3g}: n_eff {best[1]:+.3f} / {best[2]:+.3f}")
    # Hulthen s-wave (reported only); kappa_H = 1.6; variables v*' = kappa_H m_phi c/m_chi and b' = alpha m_chi/(kappa_H m_phi)
    hul_ok = 0; hul_tot = 0; hul_valid_ok = 0
    for vst in np.logspace(3.5, 7.5, 33):
        for bp in np.logspace(-1, 3, 33):
            def sh(v, vst=vst, bp=bp):
                w = v / vst
                lp = 1 + 0.5j * w + np.sqrt(bp - w**2 / 4 + 0j); lm = 1 + 0.5j * w - np.sqrt(bp - w**2 / 4 + 0j)
                d0 = np.imag(loggamma(1j * w) - loggamma(lp) - loggamma(lm)) + math.pi / 2
                return np.sin(d0)**2 / v**2
            nA, nB = n_sec(sh, SPAN_A), n_sec(sh, SPAN_B); hul_tot += 1
            if abs(nA - n) <= DN and abs(nB - n) <= DN:
                hul_ok += 1
                if 1300e3 / vst <= 1: hul_valid_ok += 1
    P(f"  C1b Hulthen s-wave (reported only): {hul_ok}/{hul_tot} grid cells meet G1; with s-wave validity (w <= 1 to 1300 km/s): {hul_valid_ok}")
    # numerology exponents for a C1b velocity scale
    X1 = a0 * T_AGE / C
    kneed = lambda vel: math.log(vel / C) / math.log(X1)
    R["cand"]["C1b"] = dict(born_vstar_ok=rng(born_ok), classical_beta_ok={k: rng(v) for k, v in cls_ok.items()},
                            hulthen=dict(ok=hul_ok, tot=hul_tot, ok_valid=hul_valid_ok),
                            G1=bool(born_ok or cls_ok["attractive"] or cls_ok["repulsive"]), G3=False,
                            X1_a0t_over_c=X1, k_for_sigma_ref=kneed(SREF))
    if born_ok:
        vmid = math.sqrt(min(born_ok) * max(born_ok))
        R["cand"]["C1b"]["born_mid"] = grade_shape("C1b Born at mid v* (amplitude by G2)",
            (lambda v, B=sref / s_eff(lambda u: born_shape(u, vmid), SREF): B * born_shape(v, vmid)),
            extra=dict(v_star=vmid, k_numerology=kneed(vmid)), note=f"v* {vmid/1e3:.0f} km/s = c (a0t/c)^{kneed(vmid):.2f}")
    for lab, fn in (("attractive", cls_attr), ("repulsive", cls_rep)):
        if cls_ok[lab]:
            bmid = math.sqrt(min(cls_ok[lab]) * max(cls_ok[lab]))
            shp = lambda v, fn=fn, bmid=bmid: fn(bmid * (SREF / v)**2)
            R["cand"]["C1b"][f"cls_{lab}_mid"] = grade_shape(f"C1b classical {lab} mid beta {bmid:.3g}",
                (lambda v, B=sref / s_eff(shp, SREF): B * shp(v)), extra=dict(beta_ref=bmid))
    P(f"  C1b G3: the shape needs one velocity scale (v* or beta_ref) set by m_phi/m_chi and alpha; a0 t/c = {X1:.4f}, so "
      f"sigma_ref = c (a0t/c)^{kneed(SREF):.2f} (non-integer; numerology) -> G3 FAIL")

    # C2 pair exchange, V = C_p / r^p
    c2 = {}
    cp = {3: 1 / (64 * math.pi**3), 5: 1 / (4 * math.pi**3), 7: 1 / (4 * math.pi**3)}
    for p in (3, 5, 6, 7):
        k = 4 / p; sm = micro_pl(k)
        row = grade_shape(f"C2 pair exchange p = {p}{' (reported only)' if p == 6 else ''}", sm)
        Bm = sref / s_eff(lambda v: v**(-k), SREF)          # sigma_T/m = Bm v^-k
        # G6: classical validity k b1 >= 10 at v_rel = 10 km/s, b1 = sqrt(sigma_T/pi): m^(3/2) >= 20 hbar sqrt(pi/(s v)) / v
        v10 = 10e3; s10 = Bm * v10**(-k)
        mmin = (20 * HBAR * math.sqrt(math.pi / s10) / v10)**(2 / 3)
        row["G6_mchi_min_GeV"] = mmin * C**2 / EV / 1e9
        # G2/G3 assignment menu
        menu = []
        if p in cp:
            for Mlab, M in (("E_Lambda", E_L), ("E_Pl", E_PL)):
                for mlab, mc2 in (("E_Lambda", E_L), ("E_Pl", E_PL), ("sqrt(E_L E_Pl)", math.sqrt(E_L * E_PL))):
                    m = mc2 / C**2
                    if p == 3: Cp = cp[3] * (HBAR * C)**3 / mc2**2
                    elif p == 5: Cp = cp[5] * (HBAR * C)**5 / M**4
                    else: Cp = cp[7] * (HBAR * C)**7 / (mc2**2 * M**4)
                    sigT_m = lambda v, Cp=Cp, m=m: AP[p] * (Cp / (m * v**2 / 4))**(2 / p) / m
                    ratio = s_eff(sigT_m, SREF) / sref
                    menu.append(dict(M=Mlab if p != 3 else "-", m=mlab, ratio=ratio, log10=math.log10(ratio)))
            # derived m_chi with M = E_Lambda (p = 5, 7): reported only
            if p in (5, 7):
                def resid(lm):
                    m = 10**lm * EV / C**2; mc2 = m * C**2
                    Cp = cp[5] * (HBAR * C)**5 / E_L**4 if p == 5 else cp[7] * (HBAR * C)**7 / (mc2**2 * E_L**4)
                    sigT_m = lambda v: AP[p] * (Cp / (m * v**2 / 4))**(2 / p) / m
                    return math.log(s_eff(sigT_m, SREF) / sref)
                lm = brentq(resid, -40, 60); row["mchi_needed_if_M_ELambda_eV"] = 10**lm
            if p == 3:
                def resid3(lm):
                    m = 10**lm * EV / C**2; mc2 = m * C**2; Cp = cp[3] * (HBAR * C)**3 / mc2**2
                    return math.log(s_eff(lambda v: AP[3] * (Cp / (m * v**2 / 4))**(2 / 3) / m, SREF) / sref)
                row["mchi_needed_lambda1_eV"] = 10**brentq(resid3, -40, 60)
        g3 = any(abs(r["log10"]) <= math.log10(2) for r in menu)
        row.update(menu=menu, G2="solvable with one free scale", G3=g3,
                   G6=True, G6_note="needs m_chi above G6_mchi_min; de Broglie and Hubble range satisfied")
        best = min(menu, key=lambda r: abs(r["log10"])) if menu else None
        extra = (f"; G6 m_chi >= {row['G6_mchi_min_GeV']:.3g} GeV" +
                 (f"; menu closest {best['M']}/{best['m']}: 10^{best['log10']:+.1f} of target -> G3 {'PASS' if g3 else 'FAIL'}" if best else "") +
                 (f"; m_chi needed if M = E_Lambda: {row['mchi_needed_if_M_ELambda_eV']/1e9:.3g} GeV" if 'mchi_needed_if_M_ELambda_eV' in row else "") +
                 (f"; m_chi needed at lambda = 1: {row['mchi_needed_lambda1_eV']/1e9:.3g} GeV" if 'mchi_needed_lambda1_eV' in row else ""))
        P("      " + extra.lstrip("; "))
        c2[p] = row
    R["cand"]["C2"] = c2
    sel = [p for p in (3, 5, 7) if c2[p]["G1"]]
    R["C2_selected_p"] = sel
    # integer windows (reported only)
    R["integer_p_window"] = [p for p in range(1, 60) if abs(4 / p - n) <= DN]
    P(f"  C2 menu powers passing G1: {sel}; all integer p with |4/p - n| <= {DN}: {R['integer_p_window']}")

    # C3 condensate
    R["cand"]["C3"] = dict(G1=False, G4=min(knt.values()) < 1, Kn_target_min=min(knt.values()),
                           note="phonon/contact scattering n = 0; hydrodynamic core needs Kn < 1 and Gamma t >> 1, target has Gamma t = 1 (LN2) and Kn >> 1")
    P(f"  C3 condensate: target Kn min {min(knt.values()):.0f} >> 1 and Gamma t = 1 (LN2 gamma_t_one) -> no hydrodynamic core: G4 FAIL; "
      f"contact/phonon scattering n = 0 -> G1 FAIL; CFG723 degenerate needs m <= 143 eV vs C2's classical bound")

    # class
    passing = []
    for cid in ("C0", "C1b"):
        if R["cand"][cid].get("G1"): passing.append(cid)
    for p in sel: passing.append(f"C2 p={p}")
    shape_ok = [c for c in passing if (c.startswith("C2") and c2[int(c[-1])]["G4"] and c2[int(c[-1])]["G5"]) or c == "C1b"]
    full = [c for c in shape_ok if c.startswith("C2") and c2[int(c[-1])]["G3"]]
    cls = ("CA1 NONE" if not passing else "CA1 CANDIDATE" if full else "CA1 SHAPE ONLY")
    R.update(G1_passing=passing, shape_ok=shape_ok, full=full, cls=cls)
    P(f"  [{f}] candidates passing G1: {passing}; G1+G4+G5+G6: {shape_ok}; also G3: {full} -> {cls}")
    RES["footings"][f] = R

sc, sa = RES["footings"]["canonical"], RES["footings"]["alt"]
split = set(sc["G1_passing"]) != set(sa["G1_passing"])
verdict = sc["cls"] if sc["cls"] == sa["cls"] else "UNDECIDED (" + sc["cls"] + " / " + sa["cls"] + ")"
if split: verdict += " + CA1 FOOTINGS SPLIT"
RES["verdict"] = verdict
P(f"\nLANE CLASS: {verdict}")
P(f"  canonical G1: {sc['G1_passing']}; alt G1: {sa['G1_passing']}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024**3 if sys.platform == "darwin" else 1024**2)
RES["checks"]["K4"] = rss < 1.0
P(f"K4 peak RSS {rss:.2f} GB, one thread -> {'PASS' if RES['checks']['K4'] else 'FAIL'}")
ok = all(RES["checks"].values())
exit_code = 0 if ok else 1
if MUTATE:
    import json as _j
    base = _j.load(open(os.path.join(HERE, "ca1_self_coupling_results.json")))
    bites = all(set(base["footings"][f]["C2_selected_p"]) != set(RES["footings"][f]["C2_selected_p"]) for f in A0)
    RES["mutate_bites"] = bites
    P(f"MUTATE: C2 selection normal {[base['footings'][f]['C2_selected_p'] for f in A0]} -> mutate "
      f"{[RES['footings'][f]['C2_selected_p'] for f in A0]}: {'BITES' if bites else 'DOES NOT BITE'}")
    exit_code = 1 if bites else 0
json.dump(RES, open(os.path.join(HERE, f"ca1_self_coupling_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"ca1_self_coupling{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(exit_code)
