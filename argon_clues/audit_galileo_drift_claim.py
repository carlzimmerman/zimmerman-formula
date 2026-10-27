"""argon_clues: audit of the 'Galileo drift' derivation of kappa=1/2 and the 'per-steradian bare G' argument."""
import sympy as s
t, dt, gN, gDC, lam, G, rho, c, tau = s.symbols('t dt g_N g_DC lambda G rho c tau', positive=True)
dr = s.integrate(gN*t, (t, 0, dt)); dvN = gN*dt
print('1. displacement dr =', dr, ', dv_N =', dvN)
# paste: (dv)^2 = dv_N^2 + g_DC*dr  -> lambda = 1  -> a0 = kappa g_DC with kappa = lambda/2
gobs2 = s.expand((dvN**2 + lam*gDC*dr)/dt**2)
print('2. g_obs^2 =', gobs2, ' -> a0 = (lambda/2) g_DC ; paste sets lambda=1')
# energy-consistent work term: Delta(v^2) = 2 a dr (v^2/2 = a dr) -> lambda = 2
print('   energy consistency: dv_N^2 = g_N^2 dt^2 = 2 g_N dr_N (check):', s.simplify(dvN**2 - 2*gN*dr) == 0)
print('   so the SAME rule applied to the drift term gives dv^2 = 2 g_DC dr -> lambda=2 -> kappa = 1, not 1/2')
print('   kappa(lambda) =', {l: s.Rational(l, 2) for l in (1, 2, 4)}, ' : lambda is a free pairing coefficient; 1/2 is inserted by choosing lambda=1')
# the pairing itself: why dr of the NEWTONIAN perturbation, why g_DC (not g_DC*sign, not time-averaged <v>?)
print('3. ordering: g_DC*dr uses the perturbation displacement; no equation of motion or action is varied, nothing fixes the cross-term (it is added by hand). Dimensions pass for any lambda.')
# the 'ray' argument: dg/dtau = c G rho does not give g = c sqrt(G rho)
g = s.Function('g')
print('4. dg/dtau = c G rho  =>  g = c G rho * tau, ', 'equals c sqrt(G rho) only if tau = 1/sqrt(G rho) is inserted (the free-fall time): a posit, not a derivation')
print('5. rho_DE is the same number whether written via H^2 = 8piG rho/3 or via bare G rho; "4pi already divided out" changes no value: c H/ g_DC = sqrt(8pi/3) is an identity either way, and the gate scale choice (sqrt(G rho) vs H) is untouched.')
print('6. Audit 1 in the paste is right (a_floor = a0/2), consistent with my correction; Audit 3 (inverting g_obs^2 = g_N^2 + a0 g_N) is trivial algebra and already certified.')
