---
title: MAT-209 Rank & Nullity Calculator
emoji: 📐
colorFrom: yellow
colorTo: green
sdk: gradio
sdk_version: 6.30.0
app_file: app.py
pinned: false
license: mit
---

# MAT-209: Interactive Rank & Nullity Calculator

An interactive, educational linear algebra workstation built with Gradio and SymPy for visualizing matrix rank, nullity, step-by-step Gaussian elimination derivation, and the Rank-Nullity Theorem.

**Author:** Suppakorn Krabtong (Tae)

## Features
- **Dark Analytical Theme:** Custom CSS styling with high-contrast mathematical typography and responsive bracket containers.
- **Strict Semantic Color Coding:**
  - 🟡 **Gold:** Pivot elements ($1$) and pivot columns.
  - 🔴 **Red:** Entirely zeroed-out rows ($0 = 0$, linear dependence).
  - 🔵 **Blue:** Free variables ($x_j$) contributing to matrix nullity.
  - 🟢 **Green:** Formally validated Rank-Nullity Theorem proof.
- **Interactive Grid & Dynamic Resizing:** Resizes matrix dimensions dynamically from $1 \times 1$ up to $10 \times 10$ with quick shortcuts ($2 \times 2$, $3 \times 3$, $4 \times 4$).
- **MATLAB-Style Matrix Input:** Paste and load matrices in native MATLAB format (e.g. `[1, 2, 3; 2, 3, 1; 2, 1, 1]`) with instant auto-resizing.
- **Dynamic Cell States & Clear:** Unfilled cells display dashed borders, filled cells display solid background, and a one-click Clear Matrix button resets the grid.
- **Grid Keyboard Navigation:** Navigate between matrix cells using arrow keys (Up, Down, Left, Right) and Tab.
- **Preset Toolbar:** Quick presets for Identity ($I_n$), Zero ($0_{m \times n}$), Randomized Integers, and Guaranteed Singular matrices.
- **Custom Gauss-Jordan Elimination Engine:** Records and formats every elementary row operation ($R_i \leftrightarrow R_j$, $R_i \leftarrow c R_i$, $R_k \leftarrow R_k - c R_i$) in strict LaTeX.
- **Exact Rational Arithmetic:** Computations carried out symbolically with SymPy fractions (e.g. $\frac{1}{3}$, $-\frac{5}{2}$), eliminating floating-point round-off errors.
- **4-Step Analytical Pipeline:** Progressive tab navigation structuring the complete linear algebra workflow: (1) RREF Visual Map, (2) Step-by-Step Derivation, (3) Rank-Nullity Theorem, and (4) Fundamental Subspaces.
- **Hero Rank & Nullity Scorecards:** Massive, high-contrast KPI cards showcasing $\operatorname{Rank}(A)$ and $\operatorname{Nullity}(A)$ with live percentage totals, subspace dimension badges, and the Rank-Nullity Theorem balance bar.
- **Column Classification & Routing Flow:** Step-by-step visual mapping tracking each column $c_j$ into either Rank (pivot / independent generator) or Nullity (free variable / linearly dependent).
- **In-Matrix RREF Column Annotations:** Directly aligns column labels ($c_j$) and direction indicators (`↑ Pivot (→ Rank)` vs `↑ Free (→ Nullity)`) directly onto the $\operatorname{RREF}(A)$ matrix.
- **Theorem Verification & Subspaces:** Dimension balance bar, determinant transpose invariance ($\det(A) = \det(A^T)$), and basis vectors for Column Space $\operatorname{Col}(A)$ and Null Space $\operatorname{Null}(A)$.

## Author
- **Suppakorn Krabtong (Tae)**
