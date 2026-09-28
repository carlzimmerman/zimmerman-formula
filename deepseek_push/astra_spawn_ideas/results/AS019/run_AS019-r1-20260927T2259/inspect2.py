import math, json
txt = open('raw_output.json').read()
d = json.loads(txt[:txt.index('BOUNDS_OK')])

# Recompute the two-component residual distribution to locate the max.
pc = 3.085677581491367e16; G = 6.67430e-11; a0 = 9.3619e-11
r1 = 2.0*1000.0*pc; R2 = 25.0*1000.0*pc
rho1 = 1.0e-20; rho2 = 3.0e-22; p = 2.0
def M_core():
    return (4.0/3.0)*math.pi*rho1*r1**3
def M_env(r):
    return 4*math.pi*rho2*r1**p*(r**(3-p)-r1**(3-p))/(3-p)
def M_enc2(r):
    if r <= r1: return (4.0/3.0)*math.pi*rho1*r**3
    if r <= R2: return M_core() + M_env(r)
    return M_core() + M_env(R2)
def rho2_fn(r):
    if r <= r1: return rho1
    if r <= R2: return rho2*(r/r1)**(-p)
    return 0.0
def log_slope_of(f, xs):
    return [(math.log(f(xs[i+1]))-math.log(f(xs[i-1])))/(math.log(xs[i+1])-math.log(xs[i-1]))
            for i in range(1, len(xs)-1)], xs[1:-1]

grid2 = [r1*1.02 + i*(R2*0.95-r1*1.02)/4000 for i in range(4001)]
s, rmid = log_slope_of(lambda r: (G*a0*M_enc2(r))**0.25, grid2)
analytic = [(1.0/4.0)*(4*math.pi*r**3*rho2_fn(r))/M_enc2(r) for r in rmid]
rel = [abs((a-b)/b) if b != 0 else 0.0 for a, b in zip(s, analytic)]
worst = sorted(range(len(rel)), key=lambda i: -rel[i])[:8]
for i in worst:
    print(f'r_pc={rmid[i]/(1000*pc):.4f}  rel={rel[i]:.3e}  rho={rho2_fn(rmid[i]):.2e}')
print('median rel:', sorted(rel)[len(rel)//2])