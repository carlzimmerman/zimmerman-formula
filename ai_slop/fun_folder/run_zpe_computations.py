import numpy as np

# Fundamental Constants
c = 299792458.0 # m/s
hbar = 1.0545718e-34 # J s
G = 6.67430e-11 # m^3 / (kg s^2)
eV = 1.602176634e-19 # J
GeV = 1e9 * eV

# Derived Conversions
hc = hbar * c # J m
eV_to_m = hc / eV # 1.9732698e-7 m
m_to_eV_inv = 1.0 / eV_to_m

def eV4_to_J_m3(energy_density_eV4):
    return energy_density_eV4 * eV * (m_to_eV_inv**3)

def J_m3_to_eV4(energy_density_J_m3):
    return energy_density_J_m3 / (eV * (m_to_eV_inv**3))

# Z^2 Framework Constants
Z2 = 32.0 * np.pi / 3.0
m_P_kg = np.sqrt(hbar * c / G)
M_P_reduced_kg = m_P_kg / np.sqrt(8.0 * np.pi)
M_P_reduced_eV = (M_P_reduced_kg * c**2) / eV

def compute_radion_dynamics(V0_J_m3, R_c_meters, delta_phi_over_MP=1e-12):
    """
    Computes radion mass, resonance frequency, and Casimir energy gradients.
    """
    V0_eV4 = J_m3_to_eV4(V0_J_m3)
    
    # 1. Radion Mass & Resonance Frequency
    # m_phi = Z^2 / M_P * sqrt(V0)
    m_phi_eV = (Z2 / M_P_reduced_eV) * np.sqrt(V0_eV4)
    m_phi_kg = m_phi_eV * eV / (c**2)
    freq_Hz = (m_phi_eV * eV) / hbar
    
    # 2. Casimir Energy Density (4D effective)
    # Using generalized geometric factor C = pi^2 / 720 (analogous to plates)
    C_geom = np.pi**2 / 720.0
    rho_casimir_J_m3 = -C_geom * hc / (R_c_meters**4)
    
    # 3. Casimir Gradient (Energy Pump)
    # delta_rho = -4 * rho * delta_phi/M_P
    delta_rho_J_m3 = -4.0 * rho_casimir_J_m3 * delta_phi_over_MP
    
    # 4. Theoretical Maximum Power Density (P/V)
    # P/V = omega * delta_rho
    omega = 2.0 * np.pi * freq_Hz
    power_density_W_m3 = omega * delta_rho_J_m3
    
    return {
        "m_phi_eV": m_phi_eV,
        "freq_Hz": freq_Hz,
        "rho_casimir_J_m3": rho_casimir_J_m3,
        "delta_rho_J_m3": delta_rho_J_m3,
        "power_density_W_m3": power_density_W_m3
    }

def print_regime(name, V0_eV4, R_c_m):
    V0_J = eV4_to_J_m3(V0_eV4)
    res = compute_radion_dynamics(V0_J, R_c_m)
    
    print(f"=== {name} ===")
    print(f"Vacuum Scale V0: {V0_eV4:.2e} eV^4  ({V0_J:.2e} J/m^3)")
    print(f"Compactification Radius R_c: {R_c_m:.2e} m")
    print(f"Radion Mass: {res['m_phi_eV']:.4e} eV")
    print(f"Resonance Frequency: {res['freq_Hz']:.4e} Hz")
    print(f"Base Casimir Density: {res['rho_casimir_J_m3']:.4e} J/m^3")
    print(f"Casimir Perturbation (delta_phi/M_P = 1e-12): {res['delta_rho_J_m3']:.4e} J/m^3")
    print(f"Max Power Extraction Density: {res['power_density_W_m3']:.4e} W/m^3\n")

if __name__ == "__main__":
    print("Running Z^2 Topological Casimir / Radion ZPE Computations\n")
    print(f"Reduced Planck Mass: {M_P_reduced_eV:.4e} eV\n")
    
    # Regime 1: Dark Energy Scale
    # V0 ~ (2.4e-3 eV)^4
    rho_Lambda_eV4 = (2.4e-3)**4
    print_regime("Regime 1: Cosmological Dark Energy (Sub-mm Compactification)", 
                 rho_Lambda_eV4, 1e-4)
    
    # Regime 2: Electroweak Scale
    # V0 ~ (246 GeV)^4
    ew_scale_eV4 = (246e9)**4
    print_regime("Regime 2: Electroweak Warped Scale", 
                 ew_scale_eV4, 1e-18)
    
    # Regime 3: GUT Scale
    # V0 ~ (1e16 GeV)^4
    gut_scale_eV4 = (1e25)**4
    print_regime("Regime 3: Grand Unified Theory (GUT) Scale", 
                 gut_scale_eV4, 1e-31)
