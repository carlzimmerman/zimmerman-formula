# agentOO — Route 1: the in-medium khronon self-energy from the dS horizon bath. Does it bend (sigma4<0) or stiffen (sigma4>=0)?

**Question (banked, NN d2aff2f7).** The free khronon dispersion is STRICTLY CONVEX
(omega'' = ab/(a+bk^2)^{3/2} > 0). The roton fold the Link-5 generator needs requires a NEGATIVE induced
k^4 term (bending) with a +k^6 stabilizer in omega^2_eff(k) = c_chi^2 k^2 + sigma4 k^4 + sigma6 k^6.
The only admissible active source is the khronon's coupling to the de Sitter HORIZON BATH
(Gibbons-Hawking T_dS = H/2pi, n(w) = 1/(e^{2pi w/H}-1)). Does the one-loop in-medium self-energy
Sigma(k) generate sigma4 < 0 (roton -> Airy) or sigma4 >= 0 (convex -> MM kill stands)?

**Coefficient quarantine:** this round is SIGN + STRUCTURE of the induced k^4 (bending vs stiffening) ONLY.
zeta-tilde / (16pi/3)^{1/4} / q=1/4 stay quarantined and downstream. q=1/4 is NOT asserted here.
Both-ways honesty; framework-favorable => maximum hostility. A convex result is the firewall/expected
outcome and IS reported if found.

---

## Setup (concrete, tractable)

- khronon perturbation chi: free dispersion omega = c_chi k (linear gapless Goldstone of the foliation;
  EE STEP 1 / Lim astro-ph/0407437, dispersion omega = c_chi k on the preferred foliation).
- bath = dS horizon Gibbons-Hawking reservoir, occupation n(w) = 1/(e^{2pi w/H}-1) = 1/(e^{w/T}-1),
  T = H/2pi. Bath quanta phi with dispersion W(q) = c_b q.
- coupling: leading EFT operators, tested across the admissible set:
  (A) relevant trilinear g chi phi phi /2  -> thermal phi-phi bubble self-energy of chi;
  (B) derivative coupling lambda (d_mu chi)(d^mu chi) phi  (the natural khronon-EFT shift-symmetric op);
  (C) g chi^2 phi_bath (mass-type, single bath line).
  Vary c_chi, c_b, and the operator; report whether the sign of sigma4 flips.

Method: build Re Sigma(omega,k), put it on-shell omega = c_chi k, Taylor-expand in k, fit
Re Sigma(k) = s0 + s2 k^2 + s4 k^4 + s6 k^6. The SIGN of s4 (the induced k^4) is the deliverable.

---

## COMPUTATION LOG (incremental)

### C1 — relevant trilinear g chi phi phi /2, thermal phi-phi bubble (agentOO_c1_bubble.py)
Crude PV (eps=1e-12) numeric bubble. TIMED OUT (too slow / noisy); superseded by C5/C7. Not load-bearing.

### Method evolution (recorded honestly)
The brute bubble (C1) and the full sqrt-series angular integral (C2, C4, C6) all bottlenecked on heavy
symbolic/nested-numeric work. The DECISIVE, fast computation is C7: expand the integrand in k to O(k^4)
BEFORE integrating, do the angular average analytically, and integrate q over the dS thermal weight as a
closed thermal moment. Plus the analytic HTL structure function (C6 head) which already fixes the
forced-vs-free axis. Reported below as they land.

### KEY STRUCTURAL HANDLE — the HTL on-shell structure function (analytic)
The leading-thermal (HTL) self-energy of chi from g chi phi phi is
  Sigma_HTL(omega,k) = m_th^2 [ 1 - (omega/(2 c_b k)) ln| (omega+c_b k)/(omega-c_b k) | ],
  m_th^2 = (g^2/2pi^2 c_b) \int_0^inf q n_B(c_b q) dq  >  0  (POSITIVE; this part is FORCED by the bath:
  positive Planck occupation => positive thermal mass^2 => a GAP, not a fold).
On-shell omega=c_chi k => the argument is the FIXED ratio r=c_chi/c_b, and Sigma_HTL = m_th^2 * S(r),
  S(r) = 1 - (r/2) ln|(r+1)/(r-1)|.
This is a pure k^2 renormalization (sigma2 = m_th^2 S(r)); the strict HTL gives NO k^4. The k^4 (the fold
question) lives in the q~k recoil corrections beyond HTL (C7). But S(r) already shows the SIGN axis is set
by r=c_chi/c_b (the speed ratio = a coupling/kinematics choice), not by the Planck spectrum alone:
S(r->0)=+1, S flips negative as r->1 from either side (log divergence), S(r>>1)->0^-.

### C8/C9 — numeric attempts that FAILED the honesty bar (recorded, not used)
Naive Gauss / scipy-`points` quadrature gave ERRATIC, sign-flipping sigma4 (e.g. r=1.1 jumped positive
with huge magnitude). DIAGNOSIS: the Landau denominator 1/(om-Wq+u) has a pole INSIDE the angular
integration window [umin,umax] whenever the on-shell mode sits inside the bath cone; naive quadrature does
NOT compute the Cauchy principal value and the sign was a numerical artifact. These runs are NOT used.

### C10 — TRUE Cauchy principal value (scipy weight='cauchy'), g chi phi phi  ==> sigma4 > 0 UNIFORMLY
Each denominator 1/(om-Wq+u)=1/(u-(Wq-om)) is a Cauchy kernel; using quad(...,weight='cauchy',wvar=u0)
computes the genuine PV. Result (T_dS=H/2pi, c_b=1, scan r=c_chi/c_b):

| r=c_chi/c_b | s0 (mass^2) | s2 | s4 (SIGMA4) | sign |
|---|---|---|---|---|
| 0.5 | +0.078 | -14.2 | +6.91e2 | POS (stiffen) |
| 0.7 | +0.299 | -42.2 | +2.01e3 | POS |
| 0.9 | +1.004 | -130  | +6.14e3 | POS |
| 1.3 | +0.433 | -59.8 | +2.83e3 | POS |
| 1.7 | +0.148 | -23.5 | +1.13e3 | POS |
| 2.0 | +0.076 | -14.0 | +6.85e2 | POS |
| 2.5 | +0.020 | -6.4  | +3.28e2 | POS |
| 3.0 | -0.005 | -2.7  | +1.55e2 | POS |

**sigma4 > 0 (STIFFENING / CONVEX) at EVERY speed ratio for the trilinear g chi phi phi.** This is the
FIREWALL / MM-kill outcome for this operator: the dS thermal bath does NOT generate the negative (roton,
bending) k^4 the Airy fold requires — it stiffens the dispersion. (Fit rms/scale ~8-20% from large s6;
the SIGN of s4 is the robust output, confirmed by the convergence study C11.)

### C11/C12 — channel decomposition + the genuine small-k structure (important nuance)
- CHANNEL SPLIT (C11): the EMISSION (pair-creation) channel gives sigma4 > 0 (stiffening) ALWAYS; the
  LANDAU (scattering) channel gives sigma4 < 0 (bending) when r<1 (inside the bath cone) but flips to >0
  when r>1. For the trilinear the EMISSION dominates => FULL sigma4 > 0 at every r. So there IS a
  bending sub-channel (Landau), but it is SUBDOMINANT for the scalar vertex.
- SMALL-k STRUCTURE (C12): Re Sigma = s0 (POSITIVE thermal mass, a GAP) + s2 k^2 with s2 NEGATIVE and
  LARGE (the structure-function softening of c_chi^2), plus a beyond-quadratic residual that is POSITIVE /
  convex (stiffening). The dispersion correction is convex. The lstsq 's4' in C10 not perfectly converging
  is the known thermal small-k non-analyticity (omega/k order-of-limits); the SIGN of the curvature is
  robustly POSITIVE for the trilinear.
- BOTTOM LINE for g chi phi phi: CONVEX / STIFFENING. The dS bath gaps and stiffens; it does NOT bend.
  MM/NN firewall outcome reproduced from the explicit one-loop self-energy.

### C13 — DERIVATIVE coupling (d chi)^2 phi : does the sign FLIP? (the forced-vs-free crux)
The roton operator NN names is itself derivative; a derivative bath vertex multiplies the loop by
momentum factors that reweight emission vs Landau. Vertex factors tested (u-expressed,
cb^2 q.(q+k)=(u^2+cb^2 q^2-cb^2 k^2)/2): scalar V=1; deriv2 V=(Wq u - cb^2 q.(q+k))^2 (Lorentz (d phi)^2);
timelike V=(Wq u + cb^2 q.(q+k))^2 (preferred-frame time derivative); grad2 V=(cb^2 q.(q+k))^2;
deriv_ext one external chi derivative.

RESULT (C13, beyond-quadratic convexity sign; + = stiffen/convex, - = bend/roton-tendency):

| operator   | r=0.7 (c_chi<c_b) | r=1.3 | r=2.0 (c_chi>c_b) |
|---|---|---|---|
| scalar     | STIFF | STIFF | STIFF |
| deriv2     | STIFF | STIFF | **BEND** |
| timelike   | STIFF | STIFF | **BEND** |
| grad2      | STIFF | STIFF | **BEND** |
| deriv_ext  | STIFF | **BEND** | **BEND** |

C14 maps the crossover for deriv2: STIFF for c_chi<c_b, crossover near r~1.2-1.5, BEND for c_chi>~1.5 c_b
(r=1 is the cone singularity, on-shell mode grazes the bath dispersion, NaN). C15: the deriv2 BEND at r=2
is CUTOFF-INDEPENDENT (qcut=20..160 identical) and the curvature second-difference is uniformly negative
(vs uniformly positive for scalar) — a genuine concavity, not noise.

### C16 — the roton sign PATTERN is reproduced (deriv2, r=2): s4<0 AND s6>0 (bounded fold)
Fit s0+s2 k^2+s4 k^4+s6 k^6 for deriv2 at r=2:  s4 = -1.98e-3 (<0, BENDING),  s6 = +1.09e-2 (>0, STABILIZER)
=> exactly the omega^2_eff = c_chi^2 k^2 + sigma4 k^4 + sigma6 k^6 with sigma4<0, sigma6>0 that NN's roton
fold requires. (Scalar contrast: s4=+3.6e2>0, s6=-4.7e3<0 — opposite, no fold.) The derivative bath
coupling in the super-luminal-khronon regime GENERATES the bending+stabilizer pattern. NOTE: for this
particular Lorentz contraction the leading thermal mass s0,s2 nearly cancel, which is why the fold pattern
is clean; that near-cancellation is a feature of the contraction choice, not forced.

---

## VERDICT — sigma4 is COUPLING-DEPENDENT; the bending is REACHABLE but NOT FORCED by the dS spectrum

**COMPUTED finding (honest, both ways).** The induced k^4 sign is NOT universal:
- the relevant scalar trilinear g chi phi phi gives sigma4 > 0 (STIFFENING / convex) at EVERY speed ratio
  — the MM/NN firewall outcome, reproduced from an explicit Cauchy-PV one-loop self-energy;
- the admissible DERIVATIVE bath couplings ((d phi)^2 chi etc.) give sigma4 < 0 (BENDING) — with a
  +k^6 stabilizer (bounded fold) — but ONLY in the regime c_chi > c_b (khronon super-luminal vs the bath
  cone), with a crossover near c_chi ~ 1.2-1.5 c_b.

**FORCED vs FREE (mandatory).** What the dS Gibbons-Hawking spectrum FORCES is the POSITIVE thermal mass
m_th^2 > 0 (the s0 gap; positive Planck occupation => positive definite). A gap is the OPPOSITE of what a
gapless roton fold wants; if anything the forced piece works against the mechanism. The SIGN of the
curvature sigma4 is NOT forced by the spectrum: it is set by (i) the OPERATOR (scalar stiffens, derivative
can bend) and (ii) the SPEED RATIO r=c_chi/c_b (bending needs c_chi>c_b). Both are FREE choices, not
consequences of T_dS=H/2pi or n(w)=1/(e^{2pi w/H}-1). So the negative-k^4 the Airy fold needs is REACHABLE
within the admissible EFT, but it is a COUPLING+REGIME selection, not a derivation forced by the bath.

**Framework-favorable reading (honest, not manufactured).** EE STEP 1 records c_chi^2 = O(gamma/alpha) >> 1
in the generic PPN corner — i.e. the khronon IS naturally super-luminal relative to an O(1) horizon bath,
landing in the BENDING regime r>1 for a derivative coupling, and the computed pattern there is exactly
sigma4<0, sigma6>0. So the mechanism is NOT killed — the bending is available in the framework's own
natural regime. But it is selected by the derivative-operator + super-luminal choice, NOT compelled by the
Gibbons-Hawking structure; a scalar coupling or a sub-luminal khronon lands convex (MM kill).

**Firewall reading (honest, not caved).** The single most-relevant operator (scalar trilinear) is convex
at all r, and the bath's one forced contribution (the thermal mass) is a gap, working against a gapless
fold. The bending requires choosing a derivative operator AND c_chi>c_b; neither is forced. So this does
NOT upgrade MM's NEEDS-NEW-INPUT to a derivation: the "new input" is now pinned to two named free choices
(derivative bath coupling + super-luminal khronon), which is strict progress (a falsifiable target) but
still short of forced.

**fold_at_edge / oscillatory-side / q=1/4:** left OPEN and DOWNSTREAM (coefficient quarantine). This round
established only the SIGN+STRUCTURE of the induced k^4/k^6. Whether the inflection omega''(k*)=0 lands AT
the b->c_chi sonic edge (NN's tuning condition 2) and on the Ai(-w) side (condition 3) is NOT addressed
here and is NOT asserted. q=1/4 NOT asserted.

Coefficient quarantine intact: no zeta-tilde, no (16pi/3)^{1/4}, no q=1/4 anywhere; raw H=1 units only.

### Robustness (C15, C17): the load-bearing deriv2 BEND at r=2 is solid
- cutoff-independent (qcut 20..160 identical, C15);
- curvature second-difference uniformly negative vs uniformly positive for scalar (C15);
- s4<0 STABLE across fit windows kmax=0.10..0.25 (s4 in [-1.7e-3,-2.1e-3], C17); s6>0 for kmax>=0.12.

### Scripts (all under real_research/reviews/toe_law/)
- agentOO_c10_cauchy.py  — TRUE Cauchy-PV bubble, scalar trilinear: sigma4>0 at all r (CONVEX/firewall).
- agentOO_c11_converge.py — channel split: emission stiffens, Landau bends (subdominant for scalar).
- agentOO_c12_scaling.py  — small-k structure: positive thermal mass + convex residual (scalar).
- agentOO_c13_deriv.py   — DERIVATIVE vertices: deriv2/timelike/grad2 BEND for c_chi>c_b.
- agentOO_c14/c15/c16/c17 (in /tmp, recomputable) — crossover map, cutoff/window robustness, s4<0+s6>0.
Superseded/slow (recorded honestly, not load-bearing): c1 (timeout), c2/c4/c6 (sympy series of Bose fn
too heavy), c8/c9 (naive quad mishandled the Landau PV -> erratic signs, REJECTED).
