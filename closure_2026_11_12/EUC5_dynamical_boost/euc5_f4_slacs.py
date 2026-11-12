#!/usr/bin/env python3
"""EUC5 check F4 (POST HOC, added after A1's DESI dispersions and the frozen SDSS ones were seen to disagree).

Is the A1 fitter right on real early-type spectra of good signal-to-noise?  It is run, unchanged, on the public SDSS
DR17 spectra of SLACS lenses (NOIRLab SPARCL), whose velocity dispersions are published (Auger et al. 2009, the table
EUC1 and EUC5 already use).  Reported: fitted / published.

Run:  python3 -I euc5_f4_slacs.py --templates <E-MILES fits dir> --cache <dir for the spectra, outside git> [--n 30]
"""
import argparse, csv, json, math, os, sys, time
import numpy as np
import requests
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc5_a1_fit as FIT
E = FIT.E
API = "https://astrosparcl.datalab.noirlab.edu/api"
UA = {"User-Agent": "generic-client", "Content-Type": "application/json"}

def post(url, payload, tries=8):
    for k in range(tries):
        time.sleep(2.0)
        try:
            r = requests.post(url, json=payload, headers=UA, timeout=180)
            if r.status_code == 200: return r.json()
            if r.status_code == 429: time.sleep(90.0)
        except Exception:
            pass
        time.sleep(5.0 * (k + 1))
    raise RuntimeError("request failed")

def sex(s, hours):
    p = s.replace(":", " ").split(); sg = -1.0 if p[0].startswith("-") else 1.0
    v = abs(float(p[0])) + float(p[1]) / 60.0 + float(p[2]) / 3600.0
    return sg * v * (15.0 if hours else 1.0)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--templates", required=True); ap.add_argument("--cache", required=True); ap.add_argument("--n", type=int, default=30)
    a = ap.parse_args(); os.makedirs(a.cache, exist_ok=True); out = []
    def P(s=""):
        print(s, flush=True); out.append(s)
    path = os.path.join(E.REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]
    hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]; hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}
    SL = []
    for l in lines[hi + 3:]:
        q = l.split("\t")
        if len(q) < len(hdr) or not q[col["sigma"]].strip(): continue
        try:
            SL.append(dict(name=q[col["SDSS"]].strip(), z=float(q[col["zlens"]]), sig=float(q[col["sigma"]]), esig=float(q[col["e_sigma"]]),
                           ra=sex(q[col["RAJ2000"]], True), dec=sex(q[col["DEJ2000"]], False)))
        except Exception:
            continue
    SL = SL[:a.n]
    F = FIT.Fitter(a.templates); FIT.DEGREE, FIT.MDEGREE = 8, 0
    P("EUC5 F4 (post hoc): the A1 fitter on SDSS DR17 spectra of %d SLACS lenses with published dispersions" % len(SL))
    R = 1.5 / 3600.0; res = []
    for d in SL:
        fp = os.path.join(a.cache, d["name"] + ".npz")
        if not os.path.exists(fp):
            dra = R / math.cos(math.radians(d["dec"]))
            found = post(API + "/find/?limit=20", dict(outfields=["sparcl_id", "ra", "dec", "redshift", "specprimary", "data_release"],
                         search=[["data_release", "SDSS-DR17", "BOSS-DR17"], ["ra", d["ra"] - dra, d["ra"] + dra], ["dec", d["dec"] - R, d["dec"] + R]]))[1:]
            found = [f for f in found if abs(f["redshift"] - d["z"]) < 0.01]
            if not found: continue
            f0 = sorted(found, key=lambda f: (not f["specprimary"], f["data_release"] != "SDSS-DR17"))[0]
            rec = post(API + "/spectras/?include=sparcl_id,flux,ivar,wavelength,mask,wave_sigma&format=json&dataset_list=%s" % f0["data_release"], [f0["sparcl_id"]])[1]
            np.savez_compressed(fp, wavelength=np.array(rec["wavelength"], float), flux=np.array(rec["flux"], np.float32), ivar=np.array(rec["ivar"], np.float32),
                                wave_sigma=np.array(rec["wave_sigma"], np.float32), release=f0["data_release"])
        sp = np.load(fp); wl = sp["wavelength"].astype(float)
        # SDSS spectra are on a log-lambda grid: resample onto a linear grid (the fitter assumes one), 1.0 A
        lin = np.arange(wl[0], wl[-1], 1.0); ivr = sp["ivar"].astype(float)
        fl = np.interp(lin, wl, sp["flux"].astype(float)); iv = np.interp(lin, wl, ivr) * np.interp(lin, wl, np.gradient(wl)) / 1.0
        iv = np.where(np.interp(lin, wl, (ivr > 0).astype(float)) > 0.99, iv, 0.0)
        ws = np.interp(lin, wl, sp["wave_sigma"].astype(float))
        if np.nanmedian(ws[ws > 0]) < 3.0 and np.nanmedian(ws[(lin > 8000) & (ws > 0)]) < 1.25 * np.nanmedian(ws[(lin < 4500) & (ws > 0)]):
            ws = ws * 1.0e-4 * math.log(10.0) * lin          # looks like pixel units (dloglam = 1e-4): convert to Angstrom
        r = FIT.Fitter.fit(F, lin, fl, iv, np.zeros(len(lin), int), ws, d["z"])
        if r is None or not np.isfinite(r["sigma"]): continue
        res.append(dict(name=d["name"], pub=d["sig"], epub=d["esig"], fit=r["sigma"], efit=r["err"], snr=r["snr"], s_ins=r["s_ins"]))
        P("  %-12s published %3.0f +- %2.0f   fitted %5.1f +- %4.1f   ratio %.3f   S/N %.0f   sigma_inst %.0f km/s" % (d["name"], d["sig"], d["esig"], r["sigma"], r["err"], r["sigma"] / d["sig"], r["snr"], r["s_ins"]))
    rat = np.array([r["fit"] / r["pub"] for r in res])
    P("F4: %d lenses; fitted / published median %.3f, mean %.3f, scatter %.3f; median S/N %.0f per pixel"
      % (len(res), np.median(rat), rat.mean(), rat.std(), np.median([r["snr"] for r in res])))
    json.dump(dict(n=len(res), median=float(np.median(rat)), mean=float(rat.mean()), sd=float(rat.std()), rows=res), open(os.path.join(HERE, "euc5_f4_slacs.json"), "w"), indent=1)
    open(os.path.join(HERE, "euc5_f4_slacs.out"), "w").write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
