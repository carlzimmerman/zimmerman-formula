// =============================================================================
// VESSEL SELECTOR UI (Directive WWW)
// =============================================================================
// Modal for selecting which vessel to fly in the Z² universe
// =============================================================================

'use client';

import React from 'react';
import { VesselType, VESSEL_CONFIGS, usePlayerStore } from '../../store/playerStore';

const VesselSelector: React.FC = () => {
  const {
    isSelectingVessel,
    activeVessel,
    setVessel,
    closeVesselSelector,
    startPlayerMode,
  } = usePlayerStore();

  if (!isSelectingVessel) return null;

  const handleSelect = (vessel: VesselType) => {
    setVessel(vessel);
  };

  const handleLaunch = () => {
    closeVesselSelector();
    startPlayerMode();
  };

  const vessels = Object.values(VESSEL_CONFIGS);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
      <div className="bg-slate-900 border border-cyan-500/50 rounded-xl p-6 max-w-2xl w-full mx-4 shadow-[0_0_50px_rgba(6,182,212,0.3)]">
        {/* Header */}
        <div className="text-center mb-6">
          <h2 className="text-3xl font-bold text-cyan-400 mb-2">
            SELECT YOUR VESSEL
          </h2>
          <p className="text-slate-400 text-sm">
            Choose your craft for exploring the T³/Z₂ universe
          </p>
        </div>

        {/* Vessel Grid */}
        <div className="grid grid-cols-5 gap-3 mb-6">
          {vessels.map((vessel) => (
            <button
              key={vessel.id}
              onClick={() => handleSelect(vessel.id)}
              className={`
                relative p-4 rounded-lg border-2 transition-all
                ${activeVessel === vessel.id
                  ? 'border-cyan-400 bg-cyan-900/30 shadow-[0_0_20px_rgba(6,182,212,0.4)]'
                  : 'border-slate-600 bg-slate-800/50 hover:border-slate-500 hover:bg-slate-800'
                }
              `}
            >
              {/* Vessel Icon */}
              <div
                className="w-12 h-12 mx-auto mb-2 rounded-full flex items-center justify-center text-2xl"
                style={{ backgroundColor: vessel.color + '33' }}
              >
                {vessel.id === 'ufo' && '🛸'}
                {vessel.id === 'truck' && '🚛'}
                {vessel.id === 'sedan' && '🚗'}
                {vessel.id === 'plane' && '✈️'}
                {vessel.id === 'donut' && '🍩'}
              </div>

              {/* Name */}
              <div className="text-white text-sm font-bold text-center">
                {vessel.name}
              </div>

              {/* Selected indicator */}
              {activeVessel === vessel.id && (
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-cyan-400 rounded-full flex items-center justify-center">
                  <span className="text-black text-xs">✓</span>
                </div>
              )}
            </button>
          ))}
        </div>

        {/* Selected Vessel Details */}
        <div className="bg-slate-800/50 rounded-lg p-4 mb-6 border border-slate-700">
          <div className="flex items-center gap-4">
            <div
              className="w-16 h-16 rounded-full flex items-center justify-center text-4xl"
              style={{ backgroundColor: VESSEL_CONFIGS[activeVessel].color + '33' }}
            >
              {activeVessel === 'ufo' && '🛸'}
              {activeVessel === 'truck' && '🚛'}
              {activeVessel === 'sedan' && '🚗'}
              {activeVessel === 'plane' && '✈️'}
              {activeVessel === 'donut' && '🍩'}
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-white">
                {VESSEL_CONFIGS[activeVessel].name}
              </h3>
              <p className="text-slate-400 text-sm mb-2">
                {VESSEL_CONFIGS[activeVessel].description}
              </p>
              <div className="flex gap-4 text-xs">
                <div>
                  <span className="text-slate-500">Max Warp:</span>
                  <span className="text-cyan-400 ml-1">
                    {VESSEL_CONFIGS[activeVessel].maxSpeed} Gpc/s
                  </span>
                </div>
                <div>
                  <span className="text-slate-500">Accel:</span>
                  <span className="text-green-400 ml-1">
                    {VESSEL_CONFIGS[activeVessel].acceleration}x
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Controls Info */}
        <div className="bg-slate-800/30 rounded-lg p-3 mb-6 text-xs text-slate-400">
          <div className="grid grid-cols-2 gap-2">
            <div><span className="text-cyan-400">WASD</span> - Move</div>
            <div><span className="text-cyan-400">Mouse</span> - Look</div>
            <div><span className="text-cyan-400">SHIFT</span> - Warp Drive</div>
            <div><span className="text-cyan-400">ESC</span> - Exit</div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <button
            onClick={closeVesselSelector}
            className="flex-1 px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white font-bold rounded-lg transition-colors"
          >
            CANCEL
          </button>
          <button
            onClick={handleLaunch}
            className="flex-1 px-6 py-3 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold rounded-lg transition-all shadow-[0_0_20px_rgba(6,182,212,0.4)]"
          >
            🚀 LAUNCH
          </button>
        </div>
      </div>
    </div>
  );
};

export default VesselSelector;
