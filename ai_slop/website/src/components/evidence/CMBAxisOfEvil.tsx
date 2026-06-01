/**
 * =============================================================================
 * CMB AXIS OF EVIL - Planck Multipole Alignment Visualization
 * =============================================================================
 *
 * Renders the Cosmic Microwave Background at its exact comoving distance
 * (14.0 Gpc) showing the anomalous alignment of the quadrupole (l=2) and
 * octupole (l=3) multipoles - the "Axis of Evil".
 *
 * Physics:
 * - CMB surface of last scattering: z ≈ 1100, d ≈ 14,000 Mpc = 14.0 Gpc
 * - Quadrupole/octupole aligned within ~1.4° (probability < 0.1% in random universe)
 * - In T³/Z₂ topology: alignment is EXPECTED acoustic signature of boundary walls
 *
 * Visualization:
 * - Translucent CMB sphere at exact scale
 * - 6 intersection circles where CMB meets T³ boundary walls (±10.3 Gpc)
 * - Quadrupole axis (red) and octupole axis (green) as geometric vectors
 * - Glowing lattice at sphere-wall intersections
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useEffect, useState } from 'react';
import * as THREE from 'three';
import { Line } from '@react-three/drei';

interface CMBAxisOfEvilProps {
  visible?: boolean;
  opacity?: number;
  showIntersections?: boolean;
  showAxes?: boolean;
  showSphere?: boolean;
}

interface CMBData {
  metadata: {
    cmb_comoving_distance_gpc: number;
    boundary_wall_gpc: number;
  };
  multipoles: {
    quadrupole: {
      axis_cartesian: number[];
      axis_galactic: { l: number; b: number };
      power_uk2: number;
    };
    octupole: {
      axis_cartesian: number[];
      axis_galactic: { l: number; b: number };
      power_uk2: number;
    };
    mutual_alignment_deg: number;
    wall_alignments: Record<string, {
      quadrupole_angle_deg: number;
      octupole_angle_deg: number;
    }>;
  };
  boundary_intersections: Array<{
    wall: string;
    wall_position_gpc: number;
    circle_radius_gpc: number;
    circle_center: number[];
    circle_points: number[][];
    normal_axis: string;
  }>;
  anomaly_statistics: {
    quadrupole_octupole_alignment_deg: number;
    probability_random: number;
    t3_interpretation: string;
  };
}

// CMB sphere radius
const CMB_RADIUS_GPC = 14.0;
const HALF_BOX_GPC = 10.3;

export function CMBAxisOfEvil({
  visible = true,
  opacity = 0.15,
  showIntersections = true,
  showAxes = true,
  showSphere = true,
}: CMBAxisOfEvilProps) {
  const groupRef = useRef<THREE.Group>(null);
  const sphereRef = useRef<THREE.Mesh>(null);
  const [data, setData] = useState<CMBData | null>(null);
  const [loading, setLoading] = useState(true);

  // Load CMB data
  useEffect(() => {
    if (!visible) return;

    fetch('/data/cmb_axis_of_evil.json')
      .then(res => res.json())
      .then((cmbData: CMBData) => {
        setData(cmbData);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load CMB data:', err);
        setLoading(false);
      });
  }, [visible]);

  // No animation - static visualization for scientific accuracy

  // Generate intersection circle geometry
  const intersectionCircles = useMemo(() => {
    if (!data?.boundary_intersections) return [];

    return data.boundary_intersections.map((intersection, idx) => {
      const points = intersection.circle_points.map(
        p => new THREE.Vector3(p[0], p[1], p[2])
      );
      // Close the circle
      if (points.length > 0) {
        points.push(points[0].clone());
      }
      return {
        ...intersection,
        points,
        idx,
      };
    });
  }, [data]);

  // Axis vectors (scaled for visibility)
  const axisLength = 20; // Gpc - extends beyond the box for visibility

  if (!visible || loading) return null;

  const quadrupoleAxis = data?.multipoles?.quadrupole?.axis_cartesian || [0.5, 0.5, 0.7];
  const octupoleAxis = data?.multipoles?.octupole?.axis_cartesian || [0.48, 0.52, 0.71];

  return (
    <group ref={groupRef}>
      {/* CMB Sphere - translucent at exact scale */}
      {showSphere && (
        <>
          <mesh ref={sphereRef}>
            <sphereGeometry args={[CMB_RADIUS_GPC, 64, 64]} />
            <meshBasicMaterial
              color="#ffdd88"
              transparent
              opacity={opacity}
              side={THREE.BackSide}
              blending={THREE.AdditiveBlending}
              depthWrite={false}
            />
          </mesh>

          {/* Wireframe overlay for structure */}
          <mesh>
            <sphereGeometry args={[CMB_RADIUS_GPC * 0.999, 32, 32]} />
            <meshBasicMaterial
              color="#ffaa44"
              transparent
              opacity={0.05}
              wireframe
              side={THREE.BackSide}
            />
          </mesh>
        </>
      )}

      {/* Intersection circles - where CMB meets T³ boundary walls */}
      {showIntersections && intersectionCircles.map((circle) => (
        <group key={circle.wall}>
          {/* Glowing intersection ring */}
          <Line
            points={circle.points.map(p => [p.x, p.y, p.z] as [number, number, number])}
            color="#00ffff"
            lineWidth={3}
            transparent
            opacity={0.8}
          />

          {/* Secondary glow ring */}
          <Line
            points={circle.points.map(p => [p.x, p.y, p.z] as [number, number, number])}
            color="#00ffff"
            lineWidth={8}
            transparent
            opacity={0.2}
          />

          {/* Intersection plane indicator (thin disk) */}
          <mesh
            position={circle.circle_center as [number, number, number]}
            rotation={
              circle.normal_axis === 'X' ? [0, Math.PI / 2, 0] :
              circle.normal_axis === 'Y' ? [Math.PI / 2, 0, 0] :
              [0, 0, 0]
            }
          >
            <ringGeometry args={[circle.circle_radius_gpc * 0.95, circle.circle_radius_gpc, 64]} />
            <meshBasicMaterial
              color="#00ffff"
              transparent
              opacity={0.1}
              side={THREE.DoubleSide}
              blending={THREE.AdditiveBlending}
              depthWrite={false}
            />
          </mesh>
        </group>
      ))}

      {/* Quadrupole axis - RED */}
      {showAxes && (
        <group>
          {/* Positive direction */}
          <Line
            points={[
              [0, 0, 0],
              [
                quadrupoleAxis[0] * axisLength,
                quadrupoleAxis[1] * axisLength,
                quadrupoleAxis[2] * axisLength,
              ],
            ]}
            color="#ff4444"
            lineWidth={4}
            transparent
            opacity={0.9}
          />
          {/* Negative direction (axis is bidirectional) */}
          <Line
            points={[
              [0, 0, 0],
              [
                -quadrupoleAxis[0] * axisLength,
                -quadrupoleAxis[1] * axisLength,
                -quadrupoleAxis[2] * axisLength,
              ],
            ]}
            color="#ff4444"
            lineWidth={4}
            transparent
            opacity={0.9}
            dashed
            dashSize={0.5}
            gapSize={0.3}
          />

          {/* Axis endpoint markers */}
          <mesh position={[
            quadrupoleAxis[0] * axisLength,
            quadrupoleAxis[1] * axisLength,
            quadrupoleAxis[2] * axisLength,
          ]}>
            <sphereGeometry args={[0.3, 16, 16]} />
            <meshBasicMaterial color="#ff4444" />
          </mesh>
          <mesh position={[
            -quadrupoleAxis[0] * axisLength,
            -quadrupoleAxis[1] * axisLength,
            -quadrupoleAxis[2] * axisLength,
          ]}>
            <sphereGeometry args={[0.3, 16, 16]} />
            <meshBasicMaterial color="#ff4444" transparent opacity={0.5} />
          </mesh>
        </group>
      )}

      {/* Octupole axis - GREEN */}
      {showAxes && (
        <group>
          {/* Positive direction */}
          <Line
            points={[
              [0, 0, 0],
              [
                octupoleAxis[0] * axisLength,
                octupoleAxis[1] * axisLength,
                octupoleAxis[2] * axisLength,
              ],
            ]}
            color="#44ff44"
            lineWidth={4}
            transparent
            opacity={0.9}
          />
          {/* Negative direction */}
          <Line
            points={[
              [0, 0, 0],
              [
                -octupoleAxis[0] * axisLength,
                -octupoleAxis[1] * axisLength,
                -octupoleAxis[2] * axisLength,
              ],
            ]}
            color="#44ff44"
            lineWidth={4}
            transparent
            opacity={0.9}
            dashed
            dashSize={0.5}
            gapSize={0.3}
          />

          {/* Axis endpoint markers */}
          <mesh position={[
            octupoleAxis[0] * axisLength,
            octupoleAxis[1] * axisLength,
            octupoleAxis[2] * axisLength,
          ]}>
            <sphereGeometry args={[0.3, 16, 16]} />
            <meshBasicMaterial color="#44ff44" />
          </mesh>
          <mesh position={[
            -octupoleAxis[0] * axisLength,
            -octupoleAxis[1] * axisLength,
            -octupoleAxis[2] * axisLength,
          ]}>
            <sphereGeometry args={[0.3, 16, 16]} />
            <meshBasicMaterial color="#44ff44" transparent opacity={0.5} />
          </mesh>
        </group>
      )}

      {/* Earth/origin marker */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.1, 16, 16]} />
        <meshBasicMaterial color="#ffffff" />
      </mesh>
    </group>
  );
}

/**
 * HUD overlay for CMB Axis of Evil statistics
 */
export function CMBAxisOfEvilHUD({
  visible = false,
  alignmentAngle = 1.36,
  probabilityRandom = 0.001,
  quadrupoleGalactic = { l: 240, b: 63 },
  octupoleGalactic = { l: 237, b: 63 },
}: {
  visible?: boolean;
  alignmentAngle?: number;
  probabilityRandom?: number;
  quadrupoleGalactic?: { l: number; b: number };
  octupoleGalactic?: { l: number; b: number };
}) {
  if (!visible) return null;

  const isAnomaly = alignmentAngle < 10;

  return (
    <div style={{
      position: 'absolute',
      top: '400px',
      right: '20px',
      background: 'rgba(0,0,0,0.9)',
      padding: '15px',
      borderRadius: '8px',
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#fff',
      minWidth: '280px',
      border: '1px solid #ffaa44',
      boxShadow: '0 0 25px rgba(255, 170, 68, 0.4)',
    }}>
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#ffaa44', fontSize: '14px' }}>
        CMB "AXIS OF EVIL"
      </div>

      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: '#aaa' }}>CMB Distance:</span>{' '}
        <span style={{ color: '#ffdd88' }}>14.0 Gpc</span>
        <span style={{ color: '#666', fontSize: '10px' }}> (z ≈ 1100)</span>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '10px', marginTop: '10px' }}>
        <div style={{ color: '#ff4444', marginBottom: '5px', fontWeight: 'bold' }}>
          Quadrupole (l=2)
        </div>
        <div style={{ fontSize: '11px', marginBottom: '8px' }}>
          Axis: l={quadrupoleGalactic.l}°, b={quadrupoleGalactic.b}°
        </div>

        <div style={{ color: '#44ff44', marginBottom: '5px', fontWeight: 'bold' }}>
          Octupole (l=3)
        </div>
        <div style={{ fontSize: '11px', marginBottom: '8px' }}>
          Axis: l={octupoleGalactic.l}°, b={octupoleGalactic.b}°
        </div>
      </div>

      <div style={{
        borderTop: '1px solid #333',
        paddingTop: '10px',
        marginTop: '10px',
        background: isAnomaly ? 'rgba(255,68,68,0.1)' : 'transparent',
        padding: '10px',
        borderRadius: '4px',
      }}>
        <div style={{ color: '#ffaa00', marginBottom: '5px', fontWeight: 'bold' }}>
          ALIGNMENT ANOMALY
        </div>
        <div style={{ marginBottom: '5px' }}>
          <span style={{ color: '#aaa' }}>Separation:</span>{' '}
          <span style={{ color: isAnomaly ? '#ff4444' : '#fff', fontWeight: 'bold', fontSize: '16px' }}>
            {alignmentAngle.toFixed(2)}°
          </span>
        </div>
        <div style={{ marginBottom: '5px' }}>
          <span style={{ color: '#aaa' }}>Random probability:</span>{' '}
          <span style={{ color: '#ff4444' }}>&lt; {(probabilityRandom * 100).toFixed(1)}%</span>
        </div>
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #333',
        fontSize: '10px',
      }}>
        <div style={{ color: '#00ffff', marginBottom: '5px' }}>
          T³/Z₂ INTERPRETATION:
        </div>
        <div style={{ color: '#888', lineHeight: '1.4' }}>
          In a finite box, the largest acoustic modes (l=2,3) are constrained
          by the boundary geometry. The "impossible" alignment is the
          <span style={{ color: '#00ffff' }}> expected signature </span>
          of primordial sound waves resonating within a 20.6 Gpc cubic room.
        </div>
      </div>

      <div style={{
        marginTop: '10px',
        fontSize: '9px',
        color: '#666',
        borderTop: '1px solid #333',
        paddingTop: '8px',
      }}>
        <span style={{ color: '#ff4444' }}>━━</span> Quadrupole axis |{' '}
        <span style={{ color: '#44ff44' }}>━━</span> Octupole axis |{' '}
        <span style={{ color: '#00ffff' }}>○</span> Boundary intersection
      </div>
    </div>
  );
}

export default CMBAxisOfEvil;
