/**
 * =============================================================================
 * GEOMETRIC GRAVITY - COSMOS-Web MOND Visualization
 * =============================================================================
 *
 * Directive UUUU: Visualize JWST COSMOS-Web weak lensing with MOND overlay
 * showing where Modified Newtonian Dynamics predicts no dark matter needed.
 *
 * Features:
 * - Convergence κ map as height field
 * - MOND regime coloring (green=MOND, purple=Newtonian)
 * - Mass peak markers
 * - Boundary contribution vectors
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { useFrame, extend } from '@react-three/fiber';
import { shaderMaterial, Text, Line } from '@react-three/drei';

// =============================================================================
// SHADER DEFINITIONS
// =============================================================================

const MONDShaderMaterial = shaderMaterial(
  {
    time: 0,
    kappaTexture: null,
    regimeTexture: null,
    showMOND: true,
    heightScale: 2.0,
    deepMONDColor: new THREE.Color('#2ECC71'),     // Green
    transitionalColor: new THREE.Color('#F39C12'), // Orange
    newtonianColor: new THREE.Color('#9B59B6'),    // Purple
  },
  // Vertex shader
  `
    uniform float time;
    uniform float heightScale;
    uniform sampler2D kappaTexture;

    varying vec2 vUv;
    varying float vKappa;
    varying float vHeight;

    void main() {
      vUv = uv;

      // Sample convergence for height
      vec4 kappaSample = texture2D(kappaTexture, uv);
      vKappa = kappaSample.r;
      vHeight = vKappa * heightScale;

      // Displace vertex
      vec3 pos = position;
      pos.z = vHeight;

      // Add subtle wave animation
      pos.z += sin(time * 0.5 + uv.x * 6.28) * 0.02;

      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  // Fragment shader
  `
    uniform float time;
    uniform bool showMOND;
    uniform sampler2D regimeTexture;
    uniform vec3 deepMONDColor;
    uniform vec3 transitionalColor;
    uniform vec3 newtonianColor;

    varying vec2 vUv;
    varying float vKappa;
    varying float vHeight;

    void main() {
      // Sample MOND regime: -1 = deep, 0 = transitional, 1 = Newtonian
      vec4 regimeSample = texture2D(regimeTexture, vUv);
      float regime = regimeSample.r * 2.0 - 1.0; // Convert from [0,1] to [-1,1]

      vec3 color;

      if (showMOND) {
        // Blend colors based on regime
        if (regime < -0.33) {
          // Deep MOND (no DM needed)
          color = deepMONDColor;
        } else if (regime < 0.33) {
          // Transitional
          color = transitionalColor;
        } else {
          // Newtonian (DM required)
          color = newtonianColor;
        }

        // Modulate by convergence intensity
        color *= 0.5 + vKappa * 3.0;
      } else {
        // Simple convergence visualization
        color = mix(
          vec3(0.1, 0.3, 0.5),  // Low kappa (blue)
          vec3(1.0, 0.4, 0.4),  // High kappa (red)
          vKappa * 5.0
        );
      }

      // Add contour lines
      float contour = fract(vKappa * 20.0);
      if (contour < 0.1) {
        color *= 0.8;
      }

      // Pulsing glow for high-mass regions
      float glow = sin(time * 2.0) * 0.1 + 0.9;
      if (vKappa > 0.08) {
        color *= glow;
      }

      gl_FragColor = vec4(color, 0.9);
    }
  `
);

extend({ MONDShaderMaterial });

// Type augmentation for the extended material
declare module '@react-three/fiber' {
  interface ThreeElements {
    mONDShaderMaterial: JSX.IntrinsicElements['shaderMaterial'] & {
      time?: number;
      kappaTexture?: THREE.DataTexture | null;
      regimeTexture?: THREE.DataTexture | null;
      showMOND?: boolean;
      heightScale?: number;
      deepMONDColor?: THREE.Color;
      transitionalColor?: THREE.Color;
      newtonianColor?: THREE.Color;
    };
  }
}

// =============================================================================
// INTERFACES
// =============================================================================

interface MassPeak {
  name: string;
  ra_offset: number;
  dec_offset: number;
  kappa_peak: number;
  redshift: number;
}

interface LensingData {
  metadata: {
    field_center_ra: number;
    field_center_dec: number;
    field_area_deg2: number;
    mond_a0: number;
  };
  convergence_map: {
    x: number[];
    y: number[];
    kappa: number[][];
    kappa_max: number;
  };
  mass_peaks: MassPeak[];
  mond_analysis: {
    regime: number[][];
    deep_mond_fraction: number;
    transitional_fraction: number;
    newtonian_fraction: number;
  };
  boundary_effects: {
    relative_contribution: number;
  };
}

interface GeometricGravityProps {
  opacity?: number;
  showMOND?: boolean;
  showPeaks?: boolean;
  heightScale?: number;
  position?: [number, number, number];
  scale?: number;
}

// =============================================================================
// COMPONENTS
// =============================================================================

/**
 * Mass peak marker
 */
function MassPeakMarker({ peak, scale = 1 }: { peak: MassPeak; scale: number }) {
  const meshRef = useRef<THREE.Mesh>(null);

  // Position based on RA/Dec offset (convert to grid coords)
  const position = useMemo(() => {
    return new THREE.Vector3(
      peak.ra_offset * scale * 10,
      peak.dec_offset * scale * 10,
      peak.kappa_peak * 2 + 0.5  // Above the surface
    );
  }, [peak, scale]);

  useFrame(({ clock }) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = clock.getElapsedTime();
    }
  });

  return (
    <group position={position}>
      <mesh ref={meshRef}>
        <octahedronGeometry args={[0.15 * scale]} />
        <meshStandardMaterial
          color="#FFD700"
          emissive="#FFD700"
          emissiveIntensity={0.5}
          wireframe
        />
      </mesh>
      <Text
        position={[0, 0.3, 0]}
        fontSize={0.12 * scale}
        color="#FFD700"
        anchorX="center"
      >
        {peak.name}
      </Text>
      <Text
        position={[0, 0.15, 0]}
        fontSize={0.08 * scale}
        color="#AAA"
        anchorX="center"
      >
        {`z=${peak.redshift.toFixed(2)}`}
      </Text>
    </group>
  );
}

/**
 * Main Geometric Gravity visualization
 */
export function GeometricGravity({
  opacity = 1,
  showMOND = true,
  showPeaks = true,
  heightScale = 2.0,
  position = [0, 0, 0],
  scale = 3,
}: GeometricGravityProps) {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const materialRef = useRef<any>(null);
  const [data, setData] = useState<LensingData | null>(null);
  const [textures, setTextures] = useState<{
    kappa: THREE.DataTexture | null;
    regime: THREE.DataTexture | null;
  }>({ kappa: null, regime: null });

  // Load data
  useEffect(() => {
    fetch('/data/cosmos_lensing_data.json')
      .then(res => res.json())
      .then((loadedData: LensingData) => {
        setData(loadedData);

        // Create textures from data
        const gridSize = loadedData.convergence_map.kappa.length;

        // Convergence texture
        const kappaArray = new Float32Array(gridSize * gridSize * 4);
        for (let j = 0; j < gridSize; j++) {
          for (let i = 0; i < gridSize; i++) {
            const idx = (j * gridSize + i) * 4;
            const kappa = loadedData.convergence_map.kappa[j][i] / loadedData.convergence_map.kappa_max;
            kappaArray[idx] = kappa;
            kappaArray[idx + 1] = kappa;
            kappaArray[idx + 2] = kappa;
            kappaArray[idx + 3] = 1;
          }
        }
        const kappaTex = new THREE.DataTexture(
          kappaArray,
          gridSize,
          gridSize,
          THREE.RGBAFormat,
          THREE.FloatType
        );
        kappaTex.needsUpdate = true;

        // Regime texture
        const regimeArray = new Float32Array(gridSize * gridSize * 4);
        for (let j = 0; j < gridSize; j++) {
          for (let i = 0; i < gridSize; i++) {
            const idx = (j * gridSize + i) * 4;
            // Convert regime from [-1, 1] to [0, 1]
            const regime = (loadedData.mond_analysis.regime[j][i] + 1) / 2;
            regimeArray[idx] = regime;
            regimeArray[idx + 1] = regime;
            regimeArray[idx + 2] = regime;
            regimeArray[idx + 3] = 1;
          }
        }
        const regimeTex = new THREE.DataTexture(
          regimeArray,
          gridSize,
          gridSize,
          THREE.RGBAFormat,
          THREE.FloatType
        );
        regimeTex.needsUpdate = true;

        setTextures({ kappa: kappaTex, regime: regimeTex });
      })
      .catch(console.error);
  }, []);

  // Animation
  useFrame(({ clock }) => {
    if (materialRef.current) {
      materialRef.current.uniforms.time.value = clock.getElapsedTime();
    }
  });

  if (!data || !textures.kappa) return null;

  return (
    <group position={position}>
      {/* Lensing surface */}
      <mesh rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[scale, scale, 63, 63]} />
        <mONDShaderMaterial
          ref={materialRef}
          kappaTexture={textures.kappa}
          regimeTexture={textures.regime}
          showMOND={showMOND}
          heightScale={heightScale}
          transparent
        />
      </mesh>

      {/* Mass peaks */}
      {showPeaks && data.mass_peaks.map((peak, i) => (
        <MassPeakMarker key={i} peak={peak} scale={scale / 3} />
      ))}

      {/* Field boundary */}
      <Line
        points={[
          [-scale/2, 0, -scale/2],
          [scale/2, 0, -scale/2],
          [scale/2, 0, scale/2],
          [-scale/2, 0, scale/2],
          [-scale/2, 0, -scale/2],
        ]}
        color="#444"
        lineWidth={1}
      />

      {/* Labels */}
      <Text
        position={[0, -0.5, scale/2 + 0.3]}
        fontSize={0.15}
        color="#888"
        anchorX="center"
      >
        COSMOS-Web 0.54 deg²
      </Text>
    </group>
  );
}

/**
 * HUD overlay for MOND statistics
 */
export function MONDHUD({
  deepMONDFraction = 0,
  transitionalFraction = 0,
  newtonianFraction = 0,
  boundaryContribution = 0,
}: {
  deepMONDFraction?: number;
  transitionalFraction?: number;
  newtonianFraction?: number;
  boundaryContribution?: number;
}) {
  return (
    <div style={{
      position: 'absolute',
      top: '280px',
      right: '20px',
      background: 'rgba(0,0,0,0.7)',
      padding: '15px',
      borderRadius: '8px',
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#fff',
      minWidth: '200px',
      border: '1px solid #333',
    }}>
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#2ECC71' }}>
        MOND GRAVITY ANALYSIS
      </div>

      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#2ECC71' }}>Deep MOND:</span> {(deepMONDFraction * 100).toFixed(1)}%
      </div>
      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#F39C12' }}>Transitional:</span> {(transitionalFraction * 100).toFixed(1)}%
      </div>
      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#9B59B6' }}>Newtonian:</span> {(newtonianFraction * 100).toFixed(1)}%
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '11px',
      }}>
        <div style={{ color: '#4ECDC4' }}>
          T³ Boundary: {(boundaryContribution * 100).toFixed(1)}%
        </div>
        <div style={{ marginTop: '5px', fontSize: '10px', color: '#666' }}>
          a₀ = 1.2×10⁻¹⁰ m/s²
        </div>
      </div>
    </div>
  );
}

export default GeometricGravity;
