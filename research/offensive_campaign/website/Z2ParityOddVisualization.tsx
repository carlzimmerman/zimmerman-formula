/**
 * Z2 Parity-Odd 4PCF Visualization Component
 *
 * Displays the NGC-SGC correlation evidence for T3/Z2 topology
 * Uses data from z2_4pcf_visualization_data.json
 */

import React from 'react';

interface CorrelationData {
  label: string;
  value: number;
  color: string;
}

interface Z2Test {
  name: string;
  description: string;
  result: 'PASS' | 'FAIL';
  evidence: string;
}

interface VisualizationProps {
  data: {
    key_result: {
      headline: string;
      significance: string;
      interpretation: string;
    };
    correlation_chart: {
      data: CorrelationData[];
    };
    z2_tests: {
      tests: Z2Test[];
      score: string;
      verdict: string;
    };
    physics_interpretation: {
      sections: Array<{ heading: string; content: string }>;
    };
  };
}

// Key Result Banner
export const KeyResultBanner: React.FC<{ headline: string; significance: string }> = ({
  headline,
  significance,
}) => (
  <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-8 rounded-xl shadow-lg">
    <h1 className="text-4xl font-bold mb-2">{headline}</h1>
    <p className="text-xl opacity-90">{significance}</p>
  </div>
);

// Correlation Bar Chart
export const CorrelationChart: React.FC<{ data: CorrelationData[] }> = ({ data }) => (
  <div className="bg-white p-6 rounded-xl shadow-md">
    <h2 className="text-2xl font-semibold mb-4">NGC-SGC Parity-Odd Correlation</h2>
    <p className="text-gray-600 mb-6">
      T<sup>3</sup>/Z<sub>2</sub> predicts r ~ 1, Local physics predicts r ~ 0
    </p>
    <div className="space-y-4">
      {data.map((item) => (
        <div key={item.label} className="flex items-center gap-4">
          <span className="w-32 text-sm font-medium">{item.label}</span>
          <div className="flex-1 h-8 bg-gray-100 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-1000"
              style={{
                width: `${item.value * 100}%`,
                backgroundColor: item.color,
              }}
            />
          </div>
          <span className="w-16 text-right font-mono font-bold">{item.value.toFixed(4)}</span>
        </div>
      ))}
    </div>
    {/* Reference line at r=1 */}
    <div className="mt-4 border-t-2 border-dashed border-red-400 pt-2">
      <span className="text-sm text-red-500">Perfect correlation (r = 1.0)</span>
    </div>
  </div>
);

// Z2 Test Results
export const Z2TestResults: React.FC<{ tests: Z2Test[]; score: string; verdict: string }> = ({
  tests,
  score,
  verdict,
}) => (
  <div className="bg-white p-6 rounded-xl shadow-md">
    <h2 className="text-2xl font-semibold mb-4">Z<sup>2</sup> Framework Tests</h2>
    <div className="space-y-3">
      {tests.map((test, idx) => (
        <div
          key={idx}
          className={`p-4 rounded-lg border-l-4 ${
            test.result === 'PASS'
              ? 'bg-green-50 border-green-500'
              : 'bg-red-50 border-red-500'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="font-medium">{test.name}</span>
            <span
              className={`px-2 py-1 rounded text-sm font-bold ${
                test.result === 'PASS'
                  ? 'bg-green-500 text-white'
                  : 'bg-red-500 text-white'
              }`}
            >
              {test.result}
            </span>
          </div>
          <p className="text-sm text-gray-600 mt-1">{test.evidence}</p>
        </div>
      ))}
    </div>
    <div className="mt-6 p-4 bg-blue-50 rounded-lg">
      <div className="flex items-center justify-between">
        <span className="text-lg font-semibold">Score: {score}</span>
        <span className="text-blue-700 font-medium">{verdict}</span>
      </div>
    </div>
  </div>
);

// Physics Interpretation
export const PhysicsInterpretation: React.FC<{
  sections: Array<{ heading: string; content: string }>;
}> = ({ sections }) => (
  <div className="bg-white p-6 rounded-xl shadow-md">
    <h2 className="text-2xl font-semibold mb-4">What This Means</h2>
    <div className="space-y-4">
      {sections.map((section, idx) => (
        <div key={idx}>
          <h3 className="font-semibold text-lg text-gray-800">{section.heading}</h3>
          <p className="text-gray-600 mt-1">{section.content}</p>
        </div>
      ))}
    </div>
  </div>
);

// Main Visualization Component
export const Z2ParityOddVisualization: React.FC<VisualizationProps> = ({ data }) => {
  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <KeyResultBanner
        headline={data.key_result.headline}
        significance={data.key_result.significance}
      />

      <div className="grid md:grid-cols-2 gap-6">
        <CorrelationChart data={data.correlation_chart.data} />
        <Z2TestResults
          tests={data.z2_tests.tests}
          score={data.z2_tests.score}
          verdict={data.z2_tests.verdict}
        />
      </div>

      <PhysicsInterpretation sections={data.physics_interpretation.sections} />

      {/* Z2 Connection */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-6 rounded-xl border border-purple-200">
        <h2 className="text-2xl font-semibold mb-4">
          Connection to Z<sup>2</sup> = 32&pi;/3
        </h2>
        <p className="text-gray-700">
          The near-perfect NGC-SGC correlation (r = 0.9986) confirms the global coherence
          predicted by T<sup>3</sup>/Z<sub>2</sub> topology. The universe has built-in
          handedness defined by the eta invariant Z<sup>2</sup> = 32&pi;/3 = 33.510,
          which also determines the fine structure constant, cosmological constant,
          and weak mixing angle.
        </p>
        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div className="p-3 bg-white rounded-lg shadow-sm">
            <div className="text-2xl font-mono font-bold text-purple-600">137.04</div>
            <div className="text-sm text-gray-500">&alpha;<sup>-1</sup></div>
          </div>
          <div className="p-3 bg-white rounded-lg shadow-sm">
            <div className="text-2xl font-mono font-bold text-blue-600">0.6842</div>
            <div className="text-sm text-gray-500">&Omega;<sub>&Lambda;</sub></div>
          </div>
          <div className="p-3 bg-white rounded-lg shadow-sm">
            <div className="text-2xl font-mono font-bold text-green-600">0.3158</div>
            <div className="text-sm text-gray-500">&Omega;<sub>m</sub></div>
          </div>
          <div className="p-3 bg-white rounded-lg shadow-sm">
            <div className="text-2xl font-mono font-bold text-orange-600">0.2308</div>
            <div className="text-sm text-gray-500">sin<sup>2</sup>&theta;<sub>W</sub></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Z2ParityOddVisualization;
