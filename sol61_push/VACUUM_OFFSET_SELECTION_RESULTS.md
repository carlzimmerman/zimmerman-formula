# Vacuum offset prevents selection of 32π in the current trial family

Status: exact conditional algebraic obstruction, not a solution of the 32π goal.
This extends the local phenomenological action and vacuum equations in
VARIABLE_CLOCK_RESULTS.md and VARIABLE_CLOCK_MODES_RESULTS.md. Natural units
c=ħ=1 are used. Assume A,B,ell,Z,G,Kc>0, M²=1/(8πG),

    U(q)=A/q²+Bq²+V0,  lambda(q)=1+ell q,  S=2+3ell q.

V0 is an additive constant in the assumed action. No mechanism forbidding or
removing it has been derived. The constant-q vacuum obeys

    H²=2U/(3M²S),  (SU)'=0.

Writing W=SU gives

    W''=12A/q⁴+4B+6ell A/q³+18ell Bq > 0.

W' tends to minus infinity at q→0+ and plus infinity at q→infinity.
There is exactly one stationary positive q* for every real V0. At the
stationary point U/S=−U0'/(3ell), where U0=A/q²+Bq². Put
qflat=(A/B)^(1/4), Umin=2√(AB). Since
W'(qflat)=3ell(Umin+V0), positive de Sitter vacua occur precisely for
V0>−Umin and have 0<q*<qflat. Implicit differentiation gives

    dq*/dV0=−3ell/W'' < 0.

The homogeneous mass is W''/(ZS)>0. The earlier linear vacuum stability
conditions also survive this offset: define

    d=−2U0'/(Zq*)=4(A/q*⁴−B)/Z > 0,
    m=U0''/Z−d=(2A/q*⁴+6B)/Z > 0.

The mode proof's mixing bound is b²/(8alpha)=d/(4S)<d/8<m,
because S>2 and m−d/8=(3A/(2q*⁴)+13B/2)/Z>0.
Together with the positive homogeneous mass these are the same sufficient
conditions used in VARIABLE_CLOCK_MODES_RESULTS.md. Thus those local linear
health conditions do not remove the offset freedom. This does not establish
nonlinear health, radiation-era health or high-frequency completion.

Using the *conditional bare* galaxy scale a0bare=1/(12πG Kc q*), the ratio is

    Cbare=Lambda/a0bare²
         =2304π³G³Kc² q*² U/S
         =(1536π³G³Kc²/ell)(A/q*−Bq*³).

Consequently

    dCbare/dV0=4608π³G³Kc²(A/q*²+3Bq*²)/W'' > 0.

As V0 decreases to −Umin, q*→qflat and Cbare→0. As V0 increases
without bound, q*→0 and Cbare→infinity. Thus the formal classical family
spans every positive bare coefficient while retaining these vacuum and linear
conditions. This unbounded range is not a claim that arbitrarily large H is
inside the effective theory's validity range: small offset changes already
demonstrate the lack of exact selection near a controlled vacuum.

There is a second independent freedom. The Kc q P³ term vanishes on P=0
vacua and has no quadratic contribution there. Scaling Kc by t leaves the
background and its linear vacuum equations unchanged but multiplies Cbare by
t². Vacuum regularity and linear stability therefore cannot select 32π in
this family, even when V0 is fixed to zero.

Physical galaxy matching remains unfinished. If a separately justified,
fixed Newton conversion RN=G_N/G is used, its corresponding ratio is
RN² Cbare. This is a conditional dictionary, not proof that observed G_N
stays fixed as V0 varies. Global source matching or an additional physical
principle could impose further restrictions; none has been demonstrated.

## Verification and next research target

vacuum_offset_selection.py checks seven exact SymPy identities, including the
stationary energy, implicit derivative, coefficient and its offset derivative.
The script prints the results; the positivity and endpoint arguments above are
analytic. No numerical scan or new literature theorem is claimed here.

The next useful breakthrough must eliminate or physically determine the
vacuum offset **and** link the remaining galaxy coupling to the cosmological
scale. Merely fitting V0 or Kc to make the coefficient 32π supplies no
prediction. A sourced solution remains necessary for the observed acceleration
dictionary, but cannot by itself establish the missing selection principle.
