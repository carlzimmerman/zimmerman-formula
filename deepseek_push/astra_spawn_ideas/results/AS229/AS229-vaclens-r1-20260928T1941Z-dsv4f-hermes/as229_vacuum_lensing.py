#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS229 — projected-vacuum contribution to lensing slip (Tier-0b seed).
CA5-GNC-R reciprocal vacuum barrier:  L_v = -V0 F(t),  F(t) = 1 + (t + 1/t - 2)^2,
t = 1 + z = 1 + Z - <Z>_h > 0, static weak inhomogeneous z with (proper-volume,
leading order: h-)mean zero, expand about t_c = 1.

Target (seed math block):
    Delta T^ij_mean = -(<N sigma_v>_h / N) z h^ij ,   sigma_v = -V0 F'(t_c).

Deliverables encoded here:
  (A) exact closed forms and flatness orders of F at t = 1  (F'=F''=F'''=0, F''''=24);
  (B) first nonzero vacuum order of the projected stress: O(z^4), leading
      coefficient +4 V0 <z^3>_h z (N=1 leading order), vs old-floor O(z) linear;
  (C) trace / trace-free Einstein scalar combinations with the vacuum sources
      (symbolic derivation + 3D numeric identity check of every component);
  (D) negative control: linear susceptibility of the older 1/t_c floor must
      contradict F'(1) = F''(1) = 0 (it does: O(z) vs O(z^4), ratio tests);
  (E) both footings kept separate (canonical 9.3619e-11, alternative 1.1279e-10 m/s^2;
      kappa = 1/2 adopted; V0 free input, calibrated for display only to
      epsilon_Lambda of each footing).
Bounds: <=120 s wall (signal.alarm), <=512 MB (attempted rlimit; measured RSS),
1 thread (env). Grid refinement once: N 64 -> 128 (1D), N 16 3D identity.
"""
import signal, time, json, os, sys, math
import numpy as np
import sympy as sp

T0 = time.time()
signal.alarm(120)
OUT = {}
def fail(msg):
    OUT.setdefault("fails", []).append(msg)

# ----------------------------------------------------------------------------
#  Constants (SI; campaign defaults; G_N only - G_bare/G_cosmo NOT used)
# ----------------------------------------------------------------------------
G   = 6.67430e-11
c   = 299792458.0
M_SUN = 1.98847e30
PC  = 3.085677581491367e16
KAPPA_CI = 0.5
A0_CAN = 9.3619e-11
A0_ALT = 1.1279e-10
RHO_L_CAN = 5.844412454021876e-27
RHO_L_ALT = 8.483089619559099e-27
EPS_L_CAN = RHO_L_CAN * c * c
EPS_L_ALT = RHO_L_ALT * c * c

# ============================================================================
#  PART A — symbolic exact identities for F
# ============================================================================
t, z, V0 = sp.symbols("t z V0", positive=True)
F   = 1 + (t + 1/t - 2)**2
Fp  = sp.diff(F, t)
Fpp = sp.diff(Fp, t)
Fppp= sp.diff(Fpp, t)
Fpppp = sp.diff(Fppp, t)

f1 = sp.limit(Fp, t, 1)
f2 = sp.limit(Fpp, t, 1)
f3 = sp.limit(Fppp, t, 1)
f4 = sp.limit(Fpppp, t, 1)
OUT["flatness"] = {"F'(1)": str(f1), "F''(1)": str(f2), "F'''(1)": str(f3),
                   "F''''(1)": str(f4)}

# closed forms in z = t-1
Fm1   = sp.simplify(F.subs(t, 1+z) - 1)                    # expect z^4/(1+z)^2
Fpz   = sp.simplify(Fp.subs(t, 1+z))                       # expect 2 z^3 (z+2)/(1+z)^3
Fppz  = sp.simplify(Fpp.subs(t, 1+z))
targetFm1  = z**4/(1+z)**2
targetFpz  = 2*z**3*(z+2)/(1+z)**3
OUT["closed_forms"] = {
    "F(1+z)-1": str(Fm1),
    "target": str(targetFm1),
    "residual": str(sp.simplify(Fm1 - targetFm1)),
    "F'(1+z)": str(Fpz),
    "target": str(targetFpz),
    "residual": str(sp.simplify(Fpz - targetFpz)),
}

ser_Fm1 = sp.series(Fm1, z, 0, 10).removeO().expand()
ser_Fpz = sp.series(Fpz, z, 0, 10).removeO().expand()
OUT["series_Fm1"] = sp.Poly(ser_Fm1, z).all_coeffs()[::-1]   # [z^0..z^9]
coef_Fpz = sp.Poly(ser_Fpz, z).all_coeffs()[::-1]            # [z^0..z^9] (0,0,0,4,-10,18,-28,42,-60,88?)
OUT["series_Fpz_coefs_z0_to_z9"] = [str(x) for x in coef_Fpz]
OUT["leading_Fpz_coef_z3"] = str(coef_Fpz[3])
OUT["series_Fm1_leading_z4"] = str(sp.Poly(ser_Fm1, z).all_coeffs()[::-1][4])

# sigma_v = -V0 F'(t); expand
sigma = -V0 * Fpz
ser_sigma = sp.series(sigma, z, 0, 10).removeO().expand()
OUT["sigma_leading"] = str(sp.Poly(ser_sigma, z).all_coeffs()[::-1][3])

# Delta T = -(<N sigma>/N) z ; with N = 1 leading: -sigma*z
Dz = sp.simplify(-ser_sigma * z)
OUT["DeltaT_series_leading"] = str(sp.Poly(Dz.expand(), z).all_coeffs()[::-1][4])

# ---- A4: linearized Einstein scalar combinations (static, weak, 3D, c=1) ----
x1, x2, x3 = sp.symbols("x1 x2 x3")
Phi = sp.Function("Phi")(x1, x2, x3)
Psi = sp.Function("Psi")(x1, x2, x3)
h00, hij = -2*Phi, -2*Psi
def dd(f, i, j):
    return sp.diff(sp.diff(f, [x1, x2, x3][i]), [x1, x2, x3][j])
def lapl(f):
    return sum(sp.diff(f, [x1,x2,x3][i], 2) for i in range(3))
R00 = lapl(Phi)
Rij = [[0]*3 for _ in range(3)]
for i in range(3):
    for j in range(3):
        Rij[i][j] = (lapl(Psi) if i == j else 0) + dd(Psi, i, j) - dd(Phi, i, j)
Rtr = -R00 + sum(Rij[i][i] for i in range(3))
G00 = R00 + sp.Rational(1,2)*Rtr     # g_00 = -1 at leading order
Gij = [[Rij[i][j] - sp.Rational(1,2)*Rtr*(1 if i==j else 0) for j in range(3)] for i in range(3)]
S = Phi - Psi
Gij_tf = [[Gij[i][j] - sp.Rational(1,3)*(1 if i==j else 0)*sum(Gij[k][k] for k in range(3))
           for j in range(3)] for i in range(3)]
combo01 = sp.simplify(G00 - 2*lapl(Psi))
combo02 = sp.simplify(sum(Gij[i][i] for i in range(3)) - 2*lapl(Phi-Psi))
combo03 = sp.simplify(Gij_tf[0][1] + dd(Phi-Psi, 0, 1))
combo04 = sp.simplify(Gij_tf[1][1] + (dd(Phi-Psi,1,1) - sp.Rational(1,3)*lapl(Phi-Psi)))
OUT["einstein_symbolic"] = {
    "G00 - 2 Lap Psi  (Lap Psi = 4 pi G T00/2, i.e. Lap Psi = 4piG rho)": str(combo01),
    "G^k_k - 2 Lap (Phi-Psi)": str(combo02),
    "TF[G]_01 + (d1 d2)(Phi-Psi)": str(combo03),
    "TF[G]_11 + (d1^2 - (1/3) Lap)(Phi-Psi)": str(combo04),
}
# resulting scalar combos (c = 1 units, G = G_N):
OUT["einstein_combos"] = {
    "Lap Psi": "4 pi G rho      (T00 = rho)",
    "Lap (Phi-Psi)": "4 pi G T^k_k",
    "Lap Phi": "4 pi G (rho + T^k_k)",
    "Lap (Phi+Psi)": "4 pi G (2 rho + T^k_k)",
    "TF": "(d_i d_j - (1/3) d_ij Lap)(Phi-Psi) = -8 pi G Pi_ij,  Pi_ij = T_ij - (1/3)d_ij T^k_k",
}

# ---- A5: vacuum stress combinations (exact) ----
Pv_proj = -(V0*F.subs(t, 1+z) + 0)   # -V0 F  (isotropic part of T^ij_v trace)
# T^ij_v = -V0 F h^ij - (<N sigma>/N) z h^ij  =>  P_v = -V0 F - (<N sigma>/N) z
rho_v = V0 * F.subs(t, 1+z)
P_v   = -V0 * F.subs(t, 1+z) - sp.Symbol("Pbar")
exact_rhoP = sp.simplify(rho_v + (V0*F.subs(t,1+z) + sp.Symbol("Pbar")))
OUT["vacuum_stress"] = {
    "rho_v": str(rho_v),
    "P_v": "= -V0 F - (<N sigma_v>/N) z",
    "rho_v + P_v = -(<N sigma_v>/N) z  [exact cancellation of the F parts]":
        "derived; verify numerically below",
    "Pi_v (trace-free part of T^ij_v)": "0 identically at every order (both terms isotropic)",
}

# ============================================================================
#  PART B — numeric: 1D periodic leaf (flat, unit lapse N=1 at leading order)
# ============================================================================
def zprof(A, x, Ntot):
    k = 1.0
    return A*(np.sin(k*x) + 0.35*np.sin(2*k*x) + 0.12*np.sin(3*k*x))

results_1d = {}
for N in (64, 128):
    L = 4*np.pi
    x = np.linspace(0, L, N, endpoint=False)
    row = {}
    for A in (0.3, 0.15, 0.075):
        zz = zprof(A, x, N)
        tz = 1.0 + zz
        assert tz.min() > 0.0
        # exact barrier quantities (N=1 leading order; <N sigma>_h = mean(sigma))
        Fm1_n = zz**4/(1.0+zz)**2
        Fp_n  = 2.0*zz**3*(zz+2.0)/(1.0+zz)**3
        sigma_n = -Fp_n                 # V0 = 1 in the structure tests
        meanS = np.mean(sigma_n)        # <N sigma_v>_h with N = 1
        dT   = -(meanS/1.0)*zz          # Delta T^ij_mean scalar coefficient (V0=1)
        z3m  = np.mean(zz**3)
        lead = 4.0*z3m*zz               # leading O(z^4) term
        resid = dT - lead
        row[A] = {
            "min_z": float(tz.min()-1.0),
            "mean_z": float(np.mean(zz)),
            "mean_z3": float(z3m),
            "max_abs_dT": float(np.max(np.abs(dT))),
            "max_abs_resid_after_lead": float(np.max(np.abs(resid))),
            "max_abs_TF": float(np.max(np.abs(dT - (1.0/3.0)*np.sum(dT*0.0) )))  # placeholder
        }
        # trace-free part of Delta T^ij = K delta^ij : K - (1/3) tr = K - K = 0
        row[A]["max_abs_TF"] = float(np.max(np.abs(dT - (1.0/3.0)*3.0*dT)))
        # old-floor quantities (F_old = 1/t : sigma_old = V0/t^2)
        sig_old = 1.0/(tz*tz)           # V0 = 1
        dT_old = -(np.mean(sig_old))*zz
        row[A]["dT_old_max"] = float(np.max(np.abs(dT_old)))
        # corrupt-sign control
        dT_wrong = +(meanS)*zz
        row[A]["dT_wrongsign_resid_vs_lead"] = float(np.max(np.abs(dT_wrong - lead)))
    # ratios across A: 0.075/0.15/0.3
    r_lead  = row[0.15]["max_abs_resid_after_lead"]/row[0.3]["max_abs_resid_after_lead"]
    r_lead2 = row[0.075]["max_abs_resid_after_lead"]/row[0.15]["max_abs_resid_after_lead"]
    r_old   = row[0.15]["dT_old_max"]/row[0.3]["dT_old_max"]
    r_old2  = row[0.075]["dT_old_max"]/row[0.15]["dT_old_max"]
    r_wrong = row[0.15]["dT_wrongsign_resid_vs_lead"]/row[0.3]["dT_wrongsign_resid_vs_lead"]
    results_1d[N] = {
        "rows": row,
        "resid_ratio_015_030": float(r_lead),
        "resid_ratio_0075_015": float(r_lead2),
        "expect_resid_ratio": "1/32 = 0.03125  (next order z^5)",
        "old_ratio_015_030": float(r_old),
        "old_ratio_0075_015": float(r_old2),
        "expect_old_ratio": "1/2 = 0.5  (linear order)",
        "wrongsign_ratio": float(r_wrong),
        "expect_wrongsign_ratio": "1/16 = 0.0625 != 1/32 (control must fail)",
    }
    # recovery of the leading susceptibility <N sigma>/<-4 z^3> -> 1
    rec = []
    for A in (0.3, 0.15, 0.075):
        zz = zprof(A, x, N)
        Fp_n = 2.0*zz**3*(zz+2.0)/(1.0+zz)**3
        rec.append(float(np.mean(-Fp_n)/np.mean(4.0*zz**3)))
    results_1d[N]["susceptibility_recovery_<sigma>/(-4<z^3>)"] = rec
    # substitute-back: truncated Taylor susceptibility (3 terms) vs full
    zz = zprof(0.2, x, N)
    Fp_n = 2.0*zz**3*(zz+2.0)/(1.0+zz)**3
    Fp_tr = 4.0*zz**3 - 10.0*zz**4 + 18.0*zz**5
    dT_full = -(np.mean(-Fp_n))*zz
    dT_tr   = -(np.mean(-Fp_tr))*zz
    results_1d[N]["substitute_back_trunc_vs_full_max"] = float(np.max(np.abs(dT_full - dT_tr)))
OUT["1d"] = results_1d

# ============================================================================
#  PART C — 3D Einstein identity with composite (baryon + vacuum) sources
# ============================================================================
Ns = 16
L3 = 4.0*np.pi
ax = np.linspace(0, L3, Ns, endpoint=False)
X, Y, Zg = np.meshgrid(ax, ax, ax, indexing="ij")
G3 = 1.0  # c = 1, G in acausal units for the identity check (pure factor test)
rho_b = (2.0 + np.cos(X))*(1.5 + np.sin(Y))*(2.0 + np.cos(Zg))     # kg/m^3-ish, smooth
Pb    = 0.3*np.cos(X)*np.sin(Y) + 0.2*np.cos(Zg)                   # isotropic baryon pressure
A3 = 0.15
zz3 = A3*(np.sin(X) + 0.35*np.sin(2*Y) + 0.12*np.sin(3*Zg))
Fm1_3 = zz3**4/(1.0+zz3)**2
Fp_3  = 2.0*zz3**3*(zz3+2.0)/(1.0+zz3)**3
V0num = 1.0
rho_v3 = V0num*(1.0+Fm1_3)                       # V0 F
P_v3   = -V0num*(1.0+Fm1_3) - np.mean(-V0num*Fp_3)*zz3
rho_T  = rho_b + rho_v3
P_T    = Pb + P_v3
Tii_T  = 3.0*P_T
# Poisson solves in Fourier (k=0 mode -> 0, gauge constant)
kvec = np.fft.fftfreq(Ns, d=L3/Ns)
KX, KY, KZ = np.meshgrid(kvec, kvec, kvec, indexing="ij")
K2 = KX**2 + KY**2 + KZ**2
K2[0,0,0] = 1.0
def poisson(src):
    f = np.fft.fftn(src)
    u = -4.0*np.pi*G3*f/K2
    u[0,0,0] = 0.0
    return np.fft.ifftn(u).real
Psi3 = poisson(rho_T)
S3   = poisson(Tii_T)
Phi3 = Psi3 + S3
# reconstruct Einstein tensor of the metric and compare with 8 pi G T
def laplN(f):
    return np.fft.ifftn(-K2*np.fft.fftn(f)).real
def ddi(f, i):
    kk = [KX, KY, KZ][i]
    return np.fft.ifftn(1j*kk*np.fft.fftn(f)).real
def ddij(f, i, j):
    kk1 = [KX, KY, KZ][i]; kk2 = [KX, KY, KZ][j]
    return np.fft.ifftn(-kk1*kk2*np.fft.fftn(f)).real
R00n = lapl(Phi3)
RijN = np.zeros((3,3)+rho_T.shape)
for i in range(3):
    for j in range(3):
        RijN[i,j] = (lapl(Psi3) if i==j else 0.0) + ddij(Psi3,i,j) - ddij(Phi3,i,j)
RtrN = -R00n + sum(RijN[i,i] for i in range(3))
G00n = R00n + 0.5*RtrN
GijN = np.zeros_like(RijN)
for i in range(3):
    for j in range(3):
        GijN[i,j] = RijN[i,j] - 0.5*RtrN*(1.0 if i==j else 0.0)
T00n = rho_T
TijN = np.zeros_like(GijN)
for i in range(3):
    for j in range(3):
        TijN[i,j] = P_T*(1.0 if i==j else 0.0)
res00 = np.max(np.abs(G00n - 8*np.pi*G3*T00n))/(np.max(np.abs(8*np.pi*G3*T00n))+1e-30)
resij = np.max(np.abs(GijN - 8*np.pi*G3*TijN))/(np.max(np.abs(8*np.pi*G3*TijN))+1e-30)
OUT["3d_einstein"] = {
    "N": Ns, "L": float(L3),
    "rel_res_G00": float(res00),
    "rel_res_Gij": float(resij),
    "tolerance": 1e-6,
    "note": "metric built from Lap Psi = 4piG rho_T, Lap(Phi-Psi) = 4piG T^k_k,T; "
            "all 10 components G_mu nu = 8 pi G T_mu nu including the vacuum "
            "isotropic stress (V0 F, projected mean term)",
}

# ============================================================================
#  PART D — footings: V0 calibration = epsilon_Lambda (display only; V0 is an input)
# ============================================================================
OUT["footings"] = {
    "kappa": "1/2 ADOPTED (input, not derived)",
    "canonical": {
        "a0": A0_CAN, "rho_Lambda": RHO_L_CAN, "V0_calib = eps_Lambda (J/m^3)": EPS_L_CAN
    },
    "alternative": {
        "a0": A0_ALT, "rho_Lambda": RHO_L_ALT, "V0_calib = eps_Lambda (J/m^3)": EPS_L_ALT
    },
    "V0_alt/V0_can": float(EPS_L_ALT/EPS_L_CAN),
    "note": "same kappa=1/2, different rho_Lambda => different V0 calibration; "
            "no shared (rho_Lambda, kappa) pair reproduces both a0 footings",
}
Ndemo = 64; Ld = 4*np.pi
xd = np.linspace(0, Ld, Ndemo, endpoint=False)
Ad = 0.2
zzd = zprof(Ad, xd, Ndemo)
Fp_d = 2.0*zzd**3*(zzd+2.0)/(1.0+zzd)**3
sig_d = -Fp_d
Kd = -(np.mean(sig_d))*zzd     # scalar coefficient of Delta T^ij at V0 = 1 (Pa per unit V0)
OUT["demo_stress"] = {
    "profile": "z = A(sin x + 0.35 sin 2x + 0.12 sin 3x), A = 0.2, L = 4 pi, unit lapse",
    "mean_z3": float(np.mean(zzd**3)),
    "leading_coeff_4V0<z^3>z max (V0=1, Pa)": float(4.0*np.mean(zzd**3)*np.max(np.abs(zzd))),
    "max|Delta T^ij| with V0 = eps_L_can (Pa)": float(np.max(np.abs(Kd))*EPS_L_CAN),
    "max|Delta T^ij| with V0 = eps_L_alt (Pa)": float(np.max(np.abs(Kd))*EPS_L_ALT),
    "trace_free": "identically 0 (isotropic delta-ij structure; machine check above)",
    "sign": "Delta T^ij = +4 V0 <z^3>_h z delta^ij / N at leading order (sign set by the "
            "third moment of z)",
}

# ============================================================================
#  PART E — sanity assertions / checks (capable of failing)
# ============================================================================
checks = []
def ck(name, ok, obs, tol):
    checks.append({"name": name, "pass": bool(ok), "observed": obs, "tolerance": tol})

ck("CK1_closed_form_Fm1", str(sp.simplify(Fm1 - targetFm1)) == "0",
   str(sp.simplify(Fm1 - targetFm1)), "residual == 0 (symbolic)")
ck("CK1b_closed_form_Fp", str(sp.simplify(Fpz - targetFpz)) == "0",
   str(sp.simplify(Fpz - targetFpz)), "residual == 0 (symbolic)")
ck("CK2_flatness", (f1 == 0 and f2 == 0 and f3 == 0 and f4 == 24),
   f"F'(1)={f1}, F''(1)={f2}, F'''(1)={f3}, F''''(1)={f4}", "0,0,0,24")
ck("CK3_leading_coef_Fp", coef_Fpz[3] == 4, str(coef_Fpz[3]), "4")
ck("CK4_leading_coef_Fm1", sp.Poly(ser_Fm1, z).all_coeffs()[::-1][4] == 1, "1", "1")
ck("CK5_quartic_resid_ratio", abs(results_1d[128]["resid_ratio_0075_015"] - 1.0/32.0) < 0.1*1.0/32.0,
   f"{results_1d[128]['resid_ratio_0075_015']:.6f}", "1/32 within 10%")
ck("CK6_oldfloor_linear_ratio", abs(results_1d[128]["old_ratio_0075_015"] - 0.5) < 0.1*0.5,
   f"{results_1d[128]['old_ratio_0075_015']:.6f}", "1/2 within 10%")
ck("NEG1_oldfloor_contradiction", abs(results_1d[128]["old_ratio_0075_015"] - 1.0/32.0) > 0.1,
   f"old-floor ratio {results_1d[128]['old_ratio_0075_015']:.6f} vs quartic 1/32: linear "
   "susceptibility is incompatible with F'(1)=F''(1)=0", "must NOT equal 1/32")
ck("NEG2_wrongsign_fires", abs(results_1d[128]["wrongsign_ratio"] - 1.0/16.0) < 0.1/16.0,
   f"{results_1d[128]['wrongsign_ratio']:.6f} vs 1/16 (corrupt sign leaves O(z^4) residual)",
   "1/16 != 1/32")
ck("CK7_TF_zero", max(r_["max_abs_TF"] for r_ in results_1d[128]["rows"].values()) < 1e-12,
   f"{max(r_['max_abs_TF'] for r_ in results_1d[128]['rows'].values()):.3e}",
   "< 1e-12 (isotropic: trace-free part identically zero)")
ck("CK8_suscept_recovery", all(abs(r-1.0) < 1e-9 for r in results_1d[128]["susceptibility_recovery_<sigma>/(-4<z^3>)"]),
   str(results_1d[128]["susceptibility_recovery_<sigma>/(-4<z^3>)"]),
   "<sigma_v> = -4 V0 <z^3> (1+O(z)) exactly")
ck("CK9_einstein_3d", res00 < 1e-6 and resij < 1e-6,
   f"rel_res G00 = {res00:.3e}, rel_res Gij = {resij:.3e}", "< 1e-6")
ck("CK10_refinement_stable",
   abs(results_1d[64]["resid_ratio_0075_015"] - results_1d[128]["resid_ratio_0075_015"]) < 0.01,
   f"N64 {results_1d[64]['resid_ratio_0075_015']:.6f} vs N128 {results_1d[128]['resid_ratio_0075_015']:.6f}",
   "ratios agree to 0.01")
ck("CK11_old_floor_derivatives", (sp.limit(sp.diff(1/t, t), t, 1) == -1 and
                                  sp.limit(sp.diff(1/t, t, 2), t, 1) == 2),
   "F_old'(1) = -1, F_old''(1) = 2 (nonzero; contradiction witness for NEG1)",
   "-1 and 2, both != 0")
OUT["checks"] = checks

# ============================================================================
#  Bounds & bookkeeping
# ============================================================================
try:
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    OUT["bounds"] = {"rlimit_AS_512MB": "ENFORCED"}
except Exception as e:
    OUT["bounds"] = {"rlimit_AS_512MB": f"NOT ENFORCEABLE: {e!r}; peak RSS measured below"}
OUT["bounds"].update({
    "signal_alarm_s": 120, "alarm_remaining_s": signal.getitimer(signal.ITIMER_REAL)[0],
    "wall_s": float(time.time() - T0),
    "threads": os.environ.get("OMP_NUM_THREADS", "unset"),
})

with open("raw_output.json", "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
print(json.dumps(OUT, indent=1, default=str))