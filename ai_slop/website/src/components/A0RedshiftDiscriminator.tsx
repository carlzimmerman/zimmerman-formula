'use client';

/**
 * A0RedshiftDiscriminator
 *
 * The framework's distinctive, falsifiable prediction: the acceleration scale a0(z)
 * DECLINES with redshift as √ρ_DE(z) — separating cleanly at z≈3 from (i) ΛCDM, where
 * a0 is constant, and (ii) the rival "modified-inertia rises with cH" branch a0 ∝ cH(z).
 *
 * Built from the audited 2026 result (DOI 10.5281/zenodo.20721540):
 *   framework:  a0(z)/a0(0) = √(ρ_DE(z)/ρ_DE(0)),  a0(z=3) ≈ 0.74
 *   ΛCDM:       a0(z)/a0(0) = 1
 *   rival:      a0(z)/a0(0) = E(z) = √(Ωm(1+z)³ + ΩΛ),  ≈ 4.56 at z=3
 *
 * The declining direction is currently CONTESTED, not confirmed; this panel shows what
 * each hypothesis predicts and where the clean discriminator lies.
 */

import { useMemo, useState } from 'react';

const OMEGA_M = 0.315;
const OMEGA_LAMBDA = 0.685;

// CPL evolving dark energy (DESI-favored representative best fit)
function rhoDEratio(z: number, w0: number, wa: number): number {
  return Math.pow(1 + z, 3 * (1 + w0 + wa)) * Math.exp((-3 * wa * z) / (1 + z));
}
function aFramework(z: number, w0: number, wa: number): number {
  return Math.sqrt(rhoDEratio(z, w0, wa));
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
  const [w0, setW0] = useState(-0.75);
  const [wa, setWa] = useState(-0.86);
  const [hoverZ, setHoverZ] = useState(3);

  const px = (z: number) => PADL + (z / Z_MAX) * (W - PADL - PADR);
  const py = (y: number) => H - PADB - (y / Y_MAX) * (H - PADT - PADB);

  const paths = useMemo(() => {
    const fw: string[] = [];
    const lcdm: string[] = [];
    const rival: string[] = [];
    for (let z = 0; z <= Z_MAX + 1e-9; z += 0.05) {
      fw.push(`${px(z).toFixed(1)},${py(aFramework(z, w0, wa)).toFixed(1)}`);
      lcdm.push(`${px(z).toFixed(1)},${py(1).toFixed(1)}`);
      rival.push(`${px(z).toFixed(1)},${py(Math.min(aRival(z), Y_MAX)).toFixed(1)}`);
    }
    return {
      fw: 'M' + fw.join(' L'),
      lcdm: 'M' + lcdm.join(' L'),
      rival: 'M' + rival.join(' L'),
    };
  }, [w0, wa]);

  const vals = {
    fw: aFramework(hoverZ, w0, wa),
    lcdm: 1,
    rival: aRival(hoverZ),
  };
  const sep = vals.rival / vals.fw;

  return (
    <div className="rounded-xl border border-gray-700 bg-black/40 p-5">
      <h3 className="mb-1 text-lg font-semibold text-white">
        a₀(z): the distinctive prediction
      </h3>
      <p className="mb-4 text-sm text-gray-400">
        The framework predicts a <span className="text-cyan-300">declining</span> acceleration scale,
        a₀(z) ∝ √ρ_DE(z). It separates cleanly at z ≈ 3 from constant-Λ (ΛCDM) and from the rival
        rising branch a₀ ∝ cH(z). Move the marker; adjust the dark-energy equation of state.
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
          <div className="font-medium text-cyan-300">Framework — a₀ ∝ √ρ_DE</div>
          <div className="font-mono text-gray-300">a₀({hoverZ})/a₀(0) = {vals.fw.toFixed(2)}</div>
        </div>
        <div className="rounded-md border border-gray-600/40 bg-gray-800/30 px-3 py-2">
          <div className="font-medium text-gray-300">ΛCDM — constant</div>
          <div className="font-mono text-gray-300">a₀({hoverZ})/a₀(0) = 1.00</div>
        </div>
        <div className="rounded-md border border-orange-700/40 bg-orange-950/20 px-3 py-2">
          <div className="font-medium text-orange-300">Rival — a₀ ∝ cH(z)</div>
          <div className="font-mono text-gray-300">a₀({hoverZ})/a₀(0) = {vals.rival.toFixed(2)}</div>
        </div>
      </div>

      <p className="mt-3 text-sm text-gray-400">
        At z = {hoverZ}, the framework and the rival branch differ by a factor of{' '}
        <span className="font-mono text-white">{sep.toFixed(1)}×</span> — cleanly separable with deep-MOND
        kinematics (ELT/JWST/ALMA). The premise (does ρ_DE evolve at all?) is hostage to DESI w(z); the
        declining direction is contested, not yet confirmed.
      </p>

      {/* controls */}
      <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <label className="text-xs text-gray-400">
          dark-energy w₀ = <span className="font-mono text-gray-200">{w0.toFixed(2)}</span>
          <input
            type="range" min={-1} max={-0.5} step={0.01} value={w0}
            onChange={(e) => setW0(parseFloat(e.target.value))}
            className="mt-1 w-full"
          />
        </label>
        <label className="text-xs text-gray-400">
          dark-energy wₐ = <span className="font-mono text-gray-200">{wa.toFixed(2)}</span>
          <input
            type="range" min={-1.5} max={0} step={0.01} value={wa}
            onChange={(e) => setWa(parseFloat(e.target.value))}
            className="mt-1 w-full"
          />
        </label>
      </div>
      <p className="mt-2 text-xs text-gray-500">
        w₀ = −1, wₐ = 0 recovers a constant a₀ (ΛCDM); the DESI-favored evolving values (w₀ ≈ −0.75,
        wₐ ≈ −0.86) give a₀(z=3) ≈ 0.74. Source: a₀ = c²√(Λ/32π), DOI 10.5281/zenodo.20721540.
      </p>
    </div>
  );
}
