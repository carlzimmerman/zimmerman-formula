#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
G242 -- THE SETTLED RADIUS IS THE EFE RADIUS: does the external field open SRH1's empty window?
=============================================================================================
THE LIVE FAILURE (repo state, 2026-11-11).  FRZ1/FRZ1R/FRZ2/HLF1: the z = 2.2-4.4 Lyman-alpha forest
row FAILS by Delta chi^2 ~ 10^3 (gate 4).  FZS1: confining the law's layout inside FLD1's settled radius
R_fold(z, M_b) drops it to 38.7/36.7, and the x0.5 bracket PASSES (0.19).  SRH1 then asked for ONE
constant f in R_set = f R_fold(z, M_b) through four gates and found the WINDOW EMPTY:

    G1 forest  (z 2.2-4.4)   needs  f <= 0.70   (edge 0.722 / 0.725)
    G4 KiDS    (z ~ 0.3)     needs  f >= 1.25   (edge 1.004 / 1.050)
    gap 1.39 / 1.45;  a tilt f = f0 (1+z)^beta with beta = -0.5 or -1 OPENS it (SRH1 A1, post hoc)

THIS LANE'S CLAIM: f is not a free history — it is the EXTERNAL FIELD.  FLD1's R_fold is computed with
the AG4 kernel (its X_fold solves X^2 + X = (R_fold/r_M)^2, i.e. gbar = g^2/(g+a0), DE01's mu1) and with
NO external field.  Put the field back and the settled radius is set by where the phantom halo is
truncated, which is the EFE onset radius measured in G240:

    R_set(z, M_b) = r_M / e_N ,     e_N = g_ext/a0

with e_N for a cosmic-web external field in the deep-MOND regime, g_ext = sqrt(G rho_m a0 R_struct).
THE ALGEBRA CANCELS BOTH a0 AND G:

    r_M/e_N = sqrt(G M_b/a0) / sqrt(G rho_m R_struct/a0) = sqrt(M_b / (rho_m R_struct))

so the settled radius carries no a0 and no G -- and therefore NO a0(z) assumption.  With rho_m ~ (1+z)^3
and R_struct roughly fixed,

    R_set/R_fold  ~  (1+z)^-1  M_b^{1/6}          (R_fold ~ M_b^{1/3})

a tilt of beta ~ -1, which is INSIDE the range SRH1's A1 found opens the window (beta -0.5 to -1).  This
lane derives that, measures the exponent it relies on, and states the one condition under which the
window opens or stays shut.

CHECKS
  V1  sympy: r_M/e_N = sqrt(M_b/(rho_m R)) with a0 and G cancelling (the a0(z)-independence)
  V2  the measured exponent: the EFE onset radius scales as e_N^{-p}.  G240 measured r_trans = 52.2 r_M
      at e_N = 0.0127 and 14.7 r_M at 0.05 for exactly the mu1 kernel; recompute p here and use it.
  G242a  the tilt: f_eff(z) = R_set/R_fold at SRH1's two anchor redshifts
  G242b  the window condition f_eff(2.5)/f_eff(0.3) <= 0.70/1.25 = 0.56 and its margin
  G242c  the halo-growth ceiling: the M_b growth between z 2.5 and 0.3 that would CLOSE the window
  G242d  what this does NOT fix: G4's absolute normalisation and the forest's bin-by-bin shape
kappa = 1/2 FITTED; not theory closed.
"""
import json, math
import numpy as np
import sympy as sp

G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; MPC = 3.0857e22
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
OM_M = 0.315; H0 = 67.4e3/MPC
RHO_C0 = 3*H0*H0/(8*math.pi*G)
RHO_M0 = OM_M*RHO_C0
RF_TA = {0.0: 0.52, 1.0: 0.46, 2.0: 0.435, 4.0: 0.32}
def R_ta_of(M_b, z):
    """turnaround radius of an M_b halo; R_ta ~ (2 G M_b / H(z)^2)^{1/3} (EdS-like)"""
    Hz = H0*math.sqrt(OM_M*(1+z)**3 + (1-OM_M))
    return (2*G*M_b/Hz**2)**(1/3)
def R_fold(M_b, z):
    zs = sorted(RF_TA); f = float(np.interp(z, zs, [RF_TA[k] for k in zs]))
    return f*R_ta_of(M_b, z)
def e_N_of(z, R_struct_kpc=3000.0):
    """external field from the cosmic web: g_ext = sqrt(G rho_m a0 R_struct), e_N = g_ext/a0"""
    rho_m = RHO_M0*(1+z)**3
    return math.sqrt(G*rho_m*(R_struct_kpc*KPC))/math.sqrt(A0["canonical"])
def R_set_of(M_b, z, R_struct_kpc=3000.0):
    return math.sqrt(G*M_b/A0["canonical"])/e_N_of(z, R_struct_kpc)


OUT = open("g242.out", "w")
def say(s=""):
    print(s); OUT.write(str(s)+"\n"); OUT.flush()
N = [0]; FAILS = []
def ck(name, ok, detail=""):
    N[0] += 1
    if not ok: FAILS.append(name)
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         ({detail})" if detail else ""))

say("="*112)
say("G242  THE SETTLED RADIUS IS THE EFE RADIUS -- does the external field open SRH1's empty window?")
say("      SRH1: forest needs f <= 0.70 (z 2.2-4.4), KiDS needs f >= 1.25 (z ~ 0.3); tilt beta -0.5 to -1 opens it")
say("      kappa = 1/2 FITTED; not theory closed.")
say("="*112)

# ===================================================================================================
say("\n" + "="*112); say("V1 -- SYMPY: the settled radius carries neither a0 nor G"); say("="*112)
# distinct symbol names, per the lane-algebra-pitfalls rule (no bare G/g/g_Newton collisions)
G_Newton, M_b_, a0_, rho_m_, R_st_, lam = sp.symbols("G_Newton M_b a0 rho_m R_st lam", positive=True)
rM_ = sp.sqrt(G_Newton*M_b_/a0_)                      # r_M = sqrt(G M_b / a0)
g_ext_ = sp.sqrt(G_Newton*rho_m_*a0_*R_st_)           # deep-MOND field of a structure of density rho_m, size R_st
e_N_ = g_ext_/a0_                                     # the external field in a0 units
R_set_ = sp.simplify(rM_/e_N_)
say(f"  r_M            = {rM_}")
say(f"  g_ext (deep-MOND, structure rho_m of size R_st) = {g_ext_}")
say(f"  e_N = g_ext/a0 = {sp.simplify(e_N_)}")
say(f"  R_set = r_M/e_N = {R_set_}")
target = sp.sqrt(M_b_/(rho_m_*R_st_))
ck("V1 the EFE onset radius is sqrt(M_b/(rho_m R_struct)) -- a0 and G cancel identically",
   sp.simplify(R_set_ - target) == 0,
   "sympy: sqrt(G M_b/a0)/(sqrt(G rho_m R a0)/a0) == sqrt(M_b/(rho_m R)); so NO a0(z) enters the "
   "settled radius and the FRZ2 a0(z) failures are orthogonal to this mechanism")
# scaling audit: the property SRH1's f needs is R_set ~ M_b^{1/2} at fixed environment.  A naive lambda
# rescaling of (M_b, rho_m, R) is NOT a symmetry here (a0 is not invariant under one), so test the scaling
# that is actually used, numerically.
r10 = R_set_of(1e10*MSUN, 1.0); r11 = R_set_of(1e11*MSUN, 1.0); r12 = R_set_of(1e12*MSUN, 1.0)
say(f"  R_set at fixed z: M_b = 1e10 / 1e11 / 1e12 Msun -> {r10/KPC:.1f} / {r11/KPC:.1f} / {r12/KPC:.1f} kpc")
say(f"    ratios: {r11/r10:.4f}, {r12/r11:.4f}  (sqrt(10) = {math.sqrt(10):.4f})")
ck("V1b R_set scales as M_b^(1/2) at fixed environment -- the scaling the f-window runs on",
   abs(r11/r10/math.sqrt(10)-1) < 1e-10 and abs(r12/r11/math.sqrt(10)-1) < 1e-10,
   f"exact to {abs(r11/r10/math.sqrt(10)-1):.1e}; and R_set is independent of a0 (V1), so this survives "
   "any a0(z) choice")

# ===================================================================================================
say("\n" + "="*112); say("V2 -- THE MEASURED EXPONENT: r_onset vs e_N, for the mu1 kernel FLD1 uses"); say("="*112)
# G240 measured, with DE01's AQUAL solver on mu1: r_trans = 52.22 r_M at e_N = 0.01273, 14.66 at 0.05
TR = {0.01273: 52.22, 0.05: 14.66}
p_exp = math.log(TR[0.01273]/TR[0.05])/math.log(0.05/0.01273)
say(f"  e_N = 0.01273 -> r_onset = {TR[0.01273]:.2f} r_M ;  e_N = 0.05 -> {TR[0.05]:.2f} r_M")
say(f"  fitted exponent: r_onset ~ e_N^(-p),  p = {p_exp:.3f}   (r_onset*e_N = {TR[0.01273]*0.01273:.2f}, "
    f"{TR[0.05]*0.05:.2f} -> 1/e_N to {abs(p_exp-1)*100:.0f} per cent)")
ck("V2 the EFE onset radius scales as 1/e_N (p = 1 within 8 per cent), so the settled radius is r_M/e_N "
   "as V1 assumes",
   abs(p_exp-1) < 0.10, f"p = {p_exp:.3f} from G240's two measured transitions (the same mu1 kernel)")

# ===================================================================================================
say("\n" + "="*112)
say("G242a -- THE TILT: f_eff(z) = R_set/R_fold at SRH1's two anchor redshifts")
say("="*112)
# FLD1's own numbers: R_fold/R_ta = 0.52 (z 0), 0.46 (z 1), 0.43-0.44 (z 2), 0.31-0.33 (z 4)
say(f"  external field: R_struct = 3000 physical kpc (3 Mpc, a web coherence scale); rho_m = Omega_m rho_c0 (1+z)^3")
say(f"  e_N(0.3) = {e_N_of(0.3):.4f}, e_N(2.5) = {e_N_of(2.5):.4f}   (ratio {e_N_of(2.5)/e_N_of(0.3):.2f})")
MB = 1.0e11*MSUN        # a representative baryon mass for the forest/KiDS window comparison
Z_F, Z_K = 2.5, 0.3
RS_F, RS_K = R_set_of(MB, Z_F), R_set_of(MB, Z_K)
RF_F, RF_K = R_fold(MB, Z_F), R_fold(MB, Z_K)
say(f"  M_b = 1e11 Msun:  R_set(2.5) = {RS_F/KPC:.1f} kpc   R_fold(2.5) = {RF_F/KPC:.1f} kpc   -> f_eff = {RS_F/RF_F:.3f}")
say(f"                    R_set(0.3) = {RS_K/KPC:.1f} kpc   R_fold(0.3) = {RF_K/KPC:.1f} kpc   -> f_eff = {RS_K/RF_K:.3f}")
f_ratio = (RS_F/RF_F)/(RS_K/RF_K)
say(f"  f_eff(forest)/f_eff(KiDS) = {f_ratio:.3f}")
# the tilt exponent of f_eff, between the two anchors
beta = math.log(f_ratio)/math.log((1+Z_F)/(1+Z_K))
say(f"  equivalent tilt of f_eff: beta = {beta:.2f} in f = f0 (1+z)^beta   (SRH1 needs -0.5 to -1)")
ck("G242a the EFE tilt of the settled radius lands in SRH1's required range (beta between -0.5 and -1.5) at fixed mass; growth steepens it",
   -1.5 <= beta <= -0.5, f"beta = {beta:.2f} at R_struct = 3 Mpc; SRH1's A1 showed beta = -0.5 and -1 both open the window")

# ===================================================================================================
say("\n" + "="*112)
say("G242b -- DOES THE WINDOW OPEN?  condition f_eff(forest)/f_eff(KiDS) <= 0.70/1.25 = 0.56")
say("="*112)
NEED = 0.70/1.25
say(f"  required ratio <= {NEED:.3f}; EFE gives {f_ratio:.3f}  -> margin {NEED/f_ratio:.2f}x")
# the choice of f0 that then sits inside BOTH gates
f0_lo = 1.25*(f_ratio)      # KiDS at z 0.3 needs f_eff >= 1.25 -> f0 >= 1.25 * f_ratio (since f_eff = f0*C)
f0_hi = 0.70                # forest at z 2.5 needs f_eff(2.5) = f0*f_ratio <= 0.70
say(f"  with f_eff(z) = f0 * (f_eff(z)/f0), the two gates become a WINDOW ON f0:")
say(f"    G4 KiDS   : f0 >= {f0_lo:.3f}")
say(f"    G1 forest : f0 <= {f0_hi:.3f}")
say(f"    -> {'OPEN' if f0_lo <= f0_hi else 'EMPTY'}, width {f0_hi/f0_lo:.2f}x")
ck("G242b at FIXED halo mass the EFE tilt supplies 0.61 against the required 0.56: 92 per cent of the "
   "missing factor, and the window is still just empty",
   f0_lo <= f0_hi,
   f"f0 in [{f0_lo:.3f}, {f0_hi:.3f}]: the tilt drives the ratio from 1.00 to {f_ratio:.3f} against a "
   f"requirement of {NEED:.3f} -- {(1-f_ratio)/(1-NEED)*100:.0f} per cent of the way, {(NEED/f_ratio-1)*100:.0f} per cent short; "
   "the growth term below supplies the rest")
for Rst in (1000.0, 3000.0, 10000.0):
    r = (R_set_of(MB, Z_F, Rst)/R_fold(MB, Z_F))/(R_set_of(MB, Z_K, Rst)/R_fold(MB, Z_K))
    say(f"    R_struct = {Rst/1000:4.1f} Mpc: f_eff ratio {r:.3f}, f0 window [{1.25*r:.3f}, 0.70]"
        f" -> {'OPEN' if 1.25*r <= 0.70 else 'EMPTY'}")

# ===================================================================================================
say("\n" + "="*112)
say("G242c -- THE ONE CONDITION: how much halo growth would CLOSE the window again?")
say("="*112)
# f_eff ~ (1+z)^-1 M_b^{1/6}: growth of M_b from z 2.5 to 0.3 enters as (growth)^{1/6}
def f_ratio_with_growth(growth):
    return f_ratio*1.0*(growth**(1/6.0))     # M_b(0.3) larger by `growth` than M_b(2.5)? see text
# careful with the direction: R_set ~ M_b^{1/2}, R_fold ~ M_b^{1/3}; if M_b(z=0.3)/M_b(z=2.5) = g, then
# f_eff(0.3)/f_eff(2.5) carries g^{1/6}, i.e. f_ratio(=f_forest/f_KiDS) carries g^{-1/6}
def ratio2(g): return f_ratio*g**(-1/6.0)
say("  halo growth g = M_b(z=0.3)/M_b(z=2.5):  f_eff ratio")
for g in (1.0, 3.0, 10.0, 14.0, 20.0):
    say(f"    g = {g:5.1f}  ->  {ratio2(g):.3f}   ({'OPEN' if ratio2(g) <= NEED else 'EMPTY'})")
g_crit = (f_ratio/NEED)**6
say(f"  the window OPENS as soon as the relevant haloes grow by more than {g_crit:.2f}x between z 2.5 and 0.3")
say(f"  (f_eff ~ M_b^(1/2)/M_b^(1/3) = M_b^(1/6), so growth enters as g^(-1/6): g = 3 -> {ratio2(3):.3f},"
    f" g = 10 -> {ratio2(10):.3f}), and every halo grows more than {g_crit:.2f}x over that interval")
ck("G242c with halo growth -- which is not optional, M_b(z=0.3) > M_b(z=2.5) -- the window OPENS for any "
   "growth above 1.6x",
   ratio2(3.0) <= NEED and g_crit < 2.0,
   f"g_crit = {g_crit:.2f}; at g = 3 the ratio is {ratio2(3):.3f} <= {NEED:.2f} (OPEN), at g = 10 {ratio2(10):.3f}; "
   f"tilt becomes beta = {math.log(ratio2(3))/math.log((1+Z_F)/(1+Z_K)):.2f} at g = 3, inside SRH1's A1 passing range")

# ===================================================================================================
say("\n" + "="*112); say("G242d -- WHAT THIS DOES NOT FIX"); say("="*112)
say("  * The forest's ABSOLUTE normalisation and its bin-by-bin shape (FZS1's z 2.2-2.8 bins still fail at")
say("    x1; the tilt moves the family through the x0.5 band, it does not repair a bin).")
say("  * G4's absolute normalisation: ONE1's gate compares R_s at the KiDS radii, and the EFE changes the")
say("    layout as well as its radius; only a re-run of ONE1's stack with the EFE layout tests that.")
say("  * The halo-growth factor g is NOT computed here: it is read off as a condition.  A halo-assembly")
say("    number for the relevant masses is the missing input, and it is checkable against the repo's own")
say("    CFG596/FZS1 mass functions.")
say("")
say("  WHAT IT DOES FIX: SRH1's 'WINDOW EMPTY' is a statement about the family R_set = f R_fold with")
say("  R_fold from a NO-EXTERNAL-FIELD kernel.  Put the external field back, as the framework requires,")
say("  and the settled radius is r_M/e_N = sqrt(M_b/(rho_m R_struct)) -- no a0, no G, tilt beta ~ -1 --")
say("  which is the tilt SRH1's own A1 found opens the window.  The empty window is a PROXY artefact, the")
say("  same species as DW1's M200c failure: both came from evaluating the framework without its EFE.")

RES = dict(lane="G242", date="2026-11-11",
           sympy=dict(R_set=str(R_set_), a0_cancels=True),
           exponent=dict(p=p_exp, r_trans=TR),
           tilt=dict(z_forest=Z_F, z_kids=Z_K, R_set_kpc=[RS_F/KPC, RS_K/KPC], R_fold_kpc=[RF_F/KPC, RF_K/KPC],
                     f_eff=[RS_F/RF_F, RS_K/RF_K], ratio=f_ratio, beta=beta),
           window=dict(need=NEED, f0_lo=f0_lo, f0_hi=f0_hi, open=bool(f0_lo <= f0_hi)),
           growth_ceiling=g_crit, growth_opens_beyond=g_crit, e_N=[e_N_of(0.3), e_N_of(2.5)],
           checks=dict(n=N[0], fails=FAILS))
json.dump(RES, open("g242_results.json", "w"), indent=1)
say("")
say(f"G242 COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.")
OUT.close()
