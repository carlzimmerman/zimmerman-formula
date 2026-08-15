'use client';

/**
 * DbiPressurePanel — the offset-DBI engine, interactively.
 * At β = 1 (μ²Λ_D² = M⁴): K(s)/M⁴ = −√(1 − s²), s ≡ (Q−Q₀)/Λ_D.
 * −K is the dark sector's pressure magnitude, and 𝒜 = a₀² ∝ −K, so the SAME curve is
 * the dark energy today (s → 0), the dust excitation (small s), and the a₀ off-switch
 * (s → 1, the wall). The excitation s grows ∝ (1+z)³ into the past.
 */

import { useMemo, useState } from 'react';

const W = 720;
const H = 380;
const PL = 60;
const PB = 44;
const PT = 20;
const PR = 20;

function Kfrac(s: number): number {
  return -Math.sqrt(Math.max(0, 1 - s * s));
}

export default function DbiPressurePanel() {
  const [s, setS] = useState(0.15);

  const px = (sv: number) => PL + sv * (W - PL - PR);
  const py = (k: number) => PT + ((k + 1.05) / 1.1) * (H - PT - PB) * -1 + (H - PB);

  const path = useMemo(() => {
    const p: string[] = [];
    for (let sv = 0; sv <= 0.9999; sv += 0.005) {
      p.push(`${px(sv).toFixed(1)},${py(Kfrac(sv)).toFixed(1)}`);
    }
    return 'M' + p.join(' L');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const k = Kfrac(s);
  const a0ratio = Math.sqrt(-k); // a0 ∝ √(−K)
  const regime =
    s < 0.02
      ? { label: 'vacuum: w = −1 EXACTLY — this is the dark energy', c: 'text-emerald-300' }
      : s < 0.85
      ? { label: 'excitation: density linear in s ⇒ dust — this is the dark matter the CMB needs', c: 'text-cyan-300' }
      : { label: 'the DBI wall: pressure bounded, a₀ → 0 — MOND switches off (recombination side)', c: 'text-amber-300' };

  return (
    <div className="rounded-xl border border-gray-700 bg-black/40 p-5">
      <h3 className="mb-1 text-lg font-semibold text-white">The engine: one bounded function, three jobs</h3>
      <p className="mb-4 text-sm text-gray-400">
        Slide the excitation s = (Q−Q₀)/Λ_D. The curve is K(s)/M⁴ = −√(1−s²) — the dark
        sector&rsquo;s pressure — and a₀² ∝ −K rides it. s grows ∝ (1+z)³ into the past, so
        &ldquo;today&rdquo; sits near 0 and recombination sits at the wall.
      </p>

      <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
        <line x1={PL} y1={H - PB} x2={W - PR} y2={H - PB} stroke="#475569" strokeWidth={1} />
        <line x1={PL} y1={PT} x2={PL} y2={H - PB} stroke="#475569" strokeWidth={1} />
        {[0, -0.5, -1].map((t) => (
          <g key={t}>
            <line x1={PL} y1={py(t)} x2={W - PR} y2={py(t)} stroke="#1e293b" strokeWidth={1} />
            <text x={PL - 8} y={py(t) + 4} textAnchor="end" fontSize={11} fill="#64748b">
              {t.toFixed(1)}
            </text>
          </g>
        ))}
        {[0, 0.25, 0.5, 0.75, 1].map((t) => (
          <text key={t} x={px(t)} y={H - PB + 18} textAnchor="middle" fontSize={11} fill="#64748b">
            {t}
          </text>
        ))}
        <text x={(W + PL - PR) / 2} y={H - 6} textAnchor="middle" fontSize={12} fill="#94a3b8">
          excitation s = (Q − Q₀)/Λ_D
        </text>
        <text x={14} y={(H - PB + PT) / 2} textAnchor="middle" fontSize={12} fill="#94a3b8"
          transform={`rotate(-90, 14, ${(H - PB + PT) / 2})`}>
          K/M⁴ (pressure)
        </text>

        <path d={path} fill="none" stroke="#22d3ee" strokeWidth={2.5} />
        <line x1={px(s)} y1={PT} x2={px(s)} y2={H - PB} stroke="#334155" strokeWidth={1} />
        <circle cx={px(s)} cy={py(k)} r={5} fill="#f59e0b" />
        <text x={px(0.02)} y={py(-1) - 8} fontSize={11} fill="#34d399">w = −1 (today)</text>
        <text x={px(0.97)} y={py(0) + 26} textAnchor="end" fontSize={11} fill="#fbbf24">the wall</text>
      </svg>

      <div className="mt-3 grid grid-cols-1 gap-3 text-sm sm:grid-cols-3">
        <div className="rounded-md border border-gray-600/40 bg-gray-800/30 px-3 py-2">
          <div className="text-gray-400">pressure −K/M⁴</div>
          <div className="font-mono text-white">{(-k).toFixed(3)}</div>
        </div>
        <div className="rounded-md border border-cyan-700/40 bg-cyan-950/20 px-3 py-2">
          <div className="text-cyan-300">a₀(s)/a₀(0) = √(−K/M⁴)</div>
          <div className="font-mono text-white">{a0ratio.toFixed(3)}</div>
        </div>
        <div className="rounded-md border border-gray-600/40 bg-gray-800/30 px-3 py-2">
          <div className="text-gray-400">regime</div>
          <div className={`text-xs ${regime.c}`}>{regime.label}</div>
        </div>
      </div>

      <input
        type="range" min={0} max={0.999} step={0.001} value={s}
        onChange={(e) => setS(parseFloat(e.target.value))}
        className="mt-4 w-full"
      />
      <p className="mt-2 text-xs text-gray-500">
        β ≡ μ²Λ_D²/M⁴ = 1 — the Lagrangian vanishes exactly at the wall — is SELECTED (by the CMB
        off-switch), not derived. With it, the a₀(z) law below is closed-form. Dark matter exists at
        full Ω_dm in this framework; the claim is &ldquo;no dark-matter particle,&rdquo; nothing stronger.
      </p>
    </div>
  );
}
