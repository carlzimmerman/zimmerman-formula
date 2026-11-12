import sympy as sp

I0, mu, a, x, T, ns, k2, X, R = sp.symbols('I0 mu a x T nstar k2 X R', positive=True)
aa, xb, xa, n0, phi = sp.symbols('a_b x_b x_a n0 phi', positive=True)

# --- (1) FRW EOS for the quadratic well ---
# V = mu^2 (Q-1)^2 /2 ; n = V_Q = mu^2 x ; Q = 1+x
xm = I0/(2*mu**2*a**3)                 # xbar(a) from a^3 n(xbar) = n0, I0 = 2 n0
w_exact = xm/(2+xm)                    # exact w = p/rho for quadratic well
w_frw = (I0/(4*mu**2))/(I0/(4*mu**2)+a**3)
print('1 FRW identity      :', sp.simplify(w_exact - w_frw) == 0)
# derive p/rho directly to be safe
xs = sp.symbols('xs', positive=True)
V  = mu**2*xs**2/2
Q  = 1+xs
n  = sp.diff(V, xs)                    # dV/dQ = dV/dx since Q=1+x
rho = (Q*n - V)
p   = V
print('  n = mu^2 x        :', sp.simplify(n - mu**2*xs) == 0)
print('  w = x/(2+x)       :', sp.simplify(p/rho - xs/(2+xs)) == 0)

# --- (2) sound speeds ---
# quadratic
n_q = mu**2*xs
dn_q = sp.diff(n_q, xs)
cs_DT1_q = sp.simplify(n_q/dn_q)                 # n/n'  (DT1 leading form)
cad_q    = sp.simplify(n_q/((1+xs)*dn_q))         # exact n/(Q n')
print('2 quad n/n\' = x     :', sp.simplify(cs_DT1_q - xs) == 0)
print('  quad cad2 = x/(1+x):', sp.simplify(cad_q - xs/(1+xs)) == 0)
print('  cad2 - w  = x/((1+x)(2+x)):', sp.simplify(cad_q - xs/(2+xs) - xs/((1+xs)*(2+xs))) == 0)
# exponential
n_e = ns*sp.exp(xs/T)
dn_e = sp.diff(n_e, xs)
cs_DT1_e = sp.simplify(n_e/dn_e)
cad_e    = sp.simplify(n_e/((1+xs)*dn_e))
print('  exp n/n\' = T      :', sp.simplify(cs_DT1_e - T) == 0)
print('  exp cad2 = T/Q    :', sp.simplify(cad_e - T/(1+xs)) == 0)
# exact w for exponential, V = T n (DT1's normalization V0 = T nstar)
Ve = T*n_e
rho_e = (1+xs)*n_e - Ve
p_e   = Ve
w_e = sp.simplify(p_e/rho_e)
print('  exp w = T/(Q-T)   :', sp.simplify(w_e - T/(1+xs-T)) == 0)
print('  w - cad2 = T^2/(Q(Q-T)):', sp.simplify(w_e - cad_e - T**2/((1+xs)*((1+xs)-T))) == 0)

# --- (3) Jeans wavenumber k_J^2 := kappa*rho / c_ad^2 ---
kJ_q = sp.simplify(rho_e.subs(xs,xs)*0)  # placeholder
kJ_quad = sp.simplify(rho / cad_q)
print('3 quad kJ2 = mu^2 (1+x)(1+x/2):', sp.simplify(kJ_quad - mu**2*(1+xs)*(1+xs/2)) == 0)
kJ_exp = sp.simplify(rho_e / cad_e)
print('  exp  kJ2 = Q(Q-T) n/T       :', sp.simplify(kJ_exp - (1+xs)*((1+xs)-T)*n_e/T) == 0)
print('  exp  n\'  = n/T (density-dep):', sp.simplify(dn_e - n_e/T) == 0)

# --- (5) budget ---
XX = (sp.sqrt(1+4*x**2)-1)/2
print('5 X(1+X) = x^2      :', sp.simplify(XX*(1+XX) - x**2) == 0)
xb_s = sp.sqrt(R*(1+R))
# sympy will not auto-simplify sqrt((2R+1)^2) with R > 0; factor the radicand by hand first
radicand = sp.factor(sp.expand(1 + 4*R*(1+R)))
print('  X(x_b) = R        :',
      sp.simplify(((sp.sqrt(radicand) - 1)/2) - R) == 0, '   [radicand =', radicand, ']')
