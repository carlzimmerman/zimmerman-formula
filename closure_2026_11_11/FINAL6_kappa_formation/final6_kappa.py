#!/usr/bin/env python3
"""FINAL6 (KAPPA): is kappa an OUTPUT of the formation reading?

Criteria: FROZEN_CRITERIA.md (committed alone, local cbba716d05). TEST lane: adopts nothing.
Run:  python3 final6_kappa.py                 -> final6.out / final6.json
      FINAL6_MUTATE=1 python3 final6_kappa.py -> final6_MUTATE.out / final6_MUTATE.json
Footings never pooled.  kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import time

import mpmath as mp
import sympy as sp

T0 = time.time()
MUT = os.environ.get("FINAL6_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = {}
LINES = []


def say(*parts):
    s = " ".join(str(p) for p in parts)
    LINES.append(s)
    print(s, flush=True)


# ------------------------------------------------------------------ constants / background
G = 6.67430e-11
C = 2.99792458e8
MSUN = 1.98847e30
KPC = 3.0856775814913673e19
MPC = 1000.0 * KPC

H0_KMS = 67.36                       # Planck 2018 TT,TE,EE+lowE+lensing
H0 = H0_KMS * 1.0e3 / MPC            # 1/s
OM, OL, OB = 0.3153, 0.6847, 0.0493
FCDM = 5.3640                        # the record's adopted Omega_c/Omega_b (v2 note)
OC = FCDM * OB                       # -> 0.264438; Omega_m - Omega_b - Omega_c = 1.56e-3 (massive neutrinos)
FB = OB / OM
RHO_CRIT = 3.0 * H0 ** 2 / (8.0 * math.pi * G)
RHO_LAM = OL * RHO_CRIT
RHO_M0 = OM * RHO_CRIT
RHO_B0 = OB * RHO_CRIT
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
X_SHARE = {"canonical": 59.4861, "alt": 59.5029}      # PD1, via FINAL4 (reported, not graded)
M_B_REF = 6.0e10 * MSUN
DELTA_V = 178.0
DELTA_C = 1.686

Z_EQ = (OL / OM) ** (1.0 / 3.0) - 1.0                 # matter--Lambda equality
Z_ACC = (2.0 * OL / OM) ** (1.0 / 3.0) - 1.0            # rho_m = 2 rho_Lambda


def E_of_z(z):
    return math.sqrt(OM * (1.0 + z) ** 3 + OL)


say("FINAL6 (KAPPA): is kappa an OUTPUT of the formation reading?   MUTATE =", MUT)
say("     criteria FROZEN_CRITERIA.md (cbba716d05).  kappa = 1/2 FITTED; not theory closed.  Adopts nothing.")
say()
say("=== BACKGROUND (Planck 2018 TT,TE,EE+lowE+lensing; reported, not graded) ===")
say(f"  H0 = {H0_KMS:.2f} km/s/Mpc = {H0:.6e} 1/s      c H0 = {C*H0:.6e} m/s^2")
say(f"  Omega_m = {OM:.4f}  Omega_Lambda = {OL:.4f}  Omega_b = {OB:.4f}  Omega_c = {OC:.5f}")
say(f"  rho_crit,0 = {RHO_CRIT:.6e} kg/m^3")
say(f"  rho_Lambda  = {RHO_LAM:.6e} kg/m^3      rho_m,0 = {RHO_M0:.6e} kg/m^3")
say(f"  f_cdm = Omega_c/Omega_b = {FCDM:.6f}  (record's adopted 5.3640)     f_b = {FB:.6f}")
say(f"  z(rho_m = rho_Lambda)   = {Z_EQ:.6f}")
say(f"  z(rho_m = 2 rho_Lambda) = {Z_ACC:.6f}")
OUT["background"] = dict(H0=H0, cH0=C * H0, OM=OM, OL=OL, OB=OB, OC=OC, rho_crit=RHO_CRIT,
                         rho_Lam=RHO_LAM, rho_m0=RHO_M0, f_cdm=FCDM, f_b=FB, z_eq=Z_EQ, z_acc=Z_ACC)

# ------------------------------------------------------------------ K1: dimensional closure (exact)
say()
say("=== K1: dimensional closure (sympy, exact) ===")
a, b, g, m = sp.symbols("a b g m")
# columns: G, c, rho, M ;  rows: L, M, T
cols = [sp.Matrix([3, -1, -2]), sp.Matrix([1, 0, -1]), sp.Matrix([-3, 1, 0]), sp.Matrix([0, 1, 0])]
A = sp.Matrix.hstack(*cols)
tgt = sp.Matrix([1, 0, -2])                      # acceleration L T^-2
_A_aug = A.row_join(tgt)
# 3 equations, 4 unknowns: affine line.  Take the g = 0 particular solution by hand and verify.
_part = sp.Matrix([sp.Integer(-1), sp.Integer(4), sp.Integer(0), sp.Integer(-1)])   # G^-1 c^4 rho^0 M^-1
assert list(A * _part) == list(tgt), "particular solution does not satisfy A x = b"
ns = A.nullspace()
# normalise the nullspace direction on its rho-component: expect (3, -6, 1, 2)
_n = ns[0]
_nn = sp.Matrix([sp.simplify(e / _n[2]) for e in _n])
t = sp.symbols("t")
expo = _part + t * _nn                     # (a,b,g,m) = (3t-1, 4-6t, t, 2t-1)
say("  exponent matrix (rows L, M, T; cols G, c, rho, M) =")
say("    " + str(A.tolist()))
say(f"  rank = {A.rank()} of 4 unknowns  -> solution space dimension = {4 - A.rank()}")
say("  particular solution (g = 0)  (a, b, g, m) = " + str(list(_part)) + "   [= c^4 / (G M)]")
say("  nullspace direction (normalised on rho) = " + str(list(_nn))
    + "   [= G^3 rho M^2 / c^6 = (G M sqrt(G rho)/c^3)^2, dimensionless]")
say("  general monomial exponents  (a, b, g, m) = " + str([sp.expand(e) for e in expo]))
sol_half = [sp.simplify(e.subs(t, sp.Rational(1, 2))) for e in expo]
say("  mass-independence (m = 2t - 1 = 0) requires t = 1/2; then (a, b, g, m) = "
    + str(sol_half) + "  -> c^1 G^(1/2) rho^(1/2) M^0 = c sqrt(G rho)")
# every monomial with m != 0 carries M  ->  the mass-free member is unique
m_expr = expo[3]                                        # m(t) = 2t - 1
k1_unique = sp.solve(sp.Eq(m_expr, 0), t) == [sp.Rational(1, 2)]
k1_rank_ok = (A.rank() == 3)
k1_null_ok = (len(ns) == 1) and (list(_nn) == [sp.Integer(3), sp.Integer(-6),
                                               sp.Integer(1), sp.Integer(2)])
k1_half_ok = all(x == y for x, y in zip(sol_half, [sp.Rational(1, 2), sp.Integer(1),
                                                   sp.Rational(1, 2), sp.Integer(0)]))
k1_pass = bool(k1_rank_ok and k1_null_ok and k1_half_ok and k1_unique)
say(f"  rank==3: {k1_rank_ok} | nullspace == (3,-6,1,2): {k1_null_ok} | t=1/2 -> (1/2,1,1/2,0): {k1_half_ok}")
say(f"  m(t) = 0 has the single root t = 1/2 : {k1_unique}")
say(f"  K1 PASS: {k1_pass}")
say("  ---> Q1 (form): universality (no M in a_0) forces a_0 = Phi * c sqrt(G rho_*) UNIQUELY.")
say("       Which rho_* is, and Phi (=kappa) is, are separate questions. K1 does not touch either.")
OUT["K1"] = dict(rank=A.rank(), particular=[str(x) for x in _part],
                nullspace=[str(x) for x in _nn], at_t_half=[str(x) for x in sol_half],
                m_zero_only_at_t_half=bool(k1_unique), PASS=k1_pass)


def rho_ref(a0):
    """the record's own tie at kappa = 1/2:  a0 = (1/2) c sqrt(G rho)  =>  rho = 4 a0^2/(c^2 G)."""
    return 4.0 * a0 ** 2 / (C ** 2 * G)


def H_of_rho(rho):
    return math.sqrt(8.0 * math.pi * G * rho / 3.0)


# ------------------------------------------------------------------ K2: what the two footings are
say()
say("=== K2: what the two footings are (kappa, both readings, both footings) ===")
K2 = {}
say("  Reading A -- the record's tie: rho_ref = 4 a0^2/(c^2 G) is the cosmic density the footing uses.")
say("  Reading B -- the fitted a0 taken as data: kappa = a0_fit / (c sqrt(G rho_cosm)).")
say()
hdr = f"  {'footing':10s} {'a0 [m/s^2]':>13s} {'rho_ref':>12s} {'rho_ref/rho_Lam':>16s} {'rho_ref/rho_crit':>17s} {'Z=cH/a0':>9s}"
say(hdr)
for f, a0 in FOOT.items():
    rr = rho_ref(a0)
    Hl = H_of_rho(rr)
    Z = C * Hl / a0
    rho_cosm = RHO_LAM if f == "canonical" else RHO_CRIT      # canonical = rho_Lambda, alt = rho_crit
    row = dict(a0=a0, rho_ref=rr, ratio_Lam=rr / RHO_LAM, ratio_crit=rr / RHO_CRIT, H=Hl, Z=Z,
               rho_cosm=rho_cosm, ratio_cosm=rr / rho_cosm)
    row["kappa_A"] = a0 / (C * math.sqrt(G * rr))
    row["kappa_B"] = a0 / (C * math.sqrt(G * rho_cosm))
    K2[f] = row
    say(f"  {f:10s} {a0:13.5e} {rr:12.5e} {rr/RHO_LAM:16.6f} {rr/RHO_CRIT:17.6f} {Z:9.5f}")
say()
say("  kappa under each reading (kappa = 1/2 is the record's adopted value):")
say(f"    {'footing':10s} {'A: vs rho_ref':>16s} {'B: vs rho_cosm':>17s}")
for f, r in K2.items():
    say(f"    {f:10s} {r['kappa_A']:16.6f} {r['kappa_B']:17.6f}")
dA = abs(K2["canonical"]["kappa_A"] - 0.5)
dA2 = abs(K2["alt"]["kappa_A"] - 0.5)
dfoot = abs(K2["canonical"]["kappa_A"] - K2["alt"]["kappa_A"])
k2_pass = bool(max(dA, dA2) <= 0.005 and dfoot <= 0.001)
say()
say(f"  |kappa_A - 1/2| = {dA:.2e} (can), {dA2:.2e} (alt)   -> both <= 5e-3: {max(dA, dA2) <= 0.005}")
say(f"  |kappa_A(can) - kappa_A(alt)| = {dfoot:.2e}                   -> <= 1e-3: {dfoot <= 0.001}")
say(f"  K2 PASS: {k2_pass}")
if k2_pass:
    say("  ---> The two fitted a0 values encode ONE posited kappa = 1/2 under two density")
    say("       conventions (canonical = rho_Lambda, alt = rho_crit). Neither footing is a")
    say("       MEASUREMENT of kappa; the 20 % spread is the rho convention, not kappa.")
OUT["K2"] = {k: {kk: vv for kk, vv in v.items()} for k, v in K2.items()}
OUT["K2"]["_pass"] = k2_pass
OUT["K2"]["_dA"] = [dA, dA2, dfoot]

# ------------------------------------------------------------------ K3: the pure-number requirement
say()
say("=== K3: kappa = Phi(dimensionless formation data) -- the frozen scan ===")
say("  Under F2+F3, kappa must be a pure number built from the dimensionless formation data.")
say("  Frozen list of closed forms in {delta_c, Delta_v, f_cdm, f_b, OL/OM, X, pi}. None is")
say("  DERIVED from any equation of F; each is an asserted functional form. Printed to show that")
say("  no natural form lands on 1/2 within the 5 % band.")
pi = math.pi
scan = [
    ("1/delta_c", 1.0 / DELTA_C),
    ("1/(2 delta_c)", 0.5 / DELTA_C),
    ("delta_c/pi", DELTA_C / pi),
    ("f_b", FB),
    ("sqrt(f_b)", math.sqrt(FB)),
    ("1/f_cdm", 1.0 / FCDM),
    ("1/sqrt(f_cdm)", 1.0 / math.sqrt(FCDM)),
    ("(Delta_v/18)^(1/3)", (DELTA_V / 18.0) ** (1.0 / 3.0)),
    ("delta_c^2/(2 pi^2)", DELTA_C ** 2 / (2 * pi ** 2)),
    ("3/(4 pi)", 3.0 / (4 * pi)),
    ("3/5  (uniform virial)", 0.6),
    ("1/(2 pi)", 1.0 / (2 * pi)),
    ("sqrt(3/(8 pi))", math.sqrt(3.0 / (8 * pi))),
    ("sqrt(3/32)", math.sqrt(3.0 / 32.0)),
    ("X^(-1/2) (can)", X_SHARE["canonical"] ** -0.5),
    ("X^(-1/2) delta_c/2 (can)", X_SHARE["canonical"] ** -0.5 * DELTA_C / 2),
    ("(OL/OM)/4", (OL / OM) / 4.0),
    ("f_cdm * f_b", FCDM * FB),
    ("1/(2 sqrt 2)  (accel-epoch)", 1.0 / (2 * math.sqrt(2))),
    ("1/2  (the claim itself)", 0.5),
]
say(f"    {'form':32s} {'value':>12s} {'dev from 1/2':>14s}  in 5% band")
hits = []
for name, val in scan:
    dev = val / 0.5 - 1.0
    inband = abs(dev) <= 0.025
    if inband:
        hits.append(name)
    say(f"    {name:32s} {val:12.6f} {dev:+14.4f}  {inband}")
say()
say(f"  forms inside the 5% band: {hits}")
say("  K3 verdict: no route PASSES. A band hit is a numerological identity, not a derivation -- there")
say("  is no equation in F that evaluates Phi. K3 PASS requires DERIVED, and none of these is derived.")
OUT["K3"] = dict(scan=[(n, v) for n, v in scan], band_hits=hits, PASS_routes=[])

# ------------------------------------------------------------------ K4: the matching condition (kappa <-> z_f)
say()
say("=== K4: the matching condition -- the one quantitative output of the reading ===")
say("  F2 with rho_* = rho_m(z_f):   a_0 = kappa * c * sqrt(G rho_m(z_f)),   rho_m(z) = rho_m,0 (1+z)^3")
say("  => required freeze-out redshift per footing (kappa = 1/2):")
say("       1 + z_f = ( rho_ref / (Omega_m rho_crit,0) )^{1/3}")
say("  and the inverse trade:")
say("       kappa(z_f) = a_0 / (c sqrt(G rho_m(z_f))) = (1/2) * ( rho_ref/rho_m(z_f) )^{1/2}")
K4 = {}
say()
say(f"    {'footing':10s} {'rho_ref/rho_m0':>16s} {'z_f required':>14s}   {'z(matter=Lam)':>15s}")
for f, a0 in FOOT.items():
    rr = rho_ref(a0)
    ratio = rr / RHO_M0
    zf = ratio ** (1.0 / 3.0) - 1.0
    K4[f] = dict(rho_ref=rr, ratio=ratio, z_f=zf)
    say(f"    {f:10s} {ratio:16.6f} {zf:14.6f}   {Z_EQ:15.6f}")
say()
say("  The trade, canonical footing, kappa -> required z_f (and beta = rho_m(z_f)/rho_Lambda):")
say(f"    {'kappa':>8s} {'rho_* [kg/m^3]':>16s} {'beta=rho_*/rho_Lam':>19s} {'z_f':>10s}  verdict")
for kap in (0.25, 1.0 / 3.0, 0.5, 0.7071, 1.0, 2.0):
    a0 = FOOT["canonical"]
    rs = a0 ** 2 / (kap ** 2 * C ** 2 * G)
    beta = rs / RHO_LAM
    zf = beta ** (1.0 / 3.0) - 1.0
    verd = "past: allowed" if zf >= 0 else "FUTURE: excluded"
    say(f"    {kap:8.4f} {rs:16.5e} {beta:19.5f} {zf:10.4f}  {verd}")
say()
# sensitivity: beta = 2 (acceleration onset) vs beta = 1 (equality)
for f, a0 in FOOT.items():
    kap1 = 0.5 / math.sqrt(1.0)
    kap2 = 0.5 / math.sqrt(2.0)
    shift = math.log10(kap2 / kap1)
    say(f"  [{f}] freeze-out defined at rho_m = rho_Lambda  -> kappa = {kap1:.5f}")
    say(f"  [{f}] freeze-out defined at rho_m = 2 rho_Lambda -> kappa = {kap2:.5f}")
    say(f"  [{f}] shift = {shift:.4f} dex   vs footing spread 0.0411 dex  ->  exceeds by {abs(shift)/0.0411:.2f}x")
k4_shift = math.log10((0.5 / math.sqrt(2.0)) / 0.5)
k4_cons = all(0.0 <= K4[f]["z_f"] <= 3.0 for f in K4)
k4_derivation = abs(k4_shift) <= 0.0411
say()
say(f"  consistency (0 <= z_f <= 3) on both footings: {k4_cons}   [z_f = "
    + ", ".join(f"{K4[f]['z_f']:.4f}" for f in K4) + "]")
say(f"  K4 consistency PASS: {k4_cons}")
say(f"  K4 as a DERIVATION: {'PASS' if k4_derivation else 'FAIL'}  (sensitivity {abs(k4_shift):.4f} dex "
    f"vs allowed 0.0411 dex)")
say("  ---> kappa = 1/(2 sqrt(beta)): kappa = 1/2 is EXACTLY the statement beta = 1, i.e. freezing at")
say("       matter--Lambda equality. That is a restatement of the fitted value, not a derivation of it:")
say("       the shutdown epoch is asymptotic, so beta is not fixed by the dynamics.")
OUT["K4"] = {k: v for k, v in K4.items()}
OUT["K4"].update(_consistency=bool(k4_cons), _shift_dex=k4_shift, _derivation=bool(k4_derivation))

# ------------------------------------------------------------------ K5: universality refutes the halo-scale routes
say()
say("=== K5: the two routes that set the scale from the halo itself, graded on universality ===")
say("  R-A (internal-acceleration route). BTFR v_f^4 = G M_b a_0 with M_b = f_b M_vir, plus virial v_f^2 = G M_vir/R_vir:")
say("        a_0 = f_b^(-1) * G M_vir / R_vir^2")
say("      with M_vir = (4 pi/3) Delta_v rho_crit(z) R_vir^3  =>  a_0 = f_b^(-1) (4pi/3)^(2/3) Delta_v^(2/3) G M_vir^(1/3) rho_crit^(2/3)")
say("  R-B (catchment-saturation route). Settled region exhausts the catchment, R_set = R_c with M_b = (4 pi/3) R_c^3 rho_b:")
say("        a_0 = f_cdm^2 (4 pi/3)^(2/3) G M_b^(1/3) rho_b^(2/3)")
say("  Both have the Buckingham form G rho^(2/3) M^(1/3)  (p = 1/6):  MASS DEPENDENT (a_0 ∝ M^(1/3)).")
MASSES = [1e8, 1e10, 6e10, 1e12]
K5 = {}
for f, a0 in FOOT.items():
    say()
    say(f"  [{f}]  a0_fit = {a0:.5e} m/s^2")
    say(f"      {'M_b [Msun]':>12s} {'R-A a0':>12s} {'R-A log10(a0/a0fit)':>22s} {'R-B a0':>12s} {'R-B log10(a0/a0fit)':>22s}")
    ra_vals, rb_vals, ra_log, rb_log = [], [], [], []
    for mb in MASSES:
        M = mb * MSUN
        a_ra = (1.0 / FB) * (4 * math.pi / 3.0) ** (2.0 / 3.0) * DELTA_V ** (2.0 / 3.0) * G * M ** (1.0 / 3.0) * RHO_CRIT ** (2.0 / 3.0)
        a_rb = FCDM ** 2 * (4 * math.pi / 3.0) ** (2.0 / 3.0) * G * M ** (1.0 / 3.0) * RHO_B0 ** (2.0 / 3.0)
        ra_vals.append(a_ra)
        rb_vals.append(a_rb)
        ra_log.append(math.log10(a_ra / a0))
        rb_log.append(math.log10(a_rb / a0))
        say(f"      {mb:12.1e} {a_ra:12.4e} {math.log10(a_ra/a0):+22.4f} {a_rb:12.4e} {math.log10(a_rb/a0):+22.4f}")
    ra_spread = max(ra_log) - min(ra_log)
    rb_spread = max(rb_log) - min(rb_log)
    K5[f] = dict(ra=ra_vals, rb=rb_vals, ra_log=ra_log, rb_log=rb_log,
                 ra_spread=ra_spread, rb_spread=rb_spread,
                 ra_ref=ra_vals[2] / a0, rb_ref=rb_vals[2] / a0)
    say(f"      spread over 1e8 -> 1e12 Msun (4 decades):  R-A = {ra_spread:.3f} dex,  R-B = {rb_spread:.3f} dex")
    say(f"      at M_b = 6e10 Msun:  R-A a0/a0_fit = {ra_vals[2]/a0:.4e} ({math.log10(ra_vals[2]/a0):+.3f} dex),"
        f"  R-B a0/a0_fit = {rb_vals[2]/a0:.4e} ({math.log10(rb_vals[2]/a0):+.3f} dex)")
spreads = [K5[f]["ra_spread"] for f in K5] + [K5[f]["rb_spread"] for f in K5]
offs = [abs(math.log10(K5[f]["ra_ref"])) for f in K5] + [abs(math.log10(K5[f]["rb_ref"])) for f in K5]
k5_refuted = bool(max(spreads) > 0.5 or max(offs) > 0.5)
say()
say(f"  worst predicted spread = {max(spreads):.3f} dex   (threshold 0.5) -> FAIL universality: {max(spreads) > 0.5}")
say(f"  worst absolute miss    = {max(offs):.3f} dex   (threshold 0.5) -> FAIL size:         {max(offs) > 0.5}")
say(f"  K5 verdict: {'REFUTED' if k5_refuted else 'not refuted by these criteria'}")
say("  ---> Any closing condition that takes the scale from the halo's own M and R makes a_0 ∝ M^(1/3):")
say("       a factor 10^1.33 across four decades of galaxy mass, against an observed non-universality")
say("       of 0.041 dex. Formation-per-galaxy is excluded; only a GLOBAL shutdown epoch survives, and")
say("       that is exactly the statement rho_* = rho_Lambda.")
OUT["K5"] = {f: {k: v for k, v in K5[f].items()} for f in K5}
OUT["K5"].update(_refuted=k5_refuted, _spread=max(spreads), _miss=max(offs))

# ------------------------------------------------------------------ K6: the cosmic-budget closure is vacuous
say()
say("=== K6: the cosmic-budget closure (reported, VACUOUS) ===")
Mtot, V, rhob = sp.symbols("M_tot V rho_b", positive=True)
f = sp.symbols("f", positive=True)                     # f := Omega_c/Omega_b by definition
expr = sp.simplify(f * rhob * V - f * rhob * V)
say("  Integrated over a volume V:  total phantom = f * rho_b * V  and  f := Omega_c/Omega_b (a definition).")
say("  The cosmic supply is  Omega_c rho_crit V = f * (Omega_b / Omega_m) * Omega_m rho_crit V = f * rho_b V.")
say(f"  Identity: total phantom - supply = {expr}   for every f, rho_b, V -- it contains no kappa.")
say("  K6: VACUOUS. Not used for a label.")
OUT["K6"] = dict(vacuous=True)

# ------------------------------------------------------------------ K7: the discriminator the reading does supply
say()
say("=== K7: the epoch-evolution discriminator (reported, not graded) ===")
say("  Under F2 a law frozen at the event inherits the time dependence of the density the event imprints:")
say("    rho_* = rho_Lambda (constant)  ->  a_0 independent of epoch;")
say("    rho_* = rho_crit(z)            ->  a_0(z)/a_0(0) = E(z).")
say()
say(f"    {'z':>6s} {'E(z)':>10s} {'a0(z)/a0(0) CAN':>16s} {'a0(z)/a0(0) ALT':>16s}")
for z in (0.3, 0.5, 1.0, 2.0, 6.0):
    Ez = E_of_z(z)
    say(f"    {z:6.2f} {Ez:10.5f} {1.0:16.5f} {Ez:16.5f}")
say()
say("  K7: the formation reading turns the two footing *conventions* into two *hypotheses* about a_0(z).")
say("  FINAL2's bound on any a_0(z) is the arbiter and FINAL2's own verdict stands; not re-graded here.")
OUT["K7"] = dict(E={str(z): E_of_z(z) for z in (0.3, 0.5, 1.0, 2.0, 6.0)})

# ------------------------------------------------------------------ known answers
say()
say("=== KNOWN ANSWERS ===")
Z_EXACT = math.sqrt(32 * math.pi / 3)
KA = {}
for f, a0 in FOOT.items():
    rr = rho_ref(a0)
    Z = C * H_of_rho(rr) / a0
    rL, rC = rr / RHO_LAM, rr / RHO_CRIT
    Rset = (1.0 + X_SHARE[f]) * math.sqrt(G * M_B_REF / a0)
    KA[f] = dict(Z=Z, dZ=abs(Z - Z_EXACT), rL=rL, rC=rC, Rset_kpc=Rset / KPC,
                 Rset_over_rM=1.0 + X_SHARE[f])
    say(f"  [{f}] Z = {Z:.6f}  vs sqrt(32 pi/3) = {Z_EXACT:.6f}  -> |dZ| = {abs(Z-Z_EXACT):.2e}")
    say(f"          rho_ref/rho_Lambda = {rL:.6f}   rho_ref/rho_crit,0 = {rC:.6f}")
    say(f"          R_set = (1+X) r_M = {Rset/KPC:.4f} kpc at M_b = 6e10 Msun   (R_set/r_M = {1.0 + X_SHARE[f]:.6f})")
    say(f"          g_N at R_set = a_0/(1+X)^2 = {a0/(1.0+X_SHARE[f])**2:.5e} m/s^2   (deep-regime consistency)")
ka1 = all(KA[f]["dZ"] <= 1e-4 for f in KA)
# KA-2 is footing-paired: canonical vs rho_Lambda, alt vs rho_crit.
ka2 = bool(abs(KA["canonical"]["rL"] - 1) <= 2e-3 and abs(KA["alt"]["rC"] - 1) <= 2e-3)
say()
say(f"  KA-1 (Z = sqrt(32 pi/3), tolerance 1e-4, both footings): {'PASS' if ka1 else 'FAIL'}")
say(f"  KA-2 (canonical = rho_Lambda, alt = rho_crit, tolerance 2e-3): {'PASS' if ka2 else 'FAIL'}")
say("  KA-3 (R_set = (1+X) r_M, PD1's X): printed above; FINAL4 states no numeric r_ta to compare, so")
say("       this item is verified structurally (R_set/r_M = 1+X exactly, and g_N(R_set) = a_0/(1+X)^2)")
say("       instead of against an external number. Recorded as a deviation from the criteria text.")
OUT["known_answers"] = {f: KA[f] for f in KA}
OUT["known_answers"].update(KA1=bool(ka1), KA2=bool(ka2), KA3="structural-only (no external r_ta number)")

# ------------------------------------------------------------------ mutate
say()
say("=== MUTATE ===")
MU = {}
if MUT:
    # MU1: kappa = 1 instead of 1/2 in the matching condition
    for f, a0 in FOOT.items():
        rs1 = a0 ** 2 / (1.0 ** 2 * C ** 2 * G)
        z1 = (rs1 / RHO_M0) ** (1.0 / 3.0) - 1.0
        MU[("MU1", f)] = z1
        say(f"  MU1 [{f}] kappa = 1  -> required rho_* = {rs1:.5e}  -> z_f = {z1:+.4f}"
            f"   (must be < -0.05): {z1 < -0.05}")
    # MU2: canonical a0 scored against rho_crit instead of rho_Lambda
    k2 = FOOT["canonical"] / (C * math.sqrt(G * RHO_CRIT))
    MU[("MU2", "kappa_crit")] = k2
    say(f"  MU2 [canonical vs rho_crit] kappa = {k2:.6f} -> |kappa - 1/2| = {abs(k2-0.5):.4f}"
        f"   (must be > 0.05): {abs(k2-0.5) > 0.05}")
    # MU3: drop universality, allow p = 1/6
    lo, hi = 1e8 * MSUN, 1e12 * MSUN
    fac = (hi / lo) ** (1.0 / 3.0)
    MU[("MU3", "factor")] = fac
    say(f"  MU3 [p = 1/6] a_0(1e12)/a_0(1e8) = {fac:.3f} = {math.log10(fac):.3f} dex"
        f"   (must be > 0.5 dex): {math.log10(fac) > 0.5}")
    MU["_pass"] = bool(all(z < -0.05 for k, z in MU.items() if isinstance(k, tuple) and k[0] == "MU1")
                       and abs(k2 - 0.5) > 0.05 and math.log10(fac) > 0.5)
    say(f"  MUTATE all bite: {MU['_pass']}")
else:
    say("  (run with FINAL6_MUTATE=1)")
OUT["mutate"] = {f"{k[0]}_{k[1]}": v for k, v in MU.items() if isinstance(k, tuple)}

# ------------------------------------------------------------------ labels
say()
say("=== LABELS ===")
k4_derivation = bool(OUT["K4"]["_derivation"])
say(f"  Q1 (form):   OUTPUT.  Universality forces a_0 = Phi * c sqrt(G rho_*) (K1, exact), and the")
say( "               requirement that the frozen normalisation not drift forces rho_* = rho_Lambda:")
say( "               the formation reading SELECTS THE CANONICAL FOOTING over the alt footing.")
say(f"  Q2 (coeff):  NOT DERIVED.  kappa = Phi is a pure number (K1) that no equation of F evaluates")
say(f"               (K3: no route passes), and the concrete closing conditions are either circular")
say(f"               (kappa -> z_f trade, K4) or excluded (halo-scale routes, K5: {max(spreads):.2f} dex spread).")
say()
label = "KAPPA NOT DERIVED (FITTED)"
if k4_derivation:
    label = "KAPPA DERIVED"
extra = []
if k5_refuted:
    extra.append("FORMATION REFUTED (per-galaxy)")
if not (ka1 and ka2):
    label = "OPEN"
    extra.append("known answer failed")
say(f"  LANE LABEL: {label}" + ("  + " + "; ".join(extra) if extra else ""))
say("  kappa = 1/2 FITTED; not theory closed.  Adopts nothing.")
OUT["label"] = label
OUT["label_extra"] = extra

with open(os.path.join(HERE, "final6" + ("_MUTATE" if MUT else "") + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "final6" + ("_MUTATE" if MUT else "") + ".out"), "w") as fh:
    fh.write("\n".join(LINES) + "\n")
say()
say(f"  runtime {time.time()-T0:.1f} s")
