# Notes for working on this site

How the site is built, previewed and published is in `README.md`. This file
keeps the decisions that are not obvious from the code, starting with colour.

## Colours in figures

Every figure on the site, whether an SVG in `includes/` or a PNG drawn by a
script in `scripts/`, uses one palette. Each colour has a fixed role, so a
reader who learns it once can read every figure.

| Role | CSS token | Light | Dark | Used for |
|---|---|---|---|---|
| Context | `--st-muted` (figures: `MUTED`) | `#51606b` (`#a3b1ba` in PNGs) | `#95a7b2` | axes, grids, reference and "before" curves, controls, arrows |
| Ink | `--st-ink` (`INK`) | `#13212b` | `#e4ecf0` | text, boundaries, the one line that must read as neutral |
| c1, vermilion | `--st-c1` (`ACCENT`) | `#cf3e24` | `#f26a3d` | the main result, theory, the highlight; Ops side of the DevOps loop; class 1 |
| c2, blue | `--st-c2` (`BLUE`) | `#1a5188` | `#6cb6f0` | data, simulations, estimates; Dev side of the loop; class 0; services |
| c3, amber | `--st-c3` (`AMBER`) | `#efb93a` | `#ffd770` | a secondary series, a third category, data stores |
| c3 edge | `--st-c3-edge` (`AMBER_EDGE`) | `#a87412` | `#ffd770` | the outline of every amber mark, because amber alone is too light on a white page |

Covers for the Blog list are drawn on the petrol banner (`#1d4e6b` to
`#0f2e42`) by `scripts/post_covers.py`, with `LIGHT` `#f26a3d`, `SKY`
`#8cc3e0`, `AMBER` `#ffd770` and white. Talk covers in `includes/cover-*.svg`
sit on a dark background and use the dark-theme values. The sun in
`cover-venus.svg` stays yellow because it is the sun, not a category.

The three colours differ in lightness as well as in hue: L* 48, 34 and 78 in
light mode. So they stay apart in greyscale and for colour-blind readers.

SVGs take their colours from the CSS tokens (`style="stroke: var(--st-c1)"`),
so they follow the light and dark themes. PNGs cannot, so they are drawn for a
white page.

### Rules

These come from four sources, listed at the end, and they agree with each
other.

- **Grey first, colour for meaning.** Draw context in grey and give colour
  only to what the reader should look at. One highlight colour is often
  enough.
- **Few colours.** At most about seven categories in one figure, better three
  or four. With more, group categories or split the figure into panels.
- **Same meaning, same colour.** A category keeps its colour in every figure.
  Never reuse a colour for something else.
- **Explain the colours.** Use a legend, or better, label the lines and areas
  directly.
- **Match the palette type to the data.**
  - Qualitative for unordered categories: distinct hues, similar weight.
  - Sequential for ordered values: light means low, dark means high.
  - Diverging for values around a meaningful centre: two clearly different
    hues, with a light grey, not white, in the middle.
  - Cyclic for values that wrap around, such as a phase or a time of day.
- **Lightness carries the information.** The eye picks out patterns by
  lightness more than by hue. A gradient must change steadily in lightness,
  so it still reads in greyscale. Never use a single-hue gradient for
  categories, because it implies an order.
- **No rainbow maps.** Jet, Turbo and other rainbows create bands that are
  not in the data, hide detail and fail in greyscale and for colour-blind
  readers. For continuous data, use perceptually uniform maps:
  - viridis or cividis
  - Crameri's scientific colour maps: batlow (sequential), vik (diverging),
    romaO (cyclic)
- **Never red against green**, and never two colours of similar lightness
  side by side.
- **Contrast scales with size.** Thin lines, small markers and text need high
  contrast with the background: at least 3:1 for marks and 4.5:1 for text.
  Large areas can use muted, desaturated colours. Avoid bright, saturated
  backgrounds.
- **Use colours people already understand.** Warm for excitation or heat,
  cool for inhibition or cold, blue for water, yellow for the sun. Avoid
  pink and blue for gender.
- **Do not rely on colour alone.** Where two series must be told apart, also
  vary the marker shape or the dash, or label them directly.

### Checks before a figure is published

1. Run `python scripts/palette_check.py` for the site palette, or pass new
   colours with `--light` and `--dark`. It prints for each colour:
   - lightness L*, which is what survives in greyscale
   - contrast with the page background
   - the colour distance between every pair, for normal vision and simulated
     protanopia, deuteranopia and tritanopia

   A distance below about 20 means small marks in those two colours look the
   same.
2. Look at the figure in greyscale. Anything that disappears there must also
   be encoded some other way.
3. For anything unusual, view it in a colour-blindness simulator, such as
   the Chromatic Vision Simulator.

### Measurements of the current palette (23 Nov 2026)

The first palette (`#e4572e`, `#2878b5`, `#e9a23b`) failed some of these
checks. Vermilion and amber were only 16 apart for deuteranopes (11 in dark
mode), and vermilion and blue had almost the same lightness (L* 56 against
49). The palette was changed to the values above. `scripts/palette_check.py`
now reports:

| Check | Light | Dark |
|---|---|---|
| L* of vermilion, blue, amber | 48, 34, 78 | 61, 72, 87 |
| Contrast with the page | 4.8, 8.2, 1.8 (edge 4.1) | 5.4, 7.5, 11.9 |
| Smallest distance, normal vision | vermilion–amber 60 | vermilion–amber 55 |
| Smallest distance, deuteranopia | vermilion–amber 32 | vermilion–amber 24 |
| Smallest distance, protanopia | vermilion–amber 49 | vermilion–amber 35 |
| Smallest distance, tritanopia | vermilion–amber 56 | vermilion–amber 59 |

What still needs care:

- **Vermilion against amber is still the closest pair** for colour-blind
  readers, at 24 in dark mode. Where those two must be told apart, also vary
  the marker or the dash, or label them directly.
- **Amber on white is 1.8:1.** In light mode, every amber mark is filled
  with `--st-c3` and outlined with `--st-c3-edge` (`AMBER_EDGE` in the
  scripts). Never draw a thin amber line alone on a white page.
- **Changing a colour means changing it everywhere at once:** the tokens in
  `site.css`, the constants at the top of every script in `scripts/`, the
  defaults in `palette_check.py`, this file, and every regenerated figure.

### Tools

- **ColorBrewer:** tested sequential, diverging and qualitative palettes,
  with a colour-blind-safe filter.
- **Colorgorical:** generates qualitative palettes with a chosen perceptual
  distance.
- **Paletton:** colour harmony.
- **ColorMoves:** tunes a colour map interactively on your own data.
- **Crameri's scientific colour maps** and matplotlib's viridis and cividis,
  for continuous data.
- **Chromatic Vision Simulator:** previews an image as colour-blind readers
  see it.
- **The W3Schools colour picker:** gives the HEX, RGB and HSL values of a
  colour, its lighter and darker shades, and whether black or white text
  reads better on it.

### Sources

- Lisa Charlotte Muth, Datawrapper blog, 2018, on choosing colours for data
  visualisation: <https://www.datawrapper.de/blog/colors>
- J. Somborski, C. Dias Santos Jr. and L. P. Coelho, "True Colors: palettes
  are also important for scientists", Big Data Biology Lab blog, 30 Nov 2022:
  <https://www.big-data-biology.org/blog/2022/11/30/true_colors/>
- S. Zeller and D. Rogers, "Visualizing science: how color determines what we
  see", Eos, 21 May 2020:
  <https://eos.org/features/visualizing-science-how-color-determines-what-we-see>
- W3Schools HTML colour picker:
  <https://www.w3schools.com/colors/colors_picker.asp>
