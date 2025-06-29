import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="SolarSize Nigeria",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #FF6B35, #F7931E);
        color: white;
        margin-bottom: 2rem;
        border-radius: 10px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Common appliances database with typical power consumption
APPLIANCES_DB = {
    "Refrigerator (Energy Efficient)": {"power": 150, "hours": 24, "priority": "High"},
    "Refrigerator (Standard)": {"power": 300, "hours": 24, "priority": "High"},
    "Air Conditioner (1HP)": {"power": 746, "hours": 8, "priority": "Medium"},
    "Air Conditioner (1.5HP)": {"power": 1119, "hours": 8, "priority": "Medium"},
    "Air Conditioner (2HP)": {"power": 1492, "hours": 8, "priority": "Low"},
    "LED TV (32 inch)": {"power": 60, "hours": 6, "priority": "Medium"},
    "LED TV (55 inch)": {"power": 120, "hours": 6, "priority": "Medium"},
    "Ceiling Fan": {"power": 75, "hours": 12, "priority": "High"},
    "LED Bulb (12W)": {"power": 12, "hours": 8, "priority": "High"},
    "Fluorescent Tube": {"power": 40, "hours": 8, "priority": "Medium"},
    "Laptop": {"power": 65, "hours": 8, "priority": "High"},
    "Desktop Computer": {"power": 200, "hours": 8, "priority": "Medium"},
    "Washing Machine": {"power": 500, "hours": 1, "priority": "Medium"},
    "Microwave": {"power": 1000, "hours": 0.5, "priority": "Low"},
    "Electric Kettle": {"power": 1500, "hours": 0.25, "priority": "Low"},
    "Iron": {"power": 1200, "hours": 1, "priority": "Low"},
    "Water Pump": {"power": 750, "hours": 2, "priority": "High"},
    "Security System": {"power": 50, "hours": 24, "priority": "High"},
    "Phone Charger": {"power": 10, "hours": 3, "priority": "High"},
    "Router/WiFi": {"power": 20, "hours": 24, "priority": "High"}
}

# Solar panel data
SOLAR_PANELS = {
    "Monocrystalline 300W": {"watts": 300, "price": 85000, "efficiency": 20, "warranty": 25},
    "Monocrystalline 400W": {"watts": 400, "price": 110000, "efficiency": 21, "warranty": 25},
    "Monocrystalline 500W": {"watts": 500, "price": 135000, "efficiency": 22, "warranty": 25},
    "Polycrystalline 300W": {"watts": 300, "price": 75000, "efficiency": 17, "warranty": 20},
    "Polycrystalline 400W": {"watts": 400, "price": 95000, "efficiency": 18, "warranty": 20},
}

# Nigerian cities with average solar irradiance (kWh/m²/day)
NIGERIAN_CITIES = {
    "Lagos": 4.5,
    "Abuja": 5.2,
    "Kano": 5.8,
    "Ibadan": 4.8,
    "Port Harcourt": 4.2,
    "Kaduna": 5.5,
    "Benin City": 4.4,
    "Jos": 5.7,
    "Ilorin": 5.1,
    "Maiduguri": 6.0
}

# Vendor database
VENDORS = {
    "Lagos": [
        {"name": "SolarMax Nigeria", "rating": 4.5, "phone": "08012345678", "speciality": "Residential"},
        {"name": "GreenTech Solar", "rating": 4.2, "phone": "08087654321", "speciality": "Commercial"},
        {"name": "PowerGen Solutions", "rating": 4.7, "phone": "08011223344", "speciality": "Hybrid Systems"}
    ],
    "Abuja": [
        {"name": "Capital Solar", "rating": 4.6, "phone": "08055667788", "speciality": "Residential"},
        {"name": "Federal Solar Co.", "rating": 4.3, "phone": "08099887766", "speciality": "Government Projects"},
        {"name": "Sunrise Energy", "rating": 4.4, "phone": "08033445566", "speciality": "Off-grid Systems"}
    ],
    "Kano": [
        {"name": "Northern Solar", "rating": 4.1, "phone": "08077889900", "speciality": "Agricultural"},
        {"name": "Sahel Power", "rating": 4.5, "phone": "08044556677", "speciality": "Residential"}
    ]
}

def calculate_daily_consumption(appliances_data):
    """Calculate total daily energy consumption"""
    total_watts = 0
    total_kwh = 0
    
    for appliance, data in appliances_data.items():
        if data['quantity'] > 0:
            watts = data['power'] * data['quantity']
            kwh = (watts * data['hours']) / 1000
            total_watts += watts
            total_kwh += kwh
    
    return total_watts, total_kwh

def calculate_solar_system(daily_kwh, location, autonomy_days=2):
    """Calculate required solar system size"""
    solar_irradiance = NIGERIAN_CITIES.get(location, 5.0)
    
    # Account for system losses (inverter, wiring, etc.)
    system_efficiency = 0.85
    
    # Calculate required solar panel capacity
    required_solar_kwp = daily_kwh / (solar_irradiance * system_efficiency)
    
    # Calculate battery capacity (for autonomy days)
    battery_kwh = daily_kwh * autonomy_days
    
    return required_solar_kwp, battery_kwh, solar_irradiance

def recommend_panels(required_kwp):
    """Recommend solar panel configuration"""
    recommendations = []
    
    for panel_name, panel_data in SOLAR_PANELS.items():
        panel_kw = panel_data['watts'] / 1000
        num_panels = int(np.ceil(required_kwp / panel_kw))
        total_capacity = num_panels * panel_kw
        total_cost = num_panels * panel_data['price']
        
        recommendations.append({
            'Panel Type': panel_name,
            'Number of Panels': num_panels,
            'Total Capacity (kW)': round(total_capacity, 2),
            'Total Cost (₦)': f"₦{total_cost:,.0f}",
            'Cost per Watt (₦)': round(panel_data['price'] / panel_data['watts'], 2),
            'Efficiency (%)': panel_data['efficiency'],
            'Warranty (Years)': panel_data['warranty']
        })
    
    return pd.DataFrame(recommendations)

# Initialize session state
if 'appliances_data' not in st.session_state:
    st.session_state.appliances_data = {}

# Header
st.markdown("""
<div class="main-header">
    <h1>☀️ SolarSize Nigeria</h1>
    <p>Calculate Your Solar Power Needs & Find the Right System</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Load Calculator", "☀️ Solar Sizing", "⚖️ Load Optimization", "🏪 Find Vendors"])

if page == "🏠 Load Calculator":
    st.header("🏠 Electrical Load Calculator")
    st.write("Add your appliances to calculate your total power consumption")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Add Appliances")
        
        # Common appliances section
        st.write("**Select from Common Appliances:**")
        selected_appliances = st.multiselect(
            "Choose appliances",
            list(APPLIANCES_DB.keys()),
            help="Select multiple appliances from the list"
        )
        
        # Add selected appliances to session state
        for appliance in selected_appliances:
            if appliance not in st.session_state.appliances_data:
                st.session_state.appliances_data[appliance] = {
                    'power': APPLIANCES_DB[appliance]['power'],
                    'hours': APPLIANCES_DB[appliance]['hours'],
                    'quantity': 1,
                    'priority': APPLIANCES_DB[appliance]['priority']
                }
        
        # Custom appliance section
        st.write("**Add Custom Appliance:**")
        with st.form("custom_appliance"):
            custom_name = st.text_input("Appliance Name")
            custom_power = st.number_input("Power (Watts)", min_value=1, value=100)
            custom_hours = st.number_input("Daily Usage (Hours)", min_value=0.1, value=4.0, step=0.1)
            custom_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            
            if st.form_submit_button("Add Custom Appliance"):
                if custom_name and custom_name not in st.session_state.appliances_data:
                    st.session_state.appliances_data[custom_name] = {
                        'power': custom_power,
                        'hours': custom_hours,
                        'quantity': 1,
                        'priority': custom_priority
                    }
                    st.success(f"Added {custom_name} to your appliances!")
    
    with col2:
        st.subheader("Quick Stats")
        if st.session_state.appliances_data:
            total_watts, total_kwh = calculate_daily_consumption(st.session_state.appliances_data)
            
            st.metric("Total Power", f"{total_watts:,.0f} W")
            st.metric("Daily Energy", f"{total_kwh:.2f} kWh")
            st.metric("Monthly Energy", f"{total_kwh * 30:.1f} kWh")
            
            # Estimated monthly cost (assuming ₦100/kWh from generator)
            monthly_cost = total_kwh * 30 * 100
            st.metric("Monthly Gen. Cost", f"₦{monthly_cost:,.0f}")
    
    # Appliances configuration
    if st.session_state.appliances_data:
        st.subheader("Configure Your Appliances")
        
        appliances_df = []
        for appliance, data in st.session_state.appliances_data.items():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            with col1:
                st.write(f"**{appliance}**")
            with col2:
                quantity = st.number_input(f"Qty", min_value=0, value=data['quantity'], key=f"qty_{appliance}")
                st.session_state.appliances_data[appliance]['quantity'] = quantity
            with col3:
                st.write(f"{data['power']}W")
            with col4:
                hours = st.number_input(f"Hours", min_value=0.0, value=float(data['hours']), step=0.1, key=f"hours_{appliance}")
                st.session_state.appliances_data[appliance]['hours'] = hours
            with col5:
                if st.button("🗑️", key=f"del_{appliance}", help="Remove appliance"):
                    del st.session_state.appliances_data[appliance]
                    st.experimental_rerun()
            
            if quantity > 0:
                daily_kwh = (data['power'] * quantity * hours) / 1000
                appliances_df.append({
                    'Appliance': appliance,
                    'Quantity': quantity,
                    'Power (W)': data['power'],
                    'Hours/Day': hours,
                    'Daily kWh': round(daily_kwh, 2),
                    'Priority': data['priority']
                })
        
        # Display summary table
        if appliances_df:
            df = pd.DataFrame(appliances_df)
            st.subheader("Load Summary")
            st.dataframe(df, use_container_width=True)
            
            # Visualization
            fig = px.pie(df, values='Daily kWh', names='Appliance', 
                        title="Daily Energy Consumption by Appliance")
            st.plotly_chart(fig, use_container_width=True)

elif page == "☀️ Solar Sizing":
    st.header("☀️ Solar System Sizing")
    
    if not st.session_state.appliances_data:
        st.warning("Please add appliances in the Load Calculator first!")
        st.stop()
    
    # Calculate current consumption
    total_watts, total_kwh = calculate_daily_consumption(st.session_state.appliances_data)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("System Configuration")
        location = st.selectbox("Select Your Location", list(NIGERIAN_CITIES.keys()))
        autonomy_days = st.slider("Battery Backup Days", 1, 5, 2, 
                                 help="Number of days the system should run without sun")
        
        # Calculate solar system requirements
        required_kwp, battery_kwh, solar_irradiance = calculate_solar_system(
            total_kwh, location, autonomy_days
        )
        
        st.subheader("Your Requirements")
        st.metric("Daily Energy Need", f"{total_kwh:.2f} kWh")
        st.metric("Required Solar Capacity", f"{required_kwp:.2f} kWp")
        st.metric("Battery Capacity Needed", f"{battery_kwh:.1f} kWh")
        st.metric("Solar Irradiance", f"{solar_irradiance} kWh/m²/day")
    
    with col2:
        st.subheader("Solar Panel Recommendations")
        recommendations_df = recommend_panels(required_kwp)
        st.dataframe(recommendations_df, use_container_width=True)
        
        # Cost comparison chart
        fig = px.bar(recommendations_df, x='Panel Type', y='Cost per Watt (₦)',
                    title="Cost Comparison per Watt")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # System overview
    st.subheader("Complete System Estimate")
    
    # Select recommended system (lowest cost per watt)
    best_option = recommendations_df.loc[recommendations_df['Cost per Watt (₦)'].idxmin()]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **Recommended System:**
        - {best_option['Panel Type']}
        - {best_option['Number of Panels']} panels
        - {best_option['Total Capacity (kW)']} kW capacity
        """)
    
    with col2:
        # Additional components estimate
        panel_cost = float(best_option['Total Cost (₦)'].replace('₦', '').replace(',', ''))
        inverter_cost = required_kwp * 200000  # ₦200k per kW
        battery_cost = battery_kwh * 150000    # ₦150k per kWh
        installation_cost = panel_cost * 0.3   # 30% of panel cost
        
        total_system_cost = panel_cost + inverter_cost + battery_cost + installation_cost
        
        st.info(f"""
        **System Cost Breakdown:**
        - Panels: ₦{panel_cost:,.0f}
        - Inverter: ₦{inverter_cost:,.0f}
        - Batteries: ₦{battery_cost:,.0f}
        - Installation: ₦{installation_cost:,.0f}
        - **Total: ₦{total_system_cost:,.0f}**
        """)
    
    with col3:
        # ROI calculation
        monthly_savings = total_kwh * 30 * 100  # ₦100/kWh generator cost
        payback_months = total_system_cost / monthly_savings
        
        st.success(f"""
        **Return on Investment:**
        - Monthly Savings: ₦{monthly_savings:,.0f}
        - Payback Period: {payback_months:.1f} months
        - 20-Year Savings: ₦{(monthly_savings * 240) - total_system_cost:,.0f}
        """)

elif page == "⚖️ Load Optimization":
    st.header("⚖️ Load Optimization")
    
    if not st.session_state.appliances_data:
        st.warning("Please add appliances in the Load Calculator first!")
        st.stop()
    
    st.write("Optimize your load based on priority and budget to reduce system costs.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Budget & Priorities")
        max_budget = st.number_input("Maximum Budget (₦)", min_value=100000, value=2000000, step=100000)
        
        st.write("**Adjust Appliance Priorities:**")
        
        # Priority adjustment
        for appliance, data in st.session_state.appliances_data.items():
            if data['quantity'] > 0:
                new_priority = st.selectbox(
                    f"{appliance}", 
                    ["High", "Medium", "Low", "Remove"],
                    index=["High", "Medium", "Low"].index(data['priority']),
                    key=f"priority_{appliance}"
                )
                st.session_state.appliances_data[appliance]['priority'] = new_priority
    
    with col2:
        st.subheader("Optimization Results")
        
        # Create scenarios based on priorities
        scenarios = {
            "Essential Only (High Priority)": ["High"],
            "Essential + Important (High + Medium)": ["High", "Medium"],
            "All Appliances": ["High", "Medium", "Low"]
        }
        
        results = []
        for scenario_name, priorities in scenarios.items():
            scenario_appliances = {
                appliance: data for appliance, data in st.session_state.appliances_data.items()
                if data['priority'] in priorities and data['quantity'] > 0 and data['priority'] != "Remove"
            }
            
            if scenario_appliances:
                total_watts, total_kwh = calculate_daily_consumption(scenario_appliances)
                required_kwp, battery_kwh, _ = calculate_solar_system(total_kwh, "Lagos")  # Default location
                
                # Estimate system cost
                panel_cost = required_kwp * 300000  # Rough estimate
                inverter_cost = required_kwp * 200000
                battery_cost = battery_kwh * 150000
                installation_cost = panel_cost * 0.3
                total_cost = panel_cost + inverter_cost + battery_cost + installation_cost
                
                results.append({
                    'Scenario': scenario_name,
                    'Daily kWh': round(total_kwh, 2),
                    'Solar kWp': round(required_kwp, 2),
                    'Est. Cost (₦)': f"₦{total_cost:,.0f}",
                    'Within Budget': "✅" if total_cost <= max_budget else "❌",
                    'Monthly Savings': f"₦{total_kwh * 30 * 100:,.0f}"
                })
        
        if results:
            results_df = pd.DataFrame(results)
            st.dataframe(results_df, use_container_width=True)
            
            # Visualization
            costs = [float(cost.replace('₦', '').replace(',', '')) for cost in results_df['Est. Cost (₦)']]
            fig = px.bar(x=results_df['Scenario'], y=costs, 
                        title="System Cost by Scenario")
            fig.add_hline(y=max_budget, line_dash="dash", line_color="red", 
                         annotation_text="Budget Limit")
            st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        affordable_scenarios = [r for r in results if r['Within Budget'] == "✅"]
        if affordable_scenarios:
            best_scenario = max(affordable_scenarios, key=lambda x: x['Daily kWh'])
            st.success(f"""
            **Recommended Configuration:**
            {best_scenario['Scenario']}
            - Daily Energy: {best_scenario['Daily kWh']} kWh
            - System Cost: {best_scenario['Est. Cost (₦)']}
            - Monthly Savings: {best_scenario['Monthly Savings']}
            """)

elif page == "🏪 Find Vendors":
    st.header("🏪 Find Solar Vendors")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Search Criteria")
        selected_city = st.selectbox("Select City", list(VENDORS.keys()))
        service_type = st.selectbox("Service Type", 
                                   ["All", "Residential", "Commercial", "Off-grid Systems", "Hybrid Systems"])
        
        if st.session_state.appliances_data:
            total_watts, total_kwh = calculate_daily_consumption(st.session_state.appliances_data)
            required_kwp, _, _ = calculate_solar_system(total_kwh, selected_city)
            
            st.info(f"""
            **Your System Requirements:**
            - Daily Energy: {total_kwh:.2f} kWh
            - Required Capacity: {required_kwp:.2f} kWp
            - Estimated Budget: ₦{required_kwp * 1000000:,.0f}
            """)
    
    with col2:
        st.subheader(f"Solar Vendors in {selected_city}")
        
        city_vendors = VENDORS.get(selected_city, [])
        
        for vendor in city_vendors:
            if service_type == "All" or vendor['speciality'] == service_type:
                with st.expander(f"⭐ {vendor['name']} - {vendor['rating']}/5.0"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Speciality:** {vendor['speciality']}")
                        st.write(f"**Phone:** {vendor['phone']}")
                    
                    with col2:
                        st.write(f"**Rating:** {'⭐' * int(vendor['rating'])} ({vendor['rating']}/5)")
                        st.write(f"**Location:** {selected_city}")
                    
                    with col3:
                        if st.button(f"Get Quote from {vendor['name']}", key=f"quote_{vendor['name']}"):
                            st.success(f"""
                            Quote request sent to {vendor['name']}!
                            They will contact you at your provided number.
                            
                            **Your Requirements Shared:**
                            - System Size: {required_kwp:.2f} kWp
                            - Daily Energy: {total_kwh:.2f} kWh
                            - Location: {selected_city}
                            """)
        
        # Add new vendor form
        st.subheader("📝 Register Your Solar Business")
        with st.form("vendor_registration"):
            vendor_name = st.text_input("Business Name")
            vendor_phone = st.text_input("Phone Number")
            vendor_speciality = st.selectbox("Speciality", 
                                           ["Residential", "Commercial", "Off-grid Systems", "Hybrid Systems"])
            vendor_city = st.selectbox("City", list(VENDORS.keys()))
            
            if st.form_submit_button("Register Business"):
                st.success(f"""
                Thank you for registering {vendor_name}!
                
                **Registration Details:**
                - Business: {vendor_name}
                - Phone: {vendor_phone}
                - Speciality: {vendor_speciality}
                - City: {vendor_city}
                
                Your business will be reviewed and added to our directory within 24 hours.
                """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>SolarSize Nigeria - Empowering Solar Adoption Across Nigeria</p>
    <p>Contact: amahagodspower@gmail.com | +234 7016323808 |+234-800-SOLAR-NG</p>
</div>
""", unsafe_allow_html=True)
