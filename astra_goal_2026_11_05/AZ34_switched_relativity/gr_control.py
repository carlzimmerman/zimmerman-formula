#!/usr/bin/env python3
"""Exact linearized-GR control: lapse changes need not be physical signals."""
import hashlib
import json
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
t,x,y,z = coords = s.symbols('t x y z', real=True)
f = s.Function('f')(t)
g = s.Function('g')(x,y,z)
xi = [f*g, s.Integer(0), s.Integer(0), s.Integer(0)]
h = s.Matrix(4,4,lambda i,j:s.diff(xi[j],coords[i])+s.diff(xi[i],coords[j]))
def curvature(h,a,b,c,d):
    return s.simplify((s.diff(h[a,d],coords[b],coords[c])
        +s.diff(h[b,c],coords[a],coords[d])
        -s.diff(h[a,c],coords[b],coords[d])
        -s.diff(h[b,d],coords[a],coords[c]))/2)
riemann = [curvature(h,a,b,c,d) for a in range(4) for b in range(4)
           for c in range(4) for d in range(4)]
# TT wave in the x direction, superposed on arbitrary pure gauge lapse.
u = s.symbols('u', real=True)
F = s.Function('F')
wave = s.zeros(4); wave[2,2]=F(t-x);wave[3,3]=-F(t-x)
tidal = curvature(wave,0,2,0,2)
wave_box=s.diff(wave[2,2],t,2)-s.diff(wave[2,2],x,2)
combined=curvature(h+wave,0,2,0,2)
checks = dict(pure_gauge_all_256_curvatures_zero=all(v==0 for v in riemann),
    lapse_nonzero=h[0,0]!=0,
    elliptic_lapse_identity=s.simplify(sum(s.diff(h[0,0],q,2) for q in (x,y,z))
        -2*s.diff(f,t)*sum(s.diff(g,q,2) for q in (x,y,z)))==0,
    retarded_wave_equation=s.simplify(wave_box)==0,
    physical_tidal_nonzero=tidal!=0,
    arbitrary_lapse_does_not_change_tidal=s.simplify(combined-tidal)==0)
result=dict(checks=checks,lapse=str(h[0,0]),tidal=str(tidal),
    assertion_tested='An arbitrary time-dependent pure gauge lapse can satisfy a spatial Poisson identity with identically zero curvature. Adding it leaves a retarded TT wave tidal field unchanged.',
    interpretation='The elliptic lapse equation alone does not establish physical acausality. In sourced linearized GR, harmonic-gauge trace-reversed metric obeys a wave equation; stress conservation propagates its divergence constraint with zero initial constraint data.',
    scope='Exact GR control, not a sourced retarded-response calculation for v3s. Both a0 footings and both switch orientations share this GR control.',
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
for mode in ('main','mutate'):
    (HERE/mode/'gr_control.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
