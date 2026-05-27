'use client';

/**
 * =============================================================================
 * KINEMATIC FLOW MAP - Dark Flow Vector Field Visualization
 * =============================================================================
 *
 * Directive SSSS Implementation: Visualizes the bulk peculiar velocity field
 * that points toward the topological boundary of the fundamental domain.
 *
 * Physics:
 * - In infinite ΛCDM, there should be NO preferred bulk motion direction
 * - Kashlinsky et al. detected ~400-1000 km/s coherent "Dark Flow"
 * - Direction: (l=285°, b=10°) in Galactic coordinates
 * - T³/Z₂ PREDICTS this: matter is gravitationally attracted to nearest boundary
 *
 * Visualization:
 * - 3D vector field with arrows pointing toward flow direction
 * - Streamlines showing particle trajectories
 * - Boundary face highlighting showing the attractor
 *
 * =============================================================================
 */

import React, { useMemo } from 'react';
import { Line } from '@react-three/drei';
import * as THREE from 'three';

// =============================================================================
// DARK FLOW DATA (from dark_flow_data.json)
// =============================================================================

const DARK_FLOW = {
  // Combined measurements
  velocity_km_s: 414,
  velocity_error_km_s: 100,

  // Direction in Galactic coordinates
  galactic_l_deg: 293.4,
  galactic_b_deg: -2.7,

  // Box alignment
  best_alignment_axis: 'Y',
  angle_to_box_deg: 23.6,
  is_aligned: true,

  // Cartesian direction (normalized)
  direction: [-0.396, -0.047, 0.917] as [number, number, number],

  // Scales
  HALF_BOX_GPC: 10.3,
  D_LSS_GPC: 12.983,

  // Kashlinsky measurement for reference
  kashlinsky_2024: {
    velocity_km_s: 800,
    depth_mpc_h: 1500,
    significance_sigma: 4.0,
  },

  // Colors
  arrowColor: new THREE.Color('#FF4444'),       // Red for flow
  streamlineColor: new THREE.Color('#FF8888'),  // Lighter red
  boundaryColor: new THREE.Color('#FFAA00'),    // Orange for attractor face
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
// FLOW ARROW COMPONENT
// =============================================================================

interface FlowArrowProps {
  position: THREE.Vector3;
  direction: THREE.Vector3;
  scale: number;
  color: THREE.Color;
  opacity: number;
}

/**
 * Flow Arrow - visualizes measured dark flow direction
 */
function FlowArrow({ position, direction, scale, color, opacity }: FlowArrowProps) {
  // Compute rotation to align arrow with measured flow direction
  const quaternion = useMemo(() => {
    const q = new THREE.Quaternion();
    q.setFromUnitVectors(new THREE.Vector3(0, 1, 0), direction.clone().normalize());
    return q;
  }, [direction]);

  // Static - no pulsing (flow direction is a measured velocity, not a pulsation)

  const arrowLength = scale * 0.5;
  const coneRadius = scale * 0.08;
  const coneHeight = scale * 0.15;

  return (
    <group position={position} quaternion={quaternion}>
      {/* Arrow shaft */}
      <mesh position={[0, arrowLength / 2, 0]}>
        <cylinderGeometry args={[coneRadius * 0.3, coneRadius * 0.3, arrowLength, 8]} />
        <meshBasicMaterial color={color} transparent opacity={opacity} />
      </mesh>

      {/* Arrow head */}
      <mesh position={[0, arrowLength, 0]}>
        <coneGeometry args={[coneRadius, coneHeight, 8]} />
        <meshBasicMaterial color={color} transparent opacity={opacity * 1.5} />
      </mesh>
    </group>
  );
}

// =============================================================================
// VECTOR FIELD COMPONENT
// =============================================================================

interface VectorFieldProps {
  flowDirection: THREE.Vector3;
  visible: boolean;
}

function VectorField({ flowDirection, visible }: VectorFieldProps) {
  // Generate arrow positions in a grid
  const arrows = useMemo(() => {
    const result: Array<{ position: THREE.Vector3; velocity: number }> = [];
    const halfBox = DARK_FLOW.HALF_BOX_GPC;
    const gridSize = 5;
    const spacing = halfBox * 0.6;

    for (let ix = -gridSize; ix <= gridSize; ix++) {
      for (let iy = -gridSize; iy <= gridSize; iy++) {
        for (let iz = -gridSize; iz <= gridSize; iz++) {
          // Skip center and far corners
          const dist = Math.sqrt(ix * ix + iy * iy + iz * iz);
          if (dist < 1 || dist > gridSize * 0.9) continue;

          const pos = new THREE.Vector3(
            ix * spacing * 0.5,
            iy * spacing * 0.5,
            iz * spacing * 0.5
          );

          // Velocity decreases with distance from center (approximate)
          const r = pos.length();
          const velocity = DARK_FLOW.velocity_km_s * Math.exp(-r / 8);

          result.push({ position: pos, velocity });
        }
      }
    }

    return result;
  }, []);

  if (!visible) return null;

  return (
    <group>
      {arrows.map((arrow, i) => {
        const opacity = 0.3 + 0.4 * (arrow.velocity / DARK_FLOW.velocity_km_s);
        const scale = 0.3 + 0.5 * (arrow.velocity / DARK_FLOW.velocity_km_s);

        return (
          <FlowArrow
            key={i}
            position={arrow.position}
            direction={flowDirection}
            scale={scale}
            color={DARK_FLOW.arrowColor}
            opacity={opacity}
          />
        );
      })}
    </group>
  );
}

// =============================================================================
// STREAMLINE COMPONENT
// =============================================================================

interface StreamlinesProps {
  flowDirection: THREE.Vector3;
  visible: boolean;
}

function Streamlines({ flowDirection, visible }: StreamlinesProps) {
  // Generate streamlines
  const lines = useMemo(() => {
    const result: Array<Array<[number, number, number]>> = [];
    const numLines = 20;
    const steps = 60;
    const stepSize = 0.2;
    const halfBox = DARK_FLOW.HALF_BOX_GPC;

    for (let i = 0; i < numLines; i++) {
      // Random starting position (behind the flow)
      const start = new THREE.Vector3(
        (Math.random() - 0.5) * halfBox * 1.2,
        (Math.random() - 0.5) * halfBox * 1.2,
        (Math.random() - 0.5) * halfBox * 1.2
      );

      // Offset against flow direction
      start.addScaledVector(flowDirection, -halfBox * 0.8);

      const points: Array<[number, number, number]> = [];
      const pos = start.clone();

      for (let step = 0; step < steps; step++) {
        points.push([pos.x, pos.y, pos.z]);

        // Add some turbulence/curl
        const noise = new THREE.Vector3(
          Math.sin(pos.x * 0.5 + step * 0.1) * 0.1,
          Math.sin(pos.y * 0.5 + step * 0.15) * 0.1,
          Math.sin(pos.z * 0.5 + step * 0.12) * 0.1
        );

        const velocity = flowDirection.clone().add(noise).normalize();
        pos.addScaledVector(velocity, stepSize);

        // Wrap at boundaries (T³ topology)
        if (Math.abs(pos.x) > halfBox) pos.x = -Math.sign(pos.x) * halfBox + (pos.x % halfBox);
        if (Math.abs(pos.y) > halfBox) pos.y = -Math.sign(pos.y) * halfBox + (pos.y % halfBox);
        if (Math.abs(pos.z) > halfBox) pos.z = -Math.sign(pos.z) * halfBox + (pos.z % halfBox);
      }

      result.push(points);
    }

    return result;
  }, [flowDirection]);

  if (!visible) return null;

  return (
    <group>
      {lines.map((points, i) => (
        <Line
          key={i}
          points={points}
          color={DARK_FLOW.streamlineColor.getStyle()}
          lineWidth={1.5}
          transparent
          opacity={0.4}
        />
      ))}
    </group>
  );
}

// =============================================================================
// ATTRACTOR BOUNDARY FACE
// =============================================================================

interface AttractorFaceProps {
  flowDirection: THREE.Vector3;
  halfBox: number;
  visible: boolean;
}

/**
 * Attractor Face - shows the T³ boundary face in the flow direction
 */
function AttractorFace({ flowDirection, halfBox, visible }: AttractorFaceProps) {
  // Determine which face is the attractor (in the flow direction)
  const faceInfo = useMemo(() => {
    const dir = flowDirection.clone().normalize();
    const absDir = new THREE.Vector3(Math.abs(dir.x), Math.abs(dir.y), Math.abs(dir.z));

    // Find dominant axis
    let faceNormal: THREE.Vector3;
    let facePosition: THREE.Vector3;

    if (absDir.x >= absDir.y && absDir.x >= absDir.z) {
      faceNormal = new THREE.Vector3(Math.sign(dir.x), 0, 0);
      facePosition = new THREE.Vector3(halfBox * Math.sign(dir.x), 0, 0);
    } else if (absDir.y >= absDir.x && absDir.y >= absDir.z) {
      faceNormal = new THREE.Vector3(0, Math.sign(dir.y), 0);
      facePosition = new THREE.Vector3(0, halfBox * Math.sign(dir.y), 0);
    } else {
      faceNormal = new THREE.Vector3(0, 0, Math.sign(dir.z));
      facePosition = new THREE.Vector3(0, 0, halfBox * Math.sign(dir.z));
    }

    // Rotation to face the normal direction
    const quaternion = new THREE.Quaternion();
    quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), faceNormal);

    return { position: facePosition, quaternion };
  }, [flowDirection, halfBox]);

  // Static - no pulsing (boundary face is a fixed geometric feature)

  if (!visible) return null;

  return (
    <mesh position={faceInfo.position} quaternion={faceInfo.quaternion}>
      <planeGeometry args={[halfBox * 2, halfBox * 2]} />
      <meshBasicMaterial
        color={DARK_FLOW.boundaryColor}
        transparent
        opacity={0.3}
        side={THREE.DoubleSide}
        depthWrite={false}
      />
    </mesh>
  );
}

// =============================================================================
// MAIN KINEMATIC FLOW MAP COMPONENT
// =============================================================================

interface KinematicFlowMapProps {
  visible: boolean;
}

export function KinematicFlowMap({ visible }: KinematicFlowMapProps) {
  // Flow direction from Galactic coordinates
  const flowDirection = useMemo(() => {
    return galacticToCartesian(
      DARK_FLOW.galactic_l_deg,
      DARK_FLOW.galactic_b_deg,
      1.0
    ).normalize();
  }, []);

  return (
    <group visible={visible}>
      {/* Vector field arrows */}
      <VectorField flowDirection={flowDirection} visible={visible} />

      {/* Streamlines */}
      <Streamlines flowDirection={flowDirection} visible={visible} />

      {/* Attractor boundary face */}
      <AttractorFace
        flowDirection={flowDirection}
        halfBox={DARK_FLOW.HALF_BOX_GPC}
        visible={visible}
      />

      {/* Main flow direction arrow */}
      <group position={[0, 0, 0]}>
        <FlowArrow
          position={new THREE.Vector3(0, 0, 0)}
          direction={flowDirection}
          scale={3.0}
          color={new THREE.Color('#FFFFFF')}
          opacity={0.9}
        />
      </group>
    </group>
  );
}

// =============================================================================
// DARK FLOW HUD (2D Overlay)
// =============================================================================

interface DarkFlowHUDProps {
  visible: boolean;
}

export function DarkFlowHUD({ visible }: DarkFlowHUDProps) {
  if (!visible) return null;

  return (
    <div className="absolute bottom-20 left-4 bg-black/80 border border-red-500/50 rounded-lg p-4 max-w-sm backdrop-blur-sm">
      <h3 className="text-red-400 font-bold text-lg mb-2 flex items-center gap-2">
        <span className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
        DARK FLOW
      </h3>

      <div className="grid grid-cols-2 gap-2 text-sm">
        <div className="text-gray-400">Bulk Velocity:</div>
        <div className="text-red-400 font-bold font-mono">
          {DARK_FLOW.velocity_km_s} ± {DARK_FLOW.velocity_error_km_s} km/s
        </div>

        <div className="text-gray-400">Direction:</div>
        <div className="text-white font-mono text-xs">
          (l={DARK_FLOW.galactic_l_deg.toFixed(1)}°, b={DARK_FLOW.galactic_b_deg.toFixed(1)}°)
        </div>

        <div className="text-gray-400">Box Alignment:</div>
        <div className="text-white font-mono">
          {DARK_FLOW.best_alignment_axis}-axis ({DARK_FLOW.angle_to_box_deg.toFixed(1)}°)
        </div>

        <div className="text-gray-400">Kashlinsky (2024):</div>
        <div className="text-orange-400 font-mono">
          {DARK_FLOW.kashlinsky_2024.velocity_km_s} km/s at {DARK_FLOW.kashlinsky_2024.significance_sigma}σ
        </div>

        <div className="text-gray-400">Depth:</div>
        <div className="text-white font-mono">
          {DARK_FLOW.kashlinsky_2024.depth_mpc_h} Mpc/h
        </div>

        <div className="text-gray-400">Status:</div>
        <div className={DARK_FLOW.is_aligned ? "text-green-400 font-bold" : "text-gray-500"}>
          {DARK_FLOW.is_aligned ? "ALIGNED WITH BOX" : "Not aligned"}
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-red-500/30">
        <div className="flex items-center gap-2 mb-2">
          <span className="w-3 h-3 bg-red-500 rounded-full" />
          <span className="text-red-400 text-xs">Flow direction (all matter)</span>
        </div>
        <div className="flex items-center gap-2 mb-2">
          <span className="w-3 h-3 bg-orange-400 rounded-full" />
          <span className="text-orange-400 text-xs">Attractor face (boundary)</span>
        </div>
        <p className="text-xs text-gray-400 mt-2">
          In infinite ΛCDM, there should be no preferred direction of bulk motion.
          The observed coherent flow toward a specific direction suggests matter
          is gravitationally attracted to the nearest T³ boundary face.
        </p>
        <p className="text-red-400 text-xs mt-1">
          This is the universe moving toward its edge.
        </p>
      </div>
    </div>
  );
}

export default KinematicFlowMap;
