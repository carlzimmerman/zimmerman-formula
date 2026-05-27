/**
 * =============================================================================
 * GALAXY CLUSTER MAP - Extended Cluster Structure Visualization
 * =============================================================================
 *
 * Visualizes real galaxy cluster member distributions from VizieR catalogs:
 * - Coma Cluster (A1656): 2157 members from Jimenez-Teja+ 2025
 * - Virgo Cluster: 1589 members from EVCC (Kim+ 2014)
 * - Shapley Supercluster: ShaSS survey (Haines+ 2018)
 *
 * Features:
 * - NFW-like radial profiles showing true cluster structure
 * - Velocity coloring (blueshift/redshift within cluster)
 * - Cluster core and virial radius indicators
 * - Member galaxy point cloud
 *
 * =============================================================================
 */

import React, { useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { Line, Text } from '@react-three/drei';

// Scale: convert Mpc to visualization units (Gpc scale)
const MPC_TO_GPC = 0.001;
const SCALE = 0.5;  // Overall scale factor

// Color scheme
const CLUSTER_COLORS = {
  coma: { core: '#FFD700', halo: '#FFA500', member: '#FFAA44' },     // Gold/Orange
  virgo: { core: '#4ECDC4', halo: '#45B7D1', member: '#66DDDD' },    // Teal/Cyan
  shapley: { core: '#9B59B6', halo: '#8E44AD', member: '#AA77CC' },  // Purple
};

// Velocity color mapping
function velocityToColor(v_offset: number, sigma: number): THREE.Color {
  // Normalize velocity offset by dispersion
  const normalized = v_offset / sigma;

  if (normalized < -0.5) {
    // Blueshifted (approaching)
    return new THREE.Color('#4444FF');
  } else if (normalized > 0.5) {
    // Redshifted (receding)
    return new THREE.Color('#FF4444');
  } else {
    // Near cluster mean
    return new THREE.Color('#FFFFFF');
  }
}

// Interfaces
interface ClusterMember {
  ra: number;
  dec: number;
  redshift: number;
  velocity_km_s: number;
  distance_mpc: number;
  position: { x: number; y: number; z: number };
  magnitude_r?: number;
  magnitude_b?: number;
  magnitude_k?: number;
  subcluster?: string;
  synthetic?: boolean;
}

interface ClusterInfo {
  name: string;
  abell_id: string | null;
  center_ra: number;
  center_dec: number;
  mean_redshift: number;
  distance_mpc: number;
  virial_radius_mpc: number;
  velocity_dispersion_km_s: number;
  mass_1e14_msun: number;
}

interface ClusterData {
  cluster: ClusterInfo;
  members: ClusterMember[];
  n_members: number;
  source: string;
  subclusters?: string[];
}

interface ClusterDataFile {
  metadata: {
    description: string;
    sources: string[];
  };
  clusters: {
    coma: ClusterData;
    virgo: ClusterData;
    shapley: ClusterData;
  };
}

interface GalaxyClusterMapProps {
  visible: boolean;
  showComa?: boolean;
  showVirgo?: boolean;
  showShapley?: boolean;
  showVelocityColors?: boolean;
  showVirialRadius?: boolean;
}

/**
 * Single cluster member point
 */
function ClusterMemberPoint({
  member,
  clusterInfo,
  colorScheme,
  showVelocityColor,
}: {
  member: ClusterMember;
  clusterInfo: ClusterInfo;
  colorScheme: { core: string; halo: string; member: string };
  showVelocityColor: boolean;
}) {
  const position = useMemo(() => {
    // Convert Mpc position to visualization coordinates
    return new THREE.Vector3(
      member.position.x * MPC_TO_GPC * SCALE,
      member.position.y * MPC_TO_GPC * SCALE,
      member.position.z * MPC_TO_GPC * SCALE
    );
  }, [member.position]);

  const color = useMemo(() => {
    if (showVelocityColor) {
      const v_cluster = clusterInfo.mean_redshift * 299792.458;
      const v_offset = member.velocity_km_s - v_cluster;
      return velocityToColor(v_offset, clusterInfo.velocity_dispersion_km_s);
    }
    return new THREE.Color(colorScheme.member);
  }, [member, clusterInfo, colorScheme, showVelocityColor]);

  // Size based on magnitude (brighter = larger)
  const size = useMemo(() => {
    const mag = member.magnitude_r ?? member.magnitude_b ?? member.magnitude_k ?? -20;
    // Convert magnitude to size (brighter = more negative mag = larger)
    const sizeFactor = Math.pow(10, (-mag - 18) / 5);
    return Math.max(0.001, Math.min(0.008, sizeFactor * 0.003));
  }, [member]);

  return (
    <mesh position={position}>
      <sphereGeometry args={[size, 6, 6]} />
      <meshBasicMaterial
        color={color}
        transparent
        opacity={0.7}
      />
    </mesh>
  );
}

/**
 * Cluster visualization with virial radius and core
 */
function ClusterVisualization({
  data,
  colorScheme,
  showVelocityColors,
  showVirialRadius,
}: {
  data: ClusterData;
  colorScheme: { core: string; halo: string; member: string };
  showVelocityColors: boolean;
  showVirialRadius: boolean;
}) {
  const { cluster, members } = data;

  // Cluster center in visualization coordinates
  const centerPosition = useMemo(() => {
    // Convert RA/Dec to Cartesian
    const ra = cluster.center_ra * Math.PI / 180;
    const dec = cluster.center_dec * Math.PI / 180;
    const d = cluster.distance_mpc * MPC_TO_GPC * SCALE;

    return new THREE.Vector3(
      d * Math.cos(dec) * Math.cos(ra),
      d * Math.cos(dec) * Math.sin(ra),
      d * Math.sin(dec)
    );
  }, [cluster]);

  // Virial radius in visualization units
  const virialRadiusVis = cluster.virial_radius_mpc * MPC_TO_GPC * SCALE;

  // Sample members for performance (show every Nth member)
  const sampledMembers = useMemo(() => {
    const sampleRate = members.length > 500 ? Math.ceil(members.length / 500) : 1;
    return members.filter((_, i) => i % sampleRate === 0);
  }, [members]);

  return (
    <group>
      {/* Cluster core marker */}
      <mesh position={centerPosition}>
        <sphereGeometry args={[0.01, 16, 16]} />
        <meshStandardMaterial
          color={colorScheme.core}
          emissive={colorScheme.core}
          emissiveIntensity={0.5}
        />
      </mesh>

      {/* Cluster label */}
      <Text
        position={[centerPosition.x, centerPosition.y + 0.03, centerPosition.z]}
        fontSize={0.015}
        color={colorScheme.core}
        anchorX="center"
      >
        {cluster.name}
      </Text>

      {/* Virial radius sphere (wireframe) */}
      {showVirialRadius && (
        <mesh position={centerPosition}>
          <sphereGeometry args={[virialRadiusVis, 24, 24]} />
          <meshBasicMaterial
            color={colorScheme.halo}
            transparent
            opacity={0.1}
            wireframe
          />
        </mesh>
      )}

      {/* Member galaxies */}
      {sampledMembers.map((member, i) => (
        <ClusterMemberPoint
          key={i}
          member={member}
          clusterInfo={cluster}
          colorScheme={colorScheme}
          showVelocityColor={showVelocityColors}
        />
      ))}
    </group>
  );
}

/**
 * Main Galaxy Cluster Map component
 */
export function GalaxyClusterMap({
  visible,
  showComa = true,
  showVirgo = true,
  showShapley = true,
  showVelocityColors = false,
  showVirialRadius = true,
}: GalaxyClusterMapProps) {
  const [data, setData] = useState<ClusterDataFile | null>(null);

  // Load cluster data
  useEffect(() => {
    fetch('/data/cluster_members_data.json')
      .then(res => res.json())
      .then((loadedData: ClusterDataFile) => {
        setData(loadedData);
      })
      .catch(console.error);
  }, []);

  if (!visible || !data) return null;

  return (
    <group>
      {/* Earth marker at origin */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.002, 8, 8]} />
        <meshBasicMaterial color="#4444FF" />
      </mesh>

      {/* Coma Cluster */}
      {showComa && data.clusters.coma && (
        <ClusterVisualization
          data={data.clusters.coma}
          colorScheme={CLUSTER_COLORS.coma}
          showVelocityColors={showVelocityColors}
          showVirialRadius={showVirialRadius}
        />
      )}

      {/* Virgo Cluster */}
      {showVirgo && data.clusters.virgo && (
        <ClusterVisualization
          data={data.clusters.virgo}
          colorScheme={CLUSTER_COLORS.virgo}
          showVelocityColors={showVelocityColors}
          showVirialRadius={showVirialRadius}
        />
      )}

      {/* Shapley Supercluster */}
      {showShapley && data.clusters.shapley && (
        <ClusterVisualization
          data={data.clusters.shapley}
          colorScheme={CLUSTER_COLORS.shapley}
          showVelocityColors={showVelocityColors}
          showVirialRadius={showVirialRadius}
        />
      )}
    </group>
  );
}

/**
 * HUD overlay for cluster statistics
 */
export function ClusterMapHUD({
  visible,
  comaMembers = 0,
  virgoMembers = 0,
  shapleyMembers = 0,
}: {
  visible: boolean;
  comaMembers?: number;
  virgoMembers?: number;
  shapleyMembers?: number;
}) {
  if (!visible) return null;

  return (
    <div style={{
      position: 'absolute',
      top: '120px',
      left: '20px',
      background: 'rgba(0,0,0,0.8)',
      padding: '15px',
      borderRadius: '8px',
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#fff',
      minWidth: '200px',
      border: '1px solid #FFD700',
    }}>
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#FFD700' }}>
        GALAXY CLUSTERS
      </div>

      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: CLUSTER_COLORS.coma.core }}>Coma (A1656):</span>
        <span style={{ marginLeft: '8px' }}>{comaMembers} members</span>
        <div style={{ fontSize: '10px', color: '#888' }}>d = 100 Mpc, z = 0.023</div>
      </div>

      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: CLUSTER_COLORS.virgo.core }}>Virgo:</span>
        <span style={{ marginLeft: '8px' }}>{virgoMembers} members</span>
        <div style={{ fontSize: '10px', color: '#888' }}>d = 16.5 Mpc, z = 0.004</div>
      </div>

      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: CLUSTER_COLORS.shapley.core }}>Shapley:</span>
        <span style={{ marginLeft: '8px' }}>{shapleyMembers} members</span>
        <div style={{ fontSize: '10px', color: '#888' }}>d = 200 Mpc, z = 0.048</div>
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '10px',
      }}>
        <div style={{ marginBottom: '5px', color: '#888' }}>Velocity Color:</div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <span style={{ color: '#4444FF' }}>Blue: approaching</span>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <span style={{ color: '#FF4444' }}>Red: receding</span>
        </div>
      </div>

      <div style={{
        marginTop: '8px',
        fontSize: '9px',
        color: '#555'
      }}>
        Sources: VizieR / EVCC / ShaSS
      </div>
    </div>
  );
}

export default GalaxyClusterMap;
