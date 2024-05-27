import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px

# Base URL for the Django backend
BASE_URL = 'http://127.0.0.1:8000/sales_app/'
MEDIA_URL = 'http://127.0.0.1:8000/media/'

st.title('Sales Data Management System')
tab1, tab2, tab3 = st.tabs(['Add Sales Record','View Sales Data','Visualize Sales Data'])

# Function to fetch products and regions
def fetch_options(endpoint):
    response = requests.get(BASE_URL + endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Fetch products and regions
products = fetch_options('products/')
regions = fetch_options('regions/')

# Convert to dictionary for easy lookup
product_dict = {product['name']: product['id'] for product in products}
region_dict = {region['name']: region['id'] for region in regions}

# if st.button('Toggle Sidebar Visibility'):
#     st.sidebar.header('Mapping Details')

#     st.sidebar.subheader('Product Mapping')
#     for name, _id in product_dict.items():
#         st.sidebar.write(f"{name}: {_id}")

#     st.sidebar.subheader('Region Mapping')
#     for name, _id in region_dict.items():
#         st.sidebar.write(f"{name}: {_id}")
# def get_key_from_value(dictionary, value):
#     for key, val in dictionary.items():
#         if val == value:
#             return key
#     return None  # If the value is not found in the dictionary
st.sidebar.header('Mapping Details')
st.sidebar.subheader('Product Mapping')
for name, _id in product_dict.items():
    st.sidebar.write(f"{name}: {_id}")

st.sidebar.subheader('Region Mapping')
for name, _id in region_dict.items():
    st.sidebar.write(f"{name}: {_id}")
# Add Sales Record Section
with tab1:
    st.header('Add Sales Record')
    date = st.date_input('Date', value=datetime.now())
    product = st.selectbox('Product', options=list(product_dict.keys()))
    sales_amount = st.number_input('Sales Amount', min_value=0.0, format="%.2f")
    region = st.selectbox('Region', options=list(region_dict.keys()))
    receipt_photo = st.file_uploader('Upload Receipt Photo', type=['png', 'jpg', 'jpeg'])
    use_camera = st.checkbox('Use Camera to Capture Receipt Photo')
    if use_camera:
        camera_photo = st.camera_input('Capture Receipt Photo')
    else:
        camera_photo = None

    if st.button('Add Record'):
        if date and product and sales_amount and region and (receipt_photo or camera_photo):
            # Determine which photo to use
            if receipt_photo:
                receipt_photo_name = receipt_photo.name
                files = {'receipt_photo': (receipt_photo_name, receipt_photo, receipt_photo.type)}
            else:
                receipt_photo_name = "camera_photo.jpg"
                files = {'receipt_photo': (receipt_photo_name, camera_photo, 'image/jpeg')}
            

    # if st.button('Add Record'):
    #     if date and product and sales_amount and region and receipt_photo:
    #         # Ensure receipt photo has a filename
    #         receipt_photo_name = receipt_photo.name
    #         files = {'receipt_photo': (receipt_photo_name, receipt_photo, receipt_photo.type)}
            data = {
                'date': date.strftime('%Y-%m-%d'),
                'product': product_dict[product],
                'sales_amount': int(sales_amount),
                'region': region_dict[region],
            }
            
            # Sending data to Django backend
            response = requests.post(BASE_URL + 'add/', data=data, files=files)

            if response.status_code == 200:
                st.success('Record added successfully!')
            else:
                st.error(f'Failed to add record: {response.json()}')
        else:
            st.error('Please fill in all fields and upload a receipt photo.')

# View Sales Data Section
with tab2:
    st.header('View Sales Data')

    if st.button('Load Data'):
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            sales_data = response.json()

            if sales_data:
                # Create DataFrame and reverse the order
                df = pd.DataFrame(sales_data)
                df = df[::-1]  # Reverse the DataFrame

                df['receipt_link'] = df['receipt_photo'].apply(lambda url: f'<a href="{MEDIA_URL}{url}" target="_blank">View Receipt</a>')
                html_table = df.to_html(escape=False, columns=['date', 'product_id', 'sales_amount', 'region_id', 'receipt_link'])
                
                # Display the HTML table
                st.markdown(html_table, unsafe_allow_html=True)
            else:
                st.warning('No sales data available.')
        else:
            st.error('Failed to load data.')

# Visualize Sales Data Section
with tab3:
    st.header('Visualize Sales Data')

    if st.button('Visualize Data'):
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            sales_data = response.json()

            if sales_data:
                # Create DataFrame and reverse the order
                df = pd.DataFrame(sales_data)
                df = df[::-1]  # Reverse the DataFrame

                # Ensure date is in datetime format for proper grouping
                df['date'] = pd.to_datetime(df['date'])
                df['sales_amount'] = pd.to_numeric(df['sales_amount'], errors='coerce')
                
                # Visualizations
                st.subheader('Sales Amount by Product')
                sales_by_product = df.groupby('product_id')['sales_amount'].sum().reset_index()
                st.bar_chart(sales_by_product.set_index('product_id'))

                st.subheader('Sales Amount by Region')
                sales_by_region = df.groupby('region_id')['sales_amount'].sum().reset_index()
                st.bar_chart(sales_by_region.set_index('region_id'))

                st.subheader('Sales Amount Over Time')
                sales_over_time = df.groupby('date')['sales_amount'].sum().reset_index()
                st.line_chart(sales_over_time.set_index('date'))

                # Pie Chart for Sales Distribution by Product
                st.subheader('Sales Distribution by Product')
                product_sales_distribution = df.groupby('product_id')['sales_amount'].sum().reset_index()
                fig = px.pie(product_sales_distribution, names='product_id', values='sales_amount')
                st.plotly_chart(fig)

                st.subheader('Sales Distribution by Region')
                regional_sales_distribution = df.groupby('region_id')['sales_amount'].sum().reset_index()
                fig = px.pie(regional_sales_distribution, names='region_id', values='sales_amount')
                st.plotly_chart(fig)

                # Histogram for Sales Amount
                # st.subheader('Distribution of Sales Amount')
                # st.hist(df['sales_amount'], bins=20)
            else:
                st.warning('No sales data available.')
        else:
            st.error('Failed to load data.')
# Add a button to toggle sidebar visibility
