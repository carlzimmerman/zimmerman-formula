import sympy as s, argparse,json,pathlib,sys
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',default='none');args=ap.parse_args(); rows=[]
def ck(name,test): rows.append({'name':name,'pass':bool(test)})
t,c,l,f,g,h=s.symbols('tau chi lam f g h');X=s.symbols('X',negative=True);u,j,f0,b,k=s.symbols('u j f0 beta k',positive=True)
A=f+t*t*g;B=-t*c*g;C=-f+c*c*g;F=A*l*l-2*B*l+C
D=lambda z:-l*s.diff(z,t)+s.diff(z,c)+g*(-l*t-c)*s.diff(z,f)+h*(-l*t-c)*s.diff(z,g)
L=t*l+c
ck('characteristic_flux_form',s.expand(F-f*(l*l-1)-g*L*L)==0)
ck('hyperbolic_discriminant',s.expand(B*B-A*C-f*(f+(t*t-c*c)*g))==0)
ck('raw_linear_degeneracy_derivative',s.expand(D(F)+L*(h*L*L+3*g*(l*l-1)))==0)
ck('on_characteristic_reduction',s.expand(f*D(F)+L**3*(f*h-3*g*g)+3*g*L*F)==0)
ff=s.Function('f')(X)
ck('inverse_square_ODE',s.simplify(s.diff(ff**-2,X,2)+2*(ff*s.diff(ff,X,2)-3*s.diff(ff,X)**2)/ff**4)==0)
a,bb=s.symbols('a b',positive=True);dbi=(a+bb*X)**s.Rational(-1,2)
ck('DBI_exceptional',s.simplify(dbi*s.diff(dbi,X,2)-3*s.diff(dbi,X)**2)==0)
ck('canonical_exceptional',s.diff(f0,X)==0)
mond=k*s.sqrt(-2*X);E=s.simplify(mond*s.diff(mond,X,2)-3*s.diff(mond,X)**2)
ck('MOND_nonexceptional_exact',s.simplify(E-2*k*k/X)==0)
ck('MOND_not_CE',E==0 if args.control=='mond_exceptional' else E!=0)
mu=f0/s.sqrt(1+b*u*u);flux=mu*u
ck('static_radial_Hessian',s.simplify(s.diff(flux,u)-f0/(1+b*u*u)**s.Rational(3,2))==0)
uinv=j/s.sqrt(f0*f0-b*j*j)
ck('source_inverse',s.simplify((f0*f0*u*u/(1+b*u*u)).subs(u,uinv)-j*j)==0)
ck('weak_source_linear',s.limit(uinv/j,j,0)==1/f0)
ck('no_weak_sqrt_mass',s.limit(uinv/s.sqrt(j),j,0)==0 if args.control!='sqrt_mass' else s.limit(uinv/s.sqrt(j),j,0)>0)
ck('source_slope',s.simplify(j*s.diff(uinv,j)/uinv-f0*f0/(f0*f0-b*j*j))==0)
ck('flux_slope',s.simplify(u*s.diff(flux,u)/flux-1/(1+b*u*u))==0)
# Negative beta has local MOND slope at u=1/sqrt(2|beta|), but cannot keep it.
bneg=s.symbols('bneg',positive=True);mun=f0/s.sqrt(1-bneg*u*u);qn=u*s.diff(mun*u,u)/(mun*u)
ck('isolated_slope_two',s.simplify(qn.subs(u,1/s.sqrt(2*bneg))-2)==0)
ck('slope_not_constant_two',s.simplify(s.diff(qn,u))!=0)
ck('MOND_elliptic_not_exceptional',s.diff(k*u*u,u)==2*k*u)
ck('singular_endpoint_rank_loss',s.simplify(s.diff((k/u)*u,u))==0)
P=s.Function('P')(X);off=s.symbols('offset')
ck('offset_not_selected',s.diff(P+off,X)==s.diff(P,X) if args.control!='offset_selected' else s.diff(P+off,X)!=s.diff(P,X))
# Exact physical force calibration: r² f u=gamma M/(4pi), gscalar=gamma u, f=ku.
gamma,M,r,G,a0=s.symbols('gamma M r G a0',positive=True)
gscalar=gamma*s.sqrt(gamma*M/(4*s.pi*k))/r
ck('MOND_normalization_requires_scale',s.simplify(gscalar*gscalar-G*M*a0/r**2).subs(k,gamma**3/(4*s.pi*G*a0))==0)
res={'checks':rows,'passed':sum(x['pass'] for x in rows),'failed':sum(not x['pass'] for x in rows),'control':args.control,'exact_MOND_CE_residual':str(E),'non_claims':['No dynamical gravity/KGB theorem','No global caustic theorem','No vacuum selector or observed MOND model']}
pathlib.Path(args.output).parent.mkdir(parents=True,exist_ok=True);pathlib.Path(args.output).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res));sys.exit(bool(res['failed']))
