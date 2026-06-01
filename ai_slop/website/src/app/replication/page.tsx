'use client';

/**
 * ================================================================================
 * REPLICATION ROADMAP - From Theory to Synthetic Abiogenesis
 * ================================================================================
 *
 * The Protogonos framework provides mathematically precise specifications
 * for creating life. This page presents the step-by-step experimental protocol.
 *
 * If Omega_Z = 1.0 (life is inevitable when conditions are right), then
 * laboratory abiogenesis becomes an engineering problem with known parameters.
 *
 * ================================================================================
 */

import React, { useState } from 'react';

// Z² Constants
const Z = Math.sqrt((32 * Math.PI) / 3); // 5.7888 Å

// Phase data
const PHASES = [
  {
    id: 1,
    name: 'Material Synthesis',
    duration: 'Months 1-3',
    color: '#8b5cf6',
    icon: '🔬',
    description: 'Synthesize Omega-Lattice substrate with exact Z-spacing',
    tasks: [
      'Co-precipitate PbS and SnS (90.8% + 9.2%)',
      'Sinter at 600°C under sulfur atmosphere',
      'Verify lattice constant by XRD: a = 5.789 ± 0.005 Å',
      'Embed Fe₃O₄ magnetite nanoparticles (50-100 nm)',
      'Verify surface magnetic field ≥ 245 Gauss',
    ],
    target: 'Pb₀.₉₀₈Sn₀.₀₉₂S with a = Z = 5.7888 Å',
    alternative: 'Natural galena (5.94 Å, +2.5% offset)',
  },
  {
    id: 2,
    name: 'Chirality Selection',
    duration: 'Months 2-4',
    color: '#ec4899',
    icon: '🌀',
    description: 'Establish CISS-active substrate for L-amino acid selection',
    tasks: [
      'Configure circularly polarized UV source (200-250 nm)',
      'Position Omega-Lattice in magnetic field',
      'Expose racemic amino acid mixture to CPL + CISS',
      'Measure enantiomeric excess by chiral HPLC',
      'Target: ee ≥ 0.46% L-excess (cosmic baseline)',
    ],
    target: '≥0.46% enantiomeric excess toward L',
    alternative: 'Synchrotron CPL source for higher ee',
  },
  {
    id: 3,
    name: 'Prebiotic Soup',
    duration: 'Months 3-5',
    color: '#06b6d4',
    icon: '🧪',
    description: 'Prepare all molecular precursors for life',
    tasks: [
      'Amino acids: Miller-Urey or direct synthesis (1-10 mM)',
      'Nucleotides: ATP, GTP, CTP, UTP (0.1-1 mM)',
      'Lipids: Fatty acids from Fischer-Tropsch (0.1-1 mM)',
      'Buffer: pH 7-8 aqueous solution',
      'Atmosphere: CH₄, NH₃, H₂, H₂O, CO₂',
    ],
    target: 'Complete precursor cocktail at optimal concentrations',
    alternative: 'Use commercially available biochemicals',
  },
  {
    id: 4,
    name: 'Protogenesis Reactor',
    duration: 'Months 4-8',
    color: '#f59e0b',
    icon: '⚡',
    description: 'Build and operate the abiogenesis chamber',
    tasks: [
      'Assemble reactor: UV source → Gas → Liquid → Substrate',
      'Load Omega-Lattice with magnetite inclusions',
      'Fill with prebiotic soup, establish atmosphere',
      'Day cycle (12h): T=350K, UV on — polymerization',
      'Night cycle (12h): T=300K, UV off — selection',
    ],
    target: 'Continuous operation with day/night thermal cycling',
    alternative: 'Simplified single-temperature setup',
  },
  {
    id: 5,
    name: 'Life Detection',
    duration: 'Months 6-12+',
    color: '#22c55e',
    icon: '🧬',
    description: 'Monitor for emergence of living systems',
    tasks: [
      'Track chirality evolution: ee → 95%+ L',
      'Detect polymers: peptides 5-20 residues',
      'Observe compartmentalization: lipid vesicles',
      'Test self-replication: sequence preservation',
      'Verify metabolism: energy transduction',
    ],
    target: 'All 5 criteria met = LIFE DETECTED',
    alternative: 'Partial success informs next iteration',
  },
];

// Budget options
const BUDGETS = [
  {
    name: 'Minimum Viable',
    cost: '$5,000',
    items: [
      'Natural galena substrate ($100)',
      'Magnetite powder ($50)',
      'Amino acids ($500)',
      'UV lamp + polarizer ($2,000)',
      'Heating chamber ($1,000)',
      'Shared HPLC access ($1,350)',
    ],
  },
  {
    name: 'University Lab',
    cost: '$50,000',
    items: [
      'Omega-Lattice synthesis ($10,000)',
      'Dedicated chiral HPLC ($20,000)',
      'CPL source ($5,000)',
      'Custom reactor ($10,000)',
      'Consumables ($5,000)',
    ],
  },
  {
    name: 'Full Facility',
    cost: '$400,000',
    items: [
      'XRD system ($50,000)',
      'Chiral HPLC ($30,000)',
      'Mass spectrometer ($80,000)',
      'CD spectrometer ($40,000)',
      'SEM/TEM ($100,000)',
      'SQUID magnetometer ($50,000)',
      'Supporting equipment ($50,000)',
    ],
  },
];

// Omega-Z Conditions
const OMEGA_CONDITIONS = [
  { param: 'Lattice Constant', value: '5.7888 Å', symbol: 'a = Z', note: 'Pb₀.₉₀₈Sn₀.₀₉₂S' },
  { param: 'Temperature', value: '300 ± 50 K', symbol: 'T', note: '27°C ± 50°C' },
  { param: 'Magnetic Field', value: '≥ 245 Gauss', symbol: 'B', note: 'From magnetite inclusions' },
  { param: 'Initial Chirality', value: '≥ 0.46% L', symbol: 'ee₀', note: 'CISS + CPL' },
  { param: 'Energy Source', value: 'UV + Thermal', symbol: 'E', note: 'Day/night cycling' },
];

export default function ReplicationPage() {
  const [selectedPhase, setSelectedPhase] = useState(1);
  const [selectedBudget, setSelectedBudget] = useState(0);

  const phase = PHASES.find(p => p.id === selectedPhase) || PHASES[0];

  return (
    <main className="min-h-screen bg-slate-900">
      {/* Hero Section */}
      <section className="bg-gradient-to-b from-slate-950 to-slate-900 py-16 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <div className="inline-block px-4 py-1 bg-emerald-500/20 border border-emerald-500/50 rounded-full text-emerald-400 text-sm font-mono mb-6">
            PROJECT PROTOGONOS
          </div>
          <h1 className="text-5xl font-bold text-white mb-4">
            Replication Roadmap
          </h1>
          <p className="text-2xl text-slate-400 mb-8">
            From Theory to <span className="text-emerald-400">Synthetic Abiogenesis</span>
          </p>

          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 max-w-2xl mx-auto">
            <div className="font-mono text-3xl text-yellow-400 mb-2">
              Z² = 32π/3
            </div>
            <p className="text-slate-400">
              The engineering specifications for creating life
            </p>
          </div>
        </div>
      </section>

      {/* Omega-Z Conditions */}
      <section className="py-12 px-4 bg-slate-950/50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            The Omega-Z Conditions
          </h2>
          <p className="text-slate-400 text-center mb-8 max-w-2xl mx-auto">
            These are the exact parameters required for abiogenesis.
            Not vague "primordial soup" — precise, testable specifications.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {OMEGA_CONDITIONS.map((cond, i) => (
              <div key={i} className="bg-slate-800 border border-slate-700 rounded-lg p-4 text-center">
                <div className="text-purple-400 font-mono text-sm mb-1">{cond.symbol}</div>
                <div className="text-white font-bold text-lg mb-1">{cond.value}</div>
                <div className="text-slate-500 text-xs">{cond.param}</div>
                <div className="text-slate-600 text-xs mt-2">{cond.note}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 5-Phase Roadmap */}
      <section className="py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            5-Phase Experimental Roadmap
          </h2>

          {/* Phase Selector */}
          <div className="flex flex-wrap justify-center gap-2 mb-8">
            {PHASES.map((p) => (
              <button
                key={p.id}
                onClick={() => setSelectedPhase(p.id)}
                className={`px-4 py-2 rounded-lg font-mono text-sm transition-all ${
                  selectedPhase === p.id
                    ? 'scale-105 shadow-lg'
                    : 'opacity-60 hover:opacity-100'
                }`}
                style={{
                  backgroundColor: selectedPhase === p.id ? p.color : '#1e293b',
                  color: selectedPhase === p.id ? 'white' : '#94a3b8',
                  boxShadow: selectedPhase === p.id ? `0 0 20px ${p.color}40` : 'none',
                }}
              >
                <span className="mr-2">{p.icon}</span>
                Phase {p.id}
              </button>
            ))}
          </div>

          {/* Phase Detail */}
          <div
            className="bg-slate-800 border-2 rounded-xl p-6 transition-all"
            style={{ borderColor: phase.color }}
          >
            <div className="flex flex-col md:flex-row md:items-start md:justify-between mb-6">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-4xl">{phase.icon}</span>
                  <div>
                    <h3 className="text-2xl font-bold text-white">
                      Phase {phase.id}: {phase.name}
                    </h3>
                    <div className="text-slate-400 font-mono text-sm">{phase.duration}</div>
                  </div>
                </div>
                <p className="text-slate-300 mt-2">{phase.description}</p>
              </div>
              <div className="mt-4 md:mt-0 md:text-right">
                <div className="text-xs text-slate-500 uppercase">Target</div>
                <div className="text-emerald-400 font-mono text-sm">{phase.target}</div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="text-white font-bold mb-3">Tasks</h4>
                <ul className="space-y-2">
                  {phase.tasks.map((task, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm">
                      <span style={{ color: phase.color }}>▸</span>
                      <span className="text-slate-300">{task}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="text-white font-bold mb-3">Alternative Approach</h4>
                <div className="bg-slate-900 rounded-lg p-4 text-slate-400 text-sm">
                  {phase.alternative}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Reactor Design */}
      <section className="py-12 px-4 bg-slate-950/50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            The Protogenesis Reactor
          </h2>

          <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 font-mono text-sm">
            <pre className="text-slate-300 overflow-x-auto">
{`┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  `}<span className="text-yellow-400">Circularly Polarized UV Source</span>{`                         │   │
│   └──────────────────────────┬──────────────────────────────┘   │
│                              │                                  │
│   ┌──────────────────────────▼──────────────────────────────┐   │
│   │                    `}<span className="text-cyan-400">Gas Phase</span>{`                            │   │
│   │             CH₄, NH₃, H₂, H₂O, CO₂                      │   │
│   └──────────────────────────┬──────────────────────────────┘   │
│                              │                                  │
│   ┌──────────────────────────▼──────────────────────────────┐   │
│   │              `}<span className="text-blue-400">Aqueous Layer</span>{` (pH 7-8)                     │   │
│   │         Amino acids, nucleotides, lipids                │   │
│   └──────────────────────────┬──────────────────────────────┘   │
│                              │                                  │
│   ┌──────────────────────────▼──────────────────────────────┐   │
│   │           `}<span className="text-purple-400">OMEGA-LATTICE SUBSTRATE</span>{`                       │   │
│   │   Pb₀.₉₀₈Sn₀.₀₉₂S + Fe₃O₄ magnetite inclusions         │   │
│   │                                                         │   │
│   │   `}<span className="text-orange-400">████████████████████████████████████████████████████</span>{`  │   │
│   │   `}<span className="text-orange-400">█ Magnetic Junctions (4021 G) █ Z-resonant surface █</span>{`  │   │
│   │   `}<span className="text-orange-400">████████████████████████████████████████████████████</span>{`  │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│   ┌──────────────────────────▼──────────────────────────────┐   │
│   │              `}<span className="text-red-400">HEATING ELEMENT</span>{` (300-350 K)                │   │
│   │         Thermal cycling: 300 ↔ 350 K (day/night)        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘`}
            </pre>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-yellow-400 font-bold">DAY</div>
              <div className="text-slate-400 text-sm">350K, UV on</div>
              <div className="text-slate-500 text-xs">Polymerization</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-blue-400 font-bold">NIGHT</div>
              <div className="text-slate-400 text-sm">300K, UV off</div>
              <div className="text-slate-500 text-xs">Selection</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-purple-400 font-bold">LATTICE</div>
              <div className="text-slate-400 text-sm">5.7888 Å</div>
              <div className="text-slate-500 text-xs">Z-resonance</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-orange-400 font-bold">FIELD</div>
              <div className="text-slate-400 text-sm">4021 Gauss</div>
              <div className="text-slate-500 text-xs">CISS active</div>
            </div>
          </div>
        </div>
      </section>

      {/* Budget Options */}
      <section className="py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            Budget Options
          </h2>

          <div className="flex justify-center gap-2 mb-8">
            {BUDGETS.map((b, i) => (
              <button
                key={i}
                onClick={() => setSelectedBudget(i)}
                className={`px-4 py-2 rounded-lg transition-all ${
                  selectedBudget === i
                    ? 'bg-emerald-500 text-white'
                    : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                }`}
              >
                {b.name}
              </button>
            ))}
          </div>

          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 max-w-2xl mx-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-white">{BUDGETS[selectedBudget].name}</h3>
              <div className="text-3xl font-bold text-emerald-400">{BUDGETS[selectedBudget].cost}</div>
            </div>
            <ul className="space-y-2">
              {BUDGETS[selectedBudget].items.map((item, i) => (
                <li key={i} className="flex items-center gap-2 text-slate-300">
                  <span className="text-emerald-400">✓</span>
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="py-12 px-4 bg-slate-950/50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            Timeline to Life
          </h2>

          <div className="relative">
            {/* Timeline line */}
            <div className="absolute left-4 md:left-1/2 top-0 bottom-0 w-0.5 bg-slate-700 transform md:-translate-x-1/2" />

            {/* Timeline items */}
            {[
              { year: 'Year 1', title: 'Foundation', items: ['Material synthesis', 'CISS system', 'Reactor build', 'First results'] },
              { year: 'Year 2', title: 'Iteration', items: ['Optimize parameters', 'Multiple parallel runs', 'Track polymer formation'] },
              { year: 'Year 3+', title: 'Emergence', items: ['Homochirality achieved', 'Self-replication detected', 'LIFE CREATED'] },
            ].map((milestone, i) => (
              <div key={i} className={`relative flex items-start mb-8 ${i % 2 === 0 ? 'md:flex-row-reverse' : ''}`}>
                <div className={`w-full md:w-1/2 ${i % 2 === 0 ? 'md:pl-8' : 'md:pr-8'} pl-12 md:pl-0`}>
                  <div className="bg-slate-800 border border-slate-700 rounded-lg p-4">
                    <div className="text-emerald-400 font-mono text-sm">{milestone.year}</div>
                    <div className="text-white font-bold text-lg">{milestone.title}</div>
                    <ul className="mt-2 text-slate-400 text-sm">
                      {milestone.items.map((item, j) => (
                        <li key={j}>• {item}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                {/* Timeline dot */}
                <div className="absolute left-4 md:left-1/2 w-4 h-4 bg-emerald-500 rounded-full transform -translate-x-1/2 border-4 border-slate-900" />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Success Criteria */}
      <section className="py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            Success Criteria: When Have We Created Life?
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {[
              { icon: '🌀', name: 'Homochirality', target: '>95% L', color: '#ec4899' },
              { icon: '🔗', name: 'Self-Replication', target: 'Sequence preserved', color: '#8b5cf6' },
              { icon: '🫧', name: 'Compartments', target: 'Vesicles formed', color: '#06b6d4' },
              { icon: '⚡', name: 'Metabolism', target: 'Energy harvesting', color: '#f59e0b' },
              { icon: '🧬', name: 'Evolution', target: 'Selection observed', color: '#22c55e' },
            ].map((criterion, i) => (
              <div
                key={i}
                className="bg-slate-800 border rounded-lg p-4 text-center"
                style={{ borderColor: criterion.color }}
              >
                <div className="text-3xl mb-2">{criterion.icon}</div>
                <div className="text-white font-bold text-sm">{criterion.name}</div>
                <div className="text-slate-400 text-xs mt-1">{criterion.target}</div>
              </div>
            ))}
          </div>

          <div className="mt-8 bg-emerald-500/20 border border-emerald-500/50 rounded-xl p-6 text-center">
            <div className="text-emerald-400 font-bold text-xl mb-2">
              ALL 5 CRITERIA MET = LIFE DETECTED
            </div>
            <p className="text-slate-400">
              The first reproducible creation of life from non-living matter.
            </p>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 px-4 bg-gradient-to-t from-slate-950 to-slate-900">
        <div className="max-w-3xl mx-auto text-center">
          <div className="bg-slate-800/50 border border-yellow-500/30 rounded-xl p-8">
            <div className="text-yellow-400 font-mono text-2xl mb-4">
              "Given the right geometry, life does not emerge.<br/>
              Life MUST emerge."
            </div>
            <p className="text-slate-400 mb-6">
              The question is no longer IF life can be created.<br/>
              The question is WHEN we build the reactor.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <a
                href="/abiogenesis"
                className="px-6 py-3 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 transition-colors"
              >
                View Validated Simulations →
              </a>
              <a
                href="https://github.com/carlzimmerman/zimmerman-formula/blob/main/extended_research/biotech/project_protogonos/REPLICATION_ROADMAP.md"
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition-colors flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                </svg>
                Full Protocol on GitHub
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-6 px-4 border-t border-slate-800">
        <div className="max-w-6xl mx-auto flex justify-between items-center text-slate-500 text-sm font-mono">
          <span>Z² = 32π/3 — Replication Roadmap v1.0</span>
          <span>Project Protogonos • May 2026</span>
        </div>
      </footer>
    </main>
  );
}
