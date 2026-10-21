"""Signed, nonlocal axisymmetric annular mass -> midplane V^2 kernel.

Lengths are kpc, masses Msun, V^2 is (km/s)^2.  Surface density is
constant inside each annulus. A stellar light profile can therefore be
multiplied by a source-bin M/L, converted to masses, and passed THROUGH
this kernel; multiplying a target-radius velocity template is incorrect.

The source radius is integrated analytically by a boundary integral.
Only height remains numerical. h is always an explicit geometric input.
Finite-height profiles are truncated at |z|/h=vertical_cut and renormalized
to unit mass. The default 24 omits <=3.776e-11 exponential mass or
<=2.851e-21 sech^2 mass before renormalization.
"""
from functools import lru_cache
import math

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy import integrate, special

G_KPC_KMS2_MSUN = 4.30091e-6


@lru_cache(maxsize=16)
def _nodes(order):
    x, w = leggauss(order)
    return (x + 1.0) / 2.0, w / 2.0


def _elliptic_boundary_factor(m, complementary_m):
    """[((2-m)K(m)-2E(m))/m], with stable small-m series."""
    m, p = np.broadcast_arrays(np.asarray(m, float), np.asarray(complementary_m, float))
    result = np.empty_like(m)
    small = m < 0.02
    # K series c_n=(binom(2n,n)/4^n)^2; cancellation begins at m^2.
    # Coefficient of m^(n-1) is pi/2*[4n*c_n/(2n-1)-c_(n-1)].
    ms = m[small]
    values = np.zeros_like(ms)
    previous = 1.0
    for n in range(1, 16):
        current = previous * ((2*n-1)/(2*n))**2
        coefficient = 4*n*current/(2*n-1) - previous
        values += coefficient * ms**(n-1)
        previous = current
    result[small] = (math.pi/2.0) * values
    other = ~small
    result[other] = ((1.0+p[other])*special.ellipkm1(p[other])
                     -2.0*special.ellipe(m[other])) / m[other]
    return result


def uniform_disk_v2_per_surface_density(radius_kpc, disk_radius_kpc, z_kpc=0.0,
                                        gravitational_constant=G_KPC_KMS2_MSUN):
    """Exact uniform disk V^2 per Msun/kpc^2 at height z.

    The sharp razor-thin edge has divergent force. Finite height averaging
    integrates its logarithmic singularity; no softening is introduced.
    """
    R, a, z = np.broadcast_arrays(np.asarray(radius_kpc, float),
                                 np.asarray(disk_radius_kpc, float), np.asarray(z_kpc, float))
    if np.any(R < 0) or np.any(a < 0):
        raise ValueError("radii must be nonnegative")
    D = (R+a)**2 + z*z
    safe_D = np.where(D == 0.0, 1.0, D)
    m = 4.0*R*a/safe_D
    # Computing p directly preserves the logarithmic near-edge limit.
    p = ((R-a)**2 + z*z)/safe_D
    value = 4.0*gravitational_constant*R*a/np.sqrt(safe_D)*_elliptic_boundary_factor(m,p)
    return np.where((R == 0.0) | (a == 0.0), 0.0, value)


def thin_uniform_disk_v2_per_surface_density(radius_kpc, disk_radius_kpc,
                                             gravitational_constant=G_KPC_KMS2_MSUN):
    """Independent analytic midplane formula using inside/outside Landen form."""
    R, a = np.broadcast_arrays(np.asarray(radius_kpc,float), np.asarray(disk_radius_kpc,float))
    value = np.zeros_like(R)
    positive = (R > 0) & (a > 0)
    minimum = np.minimum(R[positive],a[positive])
    maximum = np.maximum(R[positive],a[positive])
    m = (minimum/maximum)**2
    value[positive] = 4.0*gravitational_constant*maximum*(special.ellipk(m)-special.ellipe(m))
    return value


def _vertical_weight(u, vertical):
    if vertical == "exponential":
        return np.exp(-u)
    if vertical == "sech2":
        # Algebraic form stays finite even at large declared cut.
        e = np.exp(-2.0*u)
        return 4.0*e/(1.0+e)**2
    raise ValueError("vertical must be 'exponential' or 'sech2'")


def vertical_tail_mass(vertical="exponential", vertical_cut=24.0):
    """Mass fraction omitted before exact truncation normalization."""
    if vertical == "exponential":
        return math.exp(-vertical_cut)
    if vertical == "sech2":
        e=math.exp(-2.0*vertical_cut)
        return 2.0*e/(1.0+e)
    raise ValueError("unsupported vertical law")


def build_annular_kernel(target_radii_kpc, edges_kpc, height_kpc, vertical="exponential",
                         order=96, vertical_cut=24.0, method="gauss",
                         gravitational_constant=G_KPC_KMS2_MSUN):
    """Return matrix K[i,j], signed (km/s)^2 per nonnegative source Msun.

    height_kpc: explicit nonnegative scalar or one value per source bin.
    A zero height selects the razor-thin analytic kernel; a target exactly
    on an edge of that sharp bin is excluded as its force diverges.
    method: 'gauss' uses fixed order after z/h=t^2, 'adaptive' uses QUADPACK
    on that same integrable variable with epsrel=2e-10, limit=160.
    Compare order with twice order and/or adaptive on the actual geometry;
    output entries close to zero require absolute, not relative, comparison.
    No target/source radius is shifted and no smoothing length is fitted.
    """
    radii=np.asarray(target_radii_kpc,float)
    edges=np.asarray(edges_kpc,float)
    if radii.ndim != 1 or edges.ndim != 1 or len(edges)<2:
        raise ValueError("one-dimensional targets and >=2 edges required")
    if not np.all(np.isfinite(radii)) or not np.all(np.isfinite(edges)):
        raise ValueError("radii must be finite")
    if np.any(radii < 0) or edges[0]<0 or np.any(np.diff(edges)<=0):
        raise ValueError("radii nonnegative and source edges strictly increasing required")
    nbin=len(edges)-1
    heights=np.broadcast_to(np.asarray(height_kpc,float),(nbin,))
    if not np.all(np.isfinite(heights)) or np.any(heights<0):
        raise ValueError("explicit finite nonnegative heights required")
    if vertical not in ("exponential","sech2") or method not in ("gauss","adaptive"):
        raise ValueError("unsupported vertical law or quadrature method")
    if int(order)!=order or order<8 or not np.isfinite(vertical_cut) or vertical_cut<8:
        raise ValueError("order integer >=8 and vertical_cut >=8 required")
    areas=math.pi*(edges[1:]**2-edges[:-1]**2)
    matrix=np.empty((len(radii),nbin),float)
    normalization=1.0-vertical_tail_mass(vertical,vertical_cut)
    x,w=_nodes(int(order))
    upper=math.sqrt(vertical_cut)
    t=upper*x
    u=t*t
    weights=w*upper*2.0*t*_vertical_weight(u,vertical)/normalization
    boundary_cache={}
    def boundary(a,h):
        key=(float(a),float(h))
        if key in boundary_cache:
            return boundary_cache[key]
        if a==0:
            result=np.zeros_like(radii)
        elif h==0:
            if np.any(radii==a):
                raise ValueError("razor-thin sharp bin has a target exactly on its edge")
            result=thin_uniform_disk_v2_per_surface_density(radii,a,gravitational_constant)
        elif method=="gauss":
            result=uniform_disk_v2_per_surface_density(radii[:,None],a,h*u[None,:],gravitational_constant)@weights
        else:
            result=np.empty_like(radii)
            for i,R in enumerate(radii):
                if R==0:
                    result[i]=0.0
                    continue
                def integrand(ti):
                    ui=ti*ti
                    return float(uniform_disk_v2_per_surface_density(R,a,h*ui,gravitational_constant))*2.0*ti*float(_vertical_weight(ui,vertical))/normalization
                result[i]=integrate.quad(integrand,0.0,upper,epsabs=1e-13,
                                         epsrel=2e-10,limit=160)[0]
        boundary_cache[key]=result
        return result
    for j,h in enumerate(heights):
        matrix[:,j]=(boundary(edges[j+1],h)-boundary(edges[j],h))/areas[j]
    if not np.all(np.isfinite(matrix)):
        raise FloatingPointError("nonfinite annular kernel")
    return matrix


def annular_masses_from_surface_density(edges_kpc, surface_density_msun_kpc2):
    """Exact conservative conversion for bin-constant surface density."""
    edges=np.asarray(edges_kpc,float)
    return math.pi*np.diff(edges**2)*np.asarray(surface_density_msun_kpc2,float)


def ring_v2_direct_angle(radius_kpc, ring_radius_kpc, z_kpc=0.0,
                         gravitational_constant=G_KPC_KMS2_MSUN):
    """Independent original Newtonian angular force per unit ring mass."""
    R=float(radius_kpc); a=float(ring_radius_kpc); z=float(z_kpc)
    def integrand(phi):
        c=math.cos(phi)
        s2=(R-a)**2+2.0*R*a*(1.0-c)+z*z
        return R*(R-a*c)/s2**1.5
    return gravitational_constant*integrate.quad(integrand,0,math.pi,
                 epsabs=1e-11,epsrel=3e-11,limit=180)[0]/math.pi


def ring_v2_elliptic(radius_kpc, ring_radius_kpc, z_kpc=0.0,
                      gravitational_constant=G_KPC_KMS2_MSUN):
    """Derivative of the ring Green function, independent radial-integral control.

    Intended for benchmark ranges away from tiny R/a cancellation. The
    production annulus kernel uses the boundary expression above instead.
    """
    R,a,z=np.broadcast_arrays(np.asarray(radius_kpc,float),
                              np.asarray(ring_radius_kpc,float),np.asarray(z_kpc,float))
    D=(R+a)**2+z*z
    d=(R-a)**2+z*z
    p=d/D
    return gravitational_constant/(math.pi*np.sqrt(D))*(special.ellipkm1(p)
             +(R*R-a*a-z*z)/d*special.ellipe(1.0-p))
