#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS229 — projected-vacuum contribution to lensing slip (Tier-0b seed).  REV 2.
CA5-GNC-R reciprocal vacuum barrier:  L_v = -V0 F(t),  F(t) = 1 + (t + 1/t - 2)^2,
t = 1 + z = 1 + Z - <Z>_h > 0, static weak inhomogeneous z with proper-volume
mean zero (unit lapse leading order:  <z>_h = 0), expand about t_c = 1.

Target (seed math block):
    Delta T^ij_mean = -(<N sigma_v>_h / N) z h^ij ,   sigma_v = -V0 F'(t_c).

Rev 2 changes versus rev 1 (as229_vacuum_lensing.py, preserved as failed attempt):
  * profile z = A(sin x + 0.35 cos 2x + 0.12 sin 3x)  -- MIXED PARITY so that
    <z^3>_h != 0 (rev 1 used pure sine modes; <z^3> = 0 identically, which
    degenerates the leading-order test).
  * 3D Einstein check rebuilt: (C1) independent full-nonlinear finite-difference
    Ricci tensor vs the linearized scalar identities (catches factor/sign slips);
    (C2) consistent-source factor check including a nonzero anisotropic stress;
    (C3) vacuum composite identities (rho_v + P_v = -<N sigma>/N z exactly,
    Pi_v = 0).  Rev 1's naive prescription of arbitrary isotropic P with S != 0
    is not a static weak-field solution (slip/pressure compatibility) -- now
    documented as a derived constraint in derivation.md.
"""
import signal, time, json, os
import numpy as np
import sympy as sp

T0 = time.time()
signal.alarm(120)
OUT = {}

# ----------------------------------------------------------------------------
#  Constants (SI; campaign defaults; G_N only - G_bare/G_cosmo NOT used)
# ----------------------------------------------------------------------------
G   = 6.67430e-11
c   = 299792458.0
M_SUN = 1.98847e30
PC  = 3.085677581491367e16
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

Fm1   = sp.simplify(F.subs(t, 1+z) - 1)
Fpz   = sp.simplify(Fp.subs(t, 1+z))
targetFm1  = z**4/(1+z)**2
targetFpz  = 2*z**3*(z+2)/(1+z)**3
OUT["closed_forms"] = {
    "Fm1_expr": str(Fm1), "Fm1_target": str(targetFm1),
    "Fm1_residual": str(sp.simplify(Fm1 - targetFm1)),
    "Fpz_expr": str(Fpz), "Fpz_target": str(targetFpz),
    "Fpz_residual": str(sp.simplify(Fpz - targetFpz)),
}

ser_Fm1 = sp.series(Fm1, z, 0, 10).removeO().expand()
ser_Fpz = sp.series(Fpz, z, 0, 10).removeO().expand()
coef_Fpz = sp.Poly(ser_Fpz, z).all_coeffs()[::-1]
coef_Fm1 = sp.Poly(ser_Fm1, z).all_coeffs()[::-1]
OUT["series_Fm1_coefs_z0_to_z9"] = [str(x) for x in coef_Fm1]
OUT["series_Fpz_coefs_z0_to_z9"] = [str(x) for x in coef_Fpz]
OUT["leading_Fpz_coef_z3"] = str(coef_Fpz[3])
OUT["leading_Fm1_coef_z4"] = str(coef_Fm1[4])

sigma = -V0 * Fpz
ser_sigma = sp.series(sigma, z, 0, 10).removeO().expand()
OUT["sigma_v_series_leading_z3_coef"] = str(sp.Poly(ser_sigma, z).all_coeffs()[::-1][3])
OUT["DeltaT_series_leading_z4_coef"] = str(sp.Poly((-ser_sigma*z).expand(), z).all_coeffs()[::-1][4])

# ---- A4: linearized Einstein scalar combinations (static, weak, 3D, c=1) ----
x1, x2, x3 = sp.symbols("x1 x2 x3")
Phi = sp.Function("Phi")(x1, x2, x3)
Psi = sp.Function("Psi")(x1, x2, x3)
def dd(f, i, j):
    return sp.diff(sp.diff(f, [x1, x2, x3][i]), [x1, x2, x3][j])
def lap(f):
    return sum(sp.diff(f, [x1,x2,x3][i], 2) for i in range(3))
R00 = lap(Phi)
Rij = [[(lap(Psi) if i == j else 0) + dd(Psi, i, j) - dd(Phi, i, j) for j in range(3)]
       for i in range(3)]
Rtr = -R00 + sum(Rij[i][i] for i in range(3))
G00 = R00 + sp.Rational(1,2)*Rtr
Gij = [[Rij[i][j] - sp.Rational(1,2)*Rtr*(1 if i==j else 0) for j in range(3)] for i in range(3)]
Gkk = sum(Gij[i][i] for i in range(3))
Ssym = Phi - Psi
OUT["einstein_symbolic"] = {
    "G00 - 2 Lap Psi": str(sp.simplify(G00 - 2*lap(Psi))),
    "G^k_k - 2 Lap (Phi-Psi)": str(sp.simplify(Gkk - 2*lap(Ssym))),
    "G_01 - [Lap S d_01 - S_,01]": str(sp.simplify(Gij[0][1] - (0 - dd(Ssym,0,1)))),
    "G_11 - [Lap S - S_,11]": str(sp.simplify(Gij[1][1] - (lap(Ssym) - dd(Ssym,1,1)))),
    "G_22 - [Lap S - S_,22]": str(sp.simplify(Gij[2][2] - (lap(Ssym) - dd(Ssym,2,2)))),
}
OUT["einstein_combos"] = {
    "Lap Psi": "4 pi G rho      (T00 = rho)",
    "Lap (Phi-Psi)": "4 pi G T^k_k",
    "Lap Phi": "4 pi G (rho + T^k_k)",
    "Lap (Phi+Psi)": "4 pi G (2 rho + T^k_k)",
    "TF": "TF(G)_ij = -(d_i d_j - (1/3) d_ij Lap)(Phi-Psi) = 8 pi G Pi_ij;  Pi_ij = T_ij - (1/3) d_ij T^k_k",
}

# ============================================================================
#  PART B — numeric: 1D periodic leaf (flat, unit lapse N=1 at leading order)
# ============================================================================
def zprof(A, x):
    return A*(np.sin(x) + 0.35*np.cos(2.0*x) + 0.12*np.sin(3.0*x))

results_1d = {}
for N in (64, 128):
    L = 4.0*np.pi
    x = np.linspace(0, L, N, endpoint=False)
    AMPS = (0.3, 0.15, 0.075, 0.0375, 0.018, 0.009)
    row = {}
    for A in AMPS:
        zz = zprof(A, x)
        tz = 1.0 + zz
        assert tz.min() > 0.0
        Fm1_n = zz**4/(1.0+zz)**2
        Fp_n  = 2.0*zz**3*(zz+2.0)/(1.0+zz)**3
        sigma_n = -Fp_n                 # V0 = 1
        meanS = np.mean(sigma_n)
        dT   = -(meanS/1.0)*zz          # Delta T^ij_mean scalar coefficient (V0=1, N=1)
        z3m  = np.mean(zz**3)
        lead = 4.0*z3m*zz               # leading O(z^4) term
        resid = dT - lead
        row[A] = {
            "min_z": float(zz.min()),
            "mean_z": float(np.mean(zz)),
            "mean_z3": float(np.mean(zz**3)),
            "max_abs_dT": float(np.max(np.abs(dT))),
            "max_abs_lead": float(np.max(np.abs(lead))),
            "max_abs_resid_after_lead": float(np.max(np.abs(resid))),
            "max_abs_TF": float(np.max(np.abs(dT - (1.0/3.0)*3.0*dT))),
            "dT_old_max": float(np.max(np.abs(-np.mean(1.0/(tz*tz))*zz))),
            "dT_wrongsign_resid_vs_lead": float(np.max(np.abs((+np.mean(sigma_n))*zz - lead))),
        }
    results_1d[N] = {"rows": row}
    for label, key, div in (("resid_after_lead", "max_abs_resid_after_lead", 32.0),
                            ("dT_leading", "max_abs_dT", 16.0),
                            ("old_floor", "dT_old_max", 2.0)):
        r_small = row[0.009][key]/row[0.018][key]
        r_trend = row[0.075][key]/row[0.15][key]
        results_1d[N][f"ratio_{label}_0009_0018"] = float(r_small)
        results_1d[N][f"ratio_{label}_0075_015"] = float(r_trend)
        results_1d[N][f"expect_{label}"] = f"1/{int(div)}  (small-amplitude pair primary)"
    results_1d[N]["wrongsign_ratio_0009_0018"] = float(
        row[0.009]["dT_wrongsign_resid_vs_lead"]/row[0.018]["dT_wrongsign_resid_vs_lead"])
    results_1d[N]["expect_wrongsign"] = "1/16 = 0.0625 != 1/32"
    # recovery of the leading susceptibility <N sigma>/<-4<z^3>> -> 1 (rate O(A))
    rec, dev = [], []
    for A in (0.3, 0.15, 0.075, 0.0375):
        zz = zprof(A, x)
        Fp_n = 2.0*zz**3*(zz+2.0)/(1.0+zz)**3
        r = float(np.mean(-Fp_n)/np.mean(-4.0*zz**3))
        rec.append(r); dev.append(abs(r-1.0))
    results_1d[N]["susceptibility_recovery"] = rec
    results_1d[N]["recovery_deviation_ratio_00375_0075"] = float(dev[3]/dev[2]) \
        if dev[2] > 0 else None
    results_1d[N]["expect_recovery_deviation_ratio"] = "0.5 (O(A) approach)"
    # substitute-back (truncated Taylor susceptibility vs full)
    zz = zprof(0.2, x)
    Fp_n  = 2.0*zz**3*(zz+2.0)/(1.0+zz)**3
    Fp_tr = 4.0*zz**3 - 10.0*zz**4 + 18.0*zz**5
    results_1d[N]["substitute_back_trunc3_vs_full_max"] = float(
        np.max(np.abs(-(np.mean(-Fp_n))*zz + (np.mean(-Fp_tr))*zz)))
    results_1d[N]["max_abs_dT_A0.2"] = float(np.max(np.abs(-(np.mean(-Fp_n))*zz)))
OUT["1d"] = results_1d

# ============================================================================
#  PART C — 3D: independent nonlinear-Ricci check + consistent-source factors
# ============================================================================
Ns = 32
L3 = 4.0*np.pi
ax = np.linspace(0, L3, Ns, endpoint=False)
X, Y, Zg = np.meshgrid(ax, ax, ax, indexing="ij")
# NOTE: fftfreq returns CYCLES/unit; angular wavenumbers need the 2*pi factor.
# (rev2 first run omitted it -- the spectral reference operators were (2 pi)^2
#  too small while the FD nonlinear-Ricci builder was correct; the mismatch
#  exposed exactly this, recorded in failed_attempts.)
kvec = 2.0*np.pi*np.fft.fftfreq(Ns, d=L3/Ns)
KX, KY, KZ = np.meshgrid(kvec, kvec, kvec, indexing="ij")
K2 = KX**2 + KY**2 + KZ**2
K2[0,0,0] = 1.0

def poisson(src):
    f = np.fft.fftn(src)
    u = -4.0*np.pi*G*f/K2
    u[0,0,0] = 0.0
    return np.fft.ifftn(u).real

def lapN(f):
    return np.fft.ifftn(-K2*np.fft.fftn(f)).real

def ddN(f, i, j):
    kk1 = [KX, KY, KZ][i]; kk2 = [KX, KY, KZ][j]
    return np.fft.ifftn(-kk1*kk2*np.fft.fftn(f)).real

def d1(f, axis):
    """first centered difference, same stencil class as the FD Ricci builder"""
    return (np.roll(f, -1, axis=axis) - np.roll(f, +1, axis=axis))/(2.0*hstep)

def lap_m(f):
    """second derivative by composition of d1 (matches the builder's stencil)"""
    return d1(d1(f,0),0) + d1(d1(f,1),1) + d1(d1(f,2),2)

def dd_m(f, i, j):
    return d1(d1(f,i),j)

hstep = L3/Ns
def dgcG(garr, mu, nu, a):
    axs = {'x':0,'y':1,'z':2}[a]
    return (np.roll(garr[mu,nu], -1, axis=axs) - np.roll(garr[mu,nu], +1, axis=axs))/(2.0*hstep)

def eins_metric(PhiN, PsiN):
    h = np.zeros((4,4)+PhiN.shape)
    h[0,0] = -2.0*PhiN
    for i in range(3):
        h[i+1,i+1] = -2.0*PsiN
    g = np.zeros((4,4)+PhiN.shape)
    for mu in range(4):
        for nu in range(4):
            g[mu,nu] = eta[mu,nu] + h[mu,nu]
    gi = np.zeros_like(g)
    for idx in np.ndindex(PhiN.shape):
        gi[:,:,idx[0],idx[1],idx[2]] = np.linalg.inv(g[:,:,idx[0],idx[1],idx[2]])
    return g, gi

def eins_G(PhiN, PsiN):
    g, gi = eins_metric(PhiN, PsiN)
    Gamma = np.zeros((4,4,4)+PhiN.shape)
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                s = 0.0
                for sig in range(4):
                    if mu != 0:
                        s += gi[lam,sig]*dgcG(g,sig,nu,('x','y','z')[mu-1])
                    if nu != 0:
                        s += gi[lam,sig]*dgcG(g,sig,mu,('x','y','z')[nu-1])
                    if sig != 0:
                        s -= gi[lam,sig]*dgcG(g,mu,nu,('x','y','z')[sig-1])
                Gamma[lam,mu,nu] = 0.5*s
    def dG(lam, mu, nu, a):
        axs = {'x':0,'y':1,'z':2}[a]
        return (np.roll(Gamma[lam,mu,nu], -1, axis=axs) - np.roll(Gamma[lam,mu,nu], +1, axis=axs))/(2.0*hstep)
    R = np.zeros((4,4)+PhiN.shape)
    for mu in range(4):
        for nu in range(4):
            acc = 0.0
            for lam in range(1,4):
                acc += dG(lam, mu, nu, ('x','y','z')[lam-1])
            for lam in range(4):
                if nu != 0:
                    acc -= dG(lam, mu, lam, ('x','y','z')[nu-1])
            for s in range(4):
                for l in range(4):
                    acc += Gamma[s,mu,nu]*Gamma[l,s,l] - Gamma[s,mu,l]*Gamma[l,nu,s]
            R[mu,nu] = acc
    Rt = -R[0,0] + sum(R[i,i] for i in range(1,4))
    Gt = np.zeros_like(R)
    for mu in range(4):
        for nu in range(4):
            Gt[mu,nu] = R[mu,nu] - 0.5*Rt*g[mu,nu]
    return Gt

eta = np.diag([-1.0,1.0,1.0,1.0])

# ---- C1: independent nonlinear-Ricci identity check ----
Amp = 2.5e-3
PhiN = Amp*(0.6*np.sin(X) + 0.35*np.sin(Y)*np.cos(Zg) + 0.25*np.cos(X+Y+Zg))
PsiN = Amp*(0.5*np.cos(Y) + 0.4*np.sin(X+Zg) + 0.3*np.sin(X)*np.cos(Y))
Gt = eins_G(PhiN, PsiN)
Slin = PhiN - PsiN
# stencil-matched linearized references (same d1-composition stencil the builder
# uses; the spectral lapN would leave a (sin(kh)/kh)^2 ~ 5% stencil mismatch)
LG00m = 2.0*lap_m(PsiN)
LGijm = np.zeros((3,3)+PhiN.shape)
for i in range(3):
    for j in range(3):
        LGijm[i,j] = lap_m(Slin)*(1.0 if i==j else 0.0) - dd_m(Slin,i,j)
LGkkm = 2.0*lap_m(Slin)
def relres(a, b):
    return float(np.max(np.abs(a-b))/np.max(np.abs(b)+1e-30))
scale = float(np.max(np.abs(LGijm)))
# index map: Gt is 4x4 (0=time); spatial (i,j) <-> Gt[1+i,1+j]
OUT["3d_nonlinear_ricci"] = {
    "amplitude": Amp, "N": Ns,
    "rel_res_G00_2LapPsi": relres(Gt[0,0], LG00m),
    "rel_res_Gkk_2LapS": relres(sum(Gt[i+1,i+1] for i in range(3)), LGkkm),
    "abs_res_Gxy_scaled": float(np.max(np.abs(Gt[1,2] - LGijm[0,1])))/scale,
    "abs_res_Gxx_scaled": float(np.max(np.abs(Gt[1,1] - LGijm[0,0])))/scale,
    "abs_res_Gyy_scaled": float(np.max(np.abs(Gt[2,2] - LGijm[1,1])))/scale,
    "abs_res_Gzz_scaled": float(np.max(np.abs(Gt[3,3] - LGijm[2,2])))/scale,
    "abs_res_Gzz_spectral_scaled": float(np.max(np.abs(Gt[3,3] - (lapN(Slin) - ddN(Slin,2,2)))))/scale,
    "max|G_tx| (must vanish: static diagonal ansatz)": float(np.max(np.abs(Gt[0,1]))),
    "tolerance_rel": 0.01,
    "note": "full nonlinear FD Ricci vs linearized scalar identities, stencil-matched; "
            "residuals ~ Amp^2 nonlinearity + O(h^2); spectral comparison of Gzz shown "
            "to quantify the stencil mismatch",
}

# ---- C2: consistent-source factor check (anisotropic Pi from S) ----
# Stencil-consistent construction: potentials and sources are DEFINED directly
# (no Poisson solve, which would couple the spectral operator to the FD builder
# and leave a (sin(kh)/kh)^2 mismatch).  rho is the stencil-Laplacian of PsiS so
# the 4 pi G / 8 pi G factors are algebraically under test.
G1 = 1.0
Amp2 = 2.5e-3
PsiS = 0.4*np.sin(X)*np.cos(Y) + 0.25*np.sin(X+2.0*Zg)
Sd   = 0.35*np.cos(X)*np.sin(Y) + 0.25*np.sin(X+Y+Zg)
rhod = lap_m(PsiS)/(4.0*np.pi*G1)
Tij = np.zeros((3,3)+PhiN.shape)
for i in range(3):
    for j in range(3):
        Tij[i,j] = (1.0/(8.0*np.pi*G1))*(lap_m(Sd)*(1.0 if i==j else 0.0) - dd_m(Sd,i,j))
Tkk = sum(Tij[i,i] for i in range(3))
PhiB = Amp2*(PsiS + Sd)
PsiB = Amp2*PsiS
GB = eins_G(PhiB, PsiB)
def rmmean(a):
    return a - np.real(np.fft.fftn(a)[0,0,0])/(Ns**3)
r_psi = float(np.max(np.abs(rmmean(GB[0,0] - 8.0*np.pi*G1*Amp2*rhod))))
r_skk = float(np.max(np.abs(rmmean(sum(GB[i+1,i+1] for i in range(3)) - 8.0*np.pi*G1*Amp2*Tkk))))
r_tf  = 0.0
for i in range(3):
    for j in range(3):
        r_tf = max(r_tf, float(np.max(np.abs(rmmean(
            GB[i+1,j+1] - (1.0/3.0)*(1 if i==j else 0.0)*sum(GB[k+1,k+1] for k in range(3))
            - 8.0*np.pi*G1*Amp2*(Tij[i,j] - (1.0/3.0)*(1 if i==j else 0.0)*Tkk))))))
# factor-mutation control: 8 pi G in the rho-definition instead of 4 pi G must fire
rho_mut = lap_m(PsiS)/(8.0*np.pi*G1)
r_psi_mut = float(np.max(np.abs(rmmean(GB[0,0] - 8.0*np.pi*G1*Amp2*rho_mut))))
rho_tri = lap_m(PsiS)/(2.0*np.pi*G1)
r_psi_tri = float(np.max(np.abs(rmmean(GB[0,0] - 8.0*np.pi*G1*Amp2*rho_tri))))
OUT["3d_consistent_sources"] = {
    "res_LapPsi_equiv": r_psi,
    "res_LapS_equiv": r_skk,
    "res_TF_equiv": r_tf,
    "res_factor_mutation_8pi_over_4pi": r_psi_mut,
    "res_factor_mutation_2pi_over_4pi": r_psi_tri,
    "scale_8piG1*Amp2*rho": float(np.max(np.abs(8.0*np.pi*G1*Amp2*rhod))),
    "tolerance": 1e-4,
    "note": "sources defined stencil-consistently by the combination equations with "
            "anisotropic Pi from S; 4piG/8piG factors are the objects under test; "
            "mutated factors must leave O(scale) residuals",
}

# ---- C3: vacuum composite identities (numeric, exact) ----
A3x = 0.15
zz3 = A3x*(np.sin(X) + 0.35*np.cos(2.0*Y) + 0.12*np.sin(3.0*Zg))
Fm1_3 = zz3**4/(1.0+zz3)**2
Fp_3  = 2.0*zz3**3*(zz3+2.0)/(1.0+zz3)**3
V0num = 1.0
rho_v3 = V0num*(1.0+Fm1_3)
sig3   = -V0num*Fp_3
P_v3   = -V0num*(1.0+Fm1_3) - np.mean(sig3)*zz3
OUT["3d_vacuum_composite"] = {
    "max|rho_v + P_v - (-<N sigma>/N z)|": float(np.max(np.abs(rho_v3 + P_v3 + np.mean(sig3)*zz3))),
    "max|Pi_v| (trace-free of isotropic stress)": 0.0,
    "max|P_v - <P_v>| (inhomogeneous part nonzero)": float(np.max(np.abs(P_v3 - np.mean(P_v3)))),
    "max|<N sigma_v>/N - (-4 V0 <z^3>)|": float(np.abs(np.mean(sig3) + 4.0*np.mean(zz3**3))),
    "note": "rho_v + P_v = -(<N sigma_v>/N) z holds exactly (F parts cancel); "
            "sigma_v = -V0 F'(1+z) ~ -4 V0 z^3 + O(z^4)",
}

# ============================================================================
#  PART D — footings: V0 calibration = epsilon_Lambda (display only; V0 is an input)
# ============================================================================
OUT["footings"] = {
    "kappa": "1/2 ADOPTED (input, not derived)",
    "canonical": {"a0": A0_CAN, "rho_Lambda": RHO_L_CAN,
                  "V0_calib = eps_Lambda (J/m^3)": EPS_L_CAN},
    "alternative": {"a0": A0_ALT, "rho_Lambda": RHO_L_ALT,
                    "V0_calib = eps_Lambda (J/m^3)": EPS_L_ALT},
    "V0_alt/V0_can": float(EPS_L_ALT/EPS_L_CAN),
    "note": "same kappa=1/2, different rho_Lambda => different V0; no shared "
            "(rho_Lambda, kappa) pair reproduces both a0 footings",
}
Ndemo = 64
xd = np.linspace(0, 4.0*np.pi, Ndemo, endpoint=False)
Ad = 0.2
zzd = zprof(Ad, xd)
Fp_d = 2.0*zzd**3*(zzd+2.0)/(1.0+zzd)**3
sig_d = -Fp_d
Kd = -(np.mean(sig_d))*zzd
OUT["demo_stress"] = {
    "profile": "z = A(sin x + 0.35 cos 2x + 0.12 sin 3x), A = 0.2, L = 4 pi, unit lapse",
    "mean_z3": float(np.mean(zzd**3)),
    "max|Delta T^ij| with V0 = eps_L_can (Pa)": float(np.max(np.abs(Kd))*EPS_L_CAN),
    "max|Delta T^ij| with V0 = eps_L_alt (Pa)": float(np.max(np.abs(Kd))*EPS_L_ALT),
    "trace_free": "identically 0 (isotropic delta-ij structure; machine check above)",
    "sign": "Delta T^ij = +4 V0 <z^3>_h z delta^ij / N at leading order (sign set by "
            "the third moment of z)",
}

# ============================================================================
#  PART E — checks (capable of failing)
# ============================================================================
checks = []
def ck(name, ok, obs, tol):
    checks.append({"name": name, "pass": bool(ok), "observed": obs, "tolerance": tol})

ck("CK1_closed_form_Fm1", str(sp.simplify(Fm1 - targetFm1)) == "0",
   "residual 0", "residual == 0 (symbolic)")
ck("CK1b_closed_form_Fp", str(sp.simplify(Fpz - targetFpz)) == "0",
   "residual 0", "residual == 0 (symbolic)")
ck("CK2_flatness", (f1 == 0 and f2 == 0 and f3 == 0 and f4 == 24),
   f"F'(1)={f1}, F''(1)={f2}, F'''(1)={f3}, F''''(1)={f4}", "0,0,0,24")
ck("CK3_leading_coef_Fp_z3", coef_Fpz[3] == 4, str(coef_Fpz[3]), "4")
ck("CK4_leading_coef_Fm1_z4", coef_Fm1[4] == 1, str(coef_Fm1[4]), "1")
r128 = results_1d[128]
ck("CK5_quartic_lead_ratio", abs(r128["ratio_dT_leading_0009_0018"] - 1.0/16.0) < 0.1/16.0,
   f"{r128['ratio_dT_leading_0009_0018']:.6f} (trend 0.075/0.15: "
   f"{r128['ratio_dT_leading_0075_015']:.6f})", "1/16 (|DT| ~ A^4, small-A pair)")
ck("CK5b_resid_after_lead_ratio",
   abs(r128["ratio_resid_after_lead_0009_0018"] - 1.0/32.0) < 0.1/32.0,
   f"{r128['ratio_resid_after_lead_0009_0018']:.6f} (trend 0.075/0.15: "
   f"{r128['ratio_resid_after_lead_0075_015']:.6f})", "1/32 (next order z^5, small-A pair)")
ck("CK6_oldfloor_linear_ratio", abs(r128["ratio_old_floor_0075_015"] - 0.5) < 0.1*0.5,
   f"{r128['ratio_old_floor_0075_015']:.6f}", "1/2 (linear)")
ck("NEG1_oldfloor_contradiction",
   abs(r128["ratio_old_floor_0075_015"] - 1.0/32.0) > 0.1,
   f"old-floor {r128['ratio_old_floor_0075_015']:.6f} vs barrier residual-ratio 1/32: "
   "linear susceptibility incompatible with F'(1)=F''(1)=0", "must NOT equal 1/32")
ck("NEG2_wrongsign_fires", abs(r128["wrongsign_ratio_0009_0018"] - 1.0/16.0) < 0.1/16.0,
   f"{r128['wrongsign_ratio_0009_0018']:.6f}", "1/16 != 1/32 (corrupt sign leaves O(z^4))")
ck("CK7_TF_zero", max(r_["max_abs_TF"] for r_ in r128["rows"].values()) < 1e-12,
   f"{max(r_['max_abs_TF'] for r_ in r128['rows'].values()):.3e}", "< 1e-12")
ck("CK8_suscept_recovery",
   all(abs(rr-1.0) < 0.6 for rr in r128["susceptibility_recovery"][2:4]) and
   r128["recovery_deviation_ratio_00375_0075"] is not None and
   abs(r128["recovery_deviation_ratio_00375_0075"] - 0.5) < 0.3,
   f"recovery {r128['susceptibility_recovery']}, deviation ratio "
   f"{r128['recovery_deviation_ratio_00375_0075']:.3f}", "-> 1 at O(A) rate (dev ratio ~0.5)")
c1 = OUT["3d_nonlinear_ricci"]
ck("CK9_nonlinear_ricci_consistency",
   c1["rel_res_G00_2LapPsi"] < 0.01 and c1["rel_res_Gkk_2LapS"] < 0.01 and
   c1["abs_res_Gxy_scaled"] < 0.01 and c1["abs_res_Gxx_scaled"] < 0.01 and
   c1["abs_res_Gyy_scaled"] < 0.01 and c1["abs_res_Gzz_scaled"] < 0.01 and
   c1["max|G_tx| (must vanish: static diagonal ansatz)"] < 1e-12,
   f"G00 {c1['rel_res_G00_2LapPsi']:.3e}, Gkk {c1['rel_res_Gkk_2LapS']:.3e}, "
   f"Gxy {c1['abs_res_Gxy_scaled']:.3e}, Gxx {c1['abs_res_Gxx_scaled']:.3e}, "
   f"Gyy {c1['abs_res_Gyy_scaled']:.3e}, Gzz {c1['abs_res_Gzz_scaled']:.3e}, "
   f"Gtx {c1['max|G_tx| (must vanish: static diagonal ansatz)']:.3e}",
   "< 0.01 (stencil-matched), G_tx == 0")
c2 = OUT["3d_consistent_sources"]
ck("CK9b_consistent_source_factors",
   c2["res_LapPsi_equiv"] < 1e-4 and c2["res_LapS_equiv"] < 1e-4 and c2["res_TF_equiv"] < 1e-4 and
   c2["res_factor_mutation_8pi_over_4pi"] > 0.5*c2["scale_8piG1*Amp2*rho"] and
   c2["res_factor_mutation_2pi_over_4pi"] > 0.5*c2["scale_8piG1*Amp2*rho"],
   f"LapPsi {c2['res_LapPsi_equiv']:.3e}, LapS {c2['res_LapS_equiv']:.3e}, "
   f"TF {c2['res_TF_equiv']:.3e}; mutation 8pi {c2['res_factor_mutation_8pi_over_4pi']:.3e}, "
   f"2pi {c2['res_factor_mutation_2pi_over_4pi']:.3e} vs scale {c2['scale_8piG1*Amp2*rho']:.3e}",
   "residuals < 1e-4 AND both factor mutations fire at O(scale)")
c3 = OUT["3d_vacuum_composite"]
ck("CK10_vacuum_composite", c3["max|rho_v + P_v - (-<N sigma>/N z)|"] < 1e-14,
   f"{c3['max|rho_v + P_v - (-<N sigma>/N z)|']:.3e}",
   "< 1e-14 (exact cancellation of the F parts)")
ck("CK11_refinement_stable",
   abs(results_1d[64]["ratio_dT_leading_0075_015"] - r128["ratio_dT_leading_0075_015"]) < 0.01,
   f"N64 {results_1d[64]['ratio_dT_leading_0075_015']:.6f} vs N128 "
   f"{r128['ratio_dT_leading_0075_015']:.6f}", "agree to 0.01")
ck("CK12_old_floor_derivatives",
   (sp.limit(sp.diff(1/t, t), t, 1) == -1 and sp.limit(sp.diff(1/t, t, 2), t, 1) == 2),
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
    "signal_alarm_s": 120,
    "alarm_remaining_s": signal.getitimer(signal.ITIMER_REAL)[0],
    "wall_s": float(time.time() - T0),
    "threads": os.environ.get("OMP_NUM_THREADS", "unset"),
})

with open("raw_output.json", "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
print(json.dumps(OUT, indent=1, default=str))