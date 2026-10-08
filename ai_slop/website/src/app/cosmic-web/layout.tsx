import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'The simulation behind the growth check',
  description: "Real output of the 512³ particle-mesh run that tested the framework's growth rule, beside a Newtonian control: a 3D box, single cells, individual halo particles and a timeline from z = 49 to today. It checks that the rule does not break the cosmic web; it is not evidence for the framework.",
  openGraph: { title: 'The simulation behind the growth check', description: "Real output of the 512³ particle-mesh run that tested the framework's growth rule, beside a Newtonian control: a 3D box, single cells, individual halo particles and a timeline from z = 49 to today. It checks that the rule does not break the cosmic web; it is not evidence for the framework." },
}

export default function Layout({ children }: { children: React.ReactNode }) {
  return children
}
