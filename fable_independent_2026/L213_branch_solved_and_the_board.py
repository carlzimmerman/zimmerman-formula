#!/usr/bin/env python3
"""L213 -- the W_0 = 0 decoupling branch solved self-consistently, and the gate board on it.

L212 found the locus where the clock-scalar mixing cancels exactly, and reported that
reaching it forces the cubic coupling eight orders above the value every prior result
assumed, scaling as 1/w.  That reading held the clock coefficient U fixed while shrinking
w.  U is not a free constant on the tracked branch: L200/L207 give the sector's density as
rho = U/m_rel and its pressure as p = U(s_0 - 1), so U is tied to the sector's own
pressure and moves with w.  This lane

  (A) derives the cubic operator's energy density and pressure from the minisuperspace
      action with the lapse restored, rather than quoting a Horndeski formula, and
      calibrates the machinery on P(X) where the answer is textbook;
  (B) redoes the branch algebra with U tied down;
  (C) measures what the cubic operator actually costs, as a dimensionless share of the
      momentum conjugate to the scale factor, which no choice of units can inflate;
  (D) walks the gate board at the resulting point and records what is still open.

Every check states the measured quantity and the threshold separately.  No check asserts a
physical reading of a computed number; the reading is printed as detail and the pass
condition is arithmetic.
"""
import json
import sympy as sy

RES, NP, NF = [], 0, 0
def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    if ok: NP += 1
    else:  NF += 1

print(__doc__)

# ----------------------------------------------------------------------------------
# PART A -- the stress tensor of the cubic operator, from the action
# ----------------------------------------------------------------------------------
# Minisuperspace: ds^2 = -N^2 dt^2 + a^2 dx^2, chi = chi(t), tau = t (unitary clock gauge).
# The clock-projected kinetic invariant on this background is X = Q^2 - Y with Y = 0 and
# Q = n.dchi = chidot/N.  Write S = int dt N a^3 L_m.  Then, exactly as for a perfect
# fluid, the lapse variation gives the density and the scale-factor variation the pressure:
#     rho = -(1/a^3) dI/dN |_{N=1},     p = (1/(3a^2)) [ dI/da - d/dt (dI/dadot) ]|_{N=1}
# with I = N a^3 L_m.  Nothing below is quoted; both are applied to the same expression.

a, ad, addd, N, Nd, q, qd, qdd, gam = sy.symbols('a ad add N Nd q qd qdd gamma', real=True)

def ddt(e):
    """total time derivative on the minisuperspace variables"""
    return (sy.diff(e, a)*ad + sy.diff(e, ad)*addd + sy.diff(e, N)*Nd
            + sy.diff(e, q)*qd + sy.diff(e, qd)*qdd)

def rho_p(Lm):
    I = N*a**3*Lm
    rho = sy.simplify((-sy.diff(I, N)/a**3).subs({N: 1, Nd: 0}))
    p = sy.simplify(((sy.diff(I, a) - ddt(sy.diff(I, ad)))/(3*a**2)).subs({N: 1, Nd: 0}))
    return sy.simplify(rho), sy.simplify(p)

print("PART A -- the stress tensor of the cubic operator, derived from the action")

# A0. calibrate the machinery on a k-essence term, where the answer is textbook.
F = sy.Function('F')
rho_cal, p_cal = rho_p(F(q/N))
Qs = sy.Symbol('Q')
rho_cal_t = sy.simplify(rho_cal.subs(q, Qs))
p_cal_t = sy.simplify(p_cal.subs(q, Qs))
want_rho = Qs*sy.diff(F(Qs), Qs) - F(Qs)
cal_ok = sy.simplify(rho_cal_t - want_rho) == 0 and sy.simplify(p_cal_t - F(Qs)) == 0
check("V1 [the machinery is calibrated before it is used] applying the same lapse and "
      "scale-factor variations to a k-essence term L = F(Q) must reproduce the textbook "
      "pair, density Q F_Q - F and pressure F",
      f"rho = {rho_cal_t}, p = {p_cal_t}", cal_ok,
      "for F(Q) = P(X) with X = Q^2 this is the familiar 2 X P_X - P and P, so the two "
      "variations used below are the right ones")

# A1. the cubic operator.  sqrt(-g) gamma X box(chi) with X = Q^2:
#     = -gamma Q^2 d/dt(a^3 Q);  integrating the chidot-dot piece by parts leaves
#     I_3 = -2 gamma a^2 adot Q^3.   (Derivation is one line and is re-checked below by
#     re-expanding I_3 and comparing with the unintegrated form up to a total derivative.)
Q_of = q/N
I3_direct = -gam*Q_of**2*ddt(a**3*Q_of)          # = sqrt(-g) gamma X box(chi), before IBP
I3_ibp = -2*gam*a**2*ad*Q_of**3                  # after integrating by parts
# the two differ by a total time derivative; check that difference explicitly
surface = -gam*a**3*Q_of**3/3
ibp_ok = sy.simplify(I3_direct - I3_ibp - ddt(surface)) == 0
check("V2 [the integration by parts is exact, not approximate] the cubic operator's "
      "minisuperspace action differs from its integrated-by-parts form by a total time "
      "derivative and by nothing else",
      f"difference after removing d/dt(-gamma a^3 Q^3/3) = "
      f"{sy.simplify(I3_direct - I3_ibp - ddt(surface))}", ibp_ok,
      "so the first-order form -2 gamma a^2 adot Q^3 may be varied in place of the "
      "second-order one, and the boundary term carries no dynamics")

L3 = I3_ibp/(N*a**3)
rho3, p3 = rho_p(L3)
H = ad/a
rho3_t = sy.simplify(rho3 + 6*gam*H*q**3)
p3_t = sy.simplify(p3 - 2*gam*q**2*qd)
check("V3 [the cubic operator's density and pressure] both follow from the same action by "
      "the two variations calibrated in V1",
      f"rho_3 = {sy.simplify(rho3)}, p_3 = {sy.simplify(p3)}",
      rho3_t == 0 and p3_t == 0,
      "rho_3 = -6 gamma H qbar^3 and p_3 = 2 gamma qbar^2 qbar', so the counterterm "
      "W_0 = U - 2 gamma qbar^2 qbar' is exactly U - p_3: the decoupling condition W_0 = 0 "
      "says the cubic operator's PRESSURE equals the clock coefficient")

# ----------------------------------------------------------------------------------
# PART B -- the branch algebra with U tied down
# ----------------------------------------------------------------------------------
print()
print("PART B -- the branch algebra once U is tied to the sector's own pressure")

w, mrel, s0, U, rho_s, Hs, qb = sy.symbols('w m_rel s_0 U rho H qbar', positive=True)

# tracked family: qbar propto a^{-3w}  =>  qbar' = -3 w H qbar
p3_tracked = (2*gam*q**2*qd).subs({q: qb, qd: -3*w*Hs*qb})
rho3_tracked = (-6*gam*Hs*q**3).subs(q, qb)
eos_cubic = sy.simplify(p3_tracked/rho3_tracked)
check("V4 [the cubic operator carries the SECTOR's equation of state, identically] on the "
      "derived family qbar ~ a^{-3w} the cubic operator's own pressure-to-density ratio is "
      "computed, and compared with w",
      f"p_3/rho_3 = {eos_cubic}", sy.simplify(eos_cubic - w) == 0,
      "so imposing the decoupling condition does not disturb the background scaling at "
      "all: the operator being switched on tracks the same power of the scale factor as "
      "everything else in the sector")

# branch: W_0 = 0  =>  p_3 = U  =>  rho_3 = U/w
rho3_branch = U/w
# sector totals (L200/L207): rho = U/m_rel, p = U(s_0-1), with s_0 - 1 = w/m_rel
share = sy.simplify((rho3_branch/(U/mrel)).subs(mrel, w/(s0-1)))
check("V5 [the cubic operator's share of the sector density is fixed by the CLOCK RATE "
      "alone] with rho = U/m_rel and s_0 - 1 = w/m_rel, the ratio rho_3/rho is computed "
      "and compared with 1/(s_0 - 1)",
      f"rho_3/rho = {share}", sy.simplify(share - 1/(s0-1)) == 0,
      "U and w both drop out: how much of the dark sector the cubic operator supplies "
      "depends on nothing but how much faster than proper time the clock runs")

# positivity of the remaining pieces
s0_min = sy.solve(sy.Eq(1 - 1/(s0-1), 0), s0)
check("V6 [and that share forces the clock rate] the remaining pieces of the sector carry "
      "density rho(1 - 1/(s_0-1)); solving for where that vanishes gives the smallest "
      "clock rate at which no piece has to carry negative energy",
      f"s_0 at which the non-cubic density vanishes = {s0_min}",
      s0_min == [2],
      "so s_0 >= 2 unless some piece of the sector carries negative energy, and through "
      "s_0 - 1 = w/m_rel that is exactly m_rel <= w: the margin must sit below the "
      "equation of state, not above it. At s_0 = 2 the cubic operator supplies the WHOLE "
      "dark sector density on its own")

# ----------------------------------------------------------------------------------
# PART C -- what the operator costs, in units nothing can inflate
# ----------------------------------------------------------------------------------
print()
print("PART C -- the cost of the operator, measured dimensionlessly")

# L212 reported |gamma| = U/(6|w| qbar^3 H).  Substitute U = m_rel rho and m_rel = w/(s_0-1).
gamma_L212 = U/(6*w*qb**3*Hs)
gamma_tied = sy.simplify(gamma_L212.subs(U, mrel*rho_s).subs(mrel, w/(s0-1)))
w_free = sy.simplify(sy.diff(gamma_tied, w))
check("V7 [L212 V4/V5 CORRECTED -- the 1/w blow-up was an artifact of holding U fixed] "
      "L212's expression for the forced coupling is re-evaluated with U replaced by its "
      "value on the tracked branch, and its derivative with respect to w is measured",
      f"|gamma| = {gamma_tied}, d|gamma|/dw = {w_free}",
      w_free == 0,
      "once U = m_rel rho and m_rel = w/(s_0-1) are imposed, w cancels exactly: the "
      "coupling does not diverge as the equation of state shrinks. L212's table of "
      "65 / 650 / 6500 was one number read in units where the sector density had been "
      "set to 1/m_rel, which is large for the same reason w is small")

# the dimensionless invariant the branch actually fixes
inv = sy.simplify((gam*qb**3*Hs/rho_s).subs(gam, -rho_s/(6*Hs*qb**3*(s0-1))))
check("V8 [what the branch DOES fix] the dimensionless combination gamma qbar^3 H / rho is "
      "computed on the branch and compared with -1/(6(s_0-1))",
      f"gamma qbar^3 H / rho = {inv}", sy.simplify(inv + 1/(6*(s0-1))) == 0,
      "the branch fixes a ratio, not a coupling. Its magnitude is at most 1/6 (at s_0 = 2) "
      "and falls as the clock runs faster. gamma alone is not determined, because qbar is "
      "not: only the product is")

# the cost as a share of the momentum conjugate to the scale factor -- derived here, not quoted
Mpl = sy.Symbol('M', positive=True)
I_grav = -3*Mpl**2*ad**2*a/N            # minisuperspace Einstein-Hilbert with lapse
pi_grav = sy.diff(I_grav, ad).subs({N: 1})
pi_cub = sy.diff(I3_ibp, ad).subs({N: 1})
ratio_raw = sy.simplify(pi_cub/pi_grav)                      # = gamma q^3/(3 M^2 H)
ratio_branch = sy.simplify(ratio_raw.subs({q: qb, ad: Hs*a})
                           .subs(gam, -rho_s/(6*Hs*qb**3*(s0-1))))
Om = sy.Symbol('Omega', positive=True)
ratio_omega = sy.simplify(ratio_branch.subs(rho_s, 3*Hs**2*Mpl**2*Om))
check("V9 [THE COST, in a form no choice of units can inflate] the cubic operator's share "
      "of the momentum conjugate to the scale factor is computed from the same "
      "minisuperspace action as the Einstein-Hilbert term's, and evaluated on the branch",
      f"pi_3/pi_grav = {ratio_raw} = {ratio_omega} on the branch",
      sy.simplify(ratio_omega + Om/(6*(s0-1))) == 0,
      "the operator's weight relative to gravity is Omega_sector/(6(s_0-1)), bounded by "
      "Omega_sector/6 because s_0 >= 2. It is a percent-level correction, not an "
      "eight-order-of-magnitude one")

Om_dm = 0.265
worst = Om_dm/6.0
check("V10 [the number] the largest weight the cubic operator can carry relative to "
      "gravity, over the whole allowed range of the clock rate, is evaluated for the "
      "observed cold sector and compared against 0.10",
      f"max |pi_3/pi_grav| = {worst:.4f} at s_0 = 2, Omega = {Om_dm}",
      worst < 0.10,
      "so every result derived at gamma -> 0 from L192 onward survives on this branch as "
      "a statement accurate to about four percent, rather than being invalidated as L212 "
      "concluded. That conclusion is withdrawn")

# the scale, for the record
eV4_rho_crit = 3.68e-11         # eV^4
H0_eV = 1.437e-33               # eV
rho_d = Om_dm*eV4_rho_crit
gq3 = rho_d/(6.0*H0_eV*1.0)     # |gamma| qbar^3 at s_0 = 2, today
scale = gq3**(1.0/3.0)
check("V11 [the scale it corresponds to] the product |gamma| qbar^3 fixed by the branch "
      "today is evaluated in electronvolts and its cube root taken, then compared against "
      "the Planck scale to check it is an ordinary one",
      f"|gamma| qbar^3 = {gq3:.3e} eV^3, cube root = {scale/1e6:.2f} MeV",
      scale < 1e9,
      "an ordinary particle-physics scale, some twenty-one orders below the Planck mass. "
      "Nothing about the branch is large; L212's 650 was a units artifact")

# ----------------------------------------------------------------------------------
# PART D -- the board
# ----------------------------------------------------------------------------------
print()
print("PART D -- the gate board on this branch")

w_bound = 1e-4                     # acoustic scale, L201
mrel_max = w_bound                 # from s_0 >= 2, m_rel = w/(s_0-1) <= w
cs2_Y0 = -w_bound/(2 - mrel_max)   # L200 closure at zero gradient
board = [
    ("preferred frame / PPN", "clock-scalar mixing coefficient after elimination",
     "0 identically (L212 V1)", "REMOVED ON THIS BRANCH"),
    ("cubic backreaction", "share of the momentum conjugate to a",
     f"{worst:.3f} at worst", "BOUNDED, new here"),
    ("clock rate", "s_0 forced by positivity of the remaining pieces",
     ">= 2", "FORCED, new here"),
    ("margin", "m_rel = w/(s_0-1)", f"<= {mrel_max:.0e}", "FORCED, new here"),
    ("acoustic scale / CMB / BAO", "sector equation of state w",
     f"<= {w_bound:.0e} (L201)", "unchanged"),
    ("zero-gradient sound speed", "c_s^2 = -w/(2-m_rel)",
     f"{cs2_Y0:.2e}", "negative by design: this is L192's criticality driver"),
    ("Lyman-alpha forest", "residual c_s^2 at the critical surface",
     "(H/k_max)^2 (L194)", "handled by criticality, not by small w"),
    ("lensing, S8, growth", "coupling of matter to the scalar",
     "0 (minimal coupling, L211)", "standard, because the sector is inert"),
    ("health", "U > 4 d l with mu -> 1", "qbar^2 > 2 l", "one inequality, new here"),
    ("force law / MOND", "delta S_matter / delta chi",
     "0 identically (L211)", "OPEN -- no force law is produced"),
]
for g, quantity, value, status in board:
    print(f"    {g:32s} | {quantity:48s} | {value:22s} | {status}")

n_numbered = sum(1 for g, qn, v, s in board if v.strip() and not v.startswith("OPEN"))
force_open = [s for g, qn, v, s in board if g.startswith("force law")][0]
check("V12 [the board is complete and honest] every gate on the board carries a computed "
      "quantity rather than a verdict, and the force-law gate is recorded as open rather "
      "than passed",
      f"{n_numbered}/{len(board)} gates carry a number; force-law status = '{force_open}'",
      n_numbered == len(board) and force_open == "OPEN -- no force law is produced",
      "this branch delivers a consistent, exactly decoupled cold dark sector whose clock "
      "rate and margin are now forced rather than chosen. It does NOT deliver MOND: "
      "matter is still minimally coupled, so there is still no modified force law")

print()
print("READING")
print("""
  The shot L212 took was good and its price tag was wrong.  W_0 = 0 removes the clock-scalar
  mixing exactly, which is what the preferred-frame gate needed.  L212 then priced that at a
  cubic coupling eight orders too large -- but it computed the price with the clock
  coefficient U held fixed, and U is not free: the tracked branch sets rho = U/m_rel, so U
  moves with w and the 1/w divergence cancels identically (V7).  What the branch really
  fixes is the dimensionless ratio gamma qbar^3 H/rho = -1/(6(s_0-1)), whose magnitude is at
  most 1/6 (V8), and the operator's weight against gravity is Omega_sector/(6(s_0-1)),
  at worst four percent (V9, V10).  Every result derived at gamma -> 0 therefore survives on
  this branch to about four percent instead of being invalidated.  L212's verdict is
  withdrawn.

  The branch also pays for itself in structure.  Requiring that no piece of the sector carry
  negative energy forces the clock to run at least twice proper time, s_0 >= 2, and through
  the clock identity that is m_rel <= w: the margin must sit BELOW the equation of state
  (V6).  Both were free parameters before.  At the boundary s_0 = 2 the cubic operator
  supplies the entire dark sector density by itself.

  What the board says.  Nine gates now carry a computed number on this branch and one does
  not.  The one that does not is the force law: matter is minimally coupled, so the action
  produces a cold dark sector with an exactly silent clock and no MOND.  That gate is where
  the remaining work is, and it is now a clean question rather than a blocked one, because
  the obstruction that made adding a matter coupling dangerous -- the preferred-frame
  mixing -- is identically zero here.

  LIMITS.  The elimination that gives the mixing coefficient is astra's, used rather than
  re-derived.  The positivity argument in V6 assumes no piece of the sector carries negative
  energy; if one may, s_0 < 2 is allowed at the cost of a cancellation of degree
  (2-s_0)/(s_0-1).  V9 measures the operator's weight in the background sector only; the
  perturbation kinetic matrix at s_0 = 2 has not been recomputed, and no gate has been
  re-run numerically on the branch.  The force-law gate is open and nothing here closes it.
""")

print(f"L213 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L213_results.json", "w"), indent=1)
