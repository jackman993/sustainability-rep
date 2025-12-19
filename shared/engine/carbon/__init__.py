"""
Carbon Emission Calculation Module
"""
from .emission_calc import (
    Inputs,
    estimate,
    GRID_EMISSION_FACTORS,
    REGION_ELECTRICITY_PRICES,
    quick_estimate_from_monthly_bill,
    detailed_estimate
)
from .calculator_component import render_calculator

__all__ = [
    'Inputs',
    'estimate',
    'GRID_EMISSION_FACTORS',
    'REGION_ELECTRICITY_PRICES',
    'quick_estimate_from_monthly_bill',
    'detailed_estimate',
    'render_calculator'
]

