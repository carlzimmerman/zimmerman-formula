"""CFG888 -- does an overfill cold-energy clump's own gravity follow the law?  Decided from the record's equations.
Criteria: FROZEN_CRITERIA.md (dd7b30afb, committed alone before this script).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg888.py   (CFG888_MUTATE=1: the branch is swapped everywhere, separate outputs).
Parts: S structural (sympy + ID energy), A Newtonian isothermal (branch a), B self-boosted isothermal (branch b, conditional),
C stiffened field equation at the clump scale, D host fields.  kappa = 1/2 FITTED; footings never pooled; cold energy mass
required; no particle species; not theory closed."""
import os, sys, json, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, solve_bvp

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG888_MUTATE") == "1"; SUF = "_MUTATE" if MUT else ""; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

# ---------------------------------------------------------------- constants (CFG878's), units pc, Msun, km/s
G_SI, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
G = G_SI * MSUN / (PC * 1e6)                                   # pc (km/s)^2 / Msun
A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0 = {f: v * PC / 1e6 for f, v in A0SI.items()}                # (km/s)^2 / pc
FOOT = ("canonical", "alt")
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-300))))
nu_s = lambda y: 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / np.maximum(y, 1e-300)))      # simple nu: g_N = g^2/(g + a0)
ulaw_s = lambda gN, a0: 0.5 * (-gN + np.sqrt(gN * gN + 4.0 * gN * a0))          # u = g - g_N, u^2/(a0-u) = g_N
J = lambda *p: json.load(open(os.path.join(LANES, *p)))
R877 = J("CFG877_finite_cold_clump", "cfg877_results.json"); R878 = J("CFG878_fragment_mass", "cfg878_results.json")
RC870 = 104.0
SIG = {f: float(R877[f]["sigma"]) for f in FOOT}; VX = {f: float(R877[f]["Vx"]) for f in FOOT}
MDEEP = lambda s, a0: 81.0 * s ** 4 / (4.0 * G * a0)
MCL877 = {f: MDEEP(SIG[f], A0[f]) for f in FOOT}               # CFG877's M_cl (its line 80)
RHO870 = {f: 3 * VX[f] ** 2 / (4 * math.pi * G * RC870 ** 2) for f in FOOT}
RHO_GRID = (0.01, 0.1, 0.6, 3.0); RADII = (100.0, 200.0, 500.0, 1000.0)
HOSTS = {"H1": (1e4, 30.0), "H2": (3e5, 200.0), "H3": (2e7, 700.0)}
STOCK = 53.64
Mx870 = lambda r, f: VX[f] ** 2 * r ** 3 / (G * (r * r + RC870 ** 2))
Mx877 = lambda r, f: np.minimum(Mx870(r, f), MCL877[f])
plum = lambda r, Mb, a: Mb * r ** 3 / (r * r + a * a) ** 1.5
RES = dict(lane="CFG888", mutate=MUT, sigma=SIG, Vx=VX, Mcl877=MCL877, rho870=RHO870, a0_pc=A0, G_pc=G)
K = {}
P("CFG888  clump self-gravity from the record's equations" + ("   [MUTATE: branch swapped]" if MUT else ""))
P(f"  sigma (CFG877) {SIG['canonical']:.4f} / {SIG['alt']:.4f} km/s; M_cl(CFG877) {MCL877['canonical']:.3e} / {MCL877['alt']:.3e};"
  f" rho0_870 {RHO870['canonical']:.3f} / {RHO870['alt']:.3f} Msun/pc^3")

# ================================================================ Q1: the record's text and code (file:line, read-only)
NEEDLES = [
    ("i", "CFG541_cold_energy_equations_precise/EQUATIONS.md", "(E2) Gravity.** ∇²Φ = 4πG (ρ_b + ρ_c)", "class A gravity: Newtonian, baryons + cold energy"),
    ("i", "CFG541_cold_energy_equations_precise/EQUATIONS.md", "Only the region's own baryons enter", "E7 round-rule phantom: region's own baryons"),
    ("i", "CFG541_cold_energy_equations_precise/EQUATIONS.md", "ρ_ph is a functional of the", "rho_ph is a functional of the baryons"),
    ("i", "CFG541_cold_energy_equations_precise/cfg541.py", "y = G * self.Mbf / (rf ** 2 * a0)", "code: law argument from baryon mass only"),
    ("i", "CFG541_cold_energy_equations_precise/cfg541.py", "self.Mphf = self.Mbf * nu_m1(y)", "code: phantom = M_b (nu - 1)"),
    ("i", "CFG638_cold_energy_fluid_equations/README.md", "∇²Φ = 4πG(ρ_b + ρ_c)", "fluid system: Newtonian Phi, psi toward rho_ph"),
    ("i", "CFG638_cold_energy_fluid_equations/README.md", "overfill not handled", "fluid system: overfill open item"),
    ("ii", "THEORY_CANONICAL_2026-10-14.md", "− ρ_b Φ − W_rem(u)", "canonical S2 action: matter term -rho_b Phi only"),
    ("ii", "THEORY_CANONICAL_2026-10-14.md", "displacement is P (∂ₜP = −j, ∇·P = ρ − ρ̄", "canonical S3: cold energy = displacement of P (ID)"),
    ("ii", "THEORY_CANONICAL_2026-10-14.md", "ordinary gravity and never re-tethers", "canonical S4: free cold energy 'bound by ordinary gravity', coupling not written"),
    ("ii", "CFG722_cold_kinetic_bridge/README.md", "the critical quadratic cancels the carrier's", "ID: carrier self-gravity cancelled"),
    ("ii", "CFG722_cold_kinetic_bridge/README.md", "sourced by M_b + M_c (two-sector double counting)", "coupling G: cold mass would source the phantom"),
    ("ii", "CFG722_cold_kinetic_bridge/README.md", "The tether reads g_N of all baryons", "ID: tether reads baryons' g_N"),
    ("ii", "CFG722_cold_kinetic_bridge/README.md", "overflow **cannot sit in the core**", "ID: overflow pushed out"),
    ("ii", "CFG747_collisionless_relaxation/README.md", "The critical tether cancels the cold energy's self-gravity", "tether dynamics: r'' = -1/r^2 + m^2/r^4"),
    ("ii", "CFG776_frozen_relic/README.md", "surplus tethered cold energy is dynamically unstable", "surplus expelled"),
    ("iii", "CFG809_expelled_gas_split/cfg809.py", '(core if variant in ("ALL", "EX") else Mcond)', "H-EX: law source = condensed/core baryons"),
    ("iii", "CFG809_expelled_gas_split/cfg809.py", "return I.rg, I.M_core_g, I.M_set_g * s, I.M_res_g * s, meta", "H-EX: free reservoir returned separately"),
    ("iii", "CFG822_hex_dsph/cfg822.py", "Mtot = float(np.interp(r12, rg, Mcore)) + float(np.interp(r12, rg, Mset)) + fr", "free mass added outside nu"),
    ("iii", "CFG877_finite_cold_clump/cfg877.py", "def sx2(r_pc, Vx, Mcl): return G * Mx(r_pc, Vx, Mcl) / (3 * r_pc * PC) / 1e6", "clump added Newtonianly to sigma^2"),
    ("hlink", "CFG877_finite_cold_clump/cfg877.py", "Mcl = 81 * (sig * 1e3) ** 4 / (4 * G * a0)", "H-LINK: clump mass from the self-boost formula"),
    ("hlink", "CFG878_fragment_mass/cfg878.py", "gN = G * M_ / rr ** 2; g = gN * float(nu_e(gN / a0))", "H-LINK: clump's own mass inside nu"),
    ("hlink", "CFG871_law_linked_core/README.md", "The clump's own law-boost is an assumption of H-LINK", "H-LINK flagged as assumption"),
]
CIT = []
for tag, rel, needle, what in NEEDLES:
    lines = open(os.path.join(LANES, rel), encoding="utf-8").read().split("\n")
    hits = [i + 1 for i, l in enumerate(lines) if needle in l]
    CIT.append(dict(tag=tag, file=rel, lines=hits, what=what, found=bool(hits)))
P("\n== Q1 record citations (file:line)")
for c in CIT:
    P(f"  [{c['tag']:5s}] {c['file']}:{','.join(map(str, c['lines'])) or 'NOT FOUND'}  -- {c['what']}")
RES["citations"] = CIT

# ================================================================ Part S: sympy structure of the canonical action
P("\n== Part S: the canonical square action, one Fourier mode (rho_b = B cos kx, rho_c = C cos kx)")
x = sp.symbols("x", real=True); k, Kk = sp.symbols("k K", positive=True); B, C = sp.symbols("B C", real=True)
Phi_f, P_f = sp.Function("Phi")(x), sp.Function("P")(x)
rb, rc = B * sp.cos(k * x), C * sp.cos(k * x)
def lag(src, crit):
    return -sp.diff(Phi_f, x) ** 2 / (2 * Kk) + sp.diff(Phi_f, x) * P_f - crit * Kk * P_f ** 2 / 2 - src * Phi_f
def gN_source(L, Psub=None):
    el = sp.euler_equations(L, [Phi_f], x)[0].lhs
    Phipp = sp.solve(el, sp.diff(Phi_f, x, 2))[0]
    s = Phipp - Kk * sp.diff(P_f, x)                      # (Phi' - K P)'  = minus the divergence of g_N
    if Psub is not None: s = s.subs(P_f, Psub).doit()
    return sp.simplify(s)
avg = lambda e: sp.simplify(k / (2 * sp.pi) * sp.integrate(sp.expand(e), (x, 0, 2 * sp.pi / k)))
Pid = C / k * sp.sin(k * x)                                # dP/dx = rho_c : identification (ID)
crit_S1 = 0 if MUT else 1                                  # M3: the critical quadratic -K P^2/2 dropped
# S1: ID on-shell Lagrangian
L_id = lag(rb, crit_S1)
phi_amp = sp.symbols("phi")
el = sp.euler_equations(L_id, [Phi_f], x)[0].lhs.subs(P_f, Pid).doit()
sol_phi = sp.solve(sp.simplify(el.subs(Phi_f, phi_amp * sp.cos(k * x)).doit() / sp.cos(k * x)), phi_amp)[0]
Lon = avg(L_id.subs(P_f, Pid).subs(Phi_f, sol_phi * sp.cos(k * x)).doit())
Lnew = sp.expand(Kk * (B + C) ** 2 / (4 * k ** 2))        # Newtonian -V for rho = (B + C) cos kx
cC2, cBC, cB2 = [sp.simplify(sp.Poly(sp.expand(Lon), B, C).coeff_monomial(m)) for m in (C ** 2, B * C, B ** 2)]
nC2, nBC, nB2 = [sp.Poly(Lnew, B, C).coeff_monomial(m) for m in (C ** 2, B * C, B ** 2)]
S1 = (cC2 == 0) and sp.simplify(cBC - nBC) == 0 and sp.simplify(cB2 - nB2) == 0
P(f"  S1 (ID) on-shell <L> = {sp.factor(Lon)};  Newtonian -V = {sp.factor(Lnew)}")
P(f"      C^2 coefficient {cC2} (Newtonian {nC2}); BC {cBC} (Newtonian {nBC}); B^2 {cB2} -> carrier self-gravity "
  + ("CANCELLED exactly; mutual baryon-carrier term Newtonian" if S1 else "NOT cancelled"))
# S2/S3: the source of the law's g_N
src_G = gN_source(lag(rb + rc, 1))
src_ID = gN_source(lag(rb, 1), Pid)
S2 = sp.simplify(src_G - Kk * (rb + rc)) == 0
S3 = sp.simplify(src_ID - Kk * rb) == 0 and sp.diff(src_ID, C) == 0
P(f"  S2 (coupling G, matter term -(rho_b + rho_c) Phi): (Phi' - K P)' = {src_G}  -> law source includes rho_c: {S2}")
P(f"  S3 (ID, dP/dx = rho_c, matter term -rho_b Phi):     (Phi' - K P)' = {src_ID}  -> law source baryons only: {S3}")
# S4: stiffness under ID is a local rho_c^2 energy
S4a = sp.simplify(avg(sp.diff(Pid, x) ** 2) - avg(rc ** 2)) == 0
k1, k2, k3 = sp.symbols("k1 k2 k3", real=True); ra, rbm = sp.symbols("ra rb", real=True)
kv = [k1, k2, k3]; ksq = k1 ** 2 + k2 ** 2 + k3 ** 2; rhat = ra + sp.I * rbm
Ph = [-sp.I * kk * rhat / ksq for kk in kv]
gradsq = sum(sp.expand((kv[i] * Ph[j]) * sp.conjugate(kv[i] * Ph[j])) for i in range(3) for j in range(3))
S4b = sp.simplify(gradsq - sp.expand(rhat * sp.conjugate(rhat))) == 0
S4 = S4a and S4b
P(f"  S4 longitudinal P: <|dP/dx|^2> = <rho_c^2> ({S4a}); 3-D |k|^2|P_hat|^2 = |rho_hat|^2 ({S4b})"
  " -> (gamma/2)|grad P|^2 = pi G L*^2 rho_c^2: a local repulsive self-energy (pressure pi G L*^2 rho_c^2)")
K["K4_S1"] = bool(S1); K["K4_S2"] = bool(S2); K["K4_S3"] = bool(S3); K["K4_S4"] = bool(S4)
RES["S"] = dict(S1_onshell=str(sp.factor(Lon)), S1_C2=str(cC2), S1_BC=str(cBC), S2_source=str(src_G), S3_source=str(src_ID),
                S1=bool(S1), S2=bool(S2), S3=bool(S3), S4=bool(S4))

# ---------------------------------------------------------------- S5: ID tether force on a law-settled host + CFG877 clump
P("\n== S5: ID energy E[M] = -int M g_Nb dr + int W(GM/r^2) 4 pi r^2 dr;  F = dE/dM(<r) = -g_Nb + u^2/(a0-u)  (F > 0: outward)")
def KW(u, a0):                                             # K*W(u) = a0^2 sum_{n>=3} x^n/n,  K W'(u) = u^2/(a0-u)
    xx = u / a0; ser = sum(xx ** n / n for n in range(3, 40))
    with np.errstate(invalid="ignore", divide="ignore"):
        lg = -np.log1p(-np.minimum(xx, 1 - 1e-15)) - xx - xx * xx / 2
    return a0 ** 2 * np.where(xx < 0.05, ser, lg)
rS = np.geomspace(1e-2, 1e5, 30001)
def energy(M, gNb, a0, selfg=False):
    u = G * M / rS ** 2
    E = np.trapz(-M * gNb, rS) + np.trapz(KW(u, a0) * rS ** 2 / G, rS)
    if selfg: E += np.trapz(-G * M * np.gradient(M, rS) / rS, rS)
    return E
RES["S5"] = {}; k5i, k5ii, s5pos = True, True, True
win = (rS >= 1) & (rS <= 1000); win4 = (rS >= 1) & (rS <= 1e4)
for f in FOOT:
    a0 = A0[f]
    for h, (Mb, a) in HOSTS.items():
        gNb = G * plum(rS, Mb, a) / rS ** 2
        uL = ulaw_s(gNb, a0); ML = uL * rS ** 2 / G
        FL = -gNb + uL ** 2 / (a0 - uL)
        if MUT: FL = FL - G * ML / rS ** 2                       # M4: carrier's Newtonian self-gravity added back
        lawres = float(np.max(np.abs(FL[win4]) / gNb[win4]))
        Mex = Mx877(rS, f); M = ML + Mex; u = G * M / rS ** 2
        cap = float(np.max(u / a0))
        F = -gNb + u ** 2 / (a0 - u)
        fr = F[win] / gNb[win]
        dM = Mex * np.exp(-np.log(rS / 100.0) ** 2 / (2 * 0.3 ** 2)); eps = 1e-4
        dEfd = (energy(M + eps * dM, gNb, a0) - energy(M - eps * dM, gNb, a0)) / (2 * eps)
        dEan = np.trapz(F * dM, rS); fdrel = abs(dEfd / dEan - 1)
        rho = np.gradient(Mex, rS) / (4 * math.pi * rS ** 2); rhop = np.gradient(rho, rS)
        ih = int(np.searchsorted(Mex, MCL877[f] / 2)); Fs = -2 * math.pi * G * 24.0 ** 2 * rhop[ih]
        RES["S5"][f"{f}|{h}"] = dict(law_residual=lawres, minF_over_gNb=float(fr.min()), maxF_over_gNb=float(fr.max()), max_u_over_a0=cap,
                                     fd_rel=float(fdrel), r_half=float(rS[ih]), stiff24_over_tether=float(Fs / F[ih]))
        k5i &= lawres <= 1e-9; k5ii &= fdrel <= 1e-4; s5pos &= bool(fr.min() > 0) and cap < 1
        P(f"  [{f:9s}] {h}: law |F|/g_Nb max {lawres:.1e};  law+clump F/g_Nb on 1-1000 pc: min {fr.min():+.3e} max {fr.max():+.3e};"
          f"  max u/a0 {cap:.3f};  FD check {fdrel:.1e};  at r_half {rS[ih]:.0f} pc stiffness(24 pc)/tether push {Fs / F[ih]:.3f}")
K["K5_i_law_stationary"] = bool(k5i); K["K5_ii_fd"] = bool(k5ii)
CLS_ID = "EXCESS PUSHED OUT (no self-bound clump)" if s5pos else "LOCALLY BOUND"
P(f"  ID verdict on the clump: {CLS_ID}  (F > 0 at every radius 1-1000 pc, H1-H3, both footings: {s5pos})")
RES["CLS_ID"] = CLS_ID

# ================================================================ isothermal integrator (Parts A, B, C, D)
def iso(sig, rho0, mode, a0, host=None, rmax=3e5, stop=1e-14, kern=nu_e, uext=None, r_in=1e-3):
    """mode 'N': g = G M/r^2 [+ host law field] [+ uext];  mode 'B': g = law(G (M + M_host)/r^2) with kernel kern."""
    s2 = sig * sig
    def gfun(r, M):
        Mh = plum(r, *host) if host else 0.0
        if mode == "B":
            gN = G * (M + Mh) / r ** 2; return gN * kern(gN / a0)
        g = G * M / r ** 2
        if host:
            gh = G * Mh / r ** 2; g += gh * kern(gh / a0)
        if uext is not None: g += uext(r)
        return g
    def rhs(s, y):
        r = math.exp(s); return [-gfun(r, y[1]) * r / s2, 4 * math.pi * r ** 3 * math.exp(y[0])]
    ev = lambda s, y: y[0] - math.log(stop * rho0); ev.terminal = True; ev.direction = -1
    sol = solve_ivp(rhs, (math.log(r_in), math.log(rmax)), [math.log(rho0), 4 / 3 * math.pi * r_in ** 3 * rho0], method="DOP853",
                    rtol=1e-11, atol=[1e-12, 1e-30], dense_output=True, events=ev if stop else None)
    rs = math.exp(sol.t[-1]); Ms = float(sol.y[1, -1]); rhos = math.exp(sol.y[0, -1])
    def M(r):
        r = np.atleast_1d(np.asarray(r, float)); out = np.full(r.shape, Ms)
        m = r <= rs; out[m] = sol.sol(np.log(r[m]))[1] if m.any() else out[m]; return out
    def rho(r):
        r = np.atleast_1d(np.asarray(r, float)); out = np.zeros(r.shape)
        m = r <= rs; out[m] = np.exp(sol.sol(np.log(r[m]))[0]) if m.any() else out[m]; return out
    g = lambda r: np.array([gfun(rr, mm) for rr, mm in zip(np.atleast_1d(r), M(r))])
    slope = lambda r: float(4 * math.pi * r ** 3 * rho(r)[0] / M(r)[0])
    al = gfun(rs, Ms) * rs / s2; tail = 4 * math.pi * rs ** 3 * rhos / (al - 3) if al > 3 else float("inf")
    return dict(M=M, rho=rho, g=g, slope=slope, r_stop=rs, M_stop=Ms, M_tail=Ms + tail, sol=sol)

# ================================================================ Part A: branch (a), Newtonian self-gravity (record branch)
modeA = "B" if MUT else "N"                                 # M1: self-boost forced ON
P("\n== Part A: branch (a) -- isolated clump with Newtonian self-gravity" + ("  [M1: self-boost forced ON]" if MUT else ""))
P("   r_0 = 3 sigma/sqrt(4 pi G rho0);  M(<100/200/500/1000 pc);  dlnM/dlnr and M/(2 sigma^2 r/G) at 1e4 pc")
RES["A"] = {}
for f in FOOT:
    s = SIG[f]; a0 = A0[f]
    for rho0 in RHO_GRID + (RHO870[f],):
        rsc = s / math.sqrt(4 * math.pi * G * rho0); r0 = 3 * rsc
        Z = iso(s, rho0, modeA, a0, rmax=max(1.1e4 * rsc, 1.1e4), stop=None)
        Mr = Z["M"](np.array(RADII)); sl4 = Z["slope"](1e4); rat4 = float(Z["M"](1e4)[0] / (2 * s * s * 1e4 / G))
        lab = f"{rho0:.3f}" if rho0 not in RHO_GRID else f"{rho0}"
        RES["A"][f"{f}|{lab}"] = dict(rho0=rho0, r_s=rsc, r0=r0, M=dict(zip(map(str, RADII), map(float, Mr))), slope_1e4pc=sl4, sis_ratio_1e4pc=rat4)
        P(f"  [{f:9s}] rho0 {rho0:6.3f}: r_0 {r0:7.1f} pc | M(<100) {Mr[0]:.3e}  M(<200) {Mr[1]:.3e}  M(<500) {Mr[2]:.3e}  M(<1000) {Mr[3]:.3e}"
          f" | dlnM/dlnr(1e4 pc) {sl4:.3f}  M/(2s^2r/G) {rat4:.3f}")
        if f == "canonical" and rho0 == 0.6:
            xi = lambda X: X ** 2 / 6 - X ** 4 / 120 + X ** 6 / 1890 - 61 * X ** 8 / 1632960
            d1 = [abs(Z["rho"](X * rsc)[0] / rho0 - math.exp(-xi(X))) for X in (0.5, 1.0)]
            sl = Z["slope"](1e4 * rsc); rr = float(Z["M"](1e4 * rsc)[0] / (2 * s * s * 1e4 * rsc / G))
            K["K1_series"] = bool(max(d1) <= 1e-4); K["K1_M_propto_r"] = bool(abs(sl - 1) <= 0.05); K["K1_SIS_norm"] = bool(abs(rr - 1) <= 0.05)
            RES["K1"] = dict(series_dev=d1, slope_1e4rs=sl, sis_ratio_1e4rs=rr)
            P(f"      K1: Emden series |d(rho/rho0)| at xi 0.5/1 = {d1[0]:.1e}/{d1[1]:.1e}; dlnM/dlnr at 1e4 r_s {sl:.4f}; M/(2s^2r/G) {rr:.4f}")
# R1: Newtonian clump at CFG870's central density vs CFG870's extended form and CFG877's capped form
P("  R1 (report): Newtonian clump at rho0_870 vs CFG870 extended M_x (uncapped) and CFG877 capped M_x")
RES["R1"] = {}
for f in FOOT:
    Mr = np.array(list(RES["A"][f"{f}|{RHO870[f]:.3f}"]["M"].values())); e = Mx870(np.array(RADII), f); c = Mx877(np.array(RADII), f)
    RES["R1"][f] = dict(vs_870=list(Mr / e), vs_877=list(Mr / c))
    P(f"  [{f:9s}] Emden/CFG870 at 100/200/500/1000 pc: " + " / ".join(f"{v:.3f}" for v in Mr / e)
      + "   Emden/CFG877(capped): " + " / ".join(f"{v:.2f}" for v in Mr / c)
      + f"   (asymptotic V_c = sqrt2 sigma = {math.sqrt(2) * SIG[f]:.3f} = V_x {VX[f]:.3f} km/s by identity)")

# ================================================================ Part B: branch (b), self-boost (CONDITIONAL on coupling G)
modeB = "N" if MUT else "B"                                 # M2: self-boost forced OFF
P("\n== Part B: branch (b) -- isolated clump whose own gravity follows the law (CONDITIONAL)" + ("  [M2: self-boost forced OFF]" if MUT else ""))
RES["B"] = {}; fall = []; k3 = True
for f in FOOT:
    s = SIG[f]; a0 = A0[f]; Md = MDEEP(s, a0)
    for rho0 in RHO_GRID + (RHO870[f],):
        Z = iso(s, rho0, modeB, a0)
        fv = Z["M_stop"] / Md; Mr = Z["M"](np.array(RADII))
        rr = np.geomspace(1, Z["r_stop"], 4000); Mg = Z["M"](rr); rh = float(np.interp(Z["M_stop"] / 2, Mg, rr))
        ph = {str(R): float(Z["g"](R)[0] * R * R / G - Z["M"](R)[0]) for R in (200.0, 1000.0)}
        lab = f"{rho0:.3f}" if rho0 not in RHO_GRID else f"{rho0}"
        RES["B"][f"{f}|{lab}"] = dict(rho0=rho0, M_total=Z["M_stop"], M_tail_corrected=Z["M_tail"], f=fv, r_stop=Z["r_stop"],
                                      M=dict(zip(map(str, RADII), map(float, Mr))), r_half=rh, phantom=ph)
        if rho0 in RHO_GRID: fall.append((f, rho0, fv))
        P(f"  [{f:9s}] rho0 {rho0:6.3f}: M_tot {Z['M_stop']:.3e} (tail-corr {Z['M_tail']:.3e}), f {fv:.3f} | M(<100) {Mr[0]:.3e}  M(<200) {Mr[1]:.3e}"
          f"  M(<500) {Mr[2]:.3e}  M(<1000) {Mr[3]:.3e} | r_half {rh:6.1f} pc | phantom(<200) {ph['200.0']:.2e}  (<1000) {ph['1000.0']:.2e}")
    for rho0 in RHO_GRID:                                   # K3: CFG878 cross-code at sigma 7.53
        fv = iso(7.53, rho0, modeB, a0)["M_stop"] / MDEEP(7.53, a0); ref = R878["A"][f"{f}|7.53"][str(rho0)]
        k3 &= abs(fv / ref - 1) <= 0.01
        RES["B"][f"K3|{f}|{rho0}"] = dict(f=fv, cfg878=ref)
f01 = [fv for (ft, r0_, fv) in fall if r0_ == 0.01]
K["K2_deep_limit"] = bool(all(abs(v - 1) <= 0.06 for v in f01)); K["K2_band"] = bool(all(0.74 <= v <= 0.96 for (_, _, v) in fall))
K["K3_cfg878"] = bool(k3)
P(f"  K2: f(rho0=0.01) = {', '.join(f'{v:.3f}' for v in f01)}; all f in [{min(v for *_, v in fall):.3f}, {max(v for *_, v in fall):.3f}]."
  f"  K3 (CFG878 f at sigma 7.53 within 1%): {'PASS' if k3 else 'FAIL'}")
# R3: the clump's phantom must be tethered cold energy (ID), drawn from the supply
P("  R3 (report): self-boost needs tethered cold energy = the clump's phantom; vs the largest catchment stock 53.64 M_b")
RES["R3"] = {}
for f in FOOT:
    ph = RES["B"][f"{f}|0.6"]["phantom"]
    row = {str(Mb): dict(p200=ph["200.0"] / (STOCK * Mb), p1000=ph["1000.0"] / (STOCK * Mb)) for Mb in (1e3, 1e4, 1e5, 1e6)}
    RES["R3"][f] = row
    P(f"  [{f:9s}] phantom(<200 pc)/(53.64 M_b) for M_b 1e3/1e4/1e5/1e6: " + " / ".join(f"{v['p200']:.2f}" for v in row.values())
      + "   (<1 kpc): " + " / ".join(f"{v['p1000']:.2f}" for v in row.values()))
# R4: the action's own static kernel
RES["R4"] = {}
for f in FOOT:
    if MUT: break
    fs = iso(SIG[f], 0.6, "B", A0[f], kern=nu_s)["M_stop"] / MDEEP(SIG[f], A0[f]); RES["R4"][f] = fs
    P(f"  R4 (report) [{f}]: f at rho0 0.6 with the simple nu (canonical action's static law) = {fs:.3f}")

# ================================================================ Part C: stiffened field equation at the clump scale (branch b)
P("\n== Part C: stiffness at the clump scale: u^2/(a0-u) - (L*^2/2)(u'' + 2u'/r - 2u/r^2) = g_N (branch b source, rho0 0.6)")
LST = (1.0, 24.0, 100.0, 300.0, 1000.0); RCH = (50.0, 100.0, 200.0, 500.0)
def bvp(Msrc, L, a0, guess=None):
    gN = lambda r: G * np.reshape(Msrc(r), np.shape(r)) / r ** 2 / a0      # scalar in -> scalar out (correction 2)
    r = np.geomspace(0.05, 3e5, 900); uL = ulaw_s(gN(r), 1.0); c = L * L / 2.0
    def fun(rr, y):
        u = np.minimum(y[0], 0.999999)
        return np.vstack([y[1], (u * u / (1 - u) - gN(rr)) / c - 2 * y[1] / rr + 2 * y[0] / rr ** 2])
    bc = lambda ya, yb: np.array([ya[0] - r[0] * ya[1], yb[0] - ulaw_s(gN(r[-1]), 1.0)])
    y0 = guess if guess is not None else np.vstack([uL, np.gradient(uL, r)])
    sol = solve_bvp(fun, bc, r, y0, tol=1e-6, max_nodes=300000)
    return sol, gN
RES["C"] = {}; k6 = True
for f in FOOT:
    a0 = A0[f]; Zb = iso(SIG[f], 0.6, "B", a0); Msrc = lambda r, Z=Zb: Z["M"](r)
    for L in LST:
        sol, gN = bvp(Msrc, L, a0)
        Rs = [float((gN(R) + sol.sol(R)[0]) / (gN(R) + ulaw_s(gN(R), 1.0))) for R in RCH]
        RES["C"][f"{f}|{L}"] = dict(success=bool(sol.success), R_s=dict(zip(map(str, RCH), Rs)), est_100=L * L / (100.0 * 4.5 * SIG[f] ** 2 / a0))
        if L == 1.0: k6 &= bool(sol.success) and abs(Rs[1] - 1) <= 1e-3
        P(f"  [{f:9s}] L* {L:6.0f} pc: R_s at 50/100/200/500 pc = " + " / ".join(f"{v:.4f}" for v in Rs)
          + f"   (solver {'ok' if sol.success else 'FAILED'}; estimate L*^2/(r r_M) at 100 pc {L * L / (100.0 * 4.5 * SIG[f] ** 2 / a0):.3f})")
K["K6_stiff_control"] = bool(k6)
CLS_ST = "NEGLIGIBLE AT THE WINDOW'S LOWER EDGE" if all(RES["C"][f"{f}|24.0"]["R_s"]["100.0"] >= 0.95 for f in FOOT) else "MATTERS AT 24 pc"
P(f"  stiffness class (R_s(100 pc, L* 24 pc) >= 0.95 both footings): {CLS_ST}")
# report-only: self-consistent stiffened clump
RES["C_sc"] = {}
if not MUT:
    for f in FOOT:
        a0 = A0[f]; base = iso(SIG[f], 0.6, "B", a0, kern=nu_s)["M_stop"]
        for L in (24.0, 100.0):
            Z = iso(SIG[f], 0.6, "B", a0, kern=nu_s); Mt = Z["M_stop"]; conv = False
            rg = np.geomspace(0.05, 3e5, 20000); lrg = np.log(rg)
            for it in range(40):
                sol, gN = bvp(lambda r, Z=Z: Z["M"](r), L, a0)
                if not sol.success: break
                ut = np.clip(sol.sol(rg)[0], 0, 1) * a0          # tabulated u_stiff (km/s)^2/pc; u ~ r below 0.05 pc
                def ue(r, ut=ut):
                    return ut[0] * r / 0.05 if r < 0.05 else float(np.interp(math.log(r), lrg, ut))
                Z = iso(SIG[f], 0.6, "N", a0, uext=ue); dM = abs(Z["M_stop"] / Mt - 1); Mt = Z["M_stop"]
                if dM < 1e-3: conv = True; break
            RES["C_sc"][f"{f}|{L}"] = dict(converged=conv, iterations=it + 1, M_tot=Mt, over_unstiffened_simple=Mt / base, over_Mdeep=Mt / MDEEP(SIG[f], a0))
            P(f"  C_sc (report) [{f:9s}] L* {L:5.0f} pc: " + (f"M_tot {Mt:.3e} = {Mt / base:.3f} x unstiffened (simple nu), {Mt / MDEEP(SIG[f], a0):.3f} x M_deep"
              if conv else f"not converged after {it + 1} iterations (last M_tot {Mt:.3e})"))

# ================================================================ Part D: the clump inside a host's field, both branches
P("\n== Part D: clump (rho0 0.6) in hosts H1-H3; (a) host law field + Newtonian clump; (b) law(M_b + M_cl)")
RD = (100.0, 200.0, 500.0, 1000.0, 5000.0, 1e4)
RES["D"] = {}; conf_ok = True; addp = True
for f in FOOT:
    a0 = A0[f]; s = SIG[f]; Mcrit = 9 * s ** 4 / (G * a0)
    P(f"  [{f}] M_crit = 9 sigma^4/(G a0) = {Mcrit:.3e} Msun;  sqrt3 sigma = {math.sqrt(3) * s:.2f} km/s")
    for h, (Mb, a) in HOSTS.items():
        Vh = (G * Mb * a0) ** 0.25
        for br, md in (("a", "B" if MUT else "N"), ("b", "N" if MUT else "B")):
            Z = iso(s, 0.6, md, a0, host=(Mb, a), rmax=1e5, stop=None)
            Mr = Z["M"](np.array(RD)); sl = Z["slope"](1e4)
            RES["D"][f"{f}|{h}|{br}"] = dict(M=dict(zip(map(str, RD), map(float, Mr))), slope_1e4=sl, V_h=Vh, above_Mcrit=bool(Mb > Mcrit))
            P(f"    {h} (V_h,inf {Vh:5.2f} km/s) branch ({br}): M(<100/200/500/1e3/5e3/1e4 pc) = " + " ".join(f"{v:.2e}" for v in Mr) + f"  dlnM/dlnr(1e4) {sl:.3f}")
            if br == "a":
                if Mb > Mcrit: conf_ok &= sl < 0.1
                else:
                    conf_ok &= sl >= 0.5; addp &= Mr[5] > 3 * Mr[3]
CLS_CONF = "HOST CONFINEMENT CRITERION CONFIRMED" if conf_ok else "HOST CONFINEMENT CRITERION NOT CONFIRMED"
P(f"  {CLS_CONF};  replacement (branch a) {'ADDS A PARAMETER (outer truncation not set by sigma for hosts below M_crit)' if addp else 'does not add a parameter by the frozen rule'}")
# R2: the clump's extra acceleration over the host's law
P("  R2 (report): extra acceleration over the host's law at 200/500/1000/2000 pc: (b) / CFG870 extended, (b) / CFG877 capped")
RES["R2"] = {}; dom = True
for f in FOOT:
    a0 = A0[f]
    for h, (Mb, a) in HOSTS.items():
        Z = iso(SIG[f], 0.6, "N" if MUT else "B", a0, host=(Mb, a), rmax=1e5, stop=None)
        rr = np.array([200.0, 500.0, 1000.0, 2000.0]); Mbr = plum(rr, Mb, a); Mc = Z["M"](rr)
        law = lambda m: (G * m / rr ** 2) * nu_e(G * m / rr ** 2 / a0)
        gb = law(Mbr + Mc) - law(Mbr); ge = G * Mx870(rr, f) / rr ** 2; gc = G * Mx877(rr, f) / rr ** 2
        RES["R2"][f"{f}|{h}"] = dict(b_over_ext=list(gb / ge), b_over_capped=list(gb / gc))
        if h in ("H2", "H3"): dom &= bool(np.all((gb / ge)[1:] >= 1))
        P(f"  [{f:9s}] {h}: (b)/extended " + " / ".join(f"{v:.2f}" for v in gb / ge) + "   (b)/capped " + " / ".join(f"{v:.1f}" for v in gb / gc))
CLS_R2 = "(b) EXTERNAL >= CFG870 EXTENDED" if dom else "(b) EXTERNAL NOT >= CFG870 EXTENDED"
P(f"  R2 label: {CLS_R2}")

# ================================================================ classes
q1 = all(c["found"] for c in CIT if c["tag"] in ("i", "ii", "iii")) and S3 and S1
CLS_Q1 = "BARYONS ONLY (every record formulation)" if q1 else "NOT DETERMINED AS FROZEN (see citations/S checks)"
impl = "a" if q1 else "undetermined"
CLS_871 = "SURVIVES" if impl == "b" else "NOT DERIVED BY THE RECORD'S EQUATIONS"
CLS_877 = "SURVIVES" if impl == "b" else "NOT DERIVED"
P("\n== Classes")
P(f"  Q1 law source: {CLS_Q1}")
P(f"  Q1b clump self-gravity: class A NEWTONIAN; canonical action (ID) {'NO SELF-GRAVITY' if S1 else 'self-gravity present'} + {CLS_ID};"
  f" coupling G {'SELF-BOOST' if S2 else '?'} (not written in the record)")
P(f"  implemented branch for a clump that is not expelled: ({impl});  branch (b) CONDITIONAL on a new coupling")
P(f"  CFG871 r_c = (9/2) sigma^2/a0: {CLS_871};  CFG877 M_cl = 81 sigma^4/(4 G a0): {CLS_877};  stiffness: {CLS_ST};  {CLS_CONF};  {CLS_R2}")
RES.update(CLS_Q1=CLS_Q1, implemented=impl, CLS_871=CLS_871, CLS_877=CLS_877, CLS_ST=CLS_ST, CLS_CONF=CLS_CONF, adds_parameter=bool(addp), CLS_R2=CLS_R2)

P("\n== K-tests")
for kk, vv in K.items(): P(f"  {kk:22s} {'PASS' if vv else 'FAIL'}")
RES["K"] = K
if MUT:
    teeth = dict(M1_K1=not (K["K1_M_propto_r"] and K["K1_SIS_norm"]), M2_K2=not (K["K2_deep_limit"] and K["K2_band"]),
                 M3_S1=not K["K4_S1"], M4_K5i=not K["K5_i_law_stationary"])
    RES["teeth"] = teeth
    P("  MUTATE teeth: " + ", ".join(f"{k_} {'BITES' if v else 'DOES NOT BITE'}" for k_, v in teeth.items()))
    code = 1 if all(teeth.values()) else 0
else:
    code = 0 if all(K.values()) else 1
json.dump(RES, open(os.path.join(HERE, f"cfg888_results{SUF}.json"), "w"), indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
open(os.path.join(HERE, f"cfg888{SUF}.out"), "w").write("\n".join(OUT) + "\n")
P(f"  exit {code}")
sys.exit(code)
