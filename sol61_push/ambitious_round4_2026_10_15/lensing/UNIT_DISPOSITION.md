# Pre-fit unit disposition

Before any successor fit, root's independent source audit identifies the
source convention as Msun/h: CFG416 criteria state 10^12.5 Msun/h;
cfg416_pm.py computes Mta in Msun/h and calls fret(log10(Mta)).
These exact source files are copied under inputs and hashed in ORIGINS.json.
Accordingly native_h, log10(h*Mta_phys/Msun), is the fixed primary;
legacy_physical is a secondary historical sensitivity. h=.6736.
No choice is made using successor goodness of fit. This resolves the local
source dictionary only; the observational census calibration remains conditional.
