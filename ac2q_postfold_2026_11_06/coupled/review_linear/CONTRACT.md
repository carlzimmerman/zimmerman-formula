# Independent linear benchmark

Compare the unchanged native solver against the independently derived,
constraint-satisfying homogeneous Fourier-mode linearization. Use odd n=31,
k=128, Fourier mode m=4, initial delta beta=1e-12 cos(m theta), initial
relative lapse perturbation zero, and momenta reconstructed from the linear
Hamiltonian and momentum constraints. Integrate to t=.01 with native RK4
dt=.000625 and dt/2. Integrate the cancellation-free two-variable linear ODE
using DOP853 with tight tolerances. Record projected amplitudes, full field
relative error, momentum residual, and native constraint exceptions. This is
a local linear consistency diagnostic, not proof of nonlinear convergence,
regularity, or shocks. Preserve implementation unchanged. Single-thread run.
