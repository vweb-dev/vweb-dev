# VWEB.DEV Motion Graphics — Profile Design System

**Profile:** https://github.com/vweb-dev

## Design approach
Premium black and muted-gold palette, high contrast, measured motion and clean geometric technical illustrations. The objective is to communicate a professional digital studio identity rather than a flashy demo.

## Motion layers
- Hero: orbiting technology rings, signal particles, dashed tracer paths and soft halos.
- Section headings: moving technical indicators.
- Service realms: coordinated signal trails and pulsing nodes.
- Delivery engine: Discover → Design → Engineer → Evolve workflow choreography.
- Tech stack and project cards: project-specific telemetry, networking, chart and UI motifs.
- Statistics and CTA: decorative motion; important text stays visible at all times.

## Technical guardrails
- Pure, self-contained SVG and CSS keyframes. No JavaScript or external assets in the motion panels.
- `prefers-reduced-motion: reduce` disables CSS animations.
- Every illustration has a full static layout when animation is unsupported.
- SVG motion playback varies by GitHub context and browser. GitHub's file preview does not promise SVG animations, and some clients may present static versions. For guaranteed playback, a separately rendered animated GIF is required.
- Snapshot repository count is not a live API-driven metric and should be updated manually.
- Official VWEB.DEV logo assets have not been regenerated or changed.
