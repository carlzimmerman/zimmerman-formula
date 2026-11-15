#!/usr/bin/env python3
"""SQM1 K3 diagnostic (after the as-frozen run stopped at K3; prints no graded number).
Is the 1e-3 gap between the projected Prugniel-Simien body and the analytic Sersic 2D fraction quadrature
or the deprojection approximation?  Run: python3 -I -B sqm1_k3_diagnostic.py <dir holding sqm1.py>"""
import sys, os
sys.path.insert(0, os.path.abspath(sys.argv[1]))
import sqm1 as s
M = 1e11 * s.MSUN
for n in (4.0, 6.0):
    for Re_k, R_k in ((4.5, 7.14), (3.0, 3.0), (6.0, 12.0)):
        for nodes in (400, 3000):
            for rmax in (1e6, 1e9):
                U = s.Units(False, nodes); Re = Re_k * s.KPC; R = R_k * s.KPC
                m = s.M2D_from_gfun(R, lambda r: U.G * M * s.M3D_frac(r, Re, n) / r ** 2, U, rmax * s.KPC) / M
                f = float(s.M2D_frac(R, Re, n))
                print("n %.0f  R/Re %.3f  nodes %4d  rmax %.0e kpc : projected PS %.8f  analytic Sersic %.8f  rel %+.2e"
                      % (n, R_k / Re_k, nodes, rmax, m, f, m / f - 1))
