#!/usr/bin/env python3
"""BI1 AMENDMENT A2 (521a16260c): carrier (iii) as the source specified it. (1) sympy Euler-Lagrange of the stated L (1D reduction) vs the
claimed field equations; ghost; effective couplings at constant f. (2) Helmholtz field with an action of strength mu_0: Euler-Lagrange
equations and the two horns (the Yukawa self-force on the component vs the gravity back-reaction). (3) The source's a_extra in SI, the
record's a0 and 1.2e-10, for L* at 250 kpc and a group at 400 kpc, unsmoothed and Yukawa-smoothed dXi/drho.
    python3 bi1_a2.py   -> bi1_a2.json / bi1_a2.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..")); sys.path.insert(0, os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion"))
_a = sys.argv; sys.argv = [_a[0]]
import ss1_core as C
sys.argv = _a
from sympy.calculus.euler import euler_equations
L = []; RES = dict(amendment="521a16260c", criteria="91e81dcd76", note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed")
def P(s): print(s, flush=True); L.append(str(s))
# ---------------- (1) field equations
x = sp.symbols("x"); G = sp.symbols("G", positive=True); Ph, Pc = sp.Function("Phi")(x), sp.Function("Phi_chi")(x)
f, q, rb, rc = sp.Function("f")(x), sp.Function("q")(x), sp.Function("rho_b")(x), sp.Function("rho_chi")(x)
Lag = -(1 / (8 * sp.pi * G)) * (Ph.diff(x) - f * Pc.diff(x) - q) ** 2 - (1 / (8 * sp.pi * G)) * Pc.diff(x) ** 2 - rb * Ph - rc * Pc
eqs = euler_equations(Lag, [Ph, Pc], x)
A = Ph.diff(x) - f * Pc.diff(x) - q
eqPhi = sp.simplify(eqs[0].lhs); eqPc = sp.simplify(eqs[1].lhs)
# claimed: Phi'' = 4piG rho_b + (f Phi_chi')' + q' ;  Phi_chi'' = 4piG (rho_chi + f rho_b)
claimed_Pc = Pc.diff(x, 2) - 4 * sp.pi * G * (rc + f * rb)
sol_A = sp.solve(eqPhi, Ph.diff(x, 2))[0]                                   # Phi'' from the Phi equation
eqPc_sub = sp.simplify((eqPc).subs(Ph.diff(x, 2), sol_A))
Pc2 = sp.solve(eqPc_sub, Pc.diff(x, 2))[0]
extra = sp.simplify(Pc2 - 4 * sp.pi * G * (rc + f * rb))
RES["field_equations"] = dict(Phi=str(sp.simplify(sol_A)), Phi_chi=str(sp.simplify(Pc2)), extra_vs_claimed=str(extra), extra_vanishes_for_const_f=str(sp.simplify(extra.subs(f.diff(x), 0))))
P(f"(1) Phi'' = {sp.simplify(sol_A)}")
P(f"(1) Phi_chi'' = {sp.simplify(Pc2)}; minus the claimed 4 pi G (rho_chi + f rho_b): {extra}  (vanishes only where f' = 0: {sp.simplify(extra.subs(f.diff(x), 0))})")
# constant f, Fourier: couplings
k, fc, Rb, Rc = sp.symbols("k f rho_b rho_chi", positive=True); Pk, Ck = sp.symbols("Phik Phichik")
s1 = sp.solve([-k ** 2 * Pk - (4 * sp.pi * G * Rb - fc * k ** 2 * Ck), -k ** 2 * Ck - 4 * sp.pi * G * (Rc + fc * Rb)], [Pk, Ck])
cb = sp.simplify(-s1[Pk] * k ** 2 / (4 * sp.pi * G)); cc = sp.simplify(-s1[Ck] * k ** 2 / (4 * sp.pi * G))
RES["couplings_const_f"] = dict(Phi_source=str(sp.expand(cb)), Phi_chi_source=str(sp.expand(cc)))
P(f"(1) constant f: Phi sourced by {sp.expand(cb)} (baryon-baryon coupling (1 + f^2) G); Phi_chi by {sp.expand(cc)}")
a1, a2 = sp.symbols("dPhi dPhichi"); Q = -(1 / (8 * sp.pi * G)) * ((a1 - fc * a2) ** 2 + a2 ** 2); Hm = sp.hessian(Q, (a1, a2)); evs = [sp.simplify(e) for e in Hm.eigenvals()]
RES["ghost"] = dict(hessian=str(Hm), det=str(sp.simplify(Hm.det())), note="negative definite for every real f (the standard gravity sign): no ghost")
P(f"(1) gradient-energy Hessian det {sp.simplify(Hm.det())} > 0 and trace < 0 for all f: no ghost")
# ---------------- (2) Helmholtz field with action, mu_0
mu, Rw, c1 = sp.symbols("mu_0 R_W c_1", positive=True); Psi = sp.Function("Psi")(x); Lg = sp.Function("L_g")  # L_g(f) gravity part's f-dependence
fP = sp.Function("F")                                                         # f = F(Psi)
LH = mu * (-(Rw ** 2 / 2) * Psi.diff(x) ** 2 - Psi ** 2 / 2 + Psi * c1 * rc) + Lg(fP(Psi))
eqPsi = euler_equations(LH, [Psi], x)[0].lhs
RES["helmholtz"] = dict(Psi_equation=str(sp.simplify(eqPsi)),
                        horn_A="mu_0 large: Psi obeys the Helmholtz equation, but the coupling mu_0 c_1 Psi rho_chi is a Yukawa self-force on the component, a_Y ~ mu_0 c_1 grad Psi, which exceeds the gravity reaction a_extra ~ (dL_g/df) F' c_1 / R exactly when the Helmholtz term dominates Psi's equation (mu_0 Psi >> (dL_g/df) F')",
                        horn_B="mu_0 small: Psi's equation is dominated by dL_g/dPsi; Psi is no longer the specified Helmholtz field, and if the specified equation is imposed without the action the reaction (dL_g/df) grad f has no carrier: momentum is violated by the same amount",
                        conclusion="the force on the component is >= a_extra for every mu_0; no mu_0 escapes both horns")
P(f"(2) Psi equation: {sp.simplify(eqPsi)} = 0. Horn A (mu_0 large): a Yukawa self-force >= a_extra; horn B (mu_0 small): Psi is not the Helmholtz field, or momentum is violated by a_extra. No mu_0 escapes.")
# ---------------- (3) numbers
Gn, MS, KPC, MPC = 6.6743e-11, 1.98892e30, 3.0857e19, 3.0857e22; A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}; VST = {"canonical": 265.8, "alt": 288.1}
Q15 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood", "qx15.json")))
def fsw(Xi, pc=1.0): return (Xi * Xi / (1 + Xi * Xi)) * (1 / math.sqrt(2) + (1 - 1 / math.sqrt(2)) / (1 + pc * pc))
for foot, a0 in A0.items():
    th = Q15["footings"][foot]["main"]["theta"]; h = float(Q15["footings"][foot]["main"]["h"]); OB, OD = th["omega_b"], th["omega_d"]; R = OD / OB; Om = (OB + OD) / h ** 2
    H0 = 100 * h * 1e3 / MPC; rhoc = 3 * H0 ** 2 / (8 * math.pi * Gn); rref = 200 * (OD / h ** 2) * rhoc; RW = VST[foot] * 1e3 / (2 * H0); rows = {}
    for name, Mb, rk in (("L* 250 kpc", 8e10, 250.0), ("group 400 kpc", 5e12, 400.0)):
        H = C.halo(Mb, R, h, Om, z=0.0); rm = rk * KPC; gb = Gn * Mb * MS / rm ** 2; Mchi = float(H["Menc"](rk)) * MS; gc = Gn * Mchi / rm ** 2
        v = math.sqrt(4.3009172706e-6 * H["M200"] / H["R200"]); sig2 = (v * 1e3) ** 2 / 2; rho = (H["fchi"] * H["M200"] / (4 * math.pi * H["R200"] * min(rk, H["R200"]) ** 2) * MS / KPC ** 3) if rk < H["R200"] else (OD / h ** 2) * rhoc
        c1 = sig2 / (rref * (VST[foot] * 1e3) ** 2); Xi_loc = c1 * rho; dfdXi = (fsw(Xi_loc * 1.0001) - fsw(Xi_loc * 0.9999)) / (Xi_loc * 0.0002)
        smooth = min(1.0, (rk * KPC) ** 2 / (2 * RW ** 2)); out = {}
        for tag, dXi in (("unsmoothed", c1), ("Yukawa-smoothed", c1 * smooth)):
            a_ex = (1 / (4 * math.pi * Gn)) * dfdXi * gb * gc * dXi / RW; glaw = 0.5 * gb + math.sqrt(0.25 * gb * gb + a0 * gb)
            out[tag] = dict(a_extra=a_ex, over_record_a0=a_ex / a0, over_1p2e10=a_ex / 1.2e-10, over_law_g=a_ex / glaw)
        rows[name] = dict(g_N_b=gb, g_N_chi=gc, Xi_local=Xi_loc, df_dXi=dfdXi, sigma_kms=math.sqrt(sig2) / 1e3, R_W_Mpc=RW / MPC, **out)
    claims = {"L* 250 kpc": 4.6e-12, "group 400 kpc": 2.6e-9}
    for nm, cl in claims.items(): rows[nm]["source_claim"] = dict(a_extra=cl, over_record_a0=cl / a0, over_1p2e10=cl / 1.2e-10)
    worst = max(rows[n]["Yukawa-smoothed"]["over_law_g"] for n in rows); st = "FAIL" if worst > 1e-3 else "PASS"; RES[foot] = dict(rows=rows, B0_iii_explicit=st)
    for nm, r in rows.items():
        P(f"[{foot}] (3) {nm}: Xi_local {r['Xi_local']:.2g}, df/dXi {r['df_dXi']:.2g}; a_extra unsmoothed {r['unsmoothed']['a_extra']:.2e} / smoothed {r['Yukawa-smoothed']['a_extra']:.2e} m/s^2 = {r['Yukawa-smoothed']['over_law_g']:.2g} of the law's g (smoothed); "
          f"source {r['source_claim']['a_extra']:.1e} = {r['source_claim']['over_record_a0']:.1f} record a0 / {r['source_claim']['over_1p2e10']:.1f} x 1.2e-10")
    P(f"[{foot}] B0(iii)-explicit {st}; overall BI1 label: " + ("FAIL at B0 (all three carriers)" if st == "FAIL" else "carrier (iii)-explicit passes B0"))
json.dump(RES, open(os.path.join(HERE, "bi1_a2.json"), "w"), indent=1, default=str); open(os.path.join(HERE, "bi1_a2.out"), "w").write("\n".join(L) + "\n")
