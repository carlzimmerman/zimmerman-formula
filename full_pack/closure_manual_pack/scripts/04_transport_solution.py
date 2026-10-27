#!/usr/bin/env python3
import sympy as sp
s = sp.symbols('s', real=True)
M = sp.Function('M')(s)
F = sp.Function('F')(s)
expr = sp.diff(M + F, s)
print('Transport equation along a U-integral curve: d(M+F)/ds = 0')
print('Symbolic equation:', expr, '= 0')
print('General solution: M(s) + F(s) = C')
print('Therefore M(s) = -F(s) + C')
print('With boundary condition C=0 at the selected asymptotic endpoint: M=-F.')
