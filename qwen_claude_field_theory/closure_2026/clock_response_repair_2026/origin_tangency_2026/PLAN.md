# Same-action origin tangency and scale separation

Base: 362ddbb5d (including verified numerical checkpoint ecce4e6ce).
Goal remains a complete same-action theory; this work does not redefine it.
No new particles, local a0, reconstructed coefficients, or retuned background.

Ordered routes:
1. Isolate the center projection/evolution discrepancy using the exact chain
   rule for the already imposed clock constraint. Compare the continuum
   gradient-jet evolution with the discrete differentiated gradient evolution.
2. If route 1 identifies a numerical cause, test a minimal compatible operator
   repair without modifying action equations or prior acceptance thresholds.
3. Formalize the exact dependency/error identity in Lean, with physical
   assumptions explicit. Then use the validated equations to investigate
   scale-dependent clustering; do not substitute a neutrino analogy for it.

First experiment: saved 129/257 states at t=.02; no fresh evolution required.
Exact SymPy algebra plus float64 evaluation; max 120 seconds. Success means
isolating the discrepancy, not proving full evolution or physical closure.
