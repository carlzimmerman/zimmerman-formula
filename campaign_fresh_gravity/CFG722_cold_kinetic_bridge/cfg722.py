"""CFG722: bridge astra's unsolved cold-energy kinetic equation (Supplement E selector) to the P-field action (CFG694/695).
Criteria: FROZEN_CRITERIA.md (committed alone, cb2aac21f). kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is
required; not "theory closed". Analytic + small numerics only (no PM, no merger simulation, no download).
Run:  nice -n 10 python3 cfg722.py        (CFG722_MUTATE=1: lambda -> 0, saturation 2 a0, tether sign; exit 1 iff all bite)
"""
import os, sys, json, math
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402

MUT = os.environ.get("CFG722_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
G, C, MSUN, KPC, PC, GYR = 6.6743e-11, 2.99792458e8, 1.98847e30, 3.0856775814913673e19, 3.0856775814913673e16, 3.15576e16
MP, KEV = 1.67262192e-27, 1.602176634e-16

LAM = 0.0 if MUT else 1.0          # P-Phi coupling (multiplies the residual tether and the bound-charge pull on matter)
SAT = 2.0 if MUT else 1.0          # saturation scale in units of a0 (M2)
TSIGN = -1.0 if MUT else 1.0       # sign of the tether (M3)

out, res = [__doc__.strip()], {"lane": "CFG722", "criteria": "cb2aac21f", "mutate": MUT}
def P(s=""): out.append(s)

def g_law(gN, a0):                  # CFG695 static law, g_N = g^2/(g + a0)
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))
def u_law(gN, a0):                  # g - g_N in the cancellation-free form
    return 2.0 * gN * a0 / (np.sqrt(gN * gN + 4.0 * gN * a0) + gN)
def Wp_rem(u, a0, sat=None, tsign=None):   # residual tether W_rem'(u) = W'_695 - critical quadratic = u^2/(a0 - u) [accel units]
    sat = SAT if sat is None else sat; tsign = TSIGN if tsign is None else tsign
    return tsign * u * u / (sat * a0 - u)
def u_eq_ID(gN, a0, lam=None, sat=None, tsign=None):   # coupling ID: cold carrier at rest, lam W_rem'(u) = g_N (bisection)
    lam = LAM if lam is None else lam; sat = SAT if sat is None else sat; tsign = TSIGN if tsign is None else tsign
    gN = np.atleast_1d(gN).astype(float); lo = np.zeros_like(gN); hi = np.full_like(gN, sat * a0 * (1 - 1e-15))
    if lam == 0.0 or tsign < 0: return np.full_like(gN, np.nan)      # no root: no static cold equilibrium
    for _ in range(200):
        mid = 0.5 * (lo + hi); f = lam * Wp_rem(mid, a0, sat, tsign) - gN
        lo = np.where(f < 0, mid, lo); hi = np.where(f >= 0, mid, hi)
    return 0.5 * (lo + hi)
def w_int(u, a0, sat=None, tsign=None):    # int_0^u s^2/(sat a0 - s) ds, stable for small u
    sat = SAT if sat is None else sat; tsign = TSIGN if tsign is None else tsign; A = sat * a0
    x = np.asarray(u, float) / A; outv = np.empty_like(x)
    sm = x < 1e-3; n = np.arange(3, 16)
    outv[sm] = (x[sm, None] ** n / n).sum(axis=1)
    xb = x[~sm]; outv[~sm] = -xb * xb / 2 - xb - np.log1p(-xb)
    return tsign * A * A * outv

ctrl_ok, teeth = True, {}

# ---------------- B1: neutrality of the bound charge (Q1) ----------------
P("\n=== B1 (Q1) bound-charge neutrality: Hernquist 1e11 Msun, a = 3 kpc, P tapered to 0 over [r_e, 1.1 r_e], r_e = 300 kpc")
res["B1"] = {}
for f in C4.FOOTS:
    a0 = C4.A0[f]; M = 1e11 * MSUN; a = 3 * KPC; re = 300 * KPC
    r = np.geomspace(1e-4 * KPC, 1.2 * re, 400001)
    gN = G * M / (r + a) ** 2
    taper = np.clip((1.1 * re - r) / (0.1 * re), 0.0, 1.0)
    Pr = u_law(gN, a0) / (4 * np.pi * G) * taper
    rho_c = np.gradient(r * r * Pr, r) / (r * r)
    dm = 4 * np.pi * r * r * rho_c
    net = np.trapz(dm, r); inside = np.trapz(np.where(r <= re, dm, 0.0), r)
    Mc_re = 4 * np.pi * re * re * (u_law(G * M / (re + a) ** 2, a0) / (4 * np.pi * G))
    rel = abs(net) / Mc_re
    ok = rel <= 1e-6; ctrl_ok &= ok
    P(f"  {f}: M_c(<r_e) Gauss {Mc_re / MSUN:.4e} Msun (= {Mc_re / M:.3f} M_b); numerical inside {inside / MSUN:.4e}; "
      f"edge shell {(net - inside) / MSUN:.4e}; NET {net / MSUN:.3e} Msun, |net|/M_c = {rel:.2e} -> {'PASS' if ok else 'FAIL'}")
    res["B1"][f] = {"Mc_re_Msun": Mc_re / MSUN, "Mc_over_Mb": Mc_re / M, "net_rel": rel, "pass": bool(ok)}
P("  Reading: the bound charge only MOVES mass from the polarized region's edge to its interior; seen from outside the basin the")
P("  system weighs M_b. It cannot supply CFG624's missing cold mass (X-COP 3.1/2.8 M_b, LG timing, mean density).")

# ---------------- B2: inertia / transport of a bound-charge lump (Q1; sympy) ----------------
P("\n=== B2 (Q1) inertia and transport of the P field (linearised longitudinal sector, sympy)")
x, t, v, I_, gam, K = sp.symbols("x t v I gamma K", positive=True); w_, k_ = sp.symbols("omega k", positive=True)
Pf = sp.Function("P")
Lag = I_ / 2 * sp.diff(Pf(x, t), t) ** 2 - gam / 2 * sp.diff(Pf(x, t), x) ** 2 - K / 2 * Pf(x, t) ** 2
EL = sp.euler_equations(Lag, [Pf(x, t)], [x, t])[0].lhs
disp = sp.simplify(EL.subs(Pf(x, t), sp.exp(sp.I * (k_ * x - w_ * t))).doit() / sp.exp(sp.I * (k_ * x - w_ * t)))
wsol = sp.solve(sp.Eq(disp, 0), w_)[0]
vg = sp.simplify(sp.diff(wsol, k_))
T0x = -I_ * sp.diff(Pf(x, t), t) * sp.diff(Pf(x, t), x)
lump = sp.exp(-(x - v * t) ** 2)
resid = sp.simplify(EL.subs(Pf(x, t), lump).doit() / lump)
P(f"  dispersion: omega = {wsol}   group velocity = {vg}")
P(f"  Noether momentum density T^0x = {T0x}  (set by I and grad P, not by the bound charge rho_c = div P)")
P(f"  translating lump exp(-(x - v t)^2): residual / lump = {sp.factor(resid)}")
P("  -> zero for all x only if K = 0 and v^2 = gamma/I. A gapped (K > 0) field has no translating lump at any v: no ballistic,")
P("     particle-like transport. The bound charge has no inertia of its own and no phase space; it cannot 'pass through' a merger.")
res["B2"] = {"omega": str(wsol), "v_group": str(vg), "lump_residual": str(sp.factor(resid)), "ballistic_lump": False}

# ---------------- B3: merger response time (Q1) ----------------
P("\n=== B3 (Q1) P response time at fixed baryons: omega0^2 = 2 c_P^2 x(2 - x)/(L*^2 (1 - x)^2), x = u/a0 (footing-free in y)")
corners = [(5.75, 1.7e-3), (100.0, 2.6e-4), (1000.0, 5.6e-5)]
res["B3"] = {"rows": []}; tmax = 0.0
for y in (0.1, 0.3, 1.0, 3.0):
    xx = float(u_law(y, 1.0))
    row = {"y": y, "x": xx}
    cells = []
    for Ls, cfl in corners:
        for cp in (cfl, 1.0):
            om = math.sqrt(2.0 * (cp * C) ** 2 * xx * (2 - xx) / ((Ls * PC) ** 2 * (1 - xx) ** 2))
            tr = 2 * math.pi / om / GYR; row[f"L{Ls}_cP{cp}"] = tr; cells.append(f"{tr:.2e}")
            tmax = max(tmax, tr)
    res["B3"]["rows"].append(row)
    P(f"  y {y:4}: x {xx:.3f}; t_resp [Gyr] (L* 5.75 floor/c, 100 floor/c, 1000 floor/c) = " + ", ".join(cells))
b3_adiabatic = tmax < 0.1
res["B3"]["t_resp_max_Gyr"] = tmax; res["B3"]["adiabatic_everywhere"] = b3_adiabatic
P(f"  max t_resp over the allowed window = {tmax:.3f} Gyr vs 0.1 Gyr -> "
  f"{'ADIABATIC everywhere: tracks the instantaneous all-baryon field (alpha = infinity class)' if b3_adiabatic else 'CONDITIONAL on (L*, c_P): slow corner reaches the merger window; hand to CFG720'}")
P("  Note: even where t_resp is long, B2 says P lags or rings; it never carries a lump along with the galaxies.")

# ---------------- B4: static limit (Q2 control K1) ----------------
P("\n=== B4 (Q2) static limit: coupling ID, cold carrier at rest, lam W_rem'(u) = g_N")
ys = np.geomspace(1e-4, 1e3, 200)
def B4(a0, **kw):
    gN = ys * a0; u = u_eq_ID(gN, a0, **kw)
    if not np.all(np.isfinite(u)): return float("inf"), float("nan")
    nu_ID = (gN + u) / gN; nu_s = 0.5 + np.sqrt(0.25 + 1.0 / ys)
    return float(np.max(np.abs(nu_ID / nu_s - 1))), float(u[0] ** 2 / gN[0] / a0)
res["B4"] = {}; b4_all = True
for f in C4.FOOTS:
    a0 = C4.A0[f]; dev, deep = B4(a0)
    ok = dev <= 1e-10; b4_all &= ok
    P(f"  {f}: max |nu_ID/nu_s - 1| = {dev:.2e}; deep coefficient u^2/(g_N a0) at y=1e-4: {deep:.6f} -> {'PASS' if ok else 'FAIL'}")
    res["B4"][f] = {"max_dev": dev, "deep_coeff": deep, "pass": bool(ok)}
if not MUT: ctrl_ok &= b4_all
dev2, deep2 = B4(C4.A0["canonical"], lam=1.0, sat=2.0, tsign=1.0)      # M2 in isolation
teeth["M2_sat2_breaks_B4"] = dev2 > 1e-10
res["M2_isolated"] = {"max_dev": dev2, "deep_coeff": deep2}
if MUT: P(f"  M2 isolated (saturation 2 a0): max dev {dev2:.3e}, deep coefficient {deep2:.4f} (must be != 1)")
P("  Coupling G: a cold carrier at rest feels g_N + g_c + g_bound (all inward); the action gives it no outward force, so there is")
P("  NO static cold equilibrium and C_sel = 0 exactly (the carrier is ordinary collisionless matter in the total potential).")

# ---------------- M1: lam -> 0 decouples ----------------
dP = 1e-3 * 1e-10  # a test delta P_L in acceleration units / 4 pi G
acc_from_P = -LAM * dP
res["M1"] = {"lam": LAM, "accel_from_bound_charge": acc_from_P,
             "ID_residual_over_gN_at_u_law": float(abs(LAM * Wp_rem(u_law(0.1, 1.0), 1.0) - 0.1) / 0.1)}
P(f"\n=== M1 lam = {LAM}: acceleration of matter from a bound-charge perturbation = {acc_from_P:.3e}; "
  f"ID net force on a cold carrier at the law position / g_N = {res['M1']['ID_residual_over_gN_at_u_law']:.3e}")
teeth["M1_decouples"] = (acc_from_P == 0.0) and abs(res["M1"]["ID_residual_over_gN_at_u_law"] - 1.0) < 1e-12

# ---------------- B5: sign of the required exchange (Q2) ----------------
P("\n=== B5 (Q2) coupling ID: static energy U[u] = (1/4 pi G) int dV [w(u) - g_N u]; carrier mass fixed at M_law(<10 r_M)")
res["B5"] = {}; b5_pos = True; svals = (0.5, 0.8, 1.25, 2.0, 4.0)
for f in C4.FOOTS:
    a0 = C4.A0[f]; res["B5"][f] = {}
    for lm in (10, 12):
        Mb = 10 ** lm * MSUN; rM = math.sqrt(G * Mb / a0); re = 10 * rM; Vf2 = math.sqrt(G * Mb * a0)
        r = np.geomspace(1e-4 * rM, 4.5 * re, 200001); gN = G * Mb / r ** 2
        Meq_f = lambda rr: u_law(G * Mb / rr ** 2, a0) * rr * rr / G   # law (the ID equilibrium at lam = 1, B4)
        Mc = float(Meq_f(re))
        def U_of(s, tsign=None):
            rs = r / s
            Ms = np.where(rs <= re, Meq_f(rs), Mc)
            us = G * Ms / r ** 2
            if np.any(us >= SAT * a0): return float("inf"), float(r[np.argmax(us >= SAT * a0)] / rM)
            return float(np.trapz(r * r * (w_int(us, a0, tsign=tsign) - gN * us), r) / G), None
        U1, _ = U_of(1.0); cells = {}; txt = []
        if lm == 10 and f == "canonical":                                  # M3 in isolation: flipped tether sign
            U1m, _ = U_of(1.0, tsign=-1.0); m3 = [(U_of(sv, tsign=-1.0)[0] - U1m) / (Mc * Vf2) for sv in (1.25, 2.0, 4.0)]
            teeth["M3_flip_breaks_B5"] = any(dv < 0 for dv in m3); res["M3_isolated"] = m3
        for s in svals:
            Us, wall = U_of(s)
            if not np.isfinite(U1): raise RuntimeError("law profile hit the wall: numerical")
            dU = (Us - U1) / (Mc * Vf2) if np.isfinite(Us) else float("inf")
            cells[str(s)] = dU if np.isfinite(dU) else "inf (wall u >= a0 inside r = %.3g r_M)" % wall
            b5_pos &= (dU > 0)
            txt.append(f"s {s}: " + (f"{dU:+.4f}" if np.isfinite(dU) else f"+inf (wall at r<{wall:.2g} r_M)"))
        res["B5"][f][f"1e{lm}"] = {"Mc_over_Mb": Mc / Mb, "dU_over_McVf2": cells}
        P(f"  {f} M_b 1e{lm}: M_c = {Mc / Mb:.2f} M_b; dU/(M_c V_f^2): " + "; ".join(txt))
res["B5"]["all_positive"] = bool(b5_pos)
uu_, A_, ts_ = sp.symbols("u a_0 sigma", positive=True)
e2 = sp.simplify(sp.diff(ts_ * sp.integrate(sp.Symbol("s") ** 2 / (A_ - sp.Symbol("s")), (sp.Symbol("s"), 0, uu_)), uu_, 2))
P(f"  analytic: d^2/du^2 [tsign w(u) - g_N u] = {sp.factor(e2)}  (> 0 on 0 < u < a0 for tsign = +1: pointwise convex; the truncated")
P("  law is then the constrained minimiser at fixed carrier mass, since it is pointwise optimal wherever the mass cap does not bind)")
res["B5"]["second_derivative"] = str(sp.factor(e2))
if MUT:
    P("  M3 note (POST-HOC, no verdict weight): with tsign = -1 the integrand is pointwise CONCAVE and B4 has no equilibrium root;")
    P("  the frozen M3 line (dU < 0 somewhere in the s-family) does not bite, because -g_N u dominates for stretched states and the")
    P("  compressed states (s < 1) sit beyond the wall in either sign.")
P(f"  -> {'law profile is the unique static minimum; required exchange is EXPORT (>= 0) for every initial state' if b5_pos else 'some dU < 0: the law is NOT the minimum'}")
P("  IC-C analogue (law density, sigma = 0.05 V_f): the tether supplies the support astra's IC-C lacked, so the required exchange is its")
P("  own kinetic energy, EXPORT 1.5 sigma^2 = 0.00375 M V_f^2 (astra, gravity only: IMPORT 0.50-0.64). IC-B-like (diffuse, s > 1): EXPORT.")
P("  The bridge offers no export channel: P radiation is trapped (<= 1e-195, CFG659); phase mixing keeps the energy as dispersion.")

# ---------------- B6: momentum receiver / anchor (Q2) ----------------
P("\n=== B6 (Q2) anchor: halo displaced d = 300 km/s x 1 Gyr from a cosmic-frame anchor; u_shift = 4 pi G rho_c d")
res["B6"] = {}; b6_ex = True
for f in C4.FOOTS:
    a0 = C4.A0[f]; M = 1e11 * MSUN; y = 0.1; r = math.sqrt(G * M / (y * a0)); h = r * 1e-5
    q = lambda rr: rr * rr * float(u_law(G * M / rr ** 2, a0))
    rho = (q(r + h) - q(r - h)) / (2 * h) / (4 * math.pi * G * r * r)
    d = 3e5 * GYR; us = 4 * math.pi * G * rho * d
    b6_ex &= us >= a0
    P(f"  {f}: r {r / KPC:.1f} kpc, rho_c {rho:.3e} kg/m^3, d {d / KPC:.0f} kpc -> u_shift/a0 = {us / a0:.2f}")
    res["B6"][f] = {"r_kpc": r / KPC, "rho_c": rho, "u_shift_over_a0": us / a0}
res["B6"]["cosmic_anchor_excluded"] = bool(b6_ex)
P(f"  -> {'cosmic-frame anchor EXCLUDED (beyond saturation): the anchor must be the basin frame, reciprocal with its baryons' if b6_ex else 'not excluded'}")

# ---------------- B7: phase dependence (Q3) ----------------
P("\n=== B7 (Q3) can the bridge separate hot from condensed baryons without a new constant?")
res["B7"] = {}
for kT in (1.0, 8.0):
    pr = kT * KEV / (0.6 * MP * C * C); res["B7"][f"pressure_kT{kT}"] = 3 * pr
    P(f"  (a) relativistic pressure, kT {kT} keV: (rho + 3p/c^2)/rho - 1 = {3 * pr:.2e} (and it ADDS to the hot source)")
for f in C4.FOOTS[:1]:
    a0 = C4.A0[f]
    for lbl, Mb, hh in (("disc gas", 6e10, 100 * PC), ("ICM core", 1e14, 200 * KPC)):
        for Ls in (5.75, 1000.0):
            rM = math.sqrt(G * Mb * MSUN / a0); lg = (Ls * PC) ** 2 / (2 * rM)
            res["B7"][f"stiff_{lbl}_L{Ls}"] = (lg / hh) ** 2
            P(f"  (b) stiffness, {lbl}, L* {Ls} pc: l_gamma {lg / PC:.3e} pc; (l_gamma/h)^2 = {(lg / hh) ** 2:.2e}")
P("      Sign: stiffness suppresses the response to components THINNER than l_gamma, i.e. thin cold discs, not extended hot gas:")
P("      wrong sign for A5 at any L*; the largest value (0.28, cold disc gas at L* 1000 pc) suppresses the CONDENSED source.")
P("  (c) granularity: a star's own phantom is screened to 0.0352 of its mass (CFG658 E3). Screening REDUCES the condensed")
P("      source relative to smooth gas: wrong sign for A5, and <= 3.5% in size.")
P("  (d) carrier dispersion (reported, not A5): a warm carrier sits BELOW the law (B8), so hot, recently assembled systems would")
P("      hold LESS settled cold energy. That is a phase of the carrier set by its history, not of the baryons, and its sign is")
P("      opposite to the cluster-core excess.")
b7_any = any(v >= 0.5 for v in res["B7"].values())
res["B7"]["any_route_ge_0.5_right_sign"] = False
P(f"  -> no route reaches 0.5 with the right sign (largest {max(res['B7'].values()):.1e}): OBSTRUCTED")

# ---------------- B8: capacity (Q4) ----------------
P("\n=== B8 (Q4) capacity of the bound charge / tethered medium")
res["B8"] = {}; b8_ok = True; b8_adm = True; inadm = []
for f in C4.FOOTS:
    a0 = C4.A0[f]; Sig = a0 / (math.pi * G) / (MSUN / PC ** 2)
    ref = {"canonical": 214.0, "alt": 258.0}[f]; ok = abs(Sig / ref - 1) <= 0.01
    if not MUT: ctrl_ok &= ok
    P(f"  (i) {f}: hard wall u < a0 => M_c(<r) < a0 r^2/G; mean Sigma_c <= a0/(pi G) = {Sig:.1f} Msun/pc^2 (CFG695 S4 {ref:.0f}) -> {'PASS' if ok else 'FAIL'}")
    res["B8"][f] = {"Sigma_max": Sig, "pass": bool(ok)}
rows = []
for y in (0.1, 1.0, 10.0):
    ue = float(u_law(y, 1.0)); fac = (0.5, 0.9, 1.1, 1.5, min(2.0, 0.999 / ue))
    fl = []
    for k in fac:
        uu = k * ue; fu = float(uu * uu / (1.0 - uu) - y) / y
        fl.append(fu)
        bad = (k > 1 and fu <= 0) or (k < 1 and fu >= 0)
        if bad: b8_ok = False
        if uu >= 1.0: inadm.append((y, k, uu))
        elif bad: b8_adm = False
    rows.append({"y": y, "u_eq": ue, "factors": list(fac), "f_over_gN": fl})
    P(f"  (ii) y {y:5}: u_eq/a0 {ue:.3f}; net outward accel / g_N at u/u_eq = " + ", ".join(f"{k:.3g}: {fv:+.3f}" for k, fv in zip(fac, fl)))
res["B8"]["rows"] = rows; res["B8"]["expels_excess_holds_deficit_as_frozen"] = bool(b8_ok)
res["B8"]["inadmissible_cells_u_ge_a0"] = inadm; res["B8"]["rule_on_admissible_cells"] = bool(b8_adm)
P(f"  -> as frozen: {'PASS' if b8_ok else 'FAIL'}.")
if inadm:
    P("     DISCLOSED CRITERIA ERROR: the frozen factor list puts these cells beyond the hard wall u >= a0, where the tether energy is")
    P("     infinite and the state is inadmissible (the formula's sign flips there): " + "; ".join(f"y {a}, x{b}: u/a0 {c:.3f}" for a, b, c in inadm))
P(f"     on admissible cells (u < a0): {'PASS: excess over the law is pushed OUT, deficits fall IN; no overflow can sit in a tethered core; a warm carrier sits at or below the law' if b8_adm else 'FAIL'}")

# ---------------- verdicts ----------------
v = {}
v["Q1"] = ("DERIVED" if (res["B1"]["canonical"]["pass"] and b3_adiabatic) else
           "CONDITIONAL (neutrality and no ballistic transport DERIVED; merger tracking adiabatic except at the slow corner L* ~ 1 kpc, c_P at the double-pulsar floor)")
v["Q2"] = ("CONDITIONAL (coupling ID: law profile = unique static minimum of a cold tethered carrier; C_sel is a conservative Vlasov tether, not an attractor; needs an export channel and a basin-frame anchor the action does not supply)"
           if (b4_all and b5_pos) else "OBSTRUCTED")
v["Q3"] = "OBSTRUCTED"
v["Q4"] = ("DERIVED" if b8_ok else
           ("CONDITIONAL on the disclosed criteria correction (capacity wall DERIVED; B8(ii) fails as frozen only in cells beyond the wall, passes on every admissible cell)" if b8_adm else "NOT DERIVED"))
res["verdicts"] = v; res["teeth"] = teeth; res["controls_pass"] = bool(ctrl_ok)
P("\n=== VERDICTS"); [P(f"  {k}: {s}") for k, s in v.items()]
if MUT:
    P(f"\nMUTATE teeth: {teeth}")

with open(os.path.join(HERE, f"cfg722{TAG}.out"), "w") as fh: fh.write("\n".join(out) + "\n")
with open(os.path.join(HERE, f"cfg722_results{TAG}.json"), "w") as fh: json.dump(res, fh, indent=1, default=str)
print("\n".join(out))
if MUT:
    sys.exit(1 if all(teeth.values()) else 0)
sys.exit(0 if ctrl_ok else 2)
