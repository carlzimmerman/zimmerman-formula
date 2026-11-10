"""SCS3 reported check (not graded, added after the A4 label pass): a point baryonic mass in the same uniform external field
(SCS2's 'point' deposit: all mass inside r_min; axisymmetric, A1 mask), log M_b 9.4 and 10.9, 0.01 and 0.1 a0, both footings,
AX resolutions R0-R5, route L as in scs3_maps.py.  A point mass in a uniform field is symmetric about the field, so its
answer does not depend on the field's direction relative to a disc: if the discs' route-L rates equal the point mass's, the
axial and in-plane families are the same problem at r ~ r_e.  TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.update(SCS3_SET="X", SCS3_A1="1")
import scs3_maps as m
S = m.S
out = dict(lane="SCS3", script="scs3_pointmass.py", rows={})
ax = {}
for f in ("scs3_maps_AX_A4.json",):
    ax.update(json.load(open(os.path.join(HERE, f)))["rows"])
pl = {}
for f in ("scs3_maps_PL_A2.json", "scs3_maps_PL_A2_mmd.json"):
    pl.update(json.load(open(os.path.join(HERE, f)))["rows"])
for foot in ("canonical", "alt"):
    for lm in ("9.4", "10.9"):
        for ge in (0.01, 0.1):
            d = dict(group="POINT", foot=foot, kind="point", logm=lm, ge=ge, axis="z")
            for res in range(6):
                bg = S.background(foot, "point", lm, ge=ge, axis="z", res=res); m.a1_mask(bg, d)
                L = m.route_L(bg, "point")["L"]
                t = m.tag_of(d, res)
                cmp = {}
                for kind in ("expo", "kuzmin"):
                    k = f"AX_{foot}_{kind}_{lm}_{ge}_z_R{res}".replace(".", "p")
                    if k in ax:
                        cmp[f"AX_{kind}"] = ax[k]["routeL"]["L"]["efold_gyr"]
                    kp = f"PL_{foot}_{kind}_{lm}_{ge}_x_R{res}".replace(".", "p")
                    if kp in pl:
                        cmp[f"PL_{kind}"] = pl[kp]["routeL"]["L"]["efold_gyr"]
                row = dict(efold_gyr=L["efold_gyr"], r_over_re=L["r_over_re"], theta_deg=L["theta_deg"], discs=cmp,
                           max_rel_disc_vs_point=max(abs(v / L["efold_gyr"] - 1) for v in cmp.values()) if cmp else None)
                out["rows"][t] = row
                print(t, round(L["efold_gyr"], 4), round(L["r_over_re"], 3), round(L["theta_deg"], 1),
                      {k_: round(v, 4) for k_, v in cmp.items()}, row["max_rel_disc_vs_point"], flush=True)
out["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
json.dump(out, open(os.path.join(HERE, "scs3_pointmass.json"), "w"), indent=1)
