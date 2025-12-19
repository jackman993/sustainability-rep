"""
Carbon Calculator UI Component
Reusable calculator component for integration into Streamlit pages
"""
import streamlit as st
from datetime import datetime
from .emission_calc import Inputs, estimate, GRID_EMISSION_FACTORS, REGION_ELECTRICITY_PRICES


def render_calculator(
    show_title: bool = True,
    show_region: bool = True,
    compact_mode: bool = False,
    default_region: str = "TW"
):
    """
    Render carbon emission calculator component
    
    Args:
        show_title: Whether to show the calculator title
        show_region: Whether to show region selection
        compact_mode: Compact mode (reduced spacing)
        default_region: Default region selection
    
    Returns:
        Dictionary with calculation results if calculation was performed, None otherwise
    """
    # Region names mapping
    region_names = {
        "TW": "🇹🇼 Taiwan",
        "US": "🇺🇸 United States",
        "EU": "🇪🇺 European Union",
        "CN": "🇨🇳 China",
        "JP": "🇯🇵 Japan"
    }
    
    # Initialize session state for results
    if "carbon_calc_result" not in st.session_state:
        st.session_state.carbon_calc_result = None
    if "carbon_calc_done" not in st.session_state:
        st.session_state.carbon_calc_done = False
    
    # Title (optional)
    if show_title:
        st.subheader("🌍 Carbon Emission Calculator")
        if not compact_mode:
            st.divider()
    
    # Region Selection (optional)
    if show_region:
        st.subheader("📍 Region Selection")
        region = st.selectbox(
            "Select Your Region",
            options=list(region_names.keys()),
            format_func=lambda x: region_names[x],
            index=list(region_names.keys()).index(default_region) if default_region in region_names else 0,
            help="Different regions have different grid emission factors",
            key="carbon_calc_region_selector"
        )
        
        grid_ef = GRID_EMISSION_FACTORS[region]
        st.info(f"Grid Emission Factor: **{grid_ef} kg CO2/kWh**")
        
        if not compact_mode:
            st.divider()
    else:
        region = default_region
    
    # Store current region in session state to detect changes
    if "carbon_calc_last_region" not in st.session_state:
        st.session_state.carbon_calc_last_region = region
    
    # Reset price when region changes to match new region's default
    if st.session_state.carbon_calc_last_region != region:
        st.session_state.carbon_calc_last_region = region
        # Reset price to new region's default when region changes
        new_region_config = REGION_ELECTRICITY_PRICES.get(region, REGION_ELECTRICITY_PRICES["TW"])
        st.session_state.quick_price_kwh = float(new_region_config["price"])
    
    # Input Section
    st.subheader("📊 Input Data")
    
    tab1, tab2 = st.tabs(["Quick Mode", "Detailed Mode"])
    
    with tab1:
        st.write("**Quick Estimation (Monthly Bill)**")
        
        # Check if clear was requested
        if st.session_state.get("clear_carbon_inputs", False):
            keys_to_clear = [
                "quick_monthly_bill",
                "quick_price_kwh",
                "quick_cars",
                "quick_motorcycles",
                "carbon_calc_result",
                "carbon_calc_done",
                "carbon_emission"
            ]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.clear_carbon_inputs = False
        
        # Get region-specific currency and price
        region_config = REGION_ELECTRICITY_PRICES.get(region, REGION_ELECTRICITY_PRICES["TW"])
        currency_symbol = region_config["symbol"]
        default_price = region_config["price"]
        
        # Monthly bill input with region-specific currency
        monthly_bill = st.number_input(
            f"Monthly Electricity Bill ({currency_symbol})",
            min_value=0,
            value=5000,
            step=500,
            key="quick_monthly_bill"
        )
        
        # Price per kWh with region-specific currency and default value
        # Get current price value or use default (ensure float type)
        # If region changed, use new region's default price
        if "quick_price_kwh" in st.session_state:
            current_price = float(st.session_state.quick_price_kwh)
        else:
            current_price = float(default_price)
        
        price_per_kwh = st.number_input(
            f"Electricity Price per kWh ({currency_symbol}/kWh)",
            min_value=0.0,
            value=current_price,
            step=0.01 if default_price < 1 else (1.0 if default_price < 10 else 5.0),
            help=f"Default: {region_config['note']}. Adjust based on your actual electricity rate.",
            key="quick_price_kwh"
        )
        
        # Info box explaining this is an estimate
        st.info(f"💡 **Note**: Default electricity price is **{currency_symbol}{default_price}/kWh** ({region_config['note']}). This is an estimate and may vary by industry and consumption level. Please adjust based on your actual rate.")
        
        # Clear all button
        if st.button("🔄 Clear All Inputs", key="clear_all_inputs", use_container_width=True):
            st.session_state.clear_carbon_inputs = True
            st.rerun()
        
        col1, col2 = st.columns(2)
        
        with col1:
            cars = st.number_input("Number of Cars", min_value=0, value=5, key="quick_cars")
        
        with col2:
            motorcycles = st.number_input("Number of Motorcycles", min_value=0, value=10, key="quick_motorcycles")
        
        if st.button("Calculate (Quick)", type="primary", use_container_width=True, key="btn_quick_calc"):
            inputs = Inputs(
                region=region,
                mode="quick",
                monthly_bill_ntd=float(monthly_bill),
                price_per_kwh_ntd=float(price_per_kwh),
                car_count=float(cars),
                motorcycles=float(motorcycles),
                use_rule_of_thumb=True
            )
            
            result = estimate(inputs)
            st.session_state.carbon_calc_result = result
            st.session_state.carbon_calc_done = True
            st.session_state.carbon_calc_region = region
            st.rerun()
    
    with tab2:
        st.write("**Detailed Estimation**")
        
        annual_kwh = st.number_input(
            "Annual Electricity Consumption (kWh)",
            min_value=0,
            value=500000,
            step=10000,
            key="detail_annual_kwh"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            gasoline = st.number_input(
                "Annual Gasoline (Liters)",
                min_value=0,
                value=15000,
                step=1000,
                key="detail_gasoline"
            )
            
            refrigerant = st.number_input(
                "Refrigerant Leakage (kg/year)",
                min_value=0.0,
                value=5.0,
                step=0.5,
                key="detail_refrigerant"
            )
        
        with col2:
            diesel = st.number_input(
                "Annual Diesel (Liters)",
                min_value=0,
                value=5000,
                step=1000,
                key="detail_diesel"
            )
            
            gwp = st.number_input(
                "Refrigerant GWP",
                min_value=0,
                value=1430,
                step=100,
                help="Common: R-134a (1430), R-410A (2088), R-32 (675)",
                key="detail_gwp"
            )
        
        include_scope3 = st.checkbox("Include Scope 3 (Water & Waste)", value=True, key="detail_scope3")
        
        if include_scope3:
            col1, col2 = st.columns(2)
            with col1:
                water = st.number_input("Water (m³/year)", min_value=0, value=2000, step=100, key="detail_water")
            with col2:
                waste = st.number_input("Waste (tons/year)", min_value=0, value=50, step=5, key="detail_waste")
        else:
            water = 0
            waste = 0
        
        if st.button("Calculate (Detailed)", type="primary", use_container_width=True, key="btn_detail_calc"):
            inputs = Inputs(
                region=region,
                mode="detail",
                annual_kwh=float(annual_kwh),
                gasoline_liters_year=float(gasoline),
                diesel_liters_year=float(diesel),
                refrigerant_leak_kg=float(refrigerant),
                refrigerant_gwp=float(gwp),
                include_scope3=include_scope3,
                water_m3_year=float(water),
                waste_ton_year=float(waste)
            )
            
            result = estimate(inputs)
            st.session_state.carbon_calc_result = result
            st.session_state.carbon_calc_done = True
            st.session_state.carbon_calc_region = region
            st.rerun()
    
    # Results Section
    if st.session_state.get("carbon_calc_done") and st.session_state.carbon_calc_result:
        if not compact_mode:
            st.divider()
        
        st.subheader("📈 Calculation Results")
        
        result = st.session_state.carbon_calc_result
        calc_region = st.session_state.get("carbon_calc_region", region)
        
        # Summary Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Scope 2 (Electricity)",
                f"{result['Scope2_Electricity']} tCO2e",
                delta=f"{result['Share_Percent']['Electricity']}%"
            )
        
        with col2:
            st.metric(
                "Scope 1 (Vehicles)",
                f"{result['Scope1_Vehicles']} tCO2e",
                delta=f"{result['Share_Percent']['Vehicles']}%"
            )
        
        with col3:
            st.metric(
                "Scope 1 (Refrigerant)",
                f"{result['Scope1_Refrigerant']} tCO2e",
                delta=f"{result['Share_Percent']['Refrigerant']}%"
            )
        
        with col4:
            st.metric(
                "Total Emissions",
                f"{result['Total_S1S2']} tCO2e"
            )
        
        # Detailed Breakdown
        if not compact_mode:
            st.divider()
            st.subheader("🔍 Detailed Breakdown")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Emission Sources:**")
            st.write(f"- Scope 2 (Electricity): {result['Scope2_Electricity']} tCO2e")
            st.write(f"- Scope 1 (Vehicles): {result['Scope1_Vehicles']} tCO2e")
            st.write(f"- Scope 1 (Refrigerant): {result['Scope1_Refrigerant']} tCO2e")
            st.write(f"- Scope 1 Total: {result['Scope1_Total']} tCO2e")
            st.write(f"- **Total (S1+S2): {result['Total_S1S2']} tCO2e**")
            
            if result['Scope3_Minor'] > 0:
                st.write(f"- Scope 3 (Minor): {result['Scope3_Minor']} tCO2e")
                st.write(f"- **Total (with S3): {result['Total_With_S3']} tCO2e**")
        
        with col2:
            st.write("**Calculation Details:**")
            st.write(f"- Region: {region_names.get(calc_region, calc_region)}")
            st.write(f"- Grid Emission Factor: {result['Grid_EF']} kg CO2/kWh")
            st.write(f"- Electricity Share: {result['Share_Percent']['Electricity']}%")
            st.write(f"- Vehicles Share: {result['Share_Percent']['Vehicles']}%")
            st.write(f"- Refrigerant Share: {result['Share_Percent']['Refrigerant']}%")
        
        # Save to session state for use in other pages
        st.session_state["carbon_emission"] = {
            "total_tco2e": result['Total_S1S2'],
            "scope1": result['Scope1_Total'],
            "scope2": result['Scope2_Electricity'],
            "scope1_vehicles": result['Scope1_Vehicles'],
            "scope1_refrigerant": result['Scope1_Refrigerant'],
            "scope3_minor": result.get('Scope3_Minor', 0),
            "total_with_s3": result.get('Total_With_S3', result['Total_S1S2']),
            "region": calc_region,
            "grid_ef": result['Grid_EF'],
            "share_percent": result['Share_Percent'],
            "calculation_date": datetime.now().isoformat(),
            "full_result": result
        }
        
        # Estimated Annual Revenue Section
        st.divider()
        
        # Get monthly bill from session state
        monthly_bill = None
        if "quick_monthly_bill" in st.session_state and st.session_state.quick_monthly_bill:
            # Quick mode: use monthly bill directly
            monthly_bill = st.session_state.quick_monthly_bill
        elif "detail_annual_kwh" in st.session_state and st.session_state.detail_annual_kwh:
            # Detailed mode: calculate monthly bill from annual kWh
            # Use region's default electricity price or user-entered price if available
            annual_kwh = st.session_state.detail_annual_kwh
            region_config = REGION_ELECTRICITY_PRICES.get(calc_region, REGION_ELECTRICITY_PRICES["TW"])
            price_per_kwh = st.session_state.get("quick_price_kwh", region_config["price"])
            monthly_bill = (annual_kwh * price_per_kwh) / 12
        
        if monthly_bill:
            # Get currency information for the region
            region_config = REGION_ELECTRICITY_PRICES.get(calc_region, REGION_ELECTRICITY_PRICES["TW"])
            currency_name = region_config["currency"]
            currency_symbol = region_config["symbol"]
            
            # Calculate estimated annual revenue: monthly_bill × 12 × 111
            estimated_revenue_raw = monthly_bill * 12 * 111
            estimated_revenue_k = estimated_revenue_raw / 1000
            
            # Get or initialize the revenue value (user may have modified it)
            if "estimated_annual_revenue_k" not in st.session_state:
                st.session_state.estimated_annual_revenue_k = estimated_revenue_k
            else:
                # If region changed, reset to calculated value
                if st.session_state.get("estimated_annual_revenue_region") != calc_region:
                    st.session_state.estimated_annual_revenue_k = estimated_revenue_k
            
            # Display revenue estimation section
            st.subheader("💰 Estimated Annual Revenue")
            st.caption(f"Calculation: Monthly Bill × 12 × 111")
            
            # Display formatted initial calculated value
            formatted_initial = f"{estimated_revenue_k:,.2f}"
            st.info(f"**Calculated Value**: {formatted_initial} K {currency_name}")
            
            # Editable input for estimated revenue
            modified_revenue_k = st.number_input(
                f"Estimated Annual Revenue (K {currency_name})",
                min_value=0.0,
                value=float(st.session_state.estimated_annual_revenue_k),
                step=100.0,
                help="💡 You can modify this estimated value",
                key="estimated_annual_revenue_input"
            )
            
            # Display formatted current value
            formatted_current = f"{modified_revenue_k:,.2f}"
            if abs(modified_revenue_k - estimated_revenue_k) > 0.01:
                st.success(f"**Current Value**: {formatted_current} K {currency_name} (Modified)")
            else:
                st.caption(f"**Current Value**: {formatted_current} K {currency_name}")
            
            # Store to session state
            # Note: All numeric values are stored as float (pure numbers without comma separators)
            # This ensures compatibility with LLM prompts and programmatic processing
            # Formatting with comma separators should only be done for display purposes
            st.session_state["estimated_annual_revenue"] = {
                "k_value": float(modified_revenue_k),  # Pure number: 1234.56 (not "1,234.56")
                "raw_value": float(modified_revenue_k * 1000),  # Pure number for LLM/prompt use
                "currency": currency_name,
                "currency_symbol": currency_symbol,
                "region": calc_region,
                "monthly_bill": float(monthly_bill),  # Pure number
                "is_modified": abs(modified_revenue_k - estimated_revenue_k) > 0.01  # Allow small floating point differences
            }
            st.session_state.estimated_annual_revenue_k = float(modified_revenue_k)
            st.session_state.estimated_annual_revenue_region = calc_region
        
        # Download Button
        if not compact_mode:
            st.divider()
            
            report = f"""Carbon Emission Calculation Report
===================================

Region: {region_names.get(calc_region, calc_region)}
Grid Emission Factor: {result['Grid_EF']} kg CO2/kWh

RESULTS
-------
Scope 2 (Electricity): {result['Scope2_Electricity']} tCO2e ({result['Share_Percent']['Electricity']}%)
Scope 1 (Vehicles): {result['Scope1_Vehicles']} tCO2e ({result['Share_Percent']['Vehicles']}%)
Scope 1 (Refrigerant): {result['Scope1_Refrigerant']} tCO2e ({result['Share_Percent']['Refrigerant']}%)
Scope 1 Total: {result['Scope1_Total']} tCO2e

Total Emissions (Scope 1+2): {result['Total_S1S2']} tCO2e
"""
            
            if result.get('Scope3_Minor', 0) > 0:
                report += f"Scope 3 (Minor): {result['Scope3_Minor']} tCO2e\n"
                report += f"Total Emissions (with Scope 3): {result['Total_With_S3']} tCO2e\n"
            
            st.download_button(
                "📥 Download Report",
                data=report,
                file_name="carbon_emission_report.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        return result
    
    return None

