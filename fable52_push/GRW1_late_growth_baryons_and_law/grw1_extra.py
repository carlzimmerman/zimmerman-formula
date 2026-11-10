#!/usr/bin/env python3
"""GRW1 extras, REPORTED ONLY (written after the main run; no label rests on them):
  E1 the step family W at z_w 2 and 0.5 (the frozen W was z_w 3 and 1): cold until z_w, then 1000 km/s, cold initial state;
  E2 the IGM temperature: T-A-max and T-A (canonical) at c_s 1000 with T_IGM 0 (CLASS's own baryon temperature) and 3e4 K;
  E3 the most generous corner: T-A-max at c_s 1000, cold start, no IGM heating.
Usage: python3 grw1_extra.py -> grw1_extra.json / grw1_extra.out. TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grw1_lib as GL
import grw1_run as GR

GR.OUT.clear(); GR.RES["runs"].clear(); GR.RES["tag"] = "grw1_extra"; GR.RES["mutate"] = None
GR.RES["note_extra"] = "REPORTED ONLY, written after the main run; no label rests on these rows"
P = GR.P
P("GRW1 extras (reported only).")
for zw in (2.0, 0.5):
    c = GL.step_cs(1000.0, zw)
    o = GR.cached(f"EXTRA_W_TAmax_zw{zw:g}", lambda: GL.Run(GR.bgref, "TAmax", 1.0, c, GR.icref).solve()); GR.record(f"EXTRA_W_TAmax_zw{zw:g}", o, "TAmax")
    for f in GR.FOOT:
        o = GR.cached(f"EXTRA_W_TA_{f}_zw{zw:g}", lambda: GL.Run(GR.bgref, "TA", GL.A0[f], c, GR.icref).solve()); GR.record(f"EXTRA_W_TA_{f}_zw{zw:g}", o, "TA")
    o = GR.cached(f"EXTRA_W_off_zw{zw:g}", lambda: GL.Run(GR.bgref, "off", 1.0, c, GR.icref).solve()); GR.record(f"EXTRA_W_off_zw{zw:g}", o, "off")
M = GL.run_class(1000.0); ic = GL.transfer_ic(M, GL.ZSTART, "d_fld")
for T in (0.0, 3.0e4):
    bg = GL.Background(M); bg.cIGM *= T / GL.T_IGM
    c = GL.const_cs(1000.0)
    o = GR.cached(f"EXTRA_TIGM{T:.0f}_TAmax_cs1000", lambda: GL.Run(bg, "TAmax", 1.0, c, GR.icref).solve()); GR.record(f"EXTRA_TIGM{T:.0f}_TAmax_cs1000", o, "TAmax", cs=1000.0)
    o = GR.cached(f"EXTRA_TIGM{T:.0f}_TA_canonical_cs1000", lambda: GL.Run(bg, "TA", GL.A0["canonical"], c, ic).solve())
    GR.record(f"EXTRA_TIGM{T:.0f}_TA_canonical_cs1000", o, "TA", GL.A0["canonical"], 1000.0)
P("E3 = EXTRA_TIGM0_TAmax_cs1000 (cold start, c = 1, no IGM heating): the most generous corner computed.")
P(f"({time.time() - GR.T0:.0f} s)"); P(GR.GO.kappa_note)
json.dump(GR.RES, open(os.path.join(HERE, "grw1_extra.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "grw1_extra.out"), "w").write("\n".join(GR.OUT) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
