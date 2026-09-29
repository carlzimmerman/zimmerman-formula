#!/usr/bin/env python3
"""J3 -- do the standard emergent-photon constructions SELECT the ratio Lambda/mu?  (surjectivity / 'trading' test)

Pre-registration: J_PREREGISTRATION.md (H3).  Induced law used (J1, one loop): 1/alpha_IR = (N_eff/3 pi) ln(Lambda^2/m^2),  m = the charged fermion's IR mass.

Constructions and the microscopic dimensionless coupling that fixes m/Lambda:
  (C-b) NJL/Bjorken compositeness, 4-D Euclidean cutoff gap equation  1/g = 1 - r ln(1 + 1/r),  r = m^2/Lambda^2, g = G N Lambda^2/(4 pi^2)-type coupling.
        Critical coupling g_c = 1; g -> 1+ gives r -> 0.  h := 1 - 1/g = r ln(1 + 1/r).
  (C-c) BCS-type gap, T=0:  1/lambda = asinh(Lambda/Delta)  ->  Lambda/Delta = sinh(1/lambda); m ~ Delta.
  (C-a) Fermi point (3He-A): ratio E_UV/E_IR of the linear spectrum -- no equation; a material number (recalled illustration only, not scored).
  (C-d) compact-U(1) lattice (string-net / quantum spin ice): alpha tunable 0..alpha_c; numbers read from arXiv:2009.04499 and recalled beta_c (report only).
Test: for the 10 declared targets 1/alpha in {1,2,5,10,20,50,100,137.035999177,300,1000} and N_eff in {1, 8}, solve for the microscopic coupling numerically
(mpmath findroot from an unrelated start), substitute back and confirm 1/alpha.  Criterion 'construction constrains alpha': some target unreachable.
Also reported: the tuning that 137.036 demands (g - 1 for NJL, lambda for BCS).
MUTATE control: argv `MUTATE` (exit code 1): the NJL solver uses r ln(1 + r) instead of r ln(1 + 1/r), so solve-and-substitute must fail.
"""
import sys
import mpmath as mp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
mp.mp.dps = 40
fails = 0
def check(name, cond):
    global fails
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails += 1

targets = [mp.mpf(x) for x in ('1', '2', '5', '10', '20', '50', '100', '137.035999177', '300', '1000')]
pi = mp.pi

def h_true(s):            # s = ln(1/r) = ln(Lambda^2/m^2)
    return mp.exp(-s) * mp.log(1 + mp.exp(s))
def lnh_solver(s):        # solver's version of ln h (mutated if requested)
    if MUT:
        return -s + mp.log(mp.log(1 + mp.exp(-s)))
    return -s + mp.log(mp.log(1 + mp.exp(s)))

# monotonicity of h(s) on s in (0, 3000): decreasing, so the inverse is unique
grid = [mp.mpf(k) for k in range(1, 3000, 37)]
hs = [h_true(s) for s in grid]
check("h(s) = r ln(1+1/r) strictly decreasing in s (unique inverse, g in (1,inf) covers all s>0)", all(hs[i] > hs[i + 1] for i in range(len(hs) - 1)))

reach_njl = 0; reach_bcs = 0; total = 0
rows = []
for Neff in (1, 8):
    for t in targets:
        total += 1
        s0 = 3 * pi * t / Neff                      # ln(Lambda^2/m^2) required
        # NJL: find g from the gap equation, starting the solver away from the answer
        h0 = h_true(s0)
        try:
            s_sol = mp.findroot(lambda s: lnh_solver(s) - mp.log(h0), s0 * mp.mpf('0.7') + 2)
            alpha_inv_back = Neff * s_sol / (3 * pi)
            ok_njl = abs(alpha_inv_back / t - 1) < mp.mpf('1e-12')
        except Exception:
            ok_njl = False
        reach_njl += ok_njl
        # BCS: lambda = 1/asinh(Lambda/Delta) with ln(Lambda^2/Delta^2) = s0  -> Lambda/Delta = exp(s0/2)
        lam = 1 / mp.asinh(mp.exp(s0 / 2))
        s_back = 2 * mp.log(mp.sinh(1 / lam))
        ok_bcs = abs(Neff * s_back / (3 * pi) / t - 1) < mp.mpf('1e-12')
        reach_bcs += ok_bcs
        rows.append((Neff, t, h0, lam))
print("targets x N_eff scored as surjectivity checks: %d" % total)
check("NJL gap equation reaches every target (%d/%d)" % (reach_njl, total), reach_njl == total)
check("BCS gap reaches every target (%d/%d)" % (reach_bcs, total), reach_bcs == total)
check("NO construction rejects any alpha without an extra input (criterion 'constrains alpha' NOT met)", reach_njl == total and reach_bcs == total)

print("\nTuning that 1/alpha = 137.035999177 demands:")
for Neff, t, h0, lam in rows:
    if abs(t - mp.mpf('137.035999177')) < 1e-9:
        print("  N_eff=%d: NJL g - 1 ~ h = %s (distance from criticality)   BCS lambda = %s" % (Neff, mp.nstr(h0, 5), mp.nstr(lam, 6)))
print("  BCS: 1/alpha ~ 2 N_eff/(3 pi lambda), i.e. alpha is LINEAR in the pairing coupling: alpha = 3 pi lambda/(2 N_eff)")
print("  NJL (quadratic-divergence type) needs a hierarchy-problem-sized tuning; BCS (log-type) needs only lambda ~ 1/80 -- natural, but a free number.")

# recalled illustration for condensed matter (NOT scored): E_F/Delta ~ 1e3..1e4 in 3He-A
for ratio in (mp.mpf('1e3'), mp.mpf('1e4')):
    for Neff in (2, 16):
        print("  illustration (recalled ratio %s, N_eff=%d): 1/alpha = %s" % (mp.nstr(ratio, 3), Neff, mp.nstr(Neff * 2 * mp.log(ratio) / (3 * pi), 4)))
print("  -> a condensate whose linear spectrum spans <= 1e4 gives 1/alpha of order 3-30 (alpha of order 0.03-0.3); 1/137 needs a ratio 10^35 (N_eff=8) inside one system.")

# lattice compact U(1): report
beta_c = mp.mpf('1.011')    # recalled (Wilson action, first order); Heaviside-Lorentz e^2 = 1/beta
alpha_c_HL = 1 / (4 * pi * beta_c)
print("\n(C-d) compact U(1) lattice: read (arXiv:2009.04499) alpha_QSI tunable 0 .. ~0.2 in their units (alpha = e^2/(hbar c)); recalled beta_c ~ 1.011 gives alpha_c(HL) = %s = 1/%s" % (mp.nstr(alpha_c_HL, 4), mp.nstr(1 / alpha_c_HL, 4)))
print("      1/137.036 = %s of alpha_c: an interior point of the deconfined window; the confinement bound is an INEQUALITY (no selection)." % mp.nstr((1 / mp.mpf('137.035999177')) / alpha_c_HL, 4))
check("1/137.036 lies inside the deconfined window (0, alpha_c] (inequality only)", (1 / mp.mpf('137.035999177')) < alpha_c_HL)
print("SUMMARY: all four constructions trade alpha for a microscopic coupling or ratio; fails =", fails)
sys.exit(1 if fails else 0)
