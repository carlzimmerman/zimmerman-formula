#!/usr/bin/env python3
"""
agentS auxiliary -- COEFFICIENT-LEVEL check of the edge power law (raw numbers before comparisons).
Watson lemma: if w(omega) ~ h0 sqrt(omega) at the support floor omega=0 (the banked Wigner edge
s_E=1/2 seen by an EDGE-placed vacuum), then
    G(t) = int w(omega) e^{-i omega t} domega / int w  ->  h0 * Gamma(3/2) * e^{-3 i pi/4} * t^{-3/2} / norm.
We measure h0 directly from the banked spectral weight (fit w vs sqrt(omega) at small omega), then
compare the PREDICTED complex amplitude against the computed G(t) at late t: modulus AND phase.
A match pins the edge falloff at coefficient level: it is the soft-edge endpoint asymptotic, nothing else.
"""
import numpy as np
from math import gamma

def qpoch(a, q, N=500):
    a = np.asarray(a, dtype=complex)
    out = np.ones(a.shape, dtype=complex); qk = 1.0
    for _ in range(N):
        out *= (1 - a * qk); qk *= q
    return out

def mu_qg(th, q):
    qq = qpoch(np.array([q]), q).real[0]
    e2 = np.exp(2j * np.asarray(th, dtype=float))
    return qq * (qpoch(e2, q) * qpoch(np.conj(e2), q)).real / (2 * np.pi)

def G_amp(th1, th2, D, q):
    num = qpoch(np.array([q ** (2 * D)]), q).real[0]
    th1 = np.asarray(th1, dtype=float); th2 = np.asarray(th2, dtype=float)
    den = np.ones(np.broadcast(th1, th2).shape, dtype=complex)
    for s1 in (1, -1):
        for s2 in (1, -1):
            den *= qpoch(q ** D * np.exp(1j * (s1 * th1 + s2 * th2)), q)
    return num / den

print("EDGE placement (theta_v = pi - 1e-3): Watson-lemma coefficient check, G(t) ~ A t^{-3/2}", flush=True)
print(f"{'q':>5}{'Delta':>7} | {'h0 (w ~ h0 sqrt(om))':>21} | {'|A|_pred':>10} | "
      f"{'t':>7}{'|G| t^1.5 meas':>15}{'phase meas':>11}{'phase pred':>11}", flush=True)
for q in (0.5, 0.7, 0.9):
    for D in (0.1, 0.5, 1.0):
        thv = np.pi - 1e-3
        th = np.linspace(1e-7, np.pi - 1e-7, 600001)
        w = mu_qg(th, q) * np.abs(G_amp(th, thv, D, q)) ** 2
        om = np.cos(th) - np.cos(thv)
        norm = np.trapz(w, th)
        # density in omega: rho(om) = w(theta)/|dom/dth|; fit rho ~ h0 sqrt(om) at small positive om
        rho = w / np.abs(np.sin(th))
        m = (om > 1e-6) & (om < 1e-4)
        h0 = np.mean(rho[m] / np.sqrt(om[m]))
        # measured G at late t (exact quadrature in theta)
        A_pred = h0 * gamma(1.5) / norm           # |A|; phase pred = -3pi/4
        for tval in (8e3, 2e4):
            ph = np.exp(-1j * om * tval)
            G = np.trapz(w * ph, th) / norm
            print(f"{q:>5.2f}{D:>7.2f} | {h0:>21.6e} | {A_pred:>10.4e} | "
                  f"{tval:>7.0f}{np.abs(G)*tval**1.5:>15.4e}{np.angle(G):>11.4f}{-3*np.pi/4:>11.4f}", flush=True)
print("\nREAD: |G| t^{3/2} -> |A|_pred and arg(G) -> -3pi/4 (mod the slow drift from the next half-integer",
      flush=True)
print("endpoint term ~ t^{-2}): the edge late-time behavior is the SOFT-EDGE ENDPOINT ASYMPTOTIC at", flush=True)
print("coefficient level -- no room for a hidden exponential ladder underneath.", flush=True)
