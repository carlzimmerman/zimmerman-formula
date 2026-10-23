"""Persistent state must reverse after nonlinear full-Hamiltonian propagation."""
import numpy as np
from quantum_wavefunction import CellWavefunction
m=CellWavefunction(16,12.)
p=m.initial_x_excitation();original=p.copy()
p=m.evolve(p,.01,10);p=m.evolve(p,-.01,10)
assert np.linalg.norm(p-original)<1e-12
assert abs(np.vdot(p,p).real-1)<1e-12
print('persistent nonlinear state and inverse propagation passed')
