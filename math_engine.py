"""
================================================================================
math_engine.py - Exact SymPy Rational Mathematical Engine (Module Alias)
================================================================================
Re-exports exact rational solver, step tracker, and validation checks from engine.py.
================================================================================
"""

from engine import (
    validate_matrix_filled,
    parse_entry,
    custom_gauss_jordan,
    format_bmatrix_latex,
    format_step_matrix,
    compute_subspaces,
)

__all__ = [
    "validate_matrix_filled",
    "parse_entry",
    "custom_gauss_jordan",
    "format_bmatrix_latex",
    "format_step_matrix",
    "compute_subspaces",
]
