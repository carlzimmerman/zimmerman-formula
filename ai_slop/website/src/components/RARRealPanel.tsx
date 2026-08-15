'use client';

/**
 * RARRealPanel — the radial acceleration relation on the REAL SPARC sample.
 * Data: /data/rar_real_sparc.json — 3,389 (g_bar, g_obs) points from the 175
 * SPARC *_rotmod.dat files at the committed convention (Υ_disk = Υ_bulge = 0.70),
 * exported directly from the repository's committed pipeline. No synthetic points.
 * Curves: Newtonian identity, the a₀-line g_obs = √(g_bar² + a₀ g_bar), and the
 * Milgrom–Sanders (2008) kernel g_obs = g_bar·ν(g_bar/a₀), ν(y) = 1/(1−e^(−√y)),
 * at the canonical footing a₀ = 9.3619×10⁻¹¹ m s⁻² (alt footing toggle: 1.1279×10⁻¹⁰).
 */

import { useEffect, useMemo, useState } from 'react';

const A0_CAN = 9.3619e-11;
const A0_ALT = 1.1279e-10;
const LGMIN = -12.6;
const LGMAX = -8.4;
const W = 720;
const H = 560;
const PL = 64;
const PB = 48;
const PT = 20;
const PR = 20;

function nuMS08(y: number): number {
  return 1.0 / (1.0 - Math.exp(-Math.sqrt(y)));
}

export default function RARRealPanel() {
  const [pts, setPts] = useState<number[][] | null>(null);
  const [footing, setFooting] = useState<'can' | 'alt'>('can');
  const a0 = footing === 'can' ? A0_CAN : A0_ALT;

  useEffect(() => {
    fetch('/data/rar_real_sparc.json')
      .then((r) => r.json())
      .then((d) => setPts(d.points))
      .catch(() => setPts([]));
  }, []);

  const px = (lg: number) => PL + ((lg - LGMIN) / (LGMAX - LGMIN)) * (W - PL - PR);
  const py = (lg: number) => H - PB - ((lg - LGMIN) / (LGMAX - LGMIN)) * (H - PT - PB);

  const curves = useMemo(() => {
    const line: string[] = [];
    const ms08: string[] = [];
    const newt: string[] = [];
    for (let lg = LGMIN; lg <= LGMAX + 1e-9; lg += 0.04) {
      const gb = Math.pow(10, lg);
      const y = gb / a0;
      line.push(`${px(lg).toFixed(1)},${py(Math.log10(Math.sqrt(gb * gb + gb * a0))).toFixed(1)}`);
      ms08.push(`${px(lg).toFixed(1)},${py(Math.log10(gb * nuMS08(y))).toFixed(1)}`);
      newt.push(`${px(lg).toFixed(1)},${py(lg).toFixed(1)}`);
    }
    return {
      line: 'M' + line.join(' L'),
      ms08: 'M' + ms08.join(' L'),
      newt: 'M' + newt.join(' L'),
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [a0]);

  const scatter = useMemo(() => {
    if (!pts || pts.length === 0) return null;
    let s = 0;
    let n = 0;
    for (const [lgb, lgo] of pts) {
      const gb = Math.pow(10, lgb);
      const pred = Math.log10(Math.sqrt(gb * gb + gb * a0));
      s += (lgo - pred) * (lgo - pred);
      n += 1;
    }
    return Math.sqrt(s / n);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pts, a0]);

  return (
    <div className="rounded-xl border border-gray-700 bg-black/40 p-5">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <h3 className="text-lg font-semibold text-white">
          The relation, on the real data: 175 galaxies, {pts ? pts.length.toLocaleString() : '…'} points
        </h3>
        <button
          onClick={() => setFooting(footing === 'can' ? 'alt' : 'can')}
          className="rounded-md border border-gray-600 px-3 py-1 text-xs text-gray-300 hover:border-gray-400"
        >
          footing: {footing === 'can' ? 'canonical a₀ = 9.36×10⁻¹¹' : 'alt a₀ = 1.13×10⁻¹⁰'} — click to switch
        </button>
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
        {[-12, -11, -10, -9].map((t) => (
          <g key={t}>
            <line x1={px(t)} y1={PT} x2={px(t)} y2={H - PB} stroke="#1e293b" strokeWidth={1} />
            <line x1={PL} y1={py(t)} x2={W - PR} y2={py(t)} stroke="#1e293b" strokeWidth={1} />
            <text x={px(t)} y={H - PB + 18} textAnchor="middle" fontSize={11} fill="#64748b">
              10{'⁻'}{String(-t).split('').map((c) => '⁰¹²³⁴⁵⁶⁷⁸⁹'[+c]).join('')}
            </text>
            <text x={PL - 8} y={py(t) + 4} textAnchor="end" fontSize={11} fill="#64748b">
              10{'⁻'}{String(-t).split('').map((c) => '⁰¹²³⁴⁵⁶⁷⁸⁹'[+c]).join('')}
            </text>
          </g>
        ))}
        <text x={(W + PL - PR) / 2} y={H - 8} textAnchor="middle" fontSize={12} fill="#94a3b8">
          g_bar — the acceleration the baryons alone provide [m s⁻²]
        </text>
        <text x={16} y={(H - PB + PT) / 2} textAnchor="middle" fontSize={12} fill="#94a3b8"
          transform={`rotate(-90, 16, ${(H - PB + PT) / 2})`}>
          g_obs — the acceleration actually observed [m s⁻²]
        </text>

        {pts &&
          pts.map(([lgb, lgo], i) => (
            <circle key={i} cx={px(lgb)} cy={py(lgo)} r={1.3} fill="#38bdf8" opacity={0.18} />
          ))}

        <path d={curves.newt} fill="none" stroke="#64748b" strokeWidth={1.5} strokeDasharray="3 4" />
        <path d={curves.ms08} fill="none" stroke="#f59e0b" strokeWidth={2} strokeDasharray="6 4" />
        <path d={curves.line} fill="none" stroke="#22d3ee" strokeWidth={2.2} />
      </svg>

      <div className="mt-3 grid grid-cols-1 gap-3 text-sm sm:grid-cols-3">
        <div className="rounded-md border border-cyan-700/40 bg-cyan-950/20 px-3 py-2">
          <div className="font-medium text-cyan-300">the a₀-line (exact law)</div>
          <div className="text-gray-300">g_obs = √(g_bar² + a₀ g_bar)</div>
        </div>
        <div className="rounded-md border border-amber-700/40 bg-amber-950/20 px-3 py-2">
          <div className="font-medium text-amber-300">MS08 kernel (operative)</div>
          <div className="text-gray-300">g_obs = g_bar·ν(g_bar/a₀)</div>
        </div>
        <div className="rounded-md border border-gray-600/40 bg-gray-800/30 px-3 py-2">
          <div className="font-medium text-gray-300">Newtonian (no dark sector)</div>
          <div className="text-gray-300">g_obs = g_bar</div>
        </div>
      </div>

      <p className="mt-3 text-sm text-gray-400">
        Every dot is a measured point on a real rotation curve (SPARC, Lelli–McGaugh–Schombert 2016),
        at fixed mass-to-light Υ = 0.70 — no per-galaxy tuning.{' '}
        {scatter && (
          <>RMS scatter about the a₀-line computed live from these points:{' '}
            <span className="font-mono text-white">{scatter.toFixed(3)} dex</span> (all points, no
            quality cuts; the committed pipeline&rsquo;s quality-cut value is 0.108 dex).{' '}
          </>
        )}
        The anchored a₀ costs nothing against a fitted one — anchoring is cost-free, not
        &ldquo;better.&rdquo;
      </p>
    </div>
  );
}
