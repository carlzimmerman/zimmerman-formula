# WG3 Amendment A1: committed with the engine, after K8(a) failed as frozen and before any production run

**What happened.** K8(a) as frozen compares the T1 potential with τ = −10⁹ (switch fully on) to R1's over all modes, at 1e-6. It reads **2.8e-3: FAIL**. Locating the error:

| comparison | relative difference |
|---|---|
| off the Nyquist planes | 1.7e-7 |
| on the Nyquist planes | 2.8e-3 |
| smooth power-law field, all modes | 1.35e-4 |

**Cause.** WG2's spectral derivative (i k at k = −k_Ny) breaks Hermitian symmetry on the Nyquist planes. T1's real-space round trip (×f) projects those components out, while R1 carries them until the force step, whose inverse FFT projects them out too. The switch logic is exact; the difference is in mesh components that carry no resolved force.

**Change.** K8(a) compares off the Nyquist planes, at the same 1e-6. The all-mode number is kept in `runs/checks.json` as `on_vs_R1_all_modes_as_frozen`. Nothing else changes.

κ = ½ FITTED; not theory closed.
