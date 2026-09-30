"""CFG230 frozen transcription (from CFG230_FROZEN_CRITERIA.md, section 3.6, 4.2, 5.1, 6.2). HAND transcription; script A audits it."""
LED = "campaign_fresh_gravity/LEDGER.md"
CM = "campaign_fresh_gravity/closure_map/"
CF = "campaign_fresh_gravity/"

REQS = ["R01", "R02", "R03", "R04", "R05", "R06", "R07", "R08", "R09", "R10", "R11", "R12"]
REQ_NAMES = {
 "R01": "SCALE-EXPONENT", "R02": "ACCELERATION SCALE (R02a dimensional; R02b gradient-type trigger)", "R03": "SHAPE (declared kernel)",
 "R04": "CLOSURE (nonlocal or collisionless)", "R05": "COLD-EARLY and STATIONARY", "R06": "RECIPROCITY and ENERGY",
 "R07": "BOUND-ONLY SWITCH (ownership)", "R08": "EFE BRANCH (declared)", "R09": "SOLAR-SYSTEM TAIL", "R10": "PREFERRED FRAME",
 "R11": "STABILITY and CAUSALITY of the MOND-carrying / gating sector", "R12": "MEDIUM, TIE and CONSTANTS"}

# ---- 5.1 incidence matrix (frozen)
MATRIX = {
 "D01":  "F F F N F p* N N F U U F",
 "D02":  "P P F N U U N U F U U p*",
 "D03":  "p* p* F F F F F U p* N U F",
 "D04":  "F P F F U F N U F N F F",
 "D05":  "p* p* p* p* N N N N N N N p*",
 "D06":  "F F F F p* p* N N p* N p* p*",
 "D07":  "F F F F F p* N N p* N p* F",
 "D08":  "U F U F F F N N p* N p* F",
 "D09":  "F F F N F p* N N F U F F",
 "D10":  "F U F U F F F N F U F F",
 "D11A": "p* p* p* N U F N U F U F p*",
 "D11B": "F p* p* N F F N U F F F F",
 "D11Ca":"p* p* p* N F F N U F U U U",
 "D11Cb":"F U U N F F N U F F F U",
 "D11Cc":"F U U N F F N U U U F F",
 "D11Cd1":"F U F N p* p* F U F p* p* U",
 "D11Cd2":"F U F N F F F U U U F F",
}
MATRIX = {k: v.split() for k, v in MATRIX.items()}
ROW_ORDER = list(MATRIX)

# ---- 3.6 row records: lane prefix, lane commit, referee prefix, referee commit, referee status, shared tags, anchors (file, string)
ROWS = {
 "D01": dict(name="Mashhoon-type kernel", lane="CFG120", commit="9e4757627", ref="CFG151", refc="db335c0e7", rs="R", shared="SH1 SH5",
   anchors=[(LED, "31.6228"), (LED, "29.02 M needed vs 5.36 M available"), (LED, "1.222 against the 1.1 line"), (LED, "31.622777"),
            (LED, "0/18 exponential-sphere cases pass"), (LED, "|Q|/(k^2 phi) = 26")]),
 "D02": dict(name="Verlinde", lane="CFG117", commit="bb504274c", ref=None, refc=None, rs="X", shared="SH10 SH5",
   anchors=[(LED, "C_V/C_target = (1 + x)/x exactly"), (LED, "0 of 16 cases"), (LED, "kappa_V = sqrt(8 pi/3)/6 = 0.482"), (LED, "Hees, Famaey & Bertone 2017")]),
 "D03": dict(name="dipolar DM", lane="CFG121", commit="16fca9acd", ref="CFG157", refc="0bbd62cd7", rs="Q", shared="SH3 SH4 SH5 SH8 SH10",
   anchors=[(LED, "Q^2/kappa_I >= ~140"), (LED, "860x and 115x apart"), (LED, "1.3099 / 1.0160 / 0.4342 / 0.0632"), (LED, "Q* = 9.677"),
            (CF + "CFG121_door3_dipolar_dm/README.md", "12-202x"), (CF + "CFG121_door3_dipolar_dm/README.md", "0.51 (12 knots)")]),
 "D04": dict(name="superfluid DM", lane="CFG122", commit="b7d41c302", ref="CFG154", refc="2f6845de3", rs="R", shared="SH1 SH3 SH4 SH5 SH6",
   anchors=[(LED, "0/3600 cells"), (LED, "31.62"), (LED, "0.414 off P2"), (LED, "118-890 g_law"), (LED, "c_s^2 < 0"), (LED, "237 independent tests")]),
 "D05": dict(name="f(E,L)", lane="CFG130", commit="c1d719fbf", ref="CFG155", refc="bdbcf3fe1", rs="R", shared="SH7",
   anchors=[(LED, "encodes C(r) instead of deriving it"), (LED, "x^5/(pi (1+x^2)^(7/2))"), (LED, "1201 energies")]),
 "D06": dict(name="secondary infall", lane="CFG118", commit="d0baef700", ref="CFG158", refc="c868ad276", rs="Q", shared="SH2",
   anchors=[(LED, "M^0.33-0.34"), (LED, "0 of 8 mass-geometry cases"), (LED, "1.0-4.2x"), (LED, "0.28-0.66x"), (LED, "EdS slope -2.410 against")]),
 "D07": dict(name="fuzzy DM soliton", lane="CFG119", commit="435cb43e9", ref="CFG159", refc="a1fb4a128", rs="R", shared="SH1 SH3",
   anchors=[(LED, "1.28e-20 eV"), (LED, "1.2e5 dex"), (LED, "misses by 4.0 dex"), (LED, "1.4e-7")]),
 "D08": dict(name="interacting vacuum", lane="CFG131", commit="aa0d95aef", ref="CFG156", refc="bb7bd135d", rs="R", shared="SH2 SH3 SH4",
   anchors=[(LED, "32-353"), (LED, "0.0275"), (LED, "x = 6.29"), (LED, "4.608e-12"), (CF + "CFG131_door8_interacting_vacuum/README.md", "32-272x (point mass, exact), 32-353x (exponential sphere"),
            (CF + "CFG156_door8_vacuum_referee/README.md", "271.71")]),
 "D09": dict(name="Deser-Woodard / RR", lane="CFG123", commit="9e4757627", ref="CFG153", refc="9ce8b61c5", rs="R", shared="SH1 SH6",
   anchors=[(LED, "6.057e-11"), (LED, "-m^2 M cos(mr)/(12 pi r)"), (LED, "signature (2,2)"), (LED, "exactly 1000")]),
 "D10": dict(name="mimetic", lane="CFG124", commit="9e4757627", ref="CFG152", refc="7cb9ba39e", rs="R", shared="SH2 SH3 SH4 SH6 SH8",
   anchors=[(LED, "gt/(2 - 3 gt)"), (LED, "2624"), (LED, "factor 460"), (LED, "0/1600")]),
 "D11A": dict(name="11A inflow", lane="CFG171", commit="1c91164e9", ref=None, refc=None, rs="X", shared="SH4 SH5 SH6 SH7 SH11",
   anchors=[(LED, "1257"), (LED, "16-205"), (LED, "c_s² < 0".replace("²", "^2"))]),
 "D11B": dict(name="11B' directional", lane="CFG173", commit="e415659c7", ref=None, refc=None, rs="X", shared="SH4 SH6 SH7 SH9 SH11",
   anchors=[(LED, "3e5-1e7"), (LED, "1.2e-6")]),
 "D11Ca": dict(name="11C-a", lane="CFG172", commit="f1585212e", ref="CFG188", refc="058296d6f", rs="R", shared="SH3 SH4 SH5 SH6 SH7 SH9",
   anchors=[(LED, "0.282"), (LED, "6.3e3"), (LED, "14-240x"), (LED, "0.155"), (LED, "21 AGREE, 5 CONDITIONAL, 1 NOT DONE, 0 DISAGREE")]),
 "D11Cb": dict(name="11C-b", lane="CFG172", commit="f1585212e", ref="CFG188", refc="058296d6f", rs="R", shared="SH3 SH9",
   anchors=[(LED, "t <= 1.2e-6"), (LED, "t >= 4e6"), (LED, "3e12")]),
 "D11Cc": dict(name="11C-c", lane="CFG172", commit="f1585212e", ref="CFG188", refc="058296d6f", rs="R", shared="SH6",
   anchors=[(LED, "best deviation 0.97"), (LED, "-K_c rho")]),
 "D11Cd1": dict(name="11C-d arm 1", lane="CFG172D", commit="249fa4ec8", ref=None, refc=None, rs="X", shared="SH3 SH6",
   anchors=[(LED, "96 cells"), (LED, "4e3-9e3 km/s")]),
 "D11Cd2": dict(name="11C-d arm 2", lane="CFG172D", commit="249fa4ec8", ref=None, refc=None, rs="X", shared="SH3 SH4 SH6",
   anchors=[(LED, "5.6e4 and 49 times g_law"), (LED, "209 times orbital")]),
}
SUPPORT = {
 "S174": dict(lane="CFG174", commit="eb2e3e066", ref="CFG181", refc="305d2c2ae", anchors=[(LED, "0.293"), (LED, "365 M")]),
 "S176": dict(lane="CFG176", commit="f0eb2da28", ref=None, refc=None, anchors=[(LED, "0.078"), (LED, "0.59")]),
 "S177": dict(lane="CFG177", commit="2aa9eeda2", ref=None, refc=None, anchors=[(LED, "NO NEW CONTENT")]),
 "S179": dict(lane="CFG179", commit="97cda7ad3", ref="CFG191", refc="6eced32e2", anchors=[(LED, "F(z + z_e) - F(z_e) = F(z)"), (LED, "1.089 / 1.102")]),
 "P43": dict(lane="CFG43", commit="e42a98572", ref="CFG103", refc=None, anchors=[(CF + "CFG43_fluid_tie/README.md", "convention-dependent, from about 11")]),
 "P44": dict(lane="CFG44", commit="513ee4b28", ref=None, refc=None, anchors=[(CF + "CFG44_fluid_target/README.md", "far-shell theorem"), (CF + "CFG44_fluid_target/README.md", "temperature-slaved"), (CF + "CFG44_fluid_target/README.md", "R(x = 1) = 1.46")]),
 "P48": dict(lane="CFG48", commit="0dba13349", ref="CFG48", refc="35eebbe99", anchors=[(CF + "CFG48_gap1_switch/README.md", "44 of 48"), (CF + "CFG48_gap1_switch/README.md", "48 layer x width cases"), (CF + "CFG48_gap1_switch/README.md", "23-50 times")]),
 "P50": dict(lane="CFG50", commit="bb2a7b680", ref="CFG101", refc="55b030906", anchors=[(CM + "GAPS_1_2_JOINT_STATUS.md", "0.5008"), (CM + "GAPS_1_2_JOINT_STATUS.md", "17-19x")]),
 "P70": dict(lane="CFG70", commit="9655413f6", ref="CFG94", refc="878bab1fb", anchors=[(CM + "GAPS_1_2_JOINT_STATUS.md", "318 / 179 / 57x"), (CM + "GAPS_1_2_JOINT_STATUS.md", "64,512")]),
 "P72": dict(lane="CFG72", commit="4de2b05bc", ref=None, refc=None, anchors=[(CM + "GAPS_1_2_JOINT_STATUS.md", "22.5 g_law")]),
}

LEAN_DIR = "fable_independent_2026/lean_2026/ChainCert/"
LEAN_NAMES = {  # committed at b8d8b1ba5 or earlier (table 2.2)
 "Ownership.lean": ["noEFE_continuousLinear", "noEFE_linear_R3", "noEFE_linear_real", "noEFE_linear_ray", "deep_not_efeFreeRay", "law_not_efeFreeRay",
                    "vecLaw_not_efeFree", "ownership_distinguishes", "ownership_not_field_local", "deep_kernel_ne_one", "owned_boost_one"],
 "DoorEleven.lean": ["boosted_flux", "vacuum_no_flux", "flux_zero_iff", "vacuum_boost_invariant", "vacuum_momentum_density_zero"],
 "PointMass.lean": ["no_single_polytrope"],
 "Certificates.lean": ["C1_a0_form_iff"],
 "Theory.lean": ["ownership_nonlocal", "merged_law_has_EFE"],
}
LEAN_PENDING = ["Action.lean", "Dimension.lean", "FluidLink.lean"]

# ---- 4.2 requirement sub-claims: (claim, class, grade, load_bearing, referee_reproduced, has_referee) ; grades L S+R S N+R N D
SUB = {
 "R01": [("fixed-kernel lemma C~M^2 vs M", "THEOREM", "S+R", 1), ("tolerance window arithmetic", "THEOREM", "S", 1),
         ("per-door exponents / spreads", "SCOPED-NUMERICAL", "N+R", 1), ("band and same-constants clause", "DECLARED-CHOICE", "D", 1)],
 "R02": [("R02a dimensional (monomial family, given G4)", "THEOREM", "S", 1), ("R02b gradient-type trigger (sf05)", "SCOPED-NUMERICAL", "N", 0)],
 "R03": [("P2 profile identities (Lean)", "THEOREM", "L", 0), ("kernel is declared", "DECLARED-CHOICE", "D", 1)],
 "R04": [("local / barotropic closures excluded", "THEOREM", "S", 1), ("point-mass Gamma(x) monotone (Lean)", "THEOREM", "L", 0),
         ("constraint action", "SCOPED-NUMERICAL", "N", 0)],
 "R05": [("c_s^2 <= 4.6e-12 vs halo need", "SCOPED-NUMERICAL", "N+R", 1), ("per-door pincers", "SCOPED-NUMERICAL", "N", 1), ("growth convention", "DECLARED-CHOICE", "D", 1)],
 "R06": [("exchange closed form", "THEOREM", "S+R", 1), ("memory kernel / light cone", "SCOPED-NUMERICAL", "N", 1), ("r_ta convention, 0.10 line", "DECLARED-CHOICE", "D", 1)],
 "R07": [("07a Gauss lemma (derivation and numbers)", "THEOREM", "S+R", 1), ("07a algebra of the solution check (Lean Gauss)", "THEOREM", "L", 1), ("07b ownership non-local (Lean, conditional)", "THEOREM", "L", 1),
         ("07c local gates unstable 44/48", "SCOPED-NUMERICAL", "N+R", 1), ("07d r_ta convention edge", "DECLARED-CHOICE", "D", 1)],
 "R08": [("no-EFE dichotomy (pointwise laws; Lean)", "THEOREM", "L", 1), ("branch choice (ownership)", "DECLARED-CHOICE", "D", 0)],
 "R09": [("tail bound in (yq)'>=0 class", "THEOREM", "S+R", 1), ("Q2 ratios (kernel, g_ext dependent)", "SCOPED-NUMERICAL", "N+R", 1), ("band", "DECLARED-CHOICE", "D", 1)],
 "R10": [("11C-b pincer / KM1 / dipole", "SCOPED-NUMERICAL", "N", 1), ("branch and dressing", "DECLARED-CHOICE", "D", 1)],
 "R11": [("D10 ghost (frozen mimetic class)", "THEOREM", "S+R", 0), ("per-door stiffness tally", "SCOPED-NUMERICAL", "N", 1), ("shared reading", "DECLARED-CHOICE", "D", 0)],
 "R12": [("(a) SR algebra: w=-1 no flux (Lean)", "THEOREM", "L", 1), ("(a) GR extension (CFG176 sympy)", "THEOREM", "S", 1), ("numbers (DESI, CFG174 column)", "SCOPED-NUMERICAL", "N", 1),
         ("tie / cap entry", "DECLARED-CHOICE", "D", 1)],
}
STATED = {  # verb used in the frozen text for the requirement headline
 "R01": "moves-with", "R02": "must", "R03": "moves-with", "R04": "must", "R05": "fails-in-class", "R06": "must", "R07": "must",
 "R08": "must", "R09": "must", "R10": "fails-in-class", "R11": "fails-in-class", "R12": "must"}
# frozen hand estimates (section 8)
EST = {"whole_theorem": (3, (2, 4)), "core_plus_parts": (5, (4, 6)), "no_core": (4, (3, 5)), "referee_cores": (4, (3, 5)), "lean_cores": (4, (3, 4)), "own_no_referee": (2, None)}

# ---- pincers (4.5): (pair, statement, numeric gap as printed by the lane, source anchor)
PINCERS = [
 ("R01xR06/R02", "formation-funded gets M^(1/3); r_M needs c through an acceleration scale", None, (LED, "M^0.33-0.34")),
 ("R05xR04", "cold at z>~10 vs hot in halos", (4.3e3, 1.3e5), (LED, "4.26e3")),
 ("R05xR04(D03)", "medium budget vs growth", (860.0, 115.0), (LED, "860x and 115x apart")),
 ("R09xR11", "(yq)'>=0 forces tail >= 0.282 a0", (0.282, None), (LED, "0.282")),
 ("R03xR09", "P2 shape carries the a0/2 tail", (0.5, None), (LED, "6.3e3")),
 ("R01/R03xR10(D11Cb)", "G1 t<=1.2e-6 vs G6/G7 t>=4e6", (3e12, 8.7e9), (LED, "3e12")),
 ("R07xR06", "nonlocal gate stable but bilocal; exchange costs 23-318x orbital energy", (23.0, 318.0), (CM + "GAPS_1_2_JOINT_STATUS.md", "318 / 179 / 57x")),
 ("R05xR12(d)", "Q!=0 makes a0 flow; flat only |xi|<0.0275", (0.0275, None), (LED, "0.0275")),
 ("R12(b)xR04", "cap P_cap=a0^2/(8 pi G) vs target pressure ratio 1/x^2", None, None),
]

# ---- 6.2 screening labels (frozen). cell = label + optional tag [T]/[s]/[m]
CLASSES = {
 "C02": ("AeST", {"R04": "N", "R06": "N", "R05": "M", "R12": "F[m]"}),
 "C03": ("Khronon / Horava-type MOND", {"R04": "N", "R06": "N"}),
 "C04": ("Einstein-aether MOND", {"R04": "N", "R06": "N"}),
 "C05": ("TeVeS", {"R04": "N", "R06": "N", "R12": "F[m]"}),
 "C06": ("Nonlocal metric MOND (DEFW)", {"R04": "N", "R06": "N", "R09": "F[s]", "R11": "F[s]"}),
 "C07": ("Scale-dependent G (RG-improved)", {"R01": "F[T]", "R02": "F[T]", "R12": "F[m]"}),
 "C08": ("MOG / STVG", {"R01": "F[m]", "R02": "F[m]", "R12": "F[m]", "R10": "M"}),
 "C09": ("Cuscuton", {"R04": "F[s]"}),
 "C10": ("Disformal couplings", {}),
 "C11": ("AQUAL / QUMOND", {"R01": "M", "R02": "M", "R04": "N", "R05": "N", "R06": "N", "R07": "F[s]", "R09": "F[s]", "R10": "N", "R11": "M", "R12": "F[m]"}),
 "C12": ("Modified inertia", {"R04": "N", "R06": "N", "R02": "M", "R12": "F[m]"}),
 "C13": ("Galileon / Vainshtein scalar", {"R09": "M"}),
 "C14": ("Weyl / conformal gravity", {"R01": "F[T]", "R02": "F[T]", "R12": "F[m]"}),
}
CONTROLS = {"C15": ("Mashhoon kernel (D01)", "D01", {"R01": "F[T]"}), "C16": ("Verlinde (D02)", "D02", {}), "C17": ("superfluid (D04)", "D04", {}), "C18": ("Deser-Woodard (D09)", "D09", {})}
IN_FLIGHT = ["CFG231 (door 12, covariant emergent gravity)", "CFG232 (door 13, BIMOND / two-metric)", "CFG250 (mass-free outer-slope a0 at KURVS)",
             "CFG251 (door 11D, incl. set-at-turnaround ownership)", "CFG252 (timescape / void-wall reading vs the a0 tie)"]

# ---- Amendment 1 (post-freeze): the pending Lean batch was committed (a288aad86, 281 theorems, standard axioms only).
# R02a splits: the monomial statement the Dimension module proves (grade L, premises: monomial family, one extra constant)
# and the Newtonian-only M^(1/3) half, which no Lean file states (grade S, this lane's own derivation).
SUB_AMEND1 = dict(SUB)
SUB_AMEND1["R02"] = [("R02a monomial: no (G,M,c) length ~ M^(1/2); one extra constant X iff acceleration scale (Lean Dimension, monomials only)", "THEOREM", "L", 1),
                     ("R02a Newtonian (G,M,H) only gives (GM/H^2)^(1/3) (own derivation, no Lean file)", "THEOREM", "S", 1),
                     ("R02b gradient-type trigger (sf05)", "SCOPED-NUMERICAL", "N", 0)]
LEAN_DIMENSION_NAMES = ["no_sqrtM_length_GMc", "sqrtM_length_iff", "acc_unique", "acc_c_family", "hbar_admissible", "not_only_accelerations", "rho_length", "quarterM_velocity_iff"]

# ---- extra encoding facts used by script H
CONDITIONAL_ON = {"R02": ["G4 constant inventory"], "R06": ["r_ta convention", "0.10 line"], "R07": ["r_ta convention", "ownership rule (postulate)", "hierarchy H"],
                  "R08": ["pointwise-law class"], "R09": ["G1 band", "(yq)'>=0 premise"], "R12": ["tie / cap entry postulated"], "R04": [], "R01": []}
REFEREE_FLAG = {"R08": True}   # the dichotomy is also reproduced by CFG191 (sympy version)

# ---- Amendment 2 (post-freeze): the record's own galileon scaling scripts were read (allowed by frozen 6.2 note C13)
AMEND2_LABELS = {"C13": {"R03": "F[s]"}}
AMEND2_SOURCE = ("qwen_claude_field_theory/closure_2026/bimetric_door/galileon_mond_scaling_nogo.py", "qwen_claude_field_theory/closure_2026/bimetric_secondfield/galileon_scaling_theorem.py")
