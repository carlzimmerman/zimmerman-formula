# Zimmerman Framework Website

Interactive visualization of the Zimmerman Framework: deriving physics from Z = 2√(8π/3).

## Features

- **Animated hero** with counting Z value
- **Formula cards** with KaTeX rendering and accuracy bars
- **Dimensional hierarchy** visualization with animated nodes
- **Accuracy summary** with animated progress bars
- **Responsive design** for mobile and desktop
- **Firebase hosting** ready

## Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **KaTeX** - Math rendering
- **Firebase Hosting** - Static deployment

## Setup

```bash
# Install dependencies
cd website
npm install

# Run development server
npm run dev

# Open http://localhost:3000
```

## Deploy to Firebase

### First-time setup:

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize project (if needed)
firebase init hosting

# Select your project or create new one
```

### Deploy:

```bash
# Build the static site
npm run build

# Deploy to Firebase
firebase deploy --only hosting

# Or use the shortcut
npm run deploy
```

## Project Structure

```
website/
├── src/
│   ├── app/
│   │   ├── globals.css      # Global styles
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Home page
│   └── components/
│       ├── Hero.tsx         # Hero section with Z animation
│       ├── FormulaCard.tsx  # Formula display cards
│       ├── DimensionalHierarchy.tsx  # 26→11→8→7→3 visualization
│       ├── AccuracyTable.tsx # Summary statistics
│       └── Footer.tsx       # Links and DOI
├── firebase.json            # Firebase config
├── next.config.js           # Next.js config (static export)
├── tailwind.config.js       # Tailwind customizations
└── package.json
```

## Customization

### Colors (tailwind.config.js)
- `cosmic-dark` - Background (#0a0a1a)
- `cosmic-blue` - Secondary bg (#1a1a3a)
- `quantum-purple` - Primary accent (#6366f1)
- `dimension-gold` - Highlight (#fbbf24)
- `energy-cyan` - Secondary accent (#22d3d1)

### Adding New Formulas

Edit `src/app/page.tsx` and add a new `FormulaCard`:

```tsx
<FormulaCard
  title="Your Formula Name"
  formula="\\LaTeX_{formula}"
  predicted="1.234"
  measured="1.234"
  error={0.01}
  delay={0.6}
/>
```

## License

MIT - Carl Zimmerman 2026
