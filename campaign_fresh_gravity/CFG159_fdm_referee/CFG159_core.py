#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG159_core -- own Schroedinger-Poisson ground-state solver for the CFG159 referee lane (independent of CFG119's code).

Units: hbar = m = G = M_b = 1, so length unit a_B = hbar^2/(G M_b m^2) and energy unit G^2 M_b^2 m^3/hbar^2.
Method: radial equation for u = r psi on a log grid; log-derivative (Riccati) propagation w = u'/u with the potential piecewise
constant on each step (exact hyperbolic / trigonometric propagator per step, evaluated in log space so tails of ln u ~ -1e11 are
exponents, never floats), outward from r0 and inward from r_far, matched at the classical turning point; E from a bracketed root of the
bounded mismatch (w_out - w_in)/(|w_out|+|w_in|); a node (sign change of u) means E is above the ground state.  The sweeps are
in C (compiled at first use with the system cc); everything else is numpy/scipy.
"""
import os, sys, math, ctypes, subprocess, json
import numpy as np
from scipy.optimize import brentq
from scipy.special import gammainc

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

C_SRC = r"""
#include <math.h>
static int step_out(double q, double D, double *w, double *dl){
  double W=*w;
  if(q>1e-300){
    double k=sqrt(q), a=k*D, F;
    if(a<5.0){ F=cosh(a)+(W/k)*sinh(a); if(F<=0) return 1; *dl=log(F); }
    else { double e=exp(-2*a); double Fp=0.5*(1+W/k)+0.5*(1-W/k)*e; if(Fp<=0) return 1; F=Fp; *dl=a+log(Fp); }
    double tau=tanh(a); double den=k+W*tau; if(den==0) return 1;
    *w=k*(W+k*tau)/den; return 0;
  } else if(q<-1e-300){
    double kk=sqrt(-q), th=kk*D; double F=cos(th)+(W/kk)*sin(th); if(F<=0) return 1;
    *dl=log(F); *w=(-kk*sin(th)+W*cos(th))/F; return 0;
  } else { double F=1+W*D; if(F<=0) return 1; *dl=log(F); *w=W/F; return 0; }
}
static int step_in(double q, double D, double *w, double *dl){
  double W=*w;
  if(q>1e-300){
    double k=sqrt(q), a=k*D, F;
    if(a<5.0){ F=cosh(a)-(W/k)*sinh(a); if(F<=0) return 1; *dl=log(F); }
    else { double e=exp(-2*a); double Fp=0.5*(1-W/k)+0.5*(1+W/k)*e; if(Fp<=0) return 1; F=Fp; *dl=a+log(Fp); }
    double tau=tanh(a); double den=k-W*tau; if(den==0) return 1;
    *w=k*(W-k*tau)/den; return 0;
  } else if(q<-1e-300){
    double kk=sqrt(-q), th=kk*D; double F=cos(th)-(W/kk)*sin(th); if(F<=0) return 1;
    *dl=log(F); *w=(kk*sin(th)+W*cos(th))/F; return 0;
  } else { double F=1-W*D; if(F<=0) return 1; *dl=log(F); *w=W/F; return 0; }
}
/* nodes r[0..N], mid potentials V[0..N-1]; match node m.  returns bit0: node outward, bit1: node inward, bit2: bad start */
int sweep(int N, const double *r, const double *V, double E, int m, double w0, double *L, double *W, double *wout, double *win){
  int flags=0; double w=w0, l=0, dl; L[0]=0; W[0]=w;
  for(int i=0;i<m;i++){
    double D=r[i+1]-r[i], q=2*(V[i]-E);
    if(step_out(q,D,&w,&dl)){ flags|=1; *wout=w; *win=0; return flags; }
    l+=dl; L[i+1]=l; W[i+1]=w;
  }
  *wout=w; double Lo=l;
  double q=2*(V[N-1]-E); if(q<=0){ flags|=4; *win=0; return flags; }
  w=-sqrt(q); l=0; L[N]=0; W[N]=w;
  for(int i=N-1;i>=m;i--){
    double D=r[i+1]-r[i]; q=2*(V[i]-E);
    if(step_in(q,D,&w,&dl)){ flags|=2; *win=w; return flags; }
    l+=dl; L[i]=l; W[i]=w;
  }
  *win=w; double sh=Lo-L[m];
  for(int i=m;i<=N;i++) L[i]+=sh;
  return flags;
}
"""

_lib = None
def lib():
    global _lib
    if _lib is None:
        bd = os.path.join(HERE, "_cfg159_build"); os.makedirs(bd, exist_ok=True)
        src = os.path.join(bd, "sweep.c"); so = os.path.join(bd, "libsweep.so")
        need = (not os.path.exists(so)) or (not os.path.exists(src)) or open(src).read() != C_SRC
        if need:
            with open(src, "w") as f: f.write(C_SRC)
            subprocess.check_call(["cc", "-O2", "-shared", "-fPIC", "-o", so, src, "-lm"])
        L = ctypes.CDLL(so)
        dp = ctypes.POINTER(ctypes.c_double)
        L.sweep.argtypes = [ctypes.c_int, dp, dp, ctypes.c_double, ctypes.c_int, ctypes.c_double, dp, dp, dp, dp]
        L.sweep.restype = ctypes.c_int
        _lib = L
    return _lib

def _p(a): return a.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

def fexp_sphere(x):
    """1 - e^-x (1 + x/2): the exp-sphere potential factor, Phi = -(M/r) f(r/h)."""
    x = np.asarray(x, float)
    return np.where(x < 1e-4, x/2 - x**3/12 + x**4/24, 1.0 - np.exp(-x)*(1.0 + x/2))

class Grid:
    def __init__(self, r0, rfar, dt):
        self.dt = dt; self.N = int(math.ceil(math.log(rfar/r0)/dt))
        t = math.log(r0) + dt*np.arange(self.N+1)
        self.t = t; self.r = np.exp(t); self.rm = np.exp(t[:-1] + dt/2)
        self.Lbuf = np.empty(self.N+1); self.Wbuf = np.empty(self.N+1)

def make_vb(grid, hh, mode=""):
    """baryon potential at the mid-points and the centre charge z0 (w0 = 1/r0 - z0) and the attractive charge for the E bound."""
    if hh is None:
        vb = -1.0/grid.rm; z0 = 1.0
    else:
        vb = -fexp_sphere(grid.rm/hh)/grid.rm; z0 = 0.0
    zlo = 1.0
    if mode == "C":            # MUTATE C: baryons removed from the Schroedinger potential
        vb = np.zeros_like(vb); z0 = 0.0; zlo = 0.0
    elif mode == "D":          # MUTATE D: baryon potential sign-flipped (repulsive)
        vb = -vb; z0 = -z0; zlo = 0.0
    return vb, z0, zlo

def shoot(grid, V, E, z0):
    """returns (flag, f, m, L, W); f>0 for E below the ground state, f<0 above (node counts as f=-1)."""
    N = grid.N
    m = int(np.searchsorted(V, E)); m = min(max(m, 3), N-3)
    wo = ctypes.c_double(); wi = ctypes.c_double()
    w0 = 1.0/grid.r[0] - z0
    fl = lib().sweep(N, _p(grid.r), _p(np.ascontiguousarray(V)), float(E), m, w0, _p(grid.Lbuf), _p(grid.Wbuf), ctypes.byref(wo), ctypes.byref(wi))
    if fl & 3: return fl, -1.0, m
    if fl & 4: return fl, -1.0, m
    f = (wo.value - wi.value)/(abs(wo.value) + abs(wi.value) + 1e-300)
    return fl, f, m

def find_E(grid, V, z0, zlo_tot, Eguess=None):
    fE = lambda E: shoot(grid, V, E, z0)[1]
    Emin = -0.5*zlo_tot**2 if zlo_tot > 0 else -1e30
    if Eguess is not None and Eguess < 0:
        d = 0.02
        Ea = Eguess*(1 + d)
        while fE(Ea) <= 0:
            d *= 2; Ea = Eguess*(1 + d)
            if d > 1e6: return None
        d = 0.02; Eb = Eguess*(1 - d)
        while fE(Eb) > 0:
            d *= 2
            if d >= 1: Eb = Eguess*1e-3*d if False else Eb*0.5
            else: Eb = Eguess*(1 - d)
            if abs(Eb) < 1e-16: return None
    else:
        if zlo_tot <= 0: return None
        Ea = Emin*(1 + 1e-6)
        if fE(Ea) <= 0: return None
        Eb = 0.5*Emin
        while fE(Eb) > 0:
            Eb *= 0.5
            if abs(Eb) < 1e-16: return None
    return brentq(fE, Ea, Eb, xtol=1e-16, rtol=1e-13, maxiter=200)

def moments(grid, L, W):
    """normalised radial pdf P (per r), cumulative mass Mhat at nodes and mids, tail integral Thi = int_r^inf P dr'/r' at nodes and mids,
    all with exact exponential interpolation between nodes (integrands are exponentials in t)."""
    dt = grid.dt; r = grid.r
    Lmax = L.max(); l = L - Lmax
    g = np.exp(2*l)*r                      # P_unnorm * r  (dr = r dt)
    gp = np.exp(2*l)                       # P_unnorm     (dt integrand of P/r * r)
    def cum(gv):
        g0 = gv[:-1]; g1 = gv[1:]
        pos = (g0 > 0) & (g1 > 0)
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            lam = np.where(pos, np.log(np.where(pos, g1, 1.0)/np.where(pos, g0, 1.0))/dt, 0.0)
            small = np.abs(lam*dt) < 1e-7
            lam_s = np.where(small, 1.0, lam)
            full = np.where(small, 0.5*(g0 + g1)*dt, g0*np.expm1(lam_s*dt)/lam_s)
            half = np.where(small, 0.5*(g0 + g0*np.exp(lam*dt/2))*dt/2, g0*np.expm1(lam_s*dt/2)/lam_s)
        full = np.where(pos, full, 0.0)
        half = np.where(pos, half, 0.0)
        c = np.concatenate([[0.0], np.cumsum(full)])
        return c, c[:-1] + half
    cM, cMm = cum(g)
    Nhat = cM[-1]
    Mnode = cM/Nhat; Mmid = cMm/Nhat
    cT, cTm = cum(gp)
    Tnode = (cT[-1] - cT)/Nhat
    Tmid = (cT[-1] - cTm)/Nhat
    return dict(Lmax=Lmax, lnNhat=math.log(Nhat), Mnode=Mnode, Mmid=Mmid, Tnode=Tnode, Tmid=Tmid, l=l)

def phi_from(mom, grid):
    return -(mom["Mmid"]/grid.rm + mom["Tmid"])

def solve_state(grid, vb, z0, zlo, s, phi, Eguess, srcfac=1.0, tol=1e-11, maxit=300, beta=0.7, anderson=5, verbose=False):
    """self-consistent ground state at soliton mass s (in M_b): V = vb + srcfac*s*phi, phi the shape of the potential of unit mass.
    Fixed-point map phi -> phi_new(phi) accelerated by Anderson mixing.  Returns None when no bound state exists."""
    hist_x = []; hist_r = []
    E = Eguess; ok = False; it = 0
    x = phi.copy(); last = None
    for it in range(1, maxit + 1):
        V = vb + srcfac*s*x
        E_new = find_E(grid, V, z0, zlo + s*srcfac, E)
        if E_new is None: return None
        fl, f, m = shoot(grid, V, E_new, z0)
        Es = E_new
        k = 0
        while (fl & 7) and k < 4:               # E_new sits on the flag boundary: nudge to the bound-state side
            Es = E_new*(1 + 10.0**(-13 + 2*k)); fl, f, m = shoot(grid, V, Es, z0); k += 1
        L = grid.Lbuf.copy(); W = grid.Wbuf.copy()
        mom = moments(grid, L, W)
        xn = phi_from(mom, grid)
        resid = xn - x
        dE = abs(E_new - E)/abs(E_new) if E is not None else 1.0
        E = E_new
        last = dict(E=E, L=L, W=W, mom=mom, m=m)
        if s*srcfac < 1e-13:
            x = xn; ok = True; break
        dV = s*srcfac*np.max(np.abs(resid))/abs(E)
        if verbose: print(it, E, dE, dV)
        if dE < tol and dV < 1e-9:
            x = xn; ok = True; break
        hist_x.append(x.copy()); hist_r.append(resid.copy())
        if len(hist_x) > anderson + 1: hist_x.pop(0); hist_r.pop(0)
        xnew = x + beta*resid*(0.5 if len(hist_x) < 2 else 1.0)
        if len(hist_x) >= 2:
            dR = np.array([hist_r[i+1] - hist_r[i] for i in range(len(hist_r)-1)]).T
            dX = np.array([hist_x[i+1] - hist_x[i] for i in range(len(hist_x)-1)]).T
            with np.errstate(all="ignore"):
                gam = np.linalg.lstsq(dR, resid, rcond=1e-10)[0]
            with np.errstate(all="ignore"):
                cand = x + beta*resid - (dX + beta*dR) @ gam
            if np.all(np.isfinite(cand)): xnew = cand
        x = xnew
    V = vb + srcfac*s*x
    return dict(E=last["E"], phi=x, L=last["L"], W=last["W"], mom=last["mom"], m=last["m"], it=it, ok=ok, V=V)
