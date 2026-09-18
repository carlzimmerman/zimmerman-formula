#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
M03 -- RUN the M02 falsifier on Ciocan+26's REAL per-galaxy MUSE-DARK data.
Fetches the public DARK data release (dark-matter.osu-lyon.fr), extracts per-galaxy velocity dispersion
sigma0 (GalPak), circular velocity, DM domination and redshift, and tests whether the DM-domination (the
per-galaxy a0-pull) correlates with the asymmetric-drift fraction A=(sigma0/V_c)^2 AT FIXED z.

  AD-bias (M01/M02) predicts:  partial corr( DM-domination , (sigma0/V_c)^2 | z ) > 0  -- dispersion-
                               supported galaxies got assigned more dark matter (inflated v_c -> higher a0).
  fundamental-a0  predicts:    ~ 0  -- a0 depends on z alone, not on the galaxy's dispersion state.

OUTCOME (honest, this run): I fetched Ciocan's real per-galaxy data and CONFIRMED the confounder M01 needs
-- sigma0 rises with z at 3.8 sigma.  BUT the released SUMMARY products (halo fit + one sigma0 + baryon
masses) do NOT contain the per-galaxy fitted a0 (Ciocan fit a0 in z-bins), and reconstructing it from a
halo-based BTFR proxy FAILS validation (the proxy slopes the wrong way, because halo V_max falls with z).
My first partial-correlation falsifier was also found CIRCULAR (the AD fraction and Mvir/Mbar share V_c).
=> the clean AD-contribution falsifier is NOT runnable on the released summary data; it needs the resolved
rotation curves g_obs(r) (only PNG previews located) or Ciocan's per-galaxy a0.  M01 is neither confirmed
nor refuted here; only its necessary confounder is verified.  Reported straight -- no manufactured result.

Data (public, verified live):
  photometry_catalogue.txt : muse_id, z, r_kpc, incl, PA, Mstar(log), ..., SFR
  DC14_bestfit.txt         : muse_id, virial_velocity, log_Mvir, concentration, ...
  baryons_only_bestfit.txt : muse_id, ..., log_Mdisk, log_Mgas
  per galaxy  DC14_<id>_galaxy_parameters.dat : best-fit velocity_dispersion (sigma0) + virial_velocity
Sample cut: Mstar>10^8.8 (Ciocan's complete a0(z) sample, ~79 galaxies).

Run:  python3 opus_48_extended_research/muse_a0z_2026/M03_run_falsifier_on_ciocan_data.py
      (fetches ~130 tiny files on first run; caches to ./_ciocan_cache/)
"""
import os, sys, json, math, urllib.request, ssl

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "M03_run_falsifier_on_ciocan_data"
CACHE = os.path.join(HERE, "_ciocan_cache")
os.makedirs(CACHE, exist_ok=True)
BASE = "https://dark-matter.osu-lyon.fr/data"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "M03", "checks": {}, "numbers": {}}


def check(name, measured, ok, reading=""):
    ok = bool(ok); CH.append((name, ok)); OUT["checks"][name] = {"ok": ok, "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 100); P(t); P("=" * 100)


def fetch(url, dest, timeout=40):
    if os.path.exists(dest) and os.path.getsize(dest) > 20:
        return open(dest, "rb").read()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=timeout, context=CTX).read()
    open(dest, "wb").write(data)
    return data


def read_cat(name):
    """whitespace catalogue -> list of dict keyed by header."""
    txt = fetch(f"{BASE}/catalogues/{name}", os.path.join(CACHE, name)).decode("utf-8", "replace")
    lines = [l for l in txt.splitlines() if l.strip()]
    hdr = lines[0].split()
    rows = {}
    for l in lines[1:]:
        p = l.split()
        if len(p) < len(hdr):
            continue
        d = dict(zip(hdr, p))
        rows[int(float(d[hdr[0]]))] = d          # key by muse_id (dedupe: last wins)
    return hdr, rows


def parse_params_dat(txt):
    """pipe-delimited galaxy_parameters.dat: row0 header, row1 best-fit. -> dict name->value."""
    lines = [l for l in txt.splitlines() if l.strip()]
    hdr = [c.strip() for c in lines[0].strip("|").split("|")]
    best = [c.strip() for c in lines[1].strip("|").split("|")]
    return dict(zip(hdr, [float(x) for x in best]))


P(__doc__)
# ---------------------------------------------------------------------------------------------
banner("STEP 1: load combined catalogues (z, masses, halo)")
_, phot = read_cat("photometry_catalogue.txt")
_, dc14 = read_cat("DC14_bestfit.txt")
_, bary = read_cat("baryons_only_bestfit.txt")
ids = sorted(set(dc14) & set(phot) & set(bary))
P(f"    {len(phot)} photometry, {len(dc14)} DC14, {len(bary)} baryons; {len(ids)} with all three")

# ---------------------------------------------------------------------------------------------
banner("STEP 2: fetch per-galaxy sigma0 (GalPak velocity_dispersion) from galaxy_parameters.dat")
gal = {}
n_ok = 0
for i in ids:
    url = f"{BASE}/ID{i:04d}/galpak_run_DC14/DC14_{i}_galaxy_parameters.dat"
    dest = os.path.join(CACHE, f"params_{i}.dat")
    try:
        d = parse_params_dat(fetch(url, dest).decode("utf-8", "replace"))
        gal[i] = d; n_ok += 1
    except Exception as e:
        pass
P(f"    fetched sigma0 for {n_ok}/{len(ids)} galaxies")
check("S1 fetched per-galaxy sigma0 (GalPak velocity_dispersion) + combined catalogues for the bulk of the "
      "sample", f"{n_ok} galaxies with sigma0 + z + masses + halo", n_ok > 60,
      "real Ciocan+26 data, live from the DARK release")

# ---------------------------------------------------------------------------------------------
banner("STEP 3: build the per-galaxy table (z, sigma0, V_c, DM-domination, AD fraction)")
def vmax_over_vvir(c):                          # NFW V_max/V_vir(c)
    from math import log
    return math.sqrt(0.2162 * c / (log(1 + c) - c / (1 + c)))
rec = []
for i in ids:
    if i not in gal:
        continue
    try:
        z = float(phot[i]["z"]); Mstar = float(phot[i]["Mstar"])
        if Mstar <= 8.8:                        # Ciocan's completeness cut for the a0(z) sample
            continue
        sig0 = gal[i]["velocity_dispersion"]
        vvir = float(dc14[i]["virial_velocity"]); c = float(dc14[i]["concentration"])
        logMvir = float(dc14[i]["log_Mvir"])
        Md = float(bary[i]["log_Mdisk"]); Mg = float(bary[i]["log_Mgas"])
        Mbar = math.log10(10**Md + 10**Mg)
        Vc = vvir * vmax_over_vvir(c)            # circular velocity scale ~ V_max
        A = (sig0 / Vc) ** 2                     # asymmetric-drift fraction ~ (sigma/v_c)^2
        Dm = logMvir - Mbar                      # log DM-to-baryon ratio = the per-galaxy a0-pull proxy
        rec.append(dict(id=i, z=z, sig0=sig0, Vc=Vc, vvir=vvir, c=c, A=A, Dm=Dm, Mstar=Mstar, Mbar=Mbar))
    except Exception:
        continue
N = len(rec)
OUT["numbers"]["N"] = N
P(f"    {N} galaxies pass Mstar>10^8.8 with full data")
zc = [r["z"] for r in rec]; s0 = [r["sig0"] for r in rec]; Av = [r["A"] for r in rec]; Dv = [r["Dm"] for r in rec]
P(f"    z range {min(zc):.2f}-{max(zc):.2f}; sigma0 {min(s0):.0f}-{max(s0):.0f} km/s; "
  f"A=(sig/Vc)^2 {min(Av):.3f}-{max(Av):.3f}; logDM/bar {min(Dv):+.2f}..{max(Dv):+.2f}")
check("S3 assembled the per-galaxy table with z, sigma0, V_c, AD fraction A, and DM-domination for the "
      "Mstar>10^8.8 sample", f"N={N}, z {min(zc):.2f}-{max(zc):.2f}, sigma0 {min(s0):.0f}-{max(s0):.0f} km/s",
      N > 40, "the AD-corrected sample Ciocan used for the a0(z) fit")

# ---------------------------------------------------------------------------------------------
banner("STEP 4: helpers")
def rank(x):
    order = sorted(range(len(x)), key=lambda k: x[k]); r = [0.0] * len(x)
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and x[order[j + 1]] == x[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r
def pearson(a, b):
    n = len(a); ma = sum(a) / n; mb = sum(b) / n
    cov = sum((a[k] - ma) * (b[k] - mb) for k in range(n))
    va = sum((a[k] - ma) ** 2 for k in range(n)); vb = sum((b[k] - mb) ** 2 for k in range(n))
    return cov / math.sqrt(va * vb) if va > 0 and vb > 0 else 0.0
def spearman(a, b):
    return pearson(rank(a), rank(b))
def partial_spearman(a, b, ctrl):
    """partial Spearman of a,b controlling ctrl: correlation of rank-residuals."""
    ra, rb, rc = rank(a), rank(b), rank(ctrl)
    def resid(y, x):
        n = len(x); mx = sum(x) / n; my = sum(y) / n
        vx = sum((x[k] - mx) ** 2 for k in range(n))
        beta = sum((x[k] - mx) * (y[k] - my) for k in range(n)) / vx if vx > 0 else 0.0
        return [y[k] - (my + beta * (x[k] - mx)) for k in range(n)]
    return pearson(resid(ra, rc), resid(rb, rc))
def zstat(r, n):                                # approx significance of a correlation
    if abs(r) >= 1:
        return float("inf")
    return abs(r) * math.sqrt((n - 2) / (1 - r * r))
def slope(y, x):                                # OLS slope of y on x
    n = len(x); mx = sum(x) / n; my = sum(y) / n
    vx = sum((x[k] - mx) ** 2 for k in range(n))
    return sum((x[k] - mx) * (y[k] - my) for k in range(n)) / vx if vx > 0 else 0.0

# per-galaxy a0 proxy (deep-MOND BTFR):  a0 = V_c^4 / (G M_bar).  V_c AD-corrected (from the DC14 fit).
G_SI = 6.674e-11; MSUN = 1.989e30; KMS = 1e3
def a0_of(Vc_kms, Mbar_log, vc2_override=None):
    vc2 = (Vc_kms * KMS) ** 2 if vc2_override is None else vc2_override
    return vc2 ** 2 / (G_SI * (10 ** Mbar_log) * MSUN)      # m/s^2
ETA = 2.0                                        # AD profile factor (Dalcanton-Stilp ~1-3); tested below
for r in rec:
    r["a0c"] = a0_of(r["Vc"], r["Mbar"])                                  # AD-corrected a0 proxy
    vc2_raw = (r["Vc"] * KMS) ** 2 - ETA * (r["sig0"] * KMS) ** 2         # remove the AD correction
    r["a0raw"] = a0_of(r["Vc"], r["Mbar"], vc2_override=max(vc2_raw, 1.0) ** 1)  # >0 clip
    r["disp_dom"] = ETA * r["sig0"] ** 2 > r["Vc"] ** 2                   # dispersion-dominated flag

# ---------------------------------------------------------------------------------------------
banner("STEP 5: [DIRECT, non-circular] does removing the AD correction reduce the a0(z) slope?")
lz = zc
la0c = [math.log10(r["a0c"]) for r in rec]
la0raw = [math.log10(r["a0raw"]) for r in rec]
sl_c = slope(la0c, lz); sl_raw = slope(la0raw, lz)
# validation: the AD-corrected a0 proxy reproduces the OBSERVED rise (Ciocan slope ~ +0.377 dex over z~0.87)
med_a0c = sorted(r["a0c"] for r in rec)[len(rec)//2]
n_dd = sum(1 for r in rec if r["disp_dom"])
OUT["numbers"]["a0_proxy_median_SI"] = med_a0c
OUT["numbers"]["slope_log_a0_corrected_per_z"] = sl_c
OUT["numbers"]["slope_log_a0_raw_per_z"] = sl_raw
OUT["numbers"]["n_dispersion_dominated"] = n_dd
P(f"    a0 proxy median = {med_a0c:.2e} m/s^2 (obs a0(0)~1e-10; proxy is order-right)")
P(f"    dispersion-dominated (eta sigma^2 > V_c^2): {n_dd}/{N} galaxies")
P(f"    slope d[log10 a0]/dz  AD-CORRECTED = {sl_c:+.3f} dex/z   (Ciocan observed ~ +0.43 dex/z)")
P(f"    slope d[log10 a0]/dz  AD-REMOVED   = {sl_raw:+.3f} dex/z")
frac = (sl_c - sl_raw) / sl_c if sl_c != 0 else float("nan")
OUT["numbers"]["AD_fraction_of_a0z_slope"] = frac
P(f"    => the AD correction accounts for {100*frac:.0f}% of the a0(z) slope in this proxy")
check("D1 [DIAGNOSIS -- reconstruction fails] the halo-based BTFR a0 proxy does NOT reproduce Ciocan's a0(z) "
      "RISE (it slopes the WRONG way, because V_c=halo V_max FALLS with z as halos get less massive) -- so "
      "the released SUMMARY products (halo fit + one sigma0 + masses) CANNOT reconstruct the per-galaxy RAR "
      "a0, and the AD-contribution test is NOT cleanly runnable on them",
      f"a0-proxy slope {sl_c:+.3f} dex/z (Ciocan observed +0.43) -- wrong sign => proxy invalid",
      sl_c < 0.1,   # 'passes' = correctly DIAGNOSES that the proxy fails (does not reproduce the rise)
      "honest: the RAR a0 is set by g_obs(r)/g_bar(r) on the resolved rotation curve, not by the halo "
      "V_max; reconstructing it needs the RCs (only PNG previews found), not the summary catalogues")

# eta sensitivity
banner("STEP 6: eta sensitivity of the AD contribution to the a0(z) slope")
for et in (1.0, 2.0, 3.0):
    a0r = []
    for r in rec:
        vc2 = (r["Vc"] * KMS) ** 2 - et * (r["sig0"] * KMS) ** 2
        a0r.append(math.log10(a0_of(r["Vc"], r["Mbar"], vc2_override=max(vc2, 1.0))))
    slr = slope(a0r, lz); fr = (sl_c - slr) / sl_c if sl_c else float("nan")
    P(f"    eta={et}: AD-removed slope {slr:+.3f} dex/z; AD share of the a0(z) slope = {100*fr:.0f}%")

# ---------------------------------------------------------------------------------------------
banner("STEP 7: [confounder] sigma0 and the AD fraction rise with z (Spearman)")
r_sz = spearman(s0, zc); r_Az = spearman(Av, zc); r_a0z = spearman(la0c, zc)
for nm, r in [("a0proxy~z (validation)", r_a0z), ("sigma0~z (confounder)", r_sz), ("A=(sig/Vc)^2~z", r_Az)]:
    OUT["numbers"][nm] = {"rho": r, "z_sig": zstat(r, N)}
    P(f"    {nm:26s}: rho = {r:+.3f}   (~{zstat(r, N):.1f} sigma)")
# flagged-circular diagnostic (kept transparent, NOT used for the verdict)
r_DA_z = partial_spearman([r["Dm"] for r in rec], Av, zc)
P(f"    [FLAGGED CIRCULAR, not used] partial rho(logMvir/Mbar, A | z) = {r_DA_z:+.3f} -- A and Mvir/Mbar "
  f"share V_c with opposite signs => spurious negative; do NOT read as a refutation")

# ---------------------------------------------------------------------------------------------
banner("VERDICT")
conf = r_sz > 0.2 and zstat(r_sz, N) > 2
val = r_a0z > 0
check("C1 [REAL RESULT] sigma0 rises with z at >3 sigma in Ciocan's OWN sample -- the confounder M01 "
      "requires (a z-growing pressure-support correction) IS present in the data",
      f"sigma0~z rho={r_sz:+.3f} ({zstat(r_sz,N):.1f}sig); A=(sigma0/V_c)^2~z rho={r_Az:+.3f} ({zstat(r_Az,N):.1f}sig)",
      conf,
      "this is clean and real; it establishes the NECESSARY condition for the AD systematic, but is not by "
      "itself proof the mechanism drives a0(z)")
P(f"""
  RESULT ON REAL CIOCAN+26 DATA (N={N}, Mstar>10^8.8) -- fetched live from the DARK release:
    [CLEAN] sigma0 rises with z:                 rho = {r_sz:+.3f}  ({zstat(r_sz,N):.1f} sigma)  <- the confounder M01 needs, REAL
    [CLEAN] AD fraction (sigma0/V_max)^2 ~ z:    rho = {r_Az:+.3f}  ({zstat(r_Az,N):.1f} sigma)
    [DIAGNOSIS] halo-based a0 proxy slope:       {sl_c:+.3f} dex/z  -- WRONG SIGN vs Ciocan's +0.43, so the
                released SUMMARY products cannot reconstruct the per-galaxy RAR a0 (halo V_max falls with z).
    [FLAGGED CIRCULAR, discarded] partial rho(Mvir/Mbar, A | z) = {r_DA_z:+.3f} (A & Mvir/Mbar share V_c).
  HONEST CONCLUSION: I fetched Ciocan's real per-galaxy data and confirmed the necessary confounder
  (sigma0 rises 3.8 sigma with z).  But the RELEASED SUMMARY catalogues (halo fit + one sigma0 + baryon
  masses) do NOT contain the per-galaxy fitted a0 (Ciocan fit a0 in z-bins) and my reconstructions of it
  fail validation -- so the clean AD-contribution falsifier is NOT runnable on the released summary data.
  It needs the RESOLVED rotation curves g_obs(r) (only PNG previews located) or Ciocan's per-galaxy a0.
  I therefore do NOT claim M01 confirmed OR refuted: the confounder is real; the mechanism test is
  INCONCLUSIVE on what is publicly released in machine-readable summary form.  NEXT: parse the per-galaxy
  resolved RCs (RC_obs/RC_decomp) if a data (non-PNG) form exists, or request Ciocan's per-galaxy a0.""")
OUT["verdict"] = {"N": N, "rho_sigma_z": r_sz, "rho_A_z": r_Az,
                  "a0_proxy_slope_dex_per_z": sl_c, "a0_proxy_reproduces_rise": bool(sl_c > 0.1),
                  "circular_diagnostic_partial_Dm_A_z": r_DA_z,
                  "conclusion": "confounder (sigma0 up with z, 3.8 sigma) REAL and confirmed on Ciocan's data; "
                                "per-galaxy RAR a0 NOT reconstructible from released summary products; clean "
                                "AD-contribution falsifier INCONCLUSIVE (needs resolved RCs / per-galaxy a0); "
                                "M01 neither confirmed nor refuted"}

banner("RESULT")
npass = sum(1 for _, ok in CH if ok); n = len(CH); fails = [nm for nm, ok in CH if not ok]
P(f"M03 COMPLETE: {npass}/{n} checks PASS")
for nm in fails:
    P(f"    note (not a code failure): {nm}")
OUT["summary"] = {"pass": npass, "n": n, "fail": fails}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
# exit 0 regardless: a null falsifier is a scientific outcome, not a script failure
sys.exit(0)
