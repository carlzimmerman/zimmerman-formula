#!/usr/bin/env python3
"""Joint arbitrary-precision RK4 integration of the unchanged action.

State: three barred coefficient variables, six physical background variables,
and all 36 finite-k transfer entries. Barred variables obey their ORIGINAL
tau ODE multiplied by the solved physical tau rate, never a fitted target.
Cubic Hermite output is differentiated independently within a locked segment.
Only a short, dimensionless, single-k convergence experiment is claimed.
"""
import argparse
import json
from pathlib import Path
import mpmath as mp
import numpy as np
from transfer_evolve import Background, ALIASES, FIELDS
from transfer_precision import PrecisionEvaluator, precision_clone, mp_solve, object_array


def hermite(y0, y1, f0, f1, h, x):
    return ((2*x**3-3*x*x+1)*y0+(x**3-2*x*x+x)*h*f0
            +(-2*x**3+3*x*x)*y1+(x**3-x*x)*h*f1)


class Coupled:
    def __init__(self):
        bg = Background(.02)
        self.evaluator = PrecisionEvaluator(bg, bg.solution, .3)
        self.flow = precision_clone(bg.model.flowfunc)
        self.gamma = mp.mpf(bg.model.gamma)
        self.k = mp.mpf(.3)
        initial = [mp.mpf(x) for x in (1., .1, .5)]
        initial += [mp.mpf(float(x)) for x in bg.solution.y[:, 0]]
        initial += [mp.mpf(int(i == j)) for i in range(6) for j in range(6)]
        self.initial = mp.matrix(initial)

    def at(self, state):
        e = self.evaluator
        raw = e.bg_coefficients(*list(state[:3]))
        a, H, q, tau, rho, rad = list(state[3:9])
        if min(a, rho, rad, raw[1]-2*raw[2]*q*q,
               raw[1]-2*raw[2]*raw[0]**2) <= 0:
            raise ValueError('positive background or logarithm domain lost')
        jets = dict(zip(e.bg.model.names, e.jets(*raw, q*q, mp.mpf(0), self.gamma)))
        jets.update(zip(e.extra_names, e.extra(*raw, q*q, self.gamma)))
        v = {name: jets[alias] for name, alias in ALIASES.items()}
        v.update(a=a, H=H, q=q, rho=rho, Cr=mp.mpf(1), M2=mp.mpf(1),
                 Lambda=mp.mpf(.7), gamma=self.gamma, qr=(rad/3)**mp.mpf('.25'))
        out = object_array(e.background_system(*[v[x] for x in e.bg.names]))
        Hd, qd, s0 = mp_solve(out[:9].reshape(3, 3), out[9:12])
        if s0 <= 0:
            raise ValueError('positive clock rate lost')
        v.update(Hd=Hd, qd=qd, sbar=s0, qrd=-H*v['qr'], rhod=-3*H*rho)
        return v, out[12:14]

    def rhs(self, state):
        v, _ = self.at(state)
        barred = [x*v['sbar'] for x in self.flow(*list(state[:3]))]
        physical = [v['a']*v['H'], v['Hd'], v['qd'], v['sbar'],
                    v['rhod'], -4*v['H']*state[8]]
        u = object_array(list(state[9:])).reshape(6, 6)
        ud = self.evaluator.mode(v, self.k)[0]@u
        return mp.matrix(barred+physical+list(ud.flat))

    def fields(self, state):
        v, _ = self.at(state)
        u = object_array(list(state[9:])).reshape(6, 6)
        _, _, lapse, z, b, _ = self.evaluator.mode(v, self.k)
        fields = object_array([z@u, np.zeros(6, dtype=object), u[0], u[2],
                              u[4], u[5], lapse@u, b@u])
        return mp.matrix(fields.tolist())

    def integrate(self, step):
        h = mp.mpf(step)
        count = int(mp.nint(mp.mpf('.02')/h))
        if abs(count*h-mp.mpf('.02')) > mp.mpf('1e-25'):
            raise ValueError('step must divide 0.02')
        states = [self.initial.copy()]
        slopes = [self.rhs(states[0])]
        for _ in range(count):
            y, k1 = states[-1], slopes[-1]
            k2 = self.rhs(y+h*k1/2)
            k3 = self.rhs(y+h*k2/2)
            k4 = self.rhs(y+h*k3)
            states.append(y+h*(k1+2*k2+2*k3+k4)/6)
            slopes.append(self.rhs(states[-1]))
        maximum = np.zeros(8, dtype=object)
        momentum_max = slip_max = constraint_max = mp.mpf(0)
        knot_distances = []
        for text in ('.00413', '.01037', '.01591'):
            t = mp.mpf(text)
            index = int(mp.floor(t/h))
            knot_distances.append(float(min(t-index*h, (index+1)*h-t)))
            # Lock this segment before differentiation; no search inside f.
            def state_at(time):
                return hermite(states[index], states[index+1], slopes[index],
                               slopes[index+1], h, (time-index*h)/h)
            field_at = lambda time: self.fields(state_at(time))
            f = object_array(field_at(t).tolist())
            fd = object_array(mp.diff(field_at, t, 1).tolist())
            fdd = object_array(mp.diff(field_at, t, 2).tolist())
            jets = np.stack([f, fd, fdd], axis=1).reshape(24, 6)
            v, constraints = self.at(state_at(t))
            constraint_max = max(constraint_max, max(abs(constraints)))
            v['k'] = self.k
            matrix = self.evaluator.euler(*[v[x] for x in self.evaluator.euler_names])
            scaled = abs(matrix@jets)/(1+abs(matrix)@abs(jets))
            maximum = np.maximum(maximum, np.max(scaled, axis=1))
            u = object_array(list(state_at(t)[9:])).reshape(6, 6)
            current = self.evaluator.mode(v, self.k)[-1]@u
            mom = 2*v['M2']*(fd[0]-v['H']*f[6])+current
            momentum_max = max(momentum_max, max(abs(mom)/
                (1+abs(2*v['M2']*fd[0])+abs(2*v['M2']*v['H']*f[6])+abs(current))))
            Phi = f[6]-v['a']**2*(fd[7]+2*v['H']*f[7])/self.k
            Psi = -f[0]+v['H']*v['a']**2*f[7]/self.k
            slip_max = max(slip_max, max(abs(Phi-Psi)/(1+abs(Phi)+abs(Psi))))
        return dict(step=float(h), max_scaled_euler=float(max(maximum)),
                    euler_by_field=dict(zip(FIELDS, map(float, maximum))),
                    max_scaled_momentum=float(momentum_max), max_scaled_slip=float(slip_max),
                    max_background_constraint=float(constraint_max),
                    min_sample_knot_distance=min(knot_distances),
                    transfer_end=[float(x) for x in states[-1][9:]])


def run(steps=('.002', '.001', '.0005'), digits=40):
    with mp.workdps(digits):
        model = Coupled()
        rows = [model.integrate(step) for step in steps]
    return dict(rows=rows, decimal_digits=digits, k=.3, t_end=.02,
                sample_times=[.00413, .01037, .01591],
                scope='Joint RK4/Hermite arbitrary-precision short trajectory; no equation assigns metric derivatives; not global convergence or CMB',
                full_theory_status='OPEN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file', type=Path, required=True)
    parser.add_argument('--digits', type=int, default=40)
    args = parser.parse_args()
    result = run(digits=args.digits)
    args.result_file.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({**result, 'rows': [{k:v for k,v in row.items() if k!='transfer_end'}
                                        for row in result['rows']]}, indent=2))
