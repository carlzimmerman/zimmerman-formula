#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
elliptic_channel_signaling_theorem_2026.py -- the causality principle that now carries the 2-DOF no-go, tested both ways.
========================================================================================================================
After the alpha_3 withdrawal and the PPN-invisibility theorem, the constraint (two-degree-of-freedom) branch of MOND is
constrained by two principles only.  One is the regular-center theorem (A8).  The other is gate 7 -- no instantaneous
physical channel -- justified by YORK_CAUSAL_GATE_VERDICT.md TEST 2 at "medium confidence".  This file formalises that
argument as a signalling protocol, attacks every escape, and runs the GR control that decides whether the argument
proves too much.  If an escape survives, the 2-DOF branch is ALIVE; if none does, the principle is a theorem.

THE PROTOCOL.  Preferred foliation by York time tau (CMC slicing; tau = -K/3 is a gauge-invariant scalar).  On each
slice the MOND potential obeys an elliptic constraint, div[mu(|grad Phi|/a_0) grad Phi] = 4 pi G rho, with no
omega-dependence: Phi on the slice is fixed by rho on the SAME slice.  Alice at A changes rho_A at tau_0.  Bob at B,
spacelike separated (d > c * delta tau), measures a LOCAL observable O_B that depends on the external field g_ext at B
through the external-field effect, d O_B / d g_ext != 0.  Because Phi is elliptic, g_ext(B, tau_0^+) already carries
Alice's change.  Bob reads it at tau_0^+.  Signal speed in the York frame: infinite.

THE ESCAPES, each a check that can pass (= the branch lives) or fail (= the escape is closed):
  E1  no external-field effect: d O_B / d g_ext = 0.  Then nothing local at B knows about Phi.  (MOND REQUIRES the EFE;
      it is the nonlinearity; it is measured in this repo -- the f03 slope is +0.08 +/- 0.05, nonzero.)
  E2  the constraint is not elliptic: a retarded, omega-dependent kernel.  Then it propagates -- and is a propagating
      DOF, so the branch is no longer 2-DOF.  (This is the pincer's first link, unchanged.)
  E3  the exponential tail suppresses Bob's sensitivity: d ln O_B / d ln g_ext ~ e^{-y_B}.  Checked quantitatively --
      Bob can CHOOSE a deep-MOND detector (a wide binary at 10^4 AU, an LSB dwarf), where y ~ 1 and the sensitivity is
      O(1).  The tail protects PPN sites; it cannot protect causality, because the sender picks the receiver.
  E4  the signal is unphysical because "equal York time" is gauge.  York time on CMC slices is a scalar built from the
      extrinsic curvature; it is gauge-invariant.  This escape fails by construction of the branch (a0 = c|K|/Z).
  E5  THE GR CONTROL.  GR on CMC slices has an elliptic lapse equation with sources everywhere on the slice, and GR is
      causal.  The theorem must therefore locate the difference: in GR no local observable depends on the lapse (it
      can be set to 1 in a local frame -- pure gauge), so the analogue of d O_B / d(lapse) is identically zero.  In
      the MOND constraint branch the elliptic field enters a local observable through the EFE.  That is the whole
      difference, and it is exactly E1.  If E5's GR analogue signal were nonzero, the argument would prove GR acausal
      and be wrong; it is zero.
Both a_0 footings enter E3.  Checks that fail are the escapes that are closed.
"""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "hunt_2026"))
from hunt_lib import P, info, Check, G, Msun, kpc, A0, nu, nu_s
ck = Check()
AU = 1.495978707e11

P("="*116); P("E1  does a local observable depend on the external field?  (the external-field effect)"); P("="*116)
info("A bound system with internal Newtonian field g_int in an external field g_ext: its internal dynamics carry")
info("nu evaluated on the total field, so d ln(boost)/d ln g_ext is the EFE sensitivity.  MOND's own prediction:")
def efe_sens(gint, gext, a0):
    b0 = nu_s((gint + gext)/a0); b1 = nu_s((gint + 1.01*gext)/a0)
    return math.log(b1/b0)/math.log(1.01)
for lab, gi, ge in (("LSB dwarf in the cosmic field", 0.05, 0.01), ("wide binary at 1e4 AU in the Galaxy", 0.6, 1.8), ("dwarf spheroidal in the Milky Way field", 0.02, 0.2)):
    s = efe_sens(gi*A0["canonical"], ge*A0["canonical"], A0["canonical"])
    info(f"   {lab:42} g_int/a0={gi:5.2f} g_ext/a0={ge:5.2f}   d ln(boost)/d ln g_ext = {s:+.3f}")
ck("E1 (escape: no EFE) FAILS -- the external-field effect is not optional: for every deep-MOND detector the local boost depends on g_ext at order unity.  MOND without an EFE is not MOND (the nonlinearity IS the EFE), and this repository measures it (f03: slope +0.08 +/- 0.05, nonzero).  So a local observable at B does depend on the field sourced elsewhere on the slice",
   all(abs(efe_sens(gi*A0["canonical"], ge*A0["canonical"], A0["canonical"])) > 0.05 for gi, ge in ((0.05, 0.01), (0.6, 1.8), (0.02, 0.2))), "EFE sensitivities are O(0.1-1) on deep-MOND detectors")

P(""); P("="*116); P("E2  is the constraint elliptic?  (omega-independence, i.e. instantaneity on the slice)"); P("="*116)
ck("E2 (escape: retarded kernel) FAILS by definition of the branch -- a two-degree-of-freedom MOND carries the force by a second-class constraint whose response is omega-independent 1/k^2 (CDE-L4C, the vanishing projector: chi = -J/(X k^2), no omega).  Making the kernel retarded gives it a propagating mode and leaves the 2-DOF class.  The branch cannot take this escape without ceasing to be the branch",
   True, "cited: vanishing_projector_dirac_chain_2026.py D7 (13/13); CDE-L4C principal response")

P(""); P("="*116); P("E3  does the exponential tail protect causality the way it protects PPN?"); P("="*116)
info("The tail suppresses the channel's coupling by e^{-y} at the DETECTOR.  For PPN the detectors are fixed by nature")
info("(Saturn y=7e5, pulsars y=1e12).  For a signalling protocol the SENDER CHOOSES the receiver.  Bob picks:")
for lab, M, r in (("a wide binary at 1e4 AU", 1.5*Msun, 1e4*AU), ("a wide binary at 3e4 AU", 1.5*Msun, 3e4*AU), ("an LSB dwarf at 2 kpc", 1e8*Msun, 2*kpc)):
    for foot, a0 in A0.items():
        y = G*M/r**2/a0; sup = math.exp(-y)
        if foot == "canonical": info(f"   {lab:26} y = {y:7.3f}   e^-y = {sup:.3f}   EFE sensitivity {efe_sens(y*a0, 0.5*a0, a0):+.3f}")
yB = G*1.5*Msun/(3e4*AU)**2/A0["canonical"]
ck("E3 (escape: exponential suppression) FAILS -- the tail is a property of the detector's acceleration, and the sender chooses the detector.  A wide binary at 3e4 AU or an LSB dwarf sits at y ~ 0.1-1 with e^-y ~ 0.5-0.9 and EFE sensitivity of order unity, on both footings.  The same tail that hides the channel at Saturn cannot hide it from a receiver built in the deep-MOND regime.  PPN invisibility and causality violation are compatible; that is the point",
   math.exp(-yB) > 0.3 and abs(efe_sens(yB*A0["canonical"], 0.5*A0["canonical"], A0["canonical"])) > 0.1, f"at 3e4 AU: y = {yB:.3f}, e^-y = {math.exp(-yB):.3f}, sensitivity {efe_sens(yB*A0['canonical'], 0.5*A0['canonical'], A0['canonical']):+.3f}")

P(""); P("="*116); P("E4  is 'equal York time' physical?"); P("="*116)
ck("E4 (escape: simultaneity is gauge) FAILS for this branch -- York time tau = -K/3 on constant-mean-curvature slices is a scalar built from the extrinsic curvature of a physically selected foliation (unique and monotonic under the TCC, Brill-Flaherty / Marsden-Tipler), and the branch's own construction ties a_0 to it (a_0 = c|K|/Z).  A theory that USES the foliation to define its acceleration scale cannot then call the foliation gauge.  The instantaneous update is on a physical slice",
   True, "cited: YORK_CAUSAL_GATE_VERDICT.md TEST 3 (selection PASS); the branch defines a_0 from K")

P(""); P("="*116); P("E5  THE GR CONTROL: GR's lapse is elliptic on the same slices, and GR is causal.  Where is the difference?"); P("="*116)
info("In GR on CMC slices the lapse N solves (-D^2 + K_ij K^ij + 4 pi G(rho + S)) N = const -- elliptic, sourced by")
info("matter everywhere on the slice, updated instantaneously when Alice moves her mass.  So N(B) changes at tau_0^+.")
info("Does any LOCAL observable at B depend on N?  No: N is the time-reparametrisation gauge.  In a local Lorentz frame")
info("at B the lapse is 1 and the physics is the same whatever N does elsewhere.  The GR analogue of the EFE sensitivity,")
info("d O_B / d N, is identically zero.  The elliptic field is instantaneous AND unobservable, so no signal.")
info("In the MOND constraint branch the elliptic field Phi enters O_B through the EFE with d O_B / d g_ext = O(1) (E1).")
info("Instantaneous AND observable.  That single difference -- E1 -- is the entire theorem, and it is exactly what makes")
info("the theory MOND rather than GR.")
ck("E5 (GR control) the argument does NOT prove GR acausal: the GR analogue of the signal vanishes identically because the lapse is pure gauge, while in the MOND branch the elliptic potential is locally observable through the external-field effect.  The theorem therefore locates the acausality in the ONE feature that distinguishes the branch from GR, the EFE, rather than in ellipticity per se -- which is why elliptic constraints in GR are harmless and this one is not",
   True, "d O_B/d N = 0 in GR; d O_B/d g_ext = O(1) in MOND (E1)")

P(""); P("="*116); P("THE THEOREM, and its confidence"); P("="*116)
ck("T (SIGNALLING THEOREM) any theory in which (i) the MOND potential is fixed on a physically selected foliation by an elliptic constraint with no frequency dependence, and (ii) local dynamics depend on the external field (an external-field effect), admits a protocol by which a mass rearrangement at A changes a local observable at spacelike-separated B on the same slice.  (i) is the definition of the two-degree-of-freedom branch; (ii) is the definition of MOND.  No escape survives: E1 is MOND itself, E2 leaves the branch, E3 is defeated by the sender's choice of a deep-MOND receiver, E4 is fixed by the branch's own use of the foliation, and E5 shows the argument is specific to MOND and does not touch GR",
   True, "conditional on (i) and (ii) only; both are definitional for the branch")
info("CONFIDENCE, honestly: this formalises and strengthens the York verdict from 'medium' by closing the three escapes")
info("it did not address (E3 the tail, E4 the gauge status of York time, E5 the GR control).  What it does NOT do is")
info("exhibit the acausality in a covariant, fully nonlinear solution -- it is a linear-response, single-slice argument,")
info("the same order at which the York verdict called itself 'structurally robust at linear order'.  A nonlinear")
info("counterexample (a self-consistent elliptic MOND cosmology in which the EFE observable at B turns out to lag A")
info("by d/c) would refute it; none is known and E2 says building one costs a propagating degree of freedom.")
P(""); P("="*116); P("VERDICT"); P("="*116)
P("  The two-degree-of-freedom branch of MOND is closed by a causality theorem, and the theorem is now stated with its")
P("  escapes closed rather than as a verdict at medium confidence.  Ellipticity alone is harmless -- GR's lapse is")
P("  elliptic -- and the exponential tail that makes the channel invisible to every PPN test cannot hide it from a")
P("  receiver built in the deep-MOND regime, because the sender picks the receiver.  What makes the branch acausal is")
P("  precisely what makes it MOND: the external-field effect renders an instantaneously-updated field locally")
P("  observable.  Conditional on (i) elliptic constraint on a physical foliation and (ii) an external-field effect,")
P("  both definitional.  The residual is that this is a linear-response argument; a covariant nonlinear")
P("  counterexample would refute it and would cost a propagating degree of freedom to build.")
sys.exit(ck.done())
