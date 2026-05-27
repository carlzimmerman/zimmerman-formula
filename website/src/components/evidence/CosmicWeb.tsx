/**
 * =============================================================================
 * COSMIC WEB - DESI DR1 Galaxy Distribution Renderer
 * =============================================================================
 *
 * Renders the large-scale structure of the universe using DESI DR1 data.
 * Uses WebGL InstancedMesh for efficient rendering of millions of galaxies.
 *
 * Galaxy types:
 * - BGS (Bright Galaxy Survey): z < 0.4, cyan
 * - LRG (Luminous Red Galaxies): 0.01 < z < 1.5, red
 * - ELG (Emission Line Galaxies): 0.6 < z < 1.6, blue
 * - QSO (Quasars): 0.5 < z < 4.0, magenta
 *
 * Coordinates: Cartesian (X,Y,Z) in Gpc, Earth at origin
 * Fundamental domain: L_c = 20.6 Gpc
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useEffect, useState } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';

interface CosmicWebProps {
  visible?: boolean;
  opacity?: number;
  showBGS?: boolean;
  showLRG?: boolean;
  showELG?: boolean;
  showQSO?: boolean;
}

interface GalaxyObject {
  x: number;
  y: number;
  z: number;
  redshift: number;
  type: string;
}

interface CosmicWebData {
  metadata: {
    total_objects: number;
    source_counts: Record<string, number>;
    fundamental_domain_gpc: number;
  };
  objects: GalaxyObject[];
  boundary_alignment?: Record<string, {
    alignment_ratio: number;
    near_wall_density: number;
    far_wall_density: number;
  }>;
}

// Galaxy type colors
const TYPE_COLORS: Record<string, THREE.Color> = {
  BGS: new THREE.Color('#00ffff'),  // Cyan - nearby bright galaxies
  LRG: new THREE.Color('#ff4444'),  // Red - luminous red galaxies
  ELG: new THREE.Color('#4488ff'),  // Blue - emission line galaxies
  QSO: new THREE.Color('#ff00ff'),  // Magenta - quasars
  G: new THREE.Color('#4A90D9'),    // Default galaxy blue
};

export function CosmicWeb({
  visible = true,
  opacity = 0.7,
  showBGS = true,
  showLRG = true,
  showELG = true,
  showQSO = true,
}: CosmicWebProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const [data, setData] = useState<CosmicWebData | null>(null);
  const [loading, setLoading] = useState(true);

  // Load cosmic web data
  useEffect(() => {
    if (!visible) return;

    fetch('/data/desi_cosmic_web.json')
      .then(res => res.json())
      .then((cosmicData: CosmicWebData) => {
        setData(cosmicData);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load cosmic web data:', err);
        // Fallback to smaller dataset
        fetch('/data/desi_galaxies.json')
          .then(res => res.json())
          .then(fallbackData => {
            setData(fallbackData);
            setLoading(false);
          })
          .catch(() => setLoading(false));
      });
  }, [visible]);

  // Filter and prepare galaxy data
  const { positions, colors, count } = useMemo(() => {
    if (!data?.objects) return { positions: null, colors: null, count: 0 };

    const filtered = data.objects.filter(obj => {
      const type = obj.type;
      if (type === 'BGS' && !showBGS) return false;
      if (type === 'LRG' && !showLRG) return false;
      if (type === 'ELG' && !showELG) return false;
      if (type === 'QSO' && !showQSO) return false;
      return true;
    });

    const posArray = new Float32Array(filtered.length * 3);
    const colorArray = new Float32Array(filtered.length * 3);

    filtered.forEach((obj, i) => {
      posArray[i * 3] = obj.x;
      posArray[i * 3 + 1] = obj.y;
      posArray[i * 3 + 2] = obj.z;

      const color = TYPE_COLORS[obj.type] || TYPE_COLORS.G;
      colorArray[i * 3] = color.r;
      colorArray[i * 3 + 1] = color.g;
      colorArray[i * 3 + 2] = color.b;
    });

    return { positions: posArray, colors: colorArray, count: filtered.length };
  }, [data, showBGS, showLRG, showELG, showQSO]);

  // Create instanced mesh geometry
  useEffect(() => {
    if (!meshRef.current || !positions || count === 0) return;

    const mesh = meshRef.current;
    const matrix = new THREE.Matrix4();
    const color = new THREE.Color();

    for (let i = 0; i < count; i++) {
      matrix.setPosition(
        positions[i * 3],
        positions[i * 3 + 1],
        positions[i * 3 + 2]
      );
      mesh.setMatrixAt(i, matrix);

      color.setRGB(
        colors![i * 3],
        colors![i * 3 + 1],
        colors![i * 3 + 2]
      );
      mesh.setColorAt(i, color);
    }

    mesh.instanceMatrix.needsUpdate = true;
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
  }, [positions, colors, count]);

  // Subtle shimmer animation
  useFrame((state) => {
    if (!meshRef.current) return;
    const material = meshRef.current.material as THREE.MeshBasicMaterial;
    material.opacity = opacity * (0.9 + 0.1 * Math.sin(state.clock.elapsedTime * 0.5));
  });

  if (!visible || loading || count === 0) return null;

  return (
    <instancedMesh
      ref={meshRef}
      args={[undefined, undefined, count]}
      frustumCulled={false}
    >
      <sphereGeometry args={[0.008, 4, 4]} />
      <meshBasicMaterial
        transparent
        opacity={opacity}
        vertexColors
        blending={THREE.AdditiveBlending}
        depthWrite={false}
      />
    </instancedMesh>
  );
}

/**
 * HUD overlay for Cosmic Web statistics
 */
export function CosmicWebHUD({
  visible = false,
  galaxyCount = 0,
  sourceCounts = {},
}: {
  visible?: boolean;
  galaxyCount?: number;
  sourceCounts?: Record<string, number>;
}) {
  if (!visible) return null;

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
      minWidth: '220px',
      border: '1px solid #4A90D9',
      boxShadow: '0 0 20px rgba(74, 144, 217, 0.3)',
    }}>
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#4A90D9' }}>
        COSMIC WEB - DESI DR1
      </div>

      <div style={{ marginBottom: '8px', fontSize: '11px' }}>
        <span style={{ color: '#aaa' }}>Total galaxies:</span>{' '}
        <span style={{ color: '#4A90D9' }}>{galaxyCount.toLocaleString()}</span>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '8px', marginTop: '8px' }}>
        <div style={{ color: '#666', fontSize: '10px', marginBottom: '5px' }}>By Type:</div>
        {Object.entries(sourceCounts).map(([type, count]) => (
          <div key={type} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}>
            <span style={{ color: TYPE_COLORS[type]?.getStyle() || '#aaa' }}>{type}:</span>
            <span style={{ color: '#fff' }}>{count.toLocaleString()}</span>
          </div>
        ))}
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '8px',
        borderTop: '1px solid #333',
        fontSize: '9px',
        color: '#666',
      }}>
        L_c = 20.6 Gpc fundamental domain
        <br />
        Earth at origin (0, 0, 0)
      </div>
    </div>
  );
}

export default CosmicWeb;
