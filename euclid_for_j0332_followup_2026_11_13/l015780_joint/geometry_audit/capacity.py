"""Fixed-field source-position capacity with independent finite lower witnesses.

Released positions are model-conditioned association information, not Gaussian
astrometric errors. This diagnostic is not an image likelihood or theory p-value.
"""
import argparse,csv,json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize,linprog,brentq
from astropy.io import fits

HERE=Path(__file__).resolve().parent
FOLLOWUP=HERE.parents[1]
INPUT=FOLLOWUP/'l015780_inputs'
ZL=.428270373960303
OM=.3089
IINF=quad(lambda t:2/np.sqrt(OM+(1-OM)*t**6),0,1,epsabs=1e-13)[0]
IL=quad(lambda z:1/np.sqrt(OM*(1+z)**3+1-OM),0,ZL,epsabs=1e-13)[0]
BMAX=1-IL/IINF


def clean(x):
    if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
    if isinstance(x,list):return [clean(v) for v in x]
    if isinstance(x,np.generic):return x.item()
    return x


def sie_parameters(name):
    c=json.loads((INPUT/'results'/name).read_text())
    v=lambda p,k:p[k]['point_estimate']['value']
    p=c['lensing_entities'][0]['mass_model'][0]['parameters']
    s=c['lensing_entities'][2]['mass_model'][0]['parameters']
    angle=np.pi/2+np.deg2rad(v(p,'phi'))
    ga=np.pi/2+np.deg2rad(v(s,'phi_ext'));gamma=v(s,'gamma_ext')
    return dict(theta=v(p,'theta_E'),q=v(p,'q'),angle=angle,
        cx=v(p,'center_x'),cn=v(p,'center_y'),g1=gamma*np.cos(2*ga),g2=gamma*np.sin(2*ga))


def sie(X,N,p):
    co,si=np.cos(p['angle']),np.sin(p['angle'])
    u=co*(X-p['cx'])+si*(N-p['cn']);v=-si*(X-p['cx'])+co*(N-p['cn'])
    psi=np.maximum(np.sqrt(p['q']**2*u*u+v*v),1e-30);f=np.sqrt(1-p['q']**2)
    au=p['theta']*np.sqrt(p['q'])/f*np.arctan(f*u/psi)
    av=p['theta']*np.sqrt(p['q'])/f*np.arctanh(f*v/psi)
    return np.array([co*au-si*av+p['g1']*X+p['g2']*N,
        si*au+co*av+p['g2']*X-p['g1']*N])


def effective_radius(p):
    z,w=np.polynomial.legendre.leggauss(512);angle=(z+1)*np.pi;w=w*np.pi
    metric=np.sqrt(p['q']**2*np.cos(angle-p['angle'])**2+np.sin(angle-p['angle'])**2)
    rc=p['theta']*np.sqrt(p['q'])/metric*(1-p['g1']*np.cos(2*angle)-p['g2']*np.sin(2*angle))/(1-p['g1']**2-p['g2']**2)
    return float(np.sqrt(.5*np.sum(w*rc*rc)/np.pi))


def diameter(b):
    return float(np.max(np.linalg.norm(b[:,None,:]-b[None,:,:],axis=-1)))


def exact_null_basis(theta):
    """Rational source/shear null space from the released .05arcsec grid."""
    scaled=np.rint(theta*20).astype(int)
    assert np.max(np.abs(scaled/20-theta))<1e-12
    n=len(theta)
    matrix=[]
    matrix.append([F(1 if j%2==0 else 0) for j in range(2*n)])
    matrix.append([F(1 if j%2 else 0) for j in range(2*n)])
    matrix.append([F(int(scaled[j//2,0] if j%2==0 else -scaled[j//2,1])) for j in range(2*n)])
    matrix.append([F(int(scaled[j//2,1] if j%2==0 else scaled[j//2,0])) for j in range(2*n)])
    original=[r.copy() for r in matrix]
    pivots=[];row=0
    for col in range(2*n):
        candidates=[i for i in range(row,len(matrix)) if matrix[i][col]]
        if not candidates:continue
        j=candidates[0];matrix[row],matrix[j]=matrix[j],matrix[row]
        d=matrix[row][col];matrix[row]=[x/d for x in matrix[row]]
        for i in range(len(matrix)):
            if i!=row:
                d=matrix[i][col];matrix[i]=[x-d*y for x,y in zip(matrix[i],matrix[row])]
        pivots.append(col);row+=1
        if row==len(matrix):break
    vectors=[]
    for free in [i for i in range(2*n) if i not in pivots]:
        v=[F(0)]*(2*n);v[free]=F(1)
        for i,p in enumerate(pivots):v[p]=-matrix[i][free]
        assert all(sum(x*y for x,y in zip(r,v))==0 for r in original)
        vectors.append(v)
    return np.array([[float(v[j]) for v in vectors] for j in range(2*n)]),vectors


def rational_sqrt_upper(q):
    if q==0:return F(0)
    x=math.sqrt(float(q))
    result=F.from_float(math.nextafter(x,math.inf))
    while result*result<q:
        result=F.from_float(math.nextafter(float(result),math.inf))
    return result


def rational_down(q):
    value=float(q)
    while F.from_float(value)>q:value=math.nextafter(value,-math.inf)
    return value


def arbitrary_shear_witness(theta,alpha,beta_max,basis):
    numeric,exact=basis;n=len(theta)
    Q=np.linalg.qr(numeric)[0]
    y=theta.ravel();a=alpha.ravel()
    yp=Q@(Q.T@y);ap=Q@(Q.T@a)
    beta=float(np.clip(np.dot(yp,ap)/np.dot(ap,ap),0,beta_max))
    residual=yp-beta*ap
    coefficients=np.linalg.lstsq(numeric,residual,rcond=None)[0]
    # Coefficients and basis below are exact rationals. Both source offsets
    # and both unrestricted shear terms therefore cancel exactly.
    coefficient_f=[F.from_float(float(x)) for x in coefficients]
    w=[sum(coefficient_f[k]*exact[k][j] for k in range(len(exact))) for j in range(2*n)]
    th=[F(int(round(float(x)*20)),20) for x in y]
    ah=[F.from_float(float(x)) for x in a]
    intercept=sum(x*z for x,z in zip(w,th));slope=sum(x*z for x,z in zip(w,ah))
    left=intercept;right=intercept-F.from_float(float(beta_max))*slope
    separation=F(0) if min(left,right)<=0<=max(left,right) else min(abs(left),abs(right))
    denominator=F(0)
    for i in range(n):
        for j in range(i):
            dx,dy=w[2*i]-w[2*j],w[2*i+1]-w[2*j+1]
            denominator+=rational_sqrt_upper(dx*dx+dy*dy)
    lower=F(0) if denominator==0 else n*separation/denominator
    return dict(beta_of_projected_least_squares=beta,
        residual_SSE=float(np.dot(residual,residual)),
        generic_SSE_diameter_lower_bound=float(np.sqrt(2*np.dot(residual,residual)/(n-1))),
        certified_finite_array_diameter_lower_bound_arcsec=rational_down(lower),
        lower_bound_exact_rational=str(lower),
        witness_intercept_exact_rational=str(intercept),witness_slope_exact_rational=str(slope),
        witness_pair_norm_sum_upper_exact_rational=str(denominator),
        exact_witness_weights=[str(x) for x in w],
        scope='Exact rational nuisance cancellation and conservative square-root rounding for stored finite arrays; not an absolute physical field-error bound')


def supporting_lp(objective,eq,rhs,ineq,bound):
    result=linprog(-objective,A_ub=np.array(ineq) if ineq else None,b_ub=bound if ineq else None,
        A_eq=np.array(eq),b_eq=rhs,bounds=(0,None),method='highs',
        options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    if not result.success and len(eq)>1:
        # The primal directions are finite-precision. Relax stationarity
        # equations only; the actual dual objective below is independently
        # recomputed and remains a valid bound for any nonnegative weights.
        ai=list(ineq);bi=list(bound)
        for e,v in zip(eq[1:],rhs[1:]):
            tol=1e-7*max(1.,float(np.linalg.norm(e)))
            ai.extend([e,-e]);bi.extend([v+tol,-v+tol])
        result=linprog(-objective,A_ub=np.array(ai),b_ub=bi,
            A_eq=np.array(eq[:1]),b_eq=rhs[:1],bounds=(0,None),method='highs')
    return result


def capacity(theta,alpha,beta_max,gamma_max,basis):
    n=len(theta);ii=np.triu_indices(n,1)
    dt=theta[ii[0]]-theta[ii[1]];da=alpha[ii[0]]-alpha[ii[1]]
    h1=np.column_stack([dt[:,0],-dt[:,1]]);h2=dt[:,::-1]
    design=np.stack([da,h1,h2],axis=2)
    centered=theta-theta.mean(axis=0);ac=alpha-alpha.mean(axis=0)
    G1=np.column_stack([centered[:,0],-centered[:,1]]);G2=centered[:,::-1]
    A=np.column_stack([ac.ravel(),G1.ravel(),G2.ravel()])
    guess=np.linalg.lstsq(A,centered.ravel(),rcond=None)[0]
    guess[0]=np.clip(guess[0],0,beta_max)
    gnorm=np.linalg.norm(guess[1:])
    if gnorm>gamma_max:guess[1:]*=gamma_max/gnorm
    def residual(p):return dt-np.einsum('kij,j->ki',design,p[:3])
    def constraint(p):return p[3]-np.linalg.norm(residual(p),axis=1)
    def jac(p):
        r=residual(p);norms=np.maximum(np.linalg.norm(r,axis=1),1e-30)
        return np.column_stack([np.einsum('ki,kij->kj',r,design)/norms[:,None],np.ones(len(dt))])
    constraints=[dict(type='ineq',fun=constraint,jac=jac)]
    if gamma_max>0:
        constraints.append(dict(type='ineq',fun=lambda p:gamma_max**2-p[1]**2-p[2]**2,
            jac=lambda p:np.array([0.,-2*p[1],-2*p[2],0.])))
    opts=[]
    for g in [guess,np.array([beta_max,0.,0.])]:
        p0=np.r_[g,np.max(np.linalg.norm(residual(g),axis=1))+.01]
        opt=minimize(lambda p:p[3],p0,jac=lambda p:np.array([0.,0.,0.,1.]),method='SLSQP',
            bounds=[(0,beta_max),(-gamma_max,gamma_max),(-gamma_max,gamma_max),(0,None)],
            constraints=constraints,options={'ftol':1e-12,'maxiter':300})
        p=opt.x.copy();p[0]=np.clip(p[0],0,beta_max)
        ng=np.linalg.norm(p[1:3])
        if ng>gamma_max:p[1:3]*=gamma_max/ng
        value=float(np.max(np.linalg.norm(residual(p),axis=1)))
        opts.append((value,p,opt))
    upper,p,opt=min(opts,key=lambda x:x[0])
    # Supporting-hyperplane dual. Any nonnegative weights with sum1
    # give a valid lower bound, irrespective of optimization convergence.
    rr=residual(p);norms=np.linalg.norm(rr,axis=1)
    units=rr/np.maximum(norms[:,None],1e-30)
    intercept=np.sum(units*dt,axis=1)
    hb=np.sum(units*da,axis=1)
    hg=np.column_stack([np.sum(units*h1,axis=1),np.sum(units*h2,axis=1)])
    eq=[np.ones(len(dt))];rhs=[1.];ineq=[];bound=[]
    eps=2e-6
    if p[0]<eps:ineq.append(hb);bound.append(0.)
    elif p[0]>beta_max-eps:ineq.append(-hb);bound.append(0.)
    else:eq.append(hb);rhs.append(0.)
    ng=np.linalg.norm(p[1:3])
    if gamma_max==0:direction=np.zeros(2)
    elif ng<gamma_max-eps:
        eq.extend([hg[:,0],hg[:,1]]);rhs.extend([0.,0.]);direction=np.zeros(2)
    else:
        direction=p[1:3]/ng
        eq.append(hg[:,0]*direction[1]-hg[:,1]*direction[0]);rhs.append(0.)
        ineq.append(-hg@direction);bound.append(0.)
    objective=intercept-(beta_max*hb if p[0]>beta_max-eps else 0)-gamma_max*(hg@direction)
    lp=supporting_lp(objective,eq,rhs,ineq,bound)
    lam=lp.x if lp.success else np.ones(len(dt))/len(dt)
    lam=np.maximum(lam,0);lam/=lam.sum()
    lower=float(lam@intercept-beta_max*max(float(lam@hb),0.)-gamma_max*np.linalg.norm(lam@hg))
    lower=max(0.,lower)
    assert lower<=upper+2e-7
    b=theta-p[0]*alpha-np.column_stack([p[1]*theta[:,0]+p[2]*theta[:,1],
                                      p[2]*theta[:,0]-p[1]*theta[:,1]])
    assert abs(diameter(b)-upper)<1e-12
    return dict(minimum_diameter_primal_arcsec=upper,dual_lower_bound_arcsec=lower,
        primal_dual_gap_arcsec=upper-lower,beta=float(p[0]),g1=float(p[1]),g2=float(p[2]),
        shear_magnitude=float(np.linalg.norm(p[1:3])),source_center=b.mean(axis=0).tolist(),
        source_positions=b.tolist(),two_start_diameter_spread=max(x[0] for x in opts)-min(x[0] for x in opts),
        optimizer_success=bool(opt.success),optimizer_message=str(opt.message),
        dual_LP_success=bool(lp.success),dual_pair_weights=lam.tolist())


def minimum_convergence(theta,alpha,beta_max,gamma_max,threshold,basis):
    n=len(theta);ii=np.triu_indices(n,1)
    dt=theta[ii[0]]-theta[ii[1]];da=alpha[ii[0]]-alpha[ii[1]]
    h1=np.column_stack([dt[:,0],-dt[:,1]]);h2=dt[:,::-1]
    design=np.stack([da,h1,h2,dt],axis=2)
    def residual(p):return dt-np.einsum('kij,j->ki',design,p)
    def constraint(p):return threshold-np.linalg.norm(residual(p),axis=1)
    def jac(p):
        r=residual(p);v=np.maximum(np.linalg.norm(r,axis=1),1e-30)
        return np.einsum('ki,kij->kj',r,design)/v[:,None]
    cons=[dict(type='ineq',fun=constraint,jac=jac),dict(type='ineq',
        fun=lambda p:gamma_max**2-p[1]**2-p[2]**2,
        jac=lambda p:np.array([0.,-2*p[1],-2*p[2],0.]))]
    candidates=[]
    for guess in [np.array([beta_max,.02,.1,.3]),np.array([.2,0.,0.,.9])]:
        opt=minimize(lambda p:p[3],guess,jac=lambda p:np.array([0.,0.,0.,1.]),method='SLSQP',
            bounds=[(0,beta_max),(-gamma_max,gamma_max),(-gamma_max,gamma_max),(0,1)],
            constraints=cons,options={'ftol':1e-12,'maxiter':400})
        candidates.append(opt)
    feasible=[o for o in candidates if np.min(constraint(o.x))>-1e-8 and np.linalg.norm(o.x[1:3])<=gamma_max+1e-8]
    assert feasible
    opt=min(feasible,key=lambda o:o.x[3]);p=opt.x
    rr=residual(p);norms=np.linalg.norm(rr,axis=1);units=rr/np.maximum(norms[:,None],1e-30)
    c=np.sum(units*dt,axis=1);hb=np.sum(units*da,axis=1)
    hg=np.column_stack([np.sum(units*h1,axis=1),np.sum(units*h2,axis=1)])
    eq=[c];rhs=[1.];ineq=[];bound=[];eps=2e-6
    if p[0]<eps:ineq.append(hb);bound.append(0.)
    elif p[0]>beta_max-eps:ineq.append(-hb);bound.append(0.)
    else:eq.append(hb);rhs.append(0.)
    ng=np.linalg.norm(p[1:3])
    if ng<gamma_max-eps:
        eq.extend([hg[:,0],hg[:,1]]);rhs.extend([0.,0.]);direction=np.zeros(2)
    else:
        direction=p[1:3]/ng
        eq.append(hg[:,0]*direction[1]-hg[:,1]*direction[0]);rhs.append(0.)
        ineq.append(-hg@direction);bound.append(0.)
    objective=-(beta_max*hb if p[0]>beta_max-eps else 0)-gamma_max*(hg@direction)-threshold
    lp=supporting_lp(objective,eq,rhs,ineq,bound)
    lower=0.
    if lp.success:
        lam=np.maximum(lp.x,0);cc=lam@c
        if cc>0:lower=max(0.,float(1-(beta_max*max(lam@hb,0)+gamma_max*np.linalg.norm(lam@hg)+threshold*lam.sum())/cc))
    witness=arbitrary_shear_witness(theta,alpha,beta_max,basis)
    inter=F(witness['witness_intercept_exact_rational']);slope=F(witness['witness_slope_exact_rational'])
    den=F(witness['witness_pair_norm_sum_upper_exact_rational'])
    if inter<0:inter=-inter;slope=-slope
    exact=F(0) if inter==0 else max(F(0),1-(F.from_float(float(beta_max))*max(slope,F(0))+F(str(threshold))*den/n)/inter)
    assert lower<=p[3]+2e-7
    return dict(kappa_min_primal=float(p[3]),kappa_lower_dual=lower,
        kappa_primal_dual_gap=float(p[3]-lower),kappa_lower_exact_unrestricted_shear=rational_down(exact),
        beta=float(p[0]),g1=float(p[1]),g2=float(p[2]),shear_magnitude=float(np.linalg.norm(p[1:3])),
        achieved_diameter_arcsec=float(norms.max()),optimizer_success=bool(opt.success),
        two_start_kappa_spread=float(max(o.x[3] for o in feasible)-min(o.x[3] for o in feasible)),
        dual_LP_success=bool(lp.success))


def main(out,field_path):
    out.mkdir(parents=True,exist_ok=True)
    raw=json.loads((INPUT/'dataset/positions.json').read_text())['arguments']['values']['array']
    raw=np.asarray(raw);theta=np.column_stack([raw[:,1],-raw[:,0]])
    meta=json.loads((INPUT/'dataset/positions_meta.json').read_text());threshold=float(meta['threshold'])
    controls=[]
    for name in ['coolest.json','coolest_sersic.json']:
        p=sie_parameters(name);source=theta-sie(*theta.T,p).T
        controls.append(dict(input=name,parameters=p,source_diameter_arcsec=diameter(source),
            source_positions=source.tolist(),passes_association_gate=diameter(source)<=threshold,
            effective_critical_radius_arcsec=effective_radius(p)))
    assert controls[0]['passes_association_gate'] and controls[1]['passes_association_gate']
    with fits.open(INPUT/'results/deflections.fits') as h:
        ay,ax=np.array(h[1].data),np.array(h[2].data)
    yy,xx=np.indices(ax.shape);X=(xx-(ax.shape[1]-1)/2)*.1;N=(yy-(ax.shape[0]-1)/2)*.1
    control=sie(X,N,sie_parameters('coolest.json'))
    maperror=float(np.sqrt(np.mean((control[0]-ax)**2+(control[1]+ay)**2)))
    assert maperror<1e-10
    with (INPUT/'results/lens_mass.csv').open() as f:
        published_mass=next(csv.DictReader(f))
    published_effective_radius=float(published_mass['effective_einstein_radius'])
    assert abs(controls[0]['effective_critical_radius_arcsec']-published_effective_radius)<.001
    fields=np.load(field_path)
    assert np.max(np.abs(fields['theta_sky'].T-theta))<1e-12
    basis=exact_null_basis(theta)
    rows=[];witnesses=[];summary=[];convergence=[];crossings=[]
    for inc,field_inc in zip(fields['inclination'],fields['alpha_hat_sky']):
        for m,field in zip(fields['logmass'],field_inc):
            alpha=field.T
            for capname,cap in [('flat_matter_Lambda_horizon',BMAX),('conservative_beta_le_one',1.)]:
                witness=arbitrary_shear_witness(theta,alpha,cap,basis)
                witness.update(inclination=float(inc),logmass=float(m),geometry_cap_name=capname,beta_max=cap)
                witnesses.append(witness)
                for gamma in [0.,.1,.2,.3]:
                    result=capacity(theta,alpha,cap,gamma,basis)
                    result.update(inclination=float(inc),logmass=float(m),geometry_cap_name=capname,
                        beta_max=cap,gamma_max=gamma,association_threshold=threshold,
                        gate_feasible_witness=result['minimum_diameter_primal_arcsec']<=threshold-1e-7,
                        gate_infeasible_dual=result['dual_lower_bound_arcsec']>threshold+1e-7,
                        gate_infeasible_even_unrestricted_shear=witness['certified_finite_array_diameter_lower_bound_arcsec']>threshold)
                    rows.append(result)
        for capname in ['flat_matter_Lambda_horizon','conservative_beta_le_one']:
            for gamma in [0.,.1,.2,.3]:
                part=[r for r in rows if r['inclination']==inc and r['geometry_cap_name']==capname and r['gamma_max']==gamma]
                passing=[r for r in part if r['gate_feasible_witness']]
                first=passing[0]['logmass'] if passing else None
                failing=[r['logmass'] for r in part if r['gate_infeasible_dual'] and(first is None or r['logmass']<first)]
                summary.append(dict(inclination=float(inc),geometry_cap_name=capname,gamma_max=gamma,
                    first_scanned_feasible_logmass=first,
                    greatest_lower_scanned_infeasible_logmass=max(failing) if failing else None,
                    all_lower_scanned_masses_certified_infeasible=bool(first is not None and all(r['gate_infeasible_dual'] for r in part if r['logmass']<first)),
                    maximum_primal_dual_gap=max(r['primal_dual_gap_arcsec'] for r in part)))
        nominal=11.9268788861
        j=np.searchsorted(fields['logmass'],nominal)-1
        u=(nominal-fields['logmass'][j])/(fields['logmass'][j+1]-fields['logmass'][j])
        a=((1-u)*field_inc[j]+u*field_inc[j+1]).T
        for label,cap in [('flat_matter_Lambda_horizon',BMAX),('conservative_beta_le_one',1.)]:
            record=minimum_convergence(theta,a,cap,.3,threshold,basis)
            record.update(inclination=float(inc),geometry_cap_name=label,beta_max=cap,
                nominal_logmass=nominal,field_interpolation_bracket=fields['logmass'][j:j+2].tolist(),
                interpolation_note='Linear interpolation of alpha in logmass, not an independently solved nominal-mass field')
            convergence.append(record)
        for label,cap in [('flat_matter_Lambda_horizon',BMAX),('conservative_beta_le_one',1.)]:
            part=[r for r in rows if r['inclination']==inc and r['geometry_cap_name']==label and r['gamma_max']==.3]
            passing=[r for r in part if r['gate_feasible_witness']]
            if not passing:continue
            high=passing[0]['logmass']
            lower=max(r['logmass'] for r in part if r['logmass']<high and r['gate_infeasible_dual'])
            def at_mass(m):
                k=np.searchsorted(fields['logmass'],m)-1
                k=max(0,min(k,len(fields['logmass'])-2))
                t=(m-fields['logmass'][k])/(fields['logmass'][k+1]-fields['logmass'][k])
                ah=((1-t)*field_inc[k]+t*field_inc[k+1]).T
                return capacity(theta,ah,cap,.3,basis)
            root=brentq(lambda m:at_mass(m)['minimum_diameter_primal_arcsec']-threshold,lower,high,xtol=1e-10)
            target=at_mass(root)
            crossings.append(dict(inclination=float(inc),geometry_cap_name=label,beta_max=cap,
                interpolated_gate_crossing_logmass=float(root),field_mass_bracket=[lower,high],
                crossing_diameter=target['minimum_diameter_primal_arcsec'],
                beta=target['beta'],shear_magnitude=target['shear_magnitude'],
                note='A crossing of linearly interpolated finite fields, not a certified continuum mass floor'))
        print(json.dumps([r for r in summary if r['inclination']==inc]),flush=True)
    assert max(r['primal_dual_gap_arcsec'] for r in rows)<2e-6
    assert max(r['two_start_diameter_spread'] for r in rows)<1e-6
    assert max(r['kappa_primal_dual_gap'] for r in convergence)<2e-7
    result=dict(assertion_tested='For the named finite oblate fields and actual released markers, optimize a common-source pair-diameter gate over unknown source geometry and bounded reduced shear, with zero external convergence',
        non_claims=['No image likelihood or calibrated p-value','No arbitrary shape M/L inclination or field-error certification','No full screened action exclusion','Position association gate is conditional modelling information'],
        positions_west_north=theta.tolist(),position_metadata=meta,association_threshold=threshold,
        beta_infinity=BMAX,controls=controls,control_released_deflection_RMS_arcsec=maperror,
        published_effective_einstein_radius_median=published_effective_radius,
        COOLEST_control_minus_catalogue_effective_radius=controls[0]['effective_critical_radius_arcsec']-published_effective_radius,
        summary=summary,capacity_rows=rows,unrestricted_shear_witnesses=witnesses,
        nominal_mass_minimum_external_convergence=convergence,
        interpolated_gate_crossings=crossings,
        field_input=str(field_path),status='completed')
    (out/'result.json').write_text(json.dumps(clean(result),indent=2)+'\n')
    with (out/'summary.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=summary[0].keys());writer.writeheader();writer.writerows(summary)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--field-grid',type=Path,required=True)
    args=parser.parse_args();main(args.output,args.field_grid)
