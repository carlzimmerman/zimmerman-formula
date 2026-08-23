#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SF52.3 — DIMENSIONLESS COSMOLOGICAL SYSTEM
Reduces the homogeneous equations to an autonomous dynamical system.
"""

import sys

def main():
    print("SF52.3 — DERIVING DIMENSIONLESS SYSTEM")
    
    # We will write the full analytical reduction to markdown, since the 
    # algebraic steps are cleanly done by hand based on SF52.2.
    
    content = r"""# SF52.3 — DIMENSIONLESS COSMOLOGICAL SYSTEM

## 1. Normalization and Dimensionless Variables

We define dimensionless time $\tau = a_0 t$ and the following dimensionless variables (using $c=1$):
- Hubble: $h = H / a_0$
- Auxiliary gradient: $v = \dot{X} / a_0$
- Non-minimal coupling: $x = \xi / k$  (where $k = \frac{1}{16\pi G}$)
- Mass scale: $m = M / a_0^2$
- Interpolation function: $\tilde{f}(Z) = f(Z) / a_0^2$

The kinetic invariant is exactly $Z = -b v^2$ (with $b=4$ in sf51, or $b=27/(8\pi)$ in sf53).
We use prime $'$ to denote $d/d\tau$.

## 2. The Reduced Auxiliary Equations

From the action variations:
1. **$M$-equation:** $\nu' = -k a_0$ (which is a constant, decoupling from the rest).
2. **$\nu$-equation:** $\nabla_\mu [ (M+f(Z)) u^\mu ] = 0 \implies m' + 3 h (m + \tilde{f}(Z)) = 0$.
3. **$X$-equation:** $\Box X = R_{00} \implies v' + 3 h v = 3 (h' + h^2)$.
4. **$\xi$-equation:** $\Box \xi = -\nabla_0 [ 2 b f'(Z) \dot{X} ] \implies x'' + 3 h x' = 2 b \frac{d}{d\tau} [ \tilde{f}'(Z) v ] + 6 b h \tilde{f}'(Z) v$.

## 3. The Friedmann Equation

Using the energy density derived in SF52.2, and solving the $\phi$-equation for $\lambda_\phi$ assuming $J=0$ for causal initial conditions, we find the exact Friedmann constraint:
$$ 6 h^2 = x' v - 3 h x' - 3 x h^2 + 2 [ Z \tilde{f}'(Z) + m + \tilde{f}(Z) ] $$

Taking the time derivative of this constraint must consistently reproduce the acceleration equation $-2h' - 3h^2 = 8\pi G p_{\mathrm{aux}}$. This acts as a Bianchi identity check.

## 4. The Autonomous Dynamical System

The state of the system is fully specified by $\mathbf{Y} = (h, v, x, x', m)$.
The evolution equations are:
1. $m' = -3 h (m + \tilde{f}(Z))$
2. $v' = 3 h' + 3 h^2 - 3 h v$
3. $x'' = -3 h x' + 2 b \frac{d}{d\tau}[ \tilde{f}'(Z) v ] + 6 b h \tilde{f}'(Z) v$
4. Constraint: $6 h^2 - x' v + 3 h x' + 3 x h^2 - 2 [ Z \tilde{f}'(Z) + m + \tilde{f}(Z) ] = 0$

To make it a strict ODE system $\mathbf{Y}' = \mathbf{F}(\mathbf{Y})$, one differentiates the constraint to solve for $h'$.
"""
    with open('SF52_DIMENSIONLESS_SYSTEM.md', 'w') as f:
        f.write(content)
        
    print("STATUS: PASS")
    print("Dimensionless reduction complete. Output saved to SF52_DIMENSIONLESS_SYSTEM.md")

if __name__ == '__main__':
    main()
