# tools/assets/brand — brand assets for the factory

Drop real brand files here and every generated asset picks them up automatically:

- **Fonts** → `fonts/` (woff2/ttf/otf), then add `@font-face` + selectors in `brand.css`.
- **Logos** → e.g. `shikshalokam.png`, `shikshagraha.png`; reference them in a poster spec's
  `"logos": ["tools/assets/brand/shikshalokam.png", "..."]` and they're embedded in the footer.
- **`brand.css`** → applied on top of the built-in styles for carousel + poster (override colours,
  fonts, spacing).

Nothing here yet = assets fall back to the SL 2.0 palette + a clean system font (still on-brand).
