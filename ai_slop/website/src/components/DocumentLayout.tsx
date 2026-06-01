'use client'

import Link from 'next/link'
import { ReactNode } from 'react'

interface DocumentLayoutProps {
  title: string
  description: string
  phase: 'math' | 'physics'
  currentIndex: number
  children: ReactNode
  prevLink?: { href: string; title: string }
  nextLink?: { href: string; title: string }
}

export default function DocumentLayout({
  title,
  description,
  phase,
  currentIndex,
  children,
  prevLink,
  nextLink,
}: DocumentLayoutProps) {
  const phaseColor = phase === 'math' ? 'blue' : 'green'
  const phaseLabel = phase === 'math' ? 'Mathematics' : 'Physics'
  const phaseIcon = phase === 'math' ? '📐' : '⚛️'

  return (
    <main className="min-h-screen bg-[#fafafa]">
      <div className="max-w-4xl mx-auto px-4 py-6 md:py-8">
        {/* Breadcrumb */}
        <div className="mb-4 flex items-center gap-2 text-sm">
          <Link href="/office-hours" className="text-blue-600 hover:underline">
            Office Hours
          </Link>
          <span className="text-gray-400">/</span>
          <span className={`text-${phaseColor}-600`}>
            {phaseIcon} {phaseLabel}
          </span>
          <span className="text-gray-400">/</span>
          <span className="text-gray-600">{currentIndex.toString().padStart(2, '0')}</span>
        </div>

        {/* Header */}
        <header className="mb-8">
          <div className={`inline-block px-3 py-1 rounded-full text-xs font-medium mb-3 ${
            phase === 'math'
              ? 'bg-blue-100 text-blue-700'
              : 'bg-green-100 text-green-700'
          }`}>
            {phaseLabel} · Document {currentIndex + 1}
          </div>
          <h1 className="text-2xl md:text-3xl font-semibold text-gray-900 mb-2">
            {title}
          </h1>
          <p className="text-gray-600">{description}</p>
        </header>

        {/* Content */}
        <article className="prose prose-gray max-w-none">
          {children}
        </article>

        {/* Navigation */}
        <nav className="mt-12 pt-6 border-t border-gray-200">
          <div className="flex justify-between items-center">
            {prevLink ? (
              <Link
                href={prevLink.href}
                className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
              >
                <span>←</span>
                <div className="text-left">
                  <div className="text-xs text-gray-400">Previous</div>
                  <div className="text-sm font-medium">{prevLink.title}</div>
                </div>
              </Link>
            ) : (
              <div />
            )}

            <Link
              href="/office-hours"
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm text-gray-700 transition-colors"
            >
              All Documents
            </Link>

            {nextLink ? (
              <Link
                href={nextLink.href}
                className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
              >
                <div className="text-right">
                  <div className="text-xs text-gray-400">Next</div>
                  <div className="text-sm font-medium">{nextLink.title}</div>
                </div>
                <span>→</span>
              </Link>
            ) : (
              <div />
            )}
          </div>
        </nav>

        {/* Footer */}
        <footer className="mt-8 text-center text-sm text-gray-500 py-6 border-t border-gray-200">
          <Link href="/" className="text-blue-600 hover:underline">
            Zimmerman Framework
          </Link>
        </footer>
      </div>
    </main>
  )
}

// Reusable section components
export function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="my-8">
      <h2 className="text-xl font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">
        {title}
      </h2>
      {children}
    </section>
  )
}

export function SubSection({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="my-6">
      <h3 className="text-lg font-medium text-gray-800 mb-3">{title}</h3>
      {children}
    </div>
  )
}

export function Formula({ children, label }: { children: ReactNode; label?: string }) {
  return (
    <div className="my-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
      <div className="font-mono text-center text-lg text-gray-900">{children}</div>
      {label && <div className="text-center text-sm text-gray-600 mt-2">{label}</div>}
    </div>
  )
}

export function KeyPoint({ children }: { children: ReactNode }) {
  return (
    <div className="my-4 p-4 bg-amber-50 border-l-4 border-amber-400 rounded-r-lg">
      <div className="text-gray-800">{children}</div>
    </div>
  )
}

export function Z2Connection({ formula, description }: { formula: string; description: string }) {
  return (
    <div className="my-4 p-4 bg-purple-50 border border-purple-200 rounded-lg">
      <div className="flex items-center gap-3">
        <span className="text-purple-600 font-bold">Z²</span>
        <div>
          <div className="font-mono text-purple-800">{formula}</div>
          <div className="text-sm text-purple-600">{description}</div>
        </div>
      </div>
    </div>
  )
}

export function InteractiveBox({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="my-6 p-4 bg-white border-2 border-dashed border-gray-300 rounded-lg">
      <div className="text-sm font-medium text-gray-500 mb-3 flex items-center gap-2">
        <span>🎮</span> Interactive: {title}
      </div>
      {children}
    </div>
  )
}
