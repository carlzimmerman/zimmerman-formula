import sympy as sp

def main():
    print("--- Path 3: Unified Entropic Action ---")
    print("Goal: Rigorously check if S_tot = S_area + S_volume yields the MOND relation g \propto 1/r")
    
    # Define symbols
    r, G, L0, gamma, M_bar = sp.symbols('r G L0 gamma M_bar', positive=True, real=True)
    a = sp.symbols('a', real=True)
    
    # Constants
    # T = a / (2 * pi)
    T = a / (2 * sp.pi)
    
    # Area and Volume of spherical screen
    A = 4 * sp.pi * r**2
    V = (4 * sp.pi / 3) * r**3
    
    # Generalized entropy
    # S_area = A / 4G (in c=1, hbar=1 units)
    S_area = A / (4 * G)
    S_vol = gamma * V / (G * L0)
    S_tot = S_area + S_vol
    
    print("\n1. Thermodynamic Equation of State (Jacobson-like)")
    print("Equating enclosed mass M_bar to the integrated heat: M_bar = \int T dS")
    print("Using a localized screen: M_bar = T * (dS_tot / dr)")
    
    dS_dr = sp.diff(S_tot, r)
    print(f"dS_tot/dr = {dS_dr}")
    
    # Solve for acceleration 'a'
    eq = sp.Eq(M_bar, T * dS_dr)
    a_sol = sp.solve(eq, a)[0]
    
    print(f"\nDerived acceleration law 'a':")
    print(sp.simplify(a_sol))
    
    print("\n2. Deep-MOND Limit check")
    print("In deep-MOND, we need a \propto 1/r. Let's check the asymptotic limit r -> \infty.")
    
    # Limit of 'a' as r -> infinity
    a_large_r = sp.series(a_sol, r, sp.oo, 2).removeO()
    print(f"Limit of 'a' at large r: {a_large_r}")
    
    print("\nRESULT:")
    print("The derived acceleration at large distances goes as 1/r^2 (if gamma != 0).")
    print("It scales as G * L0 * M_bar / (gamma * r^2), which is just a rescaled Newtonian gravity.")
    print("This simple thermodynamic extension (adding S_vol) FAILS to produce the MOND 1/r law.")
    print("To get MOND, one must adopt Verlinde's complex elastic displacement strain field tensor,")
    print("which is highly non-local and controversial, or ad-hoc covariant fields (AeST).")

if __name__ == "__main__":
    main()
