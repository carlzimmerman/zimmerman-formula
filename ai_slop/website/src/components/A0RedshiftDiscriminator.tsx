'use client';

/**
 * A0RedshiftDiscriminator — the a₀(z) panel, updated August 2026 to the DERIVED law.
 *
 * The framework's a₀(z) is now derived from the action (the MOND scale is the dark
 * sector's pressure): a₀²(z)/a₀²(0) = √(1+ν₀²)/√(1+ν₀²(1+z)⁶), with the dimensionless
 * charge ν₀ pinned to [2.14×10⁻⁵, 1.77×10⁻⁴] by the CMB off-switch (below) and the RAR
 * (above). Below the transition z_t = ν₀^(−1/3) − 1 ≈ 17–35 the law is FLAT to <1% —
 * indistinguishable from constant-a₀ everywhere rotation data exist — and it is OFF at
 * recombination as an output. The earlier CPL-dressed declining law (a₀(z=3) ≈ 0.74) is
 * WITHDRAWN and kept only in the retracted-work archive.
 *
 * The rival "Hubble-tracking" reading a₀ ∝ cH(z) rises as E(z) and is disfavoured ~2σ
 * by the credible 1 < z < 5 baryonic Tully–Fisher data (two of three usable tests move
 * the wrong direction for it). Falsifier for the flat law, either sign: a robust BTFR
 * zero-point shift of 0.15 dex in gas-dominated systems at z ≤ 1.
 */

import { useMemo, useState } from 'react';

const OMEGA_M = 0.315;
const OMEGA_LAMBDA = 0.685;
const NU0_LOG_MIN = Math.log10(2.14e-5);
const NU0_LOG_MAX = Math.log10(1.77e-4);

// the derived law: a0(z)/a0(0) = [(1+nu0^2)/(1+nu0^2 (1+z)^6)]^(1/4)
function aFramework(z: number, nu0: number): number {
  return Math.pow((1 + nu0 * nu0) / (1 + nu0 * nu0 * Math.pow(1 + z, 6)), 0.25);
}
function aRival(z: number): number {
  return Math.sqrt(OMEGA_M * Math.pow(1 + z, 3) + OMEGA_LAMBDA); // E(z)
}

const Z_MAX = 4;
const Y_MAX = 5;
const W = 720;
const H = 440;
const PADL = 64;
const PADB = 48;
const PADT = 24;
const PADR = 24;

export default function A0RedshiftDiscriminator() {
  const [logNu0, setLogNu0] = useState(Math.log10(1.77e-4));
  const [hoverZ, setHoverZ] = useState(3);
  const nu0 = Math.pow(10, logNu0);
  const zT = Math.pow(nu0, -1 / 3) - 1;

  const px = (z: number) => PADL + (z / Z_MAX) * (W - PADL - PADR);
  const py = (y: number) => H - PADB - (y / Y_MAX) * (H - PADT - PADB);

  const paths = useMemo(() => {
    const fw: string[] = [];
    const lcdm: string[] = [];
    const rival: string[] = [];
    for (let z = 0; z <= Z_MAX + 1e-9; z += 0.05) {
      fw.push(`${px(z).toFixed(1)},${py(aFramework(z, nu0)).toFixed(1)}`);
      lcdm.push(`${px(z).toFixed(1)},${py(1).toFixed(1)}`);
      rival.push(`${px(z).toFixed(1)},${py(Math.min(aRival(z), Y_MAX)).toFixed(1)}`);
    }
    return {
      fw: 'M' + fw.join(' L'),
      lcdm: 'M' + lcdm.join(' L'),
      rival: 'M' + rival.join(' L'),
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [nu0]);

  const vals = {
    fw: aFramework(hoverZ, nu0),
    lcdm: 1,
    rival: aRival(hoverZ),
  };
  const sep = vals.rival / vals.fw;

  return (
    <div className="rounded-xl border border-gray-700 bg-black/40 p-5">
      <h3 className="mb-1 text-lg font-semibold text-white">
        a₀(z): flat where testable — and that is the prediction
      </h3>
      <p className="mb-4 text-sm text-gray-400">
        The derived law (August 2026) keeps a₀ <span className="text-cyan-300">constant to &lt;1%</span>{' '}
        everywhere rotation data exist (z ≲ 5) and switches off only above z_t ≈ 17–35 — so on this
        plot it sits on top of the constant-a₀ line, and the observed <em>absence</em> of
        Tully&ndash;Fisher zero-point evolution at 1 &lt; z &lt; 5 is a pass, not a tension. The rival{' '}
        <span className="text-orange-300">Hubble-tracking</span> reading a₀ ∝ cH(z) rises as E(z) and
        is disfavoured ~2σ by those same data.
      </p>

      <svg
        viewBox={`0 0 ${W} ${H}`}
        className="w-full"
        onMouseMove={(e) => {
          const r = (e.currentTarget as SVGSVGElement).getBoundingClientRect();
          const zx = ((e.clientX - r.left) / r.width) * W;
          const z = Math.max(0, Math.min(Z_MAX, ((zx - PADL) / (W - PADL - PADR)) * Z_MAX));
          setHoverZ(Number(z.toFixed(2)));
        }}
      >
        {/* axes */}
        <line x1={PADL} y1={H - PADB} x2={W - PADR} y2={H - PADB} stroke="#475569" strokeWidth={1} />
        <line x1={PADL} y1={PADT} x2={PADL} y2={H - PADB} stroke="#475569" strokeWidth={1} />
        {/* y gridlines */}
        {[0, 1, 2, 3, 4, 5].map((y) => (
          <g key={y}>
            <line x1={PADL} y1={py(y)} x2={W - PADR} y2={py(y)} stroke="#1e293b" strokeWidth={1} />
            <text x={PADL - 8} y={py(y) + 4} textAnchor="end" fontSize={11} fill="#64748b">
              {y.toFixed(0)}
            </text>
          </g>
        ))}
        {/* x ticks */}
        {[0, 1, 2, 3, 4].map((z) => (
          <text key={z} x={px(z)} y={H - PADB + 18} textAnchor="middle" fontSize={11} fill="#64748b">
            {z}
          </text>
        ))}
        <text x={(W - PADR + PADL) / 2} y={H - 8} textAnchor="middle" fontSize={12} fill="#94a3b8">
          redshift z
        </text>
        <text
          x={16}
          y={(H - PADB + PADT) / 2}
          textAnchor="middle"
          fontSize={12}
          fill="#94a3b8"
          transform={`rotate(-90, 16, ${(H - PADB + PADT) / 2})`}
        >
          a₀(z) / a₀(0)
        </text>

        {/* curves */}
        <path d={paths.rival} fill="none" stroke="#f97316" strokeWidth={2} strokeDasharray="5 4" />
        <path d={paths.lcdm} fill="none" stroke="#94a3b8" strokeWidth={2} strokeDasharray="2 4" />
        <path d={paths.fw} fill="none" stroke="#22d3ee" strokeWidth={2.5} />

        {/* hover marker + readouts */}
        <line x1={px(hoverZ)} y1={PADT} x2={px(hoverZ)} y2={H - PADB} stroke="#334155" strokeWidth={1} />
        <circle cx={px(hoverZ)} cy={py(Math.min(vals.rival, Y_MAX))} r={3.5} fill="#f97316" />
        <circle cx={px(hoverZ)} cy={py(1)} r={3.5} fill="#94a3b8" />
        <circle cx={px(hoverZ)} cy={py(vals.fw)} r={3.5} fill="#22d3ee" />
      </svg>

      {/* legend + readout */}
      <div className="mt-3 grid grid-cols-1 gap-3 text-sm sm:grid-cols-3">
        <div className="rounded-md border border-cyan-700/40 bg-cyan-950/20 px-3 py-2">
          <div className="font-medium text-cyan-300">Derived law — flat below z_t</div>
          <div className="font-mono text-gray-300">a₀({hoverZ})/a₀(0) = {vals.fw.toFixed(4)}</div>
        </div>
        <div className="rounded-md border border-gray-600/40 bg-gray-800/30 px-3 py-2">
          <div className="font-medium text-gray-300">Constant a₀ (classic MOND / ΛCDM)</div>
          <div className="font-mono text-gray-300">a₀({hoverZ})/a₀(0) = 1.00</div>
        </div>
        <div className="rounded-md border border-orange-700/40 bg-orange-950/20 px-3 py-2">
          <div className="font-medium text-orange-300">Hubble-tracking — a₀ ∝ cH(z)</div>
          <div className="font-mono text-gray-300">a₀({hoverZ})/a₀(0) = {vals.rival.toFixed(2)}</div>
        </div>
      </div>

      <p className="mt-3 text-sm text-gray-400">
        At z = {hoverZ}, the derived law and the Hubble-tracking reading differ by{' '}
        <span className="font-mono text-white">{sep.toFixed(1)}×</span> — and existing 1 &lt; z &lt; 5
        Tully&ndash;Fisher data already disfavour the rising reading at ~2σ. The derived law is
        indistinguishable from constant-a₀ below z_t; its pre-stated falsifier, either sign, is a
        robust zero-point shift of 0.15 dex in gas-dominated systems at z ≤ 1 (SKA-class HI samples
        reach this).
      </p>

      {/* control */}
      <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <label className="text-xs text-gray-400">
          dimensionless charge ν₀ = <span className="font-mono text-gray-200">{nu0.toExponential(2)}</span>
          {' '}(transition z_t ≈ <span className="font-mono text-gray-200">{zT.toFixed(0)}</span>)
          <input
            type="range" min={NU0_LOG_MIN} max={NU0_LOG_MAX} step={0.01} value={logNu0}
            onChange={(e) => setLogNu0(parseFloat(e.target.value))}
            className="mt-1 w-full"
          />
        </label>
      </div>
      <p className="mt-2 text-xs text-gray-500">
        a₀²(z)/a₀²(0) = √(1+ν₀²)/√(1+ν₀²(1+z)⁶), with ν₀ pinned to [2.1×10⁻⁵, 1.8×10⁻⁴] by the CMB
        off-switch (below) and the radial-acceleration relation (above). MOND is off at recombination
        as an output. The earlier declining-a₀ law (a₀(z=3) ≈ 0.74) is withdrawn — see Retracted work.
      </p>
    </div>
  );
}
