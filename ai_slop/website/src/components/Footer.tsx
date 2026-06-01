'use client'

import { motion } from 'framer-motion'

export default function Footer() {
  return (
    <footer className="py-16 px-4 border-t border-gray-800">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center"
        >
          {/* DOI */}
          <div className="mb-8">
            <span className="text-gray-500">DOI: </span>
            <a
              href="https://doi.org/10.5281/zenodo.19199167"
              target="_blank"
              rel="noopener noreferrer"
              className="text-quantum-purple hover:text-quantum-purple/80 transition-colors"
            >
              10.5281/zenodo.19199167
            </a>
          </div>

          {/* Links */}
          <div className="flex justify-center gap-8 mb-8">
            <a
              href="https://github.com/carlzimmerman/zimmerman-formula"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-white transition-colors flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
              </svg>
              GitHub
            </a>
            <a
              href="https://arxiv.org/search/?query=zimmerman+formula"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-white transition-colors"
            >
              arXiv
            </a>
          </div>

          {/* Creative Commons License */}
          <div className="mb-8">
            <a
              href="https://creativecommons.org/licenses/by/4.0/"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
            >
              <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9v-2h2v2zm0-4H9V7h2v5zm4 4h-2v-2h2v2zm0-4h-2V7h2v5z"/>
              </svg>
              <span className="text-sm">CC BY 4.0</span>
            </a>
            <p className="text-xs text-gray-500 mt-2">
              This work is licensed under a Creative Commons Attribution 4.0 International License.
              <br />
              Free to share and adapt with attribution.
            </p>
          </div>

          {/* Copyright */}
          <div className="text-gray-600 text-sm">
            <p>Carl Zimmerman | 2024-2026</p>
            <p className="mt-2 text-gray-700">
              "The universe is mathematical. Z = 2√(8π/3) is its fundamental constant."
            </p>
          </div>
        </motion.div>
      </div>
    </footer>
  )
}
