"""
================================================================================
engine.py - Exact SymPy Rational Mathematical Engine
================================================================================
Implements exact rational arithmetic and Gaussian elimination for MAT-209:
- parse_entry: Converts string, decimal, or fraction input into sympy.Rational.
- custom_gauss_jordan: Step-by-step Gauss-Jordan elimination tracking operations,
                       goals, and focus positions.
- format_bmatrix_latex: Clean KaTeX bmatrix generator with strict color tagging.
- format_step_matrix: Highlights the active row/entry in each elimination step.
- compute_subspaces: Bases for Col(A) and Null(A) in exact fractional vectors.
================================================================================
"""

import sympy as sp


def validate_matrix_filled(mat_grid):
    """
    Strictly verifies that every cell in the m x n grid is populated.
    Raises ValueError immediately if any cell is empty or None.
    """
    if not mat_grid:
        raise ValueError("Matrix has no rows.")
    for i, row in enumerate(mat_grid):
        for j, val in enumerate(row):
            if val is None or str(val).strip() == "":
                raise ValueError(f"Cell at Row {i + 1}, Column {j + 1} is empty. Please fill in all matrix values.")


def parse_entry(val):
    """
    Parses any raw user input into an exact SymPy Rational number.
    Accepts integers, fractions ('3/4', '-5/2'), decimals ('0.75').
    Raises ValueError on empty or invalid inputs. Never returns floating-point approximations.
    """
    if val is None:
        raise ValueError("Empty cell encountered. Please fill in all matrix values.")

    val_str = str(val).strip()
    if not val_str:
        raise ValueError("Empty cell encountered. Please fill in all matrix values.")

    if isinstance(val, (int, sp.Integer)):
        return sp.Rational(val, 1)

    if isinstance(val, float):
        return sp.nsimplify(val, rational=True)

    # Handle standard fraction notation (e.g., '1/3', '-5/2')
    if "/" in val_str:
        parts = val_str.split("/")
        if len(parts) == 2:
            try:
                num = int(parts[0].strip())
                denom = int(parts[1].strip())
                if denom == 0:
                    raise ValueError("Denominator in fraction cannot be zero.")
                return sp.Rational(num, denom)
            except ValueError as e:
                if "Denominator" in str(e):
                    raise
                pass

    # Handle decimal string notation or integers
    try:
        if "." in val_str:
            return sp.nsimplify(float(val_str), rational=True)
        return sp.Rational(int(val_str), 1)
    except Exception:
        pass

    # Safe SymPy fallback evaluation
    try:
        parsed = sp.sympify(val_str)
        if parsed.is_number:
            return sp.nsimplify(parsed, rational=True)
    except Exception:
        pass

    raise ValueError(f"Invalid entry: '{val_str}'. Please input an integer or exact fraction (e.g. 1/3, -5/2).")


def format_entry_coord(r, c):
    """
    Formats 0-indexed matrix coordinates into mathematical LaTeX notation:
    e.g., (0, 0) -> "a_{11}", (1, 0) -> "a_{21}", (9, 9) -> "a_{10,10}".
    """
    r_idx, c_idx = r + 1, c + 1
    if r_idx < 10 and c_idx < 10:
        return f"a_{{{r_idx}{c_idx}}}"
    return f"a_{{{r_idx},{c_idx}}}"


def format_bmatrix_latex(mat, pivot_positions=None, zero_rows=None, free_cols=None):
    """
    Renders a SymPy Matrix in clean LaTeX \\begin{bmatrix} format with strict KaTeX color syntax:
      - Gold (#F59E0B): Leading pivot entries (1s)
      - Red  (#EF4444): Zeroed-out rows indicating linear dependence
      - Blue (#3B82F6): Non-pivot / free variable entries
      - Exact rational numbers (fractions) preserved without decimal approximation.
    """
    rows = mat.rows
    cols = mat.cols
    pivot_pos_set = set(pivot_positions) if pivot_positions else set()
    zero_row_set = set(zero_rows) if zero_rows else set()
    free_col_set = set(free_cols) if free_cols else set()

    latex_rows = []
    for r in range(rows):
        row_entries = []
        is_zero_row = (r in zero_row_set)
        for c in range(cols):
            val = mat[r, c]
            val_latex = sp.latex(val)

            if is_zero_row:
                row_entries.append(f"{{\\color{{#EF4444}} {val_latex}}}")
            elif (r, c) in pivot_pos_set:
                row_entries.append(f"{{\\color{{#F59E0B}} \\mathbf{{{val_latex}}}}}")
            elif c in free_col_set and val != 0:
                row_entries.append(f"{{\\color{{#3B82F6}} {val_latex}}}")
            else:
                row_entries.append(val_latex)
        latex_rows.append(" & ".join(row_entries))

    return "\\begin{bmatrix} " + " \\\\ ".join(latex_rows) + " \\end{bmatrix}"


def format_step_matrix(mat, step_info):
    """
    Highlights the specific focus row and position targeted in an intermediate step:
      - Scale: Leading 1 highlighted in bold Gold (#F59E0B), scaled row in Amber (#FBBF24).
      - Replacement: Cleared 0 highlighted in bold Cyan (#38BDF8), modified row in Purple (#C084FC).
      - Swap: Swapped rows highlighted in Amber (#F59E0B).
    """
    rows = mat.rows
    cols = mat.cols
    stype = step_info.get("type")
    f_row = step_info.get("focus_row")
    f_col = step_info.get("focus_col")
    s_row = step_info.get("swap_row")

    latex_rows = []
    for r in range(rows):
        entries = []
        for c in range(cols):
            v = mat[r, c]
            vl = sp.latex(v)

            if stype == "scale" and r == f_row:
                if c == f_col:
                    entries.append(f"{{\\color{{#F59E0B}} \\mathbf{{{vl}}}}}")
                else:
                    entries.append(f"{{\\color{{#FBBF24}} {vl}}}")
            elif stype == "replacement" and r == f_row:
                if c == f_col:
                    entries.append(f"{{\\color{{#38BDF8}} \\mathbf{{{vl}}}}}")
                else:
                    entries.append(f"{{\\color{{#C084FC}} {vl}}}")
            elif stype == "swap" and (r == f_row or r == s_row):
                entries.append(f"{{\\color{{#F59E0B}} {vl}}}")
            else:
                entries.append(vl)
        latex_rows.append(" & ".join(entries))

    return "\\begin{bmatrix} " + " \\\\ ".join(latex_rows) + " \\end{bmatrix}"


def custom_gauss_jordan(mat_grid):
    """
    Executes custom step-by-step Gauss-Jordan elimination on a 2D matrix using SymPy.
    Strictly records every elementary row operation along with explicit pedagogical goals
    and target coordinates for visual highlighting.
    """
    validate_matrix_filled(mat_grid)

    m = len(mat_grid)
    n = len(mat_grid[0])
    if n == 0:
        raise ValueError("Matrix has no columns.")

    A_orig = sp.Matrix([[parse_entry(mat_grid[i][j]) for j in range(n)] for i in range(m)])
    A = A_orig.copy()

    steps = []
    # Step 0: Record initial matrix state
    steps.append({
        "type": "initial",
        "title": "Initial Input Matrix",
        "op_latex": r"\text{Initial Matrix } A",
        "matrix": A.copy(),
        "desc": f"Input matrix dimensions: ${m} \\times {n}$ (Codomain $\\mathbb{{R}}^{{{m}}}$, Domain $\\mathbb{{R}}^{{{n}}}$).",
        "goal": "Inspect starting matrix and scan Column 1 for first pivot candidate.",
        "focus_label": "Starting Matrix",
        "focus_row": None,
        "focus_col": None,
        "swap_row": None
    })

    pivot_row = 0
    pivot_positions = []

    # Iterate column by column across the matrix
    for c in range(n):
        if pivot_row >= m:
            break

        # Search for pivot candidate in rows >= pivot_row
        cand = None
        for r in range(pivot_row, m):
            if A[r, c] == 1:
                cand = r
                break
        if cand is None:
            for r in range(pivot_row, m):
                if A[r, c] == -1:
                    cand = r
                    break
        if cand is None:
            for r in range(pivot_row, m):
                if A[r, c] != 0:
                    cand = r
                    break

        if cand is None:
            continue

        # 1. Elementary Operation: Row Swap (R_pivot <-> R_cand)
        if cand != pivot_row:
            A.row_swap(pivot_row, cand)
            op = f"R_{{{pivot_row+1}}} \\leftrightarrow R_{{{cand+1}}}"
            p_entry = format_entry_coord(pivot_row, c)
            steps.append({
                "type": "swap",
                "title": "Row Swap",
                "op_latex": op,
                "matrix": A.copy(),
                "desc": f"Interchange rows $R_{{{pivot_row+1}}}$ and $R_{{{cand+1}}}$ to position non-zero pivot at ${p_entry}$.",
                "goal": f"Swap $R_{{{pivot_row+1}}} \\leftrightarrow R_{{{cand+1}}}$ to place non-zero pivot at ${p_entry}$.",
                "focus_label": f"Swap $R_{{{pivot_row+1}}} \\leftrightarrow R_{{{cand+1}}}$",
                "focus_row": pivot_row,
                "focus_col": c,
                "swap_row": cand
            })

        # 2. Elementary Operation: Row Scaling (Normalize pivot to 1)
        p = A[pivot_row, c]
        if p != 1:
            inv_p = sp.Rational(1, p)
            A[pivot_row, :] = A[pivot_row, :] * inv_p

            if inv_p == -1:
                op = f"R_{{{pivot_row+1}}} \\leftarrow -R_{{{pivot_row+1}}}"
            elif inv_p.q != 1:
                if inv_p > 0:
                    op = f"R_{{{pivot_row+1}}} \\leftarrow \\left(\\frac{{{inv_p.p}}}{{{inv_p.q}}}\\right) R_{{{pivot_row+1}}}"
                else:
                    op = f"R_{{{pivot_row+1}}} \\leftarrow \\left(-\\frac{{{-inv_p.p}}}{{{inv_p.q}}}\\right) R_{{{pivot_row+1}}}"
            else:
                op = f"R_{{{pivot_row+1}}} \\leftarrow {inv_p} R_{{{pivot_row+1}}}"

            p_entry = format_entry_coord(pivot_row, c)
            steps.append({
                "type": "scale",
                "title": "Row Scaling",
                "op_latex": op,
                "matrix": A.copy(),
                "desc": f"Multiply row $R_{{{pivot_row+1}}}$ by scalar ${sp.latex(inv_p)}$ to make leading pivot ${p_entry} = 1$.",
                "goal": f"Normalize pivot entry ${p_entry} \\to 1$.",
                "focus_label": f"Pivot ${p_entry}$",
                "focus_row": pivot_row,
                "focus_col": c,
                "swap_row": None
            })

        # 3. Elementary Operation: Row Replacement (Clear column c in all other rows)
        for r in range(m):
            if r != pivot_row and A[r, c] != 0:
                factor = A[r, c]
                A[r, :] = A[r, :] - factor * A[pivot_row, :]

                # Build LaTeX notation with proper signs
                if factor == 1:
                    op = f"R_{{{r+1}}} \\leftarrow R_{{{r+1}}} - R_{{{pivot_row+1}}}"
                elif factor == -1:
                    op = f"R_{{{r+1}}} \\leftarrow R_{{{r+1}}} + R_{{{pivot_row+1}}}"
                elif factor > 0:
                    op = f"R_{{{r+1}}} \\leftarrow R_{{{r+1}}} - {sp.latex(factor)} R_{{{pivot_row+1}}}"
                else:
                    op = f"R_{{{r+1}}} \\leftarrow R_{{{r+1}}} + {sp.latex(-factor)} R_{{{pivot_row+1}}}"

                e_entry = format_entry_coord(r, c)
                steps.append({
                    "type": "replacement",
                    "title": "Row Replacement",
                    "op_latex": op,
                    "matrix": A.copy(),
                    "desc": f"Eliminate entry ${e_entry}$ using pivot row $R_{{{pivot_row+1}}}$.",
                    "goal": f"Eliminate entry ${e_entry} \\to 0$ in pivot column.",
                    "focus_label": f"Clear ${e_entry}$",
                    "focus_row": r,
                    "focus_col": c,
                    "swap_row": None
                })

        pivot_positions.append((pivot_row, c))
        pivot_row += 1

    pivot_cols = [c for (_, c) in pivot_positions]
    free_cols = [c for c in range(n) if c not in pivot_cols]

    # Detect entirely zeroed-out rows (linear dependence)
    zero_rows = []
    for r in range(m):
        if all(A[r, c] == 0 for c in range(n)):
            zero_rows.append(r)

    rank = len(pivot_cols)
    nullity = n - rank

    return {
        "orig": A_orig,
        "rref": A,
        "steps": steps,
        "pivot_positions": pivot_positions,
        "pivot_cols": pivot_cols,
        "free_cols": free_cols,
        "zero_rows": zero_rows,
        "rank": rank,
        "nullity": nullity,
        "m": m,
        "n": n
    }


def compute_subspaces(orig_mat, pivot_cols):
    """
    Extracts the exact rational basis vectors for Col(A) and Null(A).
    """
    col_basis = [orig_mat[:, c] for c in pivot_cols]
    null_basis = orig_mat.nullspace()
    return col_basis, null_basis
