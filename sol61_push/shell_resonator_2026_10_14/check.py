"""Scalar paraxial resonator containing a concentric silica shell."""
import json,math,sys
from pathlib import Path
import numpy as np
p=json.loads(Path('sol61_push/silica_shell_retention_2026_10_14/run/results.json').read_text())
n=p['refractive_index']; wavelength=p['optical_wavelength_um']*1e-6
a=.02;b=.025;w0=.002;zR=math.pi*w0*w0/wavelength;q0=1j*zR
checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
def P(d):return np.array([[1.,d],[0,1.]])
def S(n1,n2,R):return np.array([[1.,0],[(n1-n2)/(n2*R),n1/n2]])
def apply(M,q):return (M[0,0]*q+M[0,1])/(M[1,0]*q+M[1,1])
def spot(q,index=1.):return math.sqrt(-wavelength/(math.pi*index*(1/q).imag))
shell=S(n,1,-b)@P(b-a)@S(1,n,-a)
ck('shell_unimodular',abs(np.linalg.det(shell)-1),1e-14)
qinner=apply(P(a),q0);qglass=apply(S(1,n,-a),qinner)
ck('spot_continuity_inner',abs(spot(qinner)/spot(qglass,n)-1),1e-14)
qouterglass=apply(P(b-a),qglass);qouter=apply(S(n,1,-b),qouterglass)
ck('spot_continuity_outer',abs(spot(qouter)/spot(qouterglass,n)-1),1e-14)
rows=[]
for distance in [.1,.25,.5]:
    M=P(distance-b)@shell@P(a); qm=apply(M,q0)
    radius=1/(1/qm).real
    mirror=np.array([[1.,0],[-2/radius,1.]])
    reverse=np.array([[M[1,1],M[0,1]],[M[1,0],M[0,0]]])
    half=reverse@mirror@M;roundtrip=half@half
    ck('roundtrip_q_fixed_point',abs(apply(roundtrip,q0)-q0)/abs(q0),1e-10)
    ck('roundtrip_unimodular',abs(np.linalg.det(roundtrip)-1),1e-12)
    trace=float(np.trace(roundtrip)/2);assert abs(trace)<1
    # Solve the fixed-point quadratic independently, selecting Im(q)>0.
    roots=np.roots([roundtrip[1,0],roundtrip[1,1]-roundtrip[0,0],-roundtrip[0,1]])
    stable=next(r for r in roots if r.imag>0)
    ck('independent_q_quadratic',abs(stable-q0)/abs(q0),1e-9)
    wm=spot(qm);aperture=wm*math.sqrt(math.log(1e6)/2)
    rows.append(dict(mirror_distance_from_center_m=distance,full_cavity_length_m=2*distance,mirror_radius_of_curvature_m=radius,mirror_spot_radius_m=wm,mirror_clear_radius_for_1ppm_Gaussian_clipping_m=aperture,roundtrip_half_trace=trace,mirror_wavefront_slope_at_one_spot_radius=wm/radius, symmetric_radius_stability_interval_m=[float(M[0,1]/M[1,1]),float(M[0,0]/M[1,0])], nearest_symmetric_radius_stability_margin_m=min(radius-M[0,1]/M[1,1],M[0,0]/M[1,0]-radius)))
R=p['uncoated_normal_single_interface_reflectance']; transmission=(1-R)**4
# Conditional incoherent rejection of all reflected branches: not absorptive loss.
roundtrip_loss=1-transmission**2
power=math.pi*w0*w0*1e12/2
result=dict(scope='Ideal on-axis scalar paraxial Gaussian mode; excludes aberration, coating phases, coherent internal reflections and thermal deformation',inner_radius_m=a,outer_radius_m=b,center_waist_m=w0,center_Rayleigh_length_m=zR,shell_transfer_matrix=shell.tolist(),inner_surface_spot_m=spot(qinner),outer_surface_spot_m=spot(qouter),max_inside_intensity_fraction_change=1-1/(1+(a/zR)**2),resonators=rows,required_circulating_power_per_wave_W=power,uncoated_main_branch_power_transmission_across_four_interfaces=transmission,incoherent_rejected_branch_roundtrip_fraction=roundtrip_loss,single_input_forward_wave_power_diagnostic_W=power*roundtrip_loss/(1-R)**2, balanced_center_waves_discarded_branch_power_W=2*power*(1-transmission)/(1-R)**2,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
