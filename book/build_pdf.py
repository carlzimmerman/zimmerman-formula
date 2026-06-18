#!/usr/bin/env python3
"""
Build A_BEAUTIFULLY_GEOMETRIC_UNIVERSE.pdf from the combined markdown.

The manuscript mixes real LaTeX math ($...$, $$...$$) with bare Unicode physics
symbols in the prose (Λ, κ, π, √, a₀, ½, ...). A plain pdf-engine font can't render
those, so we (1) substitute bare Unicode symbols -> LaTeX *only outside* existing
math/code spans, (2) clean Unicode symbols *inside* math spans to LaTeX commands,
then (3) compile with tectonic in continue-on-errors mode (a few agent-written
equations are malformed; this tolerates them rather than halting on a 196k-word book).

Usage:  python build_pdf.py   (run from book/)
Requires: pandoc, tectonic, python3.
"""
import re, unicodedata, subprocess, os, tempfile

SRC = "A_BEAUTIFULLY_GEOMETRIC_UNIVERSE.md"
OUT = "A_BEAUTIFULLY_GEOMETRIC_UNIVERSE.pdf"

PROSE = {  # Unicode -> $...$ (used in prose)
 'Λ':r'$\Lambda$','π':r'$\pi$','κ':r'$\kappa$','ρ':r'$\rho$','μ':r'$\mu$','ν':r'$\nu$','σ':r'$\sigma$',
 'Ω':r'$\Omega$','Υ':r'$\Upsilon$','α':r'$\alpha$','β':r'$\beta$','γ':r'$\gamma$','δ':r'$\delta$','Δ':r'$\Delta$',
 'θ':r'$\theta$','Θ':r'$\Theta$','φ':r'$\varphi$','Φ':r'$\Phi$','ψ':r'$\psi$','Ψ':r'$\Psi$','Σ':r'$\Sigma$',
 'χ':r'$\chi$','λ':r'$\lambda$','ξ':r'$\xi$','τ':r'$\tau$','ω':r'$\omega$','η':r'$\eta$','ε':r'$\varepsilon$',
 'ζ':r'$\zeta$','Γ':r'$\Gamma$','Ξ':r'$\Xi$','×':r'$\times$','≈':r'$\approx$','≃':r'$\simeq$','≅':r'$\cong$',
 '∝':r'$\propto$','√':r'$\surd$','−':r'$-$','·':r'$\cdot$','÷':r'$\div$','→':r'$\rightarrow$','←':r'$\leftarrow$',
 '↔':r'$\leftrightarrow$','⇒':r'$\Rightarrow$','≥':r'$\geq$','≤':r'$\leq$','≪':r'$\ll$','≫':r'$\gg$','≠':r'$\neq$',
 '∼':r'$\sim$','≲':r'$\lesssim$','≳':r'$\gtrsim$','∞':r'$\infty$','∂':r'$\partial$','∇':r'$\nabla$','ℏ':r'$\hbar$',
 'ℓ':r'$\ell$','°':r'$^{\circ}$','±':r'$\pm$','∈':r'$\in$','⟨':r'$\langle$','⟩':r'$\rangle$','½':r'$\tfrac12$',
 '⅓':r'$\tfrac13$','¼':r'$\tfrac14$','⅔':r'$\tfrac23$','¾':r'$\tfrac34$','⁰':r'$^0$','¹':r'$^1$','²':r'$^2$',
 '³':r'$^3$','⁴':r'$^4$','⁵':r'$^5$','⁶':r'$^6$','⁷':r'$^7$','⁸':r'$^8$','⁹':r'$^9$','⁻':r'$^{-}$','ⁿ':r'$^n$',
 '⁺':r'$^{+}$','₀':r'$_0$','₁':r'$_1$','₂':r'$_2$','₃':r'$_3$','₄':r'$_4$','₅':r'$_5$','₆':r'$_6$','₇':r'$_7$',
 '₈':r'$_8$','₉':r'$_9$','ₐ':r'$_a$','ₑ':r'$_e$','ₓ':r'$_x$','ᵢ':r'$_i$','ⱼ':r'$_j$','ₙ':r'$_n$',
 'ł':r'\l{}','Ł':r'\L{}','ś':r"\'s",'ź':r"\'z",'ż':r'\.z','ö':r'\"o','Ö':r'\"O','é':r"\'e",'è':r'\`e','ü':r'\"u',
 'ä':r'\"a','ñ':r'\~n','å':r'\aa{}','ø':r'\o{}','ç':r'\c{c}','ý':r"\'y",'ÿ':r'\"y','ř':r'\v{r}','ï':r'\"i',
 'î':r'\^i','á':r"\'a",'í':r"\'i",'ó':r"\'o",'ú':r"\'u",'à':r'\`a','â':r'\^a','ê':r'\^e','ô':r'\^o','č':r'\v{c}',
 'š':r'\v{s}','ž':r'\v{z}','ğ':r'\u{g}'}
INMATH = {k: v.strip('$') for k, v in PROSE.items() if v.startswith('$')}
GREEK = {'ALPHA':r'\alpha','BETA':r'\beta','GAMMA':r'\gamma','DELTA':r'\delta','EPSILON':r'\varepsilon',
 'ZETA':r'\zeta','ETA':r'\eta','THETA':r'\theta','IOTA':r'\iota','KAPPA':r'\kappa','LAMDA':r'\lambda',
 'MU':r'\mu','NU':r'\nu','XI':r'\xi','PI':r'\pi','RHO':r'\rho','SIGMA':r'\sigma','TAU':r'\tau',
 'UPSILON':r'\upsilon','PHI':r'\varphi','CHI':r'\chi','PSI':r'\psi','OMEGA':r'\omega'}
CAPS = {'GAMMA','DELTA','THETA','LAMDA','XI','PI','SIGMA','UPSILON','PHI','PSI','OMEGA'}

def demath(span):
    out = []
    for ch in span:
        if ch in INMATH: out.append(INMATH[ch] + ' '); continue
        if 0x1D400 <= ord(ch) <= 0x1D7FF:
            nm = unicodedata.name(ch, '')
            hit = next((k for k in GREEK if k in nm), None)
            if hit:
                cmd = GREEK[hit]
                out.append((cmd[0] + cmd[1].upper() + cmd[2:] if ('CAPITAL' in nm and hit in CAPS) else cmd) + ' ')
            else:
                out.append(unicodedata.normalize('NFKD', ch)[:1])
            continue
        out.append(ch)
    return ''.join(out)

def main():
    text = open(SRC).read()
    bookdir = os.path.dirname(os.path.abspath(__file__))
    # make figure image paths absolute so tectonic (run from a temp dir) can find them
    text = text.replace('](figures/', '](' + bookdir + '/figures/')
    pat = re.compile(r'(```.*?```|`[^`\n]*`|\$\$.*?\$\$|\$[^$\n]*\$)', re.DOTALL)
    parts = pat.split(text)
    for i, seg in enumerate(parts):
        if i % 2 == 0:
            for u, l in PROSE.items(): seg = seg.replace(u, l)
            seg = ''.join(c if (ord(c) < 0x300 or c in '—–“”’‘…•') else '' for c in seg)
        elif seg.startswith('$'):
            seg = demath(seg)
        parts[i] = seg
    with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False) as f:
        f.write(''.join(parts)); md = f.name
    tex = md.replace('.md', '.tex')
    bookdir = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(['pandoc', md, '-s', '-t', 'latex', '-V', 'documentclass=report',
                    '-V', 'geometry:margin=1in', '-V', 'fontsize=11pt',
                    '--resource-path=' + bookdir,            # so figures/*.png resolve from book/
                    '-V', 'graphics=true',
                    '--top-level-division=chapter', '--toc', '--toc-depth=1',
                    '-V', 'colorlinks=true', '-V', 'linkcolor=NavyBlue', '-o', tex], check=True)
    subprocess.run(['tectonic', tex, '--outdir', os.path.dirname(tex), '-Z', 'continue-on-errors'], check=True)
    os.replace(tex.replace('.tex', '.pdf'), OUT)
    print('wrote', OUT)

if __name__ == '__main__':
    main()
