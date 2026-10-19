# Source-first lattice normalization check

Date 2026-10-19. Saved before opening the new sea_lattice target package. This check reads the primary Wang v3 and Fu v2 sources, not an author verdict.

Wang et al., arXiv:2310.01168v3 (30 August 2024), defines the spin-averaged forward tensor with a 1/2 prefactor in equation (1), covariant ground-state completeness 1/(2E) in (9), and

`alpha_E^{ii} = -alpha_ref/(12 M) integral dt t^2 H_sum(t)`,

where `H_sum(t)=integral d^3x sum_(i=1)^3 <N|T Ji(x)Ji(0)|N>` and vacuum subtraction is necessary for disconnected contractions (discussion after eq11). The residual elastic/Born correction alpha_E^r is separate. Table II gives the included disconnected contribution, same for proton and neutron:

- 24D: 1.4(1.2) times 10^-4 fm^3.
- 32Dfine: 0.1(1.8) times 10^-4 fm^3.

These are two lattice estimates, not a continuum result and not a detection of a nonzero value. The main text says disconnected diagrams vanishing in the flavor-SU(3) limit were omitted; Supplement section Contributions from disconnected diagrams / Fig S3 shows the two included diagrams and states vacuum subtraction. The source supplies neither all omitted topologies nor an all-momentum disconnected response by this one table row. No flavor-current inventory is inferred here from diagram labels alone.

For the reduced sum correlator `C_sum=H_sum/(2M)`, algebra gives

`integral dt t^2 C_sum(t) = -6 alpha_E^{ii}/alpha_ref`.

For the spatial AVERAGE `C_avg=H_sum/(6M)`, the result is instead `-2 alpha_E^{ii}/alpha_ref`. This is the only change caused by averaging over ii; one must not insert an extra factor of three into an already summed source formula. The factor 2M is the covariant-state to reduced correlator normalization, not an electromagnetic factor.

Fu et al., arXiv:2411.03141v2 (1 February 2025), uses RAW mathcal T1, with tensor normalization 1/(8 pi M) in (1). On its special imaginary-energy line, eq(12) gives

`mathcal T1(iQ,Q^2) = -1/(24 pi M) integral dt cos(Qt) H_sum(t)`.

Equation (13) defines a different, MODIFIED object:

`T1(iQ,Q^2) = -4 pi alpha_ref [mathcal T1(iQ,Q^2)-mathcal T1(0,0)]/Q^2`.

Equations (13),(15) then give

`lim_(Q->0) T1(iQ,Q^2) = alpha_2 = alpha_E^{ii}`,

`d mathcal T1(iQ,Q^2)/d(Q^2)|0 = -alpha_2/(4 pi alpha_ref)`.

Thus the lattice row supplies the corresponding included-disconnected moment and the slope of RAW mathcal T1 along that specified line, or the zero-momentum limit of the MODIFIED T1. It does not supply the slope of modified T1, the raw subtraction function for all Q^2, another energy-subtraction point, the complete T2 response, or a Cottingham mass convolution.

The division alpha_E^{ii,disc}/alpha_ref removes the conventional electromagnetic prefactor from a QCD current response. It does not infer alpha_ref. A stated alpha_ref value can be used for conversion; it must be recorded as input. The row cannot establish all dynamical sea-charge derivatives or a complete proton electromagnetic mass response, especially after omitted Wick classes, temporal truncation and finite-volume/systematic limitations are accounted for.

Scope clarification from the source's Figure S3 caption: its disconnected estimator uses temporal windows t0=0.77 fm (24D) and 0.72 fm (32Dfine). The continuum moment formula above identifies the observable; the table supplies a finite-lattice, finite-window estimate of the included-contraction component, not a certified exact full-time moment or complete disconnected response.
