"""LAM2 wave 1: DR17 spec-lite files for lam2_sample.csv (owner approved). Resumable. Run: python3 -I lam2_get_spectra.py"""
import os, time, urllib.request, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "_external_data")
OUTD = os.path.join(EXT, "lam2_spectra_2026_11_03"); os.makedirs(OUTD, exist_ok=True)
r2 = dict(l.strip().split(",") for l in open(os.path.join(EXT, "lam2_sdss_lines_2026_11_03", "run2d.csv")).readlines()[1:])
a = np.loadtxt(os.path.join(HERE, "lam2_sample.csv"), delimiter=",", skiprows=1, dtype=str); tot = n_ok = 0
for sid, pl, mj, fb in a[:, 1:5]:
    pl, mj, fb = int(pl), int(mj), int(fb); fn = os.path.join(OUTD, f"spec-{pl:04d}-{mj}-{fb:04d}.fits")
    if os.path.exists(fn) and os.path.getsize(fn) > 10000: n_ok += 1; tot += os.path.getsize(fn); continue
    run = r2[sid]; base = "sdss/spectro/redux/26" if run == "26" else f"eboss/spectro/redux/{run}"
    url = f"https://data.sdss.org/sas/dr17/{base}/spectra/lite/{pl:04d}/spec-{pl:04d}-{mj}-{fb:04d}.fits"
    for t in range(4):
        try: b = urllib.request.urlopen(url, timeout=60).read(); open(fn + ".part", "wb").write(b); os.replace(fn + ".part", fn); break
        except Exception as e: print("retry", url, e, flush=True); time.sleep(10 * (t + 1))
    else: print("FAILED", url, flush=True); continue
    n_ok += 1; tot += len(b)
    if n_ok % 250 == 0: print(n_ok, tot, flush=True)
print("done", n_ok, "of", len(a), tot, "bytes", flush=True)
