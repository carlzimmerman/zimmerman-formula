"""One mass interpolation for both event energies and scalar/gas forces.

Positive current widths retain the pinned source interpolation; group masses
come from its common cubic mass-squared table. No source file is overwritten.
"""
from vertices import VertexBackground
class ConsistentVertexBackground(VertexBackground):
 def at(self,x):
  data=super().at(x)
  by={g['id']:g for g in data['groups']}
  for name,gid in (('U1','F1_1'),('SU2','F3_0'),('SU3','F8_0')):
   data['current_source']['gauginos_over_mu'][name]=by[gid]['mass']
  return data
