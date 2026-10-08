'use client'

import React, { useState } from 'react'

/** renders its children at once on capable devices; on weak ones it waits for a click so nothing heavy starts by itself */
export default function Gate({ auto, label, note, children }: { auto: boolean; label: string; note?: string; children: React.ReactNode }) {
  const [on, setOn] = useState(auto)
  if (on) return <>{children}</>
  return (
    <div className="rounded-xl border border-gray-300 bg-gray-50 p-6 text-sm text-gray-700 max-w-3xl">
      {note && <p className="mb-3">{note}</p>}
      <button onClick={() => setOn(true)} className="px-4 py-2 rounded-lg bg-gray-900 text-white text-sm hover:bg-gray-700">{label}</button>
    </div>
  )
}
