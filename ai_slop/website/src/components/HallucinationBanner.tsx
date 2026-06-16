'use client';

/**
 * HallucinationBanner
 *
 * An academic disclaimer placed at the top of pages whose content was generated
 * by an earlier automated AI research effort ("Z² Framework") and did NOT survive
 * independent audit. These pages are retained for transparency, not as claims.
 *
 * Pass `reason` to state the page-specific reason the content is not valid.
 */

export default function HallucinationBanner({
  reason,
  title = 'Retained for transparency — not a validated result',
}: {
  reason?: string;
  title?: string;
}) {
  return (
    <aside
      role="note"
      aria-label="Validity notice"
      className="mb-6 rounded-md border border-amber-700/60 border-l-4 border-l-amber-500 bg-amber-950/30 px-5 py-4 text-sm leading-relaxed text-amber-100/90"
    >
      <p className="mb-2 font-semibold tracking-wide text-amber-300">
        Notice — {title}
      </p>
      <p className="mb-2 text-amber-100/80">
        The material on this page was produced by an earlier automated AI system as part of the
        &ldquo;Z&sup2; Framework&rdquo; research effort. On independent audit it did not hold up, and it is
        kept here only as a record of that work — it is <span className="font-medium">not</span> a
        scientific claim of the current framework.
      </p>
      <p className="mb-2 text-amber-100/80">
        {reason ??
          'The central premise — that the number Z² = 32π/3 recurs meaningfully across unrelated ' +
            'domains — is a numerical coincidence. A randomly chosen constant of similar size reproduces the ' +
            'same retrodictions equally well, and the specific predictions fail a false-discovery / ' +
            'look-elsewhere test. The particle-physics and cosmology figures presented here (specific masses, ' +
            'ratios, and “derivations”) are fabricated and are not part of the audited framework.'}
      </p>
      <p className="text-amber-100/70">
        What did survive audit is the empirically grounded gravity-and-dark-sector physics — the radial
        acceleration relation and baryonic Tully&ndash;Fisher behaviour, with a&#8320; = c&sup2;&radic;(&Lambda;/32&pi;)
        as a de Sitter curvature scale. See the published papers and the{' '}
        <a className="underline decoration-amber-500/50 underline-offset-2 hover:text-amber-200" href="/simulate">
          Simulations
        </a>{' '}
        page. The complete retraction record is kept in <code className="text-amber-200/90">RETRACTIONS.md</code>.
      </p>
    </aside>
  );
}
