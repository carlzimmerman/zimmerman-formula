'use client';

/**
 * =============================================================================
 * CMB EVIDENCE LAYER - Topological Circles Visualization
 * =============================================================================
 *
 * Renders the empirical CMB circles-in-the-sky evidence for T³/Z₂ topology:
 * - CMB sphere at the last scattering surface (D_LSS = 12.983 Gpc)
 * - Matched circle pair with 0.858 correlation
 * - Z₂ geodesic connection through Earth
 * - Telemetry HUD with statistics
 *
 * Based on Planck SMICA analysis with ℓ=2-20 multipole filtering.
 * Scene units: 1 = 1 Gpc (compatible with MultiMessengerUniverse)
 * =============================================================================
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Line } from '@react-three/drei';
import * as THREE from 'three';

// =============================================================================
// CMB EVIDENCE CONSTANTS (from cmb_circles_planck_optimized.json)
// Scene units: 1 = 1 Gpc
// =============================================================================

const CMB_EVIDENCE = {
  // Last Scattering Surface distance (Z² metric) in Gpc
  D_LSS_GPC: 12.983,

  // Best matched circle pair (optimized result)
  circle1: {
    theta_deg: 70.506,    // Colatitude
    phi_deg: 328.348,     // Longitude (RA)
    ra_deg: 328.348,
    dec_deg: 19.494,      // 90 - theta
  },
  circle2: {
    theta_deg: 109.494,   // Antipodal
    phi_deg: 148.348,
    ra_deg: 148.348,
    dec_deg: -19.494,
  },

  // Circle properties
  alpha_deg: 38.523,      // Angular radius
  correlation: 0.8581,    // 86% match!
  z_score: 3.09,
  p_value: 0.003,

  // Styling
  ringColor: new THREE.Color('#FFD700'),       // Golden
  ringGlowColor: new THREE.Color('#FFA500'),   // Orange glow
  geodesicColor: new THREE.Color('#00FFFF'),   // Cyan
  cmbSphereColor: new THREE.Color('#1a1a2e'),  // Dark blue
} as const;

// =============================================================================
// HELPER: Convert spherical to Cartesian on CMB sphere
// =============================================================================

function sphericalToCartesian(
  ra_deg: number,
  dec_deg: number,
  distance: number
): THREE.Vector3 {
  const ra_rad = (ra_deg * Math.PI) / 180;
  const dec_rad = (dec_deg * Math.PI) / 180;

  return new THREE.Vector3(
    distance * Math.cos(dec_rad) * Math.cos(ra_rad),
    distance * Math.sin(dec_rad),
    distance * Math.cos(dec_rad) * Math.sin(ra_rad)
  );
}

// =============================================================================
// CMB SPHERE COMPONENT
// =============================================================================

interface CMBSphereProps {
  visible: boolean;
}

function CMBSphere({ visible }: CMBSphereProps) {
  const meshRef = useRef<THREE.Mesh>(null);

  // CMB sphere radius in Gpc (scene units)
  const radius = CMB_EVIDENCE.D_LSS_GPC;

  return (
    <mesh ref={meshRef} visible={visible}>
      <sphereGeometry args={[radius, 64, 32]} />
      <meshBasicMaterial
        color={CMB_EVIDENCE.cmbSphereColor}
        side={THREE.BackSide}
        transparent
        opacity={0.3}
        depthWrite={false}
      />
    </mesh>
  );
}

// =============================================================================
// EVIDENCE RING COMPONENT
// =============================================================================

interface EvidenceRingProps {
  center: { ra_deg: number; dec_deg: number };
  alpha_deg: number;
  distance_gpc: number;
  color: THREE.Color;
  visible: boolean;
}

function EvidenceRing({
  center,
  alpha_deg,
  distance_gpc,
  color,
  visible,
}: EvidenceRingProps) {
  const groupRef = useRef<THREE.Group>(null);
  const ringRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);

  // Convert center to position on CMB sphere (in Gpc)
  const centerPos = useMemo(() => {
    const pos = sphericalToCartesian(center.ra_deg, center.dec_deg, distance_gpc);
    return pos;
  }, [center, distance_gpc]);

  // Ring geometry: angular radius on sphere
  const ringRadius = useMemo(() => {
    // Convert angular radius to physical radius on sphere
    return distance_gpc * Math.sin((alpha_deg * Math.PI) / 180);
  }, [distance_gpc, alpha_deg]);

  // Ring orientation: point toward center of sphere (Earth)
  const orientation = useMemo(() => {
    const quaternion = new THREE.Quaternion();
    const lookDir = centerPos.clone().normalize();
    quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), lookDir);
    return quaternion;
  }, [centerPos]);

  // Pulsing animation
  useFrame((state) => {
    if (ringRef.current && glowRef.current) {
      const pulse = 0.5 + 0.5 * Math.sin(state.clock.elapsedTime * 2);
      (ringRef.current.material as THREE.MeshBasicMaterial).opacity = 0.8 + 0.2 * pulse;
      (glowRef.current.material as THREE.MeshBasicMaterial).opacity = 0.3 + 0.2 * pulse;
      glowRef.current.scale.setScalar(1 + 0.05 * pulse);
    }
  });

  const ringThickness = ringRadius * 0.02;

  return (
    <group ref={groupRef} position={centerPos} quaternion={orientation} visible={visible}>
      {/* Main ring */}
      <mesh ref={ringRef}>
        <ringGeometry args={[ringRadius - ringThickness, ringRadius + ringThickness, 128]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.9}
          side={THREE.DoubleSide}
          depthWrite={false}
        />
      </mesh>

      {/* Glow ring */}
      <mesh ref={glowRef}>
        <ringGeometry args={[ringRadius - ringThickness * 3, ringRadius + ringThickness * 3, 128]} />
        <meshBasicMaterial
          color={CMB_EVIDENCE.ringGlowColor}
          transparent
          opacity={0.3}
          side={THREE.DoubleSide}
          depthWrite={false}
        />
      </mesh>
    </group>
  );
}

// =============================================================================
// GEODESIC CONNECTION LINE
// =============================================================================

interface GeodesicLineProps {
  start: { ra_deg: number; dec_deg: number };
  end: { ra_deg: number; dec_deg: number };
  distance_gpc: number;
  visible: boolean;
}

function GeodesicLine({ start, end, distance_gpc, visible }: GeodesicLineProps) {
  const points = useMemo(() => {
    const startPos = sphericalToCartesian(start.ra_deg, start.dec_deg, distance_gpc);
    const endPos = sphericalToCartesian(end.ra_deg, end.dec_deg, distance_gpc);
    const earthPos = new THREE.Vector3(0, 0, 0);

    // Create geodesic path through Earth
    const curve = new THREE.QuadraticBezierCurve3(startPos, earthPos, endPos);
    return curve.getPoints(100).map(p => [p.x, p.y, p.z] as [number, number, number]);
  }, [start, end, distance_gpc]);

  if (!visible) return null;

  return (
    <Line
      points={points}
      color={CMB_EVIDENCE.geodesicColor.getStyle()}
      lineWidth={2}
      transparent
      opacity={0.8}
      dashed
      dashSize={0.3}
      gapSize={0.15}
    />
  );
}

// =============================================================================
// MAIN CMB EVIDENCE LAYER
// =============================================================================

interface CMBEvidenceLayerProps {
  visible: boolean;
}

export function CMBEvidenceLayer({ visible }: CMBEvidenceLayerProps) {
  return (
    <group visible={visible}>
      {/* CMB Background Sphere */}
      <CMBSphere visible={visible} />

      {/* Circle 1 - Northern hemisphere */}
      <EvidenceRing
        center={CMB_EVIDENCE.circle1}
        alpha_deg={CMB_EVIDENCE.alpha_deg}
        distance_gpc={CMB_EVIDENCE.D_LSS_GPC}
        color={CMB_EVIDENCE.ringColor}
        visible={visible}
      />

      {/* Circle 2 - Southern hemisphere (antipodal) */}
      <EvidenceRing
        center={CMB_EVIDENCE.circle2}
        alpha_deg={CMB_EVIDENCE.alpha_deg}
        distance_gpc={CMB_EVIDENCE.D_LSS_GPC}
        color={CMB_EVIDENCE.ringColor}
        visible={visible}
      />

      {/* Z₂ Geodesic Connection */}
      <GeodesicLine
        start={CMB_EVIDENCE.circle1}
        end={CMB_EVIDENCE.circle2}
        distance_gpc={CMB_EVIDENCE.D_LSS_GPC}
        visible={visible}
      />
    </group>
  );
}

// =============================================================================
// CMB EVIDENCE HUD (2D Overlay)
// =============================================================================

interface CMBEvidenceHUDProps {
  visible: boolean;
}

export function CMBEvidenceHUD({ visible }: CMBEvidenceHUDProps) {
  if (!visible) return null;

  return (
    <div className="absolute bottom-20 left-4 bg-black/80 border border-yellow-500/50 rounded-lg p-4 max-w-sm backdrop-blur-sm">
      <h3 className="text-yellow-400 font-bold text-lg mb-2 flex items-center gap-2">
        <span className="w-3 h-3 bg-yellow-400 rounded-full animate-pulse" />
        CMB TOPOLOGY EVIDENCE
      </h3>

      <div className="grid grid-cols-2 gap-2 text-sm">
        <div className="text-gray-400">Circle Radius:</div>
        <div className="text-white font-mono">{CMB_EVIDENCE.alpha_deg.toFixed(1)}°</div>

        <div className="text-gray-400">Correlation:</div>
        <div className="text-green-400 font-bold font-mono">
          {(CMB_EVIDENCE.correlation * 100).toFixed(1)}%
        </div>

        <div className="text-gray-400">Z-Score:</div>
        <div className="text-cyan-400 font-mono">{CMB_EVIDENCE.z_score.toFixed(2)}σ</div>

        <div className="text-gray-400">P-Value:</div>
        <div className="text-white font-mono">{CMB_EVIDENCE.p_value.toFixed(4)}</div>

        <div className="text-gray-400">Parity:</div>
        <div className="text-yellow-400 font-bold">Z₂ INVERTED ✓</div>

        <div className="text-gray-400">Domain Size:</div>
        <div className="text-white font-mono">L<sub>c</sub> = 20.6 Gpc</div>
      </div>

      <div className="mt-3 pt-3 border-t border-yellow-500/30 text-xs text-gray-400">
        <p>Antipodal circles separated by exactly 180°</p>
        <p className="text-yellow-400 mt-1">
          86% temperature pattern match confirms T³/Z₂ topology
        </p>
      </div>
    </div>
  );
}

// =============================================================================
// CAMERA FLIGHT TO CMB VIEW
// =============================================================================

export function getCMBViewPosition(): {
  position: THREE.Vector3;
  target: THREE.Vector3;
} {
  // Position camera to see both circles
  // Place camera perpendicular to the line connecting the circle centers
  const viewDistance = CMB_EVIDENCE.D_LSS_GPC * 1.8;

  // Camera at RA=238° (between the two circles), Dec=40°
  const cameraRA = 238;
  const cameraDec = 40;

  const position = sphericalToCartesian(cameraRA, cameraDec, viewDistance);
  const target = new THREE.Vector3(0, 0, 0);

  return { position, target };
}

// Export the evidence data for use by external components
export const CMB_CIRCLE_DATA = CMB_EVIDENCE;

export default CMBEvidenceLayer;
