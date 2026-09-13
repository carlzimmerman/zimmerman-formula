# Independent anti-hardcoding audit

The project contract says that ranks, determinants, PPN values, and degrees of
freedom must be *computed*, not certified by comparison with a chosen answer.
`anti_hardcode_audit.py` scans the executable tensor-compensated branch gates
for comparisons between derived count fields and literal values.  It does not
inspect or trust the reported JSON.

Run:

```text
python3 anti_hardcode_audit.py
python3 anti_hardcode_audit.py --strict
```

The first command is diagnostic.  The strict command intentionally fails while
any hard-coded expectation remains.  This is a methodological gate, not a
physics no-go theorem.
