import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(
    page_title="Hello Book",
    page_icon="😸"
)

# Display Title and Description
st.title("Inventory Portal v1.0.1")
st.markdown("Enter the details of the stationary cart.")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Vendors", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

# List of Business Types and Products
BUSINESS_TYPES = [
    "Manufacturer",
    "Distributor",
    "Wholesaler",
    "Retailer",
    "Service Provider",
]
PRODUCTS = [
    "Electronics",
    "Apparel",
    "Groceries",
    "Software",
    "Other",
]

DEPARTMENT = [
    "IT",
    "Finance",
    "HR",
    "Security"
]

# Onboarding New Vendor Form
with st.form(key="vendor_form"):
    employee_name = st.text_input(label="Employee Name*")

    department = st.selectbox(
        "Department*", options=DEPARTMENT, index=None)

    business_type = st.selectbox(
        "Business Type*", options=BUSINESS_TYPES, index=None)
    products = st.multiselect("Products Offered", options=PRODUCTS)
    years_in_business = st.slider("Years in Business", 0, 50, 5)
    onboarding_date = st.date_input(label="Onboarding Date")
    additional_info = st.text_area(label="Additional Notes")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit Vendor Details")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not employee_name or not business_type:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        # elif existing_data["EmployeeName"].str.contains(employee_name).any():
        #    st.warning("A vendor with this company name already exists.")
        #    st.stop()
        else:
            # Create a new row of vendor data
            vendor_data = pd.DataFrame(
                [
                    {
                        "EmployeeName": employee_name,
                        "BusinessType": business_type,
                        "Products": ", ".join(products),
                        "YearsInBusiness": years_in_business,
                        "OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
                        "AdditionalInfo": additional_info,
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat(
                [existing_data, vendor_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="Vendors", data=updated_df)

            st.success("Vendor details successfully submitted!")
