"""Exact meridional rays and phase-only Gaussian overlap diagnostic."""
import json,math,sys
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq,least_squares
p=json.loads(Path('sol61_push/shell_resonator_2026_10_14/run/results.json').read_text())
material=json.loads(Path('sol61_push/silica_shell_retention_2026_10_14/run/results.json').read_text())
a=p['inner_radius_m'];b=p['outer_radius_m'];n=material['refractive_index'];w0=p['center_waist_m'];wavelength=material['optical_wavelength_um']*1e-6
case=p['resonators'][-1];L=case['mirror_distance_from_center_m'];R=case['mirror_radius_of_curvature_m']
sag_coeff=np.zeros(2); mirror_scale=case["mirror_spot_radius_m"]
checks=[];worst_snell=0.;worst_norm=0.
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
def hit(pos,direction,center,radius):
    offset=pos-center; proj=np.dot(offset,direction)
    disc=proj*proj+radius*radius-np.dot(offset,offset);assert disc>=0
    roots=[-proj-math.sqrt(disc),-proj+math.sqrt(disc)]
    distance=min(t for t in roots if t>1e-12)
    return pos+distance*direction,distance

def refract(direction,normal,n1,n2):
    global worst_snell,worst_norm
    normal=normal/np.linalg.norm(normal)
    tangent=direction-np.dot(direction,normal)*normal
    transmitted=(n1/n2)*tangent
    remainder=1-np.dot(transmitted,transmitted);assert remainder>0
    out=transmitted+math.sqrt(remainder)*normal
    worst_snell=max(worst_snell,float(np.linalg.norm(n1*tangent-n2*(out-np.dot(out,normal)*normal))))
    worst_norm=max(worst_norm,abs(float(np.linalg.norm(out))-1))
    return out

def ray(radius):
    pos=np.array([radius,0.]);direction=np.array([0.,1.]);origin=np.zeros(2);opl=0.
    for surface,n1,n2 in [(a,1.,n),(b,n,1.)]:
        pos,travel=hit(pos,direction,origin,surface);opl+=n1*travel
        direction=refract(direction,pos/surface,n1,n2)
    center=np.array([0.,L-R]);_,estimate=hit(pos,direction,center,R)
    def surface(x):
        h=x/mirror_scale
        return L-R+math.sqrt(R*R-x*x)+1e-6*(sag_coeff[0]*h**4+sag_coeff[1]*h**6)
    equation=lambda t:pos[1]+t*direction[1]-surface(pos[0]+t*direction[0])
    travel=brentq(equation,estimate-.0001,estimate+.0001,xtol=1e-15)
    pos=pos+travel*direction;opl+=travel
    h=pos[0]/mirror_scale
    slope=-pos[0]/math.sqrt(R*R-pos[0]**2)+1e-6/mirror_scale*(4*sag_coeff[0]*h**3+6*sag_coeff[1]*h**5)
    normal=np.array([-slope,1.]);normal/=np.linalg.norm(normal)
    direction=direction-2*np.dot(direction,normal)*normal
    for surface,n1,n2 in [(b,1.,n),(a,n,1.)]:
        pos,travel=hit(pos,direction,origin,surface);opl+=n1*travel
        direction=refract(direction,-pos/surface,n1,n2)
    travel=-pos[1]/direction[1];assert travel>0
    pos=pos+travel*direction;opl+=travel
    return float(pos[0]),float(opl),float(direction[0]),float(direction[0]/(-direction[1]))
# Check exact rays approach independent ABCD central-plane/mirror/central-plane map.
P=lambda d:np.array([[1.,d],[0.,1.]])
M=P(L-b)@np.array(p['shell_transfer_matrix'])@P(a)
reverse=np.array([[M[1,1],M[0,1]],[M[1,0],M[0,0]]])
F=reverse@np.array([[1.,0],[-2/R,1.]])@M
small=ray(1e-7)
ck('paraxial_height_limit',abs(small[0]/1e-7-F[0,0]),2e-8)
ck('paraxial_angle_limit',abs(small[3]/1e-7-F[1,0]),2e-7)
ck('on_axis_optical_length',abs(ray(0)[1]-(2*L+2*(n-1)*(b-a))),1e-14)
# Fermat/eikonal check: d(OPL)/d(output radius) equals final tangential momentum.
for r in [.0005,.001,.002,.004]:
    delta=2e-7;lo=ray(r-delta);hi=ray(r+delta);mid=ray(r)
    derivative=(hi[1]-lo[1])/(hi[0]-lo[0])
    ck('eikonal_endpoint_derivative',abs(derivative-mid[2]),2e-8)
def evaluate(N,waist,residual_only=False):
    t,weights=leggauss(N); radii=(t+1)*3*waist/2; weights=weights*3*waist/2
    weights=weights*radii*np.exp(-2*(radii/waist)**2);weights/=sum(weights)
    rays=np.array([ray(float(r)) for r in radii]);out=rays[:,0];opl=rays[:,1]-ray(0)[1]
    # Remove piston and defocus with a weighted least-squares projection.
    design=np.column_stack((np.ones(N),(out/waist)**2))
    coef=np.linalg.lstsq(design*np.sqrt(weights[:,None]),opl*np.sqrt(weights),rcond=None)[0]
    residual=opl-design@coef
    if residual_only:return np.sqrt(weights)*residual/1e-9
    rms=math.sqrt(float(np.dot(weights,residual**2)))
    overlap=abs(np.dot(weights,np.exp(2j*math.pi*residual/wavelength)))**2
    return dict(quadrature_nodes=N,weight_waist_m=waist,wavefront_RMS_m=rms,wavefront_RMS_waves=rms/wavelength,phase_only_overlap=float(overlap),phase_only_mismatch=1-float(overlap),fitted_piston_m=float(coef[0]),fitted_quadratic_m=float(coef[1]),maximum_sampled_ray_height_mapping_deviation_m=float(np.max(abs(out-F[0,0]*radii))))

unmodified=evaluate(192,w0)
def objective(params):
    global sag_coeff
    sag_coeff=np.asarray(params)
    return evaluate(64,w0,True)
def jacobian(params):
    step=.001;columns=[]
    for j in range(2):
        change=np.zeros(2);change[j]=step
        columns.append((objective(params+change)-objective(params-change))/(2*step))
    objective(params)
    return np.column_stack(columns)
fit=least_squares(objective,np.zeros(2),jac=jacobian,xtol=1e-11,ftol=1e-11,gtol=1e-9,max_nfev=80)
assert fit.success,fit.message
sag_coeff=fit.x.copy()
base=evaluate(96,w0);fine=evaluate(192,w0)
ck('wavefront_quadrature_absolute_m',abs(base['wavefront_RMS_m']-fine['wavefront_RMS_m']),1e-13)
ck('overlap_quadrature',abs(base['phase_only_overlap']-fine['phase_only_overlap']),1e-10)
# Recheck endpoint eikonal relation after changing the mirror surface.
for r in [.0005,.001,.002,.004]:
    lo=ray(r-2e-7);hi=ray(r+2e-7);mid=ray(r)
    ck('corrected_eikonal_derivative',abs((hi[1]-lo[1])/(hi[0]-lo[0])-mid[2]),2e-8)
ck('Snell_tangent_continuity',worst_snell,1e-14);ck('refracted_unit_vectors',worst_norm,1e-14)
ck('phase_only_mismatch_target',fine['phase_only_mismatch'],1e-6)
best=sag_coeff.copy();sensitivity=[]
for error_nm in [-1.,-.1,.1,1.]:
    sag_coeff=best+np.array([error_nm*.001,0.])
    sensitivity.append(dict(quartic_coefficient_error_nm=error_nm,diagnostic=evaluate(96,w0)))
sag_coeff=best
result=dict(scope='Quartic/sextic mirror fit to one-sided geometric wavefront; phase-only diagnostic, not a diffractive cavity eigenmode',mirror_case=case,mirror_radial_scale_m=mirror_scale,sag_coefficients_m=(sag_coeff*1e-6).tolist(),quartic_coefficient_sensitivity=sensitivity,optimizer_message=fit.message,optimizer_evaluations=fit.nfev,unmodified=unmodified,corrected=base,refined=fine,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
