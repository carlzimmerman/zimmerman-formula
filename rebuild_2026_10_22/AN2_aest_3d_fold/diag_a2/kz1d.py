#!/usr/bin/env python3
"""AN2 diagnostic, 1D reduction of check KZ: same background, wave, KDK and time step as an2.py, mesh force variants. No science row. kappa = 1/2 FITTED."""
import sys, json, os
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS"): os.environ[v]="1"
import numpy as np
from scipy.integrate import quad
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from an2 import Bg, G, RX0, RB0, TU
RM = RX0 + RB0
def dep(x, N, dx, L, kind):
    u = np.mod(x, L) / dx
    if kind == "cic":
        i = np.floor(u).astype(int); w = u - i
        return (np.bincount(i % N, 1 - w, N) + np.bincount((i + 1) % N, w, N)) * N / len(x) - 1
    i = np.rint(u).astype(int); d = u - i
    return (np.bincount((i - 1) % N, .5 * (.5 - d)**2, N) + np.bincount(i % N, .75 - d**2, N) + np.bincount((i + 1) % N, .5 * (.5 + d)**2, N)) * N / len(x) - 1
def itp(x, f, N, dx, L, kind):
    u = np.mod(x, L) / dx
    if kind == "cic":
        i = np.floor(u).astype(int); w = u - i
        return (1 - w) * f[i % N] + w * f[(i + 1) % N]
    i = np.rint(u).astype(int); d = u - i
    return .5 * (.5 - d)**2 * f[(i - 1) % N] + (.75 - d**2) * f[i % N] + .5 * (.5 + d)**2 * f[(i + 1) % N]
def force(x, N, dx, L, a, kind, grad):
    d = dep(x, N, dx, L, kind); dk = np.fft.rfft(d); k = 2 * np.pi * np.fft.rfftfreq(N, dx)
    ik2 = np.zeros_like(k); ik2[1:] = 1 / k[1:]**2
    phi = -4 * np.pi * G * RM / a * dk * ik2
    if grad == "spec":
        g = 1j * k.copy(); g[-1] = 0; F = -np.fft.irfft(g * phi, N)
    else:
        ph = np.fft.irfft(phi, N)
        if grad == "fd2": F = -(np.roll(ph, -1) - np.roll(ph, 1)) / (2 * dx)
        if grad == "fd4": F = -(8 * (np.roll(ph, -1) - np.roll(ph, 1)) - (np.roll(ph, -2) - np.roll(ph, 2))) / (12 * dx)
    return itp(x, F, N, dx, L, kind)
def run(N, eta, kind, grad, rev=False):
    bg = Bg(); ai = 1 / 21.; L = 145000.; k = 2 * np.pi / L; dx = L / N; q = (np.arange(N) + .5) * dx
    Ak = bg.D(ai) / bg.D(.5); s = -Ak / k * np.sin(k * q)
    h = 1e-5 * ai; f = (np.log(bg.D(ai + h)) - np.log(bg.D(ai - h))) / (np.log(ai + h) - np.log(ai - h))
    p = ai**2 * bg.H(ai) * f * s; t = bg.t(ai); F = force(q + s, N, dx, L, ai, kind, grad); dp = None; n = 0
    while True:
        a = bg.a(t); vm = np.abs(p).max() / a**2; Fm = np.abs(F).max() / a**2
        dt = min(eta * dx / (vm + 1e-30), eta * np.sqrt(dx / (Fm + 1e-30)), .2 * eta / bg.H(a))
        p += .5 * dt * F; p0 = p
        s = s + quad(lambda u: bg.a(u)**-2, t, t + dt, epsabs=0, epsrel=1e-10)[0] * p; tp = t; t += dt
        F = force(q + s, N, dx, L, bg.a(t), kind, grad); p = p + .5 * dt * F; n += 1
        de = (np.roll(s, -1) - s) / dx + 1; m = de.min()
        if m <= 0: return (tp + (t - tp) * dp / (dp - m)) * TU, n
        dp = m
if __name__ == "__main__":
    tc = Bg().t(.5) * TU
    for kind, grad in (("cic","spec"),("cic","fd2"),("cic","fd4"),("tsc","spec"),("tsc","fd4"),("tsc","fd2")):
        for N in (64, 96, 128, 192, 256, 512, 1024):
            t, n = run(N, .05, kind, grad); print(kind, grad, N, "%+.3f%%" % (100 * (t - tc) / tc), n, flush=True)
