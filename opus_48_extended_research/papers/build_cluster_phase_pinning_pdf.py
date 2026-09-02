#!/usr/bin/env python3
"""Build CLUSTER_PHASE_PINNING_POLYTROPE.pdf from the markdown (article class).
Unicode super/subscript RUNS + single-char Greek/symbols -> inline math, emitted as \\(...\\)
(NOT $...$, which pandoc mis-parses when a closing $ is followed by a digit). Adjacent inline
math is collapsed. Usage: python build_cluster_phase_pinning_pdf.py  (from papers/). Requires: pandoc, tectonic."""
import re, subprocess, os, tempfile

SRC = "CLUSTER_PHASE_PINNING_POLYTROPE.md"
OUT = "pdf/CLUSTER_PHASE_PINNING_POLYTROPE.pdf"

SUP = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁻':'-','⁺':'+','ⁿ':'n','ⁱ':'i'}
SUB = {'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9','₊':'+','₋':'-',
       'ₐ':'a','ₑ':'e','ₓ':'x','ᵢ':'i','ⱼ':'j','ₙ':'n','ₖ':'k','ₘ':'m','ₚ':'p','ₛ':'s','ₜ':'t'}
PROSE = {
 'Λ':r'\Lambda','π':r'\pi','κ':r'\kappa','ρ':r'\rho','μ':r'\mu','ν':r'\nu','σ':r'\sigma',
 'Ω':r'\Omega','Υ':r'\Upsilon','α':r'\alpha','β':r'\beta','γ':r'\gamma','δ':r'\delta','Δ':r'\Delta',
 'θ':r'\theta','Θ':r'\Theta','φ':r'\varphi','Φ':r'\Phi','ψ':r'\psi','Ψ':r'\Psi','Σ':r'\Sigma',
 'χ':r'\chi','λ':r'\lambda','ξ':r'\xi','τ':r'\tau','ω':r'\omega','η':r'\eta','ε':r'\varepsilon',
 'ζ':r'\zeta','Γ':r'\Gamma','Ξ':r'\Xi',
 '×':r'\times','≈':r'\approx','≃':r'\simeq','≅':r'\cong','∝':r'\propto','√':r'\surd','−':r'-','·':r'\cdot',
 '÷':r'\div','→':r'\rightarrow','←':r'\leftarrow','↔':r'\leftrightarrow','⇒':r'\Rightarrow','⇔':r'\Leftrightarrow','⟹':r'\Longrightarrow',
 '≥':r'\geq','≤':r'\leq','≪':r'\ll','≫':r'\gg','≠':r'\neq','∼':r'\sim','≲':r'\lesssim','≳':r'\gtrsim','⊕':r'\oplus',
 '∞':r'\infty','∂':r'\partial','∇':r'\nabla','ℏ':r'\hbar','ℓ':r'\ell','±':r'\pm','∈':r'\in',
 '⟨':r'\langle','⟩':r'\rangle','½':r'\tfrac12','⅓':r'\tfrac13','¼':r'\tfrac14','⅔':r'\tfrac23','¾':r'\tfrac34',
}
LETT = {'ł':r'\l{}','Ł':r'\L{}','ś':r"\'{s}",'ź':r"\'{z}",'ż':r'\.{z}','ö':r'\"o','é':r"\'e",'è':r'\`e',
        'ü':r'\"u','ä':r'\"a','č':r'\v{c}','š':r'\v{s}','ž':r'\v{z}','ř':r'\v{r}','á':r"\'a",'í':r"\'i",
        'ó':r"\'o",'ú':r"\'u",'ñ':r'\~n','å':r'\aa{}','ø':r'\o{}','°':r'\textdegree{}'}
INMATH = dict(PROSE)
for k, v in SUP.items(): INMATH[k] = '^{' + v + '}'
for k, v in SUB.items(): INMATH[k] = '_{' + v + '}'

SUP_RE = re.compile('[' + ''.join(SUP) + ']+')
SUB_RE = re.compile('[' + ''.join(SUB) + ']+')
SCINOT = re.compile(r'(\d[\d.]*)×(\d[\d.]*)([⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+)')  # 9.36×10⁻¹¹ -> one clean span

def fix_prose(s):
    s = s.replace('−', '-')   # U+2212 minus -> plain hyphen (prose; avoids a $-$ span before digits)
    # scientific notation as ONE span (clean, avoids the $-before-digit problem entirely)
    s = SCINOT.sub(lambda m: '$' + m.group(1) + r'\times' + m.group(2) + '^{' + ''.join(SUP[c] for c in m.group(3)) + '}$', s)
    s = SUP_RE.sub(lambda m: '$^{' + ''.join(SUP[c] for c in m.group()) + '}$', s)
    s = SUB_RE.sub(lambda m: '$_{' + ''.join(SUB[c] for c in m.group()) + '}$', s)
    for u, l in PROSE.items():
        s = s.replace(u, '$' + l + '$')
    # Latin diacritics (ł, ś, ż, ö, …) are left as Unicode -> tectonic/XeTeX renders them natively
    # (they are < U+0300 so the strip below keeps them; LaTeX-escape forms get mangled by pandoc markdown).
    while '$$' in s:                               # collapse adjacent inline math
        s = s.replace('$$', '')
    # pandoc: a closing $ immediately followed by a digit is NOT parsed as math. The only such case
    # left after collapse is a standalone operator span (×, ·, ±) directly before a number -> insert
    # a space (× 4.42 etc., standard notation). NOTE: must NOT touch scientific-notation spans, whose
    # OPENING $ legitimately precedes a digit ($9.36\times10^{-11}$).
    for op in (r'\times', r'\cdot', r'\pm', r'\approx', r'\sim', r'\leq', r'\geq', r'\ll', r'\gg',
               r'\lesssim', r'\gtrsim', r'\neq', r'\simeq', r'\propto', r'\cong', r'\div', r'\in'):
        s = re.sub(r'(\$' + re.escape(op) + r'\$)(?=\d)', r'\1 ', s)
    s = ''.join(c if (ord(c) < 0x300 or c in '—–“”’‘…•') else '' for c in s)
    return s

def cleanmath(inner):
    return ''.join(INMATH[c] + ' ' if c in INMATH else c for c in inner)

def main():
    text = open(SRC).read()
    pat = re.compile(r'(```.*?```|`[^`\n]*`|\$\$.*?\$\$|\$[^$\n]*\$)', re.DOTALL)
    parts = pat.split(text)
    for i, seg in enumerate(parts):
        if i % 2 == 0:
            parts[i] = fix_prose(seg)
        elif seg.startswith('$$'):
            parts[i] = '$$' + cleanmath(seg[2:-2]) + '$$'
        elif seg.startswith('$'):
            parts[i] = '$' + cleanmath(seg[1:-1]) + '$'
        # backtick code spans: unchanged
    with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False) as f:
        f.write(''.join(parts)); md = f.name
    tex = md.replace('.md', '.tex')
    subprocess.run(['pandoc', md, '-s', '-t', 'latex', '-V', 'documentclass=article',
                    '-V', 'geometry:margin=1in', '-V', 'fontsize=11pt', '--toc', '--toc-depth=2',
                    '-V', 'colorlinks=true', '-V', 'linkcolor=NavyBlue', '-V', 'urlcolor=NavyBlue',
                    '-o', tex], check=True)
    subprocess.run(['tectonic', tex, '--outdir', os.path.dirname(tex), '-Z', 'continue-on-errors'], check=True)
    os.makedirs('pdf', exist_ok=True)
    os.replace(tex.replace('.tex', '.pdf'), OUT)
    print('wrote', OUT, os.path.getsize(OUT), 'bytes')

if __name__ == '__main__':
    main()
