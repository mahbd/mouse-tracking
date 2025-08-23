# Thesis: Mouse Tracking for Behavioral Biometrics and Anomaly Detection

This thesis documents the research, system design, and evaluation of a mouse-tracking based behavioral biometrics system for user identification and anomaly detection.

Contents are organized by sections in subfolders. Build this into a single document with Pandoc or your editor of choice.

## How to use

- Each section has its own folder with an `index.md` file.
- Tables and result summaries are pre-populated from the repository’s `results/` folder.
- References to two external papers are added as placeholders in `references.bib` (document.pdf and rahman2021.pdf). Update metadata as needed.

## Suggested compilation (optional)

You can concatenate sections in order:

1. sections/01-introduction/index.md
2. sections/02-background-and-related-work/index.md
3. sections/03-data-and-feature-engineering/index.md
4. sections/04-methodology/index.md
5. sections/05-system-implementation/index.md
6. sections/06-experiments-and-results/index.md
7. sections/07-discussion-and-future-work/index.md
8. sections/08-conclusion/index.md
9. appendices/A-dataset-details.md
10. appendices/B-reproducibility.md
11. appendices/C-ethics-and-privacy.md

## Notes

- Page count depends on formatting (margins, font size, line spacing). The current draft is designed to expand beyond 50 A4 pages with typical thesis formatting (11–12pt, 1.5x spacing, 1" margins). Fill in TODOs and refine prose to reach the desired length.

## Build (Pandoc)

Ensure you have Pandoc and a LaTeX engine (xelatex recommended). With your conda env `mtrack` activated:

- Run `./build.sh` to produce `thesis.pdf`, or `make` in this folder.
- Bibliography comes from `references.bib`.
