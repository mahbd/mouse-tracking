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
  sections/02-background-and-related-work/index.md
  sections/03-data-and-feature-engineering/index.md
  sections/04-methodology/index.md
  sections/05-system-implementation/index.md
  sections/06-experiments-and-results/index.md
  sections/07-discussion-and-future-work/index.md
  sections/08-conclusion/index.md
)

# Choose engine - xelatex provides better font support
engine=${PANDOC_LATEX_ENGINE:-xelatex}

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Pandoc not found. Install pandoc to build the thesis." >&2
  exit 1
fi

# Common pandoc arguments optimized for 50-page thesis
common_args=(
  -s
  -V documentclass=article
  -V geometry:margin=0.6in
  -V fontsize=11pt
  -V linestretch=1.1
  -V papersize=a4
  -V toc-title="TABLE OF CONTENTS"
  --toc
  --toc-depth=2
  --number-sections
  --citeproc
  --resource-path=.
  --bibliography=references.bib
  "${sections[@]}"
)

case "$ext" in
  pdf)
    echo "Building compact thesis PDF with pandoc..."
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
echo "Thesis optimized for ~50 pages with compact formatting."
