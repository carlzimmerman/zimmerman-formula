"""
CLEAN PHYSICS CHECK (grid-independent): does breaking baryons into discrete clumps
ADD or SUBTRACT total QUMOND phantom mass, relative to a smooth distribution of the
SAME total mass enclosed in the SAME radius?

Two rigorous, analytic-where-possible sub-checks:

(A) SPHERICAL ENCLOSED-MASS THEOREM (exact in MOND/QUMOND for spherical symmetry):
    For spherical symmetry, g(r) = nu(g_N/a0) g_N(r), g_N(r)=G M_bar(<r)/r^2.
    => total apparent mass M_app(<r) = (r^2/G) nu(g_N/a0) g_N(r) depends ONLY on
       M_bar(<r). Two systems with the same spherical M_bar(<r) have the SAME phantom.
    This is the "redistributes-only" baseline: if Carl's effect existed in spherical
    symmetry it would VIOLATE this theorem. So any collective ADD must be NON-SPHERICAL.

(B) THE NON-SPHERICAL QUESTION (the real test): take a fixed total mass M and split it
    into N equal clumps inside a region of size R, vs the same M smooth. Compute the
    TOTAL phantom mass in a large enclosing sphere. Sub-additivity of the deep-MOND
    field (field of 2 masses ~ sqrt(2M) < 2 sqrt(M)) predicts the discrete TOTAL
    phantom is <= smooth. We compute it exactly for point masses via a high-res local
    QUMOND grid AROUND the clumps and integrate the phantom, with mass-exact deposition.

Output: the sign and size of (discrete - smooth) total phantom.
"""
import numpy as np

G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.086e19
a0   = 9.36e-11

def nu_simple(y):
    return 0.5 + 0.5*np.sqrt(1.0 + 4.0/np.maximum(y,1e-30))

# =====================================================================
# (A) spherical enclosed-mass theorem -- exact, analytic
# =====================================================================
def spherical_Mapp(Mbar_enc, r):
    """apparent (baryon+phantom) enclosed mass for spherical symmetry."""
    gN = G*Mbar_enc/r**2
    g  = nu_simple(gN/a0)*gN
    return g*r**2/G

def check_spherical_theorem():
    print("="*70)
    print("(A) SPHERICAL ENCLOSED-MASS THEOREM (the redistributes-only baseline)")
    print("="*70)
    # same enclosed baryon mass, two different INTERNAL distributions (both spherical)
    M = 1e13*Msun
    r = 200*kpc
    # distribution 1: all mass at center (point); distribution 2: uniform shell inside r/2
    # both have M_bar(<r)=M -> theorem says identical apparent mass
    Mapp = spherical_Mapp(M, r)
    print(f"  M_bar(<{r/kpc:.0f}kpc)={M/Msun:.2e} -> M_app={Mapp/Msun:.3e} Msun, "
          f"phantom={ (Mapp-M)/Msun:.3e} (boost x{Mapp/M:.2f})")
    print("  THEOREM: any spherical rearrangement with the same M_bar(<r) gives the")
    print("  SAME apparent/phantom mass. => collective ADD requires NON-sphericity.\n")
    return Mapp

# =====================================================================
# (B) non-spherical: N point clumps vs smooth, exact local QUMOND
# =====================================================================
class LocalGrid:
    """High-res periodic grid for exact phantom integration around clumps.
    Mass deposited EXACTLY via analytic point-source Newtonian potential (no CIC mass
    loss): we build Phi_N analytically as sum of -G m_i / |r-r_i| (softened), so the
    Newtonian field is EXACT regardless of grid; the grid is used only to take the
    QUMOND divergence and integrate the phantom. This removes the resolution/mass-loss
    bug entirely."""
    def __init__(self, L, n):
        self.L=L; self.n=n; self.d=L/n
        ax=(np.arange(n)-n//2)*self.d
        self.X,self.Y,self.Z=np.meshgrid(ax,ax,ax,indexing='ij')
        self.r=np.sqrt(self.X**2+self.Y**2+self.Z**2)

    def phiN_points(self, masses, pos, soft):
        """EXACT Newtonian potential of point masses (Plummer-softened)."""
        phi=np.zeros_like(self.X)
        for m,(x0,y0,z0) in zip(masses,pos):
            rr=np.sqrt((self.X-x0)**2+(self.Y-y0)**2+(self.Z-z0)**2 + soft**2)
            phi += -G*m/rr
        return phi

    def gradN_points(self, masses, pos, soft):
        """EXACT analytic Newtonian gradient (acceleration field) of softened points."""
        gx=np.zeros_like(self.X);gy=np.zeros_like(self.X);gz=np.zeros_like(self.X)
        for m,(x0,y0,z0) in zip(masses,pos):
            dx=self.X-x0;dy=self.Y-y0;dz=self.Z-z0
            rr2=dx*dx+dy*dy+dz*dz+soft**2
            rr=np.sqrt(rr2)
            # grad(-Gm/r) = Gm r_vec/r^3 ; this is grad Phi (points toward mass = +dx? )
            # Phi=-Gm/r, dPhi/dx = Gm * dx / r^3
            f=G*m/(rr2*rr)
            gx+=f*dx;gy+=f*dy;gz+=f*dz
        return gx,gy,gz

    def div(self,fx,fy,fz):
        dx=(np.roll(fx,-1,0)-np.roll(fx,1,0))/(2*self.d)
        dy=(np.roll(fy,-1,1)-np.roll(fy,1,1))/(2*self.d)
        dz=(np.roll(fz,-1,2)-np.roll(fz,1,2))/(2*self.d)
        return dx+dy+dz

    def Menc(self,rho,R):
        return np.sum(rho[self.r<R])*self.d**3

def qumond_phantom_points(grid, masses, pos, soft):
    """rho_ph = div[nu grad Phi_N]/(4 pi G) - rho_bar, with EXACT analytic grad Phi_N.
    rho_bar here is the point mass -> integrates to sum(masses); we return total phantom
    by integrating div[nu grad Phi_N]/(4 pi G) (=M_app) minus the known baryon mass."""
    gx,gy,gz=grid.gradN_points(masses,pos,soft)
    gmag=np.sqrt(gx**2+gy**2+gz**2)
    nu=nu_simple(gmag/a0)
    S=grid.div(nu*gx,nu*gy,nu*gz)
    rho_app=S/(4*np.pi*G)
    return rho_app, gmag

def run_B():
    print("="*70)
    print("(B) NON-SPHERICAL: N clumps vs 1 smooth blob, EXACT analytic Newtonian field")
    print("="*70)
    # total mass M inside a region of half-size D; integrate phantom in sphere R_int >> D
    M_tot = 1e13*Msun
    D     = 150*kpc          # clumps scattered within +-D
    R_int = 800*kpc          # integration sphere (deep-MOND, >> MOND radius of M_tot)
    soft  = 8*kpc            # galaxy softening (Plummer-ish); also the smooth-blob scale floor
    rM = np.sqrt(G*M_tot/a0)
    print(f"  M_tot={M_tot/Msun:.2e}, clump region +-{D/kpc:.0f}kpc, "
          f"MOND radius r_M=sqrt(GM/a0)={rM/kpc:.0f}kpc, integrate to {R_int/kpc:.0f}kpc")

    L=4000*kpc; n=200       # cell=20 kpc; soft=8kpc<cell -> use soft>=cell for stability
    soft=max(soft, 1.5*L/n)
    grid=LocalGrid(L,n)
    print(f"  grid L={L/kpc:.0f}kpc n={n} cell={L/n/kpc:.1f}kpc soft={soft/kpc:.1f}kpc")

    results={}
    for Nc in [1, 8, 27, 100, 300]:
        np.random.seed(7)
        if Nc==1:
            masses=[M_tot]; pos=[(0,0,0)]
        else:
            # place Nc equal clumps randomly within +-D (cubic), recenter to COM
            p=np.random.uniform(-D,D,(Nc,3))
            p-=p.mean(0)
            masses=[M_tot/Nc]*Nc; pos=[tuple(pp) for pp in p]
        rho_app,gmag=qumond_phantom_points(grid,masses,pos,soft)
        Mapp=grid.Menc(rho_app,R_int)/Msun
        # baryon mass inside R_int = M_tot (all clumps are inside D<<R_int)
        Mbar=M_tot/Msun
        Mph=Mapp-Mbar
        results[Nc]=Mph
        print(f"  N={Nc:4d}: M_app(<{R_int/kpc:.0f})={Mapp:.4e}  phantom={Mph:.4e} Msun "
              f"(boost x{Mapp/Mbar:.3f})")
    print()
    ref=results[1]
    print("  COLLECTIVE EFFECT (discrete phantom / single-blob phantom):")
    for Nc,Mph in results.items():
        print(f"    N={Nc:4d}: ratio={Mph/ref:.4f}  ({100*(Mph/ref-1):+.1f}%)")
    print("\n  INTERPRETATION: ratio>1 => clumping ADDS phantom (Carl's collective effect);")
    print("  ratio<=1 => sub-additive / redistribute-only (the deep-MOND sqrt-law prediction).")
    return results

if __name__=="__main__":
    check_spherical_theorem()
    print()
    run_B()
