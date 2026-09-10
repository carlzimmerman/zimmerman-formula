#!/usr/bin/env python3
"""Exact scaling checks, including the frozen coupled EF principal expression."""
import importlib.util
from pathlib import Path
import sys
import unittest
import sympy as s
import scaling_identities as h

SOURCE_ROOT=Path(__file__).resolve().parents[3]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    out=importlib.util.module_from_spec(spec);spec.loader.exec_module(out)
    return out


class ScalingTests(unittest.TestCase):
    def zero(self,e):
        self.assertEqual(s.factor(s.cancel(e)),0)

    def test_F_amplitude_weights(self):
        d=h.model();scale=s.Symbol('scale',positive=True)
        sub={d[k]:scale*d[k] for k in ('F','w','f','j')}
        for key,weight in h.F_SCALE_WEIGHTS.items():
            self.zero(d[key].subs(sub,simultaneous=True)-scale**weight*d[key])
        for entry in d['A']:
            self.zero(entry.subs(sub,simultaneous=True)-entry)

    def test_operator_weights_are_exact_not_assigned_N_values(self):
        d=h.model();variables=d['variables'];euler=d['scale_vector']
        # Geometry can depend arbitrarily on y: Euler has no y component and
        # no coefficient below differentiates a geometry symbol under scaling.
        for v in h.bracket(euler,d['L0'],variables):self.zero(v)
        for v in h.bracket(euler,d['L1'],variables)+d['L1']:self.zero(v)
        for key in ('kappa','gamma'):
            self.zero(h.derivative(d[key],variables,euler))

    def test_full_flow_equivariance(self):
        d=h.model();scale=s.Symbol('scale',positive=True)
        sub={d[k]:scale*d[k] for k in ('F','w','f','j')}
        flow=d['L0']+d['f']*d['L1']
        for entry,weight in zip(flow,(0,1,0,0,1)):
            self.zero(entry.subs(sub,simultaneous=True)-scale**weight*entry)

    def test_matching_next_control_and_determinant_scaling(self):
        scale=s.Symbol('scale',positive=True)
        A1,A2,B1,B2,N1,N2,f,j=s.symbols('A1 A2 B1 B2 N1 N2 f j',real=True)
        for A,B,N in ((A1,B1,N1),(A2,B2,N2)):
            self.zero(A+(scale*f)*(B/scale)-(A+f*B))
            self.zero(N+(scale*j)*(B/scale)-(N+j*B))
        self.zero(N1*(B2/scale)-N2*(B1/scale)-(N1*B2-N2*B1)/scale)
        nonzero_B=s.Symbol('nonzero_B',nonzero=True)
        self.zero(-N1/(nonzero_B/scale)-scale*(-N1/nonzero_B))

    def test_EF_action_dictionary_amplitude_weights(self):
        ef=load('scaling_ef',SOURCE_ROOT/'closure_2026/kgb_nonaffine_clock_2026/dictionary/general_ef.py')
        X,C,C1,C2,P,PX,PXX,GX,GXX=s.symbols('X C C1 C2 P PX PXX GX GXX',nonzero=True)
        scale=s.Symbol('scale',positive=True)
        values=(X,C,C1,C2,P,PX,PXX,GX,GXX)
        original=ef.action_dictionary(*values)
        moved=ef.action_dictionary(X,*[scale*v for v in values[1:]])
        for key,weight in {'chi':-1,'P':-1,'P1':0,'P2':1,'G1':1,'G2':2}.items():
            self.zero(moved[key]-scale**weight*original[key])
        rr,AA,BB,pp,CC=s.symbols('radius lapse radial p Cpositive',positive=True)
        gg,bb,pr,z=s.symbols('g BrB pr z',real=True)
        bg=ef.background_dictionary(rr,AA,BB,gg,bb,pp,pr,X,z,CC,C1,sqrt=s.sqrt)
        moved_bg=ef.background_dictionary(rr,AA,BB,gg,bb,pp,pr,X,z,scale*CC,scale*C1,sqrt=s.sqrt)
        for original_v,new_v in zip(bg['v'],moved_bg['v']):
            self.zero(new_v-original_v/s.sqrt(scale))
        for i in range(4):
            for j in range(4):self.zero(moved_bg['H'][i][j]-bg['H'][i][j]/scale)

    def test_frozen_EF_principal_and_stress_scale(self):
        raw=load('scaling_kgb',SOURCE_ROOT/'closure_2026/ticking_kgb_inverse_2026/kgb_inverse.py')
        a=raw.principal_template();t=s.Symbol('sqrt_scale',positive=True)
        sub={a['P']:a['P']/t**2,a['P2']:t**2*a['P2'],
             a['G1']:t**2*a['G1'],a['G2']:t**4*a['G2']}
        sub.update({v:v/t for v in a['v']})
        sub.update({a['H'][i,j]:a['H'][i,j]/t**2 for i in range(4) for j in range(i,4)})
        for i in range(4):
            for j in range(i,4):
                self.zero(a['M'][i,j].subs(sub,simultaneous=True)-a['M'][i,j])
                self.zero(a['T'][i,j].subs(sub,simultaneous=True)-a['T'][i,j]/t**2)

    def test_clock_algebra_covariance_is_not_fixed_metric_symmetry(self):
        d=h.model();t=s.Symbol('clock_scale',positive=True)
        sub={d['X']:t*d['X'],d['U']:t*d['U'],d['f']:d['f']/t,d['j']:d['j']/t**2}
        for key,weight in h.CLOCK_SCALE_WEIGHTS.items():
            self.zero(d[key].subs(sub,simultaneous=True)-t**weight*d[key])
        self.zero(d['A'][0].subs(sub,simultaneous=True)-d['A'][0]/t)
        self.zero(d['A'][1].subs(sub,simultaneous=True)-d['A'][1]/t**s.Rational(3,2))

    def test_fixed_q_requires_a_changed_lapse_under_clock_scale(self):
        d=h.model();t=s.Symbol('clock_scale',positive=True)
        lapse=1/d['Q'];new_lapse=1/(t*d['Q'])
        self.zero(new_lapse-lapse/t)
        # Keeping q=-1 and the old A violates the new norm constraint unless t=1.
        norm_mismatch=t*d['X']-(1/lapse-t*d['U'])/2
        self.zero(norm_mismatch-(t-1)*d['Q']/2)
        # If the clock field is redefined, changing q as well restores the norm.
        self.zero(t*d['X']-(t/lapse-t*d['U'])/2)


if __name__=='__main__':
    print('EXACT_SCALING Python='+sys.version.split()[0]+' SymPy='+s.__version__,flush=True)
    unittest.main(verbosity=2)
