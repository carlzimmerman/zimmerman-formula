/**
 * =============================================================================
 * DESI GALAXIES - Real DESI DR1 LRG Galaxy Positions
 * =============================================================================
 *
 * Visualizes 100,000 Luminous Red Galaxies from DESI DR1 survey.
 * Coordinates are in T³-wrapped Gpc with L_c = 20.6 Gpc.
 *
 * Data source: DESI DR1 LRG catalog (real positions, not simulated)
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';

interface DESIGalaxiesProps {
  visible?: boolean;
  opacity?: number;
  pointSize?: number;
}

export function DESIGalaxies({
  visible = true,
  opacity = 0.6,
  pointSize = 0.02,
}: DESIGalaxiesProps) {
  const pointsRef = useRef<THREE.Points>(null);
  const [positions, setPositions] = useState<Float32Array | null>(null);
  const [loading, setLoading] = useState(true);

  // Load binary data
  useEffect(() => {
    if (!visible) return;

    fetch('/data/desi_galaxies.bin')
      .then(res => res.arrayBuffer())
      .then(buffer => {
        const floatArray = new Float32Array(buffer);
        setPositions(floatArray);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load DESI galaxies:', err);
        setLoading(false);
      });
  }, [visible]);

  // Create buffer geometry
  const geometry = useMemo(() => {
    if (!positions) return null;

    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    return geo;
  }, [positions]);

  // Material
  const material = useMemo(() => {
    return new THREE.PointsMaterial({
      color: new THREE.Color('#4A90D9'),  // DESI blue
      size: pointSize,
      transparent: true,
      opacity: opacity,
      sizeAttenuation: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
  }, [pointSize, opacity]);

  if (!visible || loading || !geometry) return null;

  return (
    <points ref={pointsRef} geometry={geometry} material={material} />
  );
}

/**
 * HUD overlay for DESI Galaxy statistics
 */
export function DESIGalaxiesHUD({
  visible = false,
}: {
  visible?: boolean;
}) {
  if (!visible) return null;

  return (
    <div style={{
      position: 'absolute',
      top: '400px',
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
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#4A90D9' }}>
        DESI DR1 LRG GALAXIES
      </div>

      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#4A90D9' }}>Count:</span> 100,000
      </div>
      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#aaa' }}>Type:</span> Luminous Red Galaxies
      </div>
      <div style={{ marginBottom: '5px' }}>
        <span style={{ color: '#aaa' }}>Survey:</span> DESI DR1
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '10px',
        color: '#666',
      }}>
        Real positions with T³ wrapping applied
        <br />
        L_c = 20.6 Gpc
      </div>
    </div>
  );
}

export default DESIGalaxies;
