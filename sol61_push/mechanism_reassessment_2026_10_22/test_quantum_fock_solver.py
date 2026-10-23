import unittest
import numpy as np
from quantum_fock_solver import Model

class QuantumHamiltonianTests(unittest.TestCase):
 def setUp(self):self.model=Model(energy_cut=6,number_cut=6,charge=2,volume=100.)
 def test_single_vertex_normalizations(self):
  a=np.zeros(12,dtype=int);a[7]=1
  b=np.zeros(12,dtype=int);b[1]=2
  i=self.model.index[tuple(a)];j=self.model.index[tuple(b)]
  self.assertAlmostEqual(self.model.H3[j,i],1/(2*np.sqrt(self.model.M*self.model.volume)),places=12)
  self.assertAlmostEqual(self.model.H4[j,j],1/(2*self.model.volume),places=12)
 def test_hermiticity(self):
  for h in [self.model.H3,self.model.H4,self.model.mass_operator]:
   self.assertLess(np.max(np.abs((h-h.T).toarray())),1e-12)
 def test_charge_momentum(self):
  self.assertTrue(np.all(self.model.states@self.model.charges==2))
  self.assertTrue(np.all(self.model.states@self.model.momenta==0))

if __name__=='__main__':unittest.main()
