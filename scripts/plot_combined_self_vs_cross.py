#!/usr/bin/env python3
"""Plot combined self vs mean-cross anomaly rates for SVM and IsolationForest.

Reads the markdown tables in thesis/sections/06-experiments-and-results/*_cross_user_matrix.md
and produces a PNG saved to thesis/figures/combined_self_vs_cross.png
"""
from pathlib import Path
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def parse_md_table(path: Path):
    """Parse a simple markdown pipe table into header and numeric matrix.

    Expects a table like:
    |       |   atiq |   masum |   rakib |   zia |
    |:------|-------:|--------:|--------:|------:|
    | atiq  |   4.99 |    4.16 |    5.26 |  3.6  |
    ...
    """
    lines = path.read_text().splitlines()
    # find lines that look like table rows (start with |)
    table_lines = [ln.strip() for ln in lines if ln.strip().startswith("|")]
    if not table_lines:
        raise ValueError(f"No markdown table found in {path}")

    # header is the first line
    header_cells = [c.strip() for c in table_lines[0].strip().strip('|').split('|')]
    # rows start from the third line (skip separator)
    data_lines = table_lines[2:]
    names = []
    mat = []
    for ln in data_lines:
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if len(cells) < 2:
            continue
        names.append(cells[0])
        # parse remaining as floats, ignore empty
        row = []
        for v in cells[1:1+ (len(header_cells)-1)]:
            # remove possible commas and non-numeric
            vclean = re.sub(r"[^0-9.+-eE]", "", v)
            try:
                row.append(float(vclean))
            except ValueError:
                row.append(np.nan)
        mat.append(row)

    return header_cells[1:], np.array(mat)


def main():
    repo_root = Path(__file__).resolve().parents[1]
    md_dir = repo_root / 'thesis' / 'sections' / '06-experiments-and-results'
    figures_dir = repo_root / 'thesis' / 'figures'
    figures_dir.mkdir(parents=True, exist_ok=True)

    svm_md = md_dir / 'svm_cross_user_matrix.md'
    iso_md = md_dir / 'iso_cross_user_matrix.md'

    users_svm, mat_svm = parse_md_table(svm_md)
    users_iso, mat_iso = parse_md_table(iso_md)

    # prefer users from header
    users = users_svm

    # compute self (diagonal) and mean cross (row mean excluding diagonal)
    def self_and_mean_cross(mat):
        di = np.diag(mat)
        mean_cross = []
        for i in range(mat.shape[0]):
            row = np.array(mat[i, :], dtype=float)
            others = np.delete(row, i)
            mean_cross.append(np.nanmean(others))
        return di, np.array(mean_cross)

    sv_self, sv_cross = self_and_mean_cross(mat_svm)
    iso_self, iso_cross = self_and_mean_cross(mat_iso)

    # Plotting
    sns.set(style='whitegrid')
    x = np.arange(len(users))
    width = 0.20

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(x - 1.5*width, sv_self, width, label='SVM self', color='#4C72B0')
    ax.bar(x - 0.5*width, sv_cross, width, label='SVM mean cross', color='#55A868')
    ax.bar(x + 0.5*width, iso_self, width, label='ISO self', color='#C44E52')
    ax.bar(x + 1.5*width, iso_cross, width, label='ISO mean cross', color='#8172B2')

    ax.set_xticks(x)
    ax.set_xticklabels(users)
    ax.set_ylabel('Anomaly rate (%)')
    ax.set_title('Self vs mean cross anomaly rates — One-Class SVM vs IsolationForest')
    ax.legend(loc='upper right')

    plt.tight_layout()
    out = figures_dir / 'combined_self_vs_cross.png'
    fig.savefig(out, dpi=200)
    print(f'Wrote: {out}')


if __name__ == '__main__':
    main()
