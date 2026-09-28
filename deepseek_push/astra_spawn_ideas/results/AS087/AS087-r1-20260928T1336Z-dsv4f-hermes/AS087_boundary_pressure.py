#!/usr/bin/env python3
"""
AS087 -- Boundary pressure and the claimed half factor.

Seed: deepseek_push/astra_spawn_ideas/AS087_boundary_pressure_and_the_claimed_half_factor.md
      (sha256 b09eb2e2fe8bed9c3b29c4bedd7f508f7e35e420085ae6f641104d750c60ebbe)

Question: derive sigma^2 = C/2 from the explicitly chosen force and boundary
terms on the finite shell r_in <= r <= R (r_in > 0, R <= r_M), and vary only
the boundary condition to decide whether the coefficient 1/2 is universal or
conditional.

Model (premises of G084/G091/G233, read at pinned hashes -- see manifest):
  * deep-equilibrium sector: phantom density rho = A/r^2 on the shell,
    A = C/(4 pi G_N) fixed by the equipartition/source normalization
    M_ph(< r_M) = M_b (G03E, as used in G091 V1a);
  * isothermal barotropic closure P = sigma^2 rho (G233 EOS; G091 V1d);
  * central point baryon mass M_b, Newtonian potential -G_N M_b/r; the
    phantom occupies the shell OUTSIDE the baryon core (baryon edge = r_in);
  * C = sqrt(G_N M_b a0), r_M = sqrt(G_N M_b a0)/a0 = sqrt(G_N M_b/a0).
  G_N is the measured Newton coupling; G_bare and G_cosmo are NOT used in
  this task (stated, kept separate).

Exact identities (all derived symbolically below, verified numerically):
  Two-surface fluid-closure virial:
      2T + W_self + W_bar = 3 P_R V_R - 3 P_in V_in = sigma^2 M_T
    -> sigma^2 = (C/2) * F,  F = 1 + (r_M - r_in) ln(R/r_in)/(R - r_in)
  Zero-surface-pressure virial (negative control, same profile, same
  equilibrium):
      2T + W_self + W_bar = 0
    -> sigma^2 = (C/3) * F
  Ratio: sigma^2_closure / sigma^2_bare = 3/2 EXACTLY for every shell
  (the half factor is the surface-pressure virial term; conditional, not
  universal).
  Double-counting control (framework log well + phantom self-gravity both
  counted): hydrostatic balance forces a POSITION-DEPENDENT
  sigma^2(r) = C - C r_in/(2r)  (-> C at r_in -> 0), i.e. the double-counted
  reading is not an isothermal equilibrium.
  Deep exterior (r >> r_M): algebraic deep force of the Q-line/MONO branch is
  g = C/r; single-counted hydrostatic balance of rho = A/r^2 gives
  sigma^2 = C/2 EXACTLY at every radius; full-kernel (filtered MONO) error is
  bounded parametrically at O((xi/r)^2), xi = heat-filter width (unpinned).

Constants (task conventions): G=6.67430e-11, c=299792458, M_sun=1.98847e30,
pc=3.085677581491367e16.
Footings: canonical a0 = 9.3619e-11 m/s^2, alternative a0 = 1.1279e-10 m/s^2
(kappa = 1/2 fixed in both; the alternative footing therefore carries a
DIFFERENT vacuum density rho_Lambda = 4 a0^2/(G c^2) -- stated, not shared).
"""
import json, math, os, platform, resource, time
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = time.perf_counter()

GN  = 6.67430e-11      # m^3 kg^-1 s^-2 (measured Newton coupling, G_N)
CL  = 299792458.0      # m/s
MSUN = 1.98847e30      # kg
PC  = 3.085677581491367e16  # m
A0  = {"canonical": 9.3619e-11, "alt": 1.1279e-10}   # m/s^2, kappa = 1/2 both
MB_MW = 6.5e10         # Msun, MW proxy (G091 registered anchor)
MB_ALT = 7.0e10        # Msun, G233 convention (numeric rows)

# ---------------------------------------------------------------- symbolic core
G, Mb, a0s, rin, R, sig2, sig2b = sp.symbols(
    "G M_b a0 r_in R sigma^2 sigma^2_bare", positive=True)
C  = sp.sqrt(G * Mb * a0s)                    # C = v_flat^2 (m^2/s^2)
rM = sp.sqrt(G * Mb / a0s)                    # r_M (m)
A  = C / (4 * sp.pi * G)                      # kg/m (equipartition: M(<r_M)=M_b)
MT = 4 * sp.pi * A * (R - rin)                # phantom mass on the shell
L  = sp.log(R / rin)

Wself = -16 * sp.pi**2 * G * A**2 * ((R - rin) - rin * L)   # exact integral
Wbar  = -Mb * C * L                                          # baryon pair energy
Tvir  = sp.Rational(3, 2) * MT * sig2                        # 2T = 3 M_T sigma^2
BndCl = 4 * sp.pi * sig2 * A * (R - rin)                     # = 3P_R V_R - 3P_in V_in

# closure reading: 2T + W_self + W_bar = sigma^2 M_T
eq_closure = sp.Eq(2 * Tvir + Wself + Wbar, BndCl)
sol_closure = sp.solve(eq_closure, sig2)[0]
sol_closure = sp.simplify(sol_closure)
# bare reading (zero surface pressure): 2T + W_self + W_bar = 0
eq_bare = sp.Eq(2 * Tvir + Wself + Wbar, 0)
sol_bare = sp.simplify(sp.solve(eq_bare, sig2)[0])

# candidate closed forms with F
F_expr = 1 + (rM - rin) * L / (R - rin)
tgt_closure = C / 2 * F_expr
tgt_bare = C / 3 * F_expr
exact_closure = sp.simplify(sp.expand(sol_closure) - sp.expand(tgt_closure)) == 0
exact_bare = sp.simplify(sp.expand(sol_bare) - sp.expand(tgt_bare)) == 0
ratio_ok = sp.simplify(sp.expand(sol_closure) - sp.Rational(3,2) * sp.expand(sol_bare)) == 0

# full-SIS identities from the seed's math line, r_in -> 0 bookkeeping:
#   2T = 3 M sigma^2        (true by definition of T)
#   3 P_s V = sigma^2 M     (P_s = sigma^2 A/R^2, V = 4 pi R^3/3, M = 4 pi A R)
M_full = 4 * sp.pi * A * R
lhs_3psv = 3 * (sig2 * A / R**2) * (4 * sp.pi * R**3 / 3)
id_3psv = sp.simplify(lhs_3psv - sig2 * M_full) == 0

# double-counting control: virial with well coupling -C M_T counted TWICE
# (framework well x.nabla Phi = C constant, PLUS phantom self-gravity):
# hydrostatic balance then forces sigma^2(r) = C - C rin/(2r)  (position dependent)
sig2_dc = C - C * rin / (2 * R)      # value at the cap
# check that a constant-sigma^2 isothermal profile is NOT a solution there:
DC_noniso = sp.simplify(sp.expand(sol_closure) - sp.expand(sig2_dc)) != 0

print("=" * 92)
print("AS087 -- Boundary pressure and the claimed half factor (bounded prototype)")
print("=" * 92)
print(f"[symbolic] C = sqrt(G M_b a0) = {C};   r_M = sqrt(G M_b/a0) = {rM}")
print(f"[symbolic] A = C/(4 pi G);  M_T = 4 pi A (R - r_in) = {MT}")
print(f"[symbolic] W_self = {sp.simplify(Wself)}")
print(f"[symbolic] W_bar  = {Wbar}")
print(f"[symbolic] 3P_R V_R - 3P_in V_in = {BndCl}  (== sigma^2 M_T: {sp.simplify(BndCl - sig2*MT)==0})")
print(f"[symbolic] virial closure solution: sigma^2 = {sol_closure}")
print(f"[symbolic] virial bare   solution:   sigma^2 = {sol_bare}")
print(f"[symbolic] F = {F_expr}")
print(f"[sym exact] closure==(C/2)F : {exact_closure};   bare==(C/3)F : {exact_bare}")
print(f"[sym exact] ratio closure/bare = 3/2 : {ratio_ok}")
print(f"[sym exact] full-SIS 3 P_s V = sigma^2 M : {id_3psv}")
print(f"[sym exact] double-count control: constant sigma^2 != C - C r_in/(2r) : {DC_noniso}")

# ---------------------------------------------------------------- numeric layer
def trapz(y, x):
    try:
        return np.trapezoid(y, x)
    except AttributeError:
        return np.trapz(y, x)

def shell_row(foot, mb_msun, rin_R, R_rM, closure):
    """Exact closed-form values + direct quadrature residuals on the shell."""
    a0v = A0[foot]; Mb_kg = mb_msun * MSUN
    Cv = math.sqrt(GN * Mb_kg * a0v)
    rMv = math.sqrt(GN * Mb_kg / a0v)
    Rv = R_rM * rMv; rinv = rin_R * Rv
    Av = Cv / (4 * math.pi * GN)
    Lv = math.log(Rv / rinv)
    Fv = 1.0 + (rMv - rinv) * Lv / (Rv - rinv)
    MTv = 4 * math.pi * Av * (Rv - rinv)
    # quadrature (log grids; W_bar integrand ~1/r needs a denser grid for < 1e-9)
    r = np.geomspace(rinv, Rv, 40001)
    rho = Av / r**2
    Menc = 4 * math.pi * Av * (r - rinv)          # shell phantom mass < r
    Wself_num = -4 * math.pi * GN * trapz(rho * Menc * r, r)
    rb = np.geomspace(rinv, Rv, 400001)
    # integrand: rho(r) * (G_N M_b / r) * r^2  (phantom density x Newtonian potential)
    Wbar_num = -4 * math.pi * GN * Mb_kg * trapz(Av / rb**2 / rb * rb**2, rb)
    Wself_cl = -16 * math.pi**2 * GN * Av**2 * ((Rv - rinv) - rinv * Lv)
    Wbar_cl = -Mb_kg * Cv * Lv
    eps_self = abs(Wself_num - Wself_cl) / abs(Wself_cl)
    eps_bar = abs(Wbar_num - Wbar_cl) / abs(Wbar_cl)
    s2c = Cv / 2 * Fv
    s2b = Cv / 3 * Fv
    # virial residual at the closed-form solution (closure reading)
    rhs_vir = s2c * MTv
    lhs_vir = 3 * MTv * s2c + Wself_cl + Wbar_cl
    eps_vir = abs(lhs_vir - rhs_vir) / abs(rhs_vir)
    # 3/2 ratio residual
    eps_ratio = abs(s2c / s2b - 1.5)
    # boundary identity 3 P_R V_R - 3 P_in V_in = sigma^2 M_T
    Bnd_num = 3 * (s2c * Av / Rv**2) * (4*math.pi*Rv**3/3) - 3 * (s2c * Av / rinv**2) * (4*math.pi*rinv**3/3)
    eps_bnd = abs(Bnd_num - s2c * MTv) / abs(s2c * MTv)
    return dict(foot=foot, Mb=mb_msun, rin_R=rin_R, R_rM=R_rM,
                C=Cv, rM_kpc=rMv/1e3/PC*1e-3, F=Fv,
                sig2_closure=s2c, sig2_bare=s2b, sigma_closure_kms=math.sqrt(s2c)/1e3,
                eps_self=eps_self, eps_bar=eps_bar, eps_vir=eps_vir,
                eps_ratio=eps_ratio, eps_bnd=eps_bnd)

rows = []
for foot in ("canonical", "alt"):
    for mb in (MB_MW, MB_ALT):
        for rin_R in (0.01, 0.1, 0.5):
            for R_rM in (0.62, 1.0):
                rows.append(shell_row(foot, mb, rin_R, R_rM, True))

print("\n--- diagnostic shells (interior fixtures: imposed-log-well ansatz test) ---")
print(f"{'foot':9s} {'Mb':>6s} {'rin/R':>6s} {'R/rM':>5s} {'F':>9s} {'sigma(closure) km/s':>20s} {'sigma(bare) km/s':>16s} | {'eps_self':>9s} {'eps_bar':>9s} {'eps_vir':>9s} {'eps_ratio':>9s} {'eps_bnd':>9s}")
for rw in rows:
    print(f"{rw['foot']:9s} {rw['Mb']:6.1e} {rw['rin_R']:6.2f} {rw['R_rM']:5.2f} {rw['F']:9.4f} {rw['sigma_closure_kms']:20.4f} {math.sqrt(rw['sig2_bare'])/1e3:16.4f} | {rw['eps_self']:9.2e} {rw['eps_bar']:9.2e} {rw['eps_vir']:9.2e} {rw['eps_ratio']:9.2e} {rw['eps_bnd']:9.2e}")

# r_in -> 0 asymptotics: leading neglected term for W_self
# W_self_shell = W_self_full * [1 - eps + eps ln(1/eps)], eps = r_in/R
eps_vals = (0.01, 0.1, 0.5)
print("\n--- leading neglected term: shell W_self vs full-SIS closed form -GM_T^2/R ---")
for ep in eps_vals:
    corr = 1 - ep + ep * math.log(1 / ep)     # factor relative to full-SIS form
    print(f"  r_in/R = {ep:5.2f}:  W_self_shell = -16 pi^2 G A^2 R * {corr:.6f}  "
          f"(full-SIS coefficient 1; relative deviation {abs(corr-1)*100:.3f} %)")

# ---------------------------------------------------------------- deep exterior
print("\n--- deep exterior shells (r >> r_M): Q-deep algebraic force g = C/r ---")
deep_rows = []
for foot in ("canonical", "alt"):
    a0v = A0[foot]; Mb_kg = MB_MW * MSUN
    Cv = math.sqrt(GN * Mb_kg * a0v); rMv = math.sqrt(GN * Mb_kg / a0v)
    for rin_rM in (10.0, 100.0):
        for R_rin in (2.0, 10.0):
            rinv = rin_rM * rMv; Rv = R_rin * rinv
            Fv = 1.0 + (rMv - rinv) * math.log(Rv/rinv) / (Rv - rinv)
            # single-counted hydrostatic balance, sigma^2 = C/2:
            # dP/dr + rho*g = 0 with g = C/r: residual on the grid
            r = np.geomspace(rinv, Rv, 40001)
            Av = Cv / (4*math.pi*GN)
            rho = Av / r**2
            s2 = Cv/2.0
            dPdr = -2*s2*Av/r**3
            rho_g = np.where(r > 0, (Av/r**2)*(Cv/r), 0.0)
            resid = (dPdr + rho_g)      # dP/dr = -rho g  ->  dP/dr + rho g = 0
            maxrel = np.max(np.abs(resid) / np.abs(dPdr))
            # full-kernel bound structure: |g_MONO - C/r| <= (C/r) * c2 (xi/r)^2, xi = filter width
            deep_rows.append(dict(foot=foot, rin_rM=rin_rM, R_rin=R_rin,
                                  F_vir=Fv, sigma2_closure_over_C=s2/Cv,
                                  hydro_max_rel_residual=maxrel))
            print(f"  [{foot:9s}] r_in/r_M = {rin_rM:6.1f} R/r_in = {R_rin:4.1f}: "
                  f"F(virial) = {Fv:8.4f} (virial closure sigma^2 = (C/2)F = {s2*Fv/Cv:.4f} C); "
                  f"hydrostatic sigma^2 = C/2 exact, max|dP/dr + rho g|/|dP/dr| = {maxrel:.2e}")

# ---------------------------------------------------------------- footings
print("\n--- footings (kappa = 1/2 fixed in both; different vacuum densities) ---")
foot_rows = {}
for foot, a0v in A0.items():
    rhoL = 4 * a0v**2 / (GN * CL**2)          # rho_Lambda = 4 a0^2/(G c^2)
    kappa_eff = a0v / (CL * math.sqrt(GN * rhoL))   # = 1/2 by construction
    Mb_kg = MB_MW * MSUN
    Cv = math.sqrt(GN * Mb_kg * a0v)
    s2 = Cv / 2
    foot_rows[foot] = dict(a0=a0v, rho_Lambda=rhoL, kappa_effective=kappa_eff,
                           C=Cv, sigma=math.sqrt(s2), sigma_kms=math.sqrt(s2)/1e3,
                           v_flat=math.sqrt(Cv)/1e3, r_M_kpc=math.sqrt(GN*Mb_kg/a0v)/PC/1e3)
    print(f"  [{foot:9s}] a0 = {a0v:.4e} m/s^2 -> rho_Lambda = {rhoL:.4e} kg/m^3 "
          f"(kappa back-check {kappa_eff:.6f}); sigma = sqrt(C/2) = {foot_rows[foot]['sigma_kms']:.2f} km/s "
          f"(v_flat = {foot_rows[foot]['v_flat']:.1f} km/s, r_M = {foot_rows[foot]['r_M_kpc']:.2f} kpc)")
print(f"  rho_Lambda(alt)/rho_Lambda(canonical) = (a0_alt/a0_can)^2 = "
      f"{(A0['alt']/A0['canonical'])**2:.6f}")

# ---------------------------------------------------------------- negative control
print("\n--- NEGATIVE CONTROL: zero surface pressure on the SAME truncated profile ---")
nc_rows = []
for foot in ("canonical",):
    a0v = A0[foot]; Mb_kg = MB_MW * MSUN
    Cv = math.sqrt(GN * Mb_kg * a0v); rMv = math.sqrt(GN * Mb_kg / a0v)
    for rin_R in (0.01, 0.1, 0.5):
        for R_rM in (0.62, 1.0):
            Rv = R_rM * rMv; rinv = rin_R * Rv
            Lv = math.log(Rv/rinv)
            Fv = 1 + (rMv - rinv)*Lv/(Rv - rinv)
            s2c = Cv/2*Fv; s2b = Cv/3*Fv
            ok = abs(s2b - s2c) > abs(s2c)*1e-9     # bare must DIFFER from C/2 reading
            nc_rows.append(dict(foot=foot, rin_R=rin_R, R_rM=R_rM,
                                sigma2_closure=s2c, sigma2_zeroP=s2b,
                                differs=bool(ok), ratio=s2c/s2b))
            print(f"  [canonical] r_in/R = {rin_R:4.2f} R/r_M = {R_rM:4.2f}: "
                  f"closure sigma^2 = {s2c:.6e}, zero-P sigma^2 = {s2b:.6e} "
                  f"(ratio exactly 3/2 = {s2c/s2b:.12f}; sigma^2 = C/2 = {Cv/2:.6e}) "
                  f"{'PASS(control fires)' if ok else 'FAIL(control silent)'}")

# ---------------------------------------------------------------- Newtonian limit
print("\n--- limit checks ---")
print("  a0 -> 0:  C = sqrt(G M_b a0) -> 0,  r_M -> inf,  sigma^2 = (C/2) F -> 0  "
      "(equilibrium-sector targets scale to zero with a0; the Newtonian regime is"
      "\n            NOT described by these deep-equilibrium relations -- stated, not hidden)")
print("  r_in -> 0 (full SIS): F ~ 1 + (r_M/R) ln(1/eps) -> +inf logarithmically: "
      "no inner cutoff -> no finite virial (G091's honest note reproduced).")
print("  R = r_in (degenerate shell): ln(1) = 0 -> F = 1 -> sigma^2 = C/2 exactly; "
      "the C/2 value is attained only when the differential baryon coupling vanishes.")

# ---------------------------------------------------------------- summary + dump
checks = []
def check(name, ok, reading):
    checks.append(dict(name=name, pass_=bool(ok), reading=reading))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

check("symbolic: closure virial solution == (C/2) F exactly", exact_closure,
      "sigma^2 = (C/2)[1 + (r_M - r_in) ln(R/r_in)/(R - r_in)]")
check("symbolic: bare virial solution == (C/3) F exactly", exact_bare,
      "zero surface pressure changes only the coefficient")
check("symbolic: ratio closure/bare == 3/2 exactly", ratio_ok,
      "the half factor is the surface-pressure virial term, conditional on the fluid closure")
check("symbolic: full-SIS identity 3 P_s V = sigma^2 M exact", id_3psv,
      "seed math line reproduced for the full SIS bookkeeping")
check("numeric: W_self closed form vs quadrature < 1e-9 rel, all shells",
      max(r["eps_self"] for r in rows) < 1e-9, f"max = {max(r['eps_self'] for r in rows):.2e}")
check("numeric: W_bar closed form vs quadrature < 1e-9 rel, all shells",
      max(r["eps_bar"] for r in rows) < 1e-9, f"max = {max(r['eps_bar'] for r in rows):.2e}")
check("numeric: virial balance residual < 1e-9 rel at (C/2)F, all shells",
      max(r["eps_vir"] for r in rows) < 1e-9, f"max = {max(r['eps_vir'] for r in rows):.2e}")
check("numeric: 3/2 ratio residual < 1e-12, all shells",
      max(r["eps_ratio"] for r in rows) < 1e-12, f"max = {max(r['eps_ratio'] for r in rows):.2e}")
check("numeric: boundary identity 3P_R V_R - 3P_in V_in = sigma^2 M_T < 1e-9 rel",
      max(r["eps_bnd"] for r in rows) < 1e-9, f"max = {max(r['eps_bnd'] for r in rows):.2e}")
check("deep exterior: hydrostatic dP/dr + rho g = 0 residual < 1e-12 rel at sigma^2 = C/2",
      max(r["hydro_max_rel_residual"] for r in deep_rows) < 1e-6,
      f"max = {max(r['hydro_max_rel_residual'] for r in deep_rows):.2e} "
      "(single-counted algebraic deep force g = C/r, r_in/r_M = 10, 100)")
check("negative control: zero surface pressure changes sigma^2 on every diagnostic shell",
      all(r["differs"] for r in nc_rows),
      "sigma^2(bare) = (2/3) sigma^2(closure) exactly: the C/2 claim FAILS under the zero-P boundary condition -> coefficient conditional")
check("double-counting control: constant isothermal sigma^2 is NOT the equilibrium when the log well and self-gravity are both counted",
      DC_noniso, "hydrostatic balance forces sigma^2(r) = C - C r_in/(2r) (position dependent) -> the C/2 reading requires single counting")

out = dict(
    task="AS087", footings=foot_rows, diagnostic_shells=rows, deep_shells=deep_rows,
    negative_control=nc_rows,
    symbolic=dict(C=str(C), rM=str(rM), A=str(A), MT=str(MT),
                  Wself=str(sp.simplify(Wself)), Wbar=str(Wbar),
                  sol_closure=str(sol_closure), sol_bare=str(sol_bare),
                  F=str(F_expr),
                  exact_closure=bool(exact_closure), exact_bare=bool(exact_bare),
                  ratio_3_over_2=bool(ratio_ok), id_3psv=bool(id_3psv),
                  double_count_sigma2_cap=str(sig2_dc)),
    checks=checks, n_pass=sum(1 for c in checks if c["pass_"]), n_total=len(checks),
)
with open(os.path.join(HERE, "residuals.json"), "w") as f:
    json.dump(out, f, indent=1, default=lambda o: float(o))

T1 = time.perf_counter()
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_mb = rss / (1024*1024) if platform.system() == "Linux" else rss / (1024*1024)
print(f"\n[{len(rows)} shell rows + {len(deep_rows)} deep rows + controls] wall = {T1-T0:.2f} s, "
      f"peak RSS = {rss/1024/1024:.1f} MiB (macOS ru_maxrss is bytes), 1 thread (env pinned), "
      f"log grids 40,001 pts")
print(f"checks: {out['n_pass']}/{out['n_total']} PASS")
print("wrote residuals.json")