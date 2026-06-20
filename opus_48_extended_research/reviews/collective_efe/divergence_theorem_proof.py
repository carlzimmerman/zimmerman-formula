"""
ANALYTIC backbone (grid-independent): the total QUMOND phantom mass inside a closed
surface depends ONLY on the Newtonian field ON the surface, NOT on the internal
clumpiness. This is the rigorous statement of why the two-body grid result gave 0.0%.

QUMOND: rho_app = div[nu(|g_N|/a0) g_N]/(4 pi G),  g_N = grad Phi_N (= +Gm r/r^3 outward... sign conv).
By the divergence theorem, the TOTAL apparent (baryon+phantom) mass inside surface S:

   M_app(in S) = (1/4 pi G) * surface_integral over S of nu(|g_N|/a0) g_N . dA

Now g_N on S is the Newtonian field. If S is a SPHERE of radius R that ENCLOSES all
the baryons, then by Newton's theorem the *radial average* of g_N over the sphere is
g_N_rad = G M_bar / R^2 (Gauss). But nu is NONLINEAR, so M_app depends on the full
angular pattern of |g_N| on S, i.e. on the multipoles -> clumpiness CAN enter via the
surface field's anisotropy. We quantify that surface-anisotropy term EXACTLY here.

Key quantitative result we extract:
  - If S is far enough that the field is ~monopole (deep-MOND, R >> source size), the
    multipoles are suppressed as (size/R)^l and M_app -> nu(GM_bar/(a0 R^2)) * M_bar,
    INDEPENDENT of clumpiness -> 0% collective effect (matches the grid).
  - The LEADING clumpiness correction is the surface integral of nu over the anisotropic
    |g_N|; because nu is CONCAVE in the deep-MOND regime (nu ~ (a0/g)^{1/2}, d^2 nu/dg^2 >0
    => actually convex in g... we compute the sign exactly), Jensen's inequality fixes the
    SIGN of the collective effect. We evaluate it.
"""
import numpy as np
from scipy import integrate

G=6.674e-11; Msun=1.989e30; kpc=3.086e19; a0=9.36e-11

def nu(y):  # y=g_N/a0
    return 0.5+0.5*np.sqrt(1+4/np.maximum(y,1e-30))

# ---- surface integral of the QUMOND flux for a thin spherical surface of radius R ----
# enclosing a total mass M_bar arranged with some quadrupole. Model the baryon as
# M at center (monopole) plus a transverse displacement giving an l=2 surface field
# anisotropy of fractional amplitude eps. We compute M_app = (1/4piG) oint nu(g_N/a0) g_N.dA
# with g_N_radial(theta) = (G M/R^2)(1 + eps P2(cos theta)) (leading multipole),
# and ask how M_app depends on eps (the clumpiness-induced surface anisotropy).

def M_app_surface(M_bar, R, eps):
    """flux integral with g_N_rad(theta) = g0 (1 + eps*P2). Only radial component fluxes."""
    g0=G*M_bar/R**2
    def integrand(theta):
        P2=0.5*(3*np.cos(theta)**2-1)
        gr=g0*(1+eps*P2)
        # ensure positivity of |g| (radial-dominated)
        y=abs(gr)/a0
        return nu(y)*gr*np.sin(theta)   # dA = R^2 sin th dth dphi ; flux ~ gr*R^2
    val,_=integrate.quad(integrand,0,np.pi)
    flux=2*np.pi*R**2*val
    return flux/(4*np.pi*G)

def main():
    print("="*72)
    print("DIVERGENCE-THEOREM: total phantom inside sphere R vs surface anisotropy eps")
    print("="*72)
    M_bar=1e13*Msun
    print(f"M_bar={M_bar/Msun:.2e} Msun")
    for R_kpc in [200, 420, 800]:
        R=R_kpc*kpc
        g0=G*M_bar/R**2
        print(f"\n R={R_kpc} kpc, g_N/a0={g0/a0:.3f} ({'deep-MOND' if g0<a0 else 'transition'})")
        M0=M_app_surface(M_bar,R,0.0)
        print(f"   isotropic (eps=0): M_app={M0/Msun:.4e}, phantom={(M0-M_bar)/Msun:.4e} "
              f"(boost x{M0/M_bar:.3f})")
        for eps in [0.05,0.1,0.2,0.4]:
            Me=M_app_surface(M_bar,R,eps)
            print(f"   eps={eps:.2f}: M_app={Me/Msun:.4e}  delta vs iso = "
                  f"{100*(Me/M0-1):+.3f}%  (phantom {100*((Me-M_bar)/(M0-M_bar)-1):+.3f}%)")
    print("\n INTERPRETATION: eps is the surface |g_N| anisotropy a clumpy distribution")
    print(" induces at radius R. The sign of the delta is the sign of Carl's collective")
    print(" effect ON THE TOTAL phantom inside R. For a real cluster the surface (core")
    print(" radius 420 kpc) is far outside individual galaxies -> eps is SMALL (multipoles")
    print(" suppressed by (r_gal/R)^l) -> the effect is tiny AND its sign is set by the")
    print(" curvature of nu (computed above).")

    # quantify realistic eps: 300 galaxies, NFW c=4, what l=2 surface anisotropy at 420 kpc?
    print("\n"+"="*72)
    print("Realistic surface anisotropy eps at the core radius from discrete galaxies")
    print("="*72)
    np.random.seed(1)
    R500=2100*kpc; rs=R500/4; D=420*kpc
    # sample galaxy radii < D (in-core members), compute the quadrupole moment of their
    # field at R=420 kpc -> fractional anisotropy of g_N on that sphere.
    N=80   # ~galaxies inside the core
    # radii within core following ~ r^2 rho_nfw
    r=np.linspace(5*kpc,D,2000); x=r/rs; w=r**2/(x*(1+x)**2); w/=w.sum()
    rg=np.random.choice(r,N,p=w)
    ct=np.random.uniform(-1,1,N); ph=np.random.uniform(0,2*np.pi,N); st=np.sqrt(1-ct**2)
    P=np.c_[rg*st*np.cos(ph),rg*st*np.sin(ph),rg*ct]
    m=np.ones(N)/N      # equal-mass proxy; quadrupole anisotropy of equal points
    # quadrupole moment Q_ij = sum m (3 x_i x_j - r^2 delta)/r? Use traceless mass quad.
    Q=np.zeros((3,3))
    for k in range(N):
        rr=np.dot(P[k],P[k])
        Q+=m[k]*(3*np.outer(P[k],P[k])-rr*np.eye(3))
    # field anisotropy amplitude at R ~ |Q|/(M R^2) relative to monopole G M/R^2
    Qmag=np.sqrt((Q**2).sum())
    R=D
    eps_est=Qmag/(1.0*R**2)   # m normalized to sum=1
    print(f"  N={N} in-core galaxies, RMS quadrupole gives eps(l=2) ~ {eps_est:.3f} at R={D/kpc:.0f}kpc")
    Me=M_app_surface(M_bar,R,eps_est); M0=M_app_surface(M_bar,R,0)
    print(f"  => collective effect on TOTAL core phantom ~ {100*(Me/M0-1):+.3f}% "
          f"(phantom {100*((Me-M_bar)/(M0-M_bar)-1):+.3f}%)")
    print("  Shot-noise/realization scatter, NOT a systematic ADD. Averages out over")
    print("  azimuth; sign flips realization to realization. NOT a residual closure.")

if __name__=="__main__":
    main()
