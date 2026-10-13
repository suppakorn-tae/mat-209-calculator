"""
================================================================================
theme.py - Dark Analytical Theme & Mathematical Visual Styling
================================================================================
Provides custom CSS for MAT-209 Rank & Nullity Calculator:
- Dark analytical background (#0B0F19, #131B2E, #1E293B)
- Semantic Math Color Palette:
    * Gold (#F59E0B): Pivots & Pivot Columns
    * Red  (#EF4444): Zeroed-out linearly dependent rows
    * Blue (#3B82F6): Free variables & Nullity
    * Green(#10B981): Verified Rank-Nullity Theorem results
- Mathematical matrix layout: A = [ ... ] (single bracket, dynamic flex scaling)
- Transparent matrix container background (no rigid gray box)
- Unfilled empty cells styled as dashed placeholder boxes
- Perfectly centered "A =" text responding smoothly to size changes
- Progressive step derivation timeline styling
================================================================================
"""

CUSTOM_CSS = """
/* ==========================================================================
   MAT-209 Analytical Dark Theme & Semantic Color Coding
   ========================================================================== */

:root {
    --bg-dark: #0b0f19;
    --card-dark: #131b2e;
    --card-border: #1e293b;
    --card-hover: #1e293b;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;

    /* Semantic Math Color Palette */
    --gold: #f59e0b;
    --gold-light: #fbbf24;
    --gold-bg: rgba(245, 158, 11, 0.12);
    --gold-border: rgba(245, 158, 11, 0.4);

    --red: #ef4444;
    --red-light: #f87171;
    --red-bg: rgba(239, 68, 68, 0.12);
    --red-border: rgba(239, 68, 68, 0.4);

    --blue: #3b82f6;
    --blue-light: #60a5fa;
    --blue-bg: rgba(59, 130, 246, 0.12);
    --blue-border: rgba(59, 130, 246, 0.4);

    --green: #10b981;
    --green-light: #34d399;
    --green-bg: rgba(16, 185, 129, 0.12);
    --green-border: rgba(16, 185, 129, 0.4);
}

/* Global Styles */
body, .gradio-container {
    background-color: var(--bg-dark) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

/* Header & Typography */
.app-header {
    background: linear-gradient(135deg, #131b2e 0%, #1e293b 100%);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 22px 26px;
    margin-bottom: 18px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
}

.app-title {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #f8fafc;
    margin: 0 0 6px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.app-subtitle {
    color: var(--text-secondary);
    font-size: 13px;
    margin: 0;
    line-height: 1.5;
}

/* Semantic Legend Bar */
.legend-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
    margin-bottom: 20px;
}

.legend-pill {
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
}

.legend-gold {
    background: var(--gold-bg);
    border: 1px solid var(--gold-border);
    color: var(--gold-light);
}

.legend-red {
    background: var(--red-bg);
    border: 1px solid var(--red-border);
    color: var(--red-light);
}

.legend-blue {
    background: var(--blue-bg);
    border: 1px solid var(--blue-border);
    color: var(--blue-light);
}

.legend-green {
    background: var(--green-bg);
    border: 1px solid var(--green-border);
    color: var(--green-light);
}

/* ==========================================================================
   MATHEMATICAL MATRIX INPUT ROW (Transparent, Vertically Centered "A =")
   ========================================================================== */

.matrix-math-row {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;  /* Center 'A =' vertically with matrix */
    justify-content: center !important; /* Centered side-by-side like an equation */
    gap: 6px !important;            /* Small gap directly next to left bracket */
    background: transparent !important; /* Completely transparent */
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    margin: 12px 0 16px 0 !important;
    padding: 0 !important;
    overflow-x: auto !important;
    width: 100% !important;
}

/* Force all matrix container chrome to be completely transparent with no gray background */
.matrix-math-row,
.matrix-math-row > div,
.matrix-math-row .form,
.matrix-math-row .block,
.matrix-math-row .gap,
.matrix-prefix-wrapper,
.matrix-bracket-box,
.matrix-row,
.matrix-cell,
.matrix-cell label,
.matrix-cell .wrap {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.matrix-math-row .matrix-prefix-wrapper,
div.matrix-prefix-wrapper {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    width: fit-content !important;
    min-width: 0 !important;
    max-width: fit-content !important;
    flex: 0 0 auto !important;
    flex-grow: 0 !important;
    flex-shrink: 0 !important;
    align-self: center !important; /* Vertically centered to middle of matrix */
}

.matrix-prefix-text {
    font-size: 32px !important;
    font-weight: 800 !important;
    font-family: 'KaTeX_Math', 'Times New Roman', Georgia, serif !important;
    font-style: italic !important;
    color: #60a5fa !important;
    user-select: none !important;
    text-shadow: 0 0 14px rgba(96, 165, 250, 0.4) !important;
    line-height: 1 !important;
    margin: 0 !important;
    padding: 0 !important;
    white-space: nowrap !important;
}

/* ==========================================================================
   EXACT SINGLE MATHEMATICAL BRACKET PAIR [ ... ]
   (Shrink-wrapped to content, dynamic horizontal & vertical scaling)
   ========================================================================== */

.matrix-math-row .matrix-bracket-box,
div.matrix-bracket-box {
    position: relative !important;
    display: inline-flex !important;
    flex-direction: column !important;
    gap: 6px !important;
    padding: 4px 14px !important;
    width: fit-content !important;
    min-width: 0 !important;
    max-width: fit-content !important;
    flex: 0 0 auto !important;
    flex-grow: 0 !important;
    flex-shrink: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Exact Single Left Bracket '[' */
.matrix-bracket-box::before {
    content: "" !important;
    position: absolute !important;
    left: 2px !important;
    top: 0px !important;
    bottom: 0px !important;
    width: 10px !important;
    border-left: 3.5px solid #60a5fa !important;
    border-top: 3.5px solid #60a5fa !important;
    border-bottom: 3.5px solid #60a5fa !important;
    border-radius: 6px 0 0 6px !important;
    pointer-events: none !important;
    transition: all 0.15s ease !important;
}

/* Exact Single Right Bracket ']' */
.matrix-bracket-box::after {
    content: "" !important;
    position: absolute !important;
    right: 2px !important;
    top: 0px !important;
    bottom: 0px !important;
    width: 10px !important;
    border-right: 3.5px solid #60a5fa !important;
    border-top: 3.5px solid #60a5fa !important;
    border-bottom: 3.5px solid #60a5fa !important;
    border-radius: 0 6px 6px 0 !important;
    pointer-events: none !important;
    transition: all 0.15s ease !important;
}

.matrix-math-row .matrix-row,
div.matrix-row {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 6px !important;
    width: fit-content !important;
    min-width: 0 !important;
    max-width: fit-content !important;
    flex: 0 0 auto !important;
    flex-grow: 0 !important;
    flex-shrink: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Individual Matrix Cell */
.matrix-cell {
    width: 62px !important;
    min-width: 62px !important;
    max-width: 62px !important;
    flex: 0 0 62px !important;
    flex-grow: 0 !important;
    flex-shrink: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.matrix-cell label,
.matrix-cell .wrap {
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.matrix-cell input {
    width: 62px !important;
    height: 38px !important;
    min-height: 38px !important;
    border-radius: 8px !important;
    color: #f8fafc !important;
    font-family: 'JetBrains Mono', 'Fira Code', 'Roboto Mono', monospace !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    text-align: center !important;
    padding: 0 4px !important;
    margin: 0 !important;
    box-sizing: border-box !important;
    outline: none !important;
    transition: background-color 0.15s ease, border-color 0.15s ease !important;
}

/* Empty State: Transparent background & dashed border */
.matrix-cell input:placeholder-shown,
.matrix-cell input.cell-empty,
.matrix-cell input[data-empty="true"] {
    background: transparent !important;
    background-color: transparent !important;
    border: 1.5px dashed #475569 !important;
}

/* Filled State: Solid background color matching theme & NO border */
.matrix-cell input:not(:placeholder-shown),
.matrix-cell input.cell-filled,
.matrix-cell input[data-empty="false"] {
    background: #131b2e !important;
    background-color: #131b2e !important;
    border: none !important;
    box-shadow: none !important;
}

/* Hover state */
.matrix-cell input:placeholder-shown:hover,
.matrix-cell input.cell-empty:hover {
    border-color: #3b82f6 !important;
    background: rgba(30, 41, 59, 0.4) !important;
}

.matrix-cell input:not(:placeholder-shown):hover,
.matrix-cell input.cell-filled:hover {
    background: #1e293b !important;
    border: none !important;
}

/* Focus / active editing state */
.matrix-cell input:placeholder-shown:focus,
.matrix-cell input.cell-empty:focus {
    border: 1.5px dashed #60a5fa !important;
    background: rgba(30, 41, 59, 0.35) !important;
    box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.35) !important;
}

.matrix-cell input:not(:placeholder-shown):focus,
.matrix-cell input.cell-filled:focus {
    background: #1c2b4d !important;
    border: none !important;
    box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.45) !important;
}

/* Preset Toolbar Buttons */
.preset-btn {
    border: 1px solid #334155 !important;
    background: #1e293b !important;
    color: #cbd5e1 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    padding: 6px 10px !important;
    transition: all 0.2s ease !important;
}

.preset-btn:hover {
    background: #334155 !important;
    color: #f8fafc !important;
    border-color: #64748b !important;
    transform: translateY(-1px);
}

.preset-info-note {
    background: rgba(15, 23, 42, 0.65) !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    margin: 8px 0 10px 0 !important;
    font-size: 12px !important;
    color: #cbd5e1 !important;
    line-height: 1.5 !important;
}

/* Clear Matrix Button */
.clear-btn {
    background: rgba(30, 41, 59, 0.7) !important;
    border: 1px solid #334155 !important;
    color: #cbd5e1 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 9px 18px !important;
    margin-top: 10px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    width: 100% !important;
}

.clear-btn:hover {
    background: rgba(239, 68, 68, 0.15) !important;
    border-color: #ef4444 !important;
    color: #fca5a5 !important;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2) !important;
    transform: translateY(-1px);
}

/* MATLAB Matrix Input Box */
#matlab_matrix_input,
#matlab_matrix_input .wrap {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

#matlab_matrix_input input {
    background: #131b2e !important;
    border: 1px solid #334155 !important;
    color: #f8fafc !important;
    font-family: 'JetBrains Mono', 'Fira Code', 'Roboto Mono', monospace !important;
    font-size: 13px !important;
    border-radius: 6px !important;
    padding: 6px 12px !important;
    height: 38px !important;
    min-height: 38px !important;
    box-sizing: border-box !important;
}

#matlab_matrix_input input:focus {
    border-color: #60a5fa !important;
    box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.35) !important;
}

/* MATLAB Accordion */
.matlab-accordion {
    background: rgba(19, 27, 46, 0.5) !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    margin: 10px 0 14px 0 !important;
    overflow: hidden !important;
}

.matlab-accordion > .label-wrap,
.matlab-accordion summary {
    background: transparent !important;
    color: #93c5fd !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    cursor: pointer !important;
    padding: 8px 12px !important;
}

/* ==========================================================================
   HERO RANK & NULLITY KPI SCORECARDS (2 PROMINENT CARDS ON TOP OF TABS)
   ========================================================================== */

.hero-kpi-grid {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 14px !important;
    margin-bottom: 16px !important;
}

@media (max-width: 640px) {
    .hero-kpi-grid {
        grid-template-columns: 1fr !important;
        gap: 10px !important;
    }
}

.hero-kpi-card {
    background: #0d1322 !important;
    border-radius: 12px !important;
    padding: 16px 18px !important;
    position: relative !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
    transition: transform 0.2s ease, border-color 0.2s ease !important;
    box-sizing: border-box !important;
}

.hero-kpi-card:hover {
    transform: translateY(-2px);
}

/* ==========================================================================
   HORIZONTALLY SCROLLABLE STEP TABS (HIDDEN SCROLLBAR, MOUSE SCROLL & PEEKING)
   ========================================================================== */

.scrollable-tabs {
    position: relative !important;
}

.scrollable-tabs > .tab-wrapper,
.scrollable-tabs .tab-wrapper {
    height: auto !important;
    padding-bottom: 0 !important;
    margin-bottom: 16px !important;
    overflow: visible !important;
    display: flex !important;
    align-items: center !important;
}

.scrollable-tabs .overflow-menu {
    display: none !important;
}

.scrollable-tabs .tab-container {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 10px !important;
    width: 100% !important;
    height: auto !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    scroll-snap-type: x mandatory !important;
    scroll-behavior: smooth !important;
    -webkit-overflow-scrolling: touch !important;
    scrollbar-width: none !important; /* Firefox */
    -ms-overflow-style: none !important; /* IE / Edge */
    padding: 4px 2px 10px 2px !important;
    cursor: grab !important;
    user-select: none !important;
    border-bottom: 1.5px solid rgba(255, 255, 255, 0.08) !important;
    background: transparent !important;
}

.scrollable-tabs .tab-container::-webkit-scrollbar {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}

.scrollable-tabs .tab-container:active,
.scrollable-tabs .tab-container.is-dragging {
    cursor: grabbing !important;
    scroll-snap-type: none !important;
}

.scrollable-tabs .tab-container * {
    -webkit-user-drag: none !important;
}

/* Individual tab button responsive sizing with peeking:
   When viewing Tab 1, Tab 2 is visible and Tab 3 peeks out on the right */
.scrollable-tabs .tab-container > button,
.scrollable-tabs .tab-container button[role="tab"] {
    flex: 0 0 calc((100% - 20px) / 2.25) !important;
    min-width: 190px !important;
    max-width: 270px !important;
    scroll-snap-align: start !important;
    scroll-margin-left: 2px !important;
    height: 42px !important;
    padding: 0 14px !important;
    border-radius: 8px !important;
    background: #0d1322 !important;
    border: 1px solid rgba(51, 65, 85, 0.6) !important;
    color: #94a3b8 !important;
    font-size: 12.5px !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease !important;
    box-sizing: border-box !important;
}

.scrollable-tabs .tab-container > button:hover:not(:disabled):not(.selected) {
    background: rgba(30, 41, 59, 0.9) !important;
    border-color: rgba(96, 165, 250, 0.5) !important;
    color: #e2e8f0 !important;
    transform: translateY(-1px);
}

.scrollable-tabs .tab-container > button.selected,
.scrollable-tabs .tab-container button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.25) 0%, rgba(13, 19, 34, 0.95) 100%) !important;
    border: 1.5px solid #3b82f6 !important;
    color: #60a5fa !important;
    box-shadow: 0 2px 10px rgba(59, 130, 246, 0.25) !important;
}

.scrollable-tabs .tab-container > button.selected::after,
.scrollable-tabs .tab-container button[role="tab"]::after {
    display: none !important;
}

@media (max-width: 768px) {
    .scrollable-tabs .tab-container > button,
    .scrollable-tabs .tab-container button[role="tab"] {
        flex: 0 0 calc((100% - 12px) / 1.25) !important;
        min-width: 175px !important;
        max-width: 240px !important;
        font-size: 12px !important;
        height: 38px !important;
        padding: 0 10px !important;
    }
}

.hero-rank-card {
    border: 1.5px solid rgba(245, 158, 11, 0.5) !important;
    background: linear-gradient(145deg, rgba(245, 158, 11, 0.1) 0%, rgba(13, 19, 34, 0.95) 100%) !important;
}

.hero-nullity-card {
    border: 1.5px solid rgba(59, 130, 246, 0.5) !important;
    background: linear-gradient(145deg, rgba(59, 130, 246, 0.1) 0%, rgba(13, 19, 34, 0.95) 100%) !important;
}

.hero-total-card {
    border: 1.5px solid rgba(16, 185, 129, 0.5) !important;
    background: linear-gradient(145deg, rgba(16, 185, 129, 0.1) 0%, rgba(13, 19, 34, 0.95) 100%) !important;
}

.hero-det-card {
    border: 1.5px solid rgba(168, 85, 247, 0.5) !important;
    background: linear-gradient(145deg, rgba(168, 85, 247, 0.1) 0%, rgba(13, 19, 34, 0.95) 100%) !important;
}

.hero-kpi-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    margin-bottom: 4px !important;
}

.hero-kpi-badge {
    font-size: 11px !important;
    font-weight: 800 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 3px 8px !important;
    border-radius: 6px !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
}

.hero-rank-badge {
    background: rgba(245, 158, 11, 0.18) !important;
    color: #fbbf24 !important;
    border: 1px solid rgba(245, 158, 11, 0.4) !important;
}

.hero-nullity-badge {
    background: rgba(59, 130, 246, 0.18) !important;
    color: #93c5fd !important;
    border: 1px solid rgba(59, 130, 246, 0.4) !important;
}

.hero-total-badge {
    background: rgba(16, 185, 129, 0.18) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16, 185, 129, 0.4) !important;
}

.hero-det-badge {
    background: rgba(168, 85, 247, 0.18) !important;
    color: #c084fc !important;
    border: 1px solid rgba(168, 85, 247, 0.4) !important;
}

.hero-kpi-pct {
    font-size: 12px !important;
    font-weight: 700 !important;
    color: #94a3b8 !important;
}

.hero-kpi-value {
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    line-height: 1 !important;
    margin: 8px 0 6px 0 !important;
    letter-spacing: -0.02em !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
}

.hero-rank-value {
    color: #f59e0b !important;
    text-shadow: 0 0 24px rgba(245, 158, 11, 0.35) !important;
}

.hero-nullity-value {
    color: #3b82f6 !important;
    text-shadow: 0 0 24px rgba(59, 130, 246, 0.35) !important;
}

.hero-total-value {
    color: #10b981 !important;
    text-shadow: 0 0 24px rgba(16, 185, 129, 0.35) !important;
}

.hero-det-value {
    color: #c084fc !important;
    text-shadow: 0 0 24px rgba(168, 85, 247, 0.35) !important;
    font-size: 2.2rem !important;
}

.hero-kpi-subtitle {
    font-size: 12.5px !important;
    color: #cbd5e1 !important;
    line-height: 1.4 !important;
    font-weight: 500 !important;
}

.hero-kpi-footer {
    margin-top: 12px !important;
    padding-top: 10px !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    display: flex !important;
    justify-content: space-between !important;
    font-size: 11.5px !important;
    color: #94a3b8 !important;
}

/* ==========================================================================
   VISUAL DIMENSION BALANCE BAR & THEOREM CARDS
   ========================================================================== */

.dim-balance-container {
    background: #131b2e;
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 18px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.dim-bar-wrapper {
    margin: 14px 0 10px 0;
}

.dim-bar-track {
    display: flex;
    height: 22px;
    border-radius: 11px;
    overflow: hidden;
    background: #090d16;
    border: 1px solid #25334d;
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.6);
}

.dim-bar-rank {
    background: linear-gradient(90deg, #d97706, #fbbf24);
    box-shadow: 0 0 12px rgba(245, 158, 11, 0.4);
    transition: width 0.4s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
    color: #0b0f19;
}

.dim-bar-null {
    background: linear-gradient(90deg, #2563eb, #60a5fa);
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.4);
    transition: width 0.4s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
    color: #0b0f19;
}

.theorem-proof-badge {
    background: rgba(16, 185, 129, 0.12);
    border: 1.5px solid var(--green);
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    margin-top: 14px;
}

/* ==========================================================================
   COLUMN CLASSIFICATION & ROUTING FLOW ("WHERE EACH COLUMN GOES")
   ========================================================================== */

.col-routing-container {
    background: #0f172a !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    margin: 16px 0 !important;
}

.col-routing-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    margin-bottom: 12px !important;
    padding-bottom: 10px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.col-routing-list {
    display: flex !important;
    flex-direction: column !important;
    gap: 8px !important;
}

.col-route-card {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 10px 16px !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    flex-wrap: wrap !important;
    gap: 12px !important;
    transition: all 0.15s ease !important;
}

.col-route-card:hover {
    transform: translateY(-1px);
}

.route-pivot {
    background: rgba(245, 158, 11, 0.08) !important;
    border: 1px solid rgba(245, 158, 11, 0.35) !important;
}

.route-pivot:hover {
    background: rgba(245, 158, 11, 0.14) !important;
    border-color: rgba(245, 158, 11, 0.55) !important;
}

.route-free {
    background: rgba(59, 130, 246, 0.08) !important;
    border: 1px solid rgba(59, 130, 246, 0.35) !important;
}

.route-free:hover {
    background: rgba(59, 130, 246, 0.14) !important;
    border-color: rgba(59, 130, 246, 0.55) !important;
}

.col-route-col {
    display: flex !important;
    align-items: center !important;
    min-width: 120px !important;
}

.route-badge-gold {
    background: rgba(245, 158, 11, 0.2) !important;
    color: #fbbf24 !important;
    border: 1px solid rgba(245, 158, 11, 0.5) !important;
    font-weight: 800 !important;
    padding: 4px 10px !important;
    border-radius: 6px !important;
    font-size: 12.5px !important;
}

.route-badge-blue {
    background: rgba(59, 130, 246, 0.2) !important;
    color: #93c5fd !important;
    border: 1px solid rgba(59, 130, 246, 0.5) !important;
    font-weight: 800 !important;
    padding: 4px 10px !important;
    border-radius: 6px !important;
    font-size: 12.5px !important;
}

.col-route-arrow {
    color: #64748b !important;
    font-weight: 800 !important;
    font-size: 14px !important;
}

.col-route-status {
    display: flex !important;
    flex-direction: column !important;
    min-width: 190px !important;
}

.col-route-dest {
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-end !important;
    min-width: 190px !important;
    text-align: right !important;
}

.dest-badge-gold {
    color: #fbbf24 !important;
    font-weight: 800 !important;
    font-size: 13px !important;
}

.dest-badge-blue {
    color: #60a5fa !important;
    font-weight: 800 !important;
    font-size: 13px !important;
}

/* ==========================================================================
   TIMELINE STEP-BY-STEP DERIVATION CARDS & GOAL BOXES
   ========================================================================== */

.timeline-container {
    max-height: 600px;
    overflow-y: auto;
    padding-right: 6px;
    margin-top: 8px;
}

.timeline-step {
    position: relative;
    padding-left: 24px;
    margin-bottom: 16px;
    border-left: 2px solid #28354f;
}

.timeline-step::before {
    content: '';
    position: absolute;
    left: -6px;
    top: 6px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #60a5fa;
    border: 2px solid #0b0f19;
}

.timeline-step.swap::before { background: #f59e0b; }
.timeline-step.scale::before { background: #3b82f6; }
.timeline-step.replacement::before { background: #a855f7; }

.step-card {
    background: #131b2e;
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 14px 18px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.step-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    flex-wrap: wrap;
    gap: 8px;
}

.step-badge {
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.step-goal-container {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid #23334d;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
}

.step-goal-text {
    font-size: 12px;
    color: #cbd5e1;
}

.step-focus-pill {
    font-size: 11px;
    font-weight: 700;
    background: rgba(96, 165, 250, 0.15);
    border: 1px solid rgba(96, 165, 250, 0.4);
    color: #93c5fd;
    padding: 2px 8px;
    border-radius: 4px;
}

.step-matrix-box {
    background: #090d16;
    border: 1px solid #1a2333;
    border-radius: 6px;
    padding: 10px;
    overflow-x: auto;
    text-align: center;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #0e1526;
}
::-webkit-scrollbar-thumb {
    background: #25334d;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #384c6e;
}
"""
