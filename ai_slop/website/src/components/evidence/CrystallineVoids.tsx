/**
 * =============================================================================
 * CRYSTALLINE VOIDS - Cosmic Void Volumetric Renderer
 * =============================================================================
 *
 * Renders cosmic voids as translucent crystalline spheres.
 * Tests for BCC (Body-Centered Cubic) lattice packing predicted by T³/Z₂ topology.
 *
 * Data includes:
 * - Literature voids (Local Void, Boötes, KBC, Eridanus, etc.)
 * - BOSS/eBOSS void catalog entries
 * - Synthetic voids from observed size distribution
 *
 * Visual encoding:
 * - Sphere radius = effective void radius (r_eff)
 * - Color = distance from T³ boundary walls (more blue = near wall)
 * - Opacity = inverse of void size (smaller = more opaque)
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useEffect, useState } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';

interface CrystallineVoidsProps {
  visible?: boolean;
  opacity?: number;
  showLiterature?: boolean;
  showSynthetic?: boolean;
  highlightBCC?: boolean;
}

interface VoidObject {
  name: string;
  x: number;
  y: number;
  z: number;
  r_eff_gpc: number;
  volume_gpc3: number;
  synthetic: boolean;
  ra?: number;
  dec?: number;
  redshift?: number;
}

interface VoidData {
  metadata: {
    total_voids: number;
    literature_voids: number;
    synthetic_voids: number;
    fundamental_domain_gpc: number;
  };
  packing_analysis: {
    bcc_lattice_score: number;
    voronoi_statistics: {
      mean_volume_gpc3: number;
      volume_uniformity: number;
    };
    boundary_packing: Record<string, {
      mean_wall_distance_gpc: number;
      wall_touching_fraction: number;
    }>;
  };
  voids: VoidObject[];
}

const HALF_BOX_GPC = 10.3; // ±10.3 Gpc fundamental domain

export function CrystallineVoids({
  visible = true,
  opacity = 0.3,
  showLiterature = true,
  showSynthetic = true,
  highlightBCC = false,
}: CrystallineVoidsProps) {
  const groupRef = useRef<THREE.Group>(null);
  const [data, setData] = useState<VoidData | null>(null);
  const [loading, setLoading] = useState(true);

  // Load void data
  useEffect(() => {
    if (!visible) return;

    fetch('/data/cosmic_voids.json')
      .then(res => res.json())
      .then((voidData: VoidData) => {
        setData(voidData);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load void data:', err);
        setLoading(false);
      });
  }, [visible]);

  // Filter voids based on visibility settings
  const filteredVoids = useMemo(() => {
    if (!data?.voids) return [];

    return data.voids.filter(v => {
      if (v.synthetic && !showSynthetic) return false;
      if (!v.synthetic && !showLiterature) return false;
      return true;
    });
  }, [data, showLiterature, showSynthetic]);

  // Compute void colors based on proximity to boundary walls
  const getVoidColor = (v: VoidObject) => {
    // Distance from nearest boundary wall
    const distFromWall = Math.min(
      HALF_BOX_GPC - Math.abs(v.x),
      HALF_BOX_GPC - Math.abs(v.y),
      HALF_BOX_GPC - Math.abs(v.z)
    );

    // Normalize: 0 = at wall, 1 = at center
    const normalized = Math.max(0, Math.min(1, distFromWall / HALF_BOX_GPC));

    if (highlightBCC) {
      // BCC mode: highlight voids that fit lattice pattern
      // Check if void center is near BCC lattice points
      const bccSpacing = 2.0; // Gpc between BCC centers
      const bccOffset = (v.x % bccSpacing + v.y % bccSpacing + v.z % bccSpacing) / 3;
      const onLattice = Math.abs(bccOffset) < 0.3;
      return onLattice ? new THREE.Color('#00ff88') : new THREE.Color('#444466');
    }

    // Standard mode: blue near walls, purple in center
    return new THREE.Color().setHSL(
      0.6 - normalized * 0.15,  // 0.6 (blue) -> 0.45 (purple)
      0.7,
      0.4 + normalized * 0.2
    );
  };

  // Subtle pulsing animation
  useFrame((state) => {
    if (!groupRef.current) return;
    const pulse = 1 + 0.02 * Math.sin(state.clock.elapsedTime * 0.3);
    groupRef.current.children.forEach((child, i) => {
      if (child instanceof THREE.Mesh) {
        const basescale = (child.userData.baseScale || 1);
        child.scale.setScalar(basescale * (pulse + 0.01 * Math.sin(state.clock.elapsedTime * 0.5 + i * 0.1)));
      }
    });
  });

  if (!visible || loading) return null;

  return (
    <group ref={groupRef}>
      {filteredVoids.map((v, i) => {
        const color = getVoidColor(v);
        const voidOpacity = opacity * (v.synthetic ? 0.15 : 0.4);

        return (
          <mesh
            key={v.name || `void-${i}`}
            position={[v.x, v.y, v.z]}
            userData={{ baseScale: v.r_eff_gpc }}
          >
            <sphereGeometry args={[v.r_eff_gpc, 24, 24]} />
            <meshBasicMaterial
              color={color}
              transparent
              opacity={voidOpacity}
              side={THREE.BackSide}
              blending={THREE.AdditiveBlending}
              depthWrite={false}
            />
          </mesh>
        );
      })}

      {/* Void boundaries (wireframe) for major voids */}
      {filteredVoids
        .filter(v => !v.synthetic && v.r_eff_gpc > 0.05)
        .map((v, i) => (
          <mesh
            key={`wire-${v.name || i}`}
            position={[v.x, v.y, v.z]}
          >
            <sphereGeometry args={[v.r_eff_gpc * 1.01, 16, 16]} />
            <meshBasicMaterial
              color="#00ffff"
              transparent
              opacity={0.15}
              wireframe
            />
          </mesh>
        ))}
    </group>
  );
}

/**
 * HUD overlay for Crystalline Voids statistics
 */
export function CrystallineVoidsHUD({
  visible = false,
  totalVoids = 0,
  literatureVoids = 0,
  syntheticVoids = 0,
  bccScore = 0,
  packingAnalysis = {},
}: {
  visible?: boolean;
  totalVoids?: number;
  literatureVoids?: number;
  syntheticVoids?: number;
  bccScore?: number;
  packingAnalysis?: Record<string, any>;
}) {
  if (!visible) return null;

  const bccInterpretation = bccScore > 0.5
    ? 'ALIGNED - T³ topology signature'
    : bccScore > 0.3
    ? 'Partial alignment'
    : 'Random distribution';

  return (
    <div style={{
      position: 'absolute',
      top: '400px',
      right: '20px',
      background: 'rgba(0,0,0,0.85)',
      padding: '15px',
      borderRadius: '8px',
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#fff',
      minWidth: '240px',
      border: '1px solid #6666ff',
      boxShadow: '0 0 20px rgba(102, 102, 255, 0.3)',
    }}>
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#6666ff' }}>
        CRYSTALLINE VOIDS
      </div>

      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#aaa' }}>Total voids:</span>{' '}
        <span style={{ color: '#6666ff' }}>{totalVoids}</span>
      </div>
      <div style={{ marginBottom: '5px', fontSize: '10px' }}>
        <span style={{ color: '#00ffff' }}>Literature:</span> {literatureVoids} |{' '}
        <span style={{ color: '#666' }}>Synthetic:</span> {syntheticVoids}
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '8px', marginTop: '8px' }}>
        <div style={{ color: '#ffaa00', fontSize: '11px', marginBottom: '5px' }}>
          BCC Lattice Analysis
        </div>
        <div style={{ marginBottom: '3px' }}>
          <span style={{ color: '#aaa' }}>BCC Score:</span>{' '}
          <span style={{ color: bccScore > 0.5 ? '#00ff88' : '#ff8800' }}>
            {bccScore.toFixed(3)}
          </span>
        </div>
        <div style={{ fontSize: '10px', color: bccScore > 0.5 ? '#00ff88' : '#888' }}>
          {bccInterpretation}
        </div>
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '8px',
        borderTop: '1px solid #333',
        fontSize: '9px',
        color: '#666',
      }}>
        Voids probe T³ fundamental domain geometry
        <br />
        BCC packing = topological constraint signature
      </div>
    </div>
  );
}

export default CrystallineVoids;
