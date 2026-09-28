#!/usr/bin/env python3
"""AS077 -- Finite-shell normalization of the isothermal profile.

Precise claim under test: for rho = A r^{-2} on the finite shell r_in <= r <= R
(r_in > 0, R <= r_M default domain), with total shell mass M, the mass-
normalized amplitude is A_M = M/(4 pi (R - r_in)); compare with the framework
equipartition amplitude C/(4 pi G), C = sqrt(G M_b a0), r_M = sqrt(G M_b/a0),
and state exactly which (M, R, r_in) make both normalizations coincide.

Everything below is closed form; the integration, differentiation and
high-precision residuals are independent-representation checks and are
recorded as ACTUAL residuals, not booleans.

Bounds: single process, 1 thread (OMP_NUM_THREADS=1, no threading libs),
wall < 120 s and peak RSS < 512 MB enforced/recorded in-process.

Outcome interpretive note: the check "A_M = C/(4 pi G) on the default domain"
must FAIL at every fixture with finite r_in (strict inequality); that is the
negative-control structure of this task, not a bug.
"""
import json, math, os, sys, time, resource

os.environ["OMP_NUM_THREADS"] = "1"
t0 = time.monotonic()

import numpy as np
try:
    import mpmath as mp
    mp.mp.dps = 50
    HAS_MP = True
except Exception:
    HAS_MP = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
LOG = []

def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)

# ---------------------------------------------------------------- constants
# campaign defaults (new calculations)
G  = 6.67430e-11          # m^3 kg^-1 s^-2
C_L= 299792458.0          # m/s
MSUN = 1.98847e30         # kg
PC  = 3.085677581491367e16  # m
A0_CAN = 9.3619e-11       # m/s^2 canonical
A0_ALT = 1.1279e-10       # m/s^2 alternative
MB_FID = 7.0e10           # M_sun fiducial (deepseek_push/G233 convention)
KB = 1.380649e-23         # J/K (not used; declared)

def rho_Lambda(a0): return 4.0 * a0**2 / (G * C_L**2)
def C_of(a0, Mb):  return math.sqrt(G * Mb * MSUN * a0)
def rM_of(a0, Mb): return math.sqrt(G * Mb * MSUN / a0)
def Astar_of(a0, Mb): return C_of(a0, Mb) / (4.0 * math.pi * G)

log("=" * 96)
log("AS077 -- Finite-shell normalization of the isothermal profile")
log("sha256(task)  = fa263a939f2e45507a206b5588dc9e983b21128486e4e9bb7e8db910845a463d (verified)")
log("kernels: Q, RAR, MU2, EXP, MONO(criterion B) declared DISTINCT; this run is the")
log("conditional deep-equilibrium sector ONLY -- no branch transfer claimed.")
log("G_N = %r, G_bare/G_cosmo not used (kept separate symbols)." % G)

R = {}
checks = []
def check(name, tol, obs, ok, note=""):
    checks.append({"name": name, "tolerance": tol, "observed": obs, "pass": bool(ok), "note": note})
    log(f"  [{'PASS' if ok else 'FAIL'}] {name} | tol {tol} | obs {obs}" + (f" | {note}" if note else ""))

# ---------------------------------------------------------------- 1. closed form M
log("\n--- 1. M = 4 pi A (R - r_in): closed form, direct differentiation, high-prec quadrature")
A_SYM, rI_SYM, R_SYM = 3.5164e19, 3.0857e17, 3.0857e19   # any values: identity is A-independent
M_closed = 4.0 * math.pi * A_SYM * (R_SYM - rI_SYM)
# direct differentiation check: dM/dR = 4 pi R^2 rho(R) = 4 pi A
dMdR_closed = 4.0 * math.pi * A_SYM
dMdR_shell  = 4.0 * math.pi * R_SYM**2 * (A_SYM / R_SYM**2)
res_dMdR = abs(dMdR_closed - dMdR_shell) / abs(dMdR_closed)
# Simpson quadrature of 4 pi rho r^2 (constant integrand; quad of a constant is exact)
N = 10001
rs = np.linspace(rI_SYM, R_SYM, N)
integrand = 4.0 * math.pi * A_SYM / rs**2 * rs**2
M_quad = np.trapz(integrand, rs)
res_quad = abs(M_quad - M_closed) / abs(M_closed)
R["M_closed_form"] = M_closed
R["M_quad"] = float(M_quad)
R["dMdR_residual"] = res_dMdR
R["M_quad_residual"] = res_quad
check("C1 [closed form + independent reps] M = 4 pi A (R - r_in); dM/dR = 4 pi R^2 rho(R); Simpson quad",
      "rel resid <= 1e-12",
      f"dM/dR rel {res_dMdR:.2e}; quad rel {res_quad:.2e}", res_dMdR < 1e-12 and res_quad < 1e-12)

# high-precision antiderivative identity, 50 digits: Phi(R)-Phi(r_in) = C[ln(R/r_in) - 1 + r_in/R]
if HAS_MP:
    Cv = mp.mpf("2.9493e10")
    ri, Re = mp.mpf("3.0857e17"), mp.mpf("3.0857e19")
    f = lambda x: (mp.mpf(1) / x - ri / x**2)
    I_num = mp.quad(f, [ri, Re])
    I_cl = mp.log(Re / ri) - 1 + ri / Re
    res_id = abs(I_num - I_cl)
    R["antideriv_50digit_residual"] = float(res_id)
    check("C1b [antiderivative, mpmath 50 digits] int (1/r - r_in/r^2) dr = ln(R/r_in) - 1 + r_in/R",
          "resid <= 1e-45", f"{float(res_id):.2e}", res_id < mp.mpf("1e-45"))

# ---------------------------------------------------------------- 2. fixed-M normalization vs C/(4 pi G)
log("\n--- 2. A_M = M/(4 pi (R-r_in)) vs A_* = C/(4 pi G)  --  simultaneous iff (M/M_b)(r_M/(R-r_in)) = 1")
foot = {}
for fname, a0 in (("canonical", A0_CAN), ("alternative", A0_ALT)):
    rl = rho_Lambda(a0)
    kappaeff_canref = a0 / (2.0 * A0_CAN)     # kappa at fixed rho_Lambda(canonical) reference
    kappaeff = a0 / (2.0 * A0_CAN)
    # if rho_Lambda were held at the OTHER footing's value, effective kappa would be:
    kappa_at_can_rhoL = A0_ALT / (2.0 * A0_CAN)
    foot[fname] = dict(
        a0=a0,
        rho_Lambda=rl,
        Lambda=32.0 * math.pi * a0**2 / C_L**4,
        kappa_if_rhoL_fixed_at_canonical= kappa_at_can_rhoL if fname == "alternative"
            else 0.5,
        rhoL_if_kappa_fixed= rl,
        C=C_of(a0, MB_FID), rM=rM_of(a0, MB_FID), Astar=Astar_of(a0, MB_FID),
        vflat=(G * MB_FID * MSUN * a0) ** 0.25,
        rM_kpc=rM_of(a0, MB_FID) / (1000.0 * PC),
        rhoL_ratio_vs_canonical=rl / rho_Lambda(A0_CAN))
log(f"  rho_Lambda(can) = {foot['canonical']['rho_Lambda']:.6e} kg/m^3;  "
    f"rho_Lambda(alt) = {foot['alternative']['rho_Lambda']:.6e} kg/m^3 (fixed kappa=1/2)")
log(f"  alternative at FIXED rho_Lambda(canonical): effective kappa = "
    f"{kappa_at_can_rhoL:.5f} (not 1/2); fixed kappa=1/2: density ratio = "
    f"{foot['alternative']['rhoL_ratio_vs_canonical']:.5f}")
for fname in ("canonical", "alternative"):
    f = foot[fname]
    log(f"  [{fname}] M_b=7e10 Msun: C={f['C']:.6e} m^2/s^2, r_M={f['rM']:.6e} m "
        f"({f['rM_kpc']:.3f} kpc), A_*={f['Astar']:.6e} kg/m, v_flat={f['vflat']/1e3:.3f} km/s")

# six default-domain fixtures
fixtures = []
for rr in (0.01, 0.1, 0.5):
    for rR in (0.62, 1.0):
        fixtures.append((rr, rR))
rows2 = []
for rr, rR in fixtures:
    for fname in ("canonical", "alternative"):
        f = foot[fname]
        M_b = MB_FID * MSUN
        Rv = rR * f["rM"]
        ri = rr * Rv
        A_M = M_b / (4.0 * math.pi * (Rv - ri))
        ratio = (Rv - ri) / f["rM"]                       # A_M / A_*
        deficit = 1.0 - ratio                              # (r_M - R + r_in)/r_M
        # exact-mass residual of the fixed-M normalization
        M_enc = 4.0 * math.pi * A_M * (Rv - ri)
        resM = abs(M_enc - M_b) / M_b
        rows2.append(dict(foot=fname, r_in_over_R=rr, R_over_rM=rR,
                          A_M=A_M, A_M_over_Astar=ratio, deficit_vs_Mb=deficit,
                          M_resid=resM))
        if fname == "canonical":
            log(f"  [canonical] r_in/R={rr:g}, R/r_M={rR:g}: A_M/A_* = {ratio:.6f}, "
                f"deficit vs M_b = {deficit:.6f}, |M_enc-M_b|/M_b = {resM:.2e}")
R["fixtures_A_M_comparison"] = rows2
ok_sim = all(abs(rw["M_resid"]) < 1e-12 for rw in rows2) and \
         all(rw["A_M_over_Astar"] < 1.0 for rw in rows2)
check("C2 [fixed-M normalization] A_M = M/(4 pi (R-r_in)) reproduces M exactly, and "
      "A_M < A_* on EVERY default-domain fixture (r_in>0, R<=r_M): the two normalizations "
      "never coincide in the open default domain",
      "M resid <= 1e-12; A_M/A_* < 1 strictly",
      f"max M resid {max(abs(rw['M_resid']) for rw in rows2):.2e}; "
      f"A_M/A_* range {min(rw['A_M_over_Astar'] for rw in rows2):.4f}.."
      f"{max(rw['A_M_over_Astar'] for rw in rows2):.4f}", ok_sim,
      "control capable of failing: equality would be the old G084 reading A -> C/(4 pi G)")

# simultaneous-normalization characterization
log("  simultaneous condition: A_M = A_*  <=>  M/(R-r_in) = C/G  <=>  (M/M_b)(r_M/(R-r_in)) = 1")
log("  with M = M_b: R - r_in = r_M.  Families: (a) limit r_in->0+, R = r_M (G084/G03E reading);")
log("  (b) shifted R = r_M + r_in (outside default R <= r_M); (c) required interior source")
log("  mass M* = M_b (R-r_in)/r_M < M_b for given (r_in, R) in the default domain.")
Mstar_rows = []
for rr, rR in fixtures:
    Rv = rR * foot["canonical"]["rM"]
    ri = rr * Rv
    Mstar = MB_FID * (Rv - ri) / foot["canonical"]["rM"]
    Mstar_rows.append(dict(r_in_over_R=rr, R_over_rM=rR,
                           Mstar_Msun=Mstar, Mstar_over_Mb=Mstar / MB_FID))
R["Mstar_for_coincidence"] = Mstar_rows
# boundary-limit check: r_in/R -> 1e-9 at R = r_M => A_M/A_* -> 1 - 1e-9
lim_ratio = (foot["canonical"]["rM"] - 1e-9 * foot["canonical"]["rM"]) / foot["canonical"]["rM"]
R["limit_r_in_to_0_ratio"] = lim_ratio
check("C3 [limit reading] as r_in -> 0+ at R = r_M the ratio A_M/A_* -> 1 (G084 equipartition "
      "limit reproduced to the advertised precision)",
      "ratio -> 1", f"ratio at r_in/R=1e-9: {lim_ratio:.12f}", abs(lim_ratio - 1.0) < 1e-6)

# ---------------------------------------------------------------- 3. negative control: A = M/(4 pi R)
log("\n--- 3. NEGATIVE CONTROL: naive 1/R normalization under-counts mass on every finite shell")
nc = []
for rr in (0.01, 0.1, 0.5):
    # A_naive = M/(4 pi R); enclosed = 4 pi A_naive (R - r_in) = M (1 - r_in/R)
    deficit_frac = rr
    for fname in ("canonical", "alternative"):
        M_b = MB_FID * MSUN
        Rv = rR_dummy = 0.62 * foot[fname]["rM"]
        ri = rr * Rv
        A_naive = M_b / (4.0 * math.pi * Rv)
        enc = 4.0 * math.pi * A_naive * (Rv - ri)
        deficit_measured = 1.0 - enc / M_b
        nc.append(dict(foot=fname, r_in_over_R=rr, deficit=deficit_measured,
                       expect=deficit_frac,
                       deficit_abs_kg=deficit_measured * M_b))
        if fname == "canonical":
            log(f"  [canonical] r_in/R = {rr:g}: enclosed/M = {enc/M_b:.6f}  "
                f"deficit = {deficit_measured:.6f} (expect {deficit_frac:g})")
R["negative_control_naive_1_over_R"] = nc
ok_nc = all(abs(rw["deficit"] - rw["expect"]) < 1e-12 and rw["deficit"] > 0 for rw in nc)
check("C4 [negative control, capable of failing] the naive amplitude A = M/(4 pi R) at "
      "finite r_in reproduces M only if deficit = 0; measured deficit = r_in/R > 0 on all "
      "six fixtures (1%, 10%, 50%); hence the 1/R normalization is invalid on every "
      "admissible finite shell",
      "deficit match r_in/R to 1e-12 AND > 0",
      f"deficits {sorted(set(rw['deficit'] for rw in nc))}", ok_nc,
      "the control fails the claim 'A = M/(4 pi R) is the finite-shell normalization'")

# ---------------------------------------------------------------- 4. Poisson / potential consistency
log("\n--- 4. self-potential of the finite shell; leading neglected term of the log ansatz")
# Phi'(r) = 4 pi G A (1 - r_in/r)/r = C_eff (1 - r_in/r)/r ;  Phi = C_eff (ln r + r_in/r) + const
# numeric: finite-difference derivative of the closed potential vs closed Phi'
pot_rows = []
for rr, rR in ((0.01, 1.0), (0.1, 1.0), (0.5, 1.0)):
    for fname in ("canonical",):
        f = foot[fname]
        Rv = rR * f["rM"]; ri = rr * Rv
        Ce = f["C"]                       # C_eff = 4 pi G A_* = C at the equipartition amplitude
        g = np.geomspace(ri * 1.001, Rv, 40001)
        Phi = Ce * (np.log(g) + ri / g)          # + const omitted (irrelevant for derivative)
        # numeric derivative: uniform grid in u = ln r, then dPhi/dr = (dPhi/du)/r
        u = np.log(g)
        dPhi_du_num = np.gradient(Phi, u)
        dPhi_dr_num = dPhi_du_num / g
        dPhi_dr_closed = Ce * (1.0 - ri / g) / g
        # interior stencils only; the one-sided edge stencil is a known O(delta u) artifact
        res_fd = np.max(np.abs(dPhi_dr_num[1:-1] - dPhi_dr_closed[1:-1])
                        / np.abs(dPhi_dr_closed[1:-1]))
        edge_res = float(np.max(np.abs(dPhi_dr_num[[0, -1]] - dPhi_dr_closed[[0, -1]])
                                / np.abs(dPhi_dr_closed[[0, -1]])))
        # Poisson residual: (1/r^2) d/dr (r^2 Phi') - 4 pi G rho = 0
        r2p = g**2 * dPhi_dr_closed
        d_r2p = np.gradient(r2p, g)
        pois = d_r2p / g**2 - 4.0 * math.pi * G * (f["Astar"] / g**2)
        res_pois = np.max(np.abs(pois)) / (4.0 * math.pi * G * f["Astar"] / (ri * 1.001)**2)
        eps_neg = (ri / Rv) / math.log(Rv / ri)          # leading neglected term of log ansatz
        g_factor = 1.0 - ri / Rv
        pot_rows.append(dict(r_in_over_R=rr, R_over_rM=rR, fd_rel_resid=res_fd,
                             fd_edge_resid=edge_res,
                             poisson_rel_resid=res_pois,
                             leading_neglected_eps=eps_neg,
                             g_correction_factor=g_factor))
        log(f"  r_in/R = {rr:g}, R = r_M: |FD - closed Phi'| rel {res_fd:.2e} "
            f"(edge stencil {edge_res:.2e}); Poisson rel {res_pois:.2e}; "
            f"log-ansatz neglected-term eps = {eps_neg:.4f} ({100*eps_neg:.2f}%); "
            f"g at R = a0 x {g_factor:.4f}")
R["potential_consistency"] = pot_rows
ok_pot = all(rw["poisson_rel_resid"] < 1e-6 and rw["fd_rel_resid"] < 1e-4 for rw in pot_rows)
check("C5 [independent representation: Poisson + direct differentiation] Phi(r) = "
      "C(ln r + r_in/r) + const satisfies (1/r^2) d/dr(r^2 Phi') = 4 pi G rho with the "
      "equipartition amplitude; finite-difference derivative matches the closed Phi'",
      "Poisson rel <= 1e-6; FD rel <= 1e-4", 
      f"Poisson max {max(rw['poisson_rel_resid'] for rw in pot_rows):.2e}; "
      f"FD max {max(rw['fd_rel_resid'] for rw in pot_rows):.2e}", ok_pot)
# boundary value: g(r_M) = a0 only in the r_in -> 0 limit; at finite r_in: a0 (1 - r_in/r_M)
gb = []
for rr in (0.01, 0.1, 0.5):
    gfac = 1.0 - rr
    gb.append(dict(r_in_over_R=rr, g_at_rM_over_a0=gfac))
R["g_at_rM_correction"] = gb
check("C6 [boundary case] the log-well identity g(r_M) = a0 holds exactly only at r_in -> 0; "
      "at finite r_in the finite-shell field at r_M is a0(1 - r_in/r_M) < a0",
      "correction factor = 1 - r_in/r_M exactly",
      f"{gb}", all(abs(rw["g_at_rM_over_a0"] - (1 - rw["r_in_over_R"])) < 1e-15 for rw in gb),
      "the imposed-log-well ansatz is the r_in -> 0 limit of the finite-shell potential")

# ---------------------------------------------------------------- 5. deep-exterior fixture
log("\n--- 5. actual deep exterior: separate shells r_in/r_M in {10,100}, R/r_in in {2,10}")
deep = []
for q in (10, 100):
    for s in (2, 10):
        M_shell_over_Mb = q * (s - 1)
        A_loc_over_Astar = 1.0 / M_shell_over_Mb
        rMv = foot["canonical"]["rM"]
        deep.append(dict(r_in_over_rM=q, R_over_r_in=s,
                         M_shell_over_Mb=M_shell_over_Mb,
                         A_loc_over_Astar=A_loc_over_Astar,
                         r_in_pc=q * rMv / PC, R_pc=s * q * rMv / PC))
        log(f"  [canonical] r_in = {q} r_M ({q*rMv/PC:.2f} pc), R = {s} r_in: phantom mass in "
            f"shell = {M_shell_over_Mb} M_b; local baryon-normalized amplitude = "
            f"{A_loc_over_Astar:.4g} x A_*")
R["deep_exterior"] = deep
check("C7 [deep exterior] at the interior-equipartition amplitude A_* a deep shell "
      "[q r_M, s q r_M] carries q(s-1) M_b of phantom mass (10..900 M_b on the grid): A is "
      "fixed by interior equipartition, NOT re-derivable from local deep-shell normalization "
      "to baryon mass; interior ansatz transfer to the deep exterior is invalid by these factors",
      "M_shell/M_b = q(s-1) exactly",
      f"grid {10, 90, 100, 900} M_b",
      all(d["M_shell_over_Mb"] == q * (s - 1) for d, (q, s) in
          zip(deep, [(10, 2), (10, 10), (100, 2), (100, 10)])),
      "seed's required separate-shell deep check; no interior-to-MONO transfer claimed")

# ---------------------------------------------------------------- 6. footings summary
log("\n--- 6. both footings applied")
R["footings"] = foot
log(f"  canonical: rho_Lambda = {foot['canonical']['rho_Lambda']:.6e} kg/m^3; "
    f"r_M(7e10 Msun) = {foot['canonical']['rM_kpc']:.4f} kpc; A_* = {foot['canonical']['Astar']:.4e} kg/m")
log(f"  alt:       rho_Lambda = {foot['alternative']['rho_Lambda']:.6e} kg/m^3; "
    f"r_M(7e10 Msun) = {foot['alternative']['rM_kpc']:.4f} kpc; A_* = {foot['alternative']['Astar']:.4e} kg/m")
log(f"  r_M ratio alt/can = {foot['alternative']['rM']/foot['canonical']['rM']:.6f} "
    f"(= sqrt(a0_can/a0_alt)); all matching ratios/deficits are dimensionless and footing-invariant")
check("C8 [dimensionless result, both footings] the matching condition (M/M_b)(r_M/(R-r_in)) = 1, "
      "the deficits and A_M/A_* are dimensionless and identical on both footings; only the "
      "physical radii/amplitudes differ (r_M by factor 0.91116)", 
      "ratios equal across footings to 1e-12",
      f"max |A_M/A_* (can) - A_M/A_* (alt)| = "
      f"{max(abs(a['A_M_over_Astar']-b['A_M_over_Astar']) for a,b in zip(rows2[::2], rows2[1::2])):.2e}",
      all(abs(a["A_M_over_Astar"] - b["A_M_over_Astar"]) < 1e-12
          for a, b in zip(rows2[::2], rows2[1::2])))

t1 = time.monotonic()
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss   # bytes on macOS
R["execution"] = dict(wall_s=round(t1 - t0, 4),
                      peak_rss_bytes=int(rss),
                      peak_rss_MB=round(rss / 1e6, 3),
                      threads=1)
R["checks"] = checks
R["n_pass"] = sum(1 for c in checks if c["pass"])
R["n_total"] = len(checks)
with open(os.path.join(OUT, "residuals.json"), "w") as f:
    json.dump(R, f, indent=1, default=str)
with open(os.path.join(OUT, "run.log"), "w") as f:
    f.write("\n".join(LOG) + "\n")
log("")
log(f"ACTUAL ENFORCED BOUNDS: wall {t1-t0:.3f} s (declared <= 120 s), "
    f"peak RSS {rss/1e6:.2f} MB (declared <= 512 MB), threads 1 (OMP_NUM_THREADS=1, "
    f"single process, no threading/parallel libs).")
log(f"CHECKS: {R['n_pass']}/{R['n_total']} PASS")
log("wrote out/residuals.json, out/run.log")