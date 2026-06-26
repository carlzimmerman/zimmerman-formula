"""
nonlinear_pump.py -- the ADVERSARIAL steelman for GATE-B.

The honest crack the gate leaves open (phase_gate.py, result a2): Maxwell antisymmetry
forbids the ANTISYMMETRIC coupling channel to all orders, but a SYMMETRIC dissipative
coupling C_sym is NOT excluded by antisymmetry alone -- only by shift symmetry (b).

This file STEELMANS the "3D nonlinear mode-mixing breaks it" hope as hard as possible:
we let the free mode phi_free = A cos(omega t + theta), omega = mu c, be driven by the
genuine AeST nonlinear cross terms (the phi-A_mu couplings, the K(Q) anharmonicity, and
an O(1) tensor/shear background h_ij that a merger supplies). We compute the TIME-AVERAGED
power injected into the free mode,
    <P> = < phi_free_dot * S_nonlinear >,
to cubic order. Phase-pinning requires <P> to depend on theta with a stable fixed point
(a restoring, theta-locking term). We test whether ANY AeST-allowed nonlinear term
produces a theta-dependent secular <P>, or whether they ALL time-average to zero / to a
theta-INDEPENDENT (amplitude-only) form.

HONEST RESULT (do not skip): NOT every channel vanishes. Two AeST-allowed channels are
theta-blind (no torque), but the RESONANT tensor/merger channel h*phidot^2 gives a
theta-DEPENDENT, NONZERO  <P> = (3/8)A^3 h0 omega^3 sin(psi-theta). So the linear
'zero power injection' is NOT exact nonlinearly -- 3D mode-mixing DOES couple to the free
mode. The reason the door still does not open is then handed to resonant_channel.py (the
nonzero pump is CONSERVATIVE/parametric -> no phase fixed point, no friction) and to
phase_gate.py (it is FREQUENCY-GATED: mu c >> cluster drive). We verify with sympy and
report the crack openly rather than asserting a false foreclosure.
"""

import sympy as sp


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


t, omega, A, theta = sp.symbols('t omega A theta', real=True, positive=True)
mu, c = sp.symbols('mu c', positive=True)

# The free mode and its velocity
phi = A * sp.cos(omega * t + theta)
phidot = sp.diff(phi, t)


def time_average(expr):
    """Average over one period T = 2 pi / omega (kills all nonzero harmonics)."""
    T = 2 * sp.pi / omega
    return sp.simplify(sp.integrate(expr, (t, 0, T)) / T)


def test_cross_term_pump():
    """
    AeST cross term: the scalar couples to the aether through J^mu = A^nu F_{nu}^mu-type
    and through Q = A^mu d_mu phi. A merger supplies an external, slowly-varying aether
    perturbation a_ext(t) and a shear/tensor background. The most dangerous SYMMETRIC-
    looking driver is a term  S ~ g * a_ext(t) * phi (a direct, NON-derivative-of-phi
    coupling) -- i.e. a SHIFT-SYMMETRY-BREAKING source. Test two cases:
      (1) shift-SYMMETRIC source  S = g * a_ext * phidot   (allowed by AeST)
      (2) shift-BREAKING source    S = g * a_ext * phi      (NOT allowed by AeST)
    and see which can pin theta.
    """
    banner("Nonlinear pump: can an AeST-allowed source phase-pin theta?")
    g = sp.Symbol('g', real=True)
    # a slowly varying external (merger) amplitude: treat as constant over a period
    a_ext = sp.Symbol('a_ext', real=True)

    # (1) shift-SYMMETRIC coupling: source involves d phi (here phidot)
    S1 = g * a_ext * phidot
    P1 = time_average(phidot * S1)
    dP1 = sp.simplify(sp.diff(P1, theta))
    print(f"[1] AeST-ALLOWED (shift-symmetric)  <phidot*S> = {P1}")
    print(f"    d<P>/dtheta = {dP1}  (theta-dependent power? {dP1 != 0})")
    print(f"    -> {'AMPLITUDE-only (anti-MOND damping), NO phase locking' if dP1==0 else 'THETA-LOCKING'}")

    # (2) shift-BREAKING coupling: source involves bare phi
    S2 = g * a_ext * phi
    P2 = time_average(phidot * S2)
    dP2 = sp.simplify(sp.diff(P2, theta))
    print(f"\n[2] NON-AeST (shift-breaking)       <phidot*S> = {P2}")
    print(f"    d<P>/dtheta = {dP2}  (theta-dependent power? {dP2 != 0})")
    print(f"    -> {'cannot pin' if dP2!=0 and P2==0 else 'time-averages to ' + str(P2)}")

    return {"shift_symmetric_dP": dP1, "shift_breaking_P": P2}


def test_anharmonic_K_pump():
    """
    The genuine AeST nonlinearity is the K(Q) free function's anharmonicity:
    expand K(Q) ~ K2 Q^2 + K3 Q^3 + ..., with Q ~ phidot (+ external aether).
    The cubic term gives a source S ~ K3 * phidot^2 -- a SHIFT-SYMMETRIC, even-in-phidot
    self-coupling. Test whether <phidot * S> pins theta (it cannot: it is shift-symmetric
    AND conservative -> time-averages to zero over a period and is theta-blind).
    """
    banner("Anharmonic K(Q) self-pump (the real AeST nonlinearity)")
    K3 = sp.Symbol('K3', real=True)
    a_ext = sp.Symbol('a_ext', real=True)
    # cubic self-source from K3 (phidot + a_ext)^2 - even powers -> derivative source
    S = K3 * (phidot + a_ext)**2
    P = time_average(phidot * S)
    dP = sp.simplify(sp.diff(P, theta))
    print(f"[K3] <phidot * K3 (phidot+a_ext)^2> = {P}")
    print(f"     d<P>/dtheta = {dP}")
    print(f"     -> conservative anharmonic self-coupling: {'NO secular pump (theta-blind)' if dP==0 else 'PUMPS'}")
    return {"K3_dP": dP, "K3_P": P}


def test_tensor_merger_pump():
    """
    O(1) tensor/shear background from a violent merger: h_ij(t) couples to the scalar
    gradient through the AeST Q = (g^{mu nu}+A^mu A^nu) d_mu phi d_nu phi. The induced
    source on the free mode is S ~ h(t) * (d phi)^2-type = h(t)*phidot^2 (shift-symmetric,
    even). Even with a RESONANT tensor mode h = h0 cos(omega t + psi), test the averaged
    power: it depends on the PHASE DIFFERENCE (theta - psi), the only way 3D could pin --
    so this is the SINGLE most dangerous channel. Compute it honestly.
    """
    banner("Tensor/merger resonant pump h(t) ~ cos(omega t + psi): the most dangerous channel")
    h0, psi = sp.symbols('h0 psi', real=True)
    h = h0 * sp.cos(omega * t + psi)
    # source from h coupling to phidot^2 (shift-symmetric, the AeST-allowed form)
    S = h * phidot**2
    P = time_average(phidot * S)
    P = sp.simplify(sp.expand_trig(P))
    print(f"[tensor] <phidot * h(t) * phidot^2> = {P}")
    # Does it depend on (theta - psi)? If P==0, NO pinning even resonantly.
    dP_theta = sp.simplify(sp.diff(P, theta))
    print(f"         d<P>/dtheta = {dP_theta}")
    print(f"         -> resonant tensor pump on shift-symmetric source: "
          f"{'ZERO secular power (odd harmonic, averages out)' if P==0 else 'PUMPS theta'}")

    # CONTRAST: if the source were shift-BREAKING (h * phi^2), would it pin?
    S_bad = h * phi**2
    P_bad = sp.simplify(sp.expand_trig(time_average(phidot * S_bad)))
    print(f"\n[contrast] shift-BREAKING h*phi^2 source: <P> = {P_bad}")
    print(f"           depends on (theta-psi)? "
          f"{'YES -> this WOULD pin, but it is NOT AeST-allowed' if P_bad!=0 else 'no'}")
    return {"tensor_P": P, "tensor_dP": dP_theta, "shift_breaking_tensor_P": P_bad}


def main():
    r1 = test_cross_term_pump()
    r2 = test_anharmonic_K_pump()
    r3 = test_tensor_merger_pump()

    banner("NONLINEAR-PUMP VERDICT (honest -- one channel does NOT vanish)")
    print("AeST-ALLOWED nonlinear sources (shift-symmetric: built from d phi):")
    print("  - direct cross term g*a_ext*phidot     : theta-blind (amplitude only) ->", r1['shift_symmetric_dP'])
    print("  - anharmonic K3 self-coupling          : no secular pump ->", r2['K3_dP'])
    print("  - resonant tensor/merger h*phidot^2    : theta-DEPENDENT, NONZERO ->", r3['tensor_P'])
    print()
    print("HONEST CORRECTION: the resonant tensor/merger channel h*phidot^2 does NOT")
    print("vanish -- it gives a theta-dependent <P> = (3/8)A^3 h0 omega^3 sin(psi-theta).")
    print("So the LINEAR 'zero power injection' is NOT exact once O(1) resonant tensor modes")
    print("are included: nonlinear 3D mode-mixing DOES couple to the free mode. This is a")
    print("real crack in the v.(Cv)=0 story and must not be hidden.")
    print()
    print("BUT (resonant_channel.py runs it to ground): that nonzero <P> is a CONSERVATIVE")
    print("PARAMETRIC pump (derives from the shift-symmetric action piece (1/3)h phidot^3),")
    print("NOT a friction. It pumps AMPLITUDE with no attracting phase fixed point -> the")
    print("phase LIBRATES/PRECESSES, never pins. AND (phase_gate.py) it is FREQUENCY-GATED:")
    print("the resonance needs Omega_drive ~ omega=mu c ~ 708 H0, while cluster mergers")
    print("drive at ~few H0 -> ~470x off resonance -> exp-suppressed in practice.")
    print()
    print("The ONLY source that pins via a true torque is the shift-BREAKING h*phi^2 type:")
    print("  shift-breaking tensor pump <P> =", r3['shift_breaking_tensor_P'])
    print("  -- a bare-phi (non-derivative) coupling BREAKS the AeST shift symmetry,")
    print("     i.e. a DIFFERENT theory; within AeST it is forbidden.")
    print()
    print(">>> NET: 3D nonlinear mode-mixing OPENS a coupling (linear antisymmetry breaks),")
    print(">>> but it is conservative (no friction -> no phase fixed point) AND off-resonant")
    print(">>> (mu c >> cluster drive). So it does NOT phase-pin omega=mu c. Door stays shut,")
    print(">>> now via no-FRICTION + STIFFNESS/RESONANCE, not via zero-power-injection.")

    # HONEST assertions: the AeST-allowed DISSIPATIVE channels are theta-blind (no pin),
    # the resonant tensor channel is NONZERO (the crack), and only shift-breaking pins.
    assert r1['shift_symmetric_dP'] == 0      # direct cross: amplitude-only, no torque
    assert r2['K3_dP'] == 0                    # anharmonic self: no secular pump
    assert r3['tensor_P'] != 0                 # HONEST: resonant tensor channel does NOT vanish
    assert r3['shift_breaking_tensor_P'] != 0  # only shift-breaking gives a true pinning torque
    print("\n[assertions PASS] resonant tensor channel is NONZERO (crack acknowledged);")
    print("non-resonant dissipative channels theta-blind; pinning needs shift-breaking/friction.")


if __name__ == "__main__":
    main()
