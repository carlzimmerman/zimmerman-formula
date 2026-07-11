# Lane 1 -- Operator reduction of Woodard's Z[g] in the Sun + external field

**Verdict: Z[g] LOCALIZES. The local-AQUAL proxy is justified. Q2 = proxy = FAILS Cassini x3.8-5.6. Road 2 does NOT beat Branch B.**

## Exact equations used (arXiv:2512.10513 = JCAP 2026 04:081; arXiv:1106.4984)
- **eq 5** `u_mu = d_mu phi`, `g^{mn} d_m phi d_n phi = -1`, `phi(0,x)=0`.
  u is the gradient of an **eikonal (Hamilton-Jacobi) scalar** with null initial data on the
  t=0 (end-of-inflation) surface -- NOT `Box^{-1}(metric)`. Corrects the brief's characterization.
- **eq 6** ADM form `phidot = N sqrt(1+gamma^{ij}d_i phi d_j phi) - N^i d_i phi`.
- **eq 15** static test geometry `ds^2 = -(1+2Psi)c^2 dt^2 + (1+2Phi)dx.dx`.
- **eq 26** `Box -> grad^2` on static fields; `(1/Box)(R_ab u^a u^b) -> Psi`;
  Box^{-1} & its first derivative **vanish on the t=0 surface** (retarded/causal, cosmological IVP).
- **eq 27** `Z[g] = (4c^4/a0^2) g^{mn} d_m[(1/Box)R uu] d_n[(1/Box)R uu] -> (4c^4/a0^2)|grad Psi|^2`.
- **eq 23** `DeltaL = (c^4/16piG)[2 Psi'^2 - (4c^2/3a0) Psi'^3 + ...] sqrt(-g)` = **LOCAL AQUAL/Milgrom**.
- **eq 30** `f(Z) = (1/2) Z exp[-(1/3) sqrt|Z|]`.
- Deferred: eq (34) region explicitly defers the interpolating inhomogeneous solve to "a nice followup."

## The reduction, tested on the three posed nonlocalities

**(b) the eikonal u^mu (the sharpest candidate).** Solving eq 5 order by order in the weak
static field (sympy, STEP 1) gives `phi = -t(1 + Psi(x))`, so
- `u^0 = 1 + O(Psi)`
- `u^i = -t d_i Psi`  (a **secular free-fall tilt**, first order in Psi, growing with t).

The tilt is real and anisotropic, but it enters `R_ab u^a u^b` only far down the order tower:
`R_ab u^a u^b = R_00 (u^0)^2 + 2 R_0i u^0 u^i + R_ij u^i u^j`.
- `R_00 = grad^2 Psi` -- **leading**, O(Psi), isotropic Poisson source.
- `2 R_0i u^0 u^i` -- **exactly zero** (static, current-free => no gravitomagnetic Ricci `R_0i=0`).
- `R_ij u^i u^j` -- O(Psi^3) t^2, carries the anisotropic `r.g_ext` dependence but is **two orders down**.

**(a) retarded/cosmological Box^{-1}.** For a source static since t=0, `(1/Box)(static F)` near the
Sun today = `grad^{-2}F` + an initial-data transient that sits on the wavefront shell at `r~ct`
(Hubble radius). The transient's residue inside the solar system varies only on the Hubble scale
=> a near-uniform offset, `d_i(offset) ~ H/c`, giving **zero** l=2 structure on 10-AU scales
(`H0 L/c ~ 1e-14`). The uniform galactic external field `Psi_ext = g_ext.x` is harmonic
(`grad^2 Psi_ext = 0`), so it sources no local `R_00`; it enters as the matched homogeneous
solution. Hence `(1/Box)(R uu) = Psi_sun + Psi_ext = Psi_total`, **local**.

**(c) cross terms.** `Z = (4c^4/a0^2)[|grad Psi_total|^2 + 2 grad Psi_total.grad(delta) + ...]`.
The leading `|grad Psi_total|^2 = |grad Psi_sun|^2 + 2 grad Psi_sun.g_ext + |g_ext|^2` -- the
anisotropic cross term `2 grad Psi_sun.g_ext` that sources the **Milgrom external-field quadrupole is
already local and IS in the proxy**. The genuinely-nonlocal `delta` only appears at sub-leading order.

## Magnitude of the nonlocal anisotropic correction
`delta-Z/Z ~ u_local^2` where `u_local` = local mimetic-dust streaming speed / c.
- Physical (energy-bounded, irrotational dust capped at v_esc): `(v_esc/c)^2 ~ 1.1e-6`.
- Even the *unphysical* naive-secular cap (`v/c = g_gal * t_age / c ~ 0.28`) gives only `~0.08`,
  i.e. a <8% shave -- nowhere near the **factor ~4-6** suppression needed to reach the ceiling.
- Horizon IR-tail l=2 leakage: `~1e-14`.

## Why localization is structural, not just power-counting
Woodard's invariant Lagrangian (28)/(27) was **reverse-engineered to reduce to the local AQUAL
Lagrangian (23) in the static geometry (15)**. Eq 23 is exactly the Milgrom Lagrangian whose
variation gives the field equation (20) that produces the external-field quadrupole. So in the
static solar-system limit the field EQUATION *is* local AQUAL, up to the non-staticity corrections
above (~(v/c)^2) and Hubble-scale IR tails -- both negligible for Cassini.

## Propagation to Q2 (both footings)
- Banked local-AQUAL proxy Q2 = 2.0-2.9e-26 s^-2; Cassini ceiling < 5.2e-27 s^-2 => FAILS x3.8-5.6.
- Woodard = proxy x (1 +/- 1e-6) = proxy => **FAILS x3.8-5.6**.
- a0 footing fork: screening `exp[-(2/3)g/a0]` is *looser* for larger a0, so a0=1.13e-10 and
  Woodard's own a0=1.2e-10 give same-or-worse Q2. **FAIL robust on all three footings.**

**No nonlocal suppression exists. Lane 2's premise (nonlocal-anisotropic delta-Z) is not triggered.**
