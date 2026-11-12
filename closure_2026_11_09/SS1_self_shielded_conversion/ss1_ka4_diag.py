"""SS1 KA4 diagnostic (post-run, reported, not graded): CLASS dcdm vs the lane's ratio method at LD1's uniform decay (canonical, QX15 h),
per L and per (k, z), plus the background check. kappa = 1/2 FITTED; not theory closed."""
import os, sys, runpy, json, math, numpy as np
sys.argv=["ss1_cosmo.py"]; os.environ["SS1_FOOT"]="canonical"
src=open("ss1_cosmo.py").read(); cut=src.index("# ================================================================== run")
ns={"__file__":os.path.abspath("ss1_cosmo.py"),"__name__":"x"}; exec(compile(src[:cut],"ss1c","exec"),ns)
L1=ns["LD1J"]["footings"]["canonical"]; gam=L1["Gamma_kmsMpc"]; Q3=ns["Q3"]; Class=ns["Class"]; BASE=ns["BASE"]
p=dict(BASE, omega_cdm=1e-7, omega_ini_dcdm=ns["OD"], Gamma_dcdm=gam); p['output']='tCl,lCl,mPk'
Mx=Class(); Mx.set(p); Mx.compute(); Xd=Q3["X_of"](Mx)
# ratio-method pieces
lifetime=977.792/gam
# reuse S_uniform_bg by exec of its definition
blk=src[src.index("    def S_uniform_bg(h):"):src.index("    Lu, _, _ = lens_eval")]
import textwrap; exec(textwrap.dedent(blk), ns | {"lifetime":lifetime}, loc:={})
bg=loc["S_uniform_bg"](ns["H_REF"]); 
g=ns["growth_source"](bg); Rz=g["src"]/ns["GREF"]["src"]; Rkz=np.tile(Rz,(len(ns["KG"]),1)); S=ns["limber4_bg"](bg,Rkz)
X0=ns["X0"]
for L in (8,10,20,40,70,100,200,300,400): print(L, "CLASS ratio %.4f  method %.4f"%(Xd[L]/X0[L], S[L]))
# matter power ratio at z=0.5, 1, 2 and k 0.01, 0.1
for z in (0.0,0.5,1.0,2.0):
  for k in (0.001,0.01,0.1):
    r=Mx.pk_lin(k,z)/ns["M"].pk_lin(k,z)
    print("z",z,"k",k,"P_CLASS_dcdm/P_ref %.4f"%r, "my (dm ratio)^2 %.4f"%(np.interp(z,ns["ZG"],g["dm"]/ns["GREF"]["dm"])**2), "src^2 %.4f"%np.interp(z,ns["ZG"],Rz**2))
print("S today", bg["S"][0], "H0", Mx.Hubble(0)*299792.458, "Omega_dcdm today CLASS", Mx.get_background()['(.)rho_dcdm'][-1]/Mx.get_background()['(.)rho_crit'][-1])
for z in (0.5,1.0,2.0): print("H ratio CLASS/mine at z",z, Mx.Hubble(z)*299792.458/np.interp(z,bg["z"],bg["H"]), " DA ratio", Mx.angular_distance(z)*(1+z)/np.interp(z,bg["z"],bg["DM"]))
