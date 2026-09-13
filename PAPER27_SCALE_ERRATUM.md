# PAPER27 scale-output erratum (source audit)

The published PAPER27 source currently displays

```text
a_0 = s/c,   kappa = 1/c
```

immediately after defining `s = c_light sqrt(G rho_Lambda)`.  The derivation
has overloaded `c`: the symbol in that line is the constitutive deep-MOND
slope, not the speed of light.  The unambiguous derivation is

```text
mu_n(g/s) = n g/s + O(g^2),
mu_n g = g_N  =>  g^2 = (s/n) g_N,
a_0 = s/n,
kappa = a_0/[c_light sqrt(G rho)] = 1/n.
```

For the selected member `n=2`, this gives `a_0=s/2` and `kappa=1/2`, exactly
the values used in the numerical tables.  The tables are therefore
unchanged; the displayed equation should be corrected in a future revision or
addendum.  No published PDF was silently rewritten by this audit.

Reproduction:

```bash
python3 qwen_claude_field_theory/closure_2026/PAPER27_scale_erratum_audit.py  # exit 0
python3 -m unittest -v qwen_claude_field_theory/closure_2026/test_PAPER27_scale_erratum_audit.py  # exit 0
```
