"""LAM3: train LAM2's B and S once on all 2352 LAM2 gas-poor graded galaxies (no folds) and save them, before any SAMI value
(criteria d5c434a268). Reuses lam2_grade.py's data block verbatim by exec. Run: python3 -I lam3_freeze_models.py"""
import os, sys, pickle, hashlib, json
HERE = os.path.dirname(os.path.abspath(__file__)); L2 = os.path.join(os.path.dirname(HERE), "LAM2_gas_poor_lambda_estimator")
sys.argv = ["lam2_grade.py"]; src = open(os.path.join(L2, "lam2_grade.py")).read().split("# ---- K1")[0]
G = {"__file__": os.path.join(L2, "lam2_grade.py"), "__name__": "lam2"}; exec(compile(src, "lam2_grade.py", "exec"), G)
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
sel = G["finite"](G["B"] + G["POP"] + G["SH"], G["poor"] & G["fitok"]); print("training galaxies", int(sel.sum()), "slow", int(G["slow"][sel].sum()))
out = {}
for name, cols in (("B", G["B"]), ("S", G["B"] + G["SH"])):
    Z = np.c_[[G["X"][k][sel] for k in cols]].T; sc = StandardScaler().fit(Z)
    m = MLPRegressor((128, 128), activation="logistic", solver="adam", early_stopping=True, validation_fraction=0.1,
                     max_iter=2000, random_state=G["SEED"]).fit(sc.transform(Z), G["lam"][sel])
    fn = os.path.join(HERE, f"lam3_model_{name}.pkl"); pickle.dump(dict(cols=cols, scaler=sc, model=m), open(fn, "wb"))
    out[name] = dict(cols=cols, sha256=hashlib.sha256(open(fn, "rb").read()).hexdigest(), n_iter=int(m.n_iter_))
    print(name, out[name])
json.dump(dict(n_train=int(sel.sum()), sklearn="1.5.2", **out), open(os.path.join(HERE, "lam3_models.json"), "w"), indent=1)
