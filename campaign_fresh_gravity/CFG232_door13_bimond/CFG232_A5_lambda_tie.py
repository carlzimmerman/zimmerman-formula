#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG232_A5_lambda_tie -- G4: constants ledgers (strict and inert-window) and the a0-Lambda tie for 13b.  Does a Lambda-sourced second metric supply the tie?
 13b-i : a0 := kappa c^2 sqrt(Lambdah/8pi) written in (rule T), Lambdah = Lambda_g imposed by hand.
 13b-ii: no Lambda in the action; the interaction's constant part M0 is the vacuum energy: kappa^2 = -16 pi beta/(sigma_s M0) DERIVED here from the
         minisuperspace vacuum (replacing the record's unfixed O(1)); the symmetric vacuum requires beta = gamma.
MUTATE M6 (break the tie: Lambdah = 4 Lambda_g so a0 doubles against the observed a0) and M7 (M0 -> 0) are run in A4 (cosmology) and here for the G1 / tie cells.
"""
import os, sys, math
import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG232_common as C

R = C.Run("CFG232_A5_lambda_tie")
MUT = R.mutate
P = R.P
bite = []

R.banner("13b-ii: vacuum relation from the minisuperspace action (own derivation)")
t = sp.Symbol("t")
N_, Nh_, a_, ah_ = [sp.Function(n, positive=True)(t) for n in ["N", "Nh", "a", "ah"]]
beta, gamma, sg, a02, F0 = sp.symbols("beta gamma sigma_s a02 F0", real=True)
adot, ahdot = sp.diff(a_, t), sp.diff(ah_, t)
# with Q_arg = 0 on the symmetric vacuum, only the constant F(0) = M0 enters; dQ/dN = dQ/dNh = 0 there (A4 Part 2)
Lveh = beta * (-6 * a_ * adot ** 2 / N_) + gamma * (-6 * ah_ * ahdot ** 2 / Nh_) + 2 * sg * a02 * sp.sqrt(N_ * Nh_) * (a_ * ah_) ** sp.Rational(3, 2) * F0
Hs = sp.Symbol("H")
def sym(ex):
    ex = ex.subs({sp.Derivative(a_, t): Hs * a_, sp.Derivative(ah_, t): Hs * ah_}).subs({N_: 1, Nh_: 1}).subs(ah_, a_)
    return sp.simplify(ex.doit())
EN = sym(sp.diff(Lveh, N_)); ENh = sym(sp.diff(Lveh, Nh_))
Hg = sp.solve(EN, Hs ** 2) if False else sp.solve(sp.Eq(EN.subs(Hs, sp.sqrt(sp.Symbol("H2"))), 0), sp.Symbol("H2"))
Hgh = sp.solve(sp.Eq(ENh.subs(Hs, sp.sqrt(sp.Symbol("H2"))), 0), sp.Symbol("H2"))
P(f"  vacuum H^2 from E_N = {Hg}, from E_Nh = {Hgh}")
req = sp.simplify(Hg[0] - Hgh[0])
P(f"  symmetric vacuum requires: {sp.factor(req)} = 0")
R.check("13b-ii the symmetric (g = g-hat) de Sitter vacuum sourced by the interaction's constant part exists only for beta = gamma (Z2 of the Planck weights): gamma/beta is NOT free in 13b-ii",
        sp.simplify(req.subs(gamma, beta)) == 0 and sp.simplify(req) != 0, f"difference = {sp.factor(req)}")
H2 = sp.simplify(Hg[0].subs(gamma, beta))
Lam_eff = sp.simplify(3 * H2)
kap2 = sp.simplify(8 * sp.pi * a02 / Lam_eff)                  # kappa^2 = a0^2/(G rho_Lambda) with G rho_Lambda = Lambda_eff c^2/(8pi), c = 1
P(f"  H^2 = {H2};  Lambda_eff = 3H^2 = {Lam_eff};  kappa^2 = 8 pi a0^2/Lambda_eff = {kap2}")
R.check("13b-ii derived tie: kappa^2 = -16 pi beta/(sigma_s M0) (sign: needs sigma_s M0 < 0); at beta = 1, kappa = 1/2 <=> sigma_s M0 = -64 pi = -201.06. This agrees with the record's quotation of Milgrom's eq. 87 (kappa^2 = 16 pi/(-M0~), O(1) 'unfixed') in this normalisation",
        sp.simplify(kap2 + 16 * sp.pi * beta / (sg * F0)) == 0, f"kappa^2 = {kap2}")
M0_half = -64 * math.pi
R.num("M0_for_kappa_half", M0_half)
P(f"  kappa = 1/2 <=> sigma_s M0 = {M0_half:.4f}")

R.banner("13b-i: rule T check, numerically (both footings) and the P_cap identity")
Om, hh = 0.3153, 0.6736
OL = 1 - Om
H0 = 100 * hh * 1e3 / 3.0856775814913673e22
c = 299792458.0
G = 6.67430e-11
rhoL = 3 * H0 ** 2 * OL / (8 * math.pi * G)
a0_rule = 0.5 * c * math.sqrt(G * rhoL)
P(f"  a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2, Omega_Lambda = {OL:.4f}, h = {hh}: {a0_rule:.4e} m/s^2 (canonical footing 9.3603e-11; alt 1.1312e-10 is a different rho_Lambda footing)")
R.check("13b-i rule T: a0 = kappa c^2 sqrt(Lambdah/8pi) with Lambdah = Lambda_g = 3 H0^2 Omega_Lambda/c^2 reproduces the canonical a0 to 1e-3", abs(a0_rule / 9.3603e-11 - 1) < 1e-3, f"{a0_rule:.5e}")
Pcap = 0.5 ** 2 / (8 * math.pi) * rhoL * c ** 2
R.check("P_cap identity: a0^2/(8 pi G) = (kappa^2/8 pi) rho_Lambda c^2 (the CFG43 tie: it is the definition of a0, so the tie is a stated equivalent, not a derivation)", abs(a0_rule ** 2 / (8 * math.pi * G) / Pcap - 1) < 1e-12)
ratio = math.sqrt(8 * math.pi / 3) / 0.5
P(f"  c H_Lambdah / a0 = sqrt(8 pi/3)/kappa = {ratio:.3f}: the tie fixes the cosmological relative expansion of a de Sitter g-hat at 5.79 a0 (canonical), so the interaction argument is O(1) in units of a0 by construction")
R.check("13b-i the tie makes c H_Lambdah / a0 = sqrt(8 pi/3)/kappa = 5.79 exactly (rule-T consequence)", abs(ratio - 5.7885) < 1e-3, f"{ratio:.4f}")
R.num("cH_Lambdah_over_a0", ratio)

R.banner("Constants ledgers (frozen 1.8), strict and inert-window")
LED = {
    "13a": dict(strict=["a0 (free)", "gamma/beta", "u1/u0"], relation_written_in=[]),
    "13b-i": dict(strict=["gamma/beta", "u1/u0"], relation_written_in=["a0 := kappa c^2 sqrt(Lambdah/8pi)", "Lambdah = Lambda_g"]),
    "13b-ii": dict(strict=["u1/u0", "M0 (= kappa, fitted)"], relation_written_in=["gamma = beta forced by the vacuum", "continuation of M to Q<0 (a new free FUNCTION, needed for any FRW background)"]),
    "13c": dict(strict=["a0 (free)", "coupling normalisation"], relation_written_in=[]),
}
# inert-window test on gamma/beta and the invariant direction
des = {gr: C.Design(C.nu_p2, 1.0, gr, +1) for gr in (1 / 3, 1.0, 3.0)}
inert = {}
for gr, d in des.items():
    dev = max(abs(C.forward(d.mfun, 1.0, gr, +1, float(v))["Phi"] / (v * float(C.nu_p2(v))) - 1) for v in np.geomspace(1e-3, 1e3, 25))
    inert[gr] = dev
P("  gamma/beta grid: G1-law max deviation after re-designing M: " + ", ".join(f"{k:.3g}: {v:.1e}" for k, v in inert.items()) + "  -> G1-law verdict unchanged; G1-C unchanged (A3); G5a unchanged (vector operator independent of b, A2 M3): gamma/beta is INERT for the verdicts (not counted in the inert-window count), but it is a constant of the action and counts in the STRICT count")
R.check("inert-window: gamma/beta in {1/3,1,3} leaves every gate verdict unchanged (G1-law after re-design, G1-C, G5a)", all(v < 5e-3 for v in inert.values()), "")
a0dev = []
for fac in (1.0, 2.0, 0.5):
    d = des[1.0]
    dev = max(abs(fac * C.forward(d.mfun, 1.0, 1.0, +1, float(v / fac))["Phi"] / (v * float(C.nu_p2(v))) - 1) for v in np.geomspace(1e-3, 1e3, 25))
    a0dev.append((fac, dev))
P("  a0 -> f a0 in the interaction against the fixed target: G1-law max deviation " + ", ".join(f"f={f}: {d_:.2f}" for f, d_ in a0dev))
R.check("a0 is NOT inert: doubling or halving the a0 the interaction uses (target fixed) flips G1-law to FAIL", a0dev[1][1] > 0.1 and a0dev[2][1] > 0.1, "")
strict = {k: len(v["strict"]) for k, v in LED.items()}
inert_count = {"13a": 1, "13b-i": 0, "13b-ii": 0, "13c": 1}
R.num("ledger", LED); R.num("strict_count", strict); R.num("inert_window_count", inert_count)
P("  strict counts: " + ", ".join(f"{k}: {v}" for k, v in strict.items()) + ";  inert-window counts: " + ", ".join(f"{k}: {v}" for k, v in inert_count.items()))
for k in LED:
    P(f"  {k}: constants {LED[k]['strict']}; relations written in / extra structure {LED[k]['relation_written_in']}")
R.verdict("G4 13a", "FAIL", "a0 is a free constant (also gamma/beta and u1/u0 in the strict count)")
R.verdict("G4 13b-i strict", "FAIL", "gamma/beta and u1/u0 remain; the a0 tie is WRITTEN IN (rule T) plus Lambdah = Lambda_g by hand: an equivalent of the CFG43 tie, not a derivation; kappa stays fitted")
R.verdict("G4 13b-i tie", "PASS as a stated equivalent (written in)", "a0^2/8piG = (kappa^2/8pi) rho_Lambda c^2 by definition; nothing in the bimetric structure forces Lambdah = Lambda_g")
R.verdict("G4 13b-ii strict", "FAIL", "u1/u0 remains, plus a required continuation of M to Q<0 (a new free function) that the ledger does not contain; gamma = beta is forced (not free)")
R.verdict("G4 13b-ii tie", "PASS as a native but INVERTED relation (a0 primary, Lambda derived), with kappa replaced by the value of a dimensionless function at zero argument", "kappa^2 = -16 pi beta/(sigma_s M0): derived here, not derived FROM anything: M0 is fitted; the vacuum energy exists only on the symmetric branch, which has no solution with matter in g only (A4)")
R.verdict("G4 13c", "FAIL", "a0 free; conformal coupling normalisation")

if MUT == "M6":
    R.banner("MUTATE M6 (G1 cell): Lambdah = 4 Lambda_g so the interaction's a0 doubles against the observed a0")
    dev = a0dev[1][1]
    P(f"  G1-law max deviation with a0 -> 2 a0: {dev:.2f}")
    bite.append(dev > 0.10)
if MUT == "M7":
    R.banner("MUTATE M7 (13b-ii): M0 -> 0")
    kap_inf = "infinite" if True else ""
    P("  with M0 = 0 the vacuum H^2 = 0: Lambda_eff = 0, kappa^2 = 8 pi a0^2/Lambda_eff diverges: the tie cell flips (no dark energy)")
    bite.append(sp.simplify(H2.subs(F0, 0)) == 0)
R.finish(bite if MUT else None)
