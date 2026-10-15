# A photon-to-controller channel, and its energy cost

2026-10-14. C3W-005. This is a **postulated interaction** added to the engineered controller model. It is not derived from cold-energy microphysics, a measured optical material or a working drive. It makes the proposed energy-transfer mechanism concrete and exposes a large cost in one sufficient stable branch.

## 1. Local optical actuation

Let Fμν be an electromagnetic field, `Eμ=Fμν Uν` its electric field in the clock frame, and W(Φ) a nonnegative fixed actuator window supported inside the flat cabin, with W≤1. Add

\[
\boxed{\mathcal L_\gamma=-\frac14F_{\mu\nu}F^{\mu\nu}
+\frac{g_p}{2}W(\Phi)\Lambda E_\mu E^\mu.}
\]

The operator is gauge invariant and covariant. gp is a new assumed coupling. At F = 0 it and all its first variations vanish, preserving every steady background and the controller equation already completed in [CONTROL.md](CONTROL.md).

In the clock rest frame, write ε = 1+gp WΛ. Then

\[
\mathcal L_\gamma=\frac\epsilon2|E|^2-\frac12|B|^2,
\quad D=\epsilon E,\quad
\mathcal H_\gamma=\frac{|D|^2}{2\epsilon}+\frac{|B|^2}{2}.
\]

This optical block has positive clock-frame energy for ε>0. Choose gp≥0 and a nonnegative small-speed branch Λ; if needed restrict gpWΛ≤1. W is confined to the cabin, where the background shift is zero. Outside that window ε=1 and |b|≤0.1. Thus the added optical block also avoids an immediate stationary-shift negative-energy problem. More generally the simple sufficient condition is `|b|sqrt(ε)<1`: the shift–Poynting cross term is then dominated by the positive electric/magnetic energy. No optical causal/front statement for the complete nonlinear theory is claimed.

The controller equation gets the nonzero source

\[
\frac{\partial\mathcal L_\gamma}{\partial\Lambda}
=\frac{g_pW}{2}|E|^2.
\]

This uses the clock-frame electric field, rather than the Lorentz-invariant F² coupling that would vanish for an ideal plane wave. In a locally fixed clock/window configuration the energy exchange is explicit:

\[
\left.\partial_\Lambda\mathcal H_\gamma\right|_{D,B}
=-\frac{g_pW}{2}|E|^2,
\qquad
P_{\gamma\to\Lambda}=\frac{g_pW}{2}\dot\Lambda|E|^2.
\]

Electromagnetic energy decreases by the work gained by the controller, with the full covariant stress also accounting for the clock/material medium. This is energy conversion, not free energy. Nonzero pump fields backreact; the zero-field stationary proof is not an operating-pump nonlinear proof.

The action-level chain is now explicit: **an independently supplied photon field → optical controller force → Λ response → clock/material stress and geometry → test-payload motion**. If the separately hypothesized χ/S reaction actually emitted useful photons, it could in principle supply the optical input to this added coupling. Neither that carrier nor gp, W, a conversion rate or a combined reacting solution is established here.

## 2. Finite-energy activation is expensive in the strong controller branch

An infinite uniform change of Λ has infinite kinetic cost. Localized changes also have an unavoidable gradient cost in this particular model. Let the controller perturbation ℓ equal a constant Δ on a sphere of radius a and decay at infinity. For each direction,

\[
\Delta=-\int_a^\infty\partial_r\ell\,dr,
\quad
\Delta^2\le\left(\int_a^\infty r^2|\partial_r\ell|^2dr\right)
\left(\int_a^\infty r^{-2}dr\right).
\]

Integrating over directions and retaining nonnegative angular gradients yields the spherical capacity bound

\[
\int_{r\ge a}|\nabla\ell|^2d^3x\ge4\pi a\Delta^2.
\]

The exterior field ℓ=Δa/r saturates the bound in the homogeneous H¹ space; no finite box is involved.

The mixed controller criterion in CONTROL.md has a coefficient norm Cmix that is defined by the action but not numerically expanded in this checkpoint. Choose the explicit **strong sufficient controller**

\[
F_c^2=\frac{2M_p^2(1+C_{\rm mix}^2)}{1-B^2}.
\]

The resulting coupled quadratic energy estimate includes

\[
E_2\ge\frac{M_p^2(1+C_{\rm mix}^2)}2\|\nabla\ell\|_2^2
\ge2\pi M_p^2(1+C_{\rm mix}^2)a\Delta^2.
\]

With SI units restored this is at least

\[
\boxed{E_2\ge\frac{c^4}{4G}a\Delta^2.}
\]

For a = 1 metre and controller offset Δ = 0.01, the quadratic model estimate is about **3.03×10^39 joules**, using [NIST's 2022 CODATA values](https://physics.nist.gov/cuu/pdf/all.pdf). Along the stationary family Δ labels a 0.01c speed-parameter difference; this calculation is **not an achieved spacecraft Δv**. It assumes the stated strong controller choice and the positive mixed-form criterion. Cmix has not been numerically certified, and finite-amplitude nonlinear corrections have not been bounded. This is not a universal lower bound for every possible geometric drive or a measured fuel requirement.

The estimate shows why a formal stability repair is not an efficient propulsion discovery. Increasing the optical coupling does not remove the energy required to establish the controller state. Improving this branch would require a construction that avoids its stiff controller/gradient cost while retaining the actual physical constraints and energy positivity.

## 3. What this closes and leaves open

The new optical term supplies a reviewable, energy-conserving hypothetical interface between light and the controller. It closes the previous absence of any specified interaction connecting those sectors at the action level. It does not verify the coupling experimentally or derive it from the cold-carrier proposal.

Still required is a localized, finite-energy time-dependent solution with a massive payload, electromagnetic work, geometry, controller and outgoing momentum all accounted for. That solution must be in one fixed theory and cannot be obtained by changing V in prescribed target functions. The background remains exotic, and its material realization and physical vacuum matching are unproved. No bystander immunity, reactionless thrust or working cold-energy engine follows.
