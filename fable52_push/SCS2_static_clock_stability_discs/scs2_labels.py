"""SCS2: the labels, read off the committed outputs by the frozen rules (FROZEN_CRITERIA.md section 4, amendments A1-A4).
No new computation: this script only reads the json files in this folder and writes scs2_labels.json / .out.

Families per footing: isolated discs (primary + thick, disc + bulge, R_d x 0.5 / x 2), external field along the axis (2D),
external field in the plane (3D). Rules:
- STABLE: route 1 has no growing root at any frozen point, and route 2 finds no negative direction at the frozen tolerance
  (pencil and inertia, every m and parity, both grids; 3D: no negative Rayleigh numerator), with every known answer passing.
- UNSTABLE IN REGIONS: both routes find growth and every known answer passes, KA4's two-resolution clause on that family
  included.
- NO VERDICT: a known answer fails, or the routes disagree. The reasons are listed, and so is the reading.
Route 1 is read from the A4 fit (A4: graded only if KA1 passes with it); the frozen fit's numbers are reported beside it.
TEST lane; adopts nothing.
"""
import os, json, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda name: json.load(open(os.path.join(HERE, name)))
OUTL = []
def P_(s=""):
    print(s, flush=True); OUTL.append(str(s))

def family(tag):
    if tag.startswith("KA1"):
        return "KA1"
    if "EF_axis" in tag:
        return "EF_axis"
    if "EF_plane" in tag:
        return "EF_plane"
    return "isolated"

def footing(tag):
    return "canonical" if "_canonical" in tag else "alt"

maps = J("scs2_maps.json"); ka = maps["known_answers"]
r2 = []
for f in sorted(glob.glob(os.path.join(HERE, "scs2_route2_part*.json"))):
    r2 += json.load(open(f))["rows"]
res = J("scs2_resolution.json")
w_frozen = J("scs2_wkb.json"); w_a4 = J("scs2_wkb_A4.json")
k1_frozen = J("scs2_wkb_KA1.json")["KA1_point_mass_frequencies"]; k1_a4 = w_a4["KA1_point_mass_frequencies"]

KA = dict(item1=w_frozen["item1_general_background"]["pass_"], KA3=w_frozen["KA3_planar_slab_TPA1"]["pass_"],
          KA1_map=all(v["positive_everywhere"] for v in ka["KA1_point_mass_map"].values()),
          KA1_freq_frozen_fit=k1_frozen["pass_"], KA1_freq_A4_fit=k1_a4["pass_"],
          KA2=ka["KA2_kuzmin"]["pass_"], KA4_graded_primaries=ka["KA4_residual_convergence"]["pass_"],
          KA5_point=ka["KA5_point_mass"]["pass_"], KA5_discs=ka["KA5_discs"]["pass_"])
P_("known answers: " + ", ".join(f"{k} {'PASS' if v else ('FAIL' if v is False else 'n/a')}" for k, v in KA.items()))
P_(f"KA1 frequencies: frozen fit max rel {k1_frozen['max_rel_to_scs1']:.2e}; A4 fit max rel {k1_a4['max_rel_to_scs1']:.2e} (line 1e-2)")
route1 = w_a4 if KA["KA1_freq_A4_fit"] else None

# KA4's clause per family, from the twins
ka4fam = collections.defaultdict(lambda: [0, 0])
for r_ in res["rows"]:
    key = (family(r_["tag"]), footing(r_["tag"]))
    ka4fam[key][0] += 1
    ka4fam[key][1] += int(r_["frac_agree"] and r_["min_agree"] and r_["sign_agree"])

LAB = {}
for fam in ("isolated", "EF_axis", "EF_plane"):
    for foot in ("canonical", "alt"):
        rs2 = [r_ for r_ in r2 if family(r_["tag"]) == fam and footing(r_["tag"]) == foot]
        neg_inertia = sum(1 for r_ in rs2 if r_.get("negative_by_inertia"))
        evaluated = sum(1 for r_ in rs2 if "negative_by_inertia" in r_)
        pencil = [r_ for r_ in rs2 if "lambda_min" in r_]
        pencil_unstable = sum(1 for r_ in pencil if r_["unstable_pencil"])
        pencil_negative = sum(1 for r_ in pencil if r_["lambda_min"] < 0)
        r1 = [r_ for r_ in (route1["rows"] if route1 else []) if family(r_["tag"]) == fam and footing(r_["tag"]) == foot]
        r1f = [r_ for r_ in w_frozen["rows"] if family(r_["tag"]) == fam and footing(r_["tag"]) == foot]
        grow1 = sum(1 for r_ in r1 if r_["growing"])
        grow1_sym = sum(1 for r_ in r1 if isinstance(r_["w2_symbol_code"], float) and r_["w2_symbol_code"] < 0)
        grow1f = sum(1 for r_ in r1f if r_["growing"])
        n_tw, n_ok = ka4fam[(fam, foot)]
        reasons = []
        if not all(KA[k] for k in ("item1", "KA3", "KA1_map", "KA2", "KA4_graded_primaries", "KA5_point", "KA5_discs")):
            reasons.append("a graded known answer fails")
        if route1 is None:
            reasons.append("KA1 fails with the A4 fit too: route 1 has no graded reading")
        if fam != "EF_plane" and n_ok < n_tw:
            reasons.append(f"KA4's two-resolution clause fails on {n_tw - n_ok} of {n_tw} backgrounds (magnitudes; the sign agrees on all)")
        if fam == "EF_plane":
            reasons.append("one resolution only (the frozen 3D grid): KA4's two-resolution clause cannot be evaluated")
        stable_r1 = route1 is not None and grow1 == 0 and grow1_sym == 0
        stable_r2 = neg_inertia == 0 and pencil_unstable == 0 and pencil_negative == 0
        growth_r1 = route1 is not None and grow1 > 0
        growth_r2 = neg_inertia > 0
        if not reasons and stable_r1 and stable_r2:
            label = "STABLE"
        elif not reasons and growth_r1 and growth_r2:
            label = "UNSTABLE IN REGIONS"
        else:
            if (growth_r1 or growth_r1 is False) and (stable_r1 != stable_r2) and not (growth_r1 and growth_r2):
                reasons.append("the two routes disagree")
            label = "NO VERDICT"
        reading = ("stable on every route" if (stable_r1 and stable_r2) else
                   "unstable in regions on both routes" if (growth_r1 and growth_r2) else
                   "mixed")
        if fam == "EF_axis" and pencil:
            reasons_note = (f"pencil clears the frozen tolerance (lambda < -1e-10 max|lambda|) on {pencil_unstable} of {len(pencil)} coarse rows; "
                            f"negative on {pencil_negative} of {len(pencil)}; inertia negative on {neg_inertia} of {evaluated}")
        else:
            reasons_note = f"inertia/Rayleigh negative on {neg_inertia} of {evaluated}; pencil negative on {pencil_negative} of {len(pencil)}"
        LAB[(fam, foot)] = dict(label=label, reading=reading, reasons=reasons, route2=reasons_note,
                                route1_A4_growing_rows=grow1, route1_A4_symbol_negative_rows=grow1_sym, route1_A4_rows=len(r1),
                                route1_frozen_growing_rows=grow1f, route1_frozen_rows=len(r1f),
                                ka4_twins_agree=f"{n_ok}/{n_tw}")
        P_(f"[{fam} {foot}] {label}; reading: {reading}; route 1 (A4) growing {grow1}/{len(r1)} (symbol {grow1_sym}), "
           f"frozen fit {grow1f}/{len(r1f)}; route 2: {reasons_note}; KA4 twins {n_ok}/{n_tw}"
           + (f"; reasons: {'; '.join(reasons)}" if reasons else ""))

# ---- MUTATE bites
bites = {}
m2 = {a: json.load(open(os.path.join(HERE, f"scs2_route2_MUTATE_{a}.json")))["rows"] for a in ("M1", "M2", "M3")}
base = {(r_["tag"], r_["m"], r_["parity"]): r_ for r_ in r2}
iso_m1 = [r_ for r_ in m2["M1"] if family(r_["tag"]) == "isolated"]
iso_m2 = [r_ for r_ in m2["M2"] if family(r_["tag"]) == "isolated"]
m1w = J("scs2_wkb_MUTATE_M1_A4.json")["rows"]
main_idx = {(r_["tag"], r_["point"], round(r_["R_kpc"], 6), round(r_["z_kpc"], 6), r_["direction"], r_["kr"]): r_ for r_ in w_a4["rows"]}
turned = [r_ for r_ in m1w if family(r_["tag"]) == "EF_axis"
          and main_idx.get((r_["tag"], r_["point"], round(r_["R_kpc"], 6), round(r_["z_kpc"], 6), r_["direction"], r_["kr"]), {}).get("growing")
          and not r_["growing"]]
was = [r_ for r_ in m1w if family(r_["tag"]) == "EF_axis"
       and main_idx.get((r_["tag"], r_["point"], round(r_["R_kpc"], 6), round(r_["z_kpc"], 6), r_["direction"], r_["kr"]), {}).get("growing")]
iso_w_m1 = [r_ for r_ in m1w if family(r_["tag"]) == "isolated"]
bites["M1"] = dict(route2_isolated_negative=f"{sum(r_['negative_by_inertia'] for r_ in iso_m1)}/{len(iso_m1)}",
                   route1_isolated_growing=f"{sum(r_['growing'] for r_ in iso_w_m1)}/{len(iso_w_m1)}",
                   route1_EF_growing_rows_turned_stable=f"{len(turned)}/{len(was)}",
                   bites=bool(all(r_["negative_by_inertia"] for r_ in iso_m1) and all(r_["growing"] for r_ in iso_w_m1)
                              and len(was) > 0 and len(turned) == len(was)))
iso_w_m2 = [r_ for r_ in J("scs2_wkb_MUTATE_M2_A4.json")["rows"] if family(r_["tag"]) == "isolated"]
bites["M2"] = dict(route2_isolated_negative=f"{sum(r_['negative_by_inertia'] for r_ in iso_m2)}/{len(iso_m2)}",
                   route1_isolated_growing=f"{sum(r_['growing'] for r_ in iso_w_m2)}/{len(iso_w_m2)}",
                   bites=bool(all(r_["negative_by_inertia"] for r_ in iso_m2)))
ch, flip = [], 0
for r_ in m2["M3"]:
    b = base.get((r_["tag"], r_["m"], r_["parity"]))
    if b and "lambda_min" in b and "lambda_min" in r_:
        ch.append(abs(r_["lambda_min"] / b["lambda_min"] - 1)); flip += int((r_["lambda_min"] < 0) != (b["lambda_min"] < 0))
m3w = J("scs2_wkb_MUTATE_M3_A4.json")["rows"]
ch1, flip1 = [], 0
for r_ in m3w:
    b = main_idx.get((r_["tag"], r_["point"], round(r_["R_kpc"], 6), round(r_["z_kpc"], 6), r_["direction"], r_["kr"]))
    if b and isinstance(r_["w2_symbol_code"], float) and isinstance(b["w2_symbol_code"], float) and b["w2_symbol_code"] != 0:
        ch1.append(abs(r_["w2_symbol_code"] / b["w2_symbol_code"] - 1)); flip1 += int((r_["w2_symbol_code"] < 0) != (b["w2_symbol_code"] < 0))
bites["M3"] = dict(route2_min_change=min(ch) if ch else None, route2_sign_flips=flip, route2_rows=len(ch),
                   route1_min_change=min(ch1) if ch1 else None, route1_sign_flips=flip1, route1_rows=len(ch1),
                   bites=bool(ch and min(ch) >= 1e-3 and flip == 0 and ch1 and min(ch1) >= 1e-3 and flip1 == 0))
for a, b in bites.items():
    P_(f"MUTATE {a}: {'BITES' if b['bites'] else 'DOES NOT BITE'} {json.dumps({k: v for k, v in b.items() if k != 'bites'})}")

RES = dict(lane="SCS2", script="scs2_labels.py", known_answers=KA, labels={f"{k[0]}|{k[1]}": v for k, v in LAB.items()},
           mutate=bites, footer="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, "scs2_labels.json"), "w") as fh:
    json.dump(RES, fh, indent=1)
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, "scs2_labels.out"), "w") as fh:
    fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
