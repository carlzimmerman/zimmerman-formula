"""X26_cold_sector_map (criteria b10263968f), section 5: first-principles cuts on (r, q), derived in sympy.
Family: c_s^2 = c_*^2 (sigma/sigma_*)^{2r} (rho/rho_*)^q a^{2p-1}.
Usage: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x26_derive.py     (X26_MUTATE=1: MUTATE twin, exit 1)
kappa = 1/2 FITTED; footings never pooled; cold energy = field mass, no particle; not theory closed."""
import os, sys, json
sys.dont_write_bytecode = True
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("X26_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)
RES = {"lane": "X26_cold_sector_map", "part": "derive", "criteria": "b10263968f", "mutate": MUT, "checks": {}}
def chk(name, ok, txt):
    RES["checks"][name] = bool(ok); P(f"{name} {'PASS' if ok else 'FAIL'}: {txt}")

a, p, r, q, cst, s0, rho0, G, M, R, c, gam = sp.symbols("a p r q c_star sigma_star rho_star G M R_L c gamma", positive=True)
rr, qq = sp.symbols("r q", real=True)
P("X26 derive: first-principles cuts (sympy); kappa = 1/2 FITTED; not theory closed")

# D1: p_eff of the cosmic medium. sigma_cos = sqrt(G M/(2 a R_L)), rho_cos = rho_b0 a^-3.
rb0 = sp.symbols("rho_b0", positive=True)
sig_cos = sp.sqrt(G*M/(2*a*R)); rho_cos = rb0*a**-3
cs = cst*(sig_cos/s0)**rr*(rho_cos/rho0)**(qq/2)*a**(p - sp.Rational(1, 2))
expo = sp.simplify(a*sp.diff(sp.log(cs), a))
peff = sp.simplify(expo + sp.Rational(1, 2))
target = p - rr/2 - 3*qq/2
chk("D1", sp.simplify(peff - target) == 0, f"c_s,cos ~ a^(p_eff - 1/2), p_eff = {sp.simplify(peff)}")
RES["p_eff"] = str(sp.simplify(peff))

# D2 (FP1): barotropic reading P = K rho^(1+q): dP/drho > 0 <=> q > -1. Schwarzschild: N^2 = g dlnP/dr (1/gamma - 1/Gamma).
K, rho = sp.symbols("K rho", positive=True)
Pp = K*rho**(1 + qq); dPdrho = sp.simplify(sp.diff(Pp, rho)/(Pp/rho))
cond_stab = sp.solve_univariate_inequality(dPdrho > 0, qq, relational=True)
chk("D2a", dPdrho == 1 + qq and sp.simplify(cond_stab) in (sp.Gt(qq, -1), sp.Lt(-1, qq), sp.And(sp.Lt(-1, qq), sp.Lt(qq, sp.oo))),
    f"dP/drho = ({dPdrho}) P/rho > 0 <=> {cond_stab}")
Gam = 1 + qq
# polytropic stratification: dln rho/dr = (1/Gamma) dlnP/dr; adiabatic: (1/gamma) dlnP/dr. N^2 = -g [dln rho/dr - (1/gamma) dlnP/dr]
dlnP = sp.symbols("dlnP", negative=True); g = sp.symbols("g", positive=True)
N2 = sp.simplify(-g*((1/Gam)*dlnP - (1/gam)*dlnP))
N2fac = sp.factor(N2)
# N2 > 0 <=> (1/gamma - 1/Gamma) > 0 (since -g dlnP > 0) <=> Gamma < gamma <=> q < gamma - 1
test53 = sp.solve_univariate_inequality((N2/(-g*dlnP)).subs(gam, sp.Rational(5, 3)) > 0, qq, relational=True, domain=sp.Interval.open(-1, sp.oo))   # -g dlnP > 0
test43 = sp.solve_univariate_inequality((N2/(-g*dlnP)).subs(gam, sp.Rational(4, 3)) > 0, qq, relational=True, domain=sp.Interval.open(-1, sp.oo))
iso_ok = sp.simplify(N2.subs(qq, 0)/(-g*dlnP)) == sp.simplify(1 - 1/gam)
chk("D2b", iso_ok and test53.as_set() == sp.Interval.open(-1, sp.Rational(2, 3)), f"N^2 = {N2fac}; isothermal (q=0, per-system) stable iff gamma > 1; barotropic: gamma=5/3 -> {test53}; gamma=4/3 -> {test43}")
RES["FP1"] = {"hard": "q > -1", "schwarzschild_barotropic": "q < gamma - 1", "gamma_5_3": str(test53), "gamma_4_3": str(test43),
              "isothermal_per_system": "stable for any gamma > 1"}

# D3 (FP2): asymptotic causality. log c_s = log c_* + r log(sigma/sigma_*) + (q/2) log(rho/rho_*).
Ls, Lr = sp.symbols("L_sigma L_rho", real=True)
logc = sp.log(cst) + rr*Ls + qq/2*Lr
lim_s0 = {rv: sp.limit(logc.subs(rr, rv), Ls, -sp.oo) for rv in (-1, 0, 1)}
lim_rinf = {qv: sp.limit(logc.subs(qq, qv), Lr, sp.oo) for qv in (-sp.Rational(1, 2), 0, sp.Rational(1, 2))}
lim_r0 = {qv: sp.limit(logc.subs(qq, qv), Lr, -sp.oo) for qv in (-sp.Rational(1, 2), 0, sp.Rational(1, 2))}
ok3 = (lim_s0[-1] == sp.oo and lim_s0[1] == -sp.oo and lim_rinf[sp.Rational(1, 2)] == sp.oo and lim_rinf[-sp.Rational(1, 2)] == -sp.oo
       and lim_r0[-sp.Rational(1, 2)] == sp.oo and lim_r0[sp.Rational(1, 2)] == -sp.oo)
chk("D3", ok3, "c_s -> inf as sigma -> 0 iff r < 0; as rho -> inf iff q > 0; as rho -> 0 iff q < 0: asymptotic causality needs r >= 0 and q = 0 "
    "(else a cutoff); the finite-range cut is computed in the main script")
RES["FP2"] = {"asymptotic": "r >= 0 and q = 0 (unbounded sigma, rho ranges); otherwise causality needs a cutoff", "computed": "main script"}

# D4 (FP3): virial theorem for an isothermal test fluid in a flat well (g = 2 sigma^2/r): rho ~ r^-beta.
x, beta, s, cs2 = sp.symbols("x beta sigma c_s2", positive=True)
Rv, rhoR = sp.symbols("R rho_R", positive=True)
prof = rhoR*(x/Rv)**(-beta)
Menc = sp.integrate(4*sp.pi*x**2*prof, (x, 0, Rv), conds="none")
Menc = sp.simplify(Menc.subs(beta, beta))  # valid for beta < 3
lhs = 3*cs2*Menc - 4*sp.pi*Rv**3*cs2*rhoR                    # 3 int P dV - surface term
W = sp.integrate(4*sp.pi*x**2*prof*x*(2*s**2/x), (x, 0, Rv), conds="none")
vir = sp.simplify((lhs - W).subs(cs2, 2*s**2/beta))
surf_frac = sp.simplify(4*sp.pi*Rv**3*rhoR/(3*Menc))       # surface term / (3 c_s^2 M) = (3 - beta)/3
bnd = sp.solve(sp.Eq(surf_frac, 0), beta)
ratio = sp.sqrt(sp.Rational(2, 3))
chk("D4", sp.simplify(vir) == 0 and sp.simplify(surf_frac - (3 - beta)/3) == 0 and bnd == [3],
    f"hydrostatic => beta c_s^2 = 2 sigma^2 (virial identity, residual {sp.simplify(vir)}); surface-pressure share (3-beta)/3 -> 0 "
    f"(self-bound, no external confinement) iff beta >= 3 iff c_s <= sqrt(2/3) sigma = {float(ratio):.4f} sigma")
# linear separability statement: log(c_s/sigma) = log c_* + (r-1) L_sigma + (q/2) L_rho
lin = sp.expand(logc - Ls)
chk("D4b", sp.Poly(lin.subs(sp.log(cst), 0), Ls, Lr).total_degree() == 1 and sp.diff(lin, Ls) == rr - 1,
    f"log(c_s/sigma) = {lin}: linear in (log sigma, log rho); with q = 0 monotone in sigma (slope r - 1), so a q = 0 member cannot be "
    "self-bound at both ends of the sigma range and unbound in the middle")
RES["FP3"] = {"retained_iff": "c_s <= sqrt(2/3) sigma (beta >= 3; X22's BCAP 2.9 is the hydrostatic edge)",
              "linear_form": str(lin), "q0": "monotone in sigma: cannot retain dwarfs and clusters while expelling SPARC"}

# D5 (FP4): mu-pincer Part F carried to the family. For r = 0, background state at (1+z_match)^3 = delta_well:
dw, zm = sp.symbols("delta_well z_match", positive=True)
cs_bg_over_well = sp.simplify(((rb0*(1 + zm)**3)/(rb0*dw))**(qq/2))
same = sp.simplify(cs_bg_over_well.subs(zm, dw**sp.Rational(1, 3) - 1))
chk("D5", same == 1, "r = 0, h ignored: the background has the well's c_s at (1+z_match)^3 = delta_well (Part F); "
    "the time factor a^(p-1/2) is the only way out, so forest gate (X22: p_eff >= p_min at c_s,need) => q <= (2/3)(p - r/2 - p_min)")
RES["FP4"] = {"inequality": "q <= (2/3)(p - r/2 - p_min)", "p_min_source": "X22 step 3B (forest not FAIL for p >= 3 at c_s,need); graded cut in main script"}
if MUT:  # MUTATE: wrong density scaling (rho ~ a^-2) must break D1
    peff_m = sp.simplify(a*sp.diff(sp.log(cst*(sig_cos/s0)**rr*((rb0*a**-2)/rho0)**(qq/2)*a**(p - sp.Rational(1, 2))), a) + sp.Rational(1, 2))
    chk("D1", sp.simplify(peff_m - target) == 0, f"MUTATE rho ~ a^-2: p_eff = {peff_m}")
n = sum(RES["checks"].values()); P(f"checks {n}/{len(RES['checks'])}")
open(os.path.join(HERE, f"x26_derive{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x26_derive_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if (n == len(RES["checks"]) and not MUT) else 1)
