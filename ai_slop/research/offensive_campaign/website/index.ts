/**
 * Z2 Framework Website Components
 *
 * Visualization components for displaying parity-odd 4PCF evidence
 * demonstrating T3/Z2 cosmic topology
 */

// Main visualization components
export { Z2ParityOddVisualization, KeyResultBanner, CorrelationChart, Z2TestResults, PhysicsInterpretation } from './Z2ParityOddVisualization';

// Full page component
export { ParityOddPage } from './ParityOddPage';

// Interactive charts
export { InteractiveScatterPlot, generateSampleData } from './InteractiveScatterPlot';

// Data loading utility
export const loadVisualizationData = async () => {
  const response = await fetch('/data/z2_4pcf_visualization_data.json');
  return response.json();
};

// Type exports
export interface CorrelationDataPoint {
  label: string;
  value: number;
  color: string;
}

export interface Z2TestResult {
  name: string;
  description: string;
  result: 'PASS' | 'FAIL';
  evidence: string;
}

export interface MultipoleDataPoint {
  ngc: number;
  sgc: number;
  l1: number;
  l2: number;
  l3: number;
  bin: number;
}
