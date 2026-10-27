"""Post-result A2: same-radius baryonic binding/circular-speed proxy C6R.

r*=sqrt(G M_catalog/a0) is a reference radius, not necessarily g_N=a0 for
extended profiles. Numerator is Newtonian baryonic binding speed; denominator
is the law's circular speed computed from M_b(<r*) at the SAME radius.
This is not escape speed in the infinite isolated-law potential.
"""
import copy
import contextlib
import io
import itertools
import json
import math


def beta_mass(radius, scale):
    x = radius/scale
    return scale**3*(x-math.atan(x))


def beta_potential_mass(radius, scale, norm, cutoff, G):
    r = min(radius, cutoff)
    menc = norm*beta_mass(r, scale)
    outer = 0.5*norm*scale**2*math.log((1+(cutoff/scale)**2)/(1+(r/scale)**2))
    return G*(menc/radius+outer), menc


def lens_potential_mass(radius, compact_mass, hot_mass, hot_radius, G):
    menc = compact_mass+hot_mass*min(1.0, (radius/hot_radius)**3)
    phi_hot = (G*hot_mass*(3*hot_radius**2-radius**2)/(2*hot_radius**3)
               if radius < hot_radius else G*hot_mass/radius)
    return G*compact_mass/radius+phi_hot, menc


def binding_ratio(catalog_mass, a0, profile, G=6.674e-11, **params):
    if catalog_mass <= 0 or a0 <= 0 or G <= 0:
        raise ValueError("positive mass, a0 and G required")
    radius = math.sqrt(G*catalog_mass/a0)
    if profile == "point":
        phi, menc = G*catalog_mass/radius, catalog_mass
    elif profile == "plummer":
        scale = params["scale"]
        phi = G*catalog_mass/math.sqrt(radius**2+scale**2)
        menc = catalog_mass*radius**3/(radius**2+scale**2)**1.5
    elif profile == "beta":
        phi, menc = beta_potential_mass(radius, params["scale"], params["norm"], params["cutoff"], G)
    elif profile == "lens":
        phi, menc = lens_potential_mass(radius, params["compact_mass"], params["hot_mass"], params["hot_radius"], G)
    else:
        raise ValueError(profile)
    gb = G*menc/radius**2
    glaw = 0.5*(gb+math.sqrt(gb*gb+4*gb*a0))
    return math.sqrt(2*phi/(glaw*radius)), radius, phi, menc


def interval(values, strict=False):
    import numpy as np
    logs = np.log10(values)
    return [float(np.min(logs) if strict or len(logs)<3 else np.percentile(logs, 16)),
            float(np.max(logs) if strict or len(logs)<3 else np.percentile(logs, 84)),
            float(np.median(logs)), len(logs)]


def separation(table, labels, key):
    names = [c for c in table if labels.get(c) in ("RETAIN", "EXCLUDED")]
    if any(table[c][key] is None for c in names):
        return dict(separates=False, complete=False)
    r = [table[c][key] for c in names if labels[c] == "RETAIN"]
    e = [table[c][key] for c in names if labels[c] == "EXCLUDED"]
    up = min(v[0] for v in r)-max(v[1] for v in e)
    down = min(v[0] for v in e)-max(v[1] for v in r)
    margin = max(up, down)
    return dict(separates=margin>0, complete=True, best_gap_dex=margin,
                direction="UP" if up >= down else "DOWN")


def enumerate_null(table, labels, keys):
    names = [c for c in table if labels.get(c) in ("RETAIN", "EXCLUDED")]
    ne = sum(labels[c] == "EXCLUDED" for c in names)
    nk = dict.fromkeys(keys, 0); count = any_count = 0
    for exc in itertools.combinations(names, ne):
        lab = {c: "EXCLUDED" if c in exc else "RETAIN" for c in names}
        hits = {k: separation(table, lab, k)["separates"] for k in keys}
        count += 1; any_count += any(hits.values())
        for k in keys:
            nk[k] += int(hits[k])
    return dict(total=count, any_count=any_count, p_any=any_count/count,
                per_candidate={k: nk[k]/count for k in keys})


def calculate(root):
    import numpy as np
    lane = root/"rebuild_2026_10_22/X64_oblique_object_keys"
    historical = json.loads((lane/"x64_oblique_keys_results.json").read_text())
    source_path = lane/"x64_oblique_keys.py"
    source = source_path.read_text()
    # This exact historical prefix rebuilds X19, checks its table, and reconstructs
    # members/lenses. It ends before CLASS/EPS and before ALL output writes.
    prefix = source[:source.index("# =====================================================================================  EPS machinery")]
    ns = {"__file__": str(source_path), "__name__": "x64_members_read_only"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(prefix, str(source_path), "exec"), ns)
    if ns["STOP"] or not ns["CHECKS"]["K0"]["ok"] or not ns["CHECKS"]["K1"]["ok"]:
        raise RuntimeError("Historical member reconstruction checks failed")
    members, G, MSUN, MPC = (ns[k] for k in ("MEM", "G", "MSUN", "MPC"))
    lenses = {v["bin"]: v for v in ns["LENS"]}
    x19 = ns["NS"]
    records = {}; new_intervals = copy.deepcopy(historical["class_intervals_log10"])
    history_max = 0.0
    for f, classes in members.items():
        records[f] = {}
        for c, rows in classes.items():
            rr = []; oldvalues = []
            for m in rows:
                params = {}; profile = "point"
                if c in ns["PRESS"]:
                    profile = "plummer"; params["scale"] = 0.75*m["r"]
                elif c.startswith("Clusters"):
                    row = x19["EF"][x19["EIDX"][m["name"]]]
                    r500 = float(row["R500"])/1000*MPC; scale = 0.15*r500
                    profile = "beta"
                    params = dict(scale=scale, norm=m["Mb"]*MSUN/beta_mass(r500, scale), cutoff=3*MPC)
                elif c == "KiDS lenses":
                    lens = lenses[int(m["name"].split("@")[0][3:])]
                    profile = "lens"
                    params = dict(compact_mass=(lens["Ms"]+lens["Mc"])*MSUN, hot_mass=lens["Mh"]*MSUN, hot_radius=0.1*MPC)
                value, radius, phi, menc = binding_ratio(m["Mb"]*MSUN, ns["A0"][f], profile, G=G, **params)
                oldvalue = math.sqrt(2*m["phi_int"]*ns["CL"]**2/(ns["A0"][f]*radius*((1+math.sqrt(5))/2)))
                oldvalues.append(oldvalue)
                rr.append(dict(name=m["name"], profile=profile, value=value, historical_value=oldvalue,
                               reference_radius_kpc=radius/(MPC/1000), catalogue_radius_kpc=m["r"]/(MPC/1000),
                               phi_N_m2_s2=phi, enclosed_baryon_mass_Msun=menc/MSUN,
                               catalog_mass_Msun=m["Mb"], lens_r_mpc=m.get("r_mpc")))
            records[f][c] = rr
            old_iv = interval(oldvalues)
            saved = historical["class_intervals_log10"][f][c]["vesc_vc"]
            history_max = max(history_max, max(abs(a-b) for a,b in zip(old_iv[:3], saved[:3])))
            if old_iv[3] != saved[3]:
                raise RuntimeError("Historical member count changed")
            new_intervals[f][c]["vesc_vc"] = interval([r["value"] for r in rr])
    if history_max > 1e-9:
        raise RuntimeError(f"Historical C6 reconstruction mismatch {history_max}")
    keys = ["Q_b", "Q_dyn", "vir", "tcross", "trelax", "fbSigma_law", "dynage", "vesc_vc"]
    labels = historical["labels_P"]
    out = dict(correction="X64 post-result A2 C6R", definition="sqrt(2 |Phi_N(r*)| / [g_law(r*) r*]); r*=sqrt(G M_catalog/a0)",
               reference_radius_is_not_actual_transition_for_extended_profiles=True,
               historical_c6_reconstruction_max_abs_log10=history_max,
               historical_c6_verdict=historical["verdict"], footings={}, members=records,
               class_intervals_log10=new_intervals, labels_P=labels,
               inherited_candidate_keys=[k for k in keys if k != "vesc_vc"],
               non_claims=["Not escape speed in the infinite isolated-law potential", "No halo or environment potential added",
                           "Only the frozen eight scalar candidates with a one-sided threshold are graded",
                           "Relabelling frequency is a null statistic, not statistical power",
                           "Seven other candidate inputs/results are inherited, not revalidated here"])
    for f, table in new_intervals.items():
        result = {k: separation(table, labels, k) for k in keys}
        null = enumerate_null(table, labels, keys)
        qualifiers = {}
        for scheme in ("P", "G", "W", "strict", "lens_r0.104"):
            ll = dict(labels); tt = copy.deepcopy(table)
            if scheme == "G":
                for c in ("Groups", "Clusters T1"): ll[c] = "-"
            if scheme == "W":
                ll["MW classical"] = "RETAIN"
                for c in ("UMa members", "TDGs", "DF2/DF4", "Crater II"): ll[c] = "EXCLUDED"
            if scheme == "strict":
                for c in tt: tt[c]["vesc_vc"] = interval([r["value"] for r in records[f][c]], strict=True)
            if scheme == "lens_r0.104":
                tt["KiDS lenses"]["vesc_vc"] = interval([r["value"] for r in records[f]["KiDS lenses"] if r["lens_r_mpc"] == 0.104])
            qualifiers[scheme] = separation(tt, ll, "vesc_vc")
        out["footings"][f] = dict(results=result, null_relabelling=null, C6R_qualifiers=qualifiers,
                                  separating_candidates=[k for k,v in result.items() if v["separates"]])
    out["verdict"] = ("NO SEPARATING KEY IN THE EIGHT TESTED SCALAR CANDIDATES" if not any(
        v["separating_candidates"] for v in out["footings"].values()) else "SEPARATION FOUND; PHYSICAL FOLLOW-UP UNRESOLVED")
    return out
