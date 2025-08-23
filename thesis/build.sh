#!/usr/bin/env zsh
# Build the thesis PDF using pandoc (requires pandoc and a LaTeX engine installed).
# Activates conda env if available.

set -euo pipefail

# Default output
out=${1:-thesis.pdf}

# Collect section files in order
sections=(
  sections/00-abstract/index.md
  sections/01-introduction/index.md
  sections/01-introduction/motivation-and-scope.md
  sections/01-introduction/contributions-and-outline.md
  sections/02-background-and-related-work/index.md
  sections/02-background-and-related-work/behavioral-biometrics-survey.md
  sections/02-background-and-related-work/mouse-dynamics-literature.md
  sections/03-data-and-feature-engineering/index.md
  sections/03-data-and-feature-engineering/segmentation-and-windows.md
  sections/03-data-and-feature-engineering/feature-definitions.md
  sections/04-methodology/index.md
  sections/04-methodology/algorithms-and-hyperparameters.md
  sections/04-methodology/evaluation-and-metrics.md
  sections/05-system-implementation/index.md
  sections/05-system-implementation/collectors.md
  sections/05-system-implementation/preprocessing-and-features.md
  sections/06-experiments-and-results/index.md
  sections/06-experiments-and-results/classification-details.md
  sections/06-experiments-and-results/anomaly-detection-details.md
  sections/06-experiments-and-results/tables-and-figures.md
  sections/07-discussion-and-future-work/index.md
  sections/07-discussion-and-future-work/limitations.md
  sections/07-discussion-and-future-work/ethics-and-privacy.md
  sections/08-conclusion/index.md
  appendices/A-dataset-details.md
  appendices/B-reproducibility.md
  appendices/C-ethics-and-privacy.md
)

# Choose engine - xelatex provides better font support
engine=${PANDOC_LATEX_ENGINE:-xelatex}

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Pandoc not found. Install pandoc to build the thesis." >&2
  exit 1
fi

pandoc \
  -V geometry:margin=1in \
  -V fontsize=12pt \
  -V linestretch=1.3 \
  --toc \
  --filter pandoc-citeproc 2>/dev/null || true \
  --citeproc \
  -o "$out" \
  --pdf-engine="$engine" \
  --resource-path=. \
  --bibliography=references.bib \
  ${sections[@]}

echo "Built $out"
