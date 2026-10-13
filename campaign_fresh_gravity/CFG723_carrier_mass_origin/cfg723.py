#!/usr/bin/env python3
"""CFG723: the carrier's mass is not what we think? Criteria: FROZEN_CRITERIA.md (e9238960c).
Run:  nice -n 10 python3 cfg723.py        (CFG723_MUTATE=1 -> _MUTATE outputs; exit 0 iff every tooth bites)
Analytic + sympy; one process; no downloads. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, sys
import numpy as np
import sympy as sp

MUT = os.environ.get("CFG723_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

# ---- constants (SI) ----
G, c, hbar, eV = 6.674e-11, 2.99792458e8, 1.054571817e-34, 1.602176634e-19
Msun, pc, Gyr = 1.98892e30, 3.0857e16, 3.15576e16
KAPPA = 0.5
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
OM_B, OM_DE, RATIO = 0.0493, 0.686, 5.364
ZREC1 = 1100.0
SIG_X = (0.1, 0.3)            # g cm^-2, Bullet crossing column, PROVISIONAL
T_AGE = 13.8 * Gyr            # declared
V_MERGE = 4.7e6               # m/s, PROVISIONAL
MASSES = [1e9, 1e10, 1e11, 1e12]
res = {"criteria": "e9238960c", "mutate": MUT}

def nu_s(y): return 0.5 + np.sqrt(0.25 + 1.0 / y)
def law(Mb, r, a0):
    gN = G * Mb / r**2; y = gN / a0; g = nu_s(y) * gN
    dnudy = -0.5 / y**2 / np.sqrt(0.25 + 1.0 / y)
    rho_ph = Mb / (4 * np.pi * r**2) * dnudy * (-2 * y / r)
    u = a0 * g / (a0 + g)
    return gN, g, rho_ph, u
def W(u, a0): return (a0 / (4 * np.pi * G)) * (-u - a0 * np.log(1 - u / a0))
def rho_DE(a0): return a0**2 / (KAPPA**2 * c**2 * G)

checks = {}
# ===================== K1 control =====================
P("=== K1: phantom density integrates to M_b (nu_s - 1)")
k1 = []
for fk, a0 in A0.items():
    for Mb in MASSES:
        M = Mb * Msun; rM = np.sqrt(G * M / a0)
        r = np.geomspace(0.01 * rM, 10 * rM, 200001)
        _, _, rho, _ = law(M, r, a0)
        integ = np.sum(0.5 * (rho[1:] * r[1:]**2 + rho[:-1] * r[:-1]**2) * np.diff(r)) * 4 * np.pi
        exact = M * (nu_s(G * M / r[-1]**2 / a0) - nu_s(G * M / r[0]**2 / a0))
        k1.append(abs(integ / exact - 1))
checks["K1"] = max(k1) <= 1e-6
P(f"  max rel err {max(k1):.2e} -> {'PASS' if checks['K1'] else 'FAIL'}")

# ===================== (A) field energy =====================
P("\n=== (A) P field energy as the mass")
A = {}
for fk, a0 in A0.items():
    rows = []
    for Mb in MASSES + ["cluster"]:
        if Mb == "cluster":
            M = 1e14 * Msun; rs = [1e6 * pc]; lab = "1e14@1Mpc"
        else:
            M = Mb * Msun; rM = np.sqrt(G * M / a0); rs = [0.1 * rM, rM, 10 * rM]; lab = f"{Mb:.0e}"
        for r in rs:
            gN, g, rho, u = law(M, r, a0)
            fac = (c / (G * M * a0) ** 0.25) ** 2 if MUT else 1.0   # M1
            A1 = fac * W(u, a0) / (rho * c**2)
            rr = np.geomspace(1e-4 * r, r, 20001)
            gN2, g2, rho2, u2 = law(M, rr, a0)
            e = fac * (W(u2, a0) + g2**2 / (8 * np.pi * G))
            Ef = np.sum(0.5 * (e[1:] * rr[1:]**2 + e[:-1] * rr[:-1]**2) * np.diff(rr)) * 4 * np.pi
            Mph = M * (nu_s(G * M / r**2 / a0) - 1)
            A2 = Ef / (Mph * c**2)    # as frozen: point-mass g^2/8piG diverges as 1/r_in (baryon self-energy; disclosed)
            e2 = fac * (W(u2, a0) + (g2**2 - gN2**2) / (8 * np.pi * G))   # A2': P energy + phantom-attributable field energy
            Ef2 = np.sum(0.5 * (e2[1:] * rr[1:]**2 + e2[:-1] * rr[:-1]**2) * np.diff(rr)) * 4 * np.pi
            A2p = Ef2 / (Mph * c**2)
            rows.append({"M": lab, "r_pc": r / pc, "A1": A1, "A2": A2, "A2p": A2p, "rho_ph_over_rhoDE": rho / rho_DE(a0)})
    emax = W(a0 / 2, a0)
    A3 = {z1: emax / (RATIO * OM_B / OM_DE * rho_DE(a0) * c**2 * z1**3) for z1 in (1.0, ZREC1)}
    A[fk] = {"rows": rows, "A3": A3}
    P(f"  [{fk}] rho_DE = {rho_DE(a0):.3e} kg/m^3;  e_max/rho_DE c^2 = {emax/(rho_DE(a0)*c**2):.3e}")
    for rw in rows:
        P(f"    M {rw['M']:>9}  r {rw['r_pc']:10.3e} pc  rho_ph/rho_DE {rw['rho_ph_over_rhoDE']:9.3e}  "
          f"A1 {rw['A1']:9.2e}  A2(frozen, r_in 1e-4 r) {rw['A2']:9.2e}  A2' {rw['A2p']:9.2e}")
    P(f"    A3 cosmic e_max/(rho_c,req c^2): z=0 {A3[1.0]:.2e}; 1+z=1100 {A3[ZREC1]:.2e}")
# A4: equation of state of static field energy (sympy)
x, y_, z_ = sp.symbols("x y z"); phi = sp.Function("phi")(x, y_, z_)
gr = [sp.diff(phi, v) for v in (x, y_, z_)]; rho_g = sum(gi**2 for gi in gr) / 2
Tij_tr = sum(gr[i] * gr[i] - rho_g for i in range(3))
w_grad = sp.simplify((Tij_tr / 3) / rho_g)
P(f"  A4: static gradient energy mean w = {w_grad}; potential energy W: w = -1 (p = -W). Not pressureless.")
res["A"] = A; res["A4_w_gradient"] = str(w_grad)
A1max = max(rw["A1"] for fk in A for rw in A[fk]["rows"])
A2max = max(rw["A2"] for fk in A for rw in A[fk]["rows"])
A2pmax = max(rw["A2p"] for fk in A for rw in A[fk]["rows"])
A3rec = max(A[fk]["A3"][ZREC1] for fk in A)

# ===================== (B) condensate =====================
P("\n=== (B) condensate / superfluid medium, P as displacement")
t = sp.symbols("t"); X = sp.symbols("X")
rho_f = sp.Function("rho")(X, t); v_f = sp.Function("v")(X, t)
# P defined by dP/dt = -j, j = rho v; continuity d_t rho + d_x j = 0 => d_t(d_x P - (rho - rhobar)) = 0
Pf = sp.Function("Pf")(X, t)
expr = sp.diff(sp.diff(Pf, X), t) - sp.diff(rho_f, t)
expr = expr.subs(sp.diff(sp.diff(Pf, X), t), -sp.diff(rho_f * v_f, X))
expr = expr.subs(sp.diff(rho_f, t), -sp.diff(rho_f * v_f, X))
B0_sym = sp.simplify(expr) == 0
# numerical 1-D check
rng = np.random.default_rng(723); N = 512; Lx = 1.0; xs = np.arange(N) * Lx / N; dx = Lx / N
rho = 1 + 0.3 * np.sin(2 * np.pi * xs) ; Pn = np.zeros(N); rhobar = rho.mean()
modes = rng.normal(size=4)
def vel(tt): return sum(modes[k] * np.sin(2 * np.pi * (k + 1) * xs + tt) for k in range(4)) * 0.05
def ddx(f): return (np.fft.ifft(1j * 2 * np.pi * np.fft.fftfreq(N, dx) * np.fft.fft(f))).real
def antideriv(f):
    F = np.fft.fft(f - f.mean()); k = 2 * np.pi * np.fft.fftfreq(N, dx); k[0] = 1.0
    out = np.fft.ifft(F / (1j * k)); out[0] = out[0]; return out.real
Pn = antideriv(rho - rhobar)
dt = 1e-4
for i in range(2000):
    def rhs(r_, P_, tt):
        j = r_ * vel(tt); return -ddx(j), -j
    k1r, k1p = rhs(rho, Pn, i * dt); k2r, k2p = rhs(rho + 0.5 * dt * k1r, Pn + 0.5 * dt * k1p, (i + .5) * dt)
    k3r, k3p = rhs(rho + 0.5 * dt * k2r, Pn + 0.5 * dt * k2p, (i + .5) * dt); k4r, k4p = rhs(rho + dt * k3r, Pn + dt * k3p, (i + 1) * dt)
    rho = rho + dt / 6 * (k1r + 2 * k2r + 2 * k3r + k4r); Pn = Pn + dt / 6 * (k1p + 2 * k2p + 2 * k3p + k4p)
B0_num = float(np.max(np.abs(ddx(Pn) - (rho - rhobar))))
checks["K2"] = B0_sym and B0_num < 1e-9
P(f"  B0: div P = rho - rhobar under dP/dt = -j: sympy {B0_sym}; 1-D numeric max err {B0_num:.1e} -> "
  f"{'PASS' if checks['K2'] else 'FAIL'} (CFG722's ID identification = kinematic identity of a medium)")
B = {}
for fk, a0 in A0.items():
    rows = []
    for Mb in MASSES:
        M = Mb * Msun; rM = np.sqrt(G * M / a0); _, _, rho_ph, _ = law(M, rM, a0)
        Vf = (G * M * a0) ** 0.25
        mdeg = (rho_ph * (2 * np.pi * hbar) ** 3 / Vf**3) ** 0.25 * c**2 / eV
        rho_cgs = rho_ph * 1e-3; v_cgs = Vf * 100
        smin = 1.0 / (rho_cgs * v_cgs * T_AGE)
        rows.append({"Mb": Mb, "rM_kpc": rM / pc / 1e3, "Vf_kms": Vf / 1e3, "rho_ph": rho_ph,
                     "m_deg_eV": mdeg, "sigma_over_m_min": smin})
        P(f"  [{fk}] M_b {Mb:.0e}: r_M {rM/pc/1e3:6.2f} kpc, V_f {Vf/1e3:6.1f} km/s, rho_ph {rho_ph:.2e} kg/m^3 -> "
          f"m <= {mdeg:.2f} eV (degenerate); thermalise needs sigma/m >= {smin:.2f} cm^2/g")
    B[fk] = rows
smax = [1 / s for s in SIG_X]
smin_all = max(r["sigma_over_m_min"] for fk in B for r in B[fk])
smin_lo = min(r["sigma_over_m_min"] for fk in B for r in B[fk])
window = smin_all < min(smax)
P(f"  B3 Bullet tau<1: sigma/m <= {min(smax):.1f}-{max(smax):.1f} cm^2/g (Sigma_x {SIG_X} PROVISIONAL)")
P(f"  B4 window: needs {smin_lo:.2f}-{smin_all:.2f} (all masses) <= sigma/m <= {min(smax):.1f}: "
      f"{'OPEN' if window else 'CLOSED at the most demanding mass'}")
cs_coh = (0.134, 3.71)   # m/s, astra microscopic_carrier contact-pressure speeds (0.62 eV, sigma/m = 1)
P(f"  B5 Landau: coherent sound speed {cs_coh[0]}-{cs_coh[1]} m/s vs merger {V_MERGE/1e3:.0f} km/s -> ratio "
  f"{V_MERGE/cs_coh[1]:.1e}: superfluidity broken in the collision; passes only as a dilute gas with tau < 1")
P("  B6: rho = m n with quanta of mass m (mass shell) -> PARTICLE IN DISGUISE")
mdeg_rng = (min(r["m_deg_eV"] for fk in B for r in B[fk]), max(r["m_deg_eV"] for fk in B for r in B[fk]))
res["B"] = {"rows": B, "B0_sym": bool(B0_sym), "B0_num": B0_num, "sigma_max": smax, "window_open": bool(window),
            "m_deg_range_eV": mdeg_rng, "landau_ratio": V_MERGE / cs_coh[1]}

# ===================== (C) vacuum-displaced =====================
P("\n=== (C) vacuum-displaced energy")
rc0 = RATIO * OM_B / OM_DE
C1 = rc0 * ZREC1**3
C2 = 0.02 / rc0
rhoV, pV = sp.symbols("rho_V p_V")
w_vac = 0 if MUT else -1          # M2
inertia = sp.simplify(rhoV + w_vac * rhoV)
C4 = {v: (c / (v * 1e3))**2 for v in (200, 1000)}   # eta with F = 1
P(f"  C1: rho_c,req(1+z=1100)/rho_DE0 = {C1:.3e}  (rho_c,req(0)/rho_DE0 = {rc0:.4f})")
P(f"  C2: late conversion allowed by a0 flat (<1% => rho_DE <2%, z<=5): {C2:.3f} of today's cold mass")
P(f"  C3: vacuum inertial density (rho+p)/c^2 = {inertia}{'  [MUTATE w=0]' if MUT else ''}")
P(f"  C4: deposit one rest mass locally needs eta = (c/v)^2: v=200 km/s {C4[200]:.2e}, 1000 km/s {C4[1000]:.2e} "
  f"-> reaction force / halo gravity = eta ~ 1e5-1e6")
res["C"] = {"C1": C1, "rc0": rc0, "C2": C2, "C3": str(inertia), "C4_eta": C4}

# ===================== (D) other =====================
P("\n=== (D) other non-particle origins")
D2 = {}
mthr = 2e-20 * eV / c**2
def jeans_kpc(m_kg, rho):
    kJ = (16 * np.pi * G * rho * m_kg**2 / hbar**2) ** 0.25; return 2 * np.pi / kJ / pc / 1e3
for fk, a0 in A0.items():
    rhoc = rc0 * rho_DE(a0)
    for lab, tg in (("c_P=c", 2e-5), ("L*5.75pc", 5e-5), ("100pc", 6e-3), ("1000pc lo", 0.06), ("1000pc hi", 0.28)):
        E = hbar * 2 * np.pi / (tg * Gyr) / eV
        D2[f"{fk}:{lab}"] = {"t_Gyr": tg, "hbar_omega_eV": E, "jeans_kpc": jeans_kpc(E * eV / c**2, rhoc)}
    D2[f"{fk}:threshold_2e-20eV"] = {"jeans_kpc": jeans_kpc(mthr, rhoc)}
for k, v in D2.items():
    P(f"  D2 {k:24s} " + (f"hbar w0 {v['hbar_omega_eV']:.2e} eV  " if 'hbar_omega_eV' in v else " " * 27)
      + f"Jeans (cosmic mean cold density) {v['jeans_kpc']:.2e} kpc")
D3 = {Mb: ((G * Mb * Msun * A0['canonical']) ** 0.25 / c) ** 2 for Mb in MASSES + [1e14]}
P("  D3 binding energy / rest mass ~ (V_f/c)^2: " + ", ".join(f"{m:.0e}: {v:.1e}" for m, v in D3.items()))
res["D"] = {"D2": D2, "D3": D3}

# ===================== general statement =====================
p_, m_ = sp.symbols("p m", positive=True)
E_ = sp.sqrt(p_**2 * c**2 + m_**2 * c**4); vg = sp.diff(E_, p_)
m_use = 0 if MUT else m_
vg_m = sp.simplify(vg.subs(m_, m_use))
cold_ok = sp.limit(vg_m, p_, 0) == 0
P(f"\n=== mass shell: group velocity v(p->0) = {sp.limit(vg_m, p_, 0)} (m {'= 0 MUTATE' if MUT else '> 0'}) -> "
  f"cold possible: {cold_ok}. With m = 0, |v| = c for every p: a collisionless kinetic carrier is cold only on a massive shell.")
res["mass_shell_cold_possible"] = bool(cold_ok)

# ===================== channels (sizes) =====================
P("\n=== detection channels (sizes)")
for gname, gv in (("Earth surface", 9.81), ("Earth orbit (Sun)", 5.93e-3), ("Saturn orbit", 6.5e-5)):
    P(f"  unscreened law: delta g / g ~ a0/g_N at {gname}: {A0['canonical']/gv:.1e} (absolute a0 ~ 1e-10 m/s^2;"
      f" the record screens below L* = 5.75 pc, CFG691)")
for tg in (0.06, 0.28):
    P(f"  merger lag d = v t_resp at {V_MERGE/1e3:.0f} km/s, t = {tg} Gyr: {V_MERGE*tg*Gyr/pc/1e3:.0f} kpc (CFG722 B3 slow corner)")

res["checks"] = checks
# ===================== verdicts =====================
Emax_D2 = max(v.get("hbar_omega_eV", 0) for v in D2.values())
verd = {
 "A": ("FAILS (R1: cosmic %.1e at 1+z=1100; R3: A1 <= %.1e, A2' <= %.1e; R4/R5: w in [-1, -1/3], not dust)" % (A3rec, A1max, A2pmax))
      if (A3rec < 0.5 and A1max < 0.5 and A2pmax < 0.5) else "NOT FAILED on R1/R3 (inspect)",
 "B": ("VIABLE-AS-PARTICLE-IN-DISGUISE (sigma/m window open; m <= %.0f-%.0f eV for degeneracy; needs non-thermal cold production)" % mdeg_rng)
      if window else "VIABLE-AS-PARTICLE-IN-DISGUISE only as a plain collisionless gas (no condensate window)",
 "C": "FAILS (R1 late / R2 inertia / R5-local reaction); early conversion = particle-in-disguise + 1 constant",
 "D1": "FAILS (R2: CFG624 G3, CFG722 B2)", "D2": ("FAILS (R4: hbar w0 <= %.1e eV vs 2e-20 eV) + amplitude free" % Emax_D2) if Emax_D2 < 2e-20 else "passes R4 (inspect)",
 "D3": "FAILS (R1)", "D4": "FAILS (R2: single-valued flow, CFG288/L374)", "D5": "VIABLE-AS-PARTICLE-IN-DISGUISE (mass induced, still a mass shell)"}
res["verdicts"] = verd
P("\n=== verdicts"); [P(f"  {k}: {v}") for k, v in verd.items()]

if MUT:
    bites = {"M1": A1max > 0.1, "M2": str(inertia) != "0", "M3": not cold_ok}
    res["mutate_bites"] = bites
    P(f"\nMUTATE bites: {bites}  (M1 A1max {A1max:.2e})")
    rc = 0 if all(bites.values()) else 1
else:
    res["summary"] = {"A1max": A1max, "A2max_frozen": A2max, "A2pmax": A2pmax, "A3_rec": A3rec}
    rc = 0 if all(checks.values()) else 1
with open(os.path.join(HERE, f"cfg723{SUF}.out"), "w") as f: f.write("\n".join(OUT) + "\n")
with open(os.path.join(HERE, f"cfg723_results{SUF}.json"), "w") as f: json.dump(res, f, indent=1, default=str)
sys.exit(rc)
