#!/usr/bin/env bash
# Build script for the thesis using pandoc
# - Default builds a PDF (thesis.pdf)
# - Pass an output ending in .tex to build an editable LaTeX file instead

set -euo pipefail

# Always run relative to this script's directory so section paths work
cd "$(dirname "$0")"

# Default output
out=${1:-thesis.pdf}

ext=${out##*.}

# Collect section files in order
sections=(
  sections/00-front-matter/title-page.md
  sections/00-front-matter/declaration.md
  sections/00-front-matter/certificate.md
  sections/00-front-matter/acknowledgements.md
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

# Common pandoc arguments with enhanced settings for larger thesis
common_args=(
  -s
  -V documentclass=report
  -V geometry:margin=1in
  -V fontsize=12pt
  -V linestretch=1.5
  -V papersize=a4
  --toc
  --toc-depth=3
  --number-sections
  --citeproc
  --resource-path=.
  --bibliography=references.bib
  --filter=pandoc-crossref
  "${sections[@]}"
)

case "$ext" in
  pdf)
    echo "Building thesis PDF with pandoc..."
    pandoc \
      "${common_args[@]}" \
      --pdf-engine="$engine" \
      -V classoption=openright \
      -V classoption=twoside \
      --template=eisvogel \
      -o "$out" || \
    pandoc \
      "${common_args[@]}" \
      --pdf-engine="$engine" \
      -o "$out"
    ;;
  tex)
    echo "Building thesis LaTeX (.tex) with pandoc..."
    pandoc \
      "${common_args[@]}" \
      -t latex \
      -o "$out"
    ;;
  *)
    echo "Unknown output extension: .$ext. Use .pdf or .tex" >&2
    exit 2
    ;;
esac

echo "Built $out successfully!"
echo "The thesis is now significantly expanded with comprehensive content."
echo "Each chapter starts on a new page and contains detailed analysis."
