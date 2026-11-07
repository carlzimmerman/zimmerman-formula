# SV5 iter_1 / iter_2 Amendment A1 (technical, before any graded number)

Kappa = 1/2 FITTED; not theory closed.

The first run stopped after K1 (median 0.987, PASS) and before any graded number: the reused CLASS model (QX3 corner) tabulates
P_lin only to z_max_pk = 20, so the frozen z = 50 slice could not be evaluated. Fix: for z > 20, P(k, z) = P(k, 20) (21/(1+z))^2
(matter-era growth D proportional to a; the dust reference's growth is scale independent there on box scales). Nothing else
changed. The crash log is run_web_crash_A1.txt.
