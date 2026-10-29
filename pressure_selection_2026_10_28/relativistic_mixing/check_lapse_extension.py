#!/usr/bin/env python3
"""Finite-box lapse extension. Fixed fugacities; no Einstein-equation solve."""
import json, math, sys
from pathlib import Path
from scipy.integrate import quad
from scipy.special import logsumexp
from check_relativistic_mixing import logZ,D

def run_case(zmin,zmax):
    nodes=[.8,1.2]; volumes=[1.,2.]
    def logQ(z): return logZ(z)-z
    def denom(z): return float(logsumexp([math.log(v)+logQ(n*z) for n,v in zip(nodes,volumes)]))
    def moments(N):
        def ratio(u):
            z=math.exp(u); return math.exp(logQ(N*z)-denom(z))
        lo,hi=math.log(zmin),math.log(zmax)
        n=quad(lambda u:math.exp(u)*ratio(u),lo,hi,epsabs=1e-12,epsrel=1e-11)[0]
        p=quad(lambda u:ratio(u)/N,lo,hi,epsabs=1e-11,epsrel=1e-11)[0]
        en=quad(lambda u:ratio(u)*(D(N*math.exp(u))+N*math.exp(u))/N,
                lo,hi,epsabs=1e-11,epsrel=1e-11)[0]
        return n,p,en
    rows=[moments(n) for n in nodes]
    totaln=sum(v*r[0] for v,r in zip(volumes,rows))
    totalKilling=sum(v*n*r[2] for v,n,r in zip(volumes,nodes,rows))
    slope=math.log(rows[1][1]/rows[0][1])/math.log(rows[1][0]/rows[0][0])
    N=1.; h=1e-4; n,p,en=moments(N)
    # Five-point derivative of P w.r.t log lapse at fixed global normalization.
    derivative=(-moments(N*math.exp(2*h))[1]+8*moments(N*math.exp(h))[1]
                -8*moments(N*math.exp(-h))[1]+moments(N*math.exp(-2*h))[1])/(12*h)
    return {'zmin':zmin,'zmax':zmax,'lapse_nodes':nodes,'proper_volumes':volumes,
            'local_rows':[{'N':N,'n':r[0],'P':r[1],'total_energy_density':r[2]} for N,r in zip(nodes,rows)],
            'number_conservation_relative_error':totaln/(zmax-zmin)-1,
            'Killing_energy':totalKilling,'UR_Killing_energy_target':3*math.log(zmax/zmin),
            'effective_two_point_pressure_density_slope':slope,
            'hydrostatic_identity_relative_error':derivative/(-(en+p))-1}

cases=[run_case(1e-10,1e-6),run_case(.01,100.)]
checks={'phase_level_number_conservation':max(abs(r['number_conservation_relative_error']) for r in cases)<1e-10,
        'UR_pressure_density_slope':abs(cases[0]['effective_two_point_pressure_density_slope']-4/3)<1e-9,
        'UR_Killing_energy':abs(cases[0]['Killing_energy']/cases[0]['UR_Killing_energy_target']-1)<1e-10,
        'relativistic_hydrostatic_identity':max(abs(r['hydrostatic_identity_relative_error']) for r in cases)<2e-8}
assert all(checks.values()),checks
out={'claim_id':'PN28_RELATIVISTIC_LAPSE_DISCRIMINATOR','checks':checks,'cases':cases,
     'non_claims':['No solution of Einstein equations','No self-consistent halo','No proof from the two-point numerical slope; analytic UR scaling supplies the proof']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
