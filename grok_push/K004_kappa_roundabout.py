#!/usr/bin/env python3
"""K004 — the roundabout that looks like a derivation of kappa = 1/2, computed and emptied.

THE QUESTION. Every gravitational half in this corpus is already spent (surface
gravity builds cH, Komar -2 builds the 8 pi, the trace-reversal half builds the
Newtonian 4 pi). The one composition nobody wrote down is: take the horizon-ball
half, which is an exact identity, and move it off c H_Lambda onto the local scale
s = c sqrt(G rho_Lambda). Algebraically that lands on s/2. Is that a derivation?

THE RESULT. No. The move cancels the horizon that justified the half, and the
conclusion is the posit a0 = s/2 with no gravitational input left. The three
compositions that do NOT cancel the horizon miss 1/2 by exact squares
(2 pi/3, 8 pi/3, 32 pi/3), none of which is 1/4. Separately, the L236 loophole
(a tau-dependent cuscuton coefficient substituting for the potential) does not
source expansion: the cuscuton energy density is the potential, identically, for
any coefficient. Scope of that last clause: a pure cuscuton. The repo's extended
clock is G001's domain and is not re-opened here.

Nothing in this lane derives kappa. It certifies why the roundabout is empty.
"""
import json
import sympy as sp

RES, NP, NF = [], 0, 0

def check(name, measured, ok, reading=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading:
        print(f"         reading : {reading}")
    RES.append({"name": name, "measured": str(measured), "pass": ok, "reading": reading})
    if ok:
        NP += 1
    else:
        NF += 1

print(__doc__)
pi = sp.pi
c, H, s, G, rho = sp.symbols("c H s G rho", positive=True)

# ---------------------------------------------------------------- ball half
print("\nPART A — the horizon-ball half is an identity, and it multiplies c H")
# rho_Lambda = 3 H^2 / (8 pi G), R = c/H
# g = (4 pi / 3) G rho R
g = sp.simplify((sp.Rational(4, 3) * pi * G) * (3 * H**2 / (8 * pi * G)) * (c / H))
check(
    "A1 [horizon-ball half] Newtonian acceleration at R = c/H sourced by rho_Lambda "
    "equals (1/2) c H, because (4 pi/3)*(3/(8 pi)) = 1/2",
    f"g_ball = {g}",
    sp.simplify(g - sp.Rational(1, 2) * c * H) == 0,
    "this 1/2 multiplies c H, the GLOBAL expansion rate. It is not yet kappa",
)

# ---------------------------------------------------------------- three compositions that keep H
kernel = sp.sqrt(8 * pi / 3)          # c H / s
# kappa := a0 / s, with s the local scale. c H = kernel * s.
# composition 1: a0 = g_ball = c H / 2  => kappa = kernel / 2
k1 = sp.simplify(kernel / 2)
# composition 2: a0-line inversion a0 = 2 k with k = g_ball => a0 = c H => kappa = kernel
k2 = sp.simplify(kernel)
# composition 3: Deser-Levin floor k = c H, a0 = 2 k => kappa = 2 kernel (Milgrom)
k3 = sp.simplify(2 * kernel)
target = sp.Rational(1, 2)

def sq_away(k):
    return sp.simplify(k**2 - target**2)

check(
    "A2 [three compositions that keep the horizon all miss 1/2] squared distance "
    "from kappa^2 = 1/4, exact",
    f"ball: kappa^2 = {sp.simplify(k1**2)} = 2 pi/3; "
    f"a0=2 g_ball: kappa^2 = {sp.simplify(k2**2)} = 8 pi/3; "
    f"Milgrom: kappa^2 = {sp.simplify(k3**2)} = 32 pi/3; target 1/4",
    sq_away(k1) != 0 and sq_away(k2) != 0 and sq_away(k3) != 0
    and sp.simplify(k1**2 - 2 * pi / 3) == 0
    and sp.simplify(k2**2 - 8 * pi / 3) == 0
    and sp.simplify(k3**2 - 32 * pi / 3) == 0,
    "none of the three is 1/4. The horizon-keeping roundabouts are dead exactly, not numerically",
)

# ---------------------------------------------------------------- the relocation
print("\nPART B — moving the half onto the local scale cancels the horizon")
reloc = sp.simplify((sp.Rational(1, 2) * c * H) * (s / (c * H)))
check(
    "B1 [the relocation identity] g_ball * (s / (c H)) equals s/2 exactly, and H cancels",
    f"(1/2 c H) * (s / (c H)) = {reloc}",
    reloc == s / 2 and H not in reloc.free_symbols and c not in reloc.free_symbols,
    "the horizon radius and the Hubble rate, which were the only reasons the 1/2 existed, "
    "cancel identically. What remains is a0 = s/2, which is the posit, not an output",
)
check(
    "B2 [anti-tautology: the conclusion is the definition of kappa = 1/2] s/2 = (1/2) s, "
    "no gravitational symbol survives",
    f"free symbols of the result: {reloc.free_symbols}",
    reloc.free_symbols == {s} and sp.simplify(reloc - sp.Rational(1, 2) * s) == 0,
    "a derivation must output the half from premises that do not already contain it. "
    "This composition outputs the half only by cancelling every premise that produced a half. "
    "It is empty",
)

# ---------------------------------------------------------------- pure cuscuton
print("\nPART C — L236's running-coefficient loophole does not source expansion")
U, V, sX = sp.symbols("U V sX", real=True)
# sX = sqrt(2X) ≠ 0; P = U*sX - V; P_X = U/sX; rho = 2X P_X - P = sX^2 * (U/sX) - P
rho = sp.simplify((sX**2) * (U / sX) - (U * sX - V))
check(
    "C1 [cuscuton energy density is the potential, for any coefficient] "
    "rho = 2X P_X - P with P = U sqrt(2X) - V collapses to V; U cancels",
    f"rho = {rho}",
    sp.simplify(rho - V) == 0 and U not in sp.simplify(rho).free_symbols,
    "a tau-dependent U changes the field equation (the extra term L236 named) and does not "
    "change the energy density. V = 0 implies rho = 0 implies H = 0 by Friedmann, if this "
    "is the only source. The running cannot substitute for the potential. "
    "SCOPE: pure cuscuton. The extended clock (rho = U/m_rel) is G001, not this clause",
)
# joint: H = 0 from Friedmann plus the field equation U' + 3 H U = -V' at V' = 0
Up, Hv = sp.symbols("U_prime H")
field = Up + 3 * Hv * U
check(
    "C2 [and the field equation then forces the coefficient not to run] "
    "at H = 0 and V' = 0, U' + 3 H U = 0 implies U' = 0",
    f"U' + 3 H U at H = 0 is {sp.simplify(field.subs(Hv, 0))}",
    sp.simplify(field.subs(Hv, 0) - Up) == 0,
    "the only joint solution is a constant coefficient and a vanishing expansion. "
    "No running-U branch expands",
)

# ---------------------------------------------------------------- what survives
print("\nPART D — the law that does survive, labelled")
n, g, gbar, ss = sp.symbols("n g g_bar s", positive=True)
# deep matching: n * (g/s) * g = g_bar  => g^2 = s g_bar / n  => a0 = s/n => kappa = 1/n
deep = n * (g / ss) * g - gbar
a0 = sp.simplify(ss / n)
kappa = sp.simplify(a0 / ss)
check(
    "D1 [surviving law, not a derivation of the integer] deep matching "
    "n (g/s) g = g_bar forces kappa = 1/n, with n not determined by parts A-C",
    f"kappa = {kappa}; n = 1 gives {sp.simplify(kappa.subs(n, 1))}; "
    f"n = 2 gives {sp.simplify(kappa.subs(n, 2))}",
    kappa == 1 / n and sp.simplify(kappa.subs(n, 2) - sp.Rational(1, 2)) == 0,
    "kappa = 1/2 is the case n = 2. Parts A-C do not select n. "
    "n = 2 remains the SPARC measurement (L232), not an output of this lane",
)

print()
print(f"K004 COMPLETE: {NP}/{NP + NF} checks PASS.")
out = {
    "pass": NP,
    "fail": NF,
    "checks": RES,
    "verdict": "roundabout empty; kappa = 1/n with n not derived here",
}
json.dump(out, open("grok_push/K004_results.json", "w"), indent=1)
raise SystemExit(0 if NF == 0 else 1)
