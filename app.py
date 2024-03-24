import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(layout="wide")

# Read the HTML file into a Python string
with open("index.html", "r") as html_file:
    html_content = html_file.read()

# Embed the HTML code in the Streamlit app
components.html(html_content, height=700)

# Display latitude and longitude received from the HTML component
latitude = st.empty()
longitude = st.empty()

# JavaScript code to send latitude and longitude back to Streamlit
javascript_code = """
<script>
    window.addEventListener("message", (event) => {
        const { latitude, longitude } = event.data;
        if (latitude !== undefined && longitude !== undefined) {
            const latitudeElement = document.getElementById("latitude");
            const longitudeElement = document.getElementById("longitude");
            latitudeElement.innerText = latitude;
            longitudeElement.innerText = longitude;
        }
    });
</script>
"""
st.markdown(javascript_code, unsafe_allow_html=True)

if "latitude" in st.session_state and "longitude" in st.session_state:
    latitude.write(f"Latitude: {st.session_state['latitude']}")
    longitude.write(f"Longitude: {st.session_state['longitude']}")

EMISSION_FACTORS = {
    "North America": {
        "Transportation": 1.85,  # kgCO2/km
        "Electricity": 4.79,  # kgCO2/kWh
        "Diet": 5.0,  # kgCO2/meal, 
        "Waste": 0.1  # kgCO2/kg
    },
    "Europe": {
        "Transportation": 1.1,
        "Electricity": 1.95,
        "Diet": 1.1,
        "Waste": 0.15
    },
    "South America": {
        "Transportation": 0.21,
        "Electricity": 1.2,
        "Diet": 2.1,
        "Waste": 0.2,
    },
    "Asia": {
        "Transportation": 2.6,
        "Electricity": 4.0,
        "Diet": 4.2,
        "Waste": 3.3
    },
    "Africa": {
        "Transportation": 3.46,
        "Electricity":2.43,
        "Diet": 2.57,
        "Waste": 3.1,
    },
    "Antarctica": {
        "Transportation": 4.14,
        "Electricity":.57,
        "Diet": 2.1,
        "Waste": 2.2,
    },
    "Australia": {
        "Transportation": 2.1,
        "Electricity": 1.52,
        "Diet": 2.7,
        "Waste": 3.1,
    }

}


# Streamlit app code
st.title("CARCALC (Carbon Calculator)")

# User inputs
st.subheader("🌍 Please choose your continent")
continent = st.selectbox("Select Continent", ["North America", "Europe", "South America", "Asia", "Africa", "Antarctica", "Australia"])
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛻 distance covered daily (in km)")
    distance =  st.number_input("Distance", 0, key="distance_input")

    st.subheader("⚡ Monthly electricity consumption (in kWh)")
    electricity = st.number_input("Electricity", 0, key="electricity_input")

with col2:
    st.subheader("🗑️ waste created per week (in kg)")
    waste = st.number_input("Waste", 0, key="waste_input")

    st.subheader("🍔 meals cooked per day")
    meals = st.number_input("Meals", 0, key="meals_input")

# Normalize inputs
if distance > 0:
    distance = distance * 365  # Convert daily distance to yearly
if electricity > 0:
    electricity = electricity * 12  # Convert monthly electricity to yearly
if meals > 0:
    meals = meals * 365  # Convert daily meals to yearly
if waste > 0:
    waste = waste * 52  # Convert weekly waste to yearly

# Calculate carbon emissions
country_emissions = EMISSION_FACTORS[continent]
transportation_emissions = country_emissions["Transportation"] * distance
electricity_emissions = country_emissions["Electricity"] * electricity
diet_emissions = country_emissions["Diet"] * meals
waste_emissions = country_emissions["Waste"] * waste

# Convert emissions to tonnes and round off to 2 decimal points
transportation_emissions = round(transportation_emissions / 1000, 2)
electricity_emissions = round(electricity_emissions / 1000, 2)
diet_emissions = round(diet_emissions / 1000, 2)
waste_emissions = round(waste_emissions / 1000, 2)

# Calculate total emissions
total_emissions = round(
    transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
)

if st.button("Calculate CO2 Emissions"):

    # Display results
    st.header("Results")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Carbon Emissions by Category")
        st.info(f"🚗 Transportation: {transportation_emissions} tonnes CO2 per year")
        st.info(f"💡 Electricity: {electricity_emissions} tonnes CO2 per year")
        st.info(f"🍽️ Diet: {diet_emissions} tonnes CO2 per year")
        st.info(f"🗑️ Waste: {waste_emissions} tonnes CO2 per year")

    with col4:
        st.subheader("Total Carbon Footprint")
        st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year")

        if total_emissions >= 4.70:
            st.warning("Your carbon footprint is too high. Try using more energy saving resources in your life")

        else:
            st.warning("Your carbon footpring is below average. Keep it up!!")

        # Warning messages based on continent
        if continent == "North America":
            st.warning("The second most polluting region in 2022 was North America, where 5.9 billion metric tons of CO₂ were emitted.")
        elif continent == "Europe":
            st.warning("In the third quarter of 2023, EU economy greenhouse gas emissions are estimated at 787 million tonnes of CO2-equivalents, a 7.1 % decrease compared with the same quarter of 2022 (847 million tonnes of CO2 equivalents).")
        elif continent == "South America":
            st.warning("In 2023, the CO2 emissions in Latin America and the Caribbean (LAC) were projected to be around 1,660 million tonnes (Mt) in the Stated Policies Scenario (STEPS), and slightly over 1,690 Mt in the Announced Pledges Scenario (APS). The CO2 emissions are expected to increase slightly from 2022 to 2030 in the STEPS scenario, but they are projected to be 200 Mt lower in the APS scenario ")
        elif continent == "Asia":
            st.warning("The Asia-Pacific region produced 17.96 billion metric tons of carbon dioxide emissions in 2022. This was more than the combined total emissions of all other regions that year.")
        elif continent == "Australia":
            st.warning("The total carbon emissions in Australia in 2023 are estimated to be 463 million tonnes of CO2-e, a decrease of 0.1% compared to the previous year.")
        elif continent == "Antarctica":
            st.warning("Antarctica itself doesn't have significant human activity that would generate large-scale carbon emissions like burning fossil fuels.  While research stations do have some emissions, these are negligible compared to global totals. Research based on satellite data indicates that between 2002 and 2023, Antarctica shed an average of 150 billion metric tons of ice per year, adding to global sea level rise.")
        elif continent == "Africa":
            st.warning("Comprising about 17 percent of the world's population, Africa contributes just 4 percent of global carbon emissions at 1.45 billion tonnes")

# Read the CSS file with background image
css_styles = """
<style>
 h1 { color: #7c795d; font-family: 'Trocchi', serif; font-size: 45px; font-weight: normal; line-height: 48px; margin: 0; text-align: center;}
 h2, h3, h4, h5, h6 { color: #7c795d; font-family: 'Trocchi'}
</style>
"""
app_container = st.container()
app_container.markdown(css_styles, unsafe_allow_html=True)
