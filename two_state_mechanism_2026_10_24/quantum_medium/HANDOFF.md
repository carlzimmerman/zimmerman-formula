# Quantum medium checkpoint

User asked interacting quantum dipole spectrum including mass/state, fewer
parameters, conservation, physical disk/dwarf/cluster selector without switches.
New folder only. Derived Gaussian/Bogoliubov two-species charged Bose response,
not exact many-body theory. psi masses m,epsm,charges+-q,mean n,restmassrho
n*m*(1+eps). Matching q²/(4pi)=Gm² conditional. No contact/spectral/rate knobs.
State cold coherent uniform LOCAL hypothesis, not derived stable global ground.

D=diag(hbar²k4/4ms²)+n qsqt/sqrt(msmt)-4piG n sqrt(msmt).
Dimensionless D=diag(Q²,Q²/eps²)+zzT-vvT; z=(1,-1/sqrteps),v=(1,sqrteps).
Dipole residues=|z.e|²; stable weights residue/(2omega). Unstable states flagged,
not vacuum spectra. Optional species-exchange eps1 removes mass-ratio freedom
but makes gravitybranch exactly electrically dark at everyk and chargebranch
gapped. Remaining m free. No derived critical nonlinear susceptibility.

Quantum Jeans threshold: t²+eps(1-eps²)t-eps(1+eps)²=0,t=QJ².
kJ²=2m omega0 QJ/hbar. Common rho=etaMb/(4pib³/3),k=pi/b gives
mcrit proportional1/sqrt(Mb*b). At eps.1 thresholds7.236e-21,2.171e-22,
5.117e-24,1.253e-26 eV. Thus diskunstable=>clusterunstable for this proxy.
723 common mass/epspoints;378 allnonrel cutoff;0 desired stabilityordering.
Stability NOTtetherfraction; no population/rotation/actualRAR success claimed.

run_response completed/valid:606spectra,12energyODEtests. Sumrule2.81e-16,
resolvent2.42e-16,analytic equalmass2.22e-16;fineenergy<=5.21e-11.
run_wave completed/valid:9 live3D nonlinear meanfieldruns12/18/24³,
dt.01/.005/.0025,time.5,Q.7,eps.1. Bothcharges and masses transport.
Periodic zero-modegravity removed, no compensator species. StrangHconservative
continuum;energyerrors7e-5,1.75e-5,4.38e-6 (secondorder);number<=7.25e-14.
Weaklynonlinear only, no causalMaxwell orrelativisticgravity or livebaryons.
run_audit completed/valid: independent FourierPDElinearizationerror2.02e-12,
figure quantum_scale.png visuallyinspected.

Important: computed full longitudinal interacting response contains Coulomb;
not irreducible constitutivechi, cannot feed it back intoMaxwell withoutdouble
counting. No exactgroundstate,thermalization,EOS,contactrepulsion,radiativecapture
or saturation derived. Bosonicattraction maylackstablethermodynamicgroundstate.
No activejobs,previousfilesunchanged,no manuscript/commit/publication.
