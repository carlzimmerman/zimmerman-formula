'use client';

/**
 * =============================================================================
 * ISOTROPY BREAKER - "Axis of Evil" Visualization
 * =============================================================================
 *
 * Directive RRRR Implementation: Visualizes the kinematic alignment of CMB
 * quadrupole and octupole axes that breaks cosmic isotropy.
 *
 * Physics:
 * - In infinite ΛCDM, quadrupole (ℓ=2) and octupole (ℓ=3) should point randomly
 * - Planck data shows they are aligned within 9° (2.4σ anomaly)
 * - This "Axis of Evil" has only 1.5% random probability
 * - T³/Z₂ PREDICTS this: cubic domain has preferred geometric axes
 *
 * Visualization:
 * - Spherical harmonic lobes (d-orbital for ℓ=2, f-orbital for ℓ=3)
 * - Axis arrow showing alignment direction
 * - Correlation to fundamental domain boundaries
 *
 * =============================================================================
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Line } from '@react-three/drei';
import * as THREE from 'three';

// =============================================================================
// AXIS OF EVIL DATA (from axis_of_evil_data.json)
// =============================================================================

const AXIS_OF_EVIL = {
  // Galactic coordinates
  galactic_l_deg: 238.0,  // Average of quadrupole/octupole
  galactic_b_deg: 63.0,

  // Alignment statistics
  alignment_angle_deg: 9.0,    // Angle between quadrupole and octupole
  random_probability: 0.015,   // 1.5% chance in ΛCDM
  significance_sigma: 2.4,

  // Box alignment (from analysis)
  best_alignment_axis: 'Z',
  angle_to_box_deg: 27.0,

  // Quadrupole axis (ℓ=2)
  quadrupole: {
    galactic_l_deg: 237.0,
    galactic_b_deg: 63.0,
    cartesian: [-0.1948, -0.3714, 0.9076],
  },

  // Octupole axis (ℓ=3)
  octupole: {
    galactic_l_deg: 239.0,
    galactic_b_deg: 63.0,
    cartesian: [-0.1828, -0.3768, 0.9080],
  },

  // CMB sphere
  D_LSS_GPC: 12.983,
  HALF_BOX_GPC: 10.3,  // L_c/2 = 20.6/2

  // Colors
  quadrupoleColor: new THREE.Color('#FF6B6B'),   // Red-coral
  octupoleColor: new THREE.Color('#4ECDC4'),     // Teal
  axisColor: new THREE.Color('#FFD93D'),         // Golden
  boxAxisColor: new THREE.Color('#FFFFFF'),      // White
} as const;

// =============================================================================
// HELPER: Convert Galactic to Cartesian
// =============================================================================

function galacticToCartesian(l_deg: number, b_deg: number, distance: number): THREE.Vector3 {
  const l_rad = (l_deg * Math.PI) / 180;
  const b_rad = (b_deg * Math.PI) / 180;

  return new THREE.Vector3(
    distance * Math.cos(b_rad) * Math.cos(l_rad),
    distance * Math.sin(b_rad),
    distance * Math.cos(b_rad) * Math.sin(l_rad)
  );
}

// =============================================================================
// SPHERICAL HARMONIC LOBE GENERATOR
// =============================================================================

function generateSphericalHarmonicMesh(ell: number, resolution: number = 48): THREE.BufferGeometry {
  const positions: number[] = [];
  const normals: number[] = [];
  const indices: number[] = [];

  // Generate vertices on unit sphere with Y_ℓ^0 deformation
  for (let i = 0; i <= resolution; i++) {
    const theta = (i * Math.PI) / resolution;
    const cosTheta = Math.cos(theta);
    const sinTheta = Math.sin(theta);

    for (let j = 0; j <= resolution * 2; j++) {
      const phi = (j * Math.PI) / resolution;

      // Compute spherical harmonic magnitude
      let r: number;
      if (ell === 2) {
        // Y_2^0 ∝ (3cos²θ - 1) - quadrupole/d-orbital shape
        r = Math.abs(3 * cosTheta * cosTheta - 1);
      } else if (ell === 3) {
        // Y_3^0 ∝ (5cos³θ - 3cosθ) - octupole/f-orbital shape
        r = Math.abs(5 * cosTheta * cosTheta * cosTheta - 3 * cosTheta);
      } else {
        r = 1;
      }

      // Normalize to reasonable size
      r = 0.3 + r * 0.7;

      // Convert to Cartesian
      const x = r * sinTheta * Math.cos(phi);
      const y = r * cosTheta;
      const z = r * sinTheta * Math.sin(phi);

      positions.push(x, y, z);

      // Approximate normal (radial for now)
      const len = Math.sqrt(x * x + y * y + z * z);
      normals.push(x / len, y / len, z / len);
    }
  }

  // Generate indices for triangle strips
  const cols = resolution * 2 + 1;
  for (let i = 0; i < resolution; i++) {
    for (let j = 0; j < resolution * 2; j++) {
      const a = i * cols + j;
      const b = a + cols;
      const c = a + 1;
      const d = b + 1;

      indices.push(a, b, c);
      indices.push(b, d, c);
    }
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geometry.setAttribute('normal', new THREE.Float32BufferAttribute(normals, 3));
  geometry.setIndex(indices);

  return geometry;
}

// =============================================================================
// SPHERICAL HARMONIC LOBE COMPONENT
// =============================================================================

interface HarmonicLobeProps {
  ell: number;
  axisDirection: THREE.Vector3;
  scale: number;
  color: THREE.Color;
  visible: boolean;
}

function HarmonicLobe({ ell, axisDirection, scale, color, visible }: HarmonicLobeProps) {
  const meshRef = useRef<THREE.Mesh>(null);

  const geometry = useMemo(() => generateSphericalHarmonicMesh(ell), [ell]);

  // Compute rotation to align with axis
  const quaternion = useMemo(() => {
    const q = new THREE.Quaternion();
    q.setFromUnitVectors(new THREE.Vector3(0, 1, 0), axisDirection.clone().normalize());
    return q;
  }, [axisDirection]);

  // Pulsing animation
  useFrame((state) => {
    if (meshRef.current) {
      const pulse = 0.95 + 0.05 * Math.sin(state.clock.elapsedTime * 2 + ell);
      meshRef.current.scale.setScalar(scale * pulse);
    }
  });

  return (
    <mesh ref={meshRef} quaternion={quaternion} visible={visible}>
      <primitive object={geometry} attach="geometry" />
      <meshBasicMaterial
        color={color}
        transparent
        opacity={0.6}
        side={THREE.DoubleSide}
        depthWrite={false}
        wireframe={false}
      />
    </mesh>
  );
}

// =============================================================================
// AXIS ARROW COMPONENT
// =============================================================================

interface AxisArrowProps {
  direction: THREE.Vector3;
  length: number;
  color: THREE.Color;
  visible: boolean;
  label?: string;
}

function AxisArrow({ direction, length, color, visible }: AxisArrowProps) {
  const points = useMemo(() => {
    const dir = direction.clone().normalize();
    const start = dir.clone().multiplyScalar(-length);
    const end = dir.clone().multiplyScalar(length);
    return [
      [start.x, start.y, start.z] as [number, number, number],
      [end.x, end.y, end.z] as [number, number, number]
    ];
  }, [direction, length]);

  // Arrow heads
  const arrowHeads = useMemo(() => {
    const dir = direction.clone().normalize();
    const end = dir.clone().multiplyScalar(length);
    const arrowLength = length * 0.1;

    // Create perpendicular vectors for arrow head
    const perp1 = new THREE.Vector3(1, 0, 0);
    if (Math.abs(dir.dot(perp1)) > 0.9) {
      perp1.set(0, 1, 0);
    }
    perp1.cross(dir).normalize().multiplyScalar(arrowLength * 0.3);

    const perp2 = perp1.clone().cross(dir).normalize().multiplyScalar(arrowLength * 0.3);

    return {
      tip: end,
      base: end.clone().sub(dir.clone().multiplyScalar(arrowLength)),
      perp1,
      perp2,
    };
  }, [direction, length]);

  if (!visible) return null;

  return (
    <group>
      {/* Main axis line */}
      <Line
        points={points}
        color={color.getStyle()}
        lineWidth={3}
        transparent
        opacity={0.9}
      />

      {/* Arrow head cone */}
      <mesh position={arrowHeads.tip}>
        <coneGeometry args={[length * 0.03, length * 0.1, 16]} />
        <meshBasicMaterial color={color} />
      </mesh>
    </group>
  );
}

// =============================================================================
// BOX BOUNDARY INDICATOR
// =============================================================================

interface BoxBoundaryProps {
  halfBox: number;
  visible: boolean;
}

function BoxBoundary({ halfBox, visible }: BoxBoundaryProps) {
  // Create wireframe box showing fundamental domain
  const points = useMemo(() => {
    const h = halfBox;
    // 12 edges of cube
    const edges: Array<[[number, number, number], [number, number, number]]> = [
      // Bottom face
      [[-h, -h, -h], [h, -h, -h]],
      [[h, -h, -h], [h, -h, h]],
      [[h, -h, h], [-h, -h, h]],
      [[-h, -h, h], [-h, -h, -h]],
      // Top face
      [[-h, h, -h], [h, h, -h]],
      [[h, h, -h], [h, h, h]],
      [[h, h, h], [-h, h, h]],
      [[-h, h, h], [-h, h, -h]],
      // Vertical edges
      [[-h, -h, -h], [-h, h, -h]],
      [[h, -h, -h], [h, h, -h]],
      [[h, -h, h], [h, h, h]],
      [[-h, -h, h], [-h, h, h]],
    ];
    return edges;
  }, [halfBox]);

  if (!visible) return null;

  return (
    <group>
      {points.map((edge, i) => (
        <Line
          key={i}
          points={edge}
          color="#FFFFFF"
          lineWidth={1}
          transparent
          opacity={0.3}
          dashed
          dashSize={0.5}
          gapSize={0.3}
        />
      ))}
    </group>
  );
}

// =============================================================================
// MAIN ISOTROPY BREAKER COMPONENT
// =============================================================================

interface IsotropyBreakerProps {
  visible: boolean;
}

export function IsotropyBreaker({ visible }: IsotropyBreakerProps) {
  // Compute axis direction from Galactic coordinates
  const axisDirection = useMemo(() => {
    return galacticToCartesian(
      AXIS_OF_EVIL.galactic_l_deg,
      AXIS_OF_EVIL.galactic_b_deg,
      1.0
    ).normalize();
  }, []);

  // Quadrupole and octupole directions (slightly different)
  const quadrupoleDir = useMemo(() => new THREE.Vector3(...AXIS_OF_EVIL.quadrupole.cartesian).normalize(), []);
  const octupoleDir = useMemo(() => new THREE.Vector3(...AXIS_OF_EVIL.octupole.cartesian).normalize(), []);

  // Scale for lobes (fits within CMB sphere)
  const lobeScale = AXIS_OF_EVIL.D_LSS_GPC * 0.4;

  return (
    <group visible={visible}>
      {/* Fundamental domain boundary (faint wireframe) */}
      <BoxBoundary halfBox={AXIS_OF_EVIL.HALF_BOX_GPC} visible={visible} />

      {/* Quadrupole lobe (ℓ=2) */}
      <HarmonicLobe
        ell={2}
        axisDirection={quadrupoleDir}
        scale={lobeScale}
        color={AXIS_OF_EVIL.quadrupoleColor}
        visible={visible}
      />

      {/* Octupole lobe (ℓ=3) - slightly smaller */}
      <HarmonicLobe
        ell={3}
        axisDirection={octupoleDir}
        scale={lobeScale * 0.7}
        color={AXIS_OF_EVIL.octupoleColor}
        visible={visible}
      />

      {/* Axis of Evil arrow */}
      <AxisArrow
        direction={axisDirection}
        length={AXIS_OF_EVIL.D_LSS_GPC}
        color={AXIS_OF_EVIL.axisColor}
        visible={visible}
        label="Axis of Evil"
      />

      {/* Box principal axes for reference */}
      <AxisArrow
        direction={new THREE.Vector3(0, 0, 1)}
        length={AXIS_OF_EVIL.HALF_BOX_GPC}
        color={new THREE.Color('#444444')}
        visible={visible}
        label="Z"
      />
    </group>
  );
}

// =============================================================================
// ISOTROPY BREAKER HUD (2D Overlay)
// =============================================================================

interface IsotropyBreakerHUDProps {
  visible: boolean;
}

export function IsotropyBreakerHUD({ visible }: IsotropyBreakerHUDProps) {
  if (!visible) return null;

  return (
    <div className="absolute bottom-20 left-4 bg-black/80 border border-yellow-500/50 rounded-lg p-4 max-w-sm backdrop-blur-sm">
      <h3 className="text-yellow-400 font-bold text-lg mb-2 flex items-center gap-2">
        <span className="w-3 h-3 bg-yellow-400 rounded-full animate-pulse" />
        AXIS OF EVIL
      </h3>

      <div className="grid grid-cols-2 gap-2 text-sm">
        <div className="text-gray-400">Alignment Angle:</div>
        <div className="text-yellow-400 font-bold font-mono">
          {AXIS_OF_EVIL.alignment_angle_deg}°
        </div>

        <div className="text-gray-400">Expected (Random):</div>
        <div className="text-gray-500 font-mono">60°</div>

        <div className="text-gray-400">Significance:</div>
        <div className="text-green-400 font-mono">
          {AXIS_OF_EVIL.significance_sigma}σ
        </div>

        <div className="text-gray-400">Random Probability:</div>
        <div className="text-red-400 font-mono">
          {(AXIS_OF_EVIL.random_probability * 100).toFixed(1)}%
        </div>

        <div className="text-gray-400">Box Alignment:</div>
        <div className="text-white font-mono">
          {AXIS_OF_EVIL.best_alignment_axis}-axis ({AXIS_OF_EVIL.angle_to_box_deg}°)
        </div>

        <div className="text-gray-400">Direction:</div>
        <div className="text-white font-mono text-xs">
          (l={AXIS_OF_EVIL.galactic_l_deg}°, b={AXIS_OF_EVIL.galactic_b_deg}°)
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-yellow-500/30">
        <div className="flex items-center gap-2 mb-2">
          <span className="w-3 h-3 rounded-full" style={{ backgroundColor: AXIS_OF_EVIL.quadrupoleColor.getStyle() }} />
          <span className="text-sm" style={{ color: AXIS_OF_EVIL.quadrupoleColor.getStyle() }}>
            Quadrupole (ℓ=2)
          </span>
        </div>
        <div className="flex items-center gap-2 mb-2">
          <span className="w-3 h-3 rounded-full" style={{ backgroundColor: AXIS_OF_EVIL.octupoleColor.getStyle() }} />
          <span className="text-sm" style={{ color: AXIS_OF_EVIL.octupoleColor.getStyle() }}>
            Octupole (ℓ=3)
          </span>
        </div>
        <p className="text-xs text-gray-400 mt-2">
          The largest CMB multipoles are anomalously aligned along a single axis.
          T³ cubic topology has preferred geometric directions that cause this.
        </p>
        <p className="text-yellow-400 text-xs mt-1">
          In an infinite universe, this has only {(AXIS_OF_EVIL.random_probability * 100).toFixed(1)}% probability.
        </p>
      </div>
    </div>
  );
}

export default IsotropyBreaker;
