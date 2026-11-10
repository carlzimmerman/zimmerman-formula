"""R541A GA5: signs of the densities and of the baryon-clock inertia matrix (from ga2's quadratic Lagrangian).
Kinetic part: (1-alpha) rho v_b^2/2 + E (v_b - v_K)^2/2 + rho_K v_K^2/2, E = alpha rho (Z_can: rho_K = E + sigma).
Output: ga5_signs.out (same folder)."""
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
out = open(os.path.join(HERE, "ga5_signs.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")
P("# R541A GA5: densities and inertia matrix (units rho_b = 1)")
for foot, R in [("canonical", 5.410), ("alt", 5.412)]:
    A = R/(1 + R)
    P(f"## footing {foot}")
    for lab, al, sig in [("as needed (Z_can)", A, 0.0), ("KA alpha=0, sigma=R", 0.0, R), ("MU alpha=1.2", 1.2, 0.0)]:
        E = al; rK = E + sig
        M = np.array([[(1 - al) + E, -E], [-E, rK + E]])
        ev = np.linalg.eigvalsh(M)
        P(f"  {lab}: baryon active density {(1 - al):+.4f}, clock density {rK:+.4f}, inertia eigenvalues {ev[0]:+.4f} {ev[1]:+.4f}"
          f" -> {'PASS' if (1 - al) >= 0 and rK >= 0 and ev.min() > 0 else 'FAIL'}")
P("(i-b): clock kinetic coefficient M0 - 2 alpha rho_b flips sign (ghost) before the a listed in ga1_background.out.")
out.close()
