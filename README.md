---
title: MAT-209 Rank & Nullity Calculator
emoji: 📐
colorFrom: yellow
colorTo: green
sdk: gradio
sdk_version: 6.30.0
app_file: app.py
pinned: false
license: cc-by-nc-4.0
---

# MAT-209: Interactive Rank & Nullity Calculator

An interactive, educational linear algebra workstation built with Gradio and SymPy for visualizing matrix rank, nullity, step-by-step Gaussian elimination derivation, and the Rank-Nullity Theorem.

## Features
- **Dark Analytical Theme:** Custom CSS styling with high-contrast mathematical typography, transparent math row container, and responsive single dynamic bracket notation ($A = [ \dots ]$).
- **Strict Semantic Color Coding:**
  - 🟡 **Gold:** Pivot elements ($1$) and pivot columns contributing to Rank.
  - 🔴 **Red:** Linearly dependent zero rows ($0 = 0$).
  - 🔵 **Blue:** Free variables ($x_j$) contributing to Nullity.
  - 🟢 **Green:** Formally validated Rank-Nullity Theorem result.
- **Top Hero KPI Scorecards:** Prominent side-by-side KPI cards placed permanently above the step tabs, displaying $\text{Rank}(A)$ (Gold) and $\text{Nullity}(A)$ (Blue) with column percentages, basis/kernel dimensions, and clean UI typography.
- **Horizontally Scrollable 4-Step Pipeline:** Tabs structured as a guided step-by-step pipeline with hidden scrollbars, responsive peeking (viewing Step 1 shows Step 2 and peeks Step 3), and mouse wheel / drag scrolling:
  1. 🎯 **RREF Visual Map:** Visual $\text{RREF}(A)$ matrix with in-matrix column annotations and interactive Column Classification & Routing Flow diagram showing where each column goes ($\text{Col } j \to \text{Rank}$ or $\text{Col } j \to \text{Nullity}$).
  2. 🪜 **Step-by-Step Derivation:** Step-by-step Gauss-Jordan timeline tracking every elementary row operation ($R_i \leftrightarrow R_j$, $R_i \leftarrow c R_i$, $R_k \leftarrow R_k - c R_i$) with intermediate matrices, goals, and highlighted focus targets.
  3. ⚖️ **Rank-Nullity Theorem:** Dynamic Identity Proof card ($\text{Rank}(A) + \text{Nullity}(A) = n$), animated horizontal dimension balance bar, variable breakdown, and determinant transpose invariance ($\text{det}(A) = \text{det}(A^T)$).
  4. 📐 **Fundamental Subspaces:** Formal basis vectors and dimensions for Column Space $\text{Col}(A) \subseteq \mathbb{R}^m$ and Null Space $\text{Null}(A) \subseteq \mathbb{R}^n$.
- **Interactive Grid & Dynamic Resizing:** Resizes matrix dimensions dynamically from $1 \times 1$ up to $10 \times 10$ with quick shortcuts ($2 \times 2$, $3 \times 3$, $4 \times 4$).
- **MATLAB-Style Matrix Input:** Collapsible input supporting native MATLAB syntax (e.g. `[1, 2, 3; 2, 3, 1; 2, 1, 1]`) with instant auto-parsing and grid population.
- **Dynamic Cell States & Clear:** Empty cells render dashed borders, filled cells render solid background, and a one-click Clear Matrix button resets all inputs.
- **Keyboard Grid Navigation:** Seamless arrow key navigation (Up, Down, Left, Right) across matrix inputs with boundary checks and first-click typing focus.
- **Preset Toolbar:** Quick presets for Identity ($I_n$), Zero ($0_{m \times n}$), Randomized Integers, and Guaranteed Singular matrices ($\text{det}(A) = 0$).
- **Exact Rational Arithmetic:** All computations evaluated symbolically with SymPy fractions (e.g. $\frac{1}{3}$, $-\frac{5}{2}$), eliminating floating-point rounding errors.

## Author
Suppakorn Krabtong (Tae)

## License
Educational and Non-Commercial Use Only. Commercial use prohibited without express written permission. See [LICENSE](LICENSE).
