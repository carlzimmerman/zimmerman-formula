# VERIFY both ways: fit the dS-Unruh FLOOR law g_obs=sqrt(gb^2 + 2 gb cH) to SPARC.
# Q: does the best-fit FLOOR scale cH come out at ~a0/2 (=> a0_eff=2cH=a0=9.36e-11, WAY 2),
#    or at cH=Z a0=5.4e-10 (=> a0_eff=11.6 a0, WAY 1)? Whichever galaxies pick is the truth.
import numpy as np, glob, os
c, Mpc, kpc = 2.99792458e8, 3.0857e22, 3.0857e19
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
A0_FRAME = 9.3612e-11; Z = 5.789
ML_D, ML_B = 0.5, 0.7
gb, go, w = [], [], []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try: d = np.genfromtxt(f, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    Rm = R*kpc; Vbar2 = np.sign(Vgas)*Vgas**2 + ML_D*Vdisk**2 + ML_B*Vbul**2
    g_b = Vbar2*1e6/Rm; g_o = (Vobs*1e3)**2/Rm
    ok = (g_b>0)&(g_o>0)&np.isfinite(g_b)&np.isfinite(g_o)&(Vobs>0)
    fr = np.clip(eV,1,None)/np.clip(Vobs,1,None)
    gb += list(g_b[ok]); go += list(g_o[ok]); w += list(1/fr[ok]**2)
gb, go, w = np.array(gb), np.array(go), np.array(w)

# FLOOR law: g_obs = sqrt(gb^2 + 2 gb cH); fit cH (scan), report a0_eff=2cH
floor = lambda gb, cH: np.sqrt(gb**2 + 2*gb*cH)
grid_cH = np.linspace(0.1e-10, 8e-10, 1600)
s = [np.sqrt(np.sum(w*(np.log10(go)-np.log10(floor(gb,ch)))**2)/np.sum(w)) for ch in grid_cH]
i = int(np.argmin(s))
cH_best = grid_cH[i]
print(f"FLOOR law fit to 175 SPARC (Upsilon 0.5/0.7, err-weighted):")
print(f"  best-fit cH      = {cH_best:.3e}  scatter {s[i]:.3f} dex")
print(f"  => a0_eff = 2 cH = {2*cH_best:.3e}  ({2*cH_best/A0_FRAME:.3f} a0_FRAME)")
print(f"  framework floor cH_Lambda = Z a0 = {Z*A0_FRAME:.3e}  ({Z:.2f} a0)")
print(f"  ratio best-fit cH / cH_Lambda = {cH_best/(Z*A0_FRAME):.3f}")
# What scatter if we FORCE cH = cH_Lambda = Z a0 (WAY 1)?
s_way1 = np.sqrt(np.sum(w*(np.log10(go)-np.log10(floor(gb, Z*A0_FRAME)))**2)/np.sum(w))
print(f"\n  FORCING cH = Z a0 = 5.4e-10 (WAY 1, floor-as-extra-scale): scatter = {s_way1:.3f} dex")
print(f"  best (cH free):                                            scatter = {s[i]:.3f} dex")
print(f"  => WAY 1 costs {s_way1 - s[i]:+.3f} dex ({s_way1/s[i]:.1f}x the optimal scatter).")
