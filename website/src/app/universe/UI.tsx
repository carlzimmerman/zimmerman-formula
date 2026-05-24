'use client';

/**
 * ================================================================================
 * WORK-ORDER MM: INTERACTIVE TOPOLOGY UI & FLY CONTROLS
 * ================================================================================
 *
 * Interactive overlay for the Z² Universe Viewer.
 *
 * Features:
 * - Scale-adaptive HUD showing current zoom level
 * - Object info panel on hover (Raycaster)
 * - Ghost Quasar toggle to visualize topological light paths
 * - Fly controls with camera tweening
 * - Velocity vector display for local bulk flow
 *
 * Author: Carl Zimmerman + Claude
 * Date: May 23, 2026
 * Framework: Z² Unified Action v11.1.0
 * ================================================================================
 */

import { useState, useCallback, useEffect } from 'react';
import { useThree, useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import * as THREE from 'three';

// =============================================================================
// TYPES
// =============================================================================

interface ObjectInfo {
  id: string;
  name: string;
  type: string;
  position: THREE.Vector3;
  z_obs?: number;         // Observed redshift
  d_lcdm?: number;        // ΛCDM distance (Mpc)
  d_z2?: number;          // Z² distance (Mpc)
  velocity?: THREE.Vector3; // Peculiar velocity
}

interface UIState {
  showGhosts: boolean;
  showVelocities: boolean;
  showGrid: boolean;
  selectedObject: ObjectInfo | null;
  hoveredObject: ObjectInfo | null;
  currentScale: string;
  cameraDistance: number;
  fpsCounter: number;
}

// =============================================================================
// SCALE LABELS
// =============================================================================

const SCALE_LABELS: Record<number, { name: string; unit: string }> = {
  0: { name: 'Solar System', unit: 'AU' },
  1: { name: 'Stellar Neighborhood', unit: 'pc' },
  2: { name: 'Milky Way', unit: 'kpc' },
  3: { name: 'Local Universe', unit: 'Mpc' },
  4: { name: 'Cosmic Web', unit: '100 Mpc' },
  5: { name: 'Topological Edge', unit: 'Gpc' },
};

// =============================================================================
// MAIN UI PANEL
// =============================================================================

interface InfoPanelProps {
  state: UIState;
  onToggleGhosts: () => void;
  onToggleVelocities: () => void;
  onToggleGrid: () => void;
  onZoomTo: (target: 'home' | 'solar' | 'milkyway' | 'edge') => void;
}

export function InfoPanel({
  state,
  onToggleGhosts,
  onToggleVelocities,
  onToggleGrid,
  onZoomTo,
}: InfoPanelProps) {
  const getCurrentScaleInfo = () => {
    if (state.cameraDistance < 0.001) return SCALE_LABELS[0];
    if (state.cameraDistance < 0.1) return SCALE_LABELS[1];
    if (state.cameraDistance < 1) return SCALE_LABELS[2];
    if (state.cameraDistance < 100) return SCALE_LABELS[3];
    if (state.cameraDistance < 5000) return SCALE_LABELS[4];
    return SCALE_LABELS[5];
  };

  const scaleInfo = getCurrentScaleInfo();

  return (
    <div
      style={{
        position: 'absolute',
        top: 20,
        left: 20,
        color: 'white',
        fontFamily: 'monospace',
        fontSize: '13px',
        background: 'rgba(0, 0, 0, 0.85)',
        padding: '16px',
        borderRadius: '8px',
        maxWidth: '320px',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(0, 255, 255, 0.3)',
      }}
    >
      {/* Header */}
      <div style={{
        fontSize: '16px',
        fontWeight: 'bold',
        color: '#00ffff',
        marginBottom: '12px',
        borderBottom: '1px solid rgba(0, 255, 255, 0.3)',
        paddingBottom: '8px',
      }}>
        Z² Universe Viewer
      </div>

      {/* Current Scale */}
      <div style={{ marginBottom: '12px' }}>
        <div style={{ color: '#888', fontSize: '11px' }}>CURRENT SCALE</div>
        <div style={{ fontSize: '18px', color: '#00ff88' }}>
          {scaleInfo.name}
        </div>
        <div style={{ color: '#666' }}>
          Distance: {formatDistance(state.cameraDistance)} {scaleInfo.unit}
        </div>
      </div>

      {/* Framework Info */}
      <div style={{
        marginBottom: '12px',
        padding: '8px',
        background: 'rgba(0, 255, 255, 0.1)',
        borderRadius: '4px',
      }}>
        <div><strong>Topology:</strong> T³/Z₂</div>
        <div><strong>L_c:</strong> 20.6 Gpc</div>
        <div><strong>Ω_m:</strong> 6/19 = 0.3158</div>
      </div>

      {/* Quick Navigation */}
      <div style={{ marginBottom: '12px' }}>
        <div style={{ color: '#888', fontSize: '11px', marginBottom: '6px' }}>
          QUICK NAVIGATION
        </div>
        <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
          <NavButton onClick={() => onZoomTo('solar')} label="☀️ Solar" />
          <NavButton onClick={() => onZoomTo('milkyway')} label="🌌 MW" />
          <NavButton onClick={() => onZoomTo('home')} label="🏠 Local" />
          <NavButton onClick={() => onZoomTo('edge')} label="🔭 Edge" />
        </div>
      </div>

      {/* Toggle Controls */}
      <div style={{ marginBottom: '12px' }}>
        <div style={{ color: '#888', fontSize: '11px', marginBottom: '6px' }}>
          VISUALIZATION
        </div>
        <ToggleButton
          active={state.showGhosts}
          onClick={onToggleGhosts}
          label="Show Ghost Quasars"
          color="#ff00ff"
        />
        <ToggleButton
          active={state.showVelocities}
          onClick={onToggleVelocities}
          label="Show Velocity Vectors"
          color="#00ff00"
        />
        <ToggleButton
          active={state.showGrid}
          onClick={onToggleGrid}
          label="Show T³ Grid"
          color="#00ffff"
        />
      </div>

      {/* Legend */}
      <div style={{
        fontSize: '11px',
        color: '#666',
        borderTop: '1px solid #333',
        paddingTop: '8px',
      }}>
        <div>🔴 Topological vertices</div>
        <div>🟢 Milky Way (observer)</div>
        <div>🟡 High-z quasars</div>
        <div>🔵 Galaxies (color = z)</div>
        <div>🟣 Ghost images</div>
      </div>

      {/* FPS */}
      <div style={{
        position: 'absolute',
        top: '8px',
        right: '12px',
        fontSize: '11px',
        color: state.fpsCounter > 30 ? '#00ff00' : '#ff0000',
      }}>
        {state.fpsCounter} FPS
      </div>
    </div>
  );
}

// =============================================================================
// BUTTON COMPONENTS
// =============================================================================

function NavButton({ onClick, label }: { onClick: () => void; label: string }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: '4px 8px',
        background: 'rgba(0, 255, 255, 0.2)',
        border: '1px solid rgba(0, 255, 255, 0.4)',
        borderRadius: '4px',
        color: '#00ffff',
        cursor: 'pointer',
        fontSize: '11px',
        fontFamily: 'monospace',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.background = 'rgba(0, 255, 255, 0.4)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.background = 'rgba(0, 255, 255, 0.2)';
      }}
    >
      {label}
    </button>
  );
}

function ToggleButton({
  active,
  onClick,
  label,
  color,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  color: string;
}) {
  return (
    <button
      onClick={onClick}
      style={{
        display: 'block',
        width: '100%',
        padding: '6px 10px',
        marginBottom: '4px',
        background: active ? `${color}22` : 'transparent',
        border: `1px solid ${active ? color : '#444'}`,
        borderRadius: '4px',
        color: active ? color : '#888',
        cursor: 'pointer',
        fontSize: '12px',
        fontFamily: 'monospace',
        textAlign: 'left',
      }}
    >
      {active ? '✓' : '○'} {label}
    </button>
  );
}

// =============================================================================
// OBJECT INFO TOOLTIP
// =============================================================================

interface ObjectTooltipProps {
  object: ObjectInfo | null;
}

export function ObjectTooltip({ object }: ObjectTooltipProps) {
  if (!object) return null;

  return (
    <div
      style={{
        position: 'absolute',
        top: '50%',
        right: 20,
        transform: 'translateY(-50%)',
        color: 'white',
        fontFamily: 'monospace',
        fontSize: '12px',
        background: 'rgba(0, 0, 0, 0.9)',
        padding: '16px',
        borderRadius: '8px',
        maxWidth: '280px',
        border: '1px solid rgba(255, 215, 0, 0.5)',
      }}
    >
      <div style={{
        fontSize: '14px',
        fontWeight: 'bold',
        color: '#ffd700',
        marginBottom: '8px',
      }}>
        {object.name}
      </div>

      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: '#888' }}>Type: </span>
        <span style={{ color: '#00ffff' }}>{object.type}</span>
      </div>

      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: '#888' }}>ID: </span>
        <span style={{ color: '#ccc' }}>{object.id}</span>
      </div>

      {object.z_obs !== undefined && (
        <div style={{ marginBottom: '4px' }}>
          <span style={{ color: '#888' }}>z_obs: </span>
          <span>{object.z_obs.toFixed(4)}</span>
        </div>
      )}

      {object.d_lcdm !== undefined && object.d_z2 !== undefined && (
        <div style={{
          marginTop: '12px',
          padding: '8px',
          background: 'rgba(255, 0, 0, 0.1)',
          borderRadius: '4px',
          border: '1px solid rgba(255, 0, 0, 0.3)',
        }}>
          <div style={{ color: '#ff8888', fontSize: '11px', marginBottom: '4px' }}>
            DISTANCE COMPARISON
          </div>
          <div>
            <span style={{ color: '#888' }}>ΛCDM: </span>
            <span>{object.d_lcdm.toFixed(1)} Mpc</span>
          </div>
          <div>
            <span style={{ color: '#888' }}>Z²: </span>
            <span style={{ color: '#00ff88' }}>{object.d_z2.toFixed(1)} Mpc</span>
          </div>
          <div style={{
            marginTop: '4px',
            fontSize: '11px',
            color: '#ff6666',
          }}>
            Δ = {Math.abs(object.d_z2 - object.d_lcdm).toFixed(1)} Mpc
            ({((object.d_z2 - object.d_lcdm) / object.d_lcdm * 100).toFixed(1)}%)
          </div>
        </div>
      )}
    </div>
  );
}

// =============================================================================
// VELOCITY VECTOR OVERLAY
// =============================================================================

interface VelocityArrowProps {
  origin: THREE.Vector3;
  direction: THREE.Vector3;
  magnitude: number; // km/s
  label: string;
}

export function VelocityArrow3D({
  origin,
  direction,
  magnitude,
  label,
}: VelocityArrowProps) {
  // Scale arrow length based on magnitude (265 km/s = 1 unit)
  const length = magnitude / 265;

  return (
    <group position={origin.toArray()}>
      <arrowHelper
        args={[
          direction.normalize(),
          new THREE.Vector3(0, 0, 0),
          length,
          0x00ff00,
          length * 0.2,
          length * 0.1,
        ]}
      />
      <Html distanceFactor={10}>
        <div
          style={{
            color: '#00ff00',
            fontSize: '10px',
            fontFamily: 'monospace',
            whiteSpace: 'nowrap',
            background: 'rgba(0,0,0,0.7)',
            padding: '2px 4px',
            borderRadius: '2px',
          }}
        >
          {label}: {magnitude.toFixed(0)} km/s
        </div>
      </Html>
    </group>
  );
}

// =============================================================================
// GHOST QUASAR PATH OVERLAY
// =============================================================================

interface GhostPathProps {
  primary: THREE.Vector3;
  ghost: THREE.Vector3;
  wrapPoint: THREE.Vector3;
  name: string;
}

export function GhostPath({ primary, ghost, wrapPoint, name }: GhostPathProps) {
  return (
    <group>
      {/* Primary quasar marker */}
      <mesh position={primary.toArray()}>
        <sphereGeometry args={[0.1, 16, 16]} />
        <meshBasicMaterial color="#ffcc00" />
      </mesh>

      {/* Path to box boundary */}
      <line>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={2}
            array={new Float32Array([...primary.toArray(), ...wrapPoint.toArray()])}
            itemSize={3}
          />
        </bufferGeometry>
        <lineBasicMaterial color="#ff00ff" linewidth={2} />
      </line>

      {/* Wrapped path from opposite side */}
      <line>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={2}
            array={new Float32Array([
              -wrapPoint.x, -wrapPoint.y, -wrapPoint.z,
              0, 0, 0, // Observer
            ])}
            itemSize={3}
          />
        </bufferGeometry>
        <lineDashedMaterial color="#ff00ff" dashSize={0.1} gapSize={0.05} />
      </line>

      {/* Ghost marker */}
      <mesh position={[-wrapPoint.x, -wrapPoint.y, -wrapPoint.z]}>
        <sphereGeometry args={[0.08, 16, 16]} />
        <meshBasicMaterial color="#ff00ff" transparent opacity={0.6} />
      </mesh>

      {/* Label */}
      <Html position={primary.toArray()} distanceFactor={15}>
        <div
          style={{
            color: '#ff00ff',
            fontSize: '10px',
            fontFamily: 'monospace',
            background: 'rgba(0,0,0,0.8)',
            padding: '2px 6px',
            borderRadius: '3px',
          }}
        >
          {name} → Ghost
        </div>
      </Html>
    </group>
  );
}

// =============================================================================
// CONTROLS HINT
// =============================================================================

export function ControlsHint() {
  return (
    <div
      style={{
        position: 'absolute',
        bottom: 20,
        right: 20,
        color: '#666',
        fontFamily: 'monospace',
        fontSize: '11px',
        textAlign: 'right',
      }}
    >
      <div>🖱️ Drag to rotate | Scroll to zoom</div>
      <div>Double-click object to fly to</div>
      <div style={{ marginTop: '4px', color: '#444' }}>
        Z² Framework v11.1.0
      </div>
    </div>
  );
}

// =============================================================================
// HELPERS
// =============================================================================

function formatDistance(d: number): string {
  if (d < 0.001) return (d * 1e6).toFixed(1);  // Convert to pc
  if (d < 1) return (d * 1000).toFixed(1);      // Convert to kpc
  if (d < 1000) return d.toFixed(1);            // Mpc
  return (d / 1000).toFixed(2);                  // Gpc
}

// =============================================================================
// RAYCASTER HOOK FOR OBJECT SELECTION
// =============================================================================

export function useObjectPicker() {
  const { camera, scene, raycaster, pointer } = useThree();
  const [hoveredObject, setHoveredObject] = useState<ObjectInfo | null>(null);

  useFrame(() => {
    raycaster.setFromCamera(pointer, camera);
    const intersects = raycaster.intersectObjects(scene.children, true);

    if (intersects.length > 0) {
      const obj = intersects[0].object;
      if (obj.userData?.objectInfo) {
        setHoveredObject(obj.userData.objectInfo);
        return;
      }
    }
    setHoveredObject(null);
  });

  return hoveredObject;
}

// =============================================================================
// EXPORTS
// =============================================================================

export type { UIState, ObjectInfo };
