#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emission Engine Core Module
---------------------------
Scope 1 + 2 Carbon Estimation for Non-Boiler Enterprises
Philosophy: One-click generation ≠ rough estimation; 80/20 principle to target major emissions.
Author: Rolling Paths Co.
Version: 1.0 (English)
"""

from dataclasses import dataclass
from typing import Optional, Literal

# === Regional Emission Factors ===
GRID_EMISSION_FACTORS = {
    "TW": 0.495,   # Taiwan (2024)
    "US": 0.386,   # United States (average 2024)
    "EU": 0.295,   # European Union (average 2024)
    "CN": 0.581,   # China (2024)
    "JP": 0.441,   # Japan (2024)
}

# Fuel emission factors (universal)
EF_GASOLINE = 2.3  # kg CO2/L
EF_DIESEL = 2.6    # kg CO2/L
DEFAULT_CAR_KM_PER_YEAR = 15000
DEFAULT_CAR_KM_PER_L = 10
CAR_T_CO2E_PER_YEAR = (DEFAULT_CAR_KM_PER_YEAR / DEFAULT_CAR_KM_PER_L) * EF_GASOLINE / 1000  # ~3.45 tCO2e/year
BIKE_EQ = 0.5  # Motorcycle equivalent to car
EF_WATER_T_PER_M3 = 0.0004  # Water consumption
EF_WASTE_T_PER_TON = 0.33   # Waste generation


@dataclass
class Inputs:
    """
    Input parameters for carbon emission estimation
    
    Attributes:
        region: Geographic region for grid emission factor (TW/US/EU/CN/JP)
        mode: Calculation mode - "quick" or "detail"
        monthly_bill_ntd: Monthly electricity bill (NTD)
        price_per_kwh_ntd: Price per kWh (NTD)
        annual_kwh: Annual electricity consumption (kWh)
        car_count: Number of company cars
        motorcycles: Number of motorcycles
        gasoline_liters_year: Annual gasoline consumption (liters)
        diesel_liters_year: Annual diesel consumption (liters)
        refrigerant_leak_kg: Refrigerant leakage (kg/year)
        refrigerant_gwp: Refrigerant Global Warming Potential
        include_scope3: Whether to include Scope 3 minor items
        water_m3_year: Annual water consumption (m³)
        waste_ton_year: Annual waste generation (tons)
        use_rule_of_thumb: Use simplified 10% rule for Scope 1 estimation
    """
    region: Literal["TW", "US", "EU", "CN", "JP"] = "TW"
    mode: Literal["quick", "detail"] = "quick"
    monthly_bill_ntd: Optional[float] = None
    price_per_kwh_ntd: float = 4.4
    annual_kwh: Optional[float] = None
    car_count: float = 0.0
    motorcycles: float = 0.0
    gasoline_liters_year: Optional[float] = None
    diesel_liters_year: Optional[float] = None
    refrigerant_leak_kg: float = 0.0
    refrigerant_gwp: float = 1000.0
    include_scope3: bool = False
    water_m3_year: float = 0.0
    waste_ton_year: float = 0.0
    use_rule_of_thumb: bool = False


def compute_scope2(annual_kwh, monthly_bill, price_per_kwh, region="TW"):
    """
    Calculate Scope 2 emissions (Purchased Electricity)
    
    Args:
        annual_kwh: Annual electricity consumption (kWh)
        monthly_bill: Monthly electricity bill (NTD)
        price_per_kwh: Price per kWh (NTD)
        region: Geographic region (TW/US/EU/CN/JP)
    
    Returns:
        Scope 2 emissions in tCO2e
    """
    ef_grid = GRID_EMISSION_FACTORS.get(region, GRID_EMISSION_FACTORS["TW"])
    
    if annual_kwh:
        return annual_kwh * ef_grid / 1000
    if monthly_bill:
        annual_kwh = (monthly_bill / price_per_kwh) * 12
        return annual_kwh * ef_grid / 1000
    return 0.0


def compute_scope1_vehicle(car, mc, gas_liters, diesel_liters):
    """
    Calculate Scope 1 emissions from vehicles
    
    Args:
        car: Number of cars
        mc: Number of motorcycles
        gas_liters: Annual gasoline consumption (liters)
        diesel_liters: Annual diesel consumption (liters)
    
    Returns:
        Vehicle emissions in tCO2e
    """
    if gas_liters or diesel_liters:
        return (gas_liters or 0) * EF_GASOLINE / 1000 + (diesel_liters or 0) * EF_DIESEL / 1000
    
    # Use vehicle count estimation
    car_equiv = car + mc * BIKE_EQ
    return car_equiv * CAR_T_CO2E_PER_YEAR


def compute_scope1_refrigerant(leak_kg, gwp):
    """
    Calculate Scope 1 emissions from refrigerant leakage
    
    Args:
        leak_kg: Refrigerant leakage (kg/year)
        gwp: Global Warming Potential of refrigerant
    
    Returns:
        Refrigerant emissions in tCO2e
    """
    return leak_kg * gwp / 1000


def compute_minor_scope3(water, waste):
    """
    Calculate minor Scope 3 emissions (water and waste)
    
    Args:
        water: Annual water consumption (m³)
        waste: Annual waste generation (tons)
    
    Returns:
        Minor Scope 3 emissions in tCO2e
    """
    return water * EF_WATER_T_PER_M3 + waste * EF_WASTE_T_PER_TON


def estimate(inputs: Inputs):
    """
    Main estimation function for carbon emissions
    
    Args:
        inputs: Inputs dataclass with all parameters
    
    Returns:
        Dictionary containing:
        - Scope2_Electricity: Scope 2 emissions (tCO2e)
        - Scope1_Vehicles: Vehicle emissions (tCO2e)
        - Scope1_Refrigerant: Refrigerant emissions (tCO2e)
        - Scope1_Total: Total Scope 1 emissions (tCO2e)
        - Total_S1S2: Total Scope 1 + 2 emissions (tCO2e)
        - Scope3_Minor: Minor Scope 3 emissions (tCO2e)
        - Total_With_S3: Total including Scope 3 (tCO2e)
        - Share_Percent: Percentage breakdown
        - Region: Selected region
        - Grid_EF: Grid emission factor used (kg CO2/kWh)
    """
    # Get grid emission factor for selected region
    ef_grid = GRID_EMISSION_FACTORS.get(inputs.region, GRID_EMISSION_FACTORS["TW"])
    
    # Calculate Scope 2 (Electricity)
    s2 = compute_scope2(inputs.annual_kwh, inputs.monthly_bill_ntd, inputs.price_per_kwh_ntd, inputs.region)
    
    # Calculate Scope 1 (Vehicles)
    s1v = compute_scope1_vehicle(
        inputs.car_count, 
        inputs.motorcycles, 
        inputs.gasoline_liters_year, 
        inputs.diesel_liters_year
    )
    
    # Calculate Scope 1 (Refrigerant)
    s1r = compute_scope1_refrigerant(inputs.refrigerant_leak_kg, inputs.refrigerant_gwp)
    
    # Total Scope 1
    s1 = s1v + s1r
    
    # Total Scope 1 + 2
    total = s1 + s2

    # Apply rule of thumb if requested (Scope 1 ≈ 10% of Scope 2)
    if inputs.use_rule_of_thumb and s2 > 0:
        total = s2 * 1.1
        s1 = total - s2
        s1v = s1 * 0.9
        s1r = s1 * 0.1

    # Calculate percentage shares
    share_s2 = s2 / total * 100 if total else 0
    share_s1v = s1v / total * 100 if total else 0
    share_s1r = s1r / total * 100 if total else 0
    
    # Calculate minor Scope 3 if requested
    s3_minor = compute_minor_scope3(inputs.water_m3_year, inputs.waste_ton_year) if inputs.include_scope3 else 0

    # Total including Scope 3
    total_with_s3 = total + s3_minor
    
    return {
        "Scope2_Electricity": round(s2, 2),
        "Scope1_Vehicles": round(s1v, 2),
        "Scope1_Refrigerant": round(s1r, 2),
        "Scope1_Total": round(s1, 2),
        "Total_S1S2": round(total, 2),
        "Scope3_Minor": round(s3_minor, 2),
        "Total_With_S3": round(total_with_s3, 2),
        "Share_Percent": {
            "Electricity": round(share_s2, 1), 
            "Vehicles": round(share_s1v, 1), 
            "Refrigerant": round(share_s1r, 1)
        },
        "Region": inputs.region,
        "Grid_EF": ef_grid
    }


# === Helper Functions for UI Integration ===

def quick_estimate_from_monthly_bill(monthly_bill_ntd: float, car_count: int = 0, motorcycles: int = 0, region: str = "TW"):
    """
    Quick estimation using only monthly electricity bill
    
    Args:
        monthly_bill_ntd: Monthly electricity bill (NTD)
        car_count: Number of company cars
        motorcycles: Number of motorcycles
        region: Geographic region (TW/US/EU/CN/JP)
    
    Returns:
        Simplified emission results
    """
    inputs = Inputs(
        region=region,
        mode="quick",
        monthly_bill_ntd=monthly_bill_ntd,
        car_count=float(car_count),
        motorcycles=float(motorcycles),
        use_rule_of_thumb=True
    )
    return estimate(inputs)


def detailed_estimate(
    annual_kwh: float,
    gasoline_liters: float = 0,
    diesel_liters: float = 0,
    refrigerant_kg: float = 0,
    refrigerant_gwp: float = 1000,
    water_m3: float = 0,
    waste_ton: float = 0,
    region: str = "TW"
):
    """
    Detailed estimation with all parameters
    
    Args:
        annual_kwh: Annual electricity consumption (kWh)
        gasoline_liters: Annual gasoline consumption (liters)
        diesel_liters: Annual diesel consumption (liters)
        refrigerant_kg: Refrigerant leakage (kg/year)
        refrigerant_gwp: Global Warming Potential
        water_m3: Annual water consumption (m³)
        waste_ton: Annual waste generation (tons)
        region: Geographic region (TW/US/EU/CN/JP)
    
    Returns:
        Detailed emission results
    """
    inputs = Inputs(
        region=region,
        mode="detail",
        annual_kwh=annual_kwh,
        gasoline_liters_year=gasoline_liters,
        diesel_liters_year=diesel_liters,
        refrigerant_leak_kg=refrigerant_kg,
        refrigerant_gwp=refrigerant_gwp,
        include_scope3=True,
        water_m3_year=water_m3,
        waste_ton_year=waste_ton
    )
    return estimate(inputs)

