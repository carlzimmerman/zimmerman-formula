# khronon_momentum_2026 — can the khronon carry a moving galaxy's phantom? (KM1–KM2)

Support computations for the field-theory lead track (no file of that track is edited).
Lean certificates: `fable_independent_2026/lean_2026/KM_khronon_momentum.lean` (10 theorems, zero `sorry`, axioms ⊆
{propext, Classical.choice, Quot.sound}; log `KM_khronon_momentum.out`) — the closed forms are verified to SOLVE the
Fourier-space equations by substitution.

| Lane | Result | Lean |
|---|---|---|
| KM1 khronon carries phantom | linearised khronometric gravity: at λ = 1 a moving momentum-free phantom does not gravitate (L330, reproduced); at λ = 1 + ε it does, and Φ_B, Ψ_B have no 1/ε term — but the 1/ε lapse is the aether's acceleration, the MOND sector's input: a₀ would track CMB-frame speed by 2w²/(εc²) (10–30% at L297's ε; independently = L333 R2) | K1–K5 |
| KM2 phantom lag law | L340's prediction T1 made exact from its own block: the phantom is AMPLIFIED, R = 1 − 3u²/(C+1) + [C/(C+1)] u²/(c_s² − u²), pole exactly at c_s² = c₂/(C(2+3c₂)); ≤ 0.3% galaxies, ≤ 4% lensing outskirts, ≤ 5% clusters — below current reach | K6 |

Rerun: `python3 real_research/khronon_momentum_2026/<lane>.py` from the repository root.
