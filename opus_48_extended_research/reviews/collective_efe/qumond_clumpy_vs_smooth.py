"""
ROUTE 1 -- DISCRETE-CLUMPY vs SMOOTH total QUMOND phantom mass.
Carl's "collective EFE / overlapping deep-MOND fields add cluster binding" idea,
computed honestly with a real QUMOND solver on a 3D FFT grid.

THE QUESTION (Carl):
  In a relaxed cluster, member galaxies each source a long-range 1/r deep-MOND
  field. These overlap in the inter-galaxy medium. Does the OVERLAPPING COLLECTIVE
  field give the whole core region MORE effective gravitating (phantom) mass than
  the SMOOTH-baryon cluster-MOND estimate -- closing part of the ~30-49% residual
  with NO new particle?

THE TEST (clumpy_vs_smooth):
  Model the SAME total baryonic mass two ways at a0 = 9.36e-11 (framework):
   (a) DISCRETE: N member galaxies as point/Plummer clumps (realistic luminosity
       function + positions) + smooth ICM gas (beta-model).
   (b) SMOOTH: the identical TOTAL baryon mass with the galaxies' mass smeared into
       the same radial profile (so M_bar(<r) is IDENTICAL between (a) and (b)).
  Compute the QUMOND phantom density rho_ph = nabla^2(Phi)/(4 pi G) - rho for BOTH,
  with Phi from the QUMOND algebraic recipe
       nabla^2 Phi = div[ nu(y) grad Phi_N ],  y = |grad Phi_N|/a0,
       nu(y) = 1/2 + 1/2 sqrt(1 + 4/y)     (the "simple"/standard QUMOND nu; deep-MOND nu->1/sqrt(y))
  and compare the TOTAL phantom mass M_ph(<r) in the core (<420 kpc).

  KEY: does DISCRETE-clumpy total phantom EXCEED smooth (collective overlap ADDS
  mass -> closes part of residual), or is it ~SAME or LESS (enclosed-mass theorem /
  sub-additivity -> redistributes only, the honest likely null)?

Physics to keep honest (BOTH WAYS):
  - Deep-MOND sub-additivity: field of 2 masses ~ sqrt(2M) < 2 sqrt(M).
  - Phantom density can be NEGATIVE between discrete masses (Milgrom 1986) -> works
    AGAINST extra mass.
  - Spherical enclosed-mass theorem: in spherical symmetry the TOTAL phantom inside r
    is fixed by enclosed baryonic mass. Discreteness BREAKS sphericity -> the question
    is whether the non-spherical correction is net POSITIVE (adds) or ~cancels.

Quarantine: a0=9.36e-11 used as INPUT, never asserted derived.
"""
import numpy as np

# ----------------------------- constants (SI) -----------------------------
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.086e19
Mpc  = 1000*kpc
a0   = 9.36e-11           # framework a0 (eta-worst footing). INPUT, not derived.

# ----------------------------- nu interpolation -----------------------------
def nu_simple(y):
    """standard QUMOND nu(y), y=|grad Phi_N|/a0. nu->1 (Newt) for y>>1, ->1/sqrt(y) deep-MOND."""
    return 0.5 + 0.5*np.sqrt(1.0 + 4.0/np.maximum(y, 1e-30))

# ----------------------------- grid / FFT Poisson -----------------------------
class Grid:
    """Cubic periodic grid; FFT Poisson solver for Phi_N from rho (vacuum-like via
    large box + zero-padding-by-size). We use an isolated (non-periodic) Green
    function via the standard 'zero-padding'? -> simpler: large box, subtract mean.
    For phantom-mass-in-core (<<box) the periodic images are far + symmetric, their
    net field in the core ~0; we verify with a box-size convergence check."""
    def __init__(self, L, n):
        self.L = L          # box size (m)
        self.n = n
        self.d = L/n        # cell size
        ax = (np.arange(n) - n//2)*self.d
        self.x = ax
        self.X, self.Y, self.Z = np.meshgrid(ax, ax, ax, indexing='ij')
        self.r = np.sqrt(self.X**2 + self.Y**2 + self.Z**2)
        # k-grid for FFT Poisson
        k1 = 2*np.pi*np.fft.fftfreq(n, d=self.d)
        KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing='ij')
        self.k2 = KX**2 + KY**2 + KZ**2
        self.k2[0,0,0] = 1.0  # avoid /0; handle DC separately

    def phi_newton(self, rho):
        """solve nabla^2 Phi_N = 4 pi G rho, periodic, zero-mean source."""
        rho0 = rho - rho.mean()      # remove DC (periodic solvability)
        rho_k = np.fft.fftn(rho0)
        phi_k = -4*np.pi*G*rho_k/self.k2
        phi_k[0,0,0] = 0.0
        return np.real(np.fft.ifftn(phi_k))

    def grad(self, f):
        """central-difference gradient (periodic)."""
        gx = (np.roll(f,-1,0) - np.roll(f,1,0))/(2*self.d)
        gy = (np.roll(f,-1,1) - np.roll(f,1,1))/(2*self.d)
        gz = (np.roll(f,-1,2) - np.roll(f,1,2))/(2*self.d)
        return gx, gy, gz

    def div(self, fx, fy, fz):
        dx = (np.roll(fx,-1,0) - np.roll(fx,1,0))/(2*self.d)
        dy = (np.roll(fy,-1,1) - np.roll(fy,1,1))/(2*self.d)
        dz = (np.roll(fz,-1,2) - np.roll(fz,1,2))/(2*self.d)
        return dx + dy + dz

    def laplacian(self, f):
        lap = (np.roll(f,-1,0)+np.roll(f,1,0)
              +np.roll(f,-1,1)+np.roll(f,1,1)
              +np.roll(f,-1,2)+np.roll(f,1,2) - 6*f)/self.d**2
        return lap

# ----------------------------- QUMOND phantom density -----------------------------
def qumond_phantom(grid, rho):
    """rho_ph = nabla^2(Phi)/(4 pi G) - rho, Phi from nabla^2 Phi = div[nu(y) grad Phi_N]."""
    phiN = grid.phi_newton(rho)
    gxN, gyN, gzN = grid.grad(phiN)
    gmag = np.sqrt(gxN**2 + gyN**2 + gzN**2)
    y = gmag/a0
    nu = nu_simple(y)
    # the QUMOND source S = div[nu * grad Phi_N] = 4 pi G rho_eff
    S = grid.div(nu*gxN, nu*gyN, nu*gzN)
    rho_eff = S/(4*np.pi*G)            # = rho_bar + rho_ph  (the total apparent density)
    rho_ph = rho_eff - rho
    return rho_ph, rho_eff, phiN, gmag

# ----------------------------- baryon models -----------------------------
def beta_rho(grid, rho0, rc, beta, center=(0,0,0)):
    xc,yc,zc = center
    rr = np.sqrt((grid.X-xc)**2+(grid.Y-yc)**2+(grid.Z-zc)**2)
    return rho0/(1.0+(rr/rc)**2)**(1.5*beta)

def beta_norm(rho0, rc, beta, Rmax):
    """analytic-ish enclosed mass of beta model out to Rmax (spherical)."""
    rr = np.linspace(1e-3*rc, Rmax, 8000)
    rho = rho0/(1.0+(rr/rc)**2)**(1.5*beta)
    return np.trapz(4*np.pi*rr**2*rho, rr)

def plummer_rho(grid, M, a, center):
    """Plummer sphere density on the grid, total mass M, scale a, centered."""
    xc,yc,zc = center
    rr2 = (grid.X-xc)**2+(grid.Y-yc)**2+(grid.Z-zc)**2
    return (3*M)/(4*np.pi*a**3)*(1.0+rr2/a**2)**(-2.5)

def smeared_galaxy_rho(grid, gal_masses, gal_radii, profile='same_radial'):
    """SMOOTH counterpart: smear total galaxy mass into a radial profile.
    'same_radial': distribute galaxy mass with the SAME radial number-density profile
    (so M_gal(<r) matches the discrete ensemble's mean) -> spherically symmetric shell.
    We build it from the radial distribution of the discrete galaxies."""
    raise NotImplementedError  # built in main via spherical shells

# ----------------------------- mass-enclosed helper -----------------------------
def M_enclosed(grid, rho, R):
    """integrate rho over the sphere r<R."""
    mask = grid.r < R
    return np.sum(rho[mask])*grid.d**3
