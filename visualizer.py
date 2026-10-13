"""
================================================================================
visualizer.py - Visual Math Diagrams & Intuitive UI Builders
================================================================================
Replaces walls of text with intuitive visual graphics and animations:
- build_dimension_bar: Visual horizontal balance bar displaying Rank + Nullity = n.
- build_rref_card: Visual RREF matrix with column and row status badges.
- build_derivation_timeline: Progressive timeline with step goals, focus targets,
                             and highlighted positions in intermediate matrices.
- build_subspaces_card: Visual subspace cards for Col(A) and Null(A) bases.
================================================================================
"""

import sympy as sp
from engine import format_bmatrix_latex, format_step_matrix


def build_hero_kpi_cards(rank, nullity, n, m, zero_rows, pivot_cols, free_cols, orig_mat=None):
    """
    Constructs the 2 Hero KPI scorecards for Rank(A) and Nullity(A) positioned on top of the tabs.
    Uses clean UI typography without LaTeX.
    """
    rank_pct = round((rank / n) * 100, 1) if n > 0 else 0
    null_pct = round((nullity / n) * 100, 1) if n > 0 else 0

    return f"""<div class="hero-kpi-grid">
<div class="hero-kpi-card hero-rank-card">
  <div class="hero-kpi-header">
    <div class="hero-kpi-badge hero-rank-badge"><span>🟡</span>Rank(A)</div>
    <div class="hero-kpi-pct">{rank_pct}% of {n} cols</div>
  </div>
  <div class="hero-kpi-value hero-rank-value">{rank}</div>
  <div class="hero-kpi-subtitle">Dimension of Column Space / Pivot Columns</div>
  <div class="hero-kpi-footer">
    <span>dim Col(A) = {rank}</span>
    <span>{len(pivot_cols)} Leading 1{"s" if len(pivot_cols) != 1 else ""}</span>
  </div>
</div>

<div class="hero-kpi-card hero-nullity-card">
  <div class="hero-kpi-header">
    <div class="hero-kpi-badge hero-nullity-badge"><span>🔵</span>Nullity(A)</div>
    <div class="hero-kpi-pct">{null_pct}% of {n} cols</div>
  </div>
  <div class="hero-kpi-value hero-nullity-value">{nullity}</div>
  <div class="hero-kpi-subtitle">Dimension of Null Space / Free Columns</div>
  <div class="hero-kpi-footer">
    <span>dim Null(A) = {nullity}</span>
    <span>{len(free_cols)} Free Var{"s" if len(free_cols) != 1 else ""}</span>
  </div>
</div>
</div>"""


def build_dimension_bar(rank, nullity, n, m, zero_rows, pivot_cols, free_cols, orig_mat=None):
    """
    Constructs the Step 3 Tab: Rank-Nullity Theorem & Dimension Balance.
    Visualizes the horizontal dimension balance bar, dynamic identity proof,
    and elaborates on determinant and transpose invariance properties.
    """
    rank_pct = round((rank / n) * 100, 1) if n > 0 else 0
    null_pct = round((nullity / n) * 100, 1) if n > 0 else 0

    pivot_badges = "".join([f"<span class='legend-pill legend-gold' style='display:inline-flex; padding:2px 8px; margin:2px;'>$x_{c+1}$</span>" for c in pivot_cols]) or "<span style='color:#94a3b8;'>None</span>"
    free_badges = "".join([f"<span class='legend-pill legend-blue' style='display:inline-flex; padding:2px 8px; margin:2px;'>$x_{c+1}$</span>" for c in free_cols]) or "<span style='color:#94a3b8;'>None (Trivial)</span>"

    zero_row_alert = ""
    if zero_rows:
        rows_str = ", ".join([f"Row {r+1}" for r in zero_rows])
        zero_row_alert = f"""<div style="background: var(--red-bg); border: 1px solid var(--red-border); border-radius: 8px; padding: 10px 14px; margin-top: 12px; display: flex; align-items: center; gap: 10px;">
<span style="font-size: 18px;">🔴</span>
<div style="font-size: 13px; color: var(--red-light);">
<b>Linear Dependence Detected:</b> {rows_str} reduced to all zeroes ($0 = 0$). The original row vectors are <b>linearly dependent</b>.
</div>
</div>"""

    det_section = ""
    if orig_mat is not None:
        if m == n:
            det_val = orig_mat.det()
            det_latex = sp.latex(det_val)
            if det_val == 0:
                det_status = (
                    f"<span style='color: var(--red-light); font-weight: 700;'>🔴 Singular Matrix ($\\det(A) = 0$):</span> "
                    f"Row and column vectors are <b>linearly dependent</b>. "
                    f"$\\operatorname{{Rank}}(A) = {rank} < {n}$, $\\operatorname{{Nullity}}(A) = {nullity} \\ge 1$. "
                    f"By Transpose Determinant Invariance, $\\det(A^T) = \\det(A) = 0$ and $\\operatorname{{Rank}}(A^T) = \\operatorname{{Rank}}(A) = {rank}$."
                )
            else:
                det_status = (
                    f"<span style='color: #34d399; font-weight: 700;'>🟢 Invertible / Full Rank Matrix ($\\det(A) \\ne 0$):</span> "
                    f"Columns and rows are <b>linearly independent</b>. "
                    f"$\\operatorname{{Rank}}(A) = {n}$, $\\operatorname{{Nullity}}(A) = 0$ (Trivial Null Space). "
                    f"By Transpose Determinant Invariance, $\\det(A^T) = \\det(A) = {det_latex} \\ne 0$ and $A^T$ is likewise invertible."
                )
            det_section = f"""<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--card-border); border-radius: 8px; padding: 12px 14px; margin-top: 12px;">
<div style="font-size: 11px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">
Square Matrix ($n = {n}$) • Determinant & Transpose Invariance
</div>
<div style="font-size: 15px; font-weight: 700; margin-bottom: 6px; color: #f8fafc;">
$$\\det(A) = \\det(A^T) = {det_latex}$$
</div>
<div style="font-size: 12.5px; line-height: 1.5; color: #cbd5e1;">
{det_status}
</div>
</div>"""
        else:
            det_section = f"""<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--card-border); border-radius: 8px; padding: 10px 14px; margin-top: 12px; font-size: 12.5px; color: #94a3b8;">
<b>Rectangular Matrix (${m} \\times {n}$):</b> Determinant is defined only for square matrices ($m = n$). However, <b>Transpose Rank Invariance</b> strictly holds: $\\operatorname{{Rank}}(A) = \\operatorname{{Rank}}(A^T) = {rank}$.
</div>"""

    # Unindented HTML prevents markdown-it from treating indented tags as pre/code blocks
    md = f"""### 3. ⚖️ Rank-Nullity Theorem & Dimension Balance

<div class="dim-balance-container">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
<div style="font-size: 15px; font-weight: 800; color: #34d399; display: flex; align-items: center; gap: 8px;">
<span>🟢</span> Rank-Nullity Theorem Formally Verified
</div>
<div style="font-size: 12px; background: #1e293b; border: 1px solid #334155; padding: 4px 10px; border-radius: 6px; color: #94a3b8;">
Domain $\\mathbb{{R}}^{{{n}}}$ $\\longrightarrow$ Codomain $\\mathbb{{R}}^{{{m}}}$
</div>
</div>

<div class="dim-bar-wrapper">
<div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 700; margin-bottom: 6px;">
<span style="color: var(--gold-light);">🟡 $\\operatorname{{Rank}}(A) = {rank}$ ({rank_pct}%)</span>
<span style="color: #10b981; font-weight: 800;">Total Columns $n = {n}$</span>
<span style="color: var(--blue-light);">🔵 $\\operatorname{{Nullity}}(A) = {nullity}$ ({null_pct}%)</span>
</div>
<div class="dim-bar-track">
<div class="dim-bar-rank" style="width: {rank_pct}%;">
{f"{rank}" if rank > 0 else ""}
</div>
<div class="dim-bar-null" style="width: {null_pct}%;">
{f"{nullity}" if nullity > 0 else ""}
</div>
</div>
</div>

<div class="theorem-proof-badge">
<div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #a7f3d0; margin-bottom: 2px;">
Dynamic Identity Proof
</div>
<div style="font-size: 24px; font-weight: 800; color: #34d399;">$$\\mathbf{{\\underbrace{{{rank}}}_{{\\color{{#F59E0B}} \\operatorname{{Rank}}(A)}} + \\underbrace{{{nullity}}}_{{\\color{{#3B82F6}} \\operatorname{{Nullity}}(A)}} = \\underbrace{{{n}}}_{{\\color{{#10B981}} n}} \\quad \\Longrightarrow \\quad {rank} + {nullity} = {n}}}$$</div>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-top: 14px;">
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--card-border); border-radius: 8px; padding: 10px 14px;">
<div style="font-size: 11px; color: var(--gold-light); font-weight: 700; text-transform: uppercase;">Pivot Variables (Rank(A))</div>
<div style="margin-top: 4px;">{pivot_badges}</div>
</div>
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--card-border); border-radius: 8px; padding: 10px 14px;">
<div style="font-size: 11px; color: var(--blue-light); font-weight: 700; text-transform: uppercase;">Free Variables (Nullity(A))</div>
<div style="margin-top: 4px;">{free_badges}</div>
</div>
</div>
{zero_row_alert}
{det_section}
</div>"""
    return md


def build_rref_card(orig_mat, rref_mat, pivot_positions, zero_rows, free_cols, m, n):
    """
    Constructs the Reduced Row Echelon Form card with clean KaTeX syntax,
    in-matrix column header & footer annotations, and the interactive Column Classification & Routing Flow diagram.
    """
    a_latex = format_bmatrix_latex(orig_mat)
    rref_core = format_bmatrix_latex(rref_mat, pivot_positions, zero_rows, free_cols)

    pivot_col_to_row = {c: r for r, c in pivot_positions}
    pivot_cols_set = set(pivot_col_to_row.keys())
    free_cols_set = set(free_cols)

    # 1. RREF Column Header & Footer Annotations (aligned directly above and beneath columns)
    top_labels = []
    # bot_labels = []
    for c in range(n):
        c_num = c + 1
        if c in pivot_cols_set:
            top_labels.append(f"{{\\color{{#F59E0B}} \\mathbf{{c_{{{c_num}}}}}}}")
            # bot_labels.append(f"{{\\color{{#F59E0B}} \\begin{{subarray}}{{c}} \\uparrow\\text{{Pivot}} \\\\[-2pt] \\scriptstyle(\\to\\text{{Rank}}) \\end{{subarray}}}}")
        else:
            top_labels.append(f"{{\\color{{#3B82F6}} \\mathbf{{c_{{{c_num}}}}}}}")
            # bot_labels.append(f"{{\\color{{#3B82F6}} \\begin{{subarray}}{{c}} \\uparrow\\text{{Free}} \\\\[-2pt] \\scriptstyle(\\to\\text{{Nullity}}) \\end{{subarray}}}}")

    top_row_latex = " & ".join(top_labels)
    # bot_row_latex = " & ".join(bot_labels)

#     annotated_rref = f"""\\begin{{array}}{{c}}
# \\begin{{matrix}} {top_row_latex} \\end{{matrix}} \\\\[2pt]
# {rref_core} \\\\[6pt]
# \\begin{{matrix}} {bot_row_latex} \\end{{matrix}}
# \\end{{array}}"""

    annotated_rref = f"""\\begin{{array}}{{c}}
\\begin{{matrix}} {top_row_latex} \\end{{matrix}} \\\\[2pt]
{rref_core} \\\\[6pt]
\\end{{array}}"""

    # 2. Visual Column-by-Column Routing Breakdown ("Where Each Column Goes")
    routing_cards = []
    for c in range(n):
        c_num = c + 1
        if c in pivot_cols_set:
            p_row = pivot_col_to_row[c]
            coord = f"a_{{{p_row + 1}{c_num}}}"
            card_html = f"""<div class="col-route-card route-pivot">
<div class="col-route-col">
  <span class="route-badge-gold">$\\text{{Col }} {c_num} \\; (x_{{{c_num}}})$</span>
</div>
<div class="col-route-arrow">⟶</div>
<div class="col-route-status">
  <span style="color: #fbbf24; font-weight: 700;">Has Pivot (Leading 1)</span>
  <span style="font-size: 11px; color: #94a3b8;">Leading 1 at entry ${coord}$</span>
</div>
<div class="col-route-arrow">⟶</div>
<div class="col-route-dest">
  <span class="dest-badge-gold">Contributes $+1$ to $\\operatorname{{Rank}}(A)$</span>
  <span style="font-size: 11px; color: #cbd5e1;">(Independent Generator)</span>
</div>
</div>"""
        else:
            card_html = f"""<div class="col-route-card route-free">
<div class="col-route-col">
  <span class="route-badge-blue">$\\text{{Col }} {c_num} \\; (x_{{{c_num}}})$</span>
</div>
<div class="col-route-arrow">⟶</div>
<div class="col-route-status">
  <span style="color: #60a5fa; font-weight: 700;">No Pivot (Free Variable)</span>
  <span style="font-size: 11px; color: #94a3b8;">No leading entry in column</span>
</div>
<div class="col-route-arrow">⟶</div>
<div class="col-route-dest">
  <span class="dest-badge-blue">Contributes $+1$ to $\\operatorname{{Nullity}}(A)$</span>
  <span style="font-size: 11px; color: #cbd5e1;">(Redundant / Dependent)</span>
</div>
</div>"""
        routing_cards.append(card_html)

    routing_cards_joined = "\n".join(routing_cards)
    routing_strip_html = f"""<div class="col-routing-container">
<div class="col-routing-header">
  <div style="font-size: 14px; font-weight: 800; color: #f8fafc; display: flex; align-items: center; gap: 8px;">
    <span>🔀</span> Column Classification & Routing Flow ("Where Each Column Goes")
  </div>
  <div style="font-size: 12px; color: #94a3b8;">
    <span style="color: var(--gold-light); font-weight: 700;">{len(pivot_cols_set)} Pivots</span> + <span style="color: var(--blue-light); font-weight: 700;">{len(free_cols_set)} Free</span> = <b style="color: #10b981;">{n} Columns</b>
  </div>
</div>
<div class="col-routing-list">
{routing_cards_joined}
</div>
</div>"""

    md = rf"""### 1. 🎯 Reduced Row Echelon Form (RREF)

<div style="background: #0f172a; border: 1px solid var(--card-border); border-radius: 10px; padding: 20px; text-align: center; margin: 12px 0; overflow-x: auto;">
$$A = {a_latex} \quad \xrightarrow{{\text{{RREF}}}} \quad \operatorname{{RREF}}(A) = {annotated_rref}$$
</div>

<div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-top: 6px; margin-bottom: 12px;">
<span style="font-size: 12px; color: var(--gold-light); font-weight: 700;">🟡 Gold: Pivot 1s (Leading Ones)</span>
<span style="font-size: 12px; color: var(--blue-light); font-weight: 700;">🔵 Blue: Free Column Coefficients</span>
<span style="font-size: 12px; color: var(--red-light); font-weight: 700;">🔴 Red: Linearly Dependent Zero Rows</span>
</div>

{routing_strip_html}"""
    return md


def build_derivation_timeline(steps):
    """
    Builds the progressive vertical timeline with visual step goals, focus targets,
    and highlighted positions in intermediate matrices.
    """
    if not steps or len(steps) <= 1:
        return """### 2. 🪜 Step-by-Step Derivation Progress

<div style="padding: 20px; color: #94a3b8; text-align: center; background: #131b2e; border-radius: 8px; border: 1px solid #1e293b;">
✨ Matrix is already in Reduced Row Echelon Form (RREF). No row operations were required!
</div>"""

    total_ops = len(steps) - 1
    cards_html = []

    badge_meta = {
        "initial": ("#94a3b8", "rgba(148, 163, 184, 0.15)", "Initial Matrix", "📋"),
        "swap": ("#f59e0b", "rgba(245, 158, 11, 0.15)", "Row Swap", "🔀"),
        "scale": ("#3b82f6", "rgba(59, 130, 246, 0.15)", "Row Scaling", "⚖️"),
        "replacement": ("#a855f7", "rgba(168, 85, 247, 0.15)", "Row Replacement", "🎯"),
    }

    for idx, s in enumerate(steps):
        step_type = s["type"]
        color, bg_color, badge_label, icon = badge_meta.get(step_type, ("#94a3b8", "rgba(148, 163, 184, 0.15)", "Step", "⚙️"))
        op_latex = s["op_latex"]
        desc = s["desc"]
        goal = s.get("goal", desc)
        focus_label = s.get("focus_label", "")
        # Highlight the specific row and entry being modified in this step
        mat_latex = format_step_matrix(s["matrix"], s)
        step_num = f"Step {idx}" if idx > 0 else "Initial Matrix"

        focus_badge = f"<span class='step-focus-pill'>📍 Focus: {focus_label}</span>" if focus_label else ""

        card = f"""<div class="timeline-step {step_type}">
<div class="step-card">
<div class="step-header">
<div style="display: flex; align-items: center; gap: 8px;">
<span style="font-size: 14px;">{icon}</span>
<span class="step-badge" style="background: {bg_color}; color: {color}; border: 1px solid {color}40;">
{badge_label}
</span>
<span style="font-size: 13px; font-weight: 700; color: #f1f5f9;">{step_num}</span>
</div>
<div style="font-size: 14px; font-weight: 700; color: {color};">$${op_latex}$$</div>
</div>
<div class="step-goal-container">
<div class="step-goal-text"><b>🎯 Goal:</b> {goal}</div>
{focus_badge}
</div>
<div class="step-matrix-box">$${mat_latex}$$</div>
</div>
</div>"""
        cards_html.append(card)

    cards_joined = "\n".join(cards_html)
    timeline = f"""### 2. 🪜 Step-by-Step Derivation Progress
<div style="margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
<span style="font-size: 15px; font-weight: 700; color: #f8fafc;">Elementary Row Operations Progress</span>
<span style="font-size: 12px; background: #1e293b; border: 1px solid #334155; padding: 4px 10px; border-radius: 12px; color: #94a3b8;">
Total Steps: <b>{total_ops}</b>
</span>
</div>
<div class="timeline-container">
{cards_joined}
</div>"""
    return timeline


def build_subspaces_card(orig_mat, pivot_cols, free_cols, zero_rows, rank, nullity, n):
    """
    Constructs the visual fundamental subspaces card for Col(A) and Null(A).
    """
    col_vectors = [sp.latex(orig_mat[:, c]) for c in pivot_cols]
    if col_vectors:
        col_basis_latex = "\\left\\{ " + ", ".join(col_vectors) + " \\right\\}"
    else:
        col_basis_latex = "\\left\\{ \\mathbf{0} \\right\\}"

    null_vectors = orig_mat.nullspace()
    if null_vectors:
        null_basis_latex = "\\left\\{ " + ", ".join([sp.latex(v) for v in null_vectors]) + " \\right\\}"
    else:
        null_basis_latex = "\\left\\{ \\mathbf{0} \\right\\}"

    md = f"""### 4. 📐 Fundamental Subspaces & Bases

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin-top: 12px;">
<div style="background: #131b2e; border: 1px solid var(--card-border); border-radius: 10px; padding: 16px;">
<div style="font-size: 15px; font-weight: 800; color: var(--gold-light); margin-bottom: 6px;">
🟡 Column Space (Image): $\\operatorname{{Col}}(A) \\subseteq \\mathbb{{R}}^{{{orig_mat.rows}}}$
</div>
<div style="font-size: 13px; color: #cbd5e1; margin-bottom: 8px;">
<b>Dimension:</b> $\\dim \\operatorname{{Col}}(A) = \\operatorname{{Rank}}(A) = {rank}$
</div>
<div style="font-size: 12px; color: #94a3b8; margin-bottom: 8px;">
Formed by the pivot columns of the <i>original</i> matrix:
</div>
<div style="background: #090d16; border-radius: 6px; padding: 12px; text-align: center; overflow-x: auto;">$$\\mathcal{{B}}_{{\\operatorname{{Col}}(A)}} = {col_basis_latex}$$</div>
</div>

<div style="background: #131b2e; border: 1px solid var(--card-border); border-radius: 10px; padding: 16px;">
<div style="font-size: 15px; font-weight: 800; color: var(--blue-light); margin-bottom: 6px;">
🔵 Null Space (Kernel): $\\operatorname{{Null}}(A) \\subseteq \\mathbb{{R}}^{{{n}}}$
</div>
<div style="font-size: 13px; color: #cbd5e1; margin-bottom: 8px;">
<b>Dimension:</b> $\\dim \\operatorname{{Null}}(A) = \\operatorname{{Nullity}}(A) = {nullity}$
</div>
<div style="font-size: 12px; color: #94a3b8; margin-bottom: 8px;">
Solutions to the homogeneous system $A \\mathbf{{x}} = \\mathbf{{0}}$:
</div>
<div style="background: #090d16; border-radius: 6px; padding: 12px; text-align: center; overflow-x: auto;">$$\\mathcal{{B}}_{{\\operatorname{{Null}}(A)}} = {null_basis_latex}$$</div>
</div>
</div>"""
    return md
