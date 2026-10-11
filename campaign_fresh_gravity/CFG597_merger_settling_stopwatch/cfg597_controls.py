#!/usr/bin/env python3
"""CFG597 controls C1, C2, C3, C5 (FROZEN_CRITERIA.md section 5; C4 runs inside cfg597_main.py).
Run: nice -n 10 python3 cfg597_controls.py   -> cfg597_controls.out, cfg597_controls_results.json"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg597_lib as L
import cfg597_sim as S

OUT = []; RES = {}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, measured):
    RES[name] = dict(ok=bool(ok), measured=measured)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")


P("CFG597 controls (criteria ae49ff4d7). Units kpc, Gyr, Msun.")
# ---------------------------------------------------------------- C1 Poisson vs analytic Hernquist force
g = L.Grid()
M, a = 1e15, 300.0
r = g.radius_from(np.zeros(3))
rho = M * a / (2 * math.pi * np.maximum(r, 1e-3) * (r + a) ** 3)    # analytic density at cell centres (no renormalisation)
phi = g.poisson(rho)
gx = -np.gradient(phi, g.dx, axis=0)
xc = g.xc[0]
j, k = g.n[1] // 2, g.n[2] // 2                     # the cell row nearest the x axis (offset half a cell in y, z)
yy, zz = g.xc[1][j], g.xc[2][k]
rr = np.sqrt(xc ** 2 + yy ** 2 + zz ** 2)
g_an = -L.G * M * (rr / (rr + a)) ** 2 / rr ** 2 * (xc / rr)        # the analytic Hernquist force (frozen C1)
sel = (rr >= 3 * g.dx) & (rr <= 1500.0)
err = np.abs(gx[:, j, k][sel] / g_an[sel] - 1)
check("C1 Poisson: grid force vs the analytic Hernquist force (M 1e15, a 300 kpc), 3 cells <= r <= 1500 kpc, <= 3%",
      err.max() <= 0.03, f"max |rel err| = {err.max():.4f}, median {np.median(err):.4f} ({sel.sum()} cells)")
RES["C1_max_err"] = float(err.max())


# ---------------------------------------------------------------- C2 Sod shock tube through the same solver
def exact_riemann(rL, uL, pL, rR, uR, pR, gam, xi):
    cL, cR = math.sqrt(gam * pL / rL), math.sqrt(gam * pR / rR)
    def f(p, rk, pk, ck):
        if p > pk:
            A = 2 / ((gam + 1) * rk); B = (gam - 1) / (gam + 1) * pk
            return (p - pk) * math.sqrt(A / (p + B))
        return 2 * ck / (gam - 1) * ((p / pk) ** ((gam - 1) / (2 * gam)) - 1)
    lo, hi = 1e-8, 10.0
    for _ in range(200):
        pm = 0.5 * (lo + hi)
        if f(pm, rL, pL, cL) + f(pm, rR, pR, cR) + uR - uL > 0:
            hi = pm
        else:
            lo = pm
    ps = 0.5 * (lo + hi); us = 0.5 * (uL + uR) + 0.5 * (f(ps, rR, pR, cR) - f(ps, rL, pL, cL))
    out = np.zeros_like(xi)
    for n, s in enumerate(xi):
        if s < us:      # left of contact
            if ps > pL:
                sL = uL - cL * math.sqrt((gam + 1) / (2 * gam) * ps / pL + (gam - 1) / (2 * gam))
                out[n] = rL * ((ps / pL + (gam - 1) / (gam + 1)) / ((gam - 1) / (gam + 1) * ps / pL + 1)) if s > sL else rL
            else:
                csL = cL * (ps / pL) ** ((gam - 1) / (2 * gam))
                sH, sT = uL - cL, us - csL
                if s < sH:
                    out[n] = rL
                elif s > sT:
                    out[n] = rL * (ps / pL) ** (1 / gam)
                else:
                    out[n] = rL * (2 / (gam + 1) + (gam - 1) / ((gam + 1) * cL) * (uL - s)) ** (2 / (gam - 1))
        else:
            if ps > pR:
                sR = uR + cR * math.sqrt((gam + 1) / (2 * gam) * ps / pR + (gam - 1) / (2 * gam))
                out[n] = rR * ((ps / pR + (gam - 1) / (gam + 1)) / ((gam - 1) / (gam + 1) * ps / pR + 1)) if s < sR else rR
            else:
                csR = cR * (ps / pR) ** ((gam - 1) / (2 * gam))
                sH, sT = uR + cR, us + csR
                if s > sH:
                    out[n] = rR
                elif s < sT:
                    out[n] = rR * (ps / pR) ** (1 / gam)
                else:
                    out[n] = rR * (2 / (gam + 1) - (gam - 1) / ((gam + 1) * cR) * (uR - s)) ** (2 / (gam - 1))
    return out


N = 200; dx = 1.0 / N
x = (np.arange(N) + 0.5) * dx
shape = (N, 4, 4)
rho0 = np.where(x < 0.5, 1.0, 0.125)[:, None, None] * np.ones(shape)
P0 = np.where(x < 0.5, 1.0, 0.1)[:, None, None] * np.ones(shape)
U = L.cons(rho0, np.zeros((3,) + shape), P0, np.zeros(shape))
t, tend = 0.0, 0.2
zero = [np.zeros(shape)] * 3
save_fix = L._fix
L._fix = lambda U, rf: None                       # the cluster pressure floor is in cluster units; off for the unit test
while t < tend - 1e-12:
    dt = min(L.hydro_dt(U, dx, 0.3), tend - t)
    U = L.hydro_step(U, zero, dt, dx, 1e-8)
    t += dt
L._fix = save_fix
num = U[0][:, 1, 1]
ex = exact_riemann(1.0, 0.0, 1.0, 0.125, 0.0, 0.1, L.GAMMA, (x - 0.5) / tend)
l1 = float(np.mean(np.abs(num - ex)) / np.mean(ex))
check("C2 Sod shock tube (gamma 5/3, 200 cells, t = 0.2): L1 density error <= 3% of the exact solution", l1 <= 0.03, f"L1/mean = {l1:.4f}")

# ---------------------------------------------------------------- C3 round phantom routine vs analytic Hernquist phantom
rng = np.random.default_rng(3)
Mb, ab = 1e14, 300.0
n = 4_000_000
u = rng.random(n)
rp = ab * np.sqrt(u) / (1 - np.sqrt(u))           # Hernquist inverse CDF
hb = np.histogram(rp, S.RB)[0] * (Mb / n)
Mcum = np.concatenate([[0.0], np.cumsum(hb)])
_, _ = L.phantom_profile_from_mass(S.RB, Mcum, L.A0["can"], 1e9)
Mph_routine = L.phantom_mass(S.RB, Mcum, L.A0["can"])
Mb_an = Mb * S.RB ** 2 / (S.RB + ab) ** 2
Mph_an = (L.nu_mono(L.G * Mb_an / (np.maximum(S.RB, 1e-6) ** 2 * L.A0["can"])) - 1) * Mb_an
selr = (S.RB >= 0.1 * ab) & (S.RB <= 2 * ab)
e3 = np.abs(Mph_routine[selr] / Mph_an[selr] - 1)
check("C3 round phantom from binned Hernquist baryons (4e6 particles) vs CFG541 E7 analytic, 0.1-2 a, <= 1%", e3.max() <= 0.01,
      f"max |rel err| = {e3.max():.4f}")
# the painted 3-D field holds the profile's mass and shape
prog = L.Progenitor(1.5e14, "can", "L")
sim = S.Sim(dict(foot="can", case="L", alpha=1.0, mode="isolated"))
fld = sim.phantom_field()
rg = sim.g.radius_from(sim.xb[0])
fan = np.interp(rg, sim.progs[0].r, sim.progs[0].rho_ph) * (rg < sim.progs[0].rt)
fan *= sim.progs[0].Mph_tot / (fan.sum() * sim.g.dV)
Mgrid = np.array([fld[rg <= R].sum() * sim.g.dV for R in (300.0, 600.0, 1000.0)])
Man = np.array([fan[rg <= R].sum() * sim.g.dV for R in (300.0, 600.0, 1000.0)])
e3b = np.abs(Mgrid / Man - 1)
RES["C3b_reported"] = dict(note="reported, not a frozen control: painted phantom of the main's SAMPLED baryons vs the painted analytic "
                                "IC phantom, same grid discretisation, M(<300, 600, 1000 kpc)", rel_err=np.round(e3b, 4).tolist())
P(f"  [reported] C3b painted phantom from sampled baryons vs painted analytic IC phantom, M(<300/600/1000): rel err {np.round(e3b, 4).tolist()}")

# ---------------------------------------------------------------- C5 conservation in the settle step
c = sim.is_c
m0 = sim.m[c].sum(); p0 = (sim.m[c, None] * sim.v[c]).sum(0)
vscale = np.sqrt((sim.m[c, None] * sim.v[c] ** 2).sum(0)).sum() * math.sqrt(sim.m[c].sum())
rho_tot = sim.U[0] + sim.g.deposit(sim.x, sim.m)
sim.settle(0.004, rho_tot)
m1 = sim.m[c].sum(); p1 = (sim.m[c, None] * sim.v[c]).sum(0)
dp = float(np.linalg.norm(p1 - p0) / vscale)
check("C5 settle step: settled cold mass unchanged exactly and total cold momentum conserved to <= 1e-3 of its |p| scale",
      (m1 == m0) and dp <= 1e-3, f"dM = {m1 - m0:.3e}, |dp|/scale = {dp:.2e}")

RES["all_pass"] = all(v["ok"] for k, v in RES.items() if isinstance(v, dict) and "ok" in v)
P(f"\nCONTROLS C1-C3, C5: {'ALL PASS' if RES['all_pass'] else 'SOME FAIL'}")
open(os.path.join(HERE, "cfg597_controls.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "cfg597_controls_results.json"), "w"), indent=1)
sys.exit(0 if RES["all_pass"] else 1)
