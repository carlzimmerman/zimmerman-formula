# Preserved exploratory failures and locator correction

1. Exact-version PDF requests through the web reader returned cache misses
   for AHLP, NP and the two BKSM papers. Version-pinned public downloads of
   source archives and BKSM PDFs subsequently succeeded and are hashed in
   SOURCE_AUTHENTICATION.json.
2. The initial unprivileged curl for arXiv source failed with exit 6,
   `Could not resolve host: arxiv.org`. The authorized public network path
   then succeeded. No source absence was inferred from that failure.
3. An exploratory direct `sympy.parsing.mathematica.parse_mathematica` call
   on `RowBox[{"x","+","1"}]` failed because it tried to sympify the literal
   `+` string (`SympifyError` / `SyntaxError: unexpected EOF while parsing`).
   No mathematical assertion was tested by that unsuccessful method. The
   independent parser instead uses Python AST over inert whitelisted box
   calls and a separately whitelisted arithmetic expression parser. The
   bounded run with this method completed successfully.
4. PRETARGET.md contains a source-numbering typo: the NP current tensor,
   basis and Born amplitudes are (2.9)–(2.11), not (2.4)/(2.6). Its actual
   source definitions and normalization algebra are unchanged. PRETARGET
   is preserved byte-for-byte as the original pretarget record.
5. Before PRETARGET, a broad `rg` accidentally exposed common-response
   lines 146–166. This is disclosed in PRETARGET and prevents a claim of
   blindness for that factor. The nonborn_proton proof/code were unread
   before PRETARGET. Finite-band numerical results were read before the
   separate finite design/code, so its comparison is an independent
   implementation with prior numerical-answer exposure.
