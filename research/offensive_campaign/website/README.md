# Z2 Framework Website Components

React/Next.js visualization components for displaying the parity-odd 4PCF evidence demonstrating T³/Z₂ cosmic topology.

## Key Result

**NGC-SGC Correlation: r = 0.9986**

This near-perfect correlation indicates globally coherent parity violation, exactly as predicted by T³/Z₂ topology.

## Components

### Z2ParityOddVisualization
Main visualization component displaying the correlation chart, Z2 tests, and physics interpretation.

```tsx
import { Z2ParityOddVisualization } from './website';

<Z2ParityOddVisualization data={visualizationData} />
```

### InteractiveScatterPlot
Interactive scatter plot showing NGC vs SGC parity-odd 4PCF values using Recharts.

```tsx
import { InteractiveScatterPlot } from './website';

<InteractiveScatterPlot data={multipoleData} correlation={0.9986} />
```

### ParityOddPage
Complete page component with header, footer, and all visualizations.

```tsx
import { ParityOddPage } from './website';

// In pages/4pcf.tsx
export default ParityOddPage;
```

## Data Files

- `z2_4pcf_visualization_data.json` - Complete visualization data structure
- Copy to `public/data/` in your Next.js app

## Dependencies

```bash
npm install recharts
# or
yarn add recharts
```

## Usage in Next.js

1. Copy components to your `components/z2/` directory
2. Copy `z2_4pcf_visualization_data.json` to `public/data/`
3. Import and use:

```tsx
// pages/evidence/4pcf.tsx
import { Z2ParityOddVisualization, loadVisualizationData } from '@/components/z2';
import { useEffect, useState } from 'react';

export default function ParityOddEvidencePage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    loadVisualizationData().then(setData);
  }, []);

  if (!data) return <div>Loading...</div>;

  return <Z2ParityOddVisualization data={data} />;
}
```

## Color Scheme

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Blue | #2E86AB | BOSS CMASS data |
| Purple | #A23B72 | DESI 50k data |
| Orange | #F18F01 | DESI 200k data |
| Success Green | #28A745 | Passed tests |
| Danger Red | #DC3545 | Failed tests |

## Scientific Context

The parity-odd 4-point correlation function (4PCF) measures chirality in galaxy clustering:

- **T³/Z₂ topology predicts**: Global chirality (r ~ 1)
- **Local physics predicts**: Independent chirality per region (r ~ 0)
- **Observed**: r = 0.9986 (extremely strong evidence for T³/Z₂)

## Data Sources

- **BOSS CMASS**: Philcox et al. (2022), ~500k galaxies
- **DESI DR1**: This work, 200k galaxies per region
- **Algorithm**: Philcox encore (NPCF estimator)

## License

MIT License - See main repository LICENSE file.
