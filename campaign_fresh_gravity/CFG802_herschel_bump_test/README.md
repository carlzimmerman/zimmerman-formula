# CFG802: CFG799's 3.2σ hint at 541.700 GHz. HINT FADES

| test | result |
|---|---|
| K1 (reproduce CFG799) | a = +20.5 ± 6.5 mK, z +3.17. PASS |
| **T1 splits** | **H polarisation z +5.3, V polarisation z −0.5** (disagree at 4.1σ). Early/late and USB/LSB agree. Line-rich targets z +1.1 vs others +3.2. |
| **T2 width** | z grows from +3.2 at 1.1 MHz to +3.9 at **4 MHz FWHM**. BROAD, not an instrument-width line. |
| T3 leave-one-out | no single observation drives it (min z +2.7). NOT DRIVEN |
| T4 look-elsewhere | local p 0.0015; trials-corrected p **0.08** |

**Class: HINT FADES**, killed by T1 and T2.
- The excess sits in **one polarisation only** (HIFI H mixer). A mirror line from a randomly polarised field must appear
  in both.
- It is **~4 MHz wide**, about 3.5× the instrument line width.
- Both point to an instrumental baseline or standing-wave feature in the H receiver, not a physical line.

**Disclosed: MUTATE did not bite on T1.**
- A 61.5 mK narrow line injected into both polarisations keeps the pre-existing H−V difference. T1 still "fails" on
  injected data, so T1's agreement rule cannot certify a real line on top of this artefact. That is a design flaw of T1
  as frozen.
- The mutation run did validate T2: the injected line is correctly classed NARROW (best FWHM 1.14 MHz).
- The verdict therefore rests on T2, which the mutation validated, and on the H-only character of the excess, which is
  read directly from the data.
- Under the frozen rule, the class stands as HINT FADES. The T1 flaw is recorded, not re-adjudicated.

κ fitted; not theory closed.
