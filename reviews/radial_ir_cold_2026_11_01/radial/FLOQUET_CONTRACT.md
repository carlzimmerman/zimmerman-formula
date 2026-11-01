# TP04-R phase-production Floquet test, frozen before runs

Test the actual leading phase coupling of a small coherent radial mode, rather than presuming perturbative decay alone bounds its lifetime. Define eta=g_sigma Sigma and tau=mt. The canonical phase mode on the harmonic canonical pump has

    y''+[kappa²+eta cos(tau)/(1+eta cos(tau))]y=0.

This is exact for the stipulated R/v=1+eta cos(tau) pump. For the microscopic field it is the leading small-amplitude derivative/cubic-coupling model; the radial potential and finite metric cause higher-amplitude corrections, quantified separately by the measured anharmonic coefficient. No finite-amplitude cosmic lifetime is inferred by treating this harmonic pump as an exact full-model solution.

1. Integrate the monodromy over2pi at eta={1e-5,1e-4,1e-3,1e-2}, scaled first-band detuning x={-1.5,-.75,0,.75,1.5}, kappa=.5(1+eta x). Compare interior Floquet exponents to eta sqrt(1-x²)/2, require<5% relative for the stated narrow samples, and no exterior growth above1e-8. Wronskian det=1 to1e-9, and the exact k=0 phase-constant solution y=1+eta cos(tau) returns after one period. DOP853 tolerance2e-13/2e-14; repeat selected points at tighter tolerances.
2. Expansion: constant h=H/m and eta(tau)=eta0 exp(-3h tau/2) for eta0=.005, chi=eta0²/h={.1,1,3}. The proper canonical mode is y=a^(3/2)R theta, Q=a^(3/2)R=exp(3h tau/2)+eta0 cos(tau+phase), so y''+[kappa0²exp(-2h tau)-Q''/Q]y=0 at kappa0=.5. Integrate a vacuum-normalized complex WKB mode across +/-8eta0/h for phases0,pi/2, and subtract/control eta0=0 expansion production. Report final adiabatic occupation as a finite in/out diagnostic, Wronskian and phase sensitivity; this is not a complete cosmological state-selection/depletion calculation. Compare the integrated instantaneous first-band growth to pi eta0²/(4h), and record the exact nonstationary result without forcing it to equal a strong-amplification ansatz.

Derive the weak crossing limit from stationary phase: N_out approximately pi eta²m/(2H)=2I for I<<1. The formal growing-mode integrated exponent I=pi eta²m/(4H), rather than muF/H, controls a redshifting narrow crossing. In rho=m²Sigma²/2, I/(Gamma_pert/H)=16pi²rho/m⁴. Retain dephasing/escape conditions as explicit inequalities, not chosen halo inputs. One thread,180wall/170CPU seconds, observed RSS; v2 records/controls and preserved failures.
