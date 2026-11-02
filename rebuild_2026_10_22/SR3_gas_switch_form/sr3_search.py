#!/usr/bin/env python3
"""SR3 search. sr3_search.py <job> <foot> <tier> <path>: job real|scrambled|planted|label; tier T0|T1F|T1FY; path free|fixed. Writes hof_<tag>.csv. A killed job restarts from scratch. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys, time
os.environ["JULIA_NUM_THREADS"] = "1"; os.environ["PYTHON_JULIACALL_THREADS"] = "1"; os.environ["PYTHON_JULIACALL_HANDLE_SIGNALS"] = "yes"
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
os.nice(19)
import numpy as np
import sr3_core as K
job, foot, tier, path = sys.argv[1:5]; NIT = int(os.environ.get("SR3_NIT", 300)); SUF = os.environ.get("SR3_SUF", ""); tag = f"{job}_{foot}_{tier}_{path}{SUF}"; HERE = K.HERE; F = os.path.join(HERE, "fronts", f"hof_{tag}.csv"); os.makedirs(os.path.dirname(F), exist_ok=True)
if os.path.exists(F): print(tag, "done"); sys.exit(0)
P = K.prep(job, foot); fixed = path == "fixed"; T = K.search_table(P, fixed); S = T["S"]; nS = len(S)
def feats(f, y): return np.column_stack([f, y, f * y, (1 - f) * y, np.ones_like(f), 2 * np.ones_like(f), np.pi * np.ones_like(f)])
X = np.vstack([feats(S[:, 0], S[:, 1]), feats(T["Xf"], T["Xy"])]); nX = len(T["Xf"])
pf, py = np.meshgrid([.1, .3, .5, .7, .9, 1.0], [1e6, 1e8, 1e10, 1e12]); PR = feats(pf.ravel(), py.ravel())
B = os.path.join(HERE, "bin", tag); os.makedirs(B, exist_ok=True)
tb = dict(lgO=S[:, 2], lgL=S[:, 3], W=S[:, 4], gid=S[:, 5] + 1, uid=S[:, 6] + 1, Xd=T["Xd"], PR=PR.ravel())
for k, v in tb.items(): np.asarray(v, float).tofile(os.path.join(B, k + ".bin"))
from pysr import PySRRegressor
from pysr.julia_import import jl
LU = list(np.log10(K.GRID)) if not fixed else [0.0]
jl.seval(f'''
module SR3D
rd(n,l) = (a=Vector{{Float64}}(undef,l); read!(joinpath({json.dumps(B)},n*".bin"),a); a)
const nS={nS}; const nX={nX}; const lgO=rd("lgO",nS); const lgL=rd("lgL",nS); const W=rd("W",nS); const gid=Int.(rd("gid",nS)); const uid=Int.(rd("uid",nS)); const Xd=rd("Xd",nX); const PR=reshape(rd("PR",7*{len(PR)}),7,{len(PR)}); const ng={T["ng"]}; const LU={LU}; const nu=length(LU)
const FIXED={str(fixed).lower()}; const T1={str(tier != "T0").lower()}; const TY={str(tier == "T1FY").lower()}
const LO=log10(0.5); const HI=log10(0.8)
end
''')
jl.seval('sr3_nc(n) = n.degree == 0 ? Int(n.constant) : (n.degree == 1 ? sr3_nc(n.l) : sr3_nc(n.l) + sr3_nc(n.r))')
jl.seval(f'''
function sr3_loss(tree, dataset::Dataset{{T,L}}, options)::L where {{T,L}}
    D = Main.SR3D; bad = L(1e12)
    if sr3_nc(tree) > 2; return bad; end
    p, ok = eval_tree_array(tree, dataset.X, options); ok || return bad
    X = dataset.X; n = D.nS + D.nX
    A = zeros(Float64, D.ng, D.nu); B = zeros(Float64, D.ng, D.nu)
    a = 0.0; b = 0.0
    @inbounds for i in 1:D.nS
        H = D.T1 ? 1 + X[1,i]*p[i] : p[i]; H > 0 || return bad; r = D.lgO[i]-D.lgL[i]-log10(H)
        if D.FIXED; a += r*r; b += 1.0; else; A[D.gid[i],D.uid[i]] += D.W[i]*r*r; B[D.gid[i],D.uid[i]] += D.W[i]; end
    end
    xs = 0.0; xq = 0.0
    @inbounds for j in 1:D.nX
        i = D.nS+j; H = D.T1 ? 1 + X[1,i]*p[i] : p[i]; H > 0 || return bad; d = D.Xd[j]-log10(H); xs += d; xq += d*d
    end
    xm = xs/D.nX; xr2 = xq/D.nX
    pen = 0.0
    if D.FIXED
        out = a/b/{K.FIX_LINE}^2
    else
        U = zeros(Float64, D.ng)
        @inbounds for g in 1:D.ng
            best = Inf; bu = 1
            for u in 1:D.nu
                if B[g,u] > 0; q = A[g,u]/B[g,u]; if q < best; best = q; bu = u; end; end
            end
            a += A[g,bu]; b += B[g,bu]; U[g] = D.LU[bu]
        end
        sort!(U); m = iseven(D.ng) ? 0.5*(U[D.ng÷2]+U[D.ng÷2+1]) : U[(D.ng+1)÷2]
        dd = m < D.LO ? D.LO-m : (m > D.HI ? m-D.HI : 0.0); pen = (dd/0.05)^2
        out = a/b/{K.L_S}^2
    end
    out += xm^2/{K.L_XM}^2 + xr2/{K.L_XR}^2 + pen
    if D.TY
        q, ok2 = eval_tree_array(tree, convert(Matrix{{T}}, D.PR), options); ok2 || return bad
        mx = 0.0
        @inbounds for k in 1:size(D.PR,2)
            H = 1 + D.PR[1,k]*q[k]; H > 0 || return bad; mx = max(mx, abs(log10(H)))
        end
        if mx > 1e-3; out += 100*mx^2; end
    end
    return L(out)
end
''')
t0 = time.time(); O = os.path.join(HERE, "pysr_runs", tag); os.makedirs(O, exist_ok=True)
m = PySRRegressor(niterations=NIT, populations=12, population_size=33, maxsize=25, maxdepth=10, binary_operators=["+", "-", "*", "/"], unary_operators=["exp", "log1p", "sqrt", "square"], nested_constraints={"exp": {"exp": 0, "log1p": 1}, "log1p": {"log1p": 0, "exp": 1}, "sqrt": {"sqrt": 0}}, complexity_of_constants=1, loss_function="sr3_loss", precision=64, parallelism="serial", deterministic=True, random_state=K.SEED, progress=False, verbosity=0, output_directory=O, run_id="r", procs=0)
m.fit(X, np.zeros(len(X)), variable_names=["f", "y", "yg", "ys", "one", "two", "pii"]); H = m.equations_
tmp = F + ".tmp"; H[["complexity", "loss", "equation"]].to_csv(tmp, index=False); os.replace(tmp, F); json.dump(dict(tag=tag, seconds=time.time() - t0, nit=NIT, rows=len(X), ng=T["ng"]), open(F.replace(".csv", ".json"), "w"), indent=1); print(tag, "finished", time.time() - t0, flush=True)
