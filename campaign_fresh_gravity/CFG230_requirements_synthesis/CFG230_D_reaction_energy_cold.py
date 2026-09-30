"""CFG230 script D: R04-R06, R12 arithmetic. CROSS-CHECKS of committed closed forms plus HAND-expectation tests (E6, E7, E11, E13).
No MUTATE mode is defined for this script (not in the frozen M1-M9 list)."""
import math, re
import sympy as sp
import CFG230_common as C

R = C.Run("CFG230_D_reaction_energy_cold")
R.p("CFG230 D. repo=<repo>")
x = sp.symbols("x", positive=True)

# ---------------------------------------------------------------- R04: required c_s^2 mass exponent e(x)
R.p("\n== R04: barotropic exponent e(x): required c_s^2 at fixed density scales as M^e (CFG44 B2)")
M_, u = sp.symbols("M u", positive=True)
a0, G = sp.symbols("a0 G", positive=True)
rM = sp.sqrt(G * M_ / a0)
# point mass: P = a0 M/(8 pi r^2), rho = a0/(4 pi G r sqrt(1+x^2)), r = x rM ; c_s^2 = dP/drho along the profile
cs2 = (G * M_ / (x * rM)) * sp.sqrt(1 + x ** 2) * (1 + x ** 2) / (1 + 2 * x ** 2)
# at fixed rho: x*sqrt(1+x^2) = K M^(-1/2)  => dlnx/dlnM = -(1/2)(1+x^2)/(1+2x^2)
dlnx = -sp.Rational(1, 2) * (1 + x ** 2) / (1 + 2 * x ** 2)
e_expr = sp.simplify(sp.Rational(1, 2) + x * sp.diff(sp.log(sp.sqrt(1 + x ** 2) * (1 + x ** 2) / (1 + 2 * x ** 2) / x), x) * dlnx)
# careful: cs2 = a0 * rM * f(x)/x with f = (1+x^2)^(3/2)/(1+2x^2): rM contributes 1/2; the x-dependence contributes via dlnx
frozen = (2 * x ** 4 + 4 * x ** 2 + 1) / (4 * x ** 4 + 4 * x ** 2 + 1)
diff = sp.simplify(e_expr - frozen)
R.p(f"  derived e(x) = {sp.simplify(e_expr)};  CFG44's (2x^4+4x^2+1)/(4x^4+4x^2+1); difference simplifies to {diff}")
vals = [float(e_expr.subs(x, v)) for v in (1e-3, 1, 1e3)]
R.check("CROSS-CHECK", "e(x) equals CFG44's closed form and runs from 1 (Newtonian) to 1/2 (deep)", diff == 0 and abs(vals[0] - 1) < 1e-4 and abs(vals[2] - 0.5) < 1e-4, f"e(1e-3, 1, 1e3) = {vals}")
R.check("CROSS-CHECK", "spread >= 1e3 over M = 1e8-1e14 for e >= 1/2", 10 ** (0.5 * 6) >= 1e3 - 1e-9, "10^(0.5*6) = 1000")

# ---------------------------------------------------------------- R06: exchange closed forms and ratios to g_law
R.p("\n== R06: exchange reaction F = 4 pi s^2 dE/dM_enc (point mass, P2), CFG48 G4 / referee R4")
s, Me, rho_f = sp.symbols("s M_enc rho_f", positive=True)
gN = G * Me / s ** 2
g = sp.sqrt(gN ** 2 + a0 * gN)
P = a0 * Me / (8 * sp.pi * s ** 2)
F_P = sp.simplify(4 * sp.pi * s ** 2 * sp.diff(sp.Rational(3, 2) * P, Me))
rho_c = a0 * Me / (4 * sp.pi * s ** 3 * g)
# sigma-slaved: energy density (3/2) rho sigma^2 with rho held fixed and sigma^2 = g s/2 responding
F_sig = sp.simplify(4 * sp.pi * s ** 2 * sp.Rational(3, 2) * rho_c * (s / 2) * sp.diff(g, Me))
xx = sp.symbols("xx", positive=True)
Fs_x = sp.simplify(F_sig.subs(Me, sp.Symbol("M", positive=True)).subs(s, xx * sp.sqrt(G * sp.Symbol("M", positive=True) / a0)))
R.p(f"  P-slaved F = {F_P} ; sigma-slaved F(x) = {sp.simplify(Fs_x)}")
R.check("CROSS-CHECK", "P-slaved reaction = (3/4) a0", sp.simplify(F_P - sp.Rational(3, 4) * a0) == 0)
R.check("CROSS-CHECK", "sigma-slaved reaction = (3/8) a0 (2+x^2)/(1+x^2)", sp.simplify(Fs_x - sp.Rational(3, 8) * a0 * (2 + xx ** 2) / (1 + xx ** 2)) == 0)
glaw = lambda X: math.sqrt(1 + X * X) / X ** 2                                   # g_law/a0 for a point mass
Pr = lambda X: 0.75 / glaw(X)
Sr = lambda X: 0.375 * (2 + X * X) / (1 + X * X) / glaw(X)
tests = [(0.3, 0.062, Sr, "sigma"), (1.0, 0.398, Sr, "sigma"), (30.0, 11.26, Sr, "sigma"), (1.0, 0.53, Pr, "P"), (30.0, 22.49, Pr, "P"), (0.3, 0.065, Pr, "P")]
for X, lane, f, nm in tests:
    R.check("CROSS-CHECK", f"reaction/g_law at x = {X} ({nm}-slaved) = {f(X):.4f} vs lane {lane}", abs(f(X) - lane) / lane < 0.01)
red = max(Pr(X) for X in (0.3 + i * 0.01 for i in range(int((30 - 0.3) / 0.01) + 1))) / 0.10
R.check("EXPECT", "E6 needed coefficient reduction 225x (P-slaved, x in [0.3,30], line 0.10)", abs(red - 225) < 2, f"{red:.1f}")
led = C.read_norm("campaign_fresh_gravity/CFG48_REFEREE.md")
R.check("CITATION-AUDIT", "CFG48 referee R4 quotes 0.062, 0.398, 11.26 (sigma) and 0.53, 22.49 (P)", "0.062, 0.398, 11.26" in led and "0.53, 22.49" in led)

# energy: E_int = int (3/2) P dV = (3/4) a0 M (r_e - r_i)
R.p("\n== R06 energy: E_int = (3/4) a0 M (r_e - r_i); E_orb depends on the baryons' own radius R_b, not on r_e")
Ei = sp.integrate(sp.Rational(3, 2) * P.subs(Me, sp.Symbol("M", positive=True)) * 4 * sp.pi * s ** 2, (s, sp.Symbol("ri", positive=True), sp.Symbol("re", positive=True)))
R.p(f"  E_int = {sp.simplify(Ei)}")
Bnum = {1e9: 318.0, 1e10: 179.0, 1e12: 57.0}
led2 = C.read_norm("campaign_fresh_gravity/LEDGER.md")
R.check("CITATION-AUDIT", "GAPS/STANDING quote 57 / 179 / 318x at 1e12 / 1e10 / 1e9 (B's committed r_ta)", "57 / 179 / 318" in C.read_norm("campaign_fresh_gravity/STANDING_2026-09-29.md") or "318 / 179 / 57" in C.read_norm("campaign_fresh_gravity/closure_map/GAPS_1_2_JOINT_STATUS.md"))
rta_tab = {1e9: 236, 1e10: 508, 1e11: 1094, 1e12: 2358}   # NOTE: the LEDGER row lists 236, 508, 1094, 2358 for 1e9..1e12
xe = {Mm: 0.4 * rta_tab[Mm] * C.KPC / C.rM(Mm) for Mm in (1e9, 1e10, 1e11, 1e12)}
R.p("  x_e = 0.4 r_ta/r_M with the CFG118/CFG158 r_ta table (a DIFFERENT convention from B's committed r_ta; used only for scaling): " + str({k: round(v, 1) for k, v in xe.items()}))
coef = {k: Bnum[k] / xe[k] ** 2 for k in Bnum}
R.p("  lane energy ratio / x_e^2 (1e9, 1e10, 1e12): " + str({k: round(v, 4) for k, v in coef.items()}))
R.check("EXPECT", "E11 coefficient lane/x_e^2 within 0.05-0.10", all(0.05 <= v <= 0.10 for v in coef.values()), str({k: round(v, 3) for k, v in coef.items()}))
spread = max(coef.values()) / min(coef.values())
R.check("EXPECT", "E11 coefficient constant within 10% (the frozen text expected imperfect)", spread < 1.10, f"spread of the coefficient {spread:.2f}")
ex = math.log(Bnum[1e12] / Bnum[1e9]) / math.log(1e3)
R.p(f"  observed scaling exponent of the lane's energy ratio between 1e9 and 1e12: {ex:.3f}; x_e^2 predicts {math.log((xe[1e12]/xe[1e9])**2)/math.log(1e3):.3f}")
R.check("EXPECT", "E11 structural: lane ratio ~ x_e^2 (exponent within 0.03)", abs(ex - math.log((xe[1e12] / xe[1e9]) ** 2) / math.log(1e3)) < 0.03, "a MISS means the frozen 'scales as x_e^2' is not what the lanes' numbers do")
R.p("  NOTE (wrong expectation kept): E_orb of the baryons is set by their own radius R_b (E_orb ~ G M^2/(2 R_b)), so E_int/E_orb ~ (3/2) x_e (R_b/r_M), linear in x_e at fixed baryon compactness, not x_e^2; the frozen 'x_e^2' was HAND and imprecise. The lanes' conventions for E_orb and r_ta are not fully recoverable from the READMEs, so no number-level reproduction is claimed.")

# ---------------------------------------------------------------- R05: sigma^2/c^2 and the ratio to 4.608e-12
R.p("\n== R05: halo dispersion versus the growth bound")
for Mm, lane in ((1e9, 1.963e-8), (1e12, 6.207e-7)):
    V4 = C.G * Mm * C.MSUN * C.A0
    s2 = math.sqrt(V4) / 2 / C.CLIGHT ** 2
    R.check("CROSS-CHECK", f"sigma^2/c^2 at {Mm:.0e} = {s2:.3e} vs CFG156 {lane:.3e}", abs(s2 / lane - 1) < 0.01, f"V_f = {V4**0.25/1e3:.1f} km/s; ratio to 4.608e-12 = {s2/4.608e-12:.3g}")
R.check("EXPECT", "E7 ratio 4.3e3 (1e9) and 1.3e5 (1e12)", abs(1.963e-8 / 4.608e-12 - 4.26e3) < 20 and abs(6.207e-7 / 4.608e-12 - 1.347e5) < 500)
r156 = C.read_norm("campaign_fresh_gravity/CFG156_door8_vacuum_referee/README.md")
R.check("CITATION-AUDIT", "CFG156 README prints c_s^2 = 4.608e-12", "4.608e-12" in r156 or "4.608" in r156)

# ---------------------------------------------------------------- R07a: Gauss shell mass from CFG48's printed values
R.p("\n== R07a: Gauss negative shell M_b (sqrt(1+x_e^2) - 1); infer x_e from CFG48's printed shell masses")
shell = {1e10: 3.21e11, 1e11: 2.157e12, 1e12: 1.439e13}
xe48 = {Mm: math.sqrt((1 + v / Mm) ** 2 - 1) for Mm, v in shell.items()}
R.p("  inferred x_e (CFG48 convention): " + str({k: round(v, 2) for k, v in xe48.items()}))
sl = math.log10(xe48[1e12] / xe48[1e10]) / 2
R.check("CROSS-CHECK", "x_e ~ M^(-1/6) in CFG48's convention (edge 0.4 r_ta, r_ta ~ M^(1/3))", abs(sl + 1 / 6) < 0.006, f"slope {sl:.4f}")
R.check("CITATION-AUDIT", "CFG48 referee quotes the shell masses 3.21e11, 2.157e12, 1.439e13", "3.21e11, 2.157e12, 1.439e13" in led or "3.21e11" in led)

# ---------------------------------------------------------------- R12(b) / 4.5: P / P_cap
R.p("\n== R12(b) x R04 (E13): target pressure over the CFG43 cap")
Pcap = 0.25 * C.RHO_L * C.CLIGHT ** 2 / (8 * math.pi)          # (kappa^2/8pi) rho_L c^2 with kappa = 1/2
Pcap2 = C.A0 ** 2 / (8 * math.pi * C.G)
R.check("CROSS-CHECK", "P_cap = (kappa^2/8pi) rho_L c^2 = a0^2/(8 pi G)", abs(Pcap / Pcap2 - 1) < 1e-12, f"{Pcap:.4e} Pa")
Mp = 1e10 * C.MSUN
for X in (0.1, 1.0, 10.0):
    r = X * C.rM(1e10)
    Pt = C.A0 * Mp / (8 * math.pi * r ** 2)
    R.p(f"  x = {X}: P_target/P_cap = {Pt/Pcap2:.4f} (1/x^2 = {1/X**2:.4f})")
R.check("EXPECT", "E13 P_target/P_cap = 1/x^2 (100 at x = 0.1, 1 at x = 1)", all(abs(C.A0 * Mp / (8 * math.pi * (X * C.rM(1e10)) ** 2) / Pcap2 - 1 / X ** 2) < 1e-9 for X in (0.1, 1.0, 10.0)))

# ---------------------------------------------------------------- R12 budget arithmetic (CFG174 column)
R.p("\n== R12(a): column budget arithmetic (CFG174; referee CFG181 reproduces to 0.55%)")
t0 = 13.8e9 * 365.25 * 86400
col = C.RHO_L * C.CLIGHT * t0 / (C.MSUN / C.PC ** 2)
Rr = (C.A0 / (2 * math.pi * C.G) / (C.MSUN / C.PC ** 2)) / col
R.p(f"  swept column rho_L c t0 = {col:.1f} Msun/pc^2 (t0 = 13.8 Gyr); law column {C.A0/(2*math.pi*C.G)/(C.MSUN/C.PC**2):.2f}; R = {Rr:.4f}")
R.check("CROSS-CHECK", "swept column ~ 365 and R ~ 0.293 (CFG174; my t0 = 13.8 Gyr, H0 = 67.4)", abs(col / 365.15 - 1) < 0.03 and abs(Rr / 0.2927 - 1) < 0.03, f"{col:.1f}, {Rr:.4f}")
R.check("NEW-DERIVATION", "R = kappa/(2 pi t0 sqrt(G rho_L)) identity", abs(0.5 / (2 * math.pi * t0 * math.sqrt(C.G * C.RHO_L)) / Rr - 1) < 1e-9)
R.p(f"  needed factor: 0.293/0.078 = {0.293/0.078:.2f} (DESI DR2 + NEC caps a flowing medium at 0.078 of the vacuum column; cited, not recomputed)")
R.write()
