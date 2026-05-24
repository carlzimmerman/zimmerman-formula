'use client';

/**
 * =============================================================================
 * UniverseCanvas.tsx - FLOAT64 CAMERA-RELATIVE DIGITAL TWIN
 * =============================================================================
 *
 * Work-Order HHH Implementation
 *
 * This component renders the Z² Digital Twin using the Float64 camera-relative
 * engine. All positions are stored in km (Float64) and transformed to
 * camera-relative Float32 coordinates just before GPU submission.
 *
 * KEY FEATURES:
 * - Seamless zoom from 10³ km (planets) to 10²³ km (cosmic horizon)
 * - Dynamic LOD with geometry ↔ label swapping
 * - Adaptive camera near/far planes
 * - True astronomical scales
 *
 * Z² Framework v11.1.0
 * =============================================================================
 */

import React, { useEffect, useRef, Suspense, useMemo, useState, useCallback } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Stars, Html, Line } from '@react-three/drei';
import * as THREE from 'three';

// Engine imports
import {
  useFloatingOrigin,
  useCinematicTour,
  useUniverseStore,
  useVisibility,
  useCameraState,
  useLODLevel,
  useGWSimulation,
  RenderMode,
  AU, KPC, MPC, GPC,
  PLANETS,
  SUN,
  MILKY_WAY,
  Z2_VERTICES,
  Z2,
  formatDistance,
  type CosmicObjectType,
  TOUR_WAYPOINTS,
  GW190521,
  WAVE_RIDER_SEQUENCE,
  createLatticePointCloud,
  gwVertexShader,
  gwFragmentShader,
} from '../engine';

// =============================================================================
// SCALE INDICATOR
// =============================================================================

const ScaleIndicator: React.FC = () => {
  const cameraState = useCameraState();
  const lodLevel = cameraState.lodLevel;
  const formattedDistance = formatDistance(cameraState.distanceFromOrigin);

  const scaleColors: Record<string, string> = {
    PLANETARY: 'text-yellow-400',
    STELLAR: 'text-orange-400',
    GALACTIC: 'text-blue-400',
    CLUSTER: 'text-purple-400',
    COSMIC: 'text-cyan-400',
  };

  const scaleNames: Record<string, string> = {
    PLANETARY: 'Solar System',
    STELLAR: 'Stellar Neighborhood',
    GALACTIC: 'Milky Way',
    CLUSTER: 'Galaxy Clusters',
    COSMIC: 'Cosmic Web',
  };

  return (
    <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-black/90 px-4 py-2 rounded-lg border border-slate-600 z-20">
      <div className={`font-mono text-sm ${scaleColors[lodLevel]}`}>
        {scaleNames[lodLevel]}
      </div>
      <div className="font-mono text-xs text-slate-400 text-center">
        {formattedDistance}
      </div>
    </div>
  );
};

// =============================================================================
// SOLAR SYSTEM (TRUE SCALE + LOD)
// =============================================================================

const SolarSystemLOD: React.FC = () => {
  const { toScenePosition, toSceneSize, getRenderMode, shouldShowLabel, lodLevel, controller } = useFloatingOrigin();
  const visibility = useVisibility();
  const [time, setTime] = useState(0);

  useFrame((state) => {
    setTime(state.clock.elapsedTime * 50);
  });

  // Only render at planetary scale when controller is ready
  if (!controller) return null;
  if (lodLevel !== 'PLANETARY' || !visibility.solarSystem) {
    return null;
  }

  return (
    <group>
      {/* Sun */}
      <SunGeometry
        toScenePosition={toScenePosition}
        toSceneSize={toSceneSize}
        shouldShowLabel={shouldShowLabel}
      />

      {/* Planets */}
      {PLANETS.map((planet, i) => {
        const angle = (time / planet.period_days) * Math.PI * 2 + i * 0.5;
        const x = Math.cos(angle) * planet.orbit_km;
        const z = Math.sin(angle) * planet.orbit_km;
        const position_km: [number, number, number] = [x, 0, z];

        return (
          <PlanetGeometry
            key={planet.name}
            planet={planet}
            position_km={position_km}
            toScenePosition={toScenePosition}
            toSceneSize={toSceneSize}
            shouldShowLabel={shouldShowLabel}
          />
        );
      })}

      {/* Orbit rings */}
      {PLANETS.map((planet) => (
        <OrbitRing
          key={`orbit-${planet.name}`}
          radius_km={planet.orbit_km}
          toSceneSize={toSceneSize}
        />
      ))}
    </group>
  );
};

const SunGeometry: React.FC<{
  toScenePosition: (pos: [number, number, number]) => THREE.Vector3;
  toSceneSize: (size: number) => number;
  shouldShowLabel: (type: CosmicObjectType, pos: [number, number, number]) => boolean;
}> = ({ toScenePosition, toSceneSize, shouldShowLabel }) => {
  const scenePos = toScenePosition([0, 0, 0]);
  const sunSize = toSceneSize(SUN.radius_km);
  const showLabel = shouldShowLabel('star', [0, 0, 0]);

  return (
    <group position={scenePos}>
      {/* Sun sphere */}
      <mesh>
        <sphereGeometry args={[sunSize, 32, 32]} />
        <meshBasicMaterial color="#ffdd00" />
      </mesh>

      {/* Corona */}
      <mesh>
        <sphereGeometry args={[sunSize * 1.5, 16, 16]} />
        <meshBasicMaterial color="#ffaa00" transparent opacity={0.2} />
      </mesh>

      {/* Label */}
      {showLabel && (
        <Html center distanceFactor={sunSize * 100}>
          <div className="bg-yellow-900/90 px-2 py-1 rounded text-yellow-300 text-xs whitespace-nowrap font-bold">
            The Sun (R = 696,340 km)
          </div>
        </Html>
      )}
    </group>
  );
};

const PlanetGeometry: React.FC<{
  planet: typeof PLANETS[number];
  position_km: [number, number, number];
  toScenePosition: (pos: [number, number, number]) => THREE.Vector3;
  toSceneSize: (size: number) => number;
  shouldShowLabel: (type: CosmicObjectType, pos: [number, number, number]) => boolean;
}> = ({ planet, position_km, toScenePosition, toSceneSize, shouldShowLabel }) => {
  const scenePos = toScenePosition(position_km);
  const planetSize = toSceneSize(planet.radius_km);
  const showLabel = shouldShowLabel('planet', position_km);

  return (
    <group position={scenePos}>
      {/* Planet sphere */}
      <mesh>
        <sphereGeometry args={[planetSize, 16, 16]} />
        <meshBasicMaterial color={planet.color} />
      </mesh>

      {/* Saturn's rings */}
      {planet.name === 'Saturn' && (
        <mesh rotation={[Math.PI / 3, 0, 0]}>
          <ringGeometry args={[planetSize * 1.4, planetSize * 2.3, 32]} />
          <meshBasicMaterial color="#d4a574" transparent opacity={0.6} side={THREE.DoubleSide} />
        </mesh>
      )}

      {/* Label */}
      {showLabel && (
        <Html center distanceFactor={planetSize * 50}>
          <div className="bg-black/80 px-1 py-0.5 rounded text-white text-[10px] whitespace-nowrap">
            {planet.name}
          </div>
        </Html>
      )}
    </group>
  );
};

const OrbitRing: React.FC<{
  radius_km: number;
  toSceneSize: (size: number) => number;
}> = ({ radius_km, toSceneSize }) => {
  const sceneRadius = toSceneSize(radius_km);
  const thickness = sceneRadius * 0.002;

  return (
    <mesh rotation={[Math.PI / 2, 0, 0]}>
      <ringGeometry args={[sceneRadius - thickness, sceneRadius + thickness, 64]} />
      <meshBasicMaterial color="#ffffff" transparent opacity={0.1} side={THREE.DoubleSide} />
    </mesh>
  );
};

// =============================================================================
// MILKY WAY (LOD)
// =============================================================================

const MilkyWayLOD: React.FC = () => {
  const { toScenePosition, toSceneSize, lodLevel, shouldShowLabel, controller } = useFloatingOrigin();
  const visibility = useVisibility();

  // Guard: need controller
  if (!controller) return null;
  if (!visibility.milkyWay) return null;

  // Render as geometry at galactic scale, as label at cosmic scale
  const renderAsGeometry = lodLevel === 'GALACTIC' || lodLevel === 'STELLAR';
  const renderAsLabel = lodLevel === 'CLUSTER' || lodLevel === 'COSMIC';

  if (renderAsGeometry) {
    return <MilkyWayGeometry toScenePosition={toScenePosition} toSceneSize={toSceneSize} />;
  }

  if (renderAsLabel) {
    return <MilkyWayLabel toScenePosition={toScenePosition} />;
  }

  return null;
};

const MilkyWayGeometry: React.FC<{
  toScenePosition: (pos: [number, number, number]) => THREE.Vector3;
  toSceneSize: (size: number) => number;
}> = ({ toScenePosition, toSceneSize }) => {
  const centerPos = toScenePosition([0, 0, 0]);
  const bulgeSize = toSceneSize(MILKY_WAY.bulge_radius_km);
  const diskRadius = toSceneSize(MILKY_WAY.radius_km);

  // Sun's position in the galaxy
  const sunGalacticPos = toScenePosition([MILKY_WAY.sun_distance_from_center_km, 0, 0]);

  // Generate disk stars
  const diskStars = useMemo(() => {
    const count = 50000;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      const r = Math.pow(Math.random(), 0.6) * diskRadius;
      const theta = Math.random() * Math.PI * 2;
      const h = (Math.random() - 0.5) * toSceneSize(MILKY_WAY.disk_height_km) * Math.exp(-r / (diskRadius * 0.3));

      positions[i * 3] = r * Math.cos(theta);
      positions[i * 3 + 1] = h;
      positions[i * 3 + 2] = r * Math.sin(theta);

      const temp = 0.4 + Math.random() * 0.4;
      colors[i * 3] = temp + 0.2;
      colors[i * 3 + 1] = temp * 0.85;
      colors[i * 3 + 2] = temp * 0.6 + 0.4;
    }

    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    return geom;
  }, [diskRadius, toSceneSize]);

  return (
    <group position={centerPos}>
      {/* Galactic bulge */}
      <mesh>
        <sphereGeometry args={[bulgeSize, 32, 32]} />
        <meshBasicMaterial color="#ffcc66" transparent opacity={0.5} />
      </mesh>

      {/* Disk stars */}
      <points geometry={diskStars}>
        <pointsMaterial size={bulgeSize * 0.01} vertexColors transparent opacity={0.8} sizeAttenuation />
      </points>

      {/* Sun marker */}
      <mesh position={[sunGalacticPos.x - centerPos.x, 0, 0]}>
        <sphereGeometry args={[bulgeSize * 0.05, 16, 16]} />
        <meshBasicMaterial color="#ffff00" />
      </mesh>

      {/* Labels */}
      <Html position={[0, diskRadius * 0.15, 0]} center>
        <div className="bg-black/85 px-2 py-1 rounded text-blue-300 text-xs font-bold border border-blue-500/30">
          Milky Way Galaxy
        </div>
      </Html>
    </group>
  );
};

const MilkyWayLabel: React.FC<{
  toScenePosition: (pos: [number, number, number]) => THREE.Vector3;
}> = ({ toScenePosition }) => {
  const pos = toScenePosition([0, 0, 0]);

  return (
    <group position={pos}>
      <mesh>
        <sphereGeometry args={[0.02, 16, 16]} />
        <meshBasicMaterial color="#6699ff" />
      </mesh>
      <Html center>
        <div className="bg-blue-900/80 px-2 py-1 rounded text-blue-300 text-[10px] whitespace-nowrap">
          Milky Way
        </div>
      </Html>
    </group>
  );
};

// =============================================================================
// Z² FUNDAMENTAL DOMAIN
// =============================================================================

const Z2Domain: React.FC = () => {
  const { toScenePosition, toSceneSize, lodLevel, controller } = useFloatingOrigin();
  const visibility = useVisibility();

  // Only render at COSMIC and CLUSTER scales (when Z² box is meaningful)
  if (!visibility.z2Domain) return null;
  if (lodLevel !== 'COSMIC' && lodLevel !== 'CLUSTER') return null;
  if (!controller) return null;

  const halfBox = toSceneSize(Z2.HALF_BOX_KM);

  // Domain box edges
  const edges: [[number, number, number], [number, number, number]][] = [
    // Bottom face
    [[-halfBox, -halfBox, -halfBox], [halfBox, -halfBox, -halfBox]],
    [[halfBox, -halfBox, -halfBox], [halfBox, halfBox, -halfBox]],
    [[halfBox, halfBox, -halfBox], [-halfBox, halfBox, -halfBox]],
    [[-halfBox, halfBox, -halfBox], [-halfBox, -halfBox, -halfBox]],
    // Top face
    [[-halfBox, -halfBox, halfBox], [halfBox, -halfBox, halfBox]],
    [[halfBox, -halfBox, halfBox], [halfBox, halfBox, halfBox]],
    [[halfBox, halfBox, halfBox], [-halfBox, halfBox, halfBox]],
    [[-halfBox, halfBox, halfBox], [-halfBox, -halfBox, halfBox]],
    // Verticals
    [[-halfBox, -halfBox, -halfBox], [-halfBox, -halfBox, halfBox]],
    [[halfBox, -halfBox, -halfBox], [halfBox, -halfBox, halfBox]],
    [[halfBox, halfBox, -halfBox], [halfBox, halfBox, halfBox]],
    [[-halfBox, halfBox, -halfBox], [-halfBox, halfBox, halfBox]],
  ];

  return (
    <group>
      {edges.map((edge, i) => (
        <Line
          key={i}
          points={edge}
          color="#00ffff"
          lineWidth={1.5}
          transparent
          opacity={0.3}
        />
      ))}

      {/* Corner labels */}
      {lodLevel === 'COSMIC' && (
        <>
          <Html position={[halfBox + 0.5, 0, 0]} center>
            <div className="text-cyan-400 font-mono text-xs">+10.3 Gpc</div>
          </Html>
          <Html position={[-halfBox - 0.5, 0, 0]} center>
            <div className="text-cyan-400 font-mono text-xs">-10.3 Gpc</div>
          </Html>
        </>
      )}
    </group>
  );
};

// =============================================================================
// Z² TOPOLOGICAL VERTICES
// =============================================================================

const Z2VerticesComponent: React.FC = () => {
  const { toScenePosition, toSceneSize, shouldShowLabel, lodLevel, controller } = useFloatingOrigin();
  const visibility = useVisibility();

  // Only render at COSMIC and CLUSTER scales
  if (!visibility.z2Vertices) return null;
  if (lodLevel !== 'COSMIC' && lodLevel !== 'CLUSTER') return null;
  if (!controller) return null;

  return (
    <group>
      {Z2_VERTICES.map((vertex) => {
        const scenePos = toScenePosition(vertex.position_km);
        const showLabel = shouldShowLabel('z2_vertex', vertex.position_km);

        // Size scales with LOD
        const baseSize = lodLevel === 'COSMIC' ? 0.3 : 0.1;

        return (
          <group key={vertex.id} position={scenePos}>
            {/* Core sphere */}
            <mesh>
              <sphereGeometry args={[baseSize, 32, 32]} />
              <meshBasicMaterial color={vertex.color} transparent opacity={0.9} />
            </mesh>

            {/* Glow */}
            <mesh>
              <sphereGeometry args={[baseSize * 1.5, 16, 16]} />
              <meshBasicMaterial color={vertex.color} transparent opacity={0.2} />
            </mesh>

            {/* Label */}
            {showLabel && (
              <Html center distanceFactor={10}>
                <div
                  className="px-2 py-1 rounded text-xs whitespace-nowrap font-bold"
                  style={{ backgroundColor: 'rgba(0,0,0,0.85)', color: vertex.color }}
                >
                  {vertex.id}: {vertex.name}
                </div>
              </Html>
            )}
          </group>
        );
      })}
    </group>
  );
};

// =============================================================================
// DYNAMIC CAMERA
// =============================================================================

const DynamicCamera: React.FC = () => {
  const { camera } = useThree();
  const cameraState = useCameraState();

  useEffect(() => {
    if (camera instanceof THREE.PerspectiveCamera) {
      camera.near = cameraState.nearPlane;
      camera.far = cameraState.farPlane;
      camera.updateProjectionMatrix();
    }
  }, [camera, cameraState.nearPlane, cameraState.farPlane]);

  return null;
};

// =============================================================================
// CONTROL PANEL
// =============================================================================

const ControlPanel: React.FC = () => {
  const visibility = useVisibility();
  const setVisibility = useUniverseStore((s) => s.setVisibility);
  const { start, stop, isRunning, waypointText } = useCinematicTour();

  // GW Simulation controls
  const gwSimulation = useGWSimulation();
  const startGWSimulation = useUniverseStore((s) => s.startGWSimulation);
  const stopGWSimulation = useUniverseStore((s) => s.stopGWSimulation);

  const toggles = [
    { key: 'solarSystem', label: 'Solar System', color: '#ffdd00' },
    { key: 'milkyWay', label: 'Milky Way', color: '#6699ff' },
    { key: 'z2Vertices', label: 'Z² Vertices', color: '#ff00ff' },
    { key: 'z2Domain', label: 'Z² Domain', color: '#00ffff' },
  ] as const;

  return (
    <div className="absolute top-16 left-4 bg-slate-900/95 p-4 rounded-lg border border-slate-700 z-10 backdrop-blur-sm max-w-[260px]">
      <h3 className="text-white font-bold mb-3">Z² Digital Twin</h3>

      {/* Tour button */}
      <button
        onClick={isRunning ? stop : start}
        disabled={gwSimulation.isRunning}
        className={`w-full mb-2 px-4 py-2 font-bold text-sm uppercase tracking-wider transition-all border rounded ${
          isRunning
            ? 'bg-red-900/50 text-red-400 border-red-500 hover:bg-red-900/80 animate-pulse'
            : gwSimulation.isRunning
            ? 'bg-slate-800/50 text-slate-500 border-slate-600 cursor-not-allowed'
            : 'bg-cyan-900/50 text-cyan-400 border-cyan-500 hover:bg-cyan-900/80'
        }`}
      >
        {isRunning ? '■ STOP' : '▶ CINEMATIC TOUR'}
      </button>

      {/* GW190521 Simulation button */}
      <button
        onClick={gwSimulation.isRunning ? stopGWSimulation : () => startGWSimulation(GW190521)}
        disabled={isRunning}
        className={`w-full mb-4 px-4 py-2 font-bold text-sm uppercase tracking-wider transition-all border rounded ${
          gwSimulation.isRunning
            ? 'bg-red-900/50 text-red-400 border-red-500 hover:bg-red-900/80 animate-pulse'
            : isRunning
            ? 'bg-slate-800/50 text-slate-500 border-slate-600 cursor-not-allowed'
            : 'bg-orange-900/50 text-orange-400 border-orange-500 hover:bg-orange-900/80'
        }`}
      >
        {gwSimulation.isRunning ? '■ STOP' : '▶ GW190521 WAVE'}
      </button>

      {/* Visibility toggles */}
      <div className="space-y-1">
        {toggles.map(({ key, label, color }) => (
          <label key={key} className="flex items-center gap-2 cursor-pointer hover:bg-slate-800 p-1 rounded">
            <input
              type="checkbox"
              checked={visibility[key]}
              onChange={() => setVisibility({ [key]: !visibility[key] })}
              className="w-3 h-3 accent-blue-500"
            />
            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />
            <span className="text-white text-xs">{label}</span>
          </label>
        ))}
      </div>

      <div className="mt-3 pt-2 border-t border-slate-700 text-slate-500 text-[10px]">
        Float64 Engine v11.1.0
      </div>
    </div>
  );
};

// =============================================================================
// TOUR OVERLAY
// =============================================================================

const TourOverlay: React.FC = () => {
  const { isRunning, waypointText } = useCinematicTour();

  if (!isRunning || !waypointText) return null;

  return (
    <div className="absolute bottom-24 left-1/2 -translate-x-1/2 z-20 max-w-2xl">
      <div className="bg-black/90 text-white font-mono text-lg border border-cyan-500 px-6 py-4 rounded-lg shadow-[0_0_30px_rgba(6,182,212,0.4)]">
        <p>{waypointText}</p>
      </div>
    </div>
  );
};

// =============================================================================
// GW SIMULATION HUD (Directive SSS)
// =============================================================================

const GWSimulationHUD: React.FC = () => {
  const gwSimulation = useGWSimulation();

  if (!gwSimulation.isRunning || !gwSimulation.currentEvent) return null;

  const currentPhase = WAVE_RIDER_SEQUENCE[gwSimulation.currentPhase];
  const phasePercent = Math.round(gwSimulation.phaseProgress * 100);

  // Format large distances
  const formatLightYears = (ly: number): string => {
    if (ly >= 1e9) return `${(ly / 1e9).toFixed(2)} Gly`;
    if (ly >= 1e6) return `${(ly / 1e6).toFixed(2)} Mly`;
    if (ly >= 1e3) return `${(ly / 1e3).toFixed(2)} kly`;
    return `${ly.toFixed(0)} ly`;
  };

  const formatStrain = (h: number): string => {
    const exp = Math.floor(Math.log10(Math.abs(h)));
    const mantissa = h / Math.pow(10, exp);
    return `${mantissa.toFixed(1)}×10^${exp}`;
  };

  return (
    <div className="absolute top-4 right-4 z-20 font-mono text-sm">
      {/* Event info */}
      <div className="bg-black/95 border border-orange-500/50 rounded-lg p-4 mb-2 shadow-[0_0_20px_rgba(249,115,22,0.3)]">
        <div className="text-orange-400 font-bold text-base mb-2">
          {gwSimulation.currentEvent.name}
        </div>
        <div className="text-slate-400 text-xs space-y-1">
          <div>Mass: {gwSimulation.currentEvent.mass1_solar} + {gwSimulation.currentEvent.mass2_solar} M☉</div>
          <div>Distance: {(gwSimulation.currentEvent.distance_Mpc / 1000).toFixed(1)} Gpc</div>
        </div>
      </div>

      {/* Phase info */}
      <div className="bg-black/95 border border-yellow-500/50 rounded-lg p-4 mb-2">
        <div className="text-yellow-400 font-bold mb-1">
          Phase {gwSimulation.currentPhase + 1}/{WAVE_RIDER_SEQUENCE.length}: {currentPhase?.name}
        </div>
        <div className="text-slate-300 text-xs mb-2">
          {currentPhase?.description}
        </div>
        {/* Progress bar */}
        <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-yellow-500 to-orange-500 transition-all"
            style={{ width: `${phasePercent}%` }}
          />
        </div>
      </div>

      {/* Live telemetry */}
      <div className="bg-black/95 border border-cyan-500/50 rounded-lg p-4">
        <div className="text-cyan-400 font-bold mb-2">LIVE TELEMETRY</div>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="text-slate-400">Wave Front:</div>
          <div className="text-cyan-300">{formatLightYears(gwSimulation.waveRadius_km / 9.461e12)}</div>

          <div className="text-slate-400">To Earth:</div>
          <div className="text-green-300">{formatLightYears(gwSimulation.lightYearsRemaining)}</div>

          <div className="text-slate-400">Strain h:</div>
          <div className="text-orange-300">{formatStrain(gwSimulation.currentStrain)}</div>
        </div>
      </div>
    </div>
  );
};

// =============================================================================
// GW LATTICE VISUALIZATION (Directive QQQ)
// =============================================================================

const GWLatticeVisualization: React.FC = () => {
  const gwSimulation = useGWSimulation();
  const updateGWSimulation = useUniverseStore((s) => s.updateGWSimulation);
  const { toScenePosition, toSceneSize, controller } = useFloatingOrigin();

  const shaderMaterialRef = useRef<THREE.ShaderMaterial>(null);
  const lastTimeRef = useRef(0);

  // Create lattice geometry
  const latticeGeometry = useMemo(() => {
    return createLatticePointCloud(50, 30); // 50 scene units, 30^3 = 27000 points
  }, []);

  // Create shader uniforms
  const uniforms = useMemo(() => ({
    time: { value: 0 },
    epicenter: { value: new THREE.Vector3(0, 0, 0) },
    waveRadius: { value: 0 },
    strain: { value: 0.3 },
    frequency: { value: 0.5 },
    decayLength: { value: 100 },
  }), []);

  // Update simulation each frame
  useFrame((state) => {
    if (!gwSimulation.isRunning) return;

    const deltaTime = state.clock.elapsedTime - lastTimeRef.current;
    lastTimeRef.current = state.clock.elapsedTime;

    // Cap delta to prevent jumps
    const cappedDelta = Math.min(deltaTime, 0.1);
    updateGWSimulation(cappedDelta);

    // Update shader uniforms
    if (shaderMaterialRef.current && gwSimulation.currentEvent) {
      shaderMaterialRef.current.uniforms.time.value = state.clock.elapsedTime;
      shaderMaterialRef.current.uniforms.waveRadius.value = toSceneSize(gwSimulation.waveRadius_km);

      const epicenter = toScenePosition(gwSimulation.currentEvent.position_km);
      shaderMaterialRef.current.uniforms.epicenter.value.copy(epicenter);
    }
  });

  if (!gwSimulation.isRunning || !gwSimulation.currentEvent) return null;

  const epicenterScene = toScenePosition(gwSimulation.currentEvent.position_km);
  const waveRadiusScene = toSceneSize(gwSimulation.waveRadius_km);

  return (
    <group>
      {/* Event epicenter marker */}
      <mesh position={epicenterScene}>
        <sphereGeometry args={[0.3, 16, 16]} />
        <meshBasicMaterial color="#ff6600" />
      </mesh>
      <mesh position={epicenterScene}>
        <sphereGeometry args={[0.5, 16, 16]} />
        <meshBasicMaterial color="#ff6600" transparent opacity={0.3} />
      </mesh>

      {/* Wave front sphere */}
      <mesh position={epicenterScene}>
        <sphereGeometry args={[Math.max(waveRadiusScene, 0.1), 64, 32]} />
        <meshBasicMaterial
          color="#ffcc00"
          transparent
          opacity={0.15}
          wireframe
        />
      </mesh>

      {/* Inner expanding shell */}
      <mesh position={epicenterScene}>
        <sphereGeometry args={[Math.max(waveRadiusScene * 0.95, 0.05), 32, 16]} />
        <meshBasicMaterial
          color="#ff8800"
          transparent
          opacity={0.1}
          side={THREE.BackSide}
        />
      </mesh>

      {/* Lattice point cloud with strain */}
      <points geometry={latticeGeometry}>
        <shaderMaterial
          ref={shaderMaterialRef}
          uniforms={uniforms}
          vertexShader={`
            uniform float time;
            uniform vec3 epicenter;
            uniform float waveRadius;
            uniform float strain;
            uniform float frequency;
            uniform float decayLength;

            attribute vec3 color;
            varying vec3 vColor;
            varying float vStrain;

            void main() {
              // Distance from epicenter
              vec3 toEpicenter = position - epicenter;
              float r = length(toEpicenter);

              // Distance from wave front
              float distFromWave = r - waveRadius;

              // Wave packet envelope
              float waveWidth = 3.0;
              float envelope = exp(-distFromWave * distFromWave / (2.0 * waveWidth * waveWidth));

              // Phase
              float phase = frequency * (r - waveRadius);

              // Strain displacement
              float h = strain * sin(phase * 6.28318) * envelope / (1.0 + r / decayLength);
              vStrain = h;

              // Displace position
              vec3 displaced = position;
              if (r > 0.01) {
                vec3 radial = toEpicenter / r;
                // Cross polarization effect
                displaced += vec3(h * 0.5, -h * 0.3, h * 0.2);
              }

              // Color based on strain
              vColor = color;
              if (envelope > 0.1) {
                vColor = mix(color, vec3(1.0, 0.8, 0.2), envelope);
              }

              vec4 mvPosition = modelViewMatrix * vec4(displaced, 1.0);
              gl_PointSize = 3.0 * (1.0 + envelope * 2.0);
              gl_Position = projectionMatrix * mvPosition;
            }
          `}
          fragmentShader={`
            varying vec3 vColor;
            varying float vStrain;

            void main() {
              // Circular point shape
              vec2 center = gl_PointCoord - 0.5;
              float dist = length(center);
              if (dist > 0.5) discard;

              // Glow effect
              float glow = 1.0 - dist * 2.0;

              vec3 finalColor = vColor * glow;
              gl_FragColor = vec4(finalColor, glow * 0.8);
            }
          `}
          transparent
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </points>

      {/* Earth marker */}
      <mesh position={toScenePosition([0, 0, 0])}>
        <sphereGeometry args={[0.15, 16, 16]} />
        <meshBasicMaterial color="#00ff00" />
      </mesh>
      <Html position={toScenePosition([0, 0.3, 0])} center>
        <div className="text-green-400 text-xs font-mono bg-black/80 px-1 rounded">EARTH</div>
      </Html>
    </group>
  );
};

// =============================================================================
// SCENE
// =============================================================================

const Scene: React.FC = () => {
  const controlsRef = useRef<any>(null);

  return (
    <>
      <color attach="background" args={['#030308']} />
      <Stars radius={100} depth={50} count={3000} factor={4} fade />
      <ambientLight intensity={0.4} />

      {/* Dynamic camera updates */}
      <DynamicCamera />

      {/* Celestial objects with LOD */}
      <SolarSystemLOD />
      <MilkyWayLOD />
      <Z2Domain />
      <Z2VerticesComponent />

      {/* GW190521 Simulation (Directives QQQ, RRR, SSS) */}
      <GWLatticeVisualization />

      {/* Controls */}
      <OrbitControls
        ref={controlsRef}
        enablePan
        enableZoom
        enableRotate
        zoomSpeed={1.2}
        rotateSpeed={0.5}
        enableDamping
        dampingFactor={0.05}
      />

      <PerspectiveCamera makeDefault position={[2, 1.5, 2]} fov={50} />
    </>
  );
};

// =============================================================================
// MAIN COMPONENT
// =============================================================================

const UniverseCanvas: React.FC = () => {
  const initFloatingOrigin = useUniverseStore((s) => s.initFloatingOrigin);

  // Initialize engine on mount
  useEffect(() => {
    initFloatingOrigin();
  }, [initFloatingOrigin]);

  return (
    <div className="relative w-full h-[800px] bg-slate-950 rounded-lg overflow-hidden">
      <ScaleIndicator />
      <ControlPanel />
      <TourOverlay />
      <GWSimulationHUD />

      <Canvas
        gl={{ antialias: true, logarithmicDepthBuffer: true }}
        dpr={[1, 2]}
      >
        <Suspense fallback={null}>
          <Scene />
        </Suspense>
      </Canvas>

      {/* Legend */}
      <div className="absolute bottom-4 right-4 bg-slate-900/95 p-2 rounded-lg border border-slate-700 z-10 text-[10px] space-y-0.5">
        <div className="flex items-center gap-1 text-yellow-400">
          <span className="w-1.5 h-1.5 rounded-full bg-yellow-400" />Solar System
        </div>
        <div className="flex items-center gap-1 text-blue-400">
          <span className="w-1.5 h-1.5 rounded-full bg-blue-400" />Milky Way
        </div>
        <div className="flex items-center gap-1 text-fuchsia-400">
          <span className="w-1.5 h-1.5 rounded-full bg-fuchsia-400" />Z² Vertices
        </div>
        <div className="flex items-center gap-1 text-cyan-400">
          <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />Z² Domain
        </div>
      </div>
    </div>
  );
};

export default UniverseCanvas;
