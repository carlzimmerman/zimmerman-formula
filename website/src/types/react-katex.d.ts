declare module 'react-katex' {
  import { ComponentType } from 'react'

  interface KatexProps {
    math: string
    errorColor?: string
    renderError?: (error: Error) => React.ReactNode
  }

  export const InlineMath: ComponentType<KatexProps>
  export const BlockMath: ComponentType<KatexProps>
}
