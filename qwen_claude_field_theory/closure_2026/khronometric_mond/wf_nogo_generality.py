#!/usr/bin/env python3
"""
wf_nogo_generality.py

Two questions:
(A) Is Flanagan's no-go GENERAL over MOND functions, or specific to Carl's W?
(B) Does the K^2 (khronometric) backbone contribute to the 2-derivative time
    KINETIC coefficient in the non-rel limit, i.e. can it flip the ghost sign?

--------------------------------------------------------------------------
(A) GENERAL NO-GO.
Longitudinal khronon time-kinetic coefficient ~ (1 - W''(y)),  W'' = (y*mu)'.
Write h(y) = 1 - mu(y) >= 0  (sub-Newtonian deficit; mu<=1).
Then   W'' = (y mu)' = (y(1-h))' = 1 - (y h)'.
So     1 - W'' = (y h)'  =  d/dy [ y (1-mu) ].
No-ghost (1-W''>=0)  <=>  y(1-mu)  is NON-DECREASING.
Flanagan's Newtonian boundary condition (5):  f -> const  <=>  f' = 2a(mu-1) -> 0
   <=>  a(1-mu) -> 0  <=>  y(1-mu) -> 0  as y->inf.
Deep-MOND boundary (4): mu->0 as y->0 so y(1-mu) -> 0 as y->0 too, and >0 between.
A function that is 0 at both ends, strictly >0 in between, CANNOT be monotonic
non-decreasing on all of (0,inf): it must turn over => (y(1-mu))' < 0 somewhere
=> 1 - W'' < 0 there => LONGITUDINAL KHRONON GHOST.  This is Flanagan Eq(54).
--------------------------------------------------------------------------
"""
import sympy as sp

y = sp.symbols('y', positive=True)

def report(name, mu_expr):
    mu = mu_expr
    h  = sp.simplify(1 - mu)                 # deficit
    g  = sp.simplify(y*h)                    # y(1-mu)  -- must be nondecreasing for no-ghost
    gp = sp.simplify(sp.diff(g, y))          # 1 - W''
    Wpp = sp.simplify(1 - gp)
    print(f"--- {name}:  mu = {mu}")
    print(f"    y(1-mu)            = {g}")
    print(f"    (1-W'') = d/dy[y(1-mu)] = {gp}")
    print(f"    W''                = {Wpp}")
    # limits
    g0 = sp.limit(g, y, 0)
    ginf = sp.limit(g, y, sp.oo)
    print(f"    y(1-mu): y->0 = {g0},  y->inf = {ginf}")
    # where is 1-W'' negative (ghost)?
    sol = sp.solve(sp.Eq(gp, 0), y)
    print(f"    ghost boundary (1-W''=0) at y = {sol}")
    print()

# Carl's exact-exponential-family primitive:
report("Carl W  (mu=1-e^-y)", 1 - sp.exp(-y))
# 'standard' MOND mu = y/sqrt(1+y^2):
report("standard  mu=y/sqrt(1+y^2)", y/sp.sqrt(1+y**2))
# 'simple' MOND mu = y/(1+y):
report("simple    mu=y/(1+y)", y/(1+y))

print("="*70)
print("POWER-LAW-TAIL LOOPHOLE (theory -> khronometric, NOT GR, at high a):")
print("Take mu -> 1 - c/y  (residual acceleration term survives at high a).")
c = sp.symbols('c', positive=True)
mu_pl = 1 - c/y
g_pl = sp.simplify(y*(1-mu_pl)); gp_pl = sp.simplify(sp.diff(g_pl,y))
print(f"   mu=1-c/y : y(1-mu) = {g_pl} (CONSTANT c) -> (1-W'') = {gp_pl} (=0, marginal)")
fprime_pl = sp.simplify(2*y*(mu_pl-1))     # ~ f'(a)/a0 units
print(f"   BUT f' ~ 2 a0 y (mu-1) = {sp.simplify(2*y*(mu_pl-1))}  -> {sp.limit(2*y*(mu_pl-1),y,sp.oo)}")
print("   => f' -> -2 a0 c  (NONzero): f does NOT ->const, i.e. Newtonian bc (5) FAILS;")
print("   theory keeps a residual Lorentz-violating acceleration term at high a")
print("   (= Bonetti-Barausse 'reduces to khronometric not GR' branch)")
print("   => avoids khronon ghost at the PRICE of preferred-frame/PPN residual (Cassini).")
print()
print("VERDICT (A): The no-go is GENERAL for any mu with mu->1 fast enough that")
print("y(1-mu)->0 (Flanagan's f->const Newtonian limit). It is NOT special to Carl.")
print("Carl's exponential mu=1-e^-y is the FASTEST decay => ghost is unavoidable,")
print("onset exactly at y=1 (a=a0), worst at y=2 (1-W''=-0.135), ->0^- as y->inf.")
