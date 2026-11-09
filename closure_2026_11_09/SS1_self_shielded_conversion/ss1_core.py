#!/usr/bin/env python3
"""SS1 core (FROZEN_CRITERIA.md b5adc7a90b + AMENDMENT_A1 9aeeb48503): the self-shielded late conversion, own implementation.
The one gate rule: self-consistent radial peeling of the component's own column,
    d rho(r)/d tau = - rho(r) / (1 + x(r,tau)^2),  x = Sigma/Sigma_gate,
    Sigma(r) = sqrt( max(R500^2 - r^2, 0) * rhobar(<0.25 R500, tau) * rho(r, tau) ),
integrated with RK4 (A1) on 300 log shells per system, vectorised over systems. Pre-conversion halos: primary truncated SIS
(KD1 P3 capture amount f_cap R M_b), brackets NFW (Duffy 2008 c-M) and Moster+2013 abundance matching (disclosed, never grade).
Reduced ODE ln(x/x0) + (x^2 - x0^2)/2 = -tau and the frozen-Da formula exp(-tau/(1+x0^2)) are the reported reading and the
disclosed bracket. Units: kpc, Msun, tau in units of 1/Gamma0. kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, math, json, itertools
import numpy as np
from scipy.optimize import brentq

CRIT = "b5adc7a90b"; AMEND = "9aeeb48503"
NOTE = "kappa = 1/2 FITTED; not theory closed"
MUT = os.environ.get("SS1_MUTATE", "")                    # M1 Sigma_gate x3, M2 /3, M3 z_dec 2, M4 gate off
Z_DEC = 2.0 if MUT == "M3" else 0.55
GAMMA0_GYR = 0.820
TAU_TOT = 4.49
def _lookback_gyr(z, h=0.674, Om=0.3115):
    zz = [z * i / 20000 for i in range(20001)]; f = [1.0 / ((1 + x) * math.sqrt(Om * (1 + x) ** 3 + 1 - Om)) for x in zz]
    return 977.792 / (100 * h) * sum(0.5 * (f[i] + f[i + 1]) * (zz[i + 1] - zz[i]) for i in range(20000))
if MUT == "M3": TAU_TOT = GAMMA0_GYR * _lookback_gyr(Z_DEC)    # M3: z_dec 2 with the frozen bare rate (tau = Gamma0 [t(z) - t(z_dec)])
SIGMA_GATE_GCM2 = 0.042
MSUN_G = 1.98892e33; KPC_CM = 3.0857e21
SIG_UNIT = MSUN_G / KPC_CM ** 2                           # g/cm^2 per Msun/kpc^2
SIGMA_GATE = SIGMA_GATE_GCM2 / SIG_UNIT * {"M1": 3.0, "M2": 1.0 / 3.0}.get(MUT, 1.0)   # Msun/kpc^2 (2.01e8)
GATE_OFF = (MUT == "M4")
F_CAP = 0.76
N_SHELL = 300
DTAU = 0.0025
OUTSIDE = dict(v_med_c=0.0632, sigma_over_m_cm2g=1.40, Gamma_psi_Myr=4.20, R_abs_kpc3_Msun_Myr=1.68e-4, Gamma0_Gyr=GAMMA0_GYR)

# ------------------------------------------------------------------ reduced ODE and frozen-Da
def reduced(x0, tau=TAU_TOT):
    """exact solution of dx/dtau = -x/(1+x^2): ln(x/x0) + (x^2 - x0^2)/2 = -tau; returns the retention x/x0."""
    if x0 <= 0: return math.exp(-tau)
    g = lambda lr: lr + 0.5 * x0 * x0 * (math.exp(2 * lr) - 1.0) + tau
    return math.exp(brentq(g, -tau - 1e-9, 0.0, xtol=1e-14))
def frozen_da(x0, tau=TAU_TOT): return math.exp(-tau / (1.0 + x0 * x0))

# ------------------------------------------------------------------ cosmology helpers
RHOC0_PER_H2 = 277.536627          # Msun / kpc^3 at h = 1
def rho_crit(z, h, Om, Or=0.0):
    E2 = Om * (1 + z) ** 3 + Or * (1 + z) ** 4 + (1.0 - Om - Or); return RHOC0_PER_H2 * h * h * E2

# ------------------------------------------------------------------ pre-conversion halos
def duffy_c200(M200, z, h): return 5.71 * (M200 / (2e12 / h)) ** -0.084 * (1 + z) ** -0.47
def moster_mstar(M, z):
    """Moster, Naab & White 2013, eqs. 2, 11-14 (best fit): M*/M = 2N [(M/M1)^-beta + (M/M1)^gamma]^-1."""
    a1 = z / (1 + z)
    lM1 = 11.590 + 1.195 * a1; N = 0.0351 - 0.0247 * a1; beta = 1.376 - 0.826 * a1; gamma = 0.608 + 0.329 * a1
    M1 = 10 ** lM1; return M * 2 * N / ((M / M1) ** -beta + (M / M1) ** gamma)
def moster_halo(Mstar, z):
    return 10 ** brentq(lambda lm: math.log10(moster_mstar(10 ** lm, z)) - math.log10(Mstar), 8.0, 17.0, xtol=1e-10)

def halo(M_b, R, h, Om, kind="SIS", M200=None, Mchi=None, z=None):
    """pre-conversion halo at z_dec. Primary: M_chi0 = f_cap R M_b, M200 = M_b + M_chi0, truncated SIS. Returns a dict with
    R200, R500, the component fraction fchi and a callable rho_chi(r) (Msun/kpc^3) and M_chi(<r)."""
    z = Z_DEC if z is None else z
    if M200 is None:
        Mchi = F_CAP * R * M_b; M200 = M_b + Mchi
    fchi = Mchi / M200; rc = rho_crit(z, h, Om)
    R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
    if kind == "SIS":
        R500 = R200 * math.sqrt(200.0 / 500.0)
        rho = lambda r: fchi * M200 / (4 * math.pi * R200 * np.asarray(r, float) ** 2)
        Menc = lambda r: fchi * M200 * np.minimum(np.asarray(r, float), R200) / R200
        c = None
    else:
        c = duffy_c200(M200, z, h); rs = R200 / c; mu = lambda x: np.log1p(x) - x / (1 + x); A = M200 / mu(c)
        rho = lambda r: fchi * A / (4 * math.pi * rs ** 3) / ((np.asarray(r, float) / rs) * (1 + np.asarray(r, float) / rs) ** 2)
        Menc = lambda r: fchi * A * mu(np.minimum(np.asarray(r, float), R200) / rs)
        R500 = brentq(lambda rr: A * mu(rr / rs) / (4 / 3 * math.pi * rr ** 3) - 500 * rc, 1e-3 * R200, R200)
    return dict(M_b=M_b, M200=M200, Mchi0=Mchi, fchi=fchi, R200=R200, R500=R500, rho=rho, Menc=Menc, c200=c, kind=kind, rho_crit=rc)

def x0_system(H):
    """the system column used by the reduced reading: x0 = R500 rhobar_chi(<0.25 R500) / Sigma_gate."""
    r25 = 0.25 * H["R500"]; rb = float(H["Menc"](r25)) / (4 / 3 * math.pi * r25 ** 3); return H["R500"] * rb / SIGMA_GATE

# ------------------------------------------------------------------ the radial peeling (vectorised over systems)
def peel(halos, host_sigma=None, geo_hold=False, tau_tot=TAU_TOT, dtau=DTAU, record_taus=None, density=None):
    """halos: list of halo dicts. host_sigma: optional list (per system) of callables tau -> Sigma_host (Msun/kpc^2) added to the
    member's own column (members only). geo_hold: KA2 test switch (geometric factor R500^2 for every shell, A1).
    density: optional list of callables rho(r) replacing H['rho'] (KA2 top-hat).
    Returns dict with edges (kpc, per system), initial and final shell masses, and optional snapshots of total retention."""
    ns = len(halos); u_out = max(H["R200"] / H["R500"] for H in halos) * 1.0000001
    ue = np.concatenate([[0.0], np.geomspace(1e-3, u_out, N_SHELL)])            # shell edges in units of R500
    if not np.any(np.isclose(ue, 0.25)): ue = np.sort(np.concatenate([ue, [0.25]]))
    nsh = len(ue) - 1; R5 = np.array([H["R500"] for H in halos]); R2 = np.array([H["R200"] for H in halos])
    E = ue[None, :] * R5[:, None]                                                 # edges kpc (ns, nsh+1)
    Ein = np.minimum(E, R2[:, None])
    M0 = np.empty((ns, nsh))
    for i, H in enumerate(halos):
        if density is None:
            Mc = H["Menc"](Ein[i]); M0[i] = np.diff(Mc)
        else:
            rr = np.sqrt(np.maximum(E[i, :-1], 1e-12) * E[i, 1:]); rr[0] = 0.5 * E[i, 1]
            M0[i] = density[i](rr) * 4 / 3 * math.pi * (E[i, 1:] ** 3 - E[i, :-1] ** 3)
            M0[i][E[i, :-1] >= R2[i]] = 0.0
    V = 4 / 3 * math.pi * (E[:, 1:] ** 3 - E[:, :-1] ** 3)
    rmid = np.sqrt(np.maximum(E[:, :-1], 1e-30) * E[:, 1:]); rmid[:, 0] = 0.0                # innermost cell represented by r = 0
    geo = (R5[:, None] ** 2 * np.ones_like(rmid)) if geo_hold else np.maximum(R5[:, None] ** 2 - rmid ** 2, 0.0)
    if geo_hold: geo = np.where(rmid < R5[:, None], geo, 0.0)
    in25 = (E[:, 1:] <= 0.25 * R5[:, None] * (1 + 1e-12)); V25 = 4 / 3 * math.pi * (0.25 * R5) ** 3
    def rate(M, tau):
        if GATE_OFF: return -M
        rho = M / V; rb = np.sum(M * in25, axis=1) / V25
        Sig = np.sqrt(geo * rb[:, None] * rho)
        if host_sigma is not None:
            Sig = Sig + np.array([hs(tau) if hs is not None else 0.0 for hs in host_sigma])[:, None]
        x = Sig / SIGMA_GATE; return -M / (1.0 + x * x)
    n = int(round(tau_tot / dtau)); M = M0.copy(); tau = 0.0; snaps = {}
    rec = set() if record_taus is None else {int(round(t / dtau)) for t in record_taus}
    if 0 in rec: snaps[0] = M.copy()
    for k in range(n):
        k1 = rate(M, tau); k2 = rate(M + 0.5 * dtau * k1, tau + 0.5 * dtau); k3 = rate(M + 0.5 * dtau * k2, tau + 0.5 * dtau); k4 = rate(M + dtau * k3, tau + dtau)
        M = M + dtau / 6 * (k1 + 2 * k2 + 2 * k3 + k4); tau += dtau
        if (k + 1) in rec: snaps[k + 1] = M.copy()
    return dict(E=E, M0=M0, M=M, R500=R5, R200=R2, snaps={round(k * dtau, 6): v for k, v in snaps.items()}, ue=ue)

def enclosed_fn(P, i, which="M"):
    """callable r_kpc -> enclosed retained (or initial) component mass of system i (linear in r inside the first edge)."""
    E = P["E"][i]; C = np.concatenate([[0.0], np.cumsum(P[which][i])])
    def f(r):
        r = np.asarray(r, float); out = np.interp(r, E, C)
        return np.where(r > E[-1], C[-1], out)
    return f
def retention(P, i, upto=None):
    """retained / initial component mass of system i, whole halo or inside r = upto (kpc)."""
    if upto is None: return float(P["M"][i].sum() / P["M0"][i].sum())
    return float(enclosed_fn(P, i, "M")(upto) / max(enclosed_fn(P, i, "M0")(upto), 1e-300))

def sigma_profile_fn(P, i, M=None):
    """Sigma(r) of system i for the given shell masses (default final), callable r_kpc -> Msun/kpc^2 (0 beyond R500)."""
    E = P["E"][i]; M = P["M"][i] if M is None else M; V = 4 / 3 * math.pi * (E[1:] ** 3 - E[:-1] ** 3); rho = M / V
    R5 = P["R500"][i]; in25 = E[1:] <= 0.25 * R5 * (1 + 1e-12); rb = M[in25].sum() / (4 / 3 * math.pi * (0.25 * R5) ** 3)
    rmid = np.sqrt(np.maximum(E[:-1], 1e-30) * E[1:])
    def f(r):
        rr = float(r)
        if rr >= R5: return 0.0
        return math.sqrt(max(R5 * R5 - rr * rr, 0.0) * rb * float(np.interp(rr, rmid, rho)))
    return f

# ------------------------------------------------------------------ Sigma_gate derivation check
def sigma_gate_search():
    """products of powers in {-1,-1/2,0,1/2,1} of the outside constants (cgs) with the dimension g cm^-2; report those within 10 %."""
    c = 2.99792458e10; myr = 3.15576e13; gyr = 1e3 * myr
    Q = dict(sigma_m=(1.40, (-1, 2, 0)),                         # cm^2/g : dims (g, cm, s) exponents
             v_med=(0.0632 * c, (0, 1, -1)), Gamma_psi=(4.20 / myr, (0, 0, -1)),
             R_abs=(1.68e-4 * KPC_CM ** 3 / MSUN_G / myr, (-1, 3, -1)), Gamma0=(GAMMA0_GYR / gyr, (0, 0, -1)), c=(c, (0, 1, -1)))
    names = list(Q); pw = [-1, -0.5, 0, 0.5, 1]; hits = []
    for combo in itertools.product(pw, repeat=len(names)):
        dims = [sum(p * Q[n][1][k] for p, n in zip(combo, names)) for k in range(3)]
        if any(abs(d - t) > 1e-9 for d, t in zip(dims, (1, -2, 0))): continue
        val = math.exp(sum(p * math.log(Q[n][0]) for p, n in zip(combo, names)))
        if abs(val / SIGMA_GATE_GCM2 - 1) <= 0.10:
            hits.append(dict(expr=" ".join(f"{n}^{p:g}" for p, n in zip(combo, names) if p != 0), value_gcm2=val, rel=val / SIGMA_GATE_GCM2 - 1))
    hits.sort(key=lambda d: abs(d["rel"]))
    simple = dict(one_over_sigma_m=1 / 1.40, one_over_sigma_m_times_vmed_over_c=0.0632 / 1.40,
                  rho_crit_Gamma_psi_over_R_abs_Msun_kpc3=4.20 / 1.68e-4, decay_length_v_over_Gamma_psi_kpc=0.0632 * c / (4.20 / myr) / KPC_CM)
    return dict(target_gcm2=SIGMA_GATE_GCM2, target_Msun_kpc2=SIGMA_GATE_GCM2 / SIG_UNIT, within_10pct=hits[:20], n_within_10pct=len(hits),
                reproduced=bool(any(abs(hh["rel"]) <= 0.02 for hh in hits)), simple_combinations=simple,
                Gamma0_over_Gamma_psi=(GAMMA0_GYR / 1e3) / 4.20)

# ------------------------------------------------------------------ KA1 / KA2
def known_answers():
    out = {}
    ka1 = {"1.35": reduced(1.35), "1.8": reduced(1.80), "3.2": reduced(3.20)}; ref = {"1.35": 0.028, "1.8": 0.056, "3.2": 0.506}
    fz = frozen_da(1.80)
    ok = abs(ka1["1.35"] - 0.028) <= 1e-3 and abs(ka1["1.8"] - 0.056) <= 1e-3 and abs(ka1["3.2"] - 0.506) <= 1e-3 and abs(fz - 0.347) <= 1e-3
    out["KA1"] = dict(reduced=ka1, frozen_1p80=fz, ref=dict(reduced=ref, frozen_1p80=0.347), pass_=bool(ok))
    # KA2: top-hat sphere with the geometric factor held at R500^2 (A1): central shell == reduced ODE
    rows = {}; ok2 = True; rep = {}
    for x0 in (1.35, 1.80, 3.20):
        R5 = 100.0; rho0 = x0 * SIGMA_GATE / R5                     # Sigma(0) = R500 rho0 -> x0
        H = dict(R500=R5, R200=R5 * 1.2)
        P = peel([H], geo_hold=True, density=[lambda r, rho0=rho0: np.full_like(np.asarray(r, float), rho0)])
        V0 = P["M0"][0]; ret_c = float(P["M"][0][0] / V0[0]); ret_all25 = float(P["M"][0][P["E"][0][1:] <= 25.0 + 1e-9].sum() / V0[P["E"][0][1:] <= 25.0 + 1e-9].sum())
        rows[f"{x0}"] = dict(central=ret_c, inner25=ret_all25, reduced=reduced(x0), dev=abs(ret_c - reduced(x0))); ok2 &= rows[f"{x0}"]["dev"] <= 1e-4
        P2 = peel([H], geo_hold=False, density=[lambda r, rho0=rho0: np.full_like(np.asarray(r, float), rho0)])
        rep[f"{x0}"] = dict(central_true_tophat=float(P2["M"][0][0] / P2["M0"][0][0]), reduced=reduced(x0))
    out["KA2"] = dict(geo_held=rows, true_tophat_reported=rep, pass_=bool(ok2))
    # convergence (A1): halve the step on a cluster-like SIS
    H = halo(1.5e14, 5.41, 0.674, 0.31); a = peel([H]); b = peel([H], dtau=DTAU / 2)
    d = float(np.max(np.abs(np.cumsum(a["M"][0]) - np.cumsum(b["M"][0])) / a["M0"][0].sum()))
    out["convergence"] = dict(max_rel_cum_change=d, pass_=bool(d <= 1e-4))
    return out

if __name__ == "__main__":
    ka = known_answers(); print(json.dumps(ka, indent=1, default=float)); print(json.dumps(sigma_gate_search(), indent=1, default=float))
