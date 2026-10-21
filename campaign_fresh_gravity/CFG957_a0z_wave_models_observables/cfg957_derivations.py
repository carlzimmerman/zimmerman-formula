"""CFG957 derivations (sympy): can anything in the framework make rho_DE (hence a0) oscillate?

The owner's idea (2026-10-21): a0(z) oscillates like a wave as the universe expands; the wave is larger early and shrinks over
time, and today a0 is on the way down from a recent peak.  This file holds the symbolic checks D1-D10 of
FROZEN_CRITERIA.md (8e884c9a2b) and one added, report-only item D11 (dated 2026-10-21, after the criteria: the effective w of
CFG689's own best-fit node curve).  kappa = 1/2 is FITTED; the two footings (9.3603e-11, 1.1312e-10 m s^-2) are never pooled.
Not a closed theory.

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg957_derivations.py      (seconds; writes cfg957_derivations.out / .json)
"""
import glob
import json
import math
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
OUT, CHECKS, RES = [], [], {}


def P(s=""):
    print(s)
    OUT.append(s)


def check(name, ok, info=""):
    CHECKS.append((name, bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}  {info}")


t, H, m, Hl = sp.symbols("t H m H_Lambda", positive=True)
lam = sp.symbols("lambda")

P("CFG957 derivations (criteria 8e884c9a2b). The owner's idea (2026-10-21): an oscillating a0(z).")
P("kappa = 1/2 FITTED; footings never pooled; not theory closed.")
P("")

# ------------------------------------------------------------------ D1 de Sitter roots
P("D1  de Sitter (H const): phi'' + 3 H phi' + m^2 phi = 0")
roots = sp.solve(sp.Eq(lam**2 + 3 * H * lam + m**2, 0), lam)
P(f"    roots: {roots}")
disc = sp.simplify((3 * H) ** 2 - 4 * m**2)
exp1 = [-sp.Rational(3, 2) * H + sg * sp.sqrt(sp.Rational(9, 4) * H**2 - m**2) for sg in (1, -1)]
check("D1 roots = -3H/2 +- sqrt(9H^2/4 - m^2)",
      len(roots) == 2 and all(any(sp.simplify(r - e) == 0 for e in exp1) for r in roots), "")
check("D1 underdamped (complex roots) iff m > 3H/2", sp.solve(sp.Eq(disc, 0), m) == [sp.Rational(3, 2) * H], f"disc = {disc}")
P("    In a universe with Lambda, H(t) -> H_Lambda from above, so the field is asymptotically underdamped iff m > (3/2) H_Lambda.")

# record rates (CFG689 primary best fit background; cfg689.json is read only)
d689 = glob.glob(os.path.join(CFG, "CFG689_*"))[0]
J = json.load(open(os.path.join(d689, "cfg689.json")))
pb = J["BAO+SN"]["P2"]["pbest"]
om = pb[7] + pb[8]
OMR = 2.4728e-5 * (1 + 0.2271 * 3.044)
wk = pb[6]
W0 = pb[0]
h2 = om + OMR + wk + W0
h = math.sqrt(h2)
OL = W0 / h2
H0s = h * 100 * 1e3 / 3.0856775814913673e22    # s^-1
c = 2.99792458e8
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
rates = {"H_Lambda": math.sqrt(OL)}
for f, a0 in A0.items():
    rates[f"a0/c ({f})"] = a0 / c / H0s
    rates[f"sqrt(G rho) ({f})"] = 2 * a0 / c / H0s          # a0 = (1/2) c sqrt(G rho)  =>  sqrt(G rho) = 2 a0 / c
thr = 1.5 * math.sqrt(OL)
P(f"    background: h = {h:.5f}, Omega_Lambda = W0/h^2 = {OL:.5f}; threshold (3/2) H_Lambda = {thr:.4f} H0")
for k, v in rates.items():
    P(f"    record rate {k:22s} = {v:.4f} H0  -> {'UNDERDAMPED' if v > thr else 'overdamped (asymptotically)'}")
check("D1 every record rate lies below (3/2) H_Lambda", all(v < thr for v in rates.values()),
      f"max {max(rates.values()):.4f} < {thr:.4f}")
RES["D1"] = dict(h=h, Omega_Lambda=OL, threshold_over_H0=thr, record_rates_over_H0=rates)
P("")

# ------------------------------------------------------------------ D2 EdS and the u-equation
P("D2  matter era (EdS, H = 2/(3t)): phi'' + (2/t) phi' + m^2 phi = 0")
j0 = sp.sin(m * t) / (m * t)
res = sp.simplify(sp.diff(j0, t, 2) + 2 / t * sp.diff(j0, t) + m**2 * j0)
check("D2 sin(mt)/(mt) solves the EdS equation (zeros at m t = k pi)", res == 0, f"residual {res}")
Hf = sp.Function("Hf")(t)
a = sp.exp(sp.Integral(Hf, t))
u = sp.Function("u")(t)
phi = u * a ** sp.Rational(-3, 2)
kg = sp.diff(phi, t, 2) + 3 * Hf * sp.diff(phi, t) + m**2 * phi
ueq = sp.simplify(sp.expand(kg * a ** sp.Rational(3, 2)))
target = sp.diff(u, t, 2) + (m**2 - sp.Rational(9, 4) * Hf**2 - sp.Rational(3, 2) * sp.diff(Hf, t)) * u
check("D2 u = a^(3/2) phi obeys u'' + (m^2 - 9H^2/4 - 3H'/2) u = 0", sp.simplify(ueq - target) == 0, "")
eds = sp.simplify((m**2 - sp.Rational(9, 4) * Hf**2 - sp.Rational(3, 2) * sp.diff(Hf, t)).subs(Hf, 2 / (3 * t)).doit())
check("D2 in EdS the effective frequency^2 is exactly m^2 (oscillation for any m once m t > pi)", sp.simplify(eds - m**2) == 0, f"{eds}")
P("    So in the matter era the field turns over once m t ~ pi; in the Lambda era the frequency^2 m^2 - 9H_L^2/4 < 0 for m < 1.5 H_L.")
P("")

# ------------------------------------------------------------------ D3 WKB damping
P("D3  WKB (two timescales): phi = A(t) cos(mt) + B(t) sin(mt), A, B slow")
A_, B_ = sp.Function("A")(t), sp.Function("B")(t)
ph = A_ * sp.cos(m * t) + B_ * sp.sin(m * t)
kg = sp.expand(sp.diff(ph, t, 2) + 3 * H * sp.diff(ph, t) + m**2 * ph)
ccos = sp.simplify(kg.coeff(sp.cos(m * t)))
csin = sp.simplify(kg.coeff(sp.sin(m * t)))
# keep terms first order in d/dt and H (drop A'', B'', H A', H B')
eps = sp.symbols("epsilon")
lead_cos = sp.expand(ccos).subs({sp.diff(A_, t, 2): 0, sp.diff(B_, t, 2): 0})
lead_sin = sp.expand(csin).subs({sp.diff(A_, t, 2): 0, sp.diff(B_, t, 2): 0})
lead_cos = lead_cos - (3 * H * sp.diff(A_, t))
lead_sin = lead_sin - (3 * H * sp.diff(B_, t))
sol = sp.solve([sp.Eq(lead_cos, 0), sp.Eq(lead_sin, 0)], [sp.diff(A_, t), sp.diff(B_, t)], dict=True)[0]
okA = sp.simplify(sol[sp.diff(A_, t)] + sp.Rational(3, 2) * H * A_) == 0
okB = sp.simplify(sol[sp.diff(B_, t)] + sp.Rational(3, 2) * H * B_) == 0
check("D3 A' = -(3/2) H A and B' = -(3/2) H B  =>  amplitude ∝ a^(-3/2), rho_osc ∝ a^(-3)", okA and okB,
      f"A' = {sol[sp.diff(A_, t)]}, B' = {sol[sp.diff(B_, t)]}")
P("    In a0 (small r = rho_osc/V0): relative wave amplitude ∝ rho_osc ∝ (1+z)^3 in the -p and V readings: beta = 3.")
P("")

# ------------------------------------------------------------------ D4 readings
P("D4  readings for a real field phi = A cos(theta), theta' = m (WKB), V = V0 + m^2 phi^2 / 2")
Am, th, V0 = sp.symbols("A_m theta V_0", positive=True)
phid = -Am * m * sp.sin(th)
phiv = Am * sp.cos(th)
rho = sp.Rational(1, 2) * m**2 * Am**2
eps_ = V0 + sp.Rational(1, 2) * phid**2 + sp.Rational(1, 2) * m**2 * phiv**2
p_ = sp.Rational(1, 2) * phid**2 - V0 - sp.Rational(1, 2) * m**2 * phiv**2
Vr = (eps_ - p_) / 2
tr = (eps_ - 3 * p_) / 4
ac = -(eps_ + 3 * p_) / 2
check("D4 eps = V0 + rho_osc (no oscillation at WKB order)", sp.simplify(eps_ - (V0 + rho)) == 0, "")
check("D4 -p = V0 + rho_osc cos 2theta", sp.simplify(-p_ - (V0 + rho * sp.cos(2 * th))) == 0, "")
check("D4 V = V0 + rho_osc (1 + cos 2theta)/2", sp.simplify(Vr - (V0 + rho * (1 + sp.cos(2 * th)) / 2)) == 0, "")
check("D4 trace/4 = V0 + rho_osc (1 + 3 cos 2theta)/4", sp.simplify(tr - (V0 + rho * (1 + 3 * sp.cos(2 * th)) / 4)) == 0, "")
check("D4 active/2 = V0 - rho_osc (1 - 3 cos 2theta)/2", sp.simplify(ac - (V0 - rho * (1 - 3 * sp.cos(2 * th)) / 2)) == 0, "")
# complex field, circular orbit: Phi = (A/sqrt2) e^{i theta}; eps = |Phi'|^2 + m^2|Phi|^2, p = |Phi'|^2 - m^2|Phi|^2
Phid2 = (Am * m) ** 2 / 2
Phi2 = Am**2 / 2
check("D4 complex field on a circular orbit (CFG288 form): p_osc = |Phi'|^2 - m^2 |Phi|^2 = 0 exactly",
      sp.simplify(Phid2 - m**2 * Phi2) == 0, "no wave in any reading")
P("    So the frequency of the a0 wave in -p and V is 2m (period pi/m in cosmic time).")
P("")

# ------------------------------------------------------------------ D5 NEC / eps monotone
P("D5  canonical scalar: eps + p = phi'^2 >= 0 (NEC) and d eps/dt = -3 H phi'^2 <= 0")
pf = sp.Function("phi")(t)
Vf = sp.Function("V")
e5 = sp.Rational(1, 2) * sp.diff(pf, t) ** 2 + Vf(pf)
p5 = sp.Rational(1, 2) * sp.diff(pf, t) ** 2 - Vf(pf)
kgeq = sp.Eq(sp.diff(pf, t, 2), -3 * H * sp.diff(pf, t) - sp.diff(Vf(pf), pf))
de5 = sp.diff(e5, t).subs(sp.diff(pf, t, 2), kgeq.rhs)
check("D5 d eps/dt = -3H(eps + p) = -3H phi'^2", sp.simplify(de5 + 3 * H * sp.diff(pf, t) ** 2) == 0 and
      sp.simplify(e5 + p5 - sp.diff(pf, t) ** 2) == 0, "")
P("    THEOREM: in the eps reading a canonical dark-energy scalar can never give a0 a local peak in time (d eps/dt <= 0);")
P("    a peak needs eps + p < 0 (phantom) or an energy inflow from another sector.")
P("")

# ------------------------------------------------------------------ D6 eps ripple
P("D6  eps ripple: d eps/dt = -3H rho_osc (1 - cos 2 m t)  =>  delta eps = (3H/2m) rho_osc sin 2mt (first order in H/m)")
rho_s = sp.symbols("rho_osc", positive=True)
deps = -3 * H * rho_s * (1 - sp.cos(2 * m * t))
osc = sp.integrate(-3 * H * rho_s * (-sp.cos(2 * m * t)), t)
check("D6 oscillating part of eps = (3H/(2m)) rho_osc sin(2mt)", sp.simplify(osc - sp.Rational(3, 2) * H / m * rho_s * sp.sin(2 * m * t)) == 0,
      f"{osc}")
check("D6 the same from the WKB solution (phi'^2 average)", sp.simplify(sp.expand(phid**2 - rho * 2 * sp.sin(th) ** 2)) == 0, "")
P("    => eps-reading ripple in a0 = (3H/4m) r, against r/2 in -p: ratio (3H/2m).")
P("")

# ------------------------------------------------------------------ D7 partner no-turning lemma
P("D7  the record's partner: phi'' + 3H phi' + V'(phi) = Q/phi', Q >= 0 (CFG542/630)")
Q = sp.symbols("Q", positive=True)
s = sp.symbols("s")       # s = phi'
Vp = sp.symbols("Vp")     # V'(phi)
sdot = -3 * H * s - Vp + Q / s
udot = sp.simplify(s * sdot)  # u = s^2/2
check("D7 u = phi'^2/2 obeys du/dt = -6H u - V' phi' + Q", sp.simplify(udot - (-6 * H * s**2 / 2 - Vp * s + Q)) == 0, f"{sp.expand(udot)}")
check("D7 at u = 0: du/dt = Q > 0, so phi' cannot change sign (no turning point, no oscillation)", sp.limit(udot, s, 0) == Q, "")
P("    Energy: d(phi'^2/2 + V)/dt = -3H phi'^2 + Q.  The rise of eps is bounded by the integral of Q (CFG630: <= 3.8e-6 rho_DE).")
P(f"    => any a0 rise from the partner <= 0.5 * log10(1 + 3.8e-6) = {0.5 * math.log10(1 + 3.8e-6):.2e} dex")
RES["D7_ceiling_dex"] = 0.5 * math.log10(1 + 3.8e-6)
P("")

# ------------------------------------------------------------------ D8 exchange
P("D8  exchange between cold energy (dust) and a w = -1 vacuum")
P("    vacuum continuity: rho_L' + 3H(1+w) rho_L = -Q with w = -1  =>  rho_L' = -Q (no Hubble term)")
x, y, qc, qd, G_, R_ = sp.symbols("x y q_c q_d Gamma R")
M = sp.Matrix([[-qd, -qc], [qd, qc - 3 * H]])
tr8, det8 = sp.simplify(M.trace()), sp.simplify(M.det())
disc8 = sp.simplify(tr8**2 - 4 * det8)
check("D8 linear Q = q_c rho_c + q_d rho_L: det = 3 H q_d", sp.simplify(det8 - 3 * H * qd) == 0, f"trace {tr8}, det {det8}, disc {sp.expand(disc8)}")
det_rel = sp.simplify(det8.subs({qc: G_, qd: -G_ * R_}))
check("D8 relaxation Q = Gamma(rho_c - R rho_L): det = -3 H Gamma R < 0  => saddle, no oscillation",
      sp.simplify(det_rel + 3 * H * G_ * R_) == 0, f"det = {det_rel}")
Hs = sp.symbols("Hs", positive=True)
fp = sp.solve([sp.Eq(-(qc * y + qd * x), 0), sp.Eq(-3 * Hs * y + (qc * y + qd * x), 0)], [x, y], dict=True)
check("D8 the only fixed point (H const) has rho_c = 0 (any linear Q)", all(sp.simplify(f_[y]) == 0 for f_ in fp), f"{fp}")
P("    Complex eigenvalues (q_d > 0 and disc < 0) would make rho_c oscillate about 0, i.e. go negative: unphysical.")
P("    A wave in rho_L needs Q to change sign periodically; every record Q is one-signed (CFG630, CFG253, CFG360-DE C1, CFG131).")
P("")

# ------------------------------------------------------------------ D9 lever
P("D9  the record's footing lever for the shear engine")
lnr = math.log(1.1312e-10 / 9.3603e-11)
lev_nat = (-9.39 - (-10.08)) / lnr
lev_inh = (-7.18 - (-7.70)) / lnr
P(f"    ln(1.1312/0.93603) = {lnr:.5f};  native (NC2x - NC1x) {lev_nat:.3f}, inherited (T2x - T1x) {lev_inh:.3f} per unit ln a0")
check("D9 lever arithmetic", abs(lnr - 0.18935) < 1e-4, "")
RES["D9"] = dict(ln_ratio=lnr, lever_native=lev_nat, lever_inherited=lev_inh)
P("")

# ------------------------------------------------------------------ D10 -p positivity
P("D10 -p >= 0 for all theta  <=>  rho_osc <= V0 (real field)")
r = sp.symbols("r", positive=True)
check("D10 min over theta of (V0 + rho cos 2theta)/V0 = 1 - r  => need r <= 1", sp.simplify((1 + r * sp.cos(sp.pi)) - (1 - r)) == 0, "")
P("")

# ------------------------------------------------------------------ D11 (added 2026-10-21, report only)
P("D11 (ADDED after the criteria, dated 2026-10-21, report only): effective w of CFG689's own best-fit node curve")
nodes = J["cfg"]["nodes"]
wn = pb[:6]
mean, std = J["BAO+SN"]["posterior"]["node_mean"], J["BAO+SN"]["posterior"]["node_std"]
segs = []
for i in range(len(nodes) - 1):
    z1, z2 = nodes[i], nodes[i + 1]
    dlnrho = math.log(wn[i] / wn[i + 1])                    # from z2 (earlier) to z1 (later)
    dlna = math.log((1 + z2) / (1 + z1))
    weff = -1 - dlnrho / (3 * dlna)
    segs.append(dict(z=[z1, z2], w_eff=weff))
    P(f"    z {z2:4.2f} -> {z1:4.2f}: rho ratio {wn[i] / wn[i + 1]:.3f}, w_eff = {weff:+.3f}{'  (phantom: NEC violated)' if weff < -1 else ''}")
P(f"    a0 ratio at the z = 0.7 node: sqrt({wn[2]:.5f}/{wn[0]:.5f}) = {math.sqrt(wn[2] / wn[0]):.3f} (a 'recent peak' in the best-fit shape)")
P(f"    node posterior (marginal) w(0.7) {mean[2]:.3f} +- {std[2]:.3f}, w(1.0) {mean[3]:.3f} +- {std[3]:.3f}; constant rho_DE is not rejected (P2 1.97 sigma)")
P("    Under the eps reading this shape needs w_eff < -1 between z 1.0 and 0.7: impossible for any canonical scalar (D5).")
RES["D11"] = dict(segments=segs, a0_ratio_z07=math.sqrt(wn[2] / wn[0]), note="report only; CFG956 A1.3 grades the rising/falling significance")
P("")

npass = sum(ok for _, ok in CHECKS)
P(f"checks: {npass}/{len(CHECKS)} PASS")
P("kappa = 1/2 FITTED; footings never pooled; not theory closed; the owner's idea (2026-10-21).")
open(os.path.join(HERE, "cfg957_derivations.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(criteria="8e884c9a2b", checks=[dict(name=n, ok=o) for n, o in CHECKS], npass=npass, n=len(CHECKS), results=RES,
               note="the owner's idea (2026-10-21); kappa = 1/2 FITTED"),
          open(os.path.join(HERE, "cfg957_derivations.json"), "w"), indent=1)
raise SystemExit(0 if npass == len(CHECKS) else 1)
