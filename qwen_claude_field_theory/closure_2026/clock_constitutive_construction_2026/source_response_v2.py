"""Same clock family, deriving a mixed-projector repair from curvature support.

V2 adds eta_X U W to the V1 action. W=Delta^dagger D_iD_j K^ij.
The source family is conserved and compact, not a fitted empirical catalogue.
"""
import json
import numpy as np
import sympy as s
from numpy.polynomial.legendre import leggauss
from construct import canonical_constraints


def retarded_radial_seed(t, radius, speed, order=64):
    """3D retarded scalar-wave convolution for a smooth radial source.

    F(t,r)=exp[-1/(t(1-t))] exp[-1/(1-(r/R)^2)], 0<t<1,r<R.
    Green function solves (d_t²-cs² Delta) u=F with zero past data.
    """
    x, weights = leggauss(order)
    R = .2
    rp = R*(x+1)/2
    lo, hi = abs(radius-rp), radius+rp
    sep = lo[:, None]+(hi-lo)[:, None]*(x[None,:]+1)/2
    tr = t-sep/speed
    temporal = np.zeros_like(tr)
    mask = (tr>0)&(tr<1)
    temporal[mask] = np.exp(-1/(tr[mask]*(1-tr[mask])))
    radial = np.exp(-1/(1-(rp/R)**2))
    inner = (temporal@weights)*(hi-lo)/2
    return float(np.dot(weights, rp*radial*inner)*R/(4*speed**2*radius))


def derive_response():
    C, ell, k, r = s.symbols('C ell k r', positive=True)
    alpha = s.symbols('alpha', positive=True)
    d, t = s.symbols('d t', real=True)
    z, n, B, F, src = s.symbols('z n B F src', real=True)
    zd, nd, Bd = s.symbols('zd nd Bd', real=True)
    L = (-6*t*zd**2+4*d*k*k*zd*B-ell*(3*zd-k*k*B)**2
         +k*k*(2*z*z-4*n*z+alpha*n*n))

    def solve_source(mult):
        # rho=-k²F, j_i=-partial_t partial_i F,
        # Tij=delta_ij Ftt gives mult=3. mult=1 is the previous source.
        source = -src*n+r*src*B+mult*r*r*src*z/k**2
        equations = [s.diff(L+source,n).subs(zd,r*z),
                     s.diff(L+source,B).subs(zd,r*z),
                     r*s.diff(L,zd).subs(zd,r*z)-s.diff(L+source,z)]
        sol = s.solve(equations, [n,B,z])
        X = s.factor(r*r*sol[z])
        Z = s.factor(-k*k*(sol[n]+r*sol[B])+X)
        return X,Z

    X1,Z1=solve_source(1)
    # GR reference already explicitly varied in construct.py; rederive here
    # at the degenerate GR equations instead of substituting a singular inverse.
    Lgr=L.subs({d:1,t:1,ell:0,alpha:0})
    srcgr=-2*src*n/C+2*r*r*src*z/(C*k*k)
    solgr=s.solve([s.diff(Lgr+srcgr,n).subs({zd:r*z,B:0}),
                  (r*s.diff(Lgr,zd).subs(zd,r*z)-s.diff(Lgr+srcgr,z)).subs(B,0)], [n,z])
    Zgr=s.factor((-k*k*n+r*r*z).subs(solgr))
    mismatch=s.factor(s.limit((Z1.subs(alpha,2-C)-Zgr)/r**2,r,0))
    tmatch=s.solve(mismatch,t)[0]
    X,Z=solve_source(3)
    X=s.factor(X.subs({alpha:2-C,src:-k*k*F,t:tmatch}))
    Z=s.factor(Z.subs({alpha:2-C,src:-k*k*F,t:tmatch}))
    # R_0i0j = X delta_ij + ki kj (Z-X)/k².
    # A nonzero k->0 value of Z-X leaves an inverse-Laplacian residue.
    residue=s.factor(s.limit(Z-X,k,0))
    roots=s.solve(residue,d)
    # Select the branch whose scalar Einstein kinetic coefficients have
    # the same normalization C/2. This selection is an explicit design choice.
    chosen=next(root for root in roots if s.simplify(root-C/2)==0)
    tv2=s.factor(tmatch.subs(d,chosen))
    X2=s.factor(X.subs(d,chosen))
    Z2=s.factor(Z.subs(d,chosen))
    local_long=s.factor((Z2-X2)/k**2)
    assert s.simplify(local_long+F/(2*C))==0
    assert s.simplify(mismatch.subs({d:chosen,t:tv2}))==0

    # Derive coefficients from actual U,W contractions:
    # U=-2 zd, W=-zd+k²B. Do not insert a desired trace matrix.
    U,W=-2*zd,-zd+k*k*B
    etaU,etaX=s.symbols('etaU etaX')
    oldkin=L.subs({d:1,t:1})
    desired=L.subs({d:chosen,t:tv2})
    residual=s.Poly(s.expand(oldkin+etaU*U**2+etaX*U*W-desired),zd,B)
    coefficients=s.solve(residual.coeffs(),[etaU,etaX])
    assert s.expand((oldkin+etaU*U**2+etaX*U*W-desired).subs(coefficients))==0

    finalL=s.factor(desired)
    aux=s.solve([s.diff(finalL,n),s.diff(finalL,B)],[n,B])
    reduced=s.factor(finalL.subs(aux))
    kinetic=s.factor(s.diff(reduced,zd,2))
    cs2=s.factor(-s.diff(reduced,z,2)/(k*k*kinetic))
    witness={C:s.Rational(5,3),ell:s.Rational(1,100)}
    count=canonical_constraints(finalL.subs(witness),[z,n,B],[zd,nd,Bd])

    # Local hyperbolic representation of the COMPLETE compact scalar response.
    # The clock wave denominator is derived from the response denominator.
    xcorrection=s.factor(X2-F*r*r/(2*C))
    wavecoef=s.factor((2-C)*(C+3*ell))
    wave=s.factor(wavecoef*r*r+2*ell*k*k)
    assert s.simplify(xcorrection+3*ell*(2-C)*F*r**4/(2*C*wave))==0
    cs_high=s.factor(2*ell/wavecoef)
    speed=float(s.sqrt(cs_high.subs(witness)))
    times=[.1,.5,1.,4.5,5.,5.5,6.]
    convolutions=[dict(time=T,order32=retarded_radial_seed(T,1.,speed,32),
                      order64=retarded_radial_seed(T,1.,speed,64)) for T in times]
    assert all(row['order64']==0 for row in convolutions if row['time']<.8)
    assert max(row['order64'] for row in convolutions)>0
    assert max(abs(row['order32']-row['order64']) for row in convolutions)<1e-9
    return dict(status='V2_CONSTRUCTED; FULL_THEORY_OPEN',
                base_commit='28bb629a4',
                previous_order_r2_condition=str(mismatch),
                trace_matching=str(tmatch), old_residue=str(residue.subs(d,1)),
                inverse_laplacian_residue=str(residue), repair_roots=str(roots),
                chosen_d=str(chosen), chosen_t=str(tv2),
                eta_U=str(coefficients[etaU]),eta_X=str(coefficients[etaX]),
                eta_V='C-2',
                Rxx=str(X2),Rzz=str(Z2),longitudinal_symbol=str(local_long),
                local_wave_denominator=str(wave),
                local_retarded_curvature_correction=str(xcorrection),
                reduced_L=str(reduced),kinetic_hessian=str(kinetic),
                clock_speed_squared=str(cs2),high_clock_speed_squared=str(cs_high),
                constraint_count=count,high_speed_witness=speed,
                retarded_wave_convolutions=convolutions,
                limits=['linear constant high-acceleration coefficients',
                        'compact conserved scalar stress, not arbitrary tensor stress',
                        'source family is a diagnostic; no material realization asserted',
                        'no finite-background or nonlinear causal theorem',
                        'no full PPN, zero-field, or empirical certificate'])


if __name__=='__main__':
    print(json.dumps(derive_response(),indent=2,default=str))
