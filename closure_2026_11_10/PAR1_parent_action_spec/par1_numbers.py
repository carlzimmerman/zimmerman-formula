"""PAR1 numbers: S9 (T-TRI: cold background span vs galaxy well depths) and S15 (T-GR: granule suppression vs the
wave dust's forest line), per footing. Criteria 51522963e0.

Run: python3 par1_numbers.py -> par1_numbers.out/.json ; PAR1_MUTATE=MU4 -> *_MUTATE_MU4.*
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, time
import numpy as np
from scipy.integrate import quad

MUT = os.environ.get("PAR1_MUTATE", "")
TAG = f"_MUTATE_{MUT}" if MUT else ""
G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; MPC = 1e3 * KPC; KMS = 1e3
HBAR = 1.054571817e-34; HPL = 2 * np.pi * HBAR; EV = 1.602176634e-19; C = 2.99792458e8
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
# cosmology (stated; the margins below do not turn on it): h, omega_b, form B share 5.41
h = 0.674; omb = 0.02237; Ob = omb / h ** 2; Oc = 5.41 * Ob; Om = Ob + Oc
H0 = 100 * h * KMS / MPC
rho_crit0 = 3 * H0 ** 2 / (8 * np.pi * G)
LOGM = [9.4, 10.45, 10.7, 10.9]
RTA = {9.4: 120.0, 10.45: 268.0, 10.7: 325.0, 10.9: 378.0}  # FLD1 canonical z 0 (alt within 0.5 %), kpc
EPS = 1.0  # Plummer softening, kpc (COL1)
OUT = {"cosmology": {"h": h, "Omega_b": Ob, "Omega_c": Oc, "Omega_m": Om}}
L = []


def rep(k, v, note=""):
    OUT[k] = v; L.append(f"{k}: {v}" + (f"   [{note}]" if note else ""))


t0 = time.time()
# ------------------------------------------------------------------ S9 (a): cbar from the record's forest line
z3 = 3.0
lam_com = 0.42 / h * MPC  # QX28 G6c / QX3 iter3 G4': comoving Jeans length <= 0.42/h Mpc at z = 3
lam_phys = lam_com / (1 + z3)
rho_m3 = Om * rho_crit0 * (1 + z3) ** 3
cbar_forest = lam_phys * np.sqrt(G * rho_m3 / np.pi)  # lambda_J = c_s sqrt(pi/(G rho))
rep("S9_cbar_forest_kms", round(cbar_forest / KMS, 3), "c_s(nbar, z 3) <= this (record forest line)")
rep("S9_half_cbar2_forest_kms2", round((cbar_forest / KMS) ** 2 / 2, 2))
cbar_grw = 300.0
rep("S9_cbar_GRW1_edge_kms", cbar_grw, "bracket: MK2/GRW1 band edge; everything fails above")
rep("S9_half_cbar2_GRW1_kms2", cbar_grw ** 2 / 2)


def law_g(gN, a0):
    y = gN / a0
    return gN * (1 + np.sqrt(1 + 4 / y)) / 2


def gN_plummer(r_kpc, Mb):
    r = r_kpc * KPC; e = EPS * KPC
    return G * Mb * r / (r ** 2 + e ** 2) ** 1.5


def depth(r_kpc, Rta_kpc, Mb, a0):
    f = lambda rr: law_g(gN_plummer(rr, Mb), a0) * KPC
    v, _ = quad(f, r_kpc, Rta_kpc, limit=200)
    return v  # m^2/s^2


S9 = {}
for foot, a0 in FOOT.items():
    S9[foot] = {}
    for lm in LOGM:
        Mb = 10 ** lm * MSUN
        d = {}
        for rr in (10.0, 30.0, 100.0):
            for lab, Rt in (("Rta", RTA[lm]), ("Rta/4", RTA[lm] / 4)):
                if rr < Rt:
                    d[f"{rr:g}kpc_to_{lab}"] = round(np.sqrt(depth(rr, Rt, Mb, a0)) / KMS, 1)
        vinf = (G * Mb * a0) ** 0.25
        d["v_inf_kms"] = round(vinf / KMS, 1)
        S9[foot][str(lm)] = d
        L.append(f"S9 {foot} logMb {lm}: sqrt(depth) km/s {d}")
OUT["S9_sqrt_depth_kms"] = S9
line_forest = all(S9[f][str(lm)]["10kpc_to_Rta"] ** 2 > (cbar_forest / KMS) ** 2 / 2 for f in FOOT for lm in LOGM)
line_forest_q = all(S9[f][str(lm)]["10kpc_to_Rta/4"] ** 2 > (cbar_forest / KMS) ** 2 / 2 for f in FOOT for lm in LOGM)
line_grw = {f: [lm for lm in LOGM if S9[f][str(lm)]["10kpc_to_Rta"] ** 2 > cbar_grw ** 2 / 2] for f in FOOT}
rep("S9_line_depth10_gt_half_cbar2_forest_all", bool(line_forest), "frozen line (graded)")
rep("S9_same_with_Rta_over_4", bool(line_forest_q), "reported")
rep("S9_masses_deeper_than_GRW1_bracket", line_grw, "reported bracket")
depth_ratio = {f: min(S9[f][str(lm)]["10kpc_to_Rta"] ** 2 / ((cbar_forest / KMS) ** 2 / 2) for lm in LOGM) for f in FOOT}
rep("S9_min_depth_over_half_cbar2_forest", {f: round(v, 1) for f, v in depth_ratio.items()})

# ------------------------------------------------------------------ S15: Gaussian granule model
rng = np.random.default_rng(1)
NS = 1_000_000
Z = rng.standard_normal((NS, 3)) / np.sqrt(3.0)  # unit rms magnitude


def Rsup(s_over_a0, g_over_a0):
    if MUT == "MU4":
        s_over_a0 = 0.0
    A = Z * s_over_a0
    A[:, 2] += g_over_a0
    Am = np.linalg.norm(A, axis=1)
    KPz = (A[:, 2] / (1 + Am)).mean()  # K P = a0 A/(a0 + |A|), units of a0
    law = g_over_a0 / (1 + g_over_a0)
    return KPz / law


grid_s = np.logspace(-2, 3, 41)
S15 = {"R_table": {}}
for gg in (0.03, 0.1, 0.3, 1.0):
    Rs = [Rsup(s, gg) for s in grid_s]
    S15["R_table"][str(gg)] = [round(float(v), 4) for v in Rs]
    # s at which R crosses 0.5 (log interpolation)
    sh = None
    for i in range(len(grid_s) - 1):
        if Rs[i] >= 0.5 > Rs[i + 1]:
            f = (Rs[i] - 0.5) / (Rs[i] - Rs[i + 1])
            sh = float(np.exp(np.log(grid_s[i]) + f * (np.log(grid_s[i + 1]) - np.log(grid_s[i]))))
    S15[f"s_half_over_a0_g{gg}"] = sh
    L.append(f"S15 g/a0 {gg}: s_half/a0 = {sh}; R(s=0.01 a0) = {Rs[0]:.4f}; R(s=1000 a0) = {Rs[-1]:.2e}")
rep("S15_R_at_s0_check", round(float(Rsup(0.0, 0.1)), 6), "MU4/KA: no fluctuation -> R = 1")
S15["s_grid_over_a0"] = [float(v) for v in grid_s]

# wave dust forest bound from the record's line: quantum Jeans k_J^4 = 16 pi G rho m^2/hbar^2 (physical, z 3)
kJ = 2 * np.pi / lam_phys
m_min = kJ ** 2 * HBAR / np.sqrt(16 * np.pi * G * rho_m3)
rep("S15_m_min_record_forest_eV", float(m_min * C ** 2 / EV), "wave dust must be at least this heavy (record line)")
m_lit = 2e-21  # Irsic+2017 (PROVISIONAL): bracket only
rep("S15_m_min_literature_bracket_eV", m_lit, "PROVISIONAL; reported, not graded")
S15["per_mass"] = {}
gap_ok = {}
for foot, a0 in FOOT.items():
    gap_ok[foot] = True
    for lm in LOGM:
        Mb = 10 ** lm * MSUN
        sig = np.sqrt(0.5 * np.sqrt(G * Mb * a0))  # law's isothermal dispersion
        row = {"sigma_kms": round(sig / KMS, 1)}
        for gg in (0.1, 0.3):
            sh = S15[f"s_half_over_a0_g{gg}"]
            if sh is None:
                row[f"g{gg}"] = "no crossing"; continue
            # s = sigma^2 / lambda_dB, lambda_dB = h/(m sigma) -> s = m sigma^3 / h ; R >= 0.5 needs s <= s_half a0
            m_max = sh * a0 * HPL / sig ** 3
            gap = m_min / m_max
            gap2pi = 2 * np.pi * m_min / m_max  # bracket: s = sigma^2/(lambda_dB/2pi) -> m_max / 2pi
            row[f"g{gg}"] = {"m_max_eV": float(m_max * C ** 2 / EV), "gap_record": round(float(gap), 3),
                             "gap_record_2pi_bracket": round(float(gap2pi), 3),
                             "gap_literature": round(float(m_lit * EV / C ** 2 / m_max), 1),
                             "lambda_dB_needed_kpc": round(float(sig ** 2 / (sh * a0) / KPC), 2)}
            if gg == 0.1 and gap < 3:
                gap_ok[foot] = False
        S15["per_mass"].setdefault(foot, {})[str(lm)] = row
        L.append(f"S15 {foot} logMb {lm}: {row}")
rep("S15_branch_fine_EMPTY_by_frozen_rule", gap_ok, "gap >= 3 at g/a0 0.1 for every mass (record forest line)")
OUT["S15"] = S15
OUT["runtime_s"] = round(time.time() - t0, 1); OUT["mutate"] = MUT
json.dump(OUT, open(f"par1_numbers{TAG}.json", "w"), indent=1, default=str)
with open(f"par1_numbers{TAG}.out", "w") as f:
    f.write(f"PAR1 numbers (criteria 51522963e0); mutate={MUT or 'none'}\n" + "\n".join(L) +
            "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
print("\n".join(L))

# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
