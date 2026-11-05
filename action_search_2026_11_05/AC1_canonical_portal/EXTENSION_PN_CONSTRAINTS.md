# AC1 extension: all-angle frozen PN constraint block

Frozen before numerical fixtures. This is an explicit conditional quadratic
model extending AZ40; its coefficients are NOT claimed to be derived from a
solved charged cosmological/galactic background. Full metric shift, expansion,
background derivatives and interfaces remain excluded. No healthy action label.

Units K=1. Let kvec=k*nhat,k>0, H=diag(HT,HT,HL), HT,HL>1,
D=H+gamma*kvec*kvec^T, gamma>=0. Constraints c=(Phi,Px,Py,Pz),
coordinates q=(phi,sigma). The quadratic Lagrangian is

 L=dotq^T A dotq/2-q^T M q/2+c^T C c/2+c^T(B dotq+E q),
 A=diag(1,mu²), M=diag(k²+m²,rho_tau*k²),
 C=[[-k²+mu²,kvec^T],[kvec,-D]],
 B=[[-v,-mu²],[0,-kvec]], E=[[-t,0],[-h*ez,0]].

Here m² includes V_phiphi+W_phiphi at fixed P, h=W_Pphi projected
along the polarization, and t is a free algebraic lapse/scalar coefficient.
Do not assume the original action gives a chosen t without deriving it.
Potential-only coupling does not add a scalar-velocity term to W.

Targets: eliminate constraints; retain K=A-B^T C^-1 B,
R=-B^T C^-1 E and U=M+E^T C^-1 E. Derive the kinetic condition
for arbitrary angle and mu, reducing to AZ40 when mu=0 and parallel.
Establish a sufficient energy-positivity condition K>0,U>0; compute the
2x2 characteristic polynomial including the antisymmetric part R-R^T.
Check the decoupled scalar/clock known answer. For rho_tau>0 determine what
U11<0 implies (one negative omega² if detK>0).

Numerical corroboration: HT=1+s,HL=(1+s)², s=.1,1,100;
angles=0,pi/4,pi/2; k=1,100; gamma=0,1; v=0,1;
mu²=0 or one tenth k²*(1-Q), Q=nhat^T D^-1 nhat;
rho_tau=1. Coefficient t=.3,h=.2,m²=1 are fixtures, not astrophysical values.
Compare direct 4x4 constraint inversion and analytic formulas at 40/80 digits
(normalized <1e-25), all 144? enumerate explicitly and report true count
(3*3*2*2*2*2=144). Retain negative control mu²=2*k²*(1-Q), which must
fail positive definiteness; and U11<0 fixture with rho_tau=1 must yield
opposite signs of squared frequencies. No extra spectrum-wide claim from
fixtures; analytic inequalities carry the conditional conclusion.
