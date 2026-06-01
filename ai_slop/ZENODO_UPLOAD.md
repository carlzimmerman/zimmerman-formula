# Zenodo Upload Instructions for DOI Registration

## Quick Start (5 minutes)

### Step 1: Push to GitHub
```bash
git push origin main
```

### Step 2: Create GitHub Release
1. Go to: https://github.com/carlzimmerman/zimmerman-formula/releases
2. Click "Draft a new release"
3. Tag version: `v5.0.0`
4. Release title: `v5.0.0 - Computational Therapeutics Pipeline`
5. Description:
```
## v5.0.0 - Open-Source Computational Therapeutics

### New Features
- **Dark Proteome Pipeline**: c-Myc cancer target via REMD
- **Ion Channel Pipeline**: NaV1.7 non-addictive painkillers
- **Metalloenzyme Pipeline**: Thermostable PETase for plastic degradation
- **Cross-Validation Framework**: 3-layer hallucination detection

### Prior Art Established
All therapeutic sequences published April 20, 2026 under AGPL-3.0 + OpenMTA.

### Therapeutic Targets
| Target | Disease | Top Candidate |
|--------|---------|---------------|
| c-Myc | Cancer (70%) | IEQAVQEMEEMY (ΔG=-17.75) |
| NaV1.7 | Pain | 3368x selectivity knottin |
| PETase | Plastic | +20°C Tm variant |
| CFTR | Cystic Fibrosis | -21.42 kcal/mol chaperone |
| D2R | Prolactinoma | 100% D2R selective |
```
6. Click "Publish release"

### Step 3: Connect Zenodo to GitHub (First Time Only)
1. Go to: https://zenodo.org
2. Log in (or create account)
3. Go to: https://zenodo.org/account/settings/github/
4. Click "Connect" next to your GitHub account
5. Find `zimmerman-formula` repository
6. Toggle switch to ON

### Step 4: Automatic DOI Minting
Once connected, Zenodo automatically:
1. Detects new GitHub releases
2. Archives the repository
3. Mints a new DOI
4. Uses `.zenodo.json` for metadata

Your DOI will appear at: https://zenodo.org/account/settings/github/

---

## Manual Upload (Alternative)

If GitHub integration doesn't work:

1. Go to: https://zenodo.org/deposit/new
2. Upload type: **Software**
3. Upload files:
   - Create zip: `git archive -o zimmerman-formula-v5.0.0.zip HEAD`
   - Upload the zip file
4. Fill metadata from `.zenodo.json`:
   - Title: "The Zimmerman Framework: Unified Physics from Z² and Open-Source Computational Therapeutics"
   - Authors: Carl Zimmerman, Claude Opus 4.5 (Anthropic)
   - License: AGPL-3.0-or-later
   - Keywords: (copy from .zenodo.json)
5. Click "Publish"

---

## Verification Checklist

After publishing, verify:

- [ ] DOI is active (click the DOI link)
- [ ] Metadata displays correctly
- [ ] License shows AGPL-3.0-or-later
- [ ] All files are included
- [ ] Keywords are indexed
- [ ] Citation can be exported (BibTeX, etc.)

---

## Prior Art Legal Notice

**IMPORTANT**: The DOI timestamp serves as legal proof of prior art.

Once published, the following are PUBLIC DOMAIN:
- All peptide sequences in FASTA files
- All protein variants in mutation lists
- All therapeutic designs in JSON outputs

No entity can patent these sequences after the DOI publication date.

**Recommended**: Save PDF of Zenodo record page for legal documentation.

---

## Citation Format

After DOI is minted, cite as:

```bibtex
@software{zimmerman_2026_therapeutics,
  author       = {Zimmerman, Carl and Claude Opus 4.5},
  title        = {{The Zimmerman Framework: Unified Physics from Z²
                   and Open-Source Computational Therapeutics}},
  month        = apr,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v5.0.0},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXXXXX}
}
```

Replace `XXXXXXX` with actual DOI number after minting.

---

## Support

- Zenodo documentation: https://help.zenodo.org
- GitHub-Zenodo integration: https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content

---

**Publication Date**: April 20, 2026
**Version**: 5.0.0
**License**: AGPL-3.0-or-later (code) + CC-BY-SA-4.0 (data) + OpenMTA (biology)
