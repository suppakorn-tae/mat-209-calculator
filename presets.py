"""
================================================================================
presets.py - Matrix Presets & Grid Resizing Utilities
================================================================================
Provides matrix generators for quick student exploration:
- Identity Matrix (I_n)
- Zero Matrix (0_{m x n})
- Randomized Integer Matrix
- Guaranteed Singular Matrix (guaranteed linear dependence among rows)
- Matrix resizing while preserving existing cell values
================================================================================
"""

import random
import re
from engine import parse_entry


def parse_matlab_matrix(text: str):
    """
    Parses a MATLAB-formatted matrix string into a 2D list of strings, plus dimensions (m, n).
    Supports MATLAB syntax, e.g.:
      [1, 2, 3; 2, 3, 1; 2, 1, 1]
      [1 2 3; 2 3 1; 2 1 1]
      1, 2, 3; 4, 5, 6
      Fractions (e.g. 1/2, -3/4), decimals (0.5), and multiline input.
    """
    if not text or not text.strip():
        raise ValueError("Matrix input is empty. Please enter MATLAB matrix syntax like [1, 2, 3; 2, 3, 1; 2, 1, 1].")

    s = text.strip()
    # Strip brackets if present
    s = s.replace("[", "").replace("]", "").strip()
    if not s:
        raise ValueError("Matrix body is empty.")

    # Normalize newlines to semicolons
    s = s.replace("\n", ";").replace("\r", "")
    raw_rows = s.split(";")

    grid = []
    for raw_r in raw_rows:
        cleaned_r = raw_r.strip()
        if not cleaned_r:
            continue
        # Split row entries by comma or whitespace
        tokens = re.sub(r"[,]+", " ", cleaned_r).strip().split()
        if tokens:
            for tok in tokens:
                parse_entry(tok)  # Raises ValueError if token is invalid
            grid.append(tokens)

    if not grid:
        raise ValueError("No matrix entries found.")

    m = len(grid)
    n = len(grid[0])
    for i, r in enumerate(grid):
        if len(r) != n:
            raise ValueError(f"Inconsistent column count: Row 1 has {n} columns, but Row {i+1} has {len(r)}.")

    if m < 1 or n < 1:
        raise ValueError("Matrix dimensions must be at least 1×1.")
    if m > 10 or n > 10:
        raise ValueError(f"Matrix dimensions ({m}×{n}) exceed maximum 10×10 limit.")

    return grid, m, n


def resize_matrix(rows, cols, current_matrix):
    """
    Resizes a 2D matrix grid to (rows x cols) while preserving existing entries
    where possible, padding newly created cells with strictly empty string "" (unfilled dashed box).
    """
    rows = max(1, min(10, int(rows)))
    cols = max(1, min(10, int(cols)))
    raw_data = current_matrix or []

    new_data = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if r < len(raw_data) and c < len(raw_data[r]):
                val = raw_data[r][c]
                val_str = str(val).strip() if val is not None else ""
                row.append(val_str)
            else:
                row.append("")
        new_data.append(row)
    return new_data


def generate_identity(rows, cols):
    """
    Generates an m x n matrix with 1s on the main diagonal and 0s elsewhere.
    """
    rows, cols = int(rows), int(cols)
    return [["1" if r == c else "0" for c in range(cols)] for r in range(rows)]


def generate_zero(rows, cols):
    """
    Generates an m x n all-zero matrix.
    """
    rows, cols = int(rows), int(cols)
    return [["0" for _ in range(cols)] for _ in range(rows)]


def generate_random(rows, cols):
    """
    Generates an m x n matrix populated with randomized integers between -4 and 7.
    """
    rows, cols = int(rows), int(cols)
    return [[str(random.randint(-4, 7)) for _ in range(cols)] for _ in range(rows)]


def generate_singular(rows, cols):
    """
    Generates an m x n matrix guaranteed to possess linearly dependent rows.
    For m >= 2, forces at least one row to be an exact linear combination of others.
    """
    rows, cols = int(rows), int(cols)
    if rows == 1:
        return [["0" for _ in range(cols)]]

    # Generate random base rows
    mat = [[random.randint(-3, 4) for _ in range(cols)] for _ in range(rows)]

    # Ensure Row 0 has at least one non-zero component
    if all(x == 0 for x in mat[0]):
        mat[0][0] = 1

    if rows == 2:
        # Row 1 is an integer multiple of Row 0
        scalar = random.choice([-2, 2, 3])
        mat[1] = [scalar * x for x in mat[0]]
    else:
        # Last row is the explicit sum of Row 0 and Row 1
        mat[-1] = [mat[0][c] + mat[1][c] for c in range(cols)]

    return [[str(x) for x in row] for row in mat]


def generate_symmetric(rows, cols):
    """
    Generates a symmetric matrix where A = A^T (a_ij = a_ji),
    demonstrating Transpose Invariance det(A) = det(A^T) and orthogonal eigenspaces.
    """
    rows, cols = int(rows), int(cols)
    mat = [["0" for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if r <= c:
                val = str(random.randint(-3, 6))
                mat[r][c] = val
                if c < rows and r < cols:
                    mat[c][r] = val
    return mat


def generate_triangular(rows, cols):
    """
    Generates an upper triangular matrix (entries below main diagonal are 0),
    demonstrating det(A) = det(A^T) = product of main diagonal entries.
    """
    rows, cols = int(rows), int(cols)
    mat = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if r > c:
                row.append("0")
            elif r == c:
                row.append(str(random.choice([-2, -1, 1, 2, 3])))
            else:
                row.append(str(random.randint(-3, 5)))
        mat.append(row)
    return mat


PRESET_DESCRIPTIONS = {
    "identity": (
        "🟢 **Identity Matrix ($I_n$)** • Full Rank ($\\operatorname{Rank} = n$, $\\operatorname{Nullity} = 0$) • "
        "$\\det(I) = \\det(I^T) = 1$. All columns are pivot columns; null space is trivial $\\{\\mathbf{0}\\}$."
    ),
    "singular": (
        "🔴 **Singular Matrix ($\\det(A) = 0$)** • Linearly Dependent Rows ($R_m = R_1 + R_2$) • "
        "Demonstrates $\\det(A) = \\det(A^T) = 0$, non-invertibility, $\\operatorname{Rank}(A) < n$, and non-trivial null space ($\\operatorname{Nullity}(A) \\ge 1$)."
    ),
    "symmetric": (
        "🔵 **Symmetric Matrix ($A = A^T$)** • Transpose Invariant • "
        "Demonstrates $\\det(A) = \\det(A^T)$, identical row and column spaces, all real eigenvalues, and orthogonal eigenspaces."
    ),
    "triangular": (
        "📐 **Upper Triangular Matrix** • Entries below diagonal are $0$ • "
        "Demonstrates that pivots sit on the diagonal and $\\det(A) = \\det(A^T) = \\prod_{i=1}^n a_{ii}$ directly from diagonal entries."
    ),
    "zero": (
        "⚪ **Zero Matrix ($0_{m \\times n}$)** • Complete Degeneracy • "
        "$\\det(0) = 0$, $\\operatorname{Rank}(0) = 0$, and null space spans the entire domain $\\mathbb{R}^n$ ($\\operatorname{Nullity} = n$)."
    ),
    "random": (
        "🎲 **Random Integer Matrix** • General Testing • "
        "Arbitrary integer entries for verifying Gaussian elimination and the Rank-Nullity Theorem $\\operatorname{Rank}(A) + \\operatorname{Nullity}(A) = n$."
    )
}

