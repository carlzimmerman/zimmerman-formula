"""argon_clues: audit of the 'advected strain-memory' basin derivation."""
import sympy as s, math
# 1. The pasted pass test is tautological: u_eff is DEFINED without g_ext in the primary branch.
g_ext,u,tid=s.symbols('g_ext u tid',positive=True)
u_eff = u*(1 + 0*(g_ext) + tid**2)
print('1. d(u_eff)/d(g_ext) =', s.diff(u_eff,g_ext), ' (zero because the pasted u_eff formula omits g_ext by construction; the sigma ratio (1+eta^3)^(-1/4) is also written down, not derived from the transport equation)')
# 2. (P.grad)v_c for a rotating medium is orthogonal to P
x,y,z,Om,Pr=s.symbols('x y z Omega P_r',real=True)
v=sp=s.Matrix([-Om*y, Om*x, 0]); P=s.Matrix([Pr*x/s.sqrt(x**2+y**2), Pr*y/s.sqrt(x**2+y**2), 0])
J=v.jacobian([x,y,z]); PdotGradV=J*P
print('2. (P.grad)v_c for rigid rotation, radial P:', s.simplify(PdotGradV.T), ' dot P =', s.simplify(PdotGradV.dot(P)), '-> P_eff is perpendicular to P (azimuthal), so the steady state cannot give P_eff = P; a spherical non-rotating system gives P_eff = 0 (the paste admits this as Objection 2)')
# 3. numbers
G=6.6743e-11; Ms=1.98847e30; a0=9.36e-11; kpc=3.0857e19
for Mst in (1.6e5, 2.5e5, 1.0e6):
    sig=(4*G*Mst*Ms*a0/81)**0.25/1e3
    print('3. sigma_iso(M*=%.1e) = %.2f km/s (paste: 4.10)'%(Mst,sig))
sig=(4*G*1.6e5*Ms*a0/81)**0.25/1e3
for obs,e in ((2.7,0.3),):
    print('   vs observed %.1f+-%.1f: tension of the hard-basin isolated law = %.1f sigma (paste: 3.6 sigma using 4.10: %.1f)'%(obs,e,(sig-obs)/e,(4.10-obs)/e))
print('   McGaugh 2016 (EFE) predicted ~2.1 km/s for Crater II (paste: global AQUAL 2.10): the observed 2.7+-0.3 lies 2 sigma above it and 1.4 sigma below the isolated law with M*=1.6e5: not decisive')
# 4. basin radius from baryons only
for Mh,R in ((6e10,30),(1e12,30)):
    rB=R*kpc*(1.6e5/(2*Mh))**(1/3)/kpc
    print('4. r_B = R (M_sat/2M_host)^(1/3), R=30 kpc, M_sat=1.6e5, M_host=%.0e -> %.2f kpc (paste: 1.4 kpc; needs M_sat ~ %.1e Msun)'%(Mh,rB,2*Mh*(1.4/30)**3))
