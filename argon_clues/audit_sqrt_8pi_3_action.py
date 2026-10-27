"""argon_clues: hostile audit of 'where does sqrt(8pi/3) come from' (Z/2 = a_kin/a0)."""
import sympy as s
c, G, rho, H, r, M, Lam = s.symbols('c G rho H r M Lambda', positive=True)
Hsq = 8*s.pi*G*rho/3                       # Friedmann, flat, Lambda-dominated
# 1. The pi is a UNITS ARTEFACT: in (c, G, rho) units a0 has no pi
a0 = c*s.sqrt(G*rho)/2
print('1. a0/(c sqrt(G rho)) =', s.simplify(a0/(c*s.sqrt(G*rho))), '| rational. a0/(cH) =', s.simplify(a0/(c*s.sqrt(Hsq))), '= 1/Z; its pi is Friedmann\'s 8pi/3, not new')
print('   a0^2 in Lambda units: c^4 Lambda/(32pi) =', s.simplify((a0**2).subs(rho, Lam*c**2/(8*s.pi*G))))
# 2. Local spherical Gauss: 4pi cancels
g = s.symbols('g'); flux = 4*s.pi*r**2*g
print('2. Gauss: g =', s.solve(s.Eq(flux, 4*s.pi*G*M), g)[0], '| 4pi cancels; Green fn 1/(4 pi |x-x\'|) x 4pi r^2 dr also cancels')
# 3. natural local accelerations from (c,G,rho), relative to c sqrt(G rho)
base = c*s.sqrt(G*rho)
cands = {
 'c H (Friedmann)': c*s.sqrt(Hsq),
 'c H/2 (tidal-type, NOT the DL gate scale)': c*s.sqrt(Hsq)/2,
 'DL gate with floor=kappa_dS: a0=2cH': 2*c*s.sqrt(Hsq),
 'tidal (4pi/3)G rho * (c/H)': (4*s.pi/3)*G*rho*c/s.sqrt(Hsq),
 'c sqrt(4 pi G rho) (Jeans)': c*s.sqrt(4*s.pi*G*rho),
 'field-energy balance g^2/(8piG)=rho c^2': c*s.sqrt(8*s.pi*G*rho),
 'observed a0': a0}
for k_, v in cands.items():
    print('3. %-44s / (c sqrt(G rho)) = %s = %.4f' % (k_, s.simplify(v/base), float(s.simplify(v/base))))
print('   -> every Lambda/H-only construction lands on cH x rational; a0 needs the rational 1/2 in (G,rho) units')
# 4. what the action-level condition would have to say
print('4. a0^2/G = rho c^2/4 ; equivalently field-energy density at a0: a0^2/(8 pi G) = rho c^2/(32 pi).')
print('   The "32pi" is the same statement as a0^2 = (rho c^2 G)/4 divided by 8piG: no new content, and no local action step supplies the 1/4.')
print('VERDICT: no sqrt(8pi/3) puzzle independent of kappa=1/2. The pi in Z is Friedmann\'s; the open number is the rational 1/2 in a0 = (1/2) c sqrt(G rho_DE). Unchanged: kappa FITTED.')
