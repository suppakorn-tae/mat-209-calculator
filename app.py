"""
================================================================================
MAT-209: Interactive Rank & Nullity Calculator
================================================================================
Main Application Entry Point for Hugging Face Spaces (with @spaces.GPU support).

Modular Architecture:
- theme.py: Dark analytical CSS theme, transparent math row, single dynamic brackets.
- engine.py / math_engine.py: Exact SymPy rational arithmetic & Gauss-Jordan elimination.
- presets.py: Preset generators & resizing with empty dashed placeholders.
- visualizer.py: Visual Dimension Balance Bar, RREF card, & derivation timeline.
- app.py: Gradio UI assembly, side-by-side Left/Right layout, and event wiring.
================================================================================
"""

import gradio as gr
from theme import CUSTOM_CSS
from presets import (
    generate_identity,
    generate_zero,
    generate_random,
    generate_singular,
    parse_matlab_matrix,
)
from engine import custom_gauss_jordan
from visualizer import (
    build_hero_kpi_cards,
    build_dimension_bar,
    build_rref_card,
    build_derivation_timeline,
    build_subspaces_card,
)

MAX_DIM = 10

KEYBOARD_NAV_JS = """
(function() {
  if (window.__matrix_nav_installed) return;
  window.__matrix_nav_installed = true;

  function isVisible(el) {
    if (!el) return false;
    if (el.classList.contains("hidden") || el.classList.contains("hide")) return false;
    if (el.style.display === "none" || el.style.visibility === "hidden") return false;
    if (el.closest(".hidden")) return false;
    if (typeof el.checkVisibility === "function") {
      return el.checkVisibility();
    }
    return el.offsetParent !== null || el.offsetWidth > 0 || el.offsetHeight > 0;
  }

  function updateInputVisualState(input) {
    if (!input || input.tagName !== "INPUT") return;
    const val = (input.value || "").trim();
    if (val === "") {
      input.classList.add("cell-empty");
      input.classList.remove("cell-filled");
      input.setAttribute("data-empty", "true");
    } else {
      input.classList.remove("cell-empty");
      input.classList.add("cell-filled");
      input.setAttribute("data-empty", "false");
    }
  }

  function updateAllCells() {
    document.querySelectorAll(".matrix-bracket-box input, .matrix-cell input").forEach(updateInputVisualState);
  }

  function setupTabsScroller() {
    const containers = document.querySelectorAll(".scrollable-tabs .tab-container, .tabs .tab-container");
    containers.forEach(function(container) {
      if (container.__scroller_attached) return;
      container.__scroller_attached = true;

      // 1. Mouse wheel horizontal scroll (converts vertical deltaY into horizontal scroll)
      container.addEventListener("wheel", function(e) {
        if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
          e.preventDefault();
          container.scrollLeft += e.deltaY;
        }
      }, { passive: false });

      // 2. Mouse click & drag to scroll
      let isDown = false;
      let startX = 0;
      let scrollStart = 0;
      let hasDragged = false;

      container.addEventListener("mousedown", function(e) {
        if (e.button !== 0) return;
        isDown = true;
        hasDragged = false;
        container.classList.add("is-dragging");
        startX = e.pageX - container.offsetLeft;
        scrollStart = container.scrollLeft;
      });

      window.addEventListener("mouseup", function() {
        if (isDown) {
          isDown = false;
          container.classList.remove("is-dragging");
        }
      });

      container.addEventListener("mouseleave", function() {
        if (isDown) {
          isDown = false;
          container.classList.remove("is-dragging");
        }
      });

      container.addEventListener("mousemove", function(e) {
        if (!isDown) return;
        const x = e.pageX - container.offsetLeft;
        const walk = (x - startX) * 1.5;
        if (Math.abs(walk) > 4) {
          hasDragged = true;
          e.preventDefault();
          container.scrollLeft = scrollStart - walk;
        }
      });

      // Prevent accidental tab switch if user dragged
      container.addEventListener("click", function(e) {
        if (hasDragged) {
          e.stopPropagation();
          e.preventDefault();
          hasDragged = false;
        }
      }, true);

      // Smoothly scroll active tab into view when clicked
      container.querySelectorAll("button").forEach(function(btn) {
        btn.addEventListener("click", function() {
          setTimeout(function() {
            btn.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "nearest" });
          }, 50);
        });
      });
    });
  }

  function handleMatrixNav(e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    const key = e.key;
    if (key !== "ArrowUp" && key !== "ArrowDown" && key !== "ArrowLeft" && key !== "ArrowRight") {
      return;
    }

    const active = document.activeElement;
    if (!active || active.tagName !== "INPUT") return;

    const bracketBox = active.closest(".matrix-bracket-box");
    if (!bracketBox) return;

    const rowEl = active.closest(".matrix-row");
    if (!rowEl) return;

    const allRows = Array.from(bracketBox.querySelectorAll(".matrix-row"));
    const r = allRows.indexOf(rowEl);
    if (r === -1) return;

    const allInputs = Array.from(rowEl.querySelectorAll("input"));
    const c = allInputs.indexOf(active);
    if (c === -1) return;

    let targetR = r;
    let targetC = c;

    if (key === "ArrowUp") targetR = r - 1;
    else if (key === "ArrowDown") targetR = r + 1;
    else if (key === "ArrowLeft") targetC = c - 1;
    else if (key === "ArrowRight") targetC = c + 1;

    // Grid boundary checks: keep focus inside grid without scrolling the page
    if (targetR < 0 || targetR >= allRows.length) {
      e.preventDefault();
      return;
    }

    const targetRow = allRows[targetR];
    if (!isVisible(targetRow)) {
      e.preventDefault();
      return;
    }

    const targetInputs = Array.from(targetRow.querySelectorAll("input"));
    if (targetC < 0 || targetC >= targetInputs.length) {
      e.preventDefault();
      return;
    }

    const targetInput = targetInputs[targetC];
    if (!isVisible(targetInput)) {
      e.preventDefault();
      return;
    }

    e.preventDefault();
    targetInput.focus();
    targetInput.select();
  }

  // Intercept navigation keys in capture phase
  document.addEventListener("keydown", handleMatrixNav, true);

  // Dynamic real-time empty/filled styling toggles
  document.addEventListener("input", function(e) {
    if (e.target && e.target.tagName === "INPUT") {
      updateInputVisualState(e.target);
    }
  }, true);

  document.addEventListener("change", function(e) {
    if (e.target && e.target.tagName === "INPUT") {
      updateInputVisualState(e.target);
    }
  }, true);

  // Sync states on load and DOM mutations
  updateAllCells();
  setupTabsScroller();
  setTimeout(function() { updateAllCells(); setupTabsScroller(); }, 50);
  setTimeout(function() { updateAllCells(); setupTabsScroller(); }, 300);

  if (window.MutationObserver) {
    const observer = new MutationObserver(function() {
      updateAllCells();
      setupTabsScroller();
    });
    observer.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ["value"] });
  }

  window.__setup_matrix_nav = function() {
    document.removeEventListener("keydown", handleMatrixNav, true);
    document.addEventListener("keydown", handleMatrixNav, true);
    updateAllCells();
    setupTabsScroller();
  };
})();
"""



# -----------------------------------------------------------------------------
# 1. Hugging Face Spaces GPU Decorator Handling
# -----------------------------------------------------------------------------
try:
    import spaces
    HAVE_SPACES = True
except ImportError:
    class spaces:
        @staticmethod
        def GPU(func=None, duration=None):
            if func is None:
                def decorator(f):
                    return f
                return decorator
            return func
    HAVE_SPACES = False


# -----------------------------------------------------------------------------
# 2. Matrix Validation & Core Calculation Pipeline (Decorated with @spaces.GPU)
# -----------------------------------------------------------------------------
def is_matrix_filled(matrix_grid):
    """
    Checks if every entry in the current m x n grid is populated.
    Returns False if any cell is empty, None, or pure whitespace.
    """
    if not matrix_grid:
        return False
    for row in matrix_grid:
        for val in row:
            if val is None or str(val).strip() == "":
                return False
    return True


@spaces.GPU
def calculate_matrix_results(matrix_grid):
    """
    Runs custom Gauss-Jordan elimination and compiles all visual cards.
    Pauses with polite instructional banner when matrix is incomplete.
    """
    m = len(matrix_grid)
    n = len(matrix_grid[0]) if m > 0 else 0

    if not is_matrix_filled(matrix_grid):
        incomplete_notice = """
<div style="background: rgba(30, 41, 59, 0.4); border: 1.5px dashed #475569; border-radius: 10px; padding: 24px; text-align: center; color: #94a3b8; margin: 12px 0;">
  <div style="font-size: 20px; font-weight: 700; color: #93c5fd; margin-bottom: 6px;">✏️ Matrix Incomplete</div>
  <p style="font-size: 13px; margin: 0; color: #cbd5e1;">Please fill in all matrix entries (dashed boxes), paste MATLAB syntax, or select a preset to compute the step-by-step pipeline.</p>
</div>
"""
        return "", incomplete_notice, incomplete_notice, incomplete_notice, incomplete_notice

    try:
        # Run custom step-tracking Gauss-Jordan elimination
        sol = custom_gauss_jordan(matrix_grid)
        rank = sol["rank"]
        nullity = sol["nullity"]
        pivot_cols = sol["pivot_cols"]
        pivot_positions = sol["pivot_positions"]
        free_cols = sol["free_cols"]
        zero_rows = sol["zero_rows"]
        steps = sol["steps"]
        rref_mat = sol["rref"]
        orig_mat = sol["orig"]

        # Build visual output cards
        kpi_md = build_hero_kpi_cards(rank, nullity, n, m, zero_rows, pivot_cols, free_cols, orig_mat=orig_mat)
        rref_md = build_rref_card(orig_mat, rref_mat, pivot_positions, zero_rows, free_cols, m, n)
        steps_md = build_derivation_timeline(steps)
        dim_bar_md = build_dimension_bar(rank, nullity, n, m, zero_rows, pivot_cols, free_cols, orig_mat=orig_mat)
        subspaces_md = build_subspaces_card(orig_mat, pivot_cols, free_cols, zero_rows, rank, nullity, n)

        return kpi_md, rref_md, steps_md, dim_bar_md, subspaces_md

    except Exception as e:
        error_md = f"""
<div style="background: var(--red-bg); border: 2px solid var(--red); border-radius: 8px; padding: 16px; color: var(--red-light); margin: 12px 0;">
  <h4 style="margin: 0 0 6px 0;">⚠️ Calculation Notice</h4>
  <p style="margin: 0; font-size: 13px;">{str(e)}</p>
</div>
"""
        return "", error_md, "", "", ""


# -----------------------------------------------------------------------------
# 3. Helper for 2D Grid Extraction from Flat Array
# -----------------------------------------------------------------------------
def extract_grid(r_val, c_val, flat_vals):
    """Slices 1D flat array into an m x n 2D grid."""
    m, n = int(r_val), int(c_val)
    grid = []
    for r in range(m):
        row = []
        for c in range(n):
            idx = r * MAX_DIM + c
            row.append(flat_vals[idx])
        grid.append(row)
    return grid


# -----------------------------------------------------------------------------
# 4. Reactive Event Handlers (Sliders, Shortcuts, Presets & Live Edits)
# -----------------------------------------------------------------------------
def on_dimension_change(r_val, c_val, *flat_vals):
    """Dynamically updates row and cell visibility and recalculates or shows incomplete state."""
    m, n = int(r_val), int(c_val)
    row_updates = [gr.update(visible=(r < m)) for r in range(MAX_DIM)]
    cell_updates = []
    for r in range(MAX_DIM):
        for c in range(MAX_DIM):
            is_vis = (c < n)
            idx = r * MAX_DIM + c
            # Preserve existing value in visible zone; newly exposed cells start empty
            val = flat_vals[idx] if (r < m and c < n) else ""
            cell_updates.append(gr.update(value=val, visible=is_vis))
    grid = extract_grid(m, n, flat_vals)
    kpi, rf, st, d_bar, sub = calculate_matrix_results(grid)
    return row_updates + cell_updates + [kpi, rf, st, d_bar, sub]


def on_shortcut_size(target_r, target_c, *flat_vals):
    """Sets sliders, updates grid dimensions, and computes output."""
    m, n = int(target_r), int(target_c)
    row_updates = [gr.update(visible=(r < m)) for r in range(MAX_DIM)]
    cell_updates = []
    for r in range(MAX_DIM):
        for c in range(MAX_DIM):
            is_vis = (c < n)
            idx = r * MAX_DIM + c
            val = flat_vals[idx] if (r < m and c < n) else ""
            cell_updates.append(gr.update(value=val, visible=is_vis))
    grid = extract_grid(m, n, flat_vals)
    kpi, rf, st, d_bar, sub = calculate_matrix_results(grid)
    return [m, n] + row_updates + cell_updates + [kpi, rf, st, d_bar, sub]


def on_apply_preset(generator_fn, r_val, c_val):
    """Populates visible grid with preset values and calculates results immediately."""
    m, n = int(r_val), int(c_val)
    preset_data = generator_fn(m, n)
    cell_updates = []
    for r in range(MAX_DIM):
        for c in range(MAX_DIM):
            if r < m and c < n:
                val = str(preset_data[r][c])
            else:
                val = ""
            cell_updates.append(gr.update(value=val, visible=(c < n)))
    kpi, rf, st, d_bar, sub = calculate_matrix_results(preset_data)
    return cell_updates + [kpi, rf, st, d_bar, sub]


def on_cell_input(r_val, c_val, *flat_vals):
    """
    Calculates whenever matrix entries are edited.
    Only outputs to the right-hand side Markdown cards; never re-renders textboxes,
    preserving native browser cursor focus on every keystroke.
    """
    m, n = int(r_val), int(c_val)
    grid = extract_grid(m, n, flat_vals)
    kpi, rf, st, d_bar, sub = calculate_matrix_results(grid)
    return kpi, rf, st, d_bar, sub


def on_clear_matrix():
    """
    Clears all matrix cells back to empty strings and resets right-side analysis cards.
    """
    cell_updates = [gr.update(value="") for _ in range(MAX_DIM * MAX_DIM)]
    kpi, rf, st, d_bar, sub = calculate_matrix_results([[""]])
    return cell_updates + [kpi, rf, st, d_bar, sub]


def on_load_matlab_matrix(text):
    """
    Parses MATLAB-formatted matrix string, updates sliders and grid, populates entries,
    and calculates RREF and fundamental subspaces.
    """
    total_outputs = 2 + MAX_DIM + (MAX_DIM * MAX_DIM) + 5
    try:
        grid, m, n = parse_matlab_matrix(text)
    except Exception as e:
        gr.Warning(str(e))
        return [gr.skip()] * total_outputs

    row_updates = [gr.update(visible=(r < m)) for r in range(MAX_DIM)]
    cell_updates = []
    for r in range(MAX_DIM):
        for c in range(MAX_DIM):
            is_vis = (c < n)
            val = str(grid[r][c]) if (r < m and c < n) else ""
            cell_updates.append(gr.update(value=val, visible=is_vis))

    kpi, rf, st, d_bar, sub = calculate_matrix_results(grid)
    return [m, n] + row_updates + cell_updates + [kpi, rf, st, d_bar, sub]


# -----------------------------------------------------------------------------
# 5. Main Gradio Application Interface (Side-by-Side Left/Right Layout)
# -----------------------------------------------------------------------------
def build_app():
    latex_delims = [
        {"left": "$$", "right": "$$", "display": True},
        {"left": "$", "right": "$", "display": False}
    ]

    # Explicit default refresh state: strictly 2x2 with all 4 cells empty
    initial_matrix = [["", ""], ["", ""]]
    init_kpi, init_rref, init_steps, init_dim, init_sub = calculate_matrix_results(initial_matrix)

    with gr.Blocks(title="MAT-209: Rank & Nullity Calculator", fill_width=True) as demo:
        # Injected analytical stylesheet
        gr.HTML(f"<style>{CUSTOM_CSS}</style>")

        # Header Title Banner
        gr.HTML("""
<div class="app-header">
  <div class="app-title">
    <span>📐</span> MAT-209: Interactive Rank & Nullity Calculator
  </div>
  <p class="app-subtitle">
    Intuitive Linear Algebra • Exact Rational Step-by-Step Derivation
  </p>
</div>
""")

        # Strict Semantic Legend Bar
        gr.HTML("""
<div class="legend-container">
  <div class="legend-pill legend-gold">
    <span>🟡</span>
    <div><b>Gold:</b> Pivots (Leading 1s) & Pivot Columns</div>
  </div>
  <div class="legend-pill legend-red">
    <span>🔴</span>
    <div><b>Red:</b> Zero Rows (0 = 0, Linear Dependence)</div>
  </div>
  <div class="legend-pill legend-blue">
    <span>🔵</span>
    <div><b>Blue:</b> Free Variables & Null Space</div>
  </div>
  <div class="legend-pill legend-green">
    <span>🟢</span>
    <div><b>Green:</b> Validated Theorem Result</div>
  </div>
</div>
""")

        # =====================================================================
        # SIDE-BY-SIDE MAIN LAYOUT: Left (Controls & Matrix A) | Right (Results)
        # =====================================================================
        with gr.Row():
            # -----------------------------------------------------------------
            # LEFT COLUMN: Matrix Controls, Presets, and Input Grid A = [ ... ]
            # -----------------------------------------------------------------
            with gr.Column(scale=6):
                gr.Markdown("### 🎛️ Matrix Controls", latex_delimiters=latex_delims)

                # Dynamic dimension sliders (1x1 to 10x10) - starts explicitly at 2x2
                with gr.Row():
                    slider_rows = gr.Slider(
                        minimum=1, maximum=10, value=2, step=1,
                        label="Rows (m) [Codomain ℝᵐ]"
                    )
                    slider_cols = gr.Slider(
                        minimum=1, maximum=10, value=2, step=1,
                        label="Columns (n) [Domain Space ℝⁿ]"
                    )

                # Quick Size Shortcuts (2x2, 3x3, 4x4)
                with gr.Row():
                    btn_size_2x2 = gr.Button("2 × 2", size="sm", elem_classes=["preset-btn"])
                    btn_size_3x3 = gr.Button("3 × 3", size="sm", elem_classes=["preset-btn"])
                    btn_size_4x4 = gr.Button("4 × 4", size="sm", elem_classes=["preset-btn"])

                # Presets Toolbar
                gr.Markdown("#### 📋 Presets", latex_delimiters=latex_delims)
                with gr.Row():
                    btn_preset_ident = gr.Button("Identity (Iₙ)", elem_classes=["preset-btn"])
                    btn_preset_sing = gr.Button("Singular (det=0)", elem_classes=["preset-btn"])
                    btn_preset_zero = gr.Button("Zero (0ₘₓₙ)", elem_classes=["preset-btn"])
                    btn_preset_rand = gr.Button("Random Integers", elem_classes=["preset-btn"])

                # MATLAB Syntax Matrix Input (Collapsed by default)
                with gr.Accordion("💻 MATLAB-Style Matrix Input", open=False, elem_classes=["matlab-accordion"]):
                    with gr.Row():
                        txt_matlab = gr.Textbox(
                            placeholder="e.g. [1, 2, 3; 2, 3, 1; 2, 1, 1]",
                            container=False,
                            scale=4,
                            elem_id="matlab_matrix_input"
                        )
                        btn_matlab_load = gr.Button("📥 Load", variant="primary", scale=1, elem_classes=["preset-btn"])

                gr.Markdown("#### ✏️ Matrix Input Grid", latex_delimiters=latex_delims)

                # Mathematical Matrix Layout: A = [ ... ]
                # Exactly single bracket pair, transparent container, vertically centered "A =",
                # shrink-wrapped tightly to content with instant first-click native inputs.
                with gr.Row(elem_classes=["matrix-math-row"]):
                    gr.HTML(
                        value="<div class='matrix-prefix-text'>A =</div>",
                        elem_classes=["matrix-prefix-wrapper"],
                        scale=0,
                        min_width=0,
                        head=f"<script>{KEYBOARD_NAV_JS}</script>",
                        js_on_load=KEYBOARD_NAV_JS
                    )
                    with gr.Column(elem_classes=["matrix-bracket-box"], scale=0, min_width=0):
                        row_boxes = []
                        cells = []
                        flat_cells = []
                        for r in range(MAX_DIM):
                            with gr.Row(visible=(r < 2), elem_classes=["matrix-row"], scale=0) as rb:
                                row_cells = []
                                for c in range(MAX_DIM):
                                    tb = gr.Textbox(
                                        value="",
                                        placeholder=" ",
                                        visible=(c < 2),
                                        container=False,
                                        min_width=0,
                                        elem_id=f"matrix_cell_{r}_{c}",
                                        elem_classes=["matrix-cell", f"cell-r-{r}", f"cell-c-{c}"]
                                    )
                                    row_cells.append(tb)
                                    flat_cells.append(tb)
                                cells.append(row_cells)
                            row_boxes.append(rb)

                btn_clear = gr.Button(
                    "🗑️ Clear Matrix",
                    variant="secondary",
                    elem_classes=["clear-btn"]
                )

            # -----------------------------------------------------------------
            # RIGHT COLUMN: Step-by-Step Analytical Pipeline (Tabs 1 to 4)
            # -----------------------------------------------------------------
            with gr.Column(scale=6):
                # Hero KPI Scorecards container positioned permanently on top of the tabs
                out_hero_kpi = gr.Markdown(value=init_kpi, latex_delimiters=latex_delims)

                with gr.Tabs(elem_classes=["scrollable-tabs"], elem_id="steps_tabs", overflow_behavior="wrap"):
                    with gr.TabItem("1. 🎯 RREF Visual Map"):
                        out_rref = gr.Markdown(value=init_rref, latex_delimiters=latex_delims)

                    with gr.TabItem("2. 🪜 Step-by-Step Derivation"):
                        out_steps = gr.Markdown(value=init_steps, latex_delimiters=latex_delims)

                    with gr.TabItem("3. ⚖️ Rank-Nullity Theorem"):
                        out_dimension_bar = gr.Markdown(value=init_dim, latex_delimiters=latex_delims)

                    with gr.TabItem("4. 📐 Fundamental Subspaces"):
                        out_subspaces = gr.Markdown(value=init_sub, latex_delimiters=latex_delims)

        # ---------------------------------------------------------------------
        # Event Wiring: Reactive Sliders, Presets, Live Edits & Calculate
        # ---------------------------------------------------------------------
        analysis_outputs = [out_hero_kpi, out_rref, out_steps, out_dimension_bar, out_subspaces]

        # 1. Sliders update grid dynamically and auto-calculate (or pause if empty)
        dim_outputs = row_boxes + flat_cells + analysis_outputs
        slider_rows.change(
            fn=on_dimension_change,
            inputs=[slider_rows, slider_cols] + flat_cells,
            outputs=dim_outputs
        )
        slider_cols.change(
            fn=on_dimension_change,
            inputs=[slider_rows, slider_cols] + flat_cells,
            outputs=dim_outputs
        )

        # 2. Quick size shortcuts: set sliders, resize grid & auto-calculate
        shortcut_outputs = [slider_rows, slider_cols] + row_boxes + flat_cells + analysis_outputs
        btn_size_2x2.click(
            fn=lambda *vals: on_shortcut_size(2, 2, *vals),
            inputs=flat_cells,
            outputs=shortcut_outputs
        )
        btn_size_3x3.click(
            fn=lambda *vals: on_shortcut_size(3, 3, *vals),
            inputs=flat_cells,
            outputs=shortcut_outputs
        )
        btn_size_4x4.click(
            fn=lambda *vals: on_shortcut_size(4, 4, *vals),
            inputs=flat_cells,
            outputs=shortcut_outputs
        )

        # 3. Presets Toolbar: populates grid & calculates immediately
        preset_outputs = flat_cells + analysis_outputs
        btn_preset_ident.click(
            fn=lambda r, c: on_apply_preset(generate_identity, r, c),
            inputs=[slider_rows, slider_cols],
            outputs=preset_outputs
        )
        btn_preset_sing.click(
            fn=lambda r, c: on_apply_preset(generate_singular, r, c),
            inputs=[slider_rows, slider_cols],
            outputs=preset_outputs
        )
        btn_preset_zero.click(
            fn=lambda r, c: on_apply_preset(generate_zero, r, c),
            inputs=[slider_rows, slider_cols],
            outputs=preset_outputs
        )
        btn_preset_rand.click(
            fn=lambda r, c: on_apply_preset(generate_random, r, c),
            inputs=[slider_rows, slider_cols],
            outputs=preset_outputs
        )

        # 4. In-place Cell Editing: instant first-click typing, auto-calculates without re-rendering inputs
        for tb in flat_cells:
            tb.input(
                fn=on_cell_input,
                inputs=[slider_rows, slider_cols] + flat_cells,
                outputs=analysis_outputs,
                show_progress="hidden"
            )

        # 5. Clear button: resets all cells to empty strings and resets analysis
        btn_clear.click(
            fn=on_clear_matrix,
            inputs=None,
            outputs=flat_cells + analysis_outputs
        )

        # 6. MATLAB syntax parser: load matrix string directly into grid & compute
        matlab_outputs = [slider_rows, slider_cols] + row_boxes + flat_cells + analysis_outputs
        btn_matlab_load.click(
            fn=on_load_matlab_matrix,
            inputs=[txt_matlab],
            outputs=matlab_outputs
        )
        txt_matlab.submit(
            fn=on_load_matlab_matrix,
            inputs=[txt_matlab],
            outputs=matlab_outputs
        )

        # 7. Grid keyboard arrow navigation (Up, Down, Left, Right)
        demo.load(fn=None, inputs=None, outputs=None, js=KEYBOARD_NAV_JS)

    return demo


# -----------------------------------------------------------------------------
# 6. Application Entry Point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app = build_app()
    app.launch(head=f"<script>({KEYBOARD_NAV_JS})();</script>")
