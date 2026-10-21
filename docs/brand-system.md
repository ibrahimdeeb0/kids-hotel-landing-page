# Kids Hotel visual system

## Source

The client-supplied `Kids hotel.pdf` contains a single embedded 5906 × 5906 RGB image. The web logo assets are resized copies of that artwork, preserving its colors, white background, lettering and stars. They are not a vector recreation. The old house illustration and letter-k icon are no longer referenced by the pages.

Re-extract with `python3 scripts/extract-logo.py '/path/to/Kids hotel.pdf'` using a Python environment with Pillow and pypdf. The PDF itself is not required for serving or building the website.

## Palette

Values are sampled from the raster artwork; they are not an official supplied brand specification.

| Token | Hex | Use |
| --- | --- | --- |
| Primary | `#EE5255` | Logo coral, decorative icons, color strip |
| Primary strong | `#B82D42` | Buttons, links, emphasized headings |
| Primary hover | `#992238` | Button interaction |
| Blue | `#43B3E5` | Decorative accents |
| Yellow | `#FEC92D` | Decorative accents |
| Purple | `#9E4EA5` | Secondary accent |
| Green | `#69B76C` | Secondary accent |
| Canvas | `#FFF8F8` | Main background |
| Surface | `#FFFFFF` | Artwork and contact panel |
| Surface soft | `#FFF0F1` | Company section |
| Text | `#322B3D` | Main reading text |
| Muted text | `#655C70` | Supporting copy |

The logo's bright red is retained for artwork. The darker derivative supports readable white button labels and small colored text. Do not use yellow, blue or green as small text on white.

## Typography and components

- English: Trebuchet MS, with Arial/sans-serif fallbacks. Arabic: Tahoma, with Arial/sans-serif fallbacks. All fonts are local system fonts; the logo lettering remains part of the original image.
- Bold rounded headings, balanced text wrapping, Arabic-specific line heights and no Arabic letter spacing.
- Eight spacing steps (`--space-1` through `--space-8`), three radius tokens and one shared soft shadow.
- Pill buttons and language switch; rounded white contact panel; circular decorative accents echo the logo.
- Keep clear space around the original logo. Do not stretch, recolor or crop the artwork.
- The original five stars remain part of the artwork; the website makes no rating or accreditation claim.
- Shared components support RTL and LTR, visible keyboard focus, a skip link and reduced motion.

## Files

`styles.css` is the source of truth for tokens and component styles. Shared header/footer live in `src/partials`; localized content stays in `src/locales`. Rebuild all four pages with `node scripts/build.mjs` after editing templates.
