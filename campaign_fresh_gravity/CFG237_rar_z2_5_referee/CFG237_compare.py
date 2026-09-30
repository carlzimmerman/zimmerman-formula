"""CFG237_compare.py -- POST-RUN. Written and run ONLY after every CFG237 main, attack and MUTATE output was saved (see CFG237_run_all.sh outputs).
Opens CFG227's cfg227_points.csv and cfg227_rar_z2_5_results.json and compares them with my results; also uses their pre-flight SD/signal with MY systematic
function to see whether the B* difference is Monte Carlo or definition. Labelled post-run; nothing here is frozen."""
import sys, json
from CFG237_common import *

t = start("CFG237_compare")
C227 = os.path.join(REPO, "campaign_fresh_gravity", "CFG227_rar_z2_5")
pts = pd.read_csv(os.path.join(C227, "cfg227_points.csv"))
J = json.load(open(os.path.join(C227, "cfg227_rar_z2_5_results.json")))
M = json.load(open(os.path.join(HERE, "CFG237_main_results.json")))
PW = json.load(open(os.path.join(HERE, "CFG237_power_results.json")))
print("POST-RUN comparison. CFG227 points:", len(pts), "rows; groups:", pts.group.value_counts().to_dict())
print("CFG227 classes present:", sorted(pts["class"].unique()), "; any class M row:", bool((pts["class"] == "M").any()))

# --- S1 rows
s1 = pts[pts.set == "S1 Amvrosiadis"].reset_index(drop=True)
d = load_s1(); P = s1_points(d)
print("\nS1 rows: ids equal", list(s1.id.astype(str)) == list(d.alessid))
for nm, mine, col in (("g_obs", P["gobs"], "g_obs"), ("g_bar", P["gbar"], "g_bar"), ("r_kpc", P["r"], "r_kpc")):
    print(f"   {nm}: max rel diff {np.max(np.abs(mine / s1[col].values - 1)):.2e}")
for law, col in (("FLAT", "delta_FLAT"), ("PROXY", "delta_PROXY"), ("Hz", "delta_H(z)"), ("MDEC", "delta_M-DEC")):
    dd = delta(P["gobs"], P["gbar"], P["z"], law) - s1[col].values
    print(f"   delta_{law}: max |diff| {np.max(np.abs(dd)):.2e}")
print("   f_gas of g_bar: mine vs theirs max |diff|", float(np.max(np.abs(P["g_gas"] / P["gbar"] - s1.f_gas_of_gbar.values))))

# --- ALPAKA
al = pts[pts.set.str.startswith("S3")].reset_index(drop=True)
A = alpaka_points(load_alpaka()); mk = np.isfinite(A["gbar"])
ids_m = A["ids"][mk]
print("\nALPAKA rows: ids equal", list(al.id.astype(int)) == list(ids_m))
print(f"   g_obs max rel diff {np.max(np.abs(A['gobs'][mk] / al.g_obs.values - 1)):.2e}; g_bar {np.max(np.abs(A['gbar'][mk] / al.g_bar.values - 1)):.2e}; r {np.max(np.abs(A['R'][mk] / al.r_kpc.values - 1)):.2e}")
# --- RC100
rc = pts[pts.set.str.startswith("S4")].reset_index(drop=True)
R4 = rc100_rows(load_rc100("corrected"))
print("\nRC100 rows:", len(rc), "mine", len(R4["z"]), "; g_obs max rel diff", float(np.max(np.abs(R4["gobs"] / rc.g_obs.values - 1))), "; delta_FLAT max |diff|", float(np.max(np.abs(delta(R4["gobs"], R4["gbar"], R4["z"], "FLAT") - rc.delta_FLAT.values))))
# --- CRISTAL
cr = load_cristal(); det = cr.loc[DETECTED6]; vec = load_vec_outer()
for grp, rows in (("CRISTAL R_e independent (6)", cristal_Re_rows(det)), ("CRISTAL R_out independent (6)", cristal_Rout_rows(det, vec, "table_Rout"))):
    sub = pts[pts.group == grp].reset_index(drop=True)
    order = {str(i): k for k, i in enumerate(rows["ids"])}
    idx = [order[str(i)] for i in sub.id]
    print(f"\n{grp}: g_bar max rel diff {np.max(np.abs(rows['gind'][idx] / sub.g_bar.values - 1)):.2e}; D {np.max(np.abs(rows['Dind'][idx] / sub.D.values - 1)):.2e}; delta_FLAT max |diff| "
          f"{np.max(np.abs(delta(rows['gobs'][idx], rows['gind'][idx], rows['z'][idx], 'FLAT', D=rows['Dind'][idx]) - sub.delta_FLAT.values)):.2e}")
r12 = cristal_Re_rows(cr.loc[ID12]); sub = pts[pts.group == "CRISTAL R_e fit (12)"].reset_index(drop=True)
print(f"CRISTAL R_e fit (12): delta_FLAT max |diff| {np.max(np.abs(np.sort(delta(r12['gobs'], r12['gfit'], r12['z'], 'FLAT', D=r12['Dfit'])) - np.sort(sub.delta_FLAT.values))):.2e} (sorted)")

# --- group medians and CI edges
print("\nGROUP MEDIANS (mine seed 237 vs CFG227 seed 227)")
names = {"S1 Amvrosiadis": ("S1", None), "CRISTAL R_e independent (6)": ("CRISTAL_L", "R_e"), "CRISTAL R_out independent (6)": ("CRISTAL_L", "R_out")}
for g in J["groups"]:
    r = J["groups"][g]
    for law, lj in (("FLAT", "FLAT"), ("PROXY", "PROXY"), ("Hz", "H(z)"), ("MDEC", "M-DEC")):
        mine = None
        if g == "S1 Amvrosiadis": mine = M["S1"][law]
        elif g == "CRISTAL R_e independent (6)": mine = M["CRISTAL_L"]["R_e"][law]
        elif g == "CRISTAL R_out independent (6)": mine = M["CRISTAL_L"]["R_out"][law]
        if mine is None: continue
        print(f"   {g[:30]:30s} {law:5s}: median mine {mine['med']:+.4f} theirs {r[lj]['median']:+.4f} (diff {mine['med'] - r[lj]['median']:+.1e}); edges mine [{mine['lo']:+.3f},{mine['hi']:+.3f}] theirs [{r[lj]['lo']:+.3f},{r[lj]['hi']:+.3f}]")
# band medians
print("\nBAND MEDIANS S1 flat: theirs", {k: round(v, 3) for k, v in J["groups"]["S1 Amvrosiadis"]["FLAT"]["bands"].items()}, "| mine", {k: round(v["FLAT"], 3) for k, v in M["S1_band"].items() if k in ("-0.671", "-0.213", "0.213", "0.671")})

# --- pre-flight
print("\nPRE-FLIGHT: theirs vs mine (seed 237); their calibration systematic = max(|shift at +-B|) = my S_max")
for g, mk_ in (("S1 Amvrosiadis", "S1"), ("CRISTAL R_e independent (6)", "CRISTAL_Re"), ("CRISTAL R_out independent (6)", "CRISTAL_Rout")):
    q = J["preflight"][g]; a = PW[mk_]["main"]
    print(f"   {g[:30]:30s} SD {q['sd_stat']:.4f}/{a['sd']:.4f} | S {q['syst']:.4f}/S_max {a['S_max']:.4f} (S_half {a['S_half']:.4f}) | signal H(z) {q['signal']['H(z)']:.4f}/{a['sig_H']:.4f} | proxy {q['signal']['PROXY']:.4f}/{a['sig_P']:.4f} | needs {q['syst'] + 2 * q['sd_stat']:.3f}/{a['need_H_max']:.3f}")
    print(f"      their recovery {q['recovery']}; their band_needed {q['band_needed']}; mine B* {PW['Bstar'][mk_] if mk_ in PW.get('Bstar', {}) else 'n/a'}")

# B* with THEIR signal and SD but MY systematic function (S_max)
def syst_fn(group_key):
    sys.path.insert(0, HERE)
    import importlib
    return None

# reconstruct groups (same as CFG237_power)
d_ = load_s1(); P_ = s1_points(d_)
def grp_re(rows):
    Mst = 10 ** det.logMstar.values; f = det.f_molgas.values; Mg = Mst * f / (1 - f); s = Mst / (Mst + Mg)
    return dict(z=rows["z"], g_st=rows["gind"] * s, g_gas=rows["gind"] * (1 - s))
G = {"CRISTAL R_e independent (6)": grp_re(cristal_Re_rows(det)), "CRISTAL R_out independent (6)": grp_re(cristal_Rout_rows(det, vec, "table_Rout"))}
def smax(g, B):
    def dd(tau):
        gb = g["g_st"] + g["g_gas"] * 10 ** tau
        gobs = (g["g_st"] + g["g_gas"]) * nu_mono((g["g_st"] + g["g_gas"]) / A0["canonical"])
        return float(np.median(np.log10(gobs) - np.log10(gb * nu_mono(gb / A0["canonical"]))))
    d0 = dd(0.0)
    return max(abs(dd(B) - d0), abs(dd(-B) - d0))
print("\nB* using THEIR signal and SD with MY S_max function (is the R_e proxy 0.125 vs my 0.100 a Monte Carlo difference?)")
for g, gr in G.items():
    q = J["preflight"][g]
    for T in ("H(z)", "PROXY"):
        room = q["signal"][T] - 2 * q["sd_stat"]
        lo, hi = 1e-6, 3.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if smax(gr, mid) < room: lo = mid
            else: hi = mid
        print(f"   {g[:30]:30s} {T}: room {room:.4f} -> B* = {0.5 * (lo + hi):.3f}  (their printed {q['band_needed'][T]:.3f})")

# noise-free signal (what CFG227's code computes) vs the frozen text (A4 i: median over mocks): my noise-free values
print("\nNOISE-FREE signal = |median delta_FLAT when truth is H(z) (or proxy), no noise| (CFG227's code) against my median-over-mocks (frozen text)")
G["S1 Amvrosiadis"] = dict(z=P_["z"], g_st=P_["g_st"], g_gas=P_["g_gas"])
for g, gr in G.items():
    gb = gr["g_st"] + gr["g_gas"]
    out = {}
    for T in ("Hz", "PROXY"):
        gobs = gb * nu_mono(gb / (A0["canonical"] * LAWS[T](gr["z"])))
        out[T] = abs(float(np.median(np.log10(gobs) - np.log10(gb * nu_mono(gb / A0["canonical"])))))
    q = J["preflight"][g]
    print(f"   {g[:30]:30s} noise-free H(z) {out['Hz']:.4f} (theirs {q['signal']['H(z)']:.4f}); proxy {out['PROXY']:.4f} (theirs {q['signal']['PROXY']:.4f})")

# --- C5 and C7 implementation facts
src = open(os.path.join(C227, "cfg227_rar_z2_5.py")).read()
print("\nCODE FACTS (CFG227 script)")
print("   class M count computed anywhere?  'N_M' occurrences:", src.count("N_M"), "| the string 'N_M = 0' appears inside a P(...) literal:", "N_M = 0 -> pooled" in src)
print("   class assignment mechanism: a hard-coded dict CLASS (", "CLASS = {" in src, ") -- no rule, no cross-match")
print("   CRISTAL rows via exec of CFG213/CFG220 scripts:", "exec_lane(" in src, "; C5 compares against CFG222's results JSON:", "cfg222_lcdm_proxy_results.json" in src)
print("   C7 uses base = S1 * 3 (nine galaxies repeated) and first 20 rows:", "base = S1 * 3" in src)
print("   S1 footnote-flagged sources (049.1, 075.1, 122.1) treated as class S with alpha_CO 0.92 scaling?  the script has no footnote handling:", "footnote" not in src.lower())
print("   CRISTAL independent route gas share from f_molgas (stars (1-fm) g_bar, gas fm g_bar):", "(1 - fm) * gb" in src)
sys.exit(0)
