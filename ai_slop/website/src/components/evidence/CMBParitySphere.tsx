'use client';

/**
 * =============================================================================
 * CMB PARITY SPHERE - Z₂ Parity Asymmetry Visualization
 * =============================================================================
 *
 * Directive QQQQ Implementation: Visualizes the CMB parity asymmetry that
 * demonstrates Z₂ involution suppression of even harmonics.
 *
 * Physics:
 * - In infinite ΛCDM, even and odd multipoles have equal power
 * - Planck observes P = (odd - even) / (odd + even) = 0.054 at 2.9σ
 * - T³/Z₂ orbifold PREDICTS this: Z₂ involution (p → -p) suppresses even modes
 *
 * Visualization:
 * - Sphere at D_LSS shows odd (cyan) vs even (magenta) power distribution
 * - Spherical harmonic pattern overlay (Y_ℓ shapes)
 * - Animated crossfade between even/odd dominance
 *
 * =============================================================================
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// =============================================================================
// PARITY EVIDENCE DATA (from parity_data.json)
// =============================================================================

const PARITY_DATA = {
  // Overall parity asymmetry
  P_2_30: 0.054,            // Parity parameter for ℓ=2-30
  significance_sigma: 2.9,
  p_value: 0.004,

  // Power sums
  odd_power_sum: 12621,     // μK²
  even_power_sum: 11329,    // μK²
  ratio_odd_to_even: 1.114,

  // CMB sphere radius (same as circles layer)
  D_LSS_GPC: 12.983,

  // Colors
  oddColor: new THREE.Color('#00FFFF'),    // Cyan for odd modes
  evenColor: new THREE.Color('#FF00FF'),   // Magenta for even modes
  neutralColor: new THREE.Color('#FFFFFF'), // White for balance
} as const;

// =============================================================================
// PARITY SHADER MATERIAL
// =============================================================================

const parityVertexShader = `
  varying vec3 vNormal;
  varying vec3 vPosition;
  varying vec2 vUv;

  void main() {
    vNormal = normalize(normalMatrix * normal);
    vPosition = position;
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const parityFragmentShader = `
  uniform float time;
  uniform float parityRatio;
  uniform vec3 oddColor;
  uniform vec3 evenColor;

  varying vec3 vNormal;
  varying vec3 vPosition;
  varying vec2 vUv;

  // Spherical harmonic approximations for visualization
  float Y_2_0(vec3 n) {
    // Quadrupole: 3cos²θ - 1
    return 3.0 * n.y * n.y - 1.0;
  }

  float Y_3_0(vec3 n) {
    // Octupole: 5cos³θ - 3cosθ
    return 5.0 * n.y * n.y * n.y - 3.0 * n.y;
  }

  float Y_4_0(vec3 n) {
    // Hexadecapole
    float c2 = n.y * n.y;
    return 35.0 * c2 * c2 - 30.0 * c2 + 3.0;
  }

  float Y_5_0(vec3 n) {
    float c = n.y;
    float c2 = c * c;
    return 63.0 * c2 * c2 * c - 70.0 * c2 * c + 15.0 * c;
  }

  void main() {
    vec3 n = normalize(vPosition);

    // Compute even and odd harmonic contributions
    float evenHarmonics = abs(Y_2_0(n)) * 0.4 + abs(Y_4_0(n)) * 0.15;
    float oddHarmonics = abs(Y_3_0(n)) * 0.5 + abs(Y_5_0(n)) * 0.2;

    // Normalize
    evenHarmonics = evenHarmonics / 1.5;
    oddHarmonics = oddHarmonics / 1.5;

    // Apply observed parity asymmetry (odd dominates by ~11%)
    oddHarmonics *= parityRatio;

    // Time-varying crossfade animation
    float phase = sin(time * 0.5) * 0.5 + 0.5;

    // Mix colors based on which harmonic dominates locally
    float oddDominance = oddHarmonics / (oddHarmonics + evenHarmonics + 0.01);

    // Apply phase animation
    oddDominance = mix(oddDominance, 1.0 - oddDominance, phase * 0.3);

    vec3 color = mix(evenColor, oddColor, oddDominance);

    // Add glow at multipole maxima
    float intensity = max(oddHarmonics, evenHarmonics);
    intensity = pow(intensity, 0.5);

    // Fresnel edge glow
    float fresnel = pow(1.0 - abs(dot(vNormal, vec3(0.0, 0.0, 1.0))), 2.0);

    // Final color with intensity and alpha
    vec3 finalColor = color * (0.3 + intensity * 0.7);
    finalColor += vec3(1.0) * fresnel * 0.3;

    float alpha = 0.15 + intensity * 0.4 + fresnel * 0.2;

    gl_FragColor = vec4(finalColor, alpha);
  }
`;

// =============================================================================
// PARITY SPHERE COMPONENT
// =============================================================================

interface ParitySphereProps {
  visible: boolean;
}

function ParitySphere({ visible }: ParitySphereProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const materialRef = useRef<THREE.ShaderMaterial>(null);

  const uniforms = useMemo(() => ({
    time: { value: 0 },
    parityRatio: { value: PARITY_DATA.ratio_odd_to_even },
    oddColor: { value: PARITY_DATA.oddColor },
    evenColor: { value: PARITY_DATA.evenColor },
  }), []);

  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uniforms.time.value = state.clock.elapsedTime;
    }
  });

  return (
    <mesh ref={meshRef} visible={visible}>
      <sphereGeometry args={[PARITY_DATA.D_LSS_GPC, 128, 64]} />
      <shaderMaterial
        ref={materialRef}
        vertexShader={parityVertexShader}
        fragmentShader={parityFragmentShader}
        uniforms={uniforms}
        transparent
        side={THREE.DoubleSide}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </mesh>
  );
}

// =============================================================================
// MULTIPOLE MARKERS - Show dominant harmonic locations
// =============================================================================

interface MultipoleMarkerProps {
  position: THREE.Vector3;
  ell: number;
  isOdd: boolean;
  visible: boolean;
}

function MultipoleMarker({ position, ell, isOdd, visible }: MultipoleMarkerProps) {
  const color = isOdd ? PARITY_DATA.oddColor : PARITY_DATA.evenColor;
  const size = 0.3 + (0.5 / ell); // Larger markers for lower ℓ

  // Static - no pulsing animation (multipole positions are fixed mathematical locations)

  return (
    <mesh position={position} visible={visible}>
      <sphereGeometry args={[size, 16, 16]} />
      <meshBasicMaterial
        color={color}
        transparent
        opacity={0.8}
        depthWrite={false}
      />
    </mesh>
  );
}

// =============================================================================
// MAIN CMB PARITY SPHERE COMPONENT
// =============================================================================

interface CMBParitySphereProps {
  visible: boolean;
}

export function CMBParitySphere({ visible }: CMBParitySphereProps) {
  // Generate multipole marker positions
  const markers = useMemo(() => {
    const result: Array<{ position: THREE.Vector3; ell: number; isOdd: boolean }> = [];

    // Place markers at characteristic locations for each multipole
    for (let ell = 2; ell <= 6; ell++) {
      const isOdd = ell % 2 === 1;
      const numMarkers = ell + 1;

      for (let i = 0; i < numMarkers; i++) {
        // Distribute around theta = π/2 (equator) for visualization
        const theta = (Math.PI / (numMarkers + 1)) * (i + 1);
        const phi = (2 * Math.PI * ell / 7) + (i * 0.3);

        const r = PARITY_DATA.D_LSS_GPC;
        const x = r * Math.sin(theta) * Math.cos(phi);
        const y = r * Math.cos(theta);
        const z = r * Math.sin(theta) * Math.sin(phi);

        result.push({
          position: new THREE.Vector3(x, y, z),
          ell,
          isOdd,
        });
      }
    }

    return result;
  }, []);

  return (
    <group visible={visible}>
      {/* Parity-colored CMB sphere */}
      <ParitySphere visible={visible} />

      {/* Multipole markers */}
      {markers.map((marker, i) => (
        <MultipoleMarker
          key={i}
          position={marker.position}
          ell={marker.ell}
          isOdd={marker.isOdd}
          visible={visible}
        />
      ))}
    </group>
  );
}

// =============================================================================
// PARITY EVIDENCE HUD (2D Overlay)
// =============================================================================

interface ParityEvidenceHUDProps {
  visible: boolean;
}

export function ParityEvidenceHUD({ visible }: ParityEvidenceHUDProps) {
  if (!visible) return null;

  return (
    <div className="absolute bottom-20 left-4 bg-black/80 border border-cyan-500/50 rounded-lg p-4 max-w-sm backdrop-blur-sm">
      <h3 className="text-cyan-400 font-bold text-lg mb-2 flex items-center gap-2">
        <span className="w-3 h-3 bg-cyan-400 rounded-full animate-pulse" />
        Z₂ PARITY ASYMMETRY
      </h3>

      <div className="grid grid-cols-2 gap-2 text-sm">
        <div className="text-gray-400">Parity Parameter:</div>
        <div className="text-cyan-400 font-bold font-mono">
          P = {(PARITY_DATA.P_2_30 * 100).toFixed(1)}%
        </div>

        <div className="text-gray-400">Significance:</div>
        <div className="text-green-400 font-mono">
          {PARITY_DATA.significance_sigma}σ
        </div>

        <div className="text-gray-400">Odd Power:</div>
        <div className="text-cyan-400 font-mono">
          {PARITY_DATA.odd_power_sum.toLocaleString()} μK²
        </div>

        <div className="text-gray-400">Even Power:</div>
        <div className="text-purple-400 font-mono">
          {PARITY_DATA.even_power_sum.toLocaleString()} μK²
        </div>

        <div className="text-gray-400">Odd/Even Ratio:</div>
        <div className="text-white font-mono">
          {PARITY_DATA.ratio_odd_to_even.toFixed(3)}
        </div>

        <div className="text-gray-400">ΛCDM Probability:</div>
        <div className="text-red-400 font-mono">
          {(PARITY_DATA.p_value * 100).toFixed(1)}%
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-cyan-500/30">
        <div className="flex items-center gap-2 mb-2">
          <span className="w-3 h-3 bg-cyan-400 rounded-full" />
          <span className="text-cyan-400 text-xs">Odd multipoles (ℓ = 3, 5, 7...)</span>
        </div>
        <div className="flex items-center gap-2 mb-2">
          <span className="w-3 h-3 bg-purple-500 rounded-full" />
          <span className="text-purple-400 text-xs">Even multipoles (ℓ = 2, 4, 6...)</span>
        </div>
        <p className="text-xs text-gray-400 mt-2">
          Z₂ involution (p → -p) suppresses even-parity standing waves,
          causing odd multipoles to dominate.
        </p>
        <p className="text-cyan-400 text-xs mt-1">
          This is a direct signature of the orbifold topology.
        </p>
      </div>
    </div>
  );
}

export default CMBParitySphere;
