import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from IPython.display import display
from streamlit_folium import folium_static

# Load data
st.set_page_config(page_title="Bike_Store🚴‍", page_icon="bike-store-high-resolution-logo-transparent.png", layout="wide")
df = pd.read_csv('sales_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Title

#Sidebar
image_path = 'bike-store-high-resolution-logo-transparent.png'
image = st.sidebar.image(image_path, use_column_width=True)

page = st.sidebar.selectbox("Choose a page", ["Home", "Data Overview","Customer Age Analysis","Geographical Analysis 1","Geographical Analysis 2","Geographical Analysis 3","Order Quantity Analysis 1","Order Quantity Analysis 2"
    ,"Order Quantity Analysis 3","Sales Analysis"])
 #Page 1
if page == "Home":
    st.title("*Streamlit Dashboard Demo*")
    st.header("*Introduction to Global Bike Store Sales Dataset*")
    st.snow()    

# Introduction
    st.markdown(""" *Welcome to the rich and diverse world of global bike store sales data! This dataset provides a comprehensive glimpse into the dynamics of bike sales across various countries, offering valuable insights into customer behaviors, sales trends, and regional preferences. Spanning the years 2011 to 2016, the dataset encompasses a treasure trove of information, including customer demographics, order quantities, sales revenue, and more.*

""")

    if st.button("*Let the exploration begin! 🚴‍♂️🌎📊*"):
    # Move to the next page
     show_page = ("Data Overview")
# Insert a chat message container.

# Set your OpenAI API key
    

elif page == "Data Overview":
    st.title("*Data Random Sample*")
    st.markdown("""*This app provides insights into customer data, allowing you to explore various aspects of customer transactions.*  
***Click here to show a random sample of the dataset.***""")
            
    btn=st.button("Show Data")
    if btn:
       st.dataframe(df.sample(5))
    
    st.title("*Dashboard Summary*")

    def styled_metric_table(labels, values, bg_color, text_color='black', font_size='1em'):
        styled_text = "<div style='display: flex;'>"

        for label, value in zip(labels, values):
            metric_card = f"<div style='flex: 1; margin: 10px; background-color: {bg_color}; padding: 10px; border-radius: 5px; text-align: center;'><span style='color: {text_color}; font-size: {font_size};'><b>{label}:</b></span><br><span style='color: {text_color}; font-size: {font_size};'>{value}</span></div>"
            styled_text += metric_card

        styled_text += "</div>"
        st.markdown(styled_text, unsafe_allow_html=True)


# 1. Total Number Of Countries
    total_countries = df['Country'].nunique()

# 2. Total Count Of Products
    total_products = df['Product'].nunique()

# 3. Total Sum Of Revenue
    total_revenue = df['Revenue'].sum()
    total_revenue = df['Revenue'].sum()
    total_revenue_in_millions = total_revenue / 1_000_000
    total_revenue_in_thousands = total_revenue / 1_000
    
# 4. Total Sum Of Profit
    total_profit = df['Profit'].sum()


# Total Sum Of Profit in millions and K
    total_profit = df['Profit'].sum()
    total_profit_in_millions = total_profit / 1_000_000
    total_profit_in_thousands = total_profit / 1_000

# 5. Total Count Of Orders
    total_orders = df.shape[0] / 1_000

# Assuming df is defined somewhere in your code
# Example usage
    labels = ["Total Number Of Countries", "Total Count Of Products", "Total Sum Of Revenue", "Total Sum Of Profit", "Total Count Of Orders"]
    values = [total_countries, total_products, f"{total_revenue_in_millions:.2f}M", f"{total_profit_in_millions:.2f}M", f"{total_orders:.2f}K"]

    styled_metric_table(labels, values, '#F0F1F2', 'black')
       
    
   
# Streamlit App
    st.title('*Sales Analysis per Year*')
    st.markdown("""*Tthe line plot shows the store sales for a six-year period. in 2016, the sales decreased dramatically .more digging will be needed to know the root cause for that fall.*""")

    df['Calculated_Date'] = df[['Year', 'Month', 'Day']].apply(lambda x: '{}-{}-{}'.format(x[0], x[1], x[2]), axis=1)
    df['Year'] = df['Year'].astype(str)
    #df['Month'] = df['Month'].astype(str)
    #df['Day'] = df['Day'].astype(str)
    df['Calculated_Date'] = pd.to_datetime(df['Calculated_Date'])
    
# Convert 'Year' column to string
    # Streamlit App
    #st.title('Sales Analysis per Year')

# Convert 'Year' column to string
   # df['Year'] = df['Year'].astype(str)

# Convert 'Your_Date_Column_Name' to datetime
   
    #df['Calculated_Date'] = pd.to_datetime(df['Calculated_Date'])

# Display the calculated date
    #st.subheader('Calculated Dates:')
    #st.write(df[['Calculated_Date']].head())
  

# Group by 'Your_Date_Column_Name' and calculate the count of sales
    sales_count_per_date = df.groupby('Calculated_Date')['Product'].count().reset_index()

# Display the sales count per date
   # st.subheader('Sales Count per Date:')
  #  st.write(sales_count_per_date)

# Plotting with Plotly
    fig = px.line(df.groupby(df['Calculated_Date'].dt.year)['Revenue'].sum().reset_index(),
              x='Calculated_Date', y='Revenue',
              labels={'Revenue': 'Sales', 'Calculated_Date': 'Year'},
              title='Sales per Year')

# Streamlit Display
    st.plotly_chart(fig)


# Page 3

elif page == "Customer Age Analysis":
    st.title("*Customer Age Analysis*")
    st.write("*Explore the age distribution of customers.*")

    
# Assuming df is your DataFrame

    
    # Create a KDE (Kernel Density Estimate) plot using Plotly Express (histogram)

    st.subheader("*Kernel Density Estimate (KDE) Plot for Customer Age:*")
    st.markdown("""*The plot indicates the distribution of ages, with a higher density of customers having ages around 35 and a lower density having ages around 17 and 65. The plot shows that the majority of customers have ages between 28 and 43, with a slight right skew, indicating a longer tail towards older ages. The minimum customer age is 17, and the maximum is 87. The lower and upper fences are at 17 and 65, respectively, and the interquartile range (IQR) is between 28 and 43.*""")
# Check if the DataFrame is not empty
    if not df.empty:
    # Create a KDE (Kernel Density Estimate) plot using Plotly Express
        fig = px.histogram(df, x='Customer_Age', marginal='box', 
                       title='Kernel Density Estimate (KDE) Plot for Customer Age',
                       labels={'Customer_Age': 'Customer Age'},
                       template='plotly', color_discrete_sequence=['lightblue'])

    # Add vertical lines for mean and median
        mean_line = df['Customer_Age'].mean()
        median_line = df['Customer_Age'].median()

        fig.add_shape(type='line', x0=mean_line, x1=mean_line,
                  y0=0, y1=1, line=dict(color='red', width=2), 
                  xref='x', yref='paper')

        fig.add_shape(type='line', x0=median_line, x1=median_line,
                  y0=0, y1=1, line=dict(color='green', width=2), 
                  xref='x', yref='paper')

    # Show the plot in Streamlit
        st.plotly_chart(fig)
    else:
        st.warning("The DataFrame is empty.")
        
    # Streamlit App
    st.title('*Customer Age Analysis per Country*')
    st.markdown("""*This is a grouped box plot displaying the distribution of customer ages for different countries. The box plot for each country shows the median age (horizontal line inside the box), the upper and lower quartiles (the box), and the range of ages (outliers). The countries included in this plot are Canada, Australia, United States, Germany, France, and United Kingdom. Overall, this plot provides a visual comparison of the age distribution of customers across different countries.*""")
# Create a grouped box plot with Plotly
    fig = px.box(df, x='Country', y='Customer_Age', color='Country',
             title='Grouped Box Plot: Customer Age per Country',
             labels={'Customer_Age': 'Customer Age'})
    fig.update_layout(xaxis_title='Country', yaxis_title='Customer Age')

# Streamlit Display
    st.plotly_chart(fig)

elif page == "Geographical Analysis 1":
     st.title('*Bike Store Sales Geographical Distribution*')
     st.markdown("""*This interactive map shows the geographical distribution of our bike store sales worldwide. Each point on the map represents a location where bike sales have been recorded. The size of the point corresponds to the revenue generated at that location, with larger points indicating higher revenue.*

*By hovering over each point, viewers can see specific details about each location, including the revenue, profit, expenses, and order quantity. The map includes locations in countries such as the United States , Canada , United Kingdom, France, Germany and Australia and states in these countries*""")
     country_coordinates = {
        'Australia': [-25.2744, 133.7751],
        'Canada': [56.1304, -106.3468],
        'France': [46.6035, 1.888334],
        'Germany': [51.1657, 10.4515],
        'United Kingdom': [55.3781, -3.4360],
        'United States': [37.0902, -95.7129]
     }
     state_coordinates = {
    'Alabama': [32.806671, -86.791130],
    'Alberta': [53.9333, -116.5765],
    'Arizona': [33.7298, -111.4312],
    'Bayern': [48.7904, 11.4979],
    'Brandenburg': [52.3001, 12.6159],
    'British Columbia': [53.7267, -127.6476],
    'California': [36.7783, -119.4179],
    'Charente-Maritime': [45.7500, -0.9994],
    'England': [52.3555, -1.1743],
    'Essonne': [48.4487, 2.3195],
    'Florida': [27.9944, -81.7603],
    'Garonne (Haute)': [43.6465, 0.8858],
    'Georgia': [32.1574, -82.9071],
    'Hamburg': [53.5511, 9.9937],
    'Hauts de Seine': [48.8566, 2.3522],
    'Hessen': [51.1657, 9.6216],
    'Illinois': [40.3495, -88.9861],
    'Kentucky': [37.6681, -84.6701],
    'Loir et Cher': [47.4037, 1.3972],
    'Loiret': [47.9794, 2.2519],
    'Massachusetts': [42.4072, -71.3824],
    'Minnesota': [46.7296, -94.6859],
    'Mississippi': [32.7416, -89.6787],
    'Missouri': [38.4561, -92.2884],
    'Montana': [46.9219, -110.4544],
    'Moselle': [49.1193, 6.1727],
    'New South Wales': [-31.8402, 145.6128],
    'New York': [40.7128, -74.0060],
    'Nord': [50.6927, 3.1751],
    'Nordrhein-Westfalen': [51.4332, 7.6616],
    'North Carolina': [35.7596, -79.0193],
    'Ohio': [40.4173, -82.9071],
    'Ontario': [51.2538, -85.3232],
    'Oregon': [43.8041, -120.5542],
    'Pas de Calais': [50.5879, 2.9522],
    'Queensland': [-20.9176, 142.7028],
    'Saarland': [49.3964, 7.0229],
    'Seine (Paris)': [48.8566, 2.3522],
    'Seine et Marne': [48.8414, 2.8128],
    'Seine Saint Denis': [48.9382, 2.3801],
    'Somme': [49.9762, 2.5375],
    'South Australia': [-30.0002, 136.2092],
    'South Carolina': [33.8361, -81.1637],
    'Tasmania': [-41.4545, 145.9707],
    'Texas': [31.9686, -99.9018],
    'Utah': [39.3200, -111.0937],
    'Val de Marne': [48.7904, 2.4068],
    'Val d\'Oise': [49.0720, 2.1445],
    'Victoria': [-36.7789, 144.6970],
    'Virginia': [37.4316, -78.6569],
    'Washington': [47.7511, -120.7401],
    'Wyoming': [43.0750, -107.2903],
    'Yveline': [48.7718, 1.9659]
     }
# Create a base map centered at a location
     mymap = folium.Map(location=[48.8566, 2.3522], zoom_start=2)

# Create a MarkerCluster to handle overlapping markers
     marker_cluster = MarkerCluster().add_to(mymap)

# Function to format currency values in the popup
     def format_currency(value, color):
         return f'<span style="color: {color}; font-weight: bold;">${value:,.0f}</span>'

# Add markers for countries with profit information
     for country, coordinates in country_coordinates.items():
         country_data = df[df['Country'] == country]
         country_profit = country_data['Profit'].sum()
         country_revenue = country_data['Revenue'].sum()
         country_expenses = country_data['Cost'].sum()
         country_Order_Quantity=country_data['Order_Quantity'].sum()

    # Enhanced popup content with larger font size and styling
         popup_content = f"""
    <div style="font-size: 16px; padding: 10px; background-color: white; border-radius: 5px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
        <strong>{country}</strong><br>
        Revenue: {format_currency(country_revenue, 'blue')}<br>
        Profit: {format_currency(country_profit, 'green')}<br>
        Expenses: {format_currency(country_expenses, 'red')}<br>
        Order_Quantity:{(country_Order_Quantity)}<br>
    </div>
    """

         folium.Marker(location=coordinates,
                       popup=folium.Popup(popup_content, max_width=300),
                       icon=folium.Icon(color='blue')).add_to(marker_cluster)

# Add markers for states with profit information
     for state, coordinates in state_coordinates.items():
         state_data = df[df['State'] == state]
         state_profit = state_data['Profit'].sum()
         state_revenue = state_data['Revenue'].sum()
         state_expenses = state_data['Cost'].sum()
         state_Order_Quantity=state_data['Order_Quantity'].sum()

    # Enhanced popup content with larger font size and styling
         popup_content = f"""
    <div style="font-size: 16px; padding: 10px; background-color: white; border-radius: 5px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
        <strong>{state}</strong><br>
        Revenue: {format_currency(state_revenue, 'blue')}<br>
        Profit: {format_currency(state_profit, 'green')}<br>
        Expenses: {format_currency(state_expenses, 'red')}<br>
        Order_Quantity:{(state_Order_Quantity)}<br>
    </div>
    """

         folium.Marker(location=coordinates,
                       popup=folium.Popup(popup_content, max_width=300),
                       icon=folium.Icon(color='green')).add_to(marker_cluster)

# Display the map in the Jupyter Notebook
     folium_static(mymap)
# Finally, run the Streamlit app
# Save this script in a file named 'app.py' and run the following command in the terminal:
# streamlit run app.py
elif page == "Geographical Analysis 2":
    
    st.title('*Profit Analysis per Country*')
    st.markdown("""*This interactive map showcases the total profit for six countries, United states have the highest profit which is 11.07364 million dollars.*""")

# Profit per Country
    Profit_per_country = df.groupby('Country')['Profit'].sum().reset_index()
    Profit_per_country = Profit_per_country.sort_values('Profit', ascending=True)

# Display Profit per Country
    st.write(Profit_per_country)
  
# Plotting with Plotly Map
    fig = px.choropleth(Profit_per_country,
                         locations='Country',
                         locationmode='country names',
                         color='Profit',
                         color_continuous_scale='Blues',
                         title='Profit per Country Map',
                         labels={'Profit': 'Total Profit'})

# Streamlit Display
    st.plotly_chart(fig)


# Assuming df is your DataFrame with columns 'Country', 'Profit', and 'Customer_gender'
# Make sure to load your data or replace df with your actual DataFrame

# Streamlit App
    st.title('*Profit Analysis per Country and Customer Gender*')
    st.markdown("""*This interactive maps appear to be a profit analysis comparing data from selected countries and customer genders. The countries selected are Canada, Australia, United States, Germany, and France. The customer genders selected are (M) and female (F). The analysis includes a profit per country map, which compares the total profit for each country gender. the total profits seem to be almost equal between both genders with a slightly skew to the males.*""")
# Multiselect for filtering countries
    selected_countries = st.multiselect('Select Countries', df['Country'].unique(), df['Country'].unique())

# Multiselect for filtering customer gender
    selected_gender = st.multiselect('Select Customer Gender', df['Customer_Gender'].unique(), df['Customer_Gender'].unique())

# Filter DataFrame based on selected countries and customer gender
    filtered_df = df[(df['Country'].isin(selected_countries)) & (df['Customer_Gender'].isin(selected_gender))]

# Profit per Country
    Profit_per_country = filtered_df.groupby(['Country', 'Customer_Gender'])['Profit'].sum().reset_index()
    Profit_per_country = Profit_per_country.sort_values('Profit', ascending=True)

# Display Profit per Country and Customer Gender
    
# Plotting with Plotly Map
    fig = px.choropleth(Profit_per_country,
                    locations='Country',
                    locationmode='country names',
                    color='Profit',
                    color_continuous_scale='Blues',
                    title='Profit per Country Map',
                    labels={'Profit': 'Total Profit'},
                    facet_col='Customer_Gender')  # Use 'Customer_gender' instead of 'Customer_Gender'

# Streamlit Display
    st.plotly_chart(fig)
    
elif page == "Geographical Analysis 3":
# Streamlit App
     st.title('*Profit Analysis per Country*')
     st.markdown("""*In this box plot, we can see that the United States has the highest median profit, followed by the United Kingdom, Germany, Canada, and Australia. France has the lowest median profit. The United States also has the widest IQR(interquartile range), indicating a larger spread of profits compared to the other countries. Canada and Australia have several outliers, which are points above the upper whisker, indicating that some profits in these countries are significantly higher than the majority of profits. France and Germany have no outliers. The United Kingdom has one outlier, which is a profit significantly lower than the majority of profits.*""")
# Box Plotting with Plotly
     fig = px.box(df, x='Country', y='Profit', color='Country', points='all',
             title='Profit per Country Box Plot', labels={'Profit': 'Profit'})
     fig.update_traces(marker=dict(color='blue'))
     fig.update_layout(xaxis_title='Country', yaxis_title='Profit')

# Streamlit Display
     st.plotly_chart(fig)    

elif page == "Order Quantity Analysis 1":
     st.title("*Order Quantity Analysis*")
     st.markdown("""*This bar plot compares the number of orders from six different countries: United States, United Kingdom, Germany, France, Canada, and Australia. The height of each bar represents the count of orders for each country. The United States has the highest number of orders with 39.206K, followed by Australia with 23.936 K and the United Kingdom with 13.62K orders.  and Canada have 14.178K orders each. Germany and France came with the least number of orders 11.098K and  10.998K repectively.*""")

     orders_per_Country = df.groupby(['Country'])['Product'].count().reset_index()

# Sort the DataFrame in descending order based on the 'Product' count
     orders_per_Country_descending = orders_per_Country.sort_values(by='Country', ascending=False)

    
     
# Bar plot with Plotly Express
     fig = px.bar(orders_per_Country_descending , x='Country', y='Product', color='Country',
               labels={'Product': 'Count of Orders'},
               title='Orders Per Each Country')

# Streamlit Display
     st.plotly_chart(fig)
# Group by 'Country' & 'State' and calculate the count of 'Product'

     orders_per_state = df.groupby(['Country', 'State'])['Product'].count().reset_index()

# Sort the DataFrame in descending order based on the 'Product' count
     orders_per_state_descending = orders_per_state.sort_values(by='Country', ascending=False)



# Display the result in Streamlit
     #st.write(orders_per_state_descending)

# Filter rows where 'Country' is 'France' and sort the values
     filtered_orders_france = orders_per_state_descending[orders_per_state_descending['Country'] == 'France'].sort_values(by='Product', ascending=False)

# Display the result in Streamlit
     var=(filtered_orders_france)
    
     st.markdown("""*This bar plot represents the number of orders  for each state in France. The states are arranged in descending order. height of each bar corresponds to the number of orders for that state. For example, the state "paris" has the highest number of orders at around 2300, while "Loir et Cher" and "Pas de Calais" have the lowest number of orders at around 100.*""")
# Bar plot with Plotly Express
     fig = px.bar(var, x='State', y='Product', color='State',
               labels={'Product': 'Count of Orders'},
               title='Orders Per Each State in France Using a Bar Plot')

# Streamlit Display
     st.plotly_chart(fig)

elif page == "Order Quantity Analysis 2":
     
    
    orders_per_subcategory = df.groupby(['Product_Category', 'Sub_Category'])['Product'].count().reset_index()

# Sort the DataFrame in descending order based on the 'Product' count
    orders_per_subcategory_descending = orders_per_subcategory.sort_values(by='Product', ascending=False)

# Streamlit App
    st.title('*Orders Per Sub-Category Analysis for All Categories*')

# Display the result in Streamlit
    st.markdown("""*The bar plot shows the number of orders for each sub-category. The number of orders ranges from 0 to 35,000. The sub-categories with the most orders are Tire and tubes, while the sub-categories with the fewest orders are Bike Racks and Bike Stands.*""")
# Bar plot with Plotly Express
    fig = px.bar(orders_per_subcategory_descending, x='Sub_Category', y='Product', color='Sub_Category',
             labels={'Product': 'Count of Orders'},
             title='Orders Per Each Sub-Category For All Categories Using a Bar Plot')

# Streamlit Display
    st.plotly_chart(fig)
    
    
    
# Group by 'Product_Category' & 'Sub_Category' and calculate the count of 'Product'
    orders_per_subcategory = df.groupby(['Product_Category', 'Sub_Category'])['Product'].count().reset_index()

# Sort the DataFrame in descending order based on the 'Product' count
    orders_per_subcategory_descending = orders_per_subcategory.sort_values(by='Product_Category', ascending=False)

# Steamlit App
    st.title('*Orders Per Sub-Category Analysis for Accessories Category*')

# Display the result in Streamlit
    st.markdown("""*The bar plot shows the number of orders for each sub-category in Accessories Category . The number of orders ranges from around 450 to 34,000. The sub-categories with the most orders are Tire and tubes, while the sub-categories with the fewest orders are Bike Racks and Bike Stands.*""")
# Filter rows where 'Product_Category' is 'Accessories' and sort the values
    filtered_orders_accessories = orders_per_subcategory_descending[orders_per_subcategory_descending['Product_Category'] == 'Accessories'].sort_values(by='Product', ascending=False)

# Display the result in Streamlit
    
# Bar plot with Plotly Express
    fig = px.bar(filtered_orders_accessories, x='Sub_Category', y='Product', color='Sub_Category',
               labels={'Product': 'Count of Orders'},
               title='Orders Per Each Sub-Category For Accessories Category Using a Bar Plot')

# Streamlit Display
    st.plotly_chart(fig)

# Filter rows where 'Product_Category' is 'Bikes' and sort the values
    filtered_orders_bikes = orders_per_subcategory_descending[orders_per_subcategory_descending['Product_Category'] == 'Bikes'].sort_values(by='Product', ascending=False)

# Streamlit App
    st.title('*Orders Per Sub-Category Analysis for Bikes Category*')
    st.markdown("""*The pie chart shows the number of orders for each sub-category in Bikes Category . The number of orders ranges from around 3000 to 13400. The sub-categories with the most orders are Roud Bikes , while the sub-category with the fewest order is Touring Bikes.*""")
# Display the result in Streamlit
     
# Pie plot with Plotly Express
    fig = px.pie(filtered_orders_bikes, values='Product', names='Sub_Category',
               title='Total Orders Per Bike Subcategory',
               labels={'Product': 'Count of Orders'},
               hole=0.3)

# Streamlit Display
    st.plotly_chart(fig)
     
elif page == "Order Quantity Analysis 3":
   
# Order Quantity per Country and State
    order_quantity_per_location = df.groupby(['Country', 'State'])['Order_Quantity'].sum().reset_index()
    order_quantity_per_location = order_quantity_per_location.sort_values('Order_Quantity', ascending=True)

# Display Order Quantity per Country and State
    var=(order_quantity_per_location)

#Streamlit App (Box Plotting with Plotly)
    st.title('*Order Quantity Analysis per Country*')

    fig_box = px.box(df, x='Country', y='Order_Quantity', color='Country', points='all',
                     title='Order Quantity per Country Box Plot', labels={'Order_Quantity': 'Order Quantity'})
    fig_box.update_traces(marker=dict(color='blue'))
    fig_box.update_layout(xaxis_title='Country', yaxis_title='Order Quantity')

# Streamlit Display
    st.plotly_chart(fig_box)

elif page == "Sales Analysis":
    st.title("Sales Analysis")
    

# Group by Year and sum the Revenue
    sales_by_year = df.groupby('Year')['Revenue'].sum().reset_index()

# Create a pie chart using Plotly Express
    fig = px.pie(sales_by_year, values='Revenue', names='Year', title='Sales by Year', 
             labels={'Revenue': 'Revenue', 'Year': 'Year'}, 
             template='plotly', hole=0.3, 
             color_discrete_sequence=px.colors.sequential.Blues[::-1])
    st.plotly_chart(fig)
    
# Sales by Month Bar Plot
    st.subheader("Sales by Month:")
    sales_by_month = df.groupby('Month')['Revenue'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(sales_by_month['Month'], sales_by_month['Revenue'], color='skyblue')
    ax.set_ylabel('Sales')
    ax.set_xlabel('Month')
    ax.set_title('Sales Per Month Using a Bar Plot')
    ax.set_xticks(sales_by_month['Month'])
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.plotly_chart(fig)
    


# Assuming df is your DataFrame with columns 'Country' and 'Revenue'
# Make sure to load your data or replace df with your actual DataFrame


# Sales per Country
    sales_per_country = df.groupby('Country')['Revenue'].sum().reset_index()
    sales_per_country = sales_per_country.sort_values('Revenue', ascending=True)

# Plotting with Plotly
    fig = px.bar(sales_per_country, x='Country', y='Revenue', color='Revenue', color_continuous_scale='Blues', labels={'Revenue': 'Sales'})
    fig.update_layout(title='Sales per Country', xaxis_title='Country', yaxis_title='Sales')

# Streamlit Display
    st.plotly_chart(fig)


# Display unique products


# Sales per Product
    st.title('Product Sales Analysis')
# Sales per Product
    sales_per_product = df.groupby('Product')['Revenue'].sum().reset_index()
    sales_per_product = sales_per_product.sort_values('Revenue', ascending=True)
    top_10_sold_products = sales_per_product.head(10)
    
# Display top 10 sold products
    st.write(top_10_sold_products)

# Plotting with Plotly
    fig = px.bar(top_10_sold_products, x='Product', y='Revenue', color='Revenue', labels={'Revenue': 'Sales'})
    fig.update_layout(title='Top 10 Sold Products', xaxis_title='Product', yaxis_title='Sales', xaxis_tickangle=-45)

# Streamlit Display
    st.plotly_chart(fig)
# Assuming df is your DataFrame with columns 'Unit_Cost' and 'Unit_Price'
# Make sure to load your data or replace df with your actual DataFrame
    st.subheader("Relations")
# Streamlit App
    st.title('Scatter Plot: Unit_Cost vs. Unit_Price')

# Plotting with Plotly
    fig = px.scatter(df, x='Unit_Cost', y='Unit_Price', color=df.index, title='Scatter Plot: Unit_Cost vs. Unit_Price', labels={'Unit_Cost': 'Unit Cost', 'Unit_Price': 'Unit Price'})
    fig.update_traces(marker=dict(color='blue', symbol='circle'))

# Streamlit Display
    st.plotly_chart(fig)
    
# Assuming df is your DataFrame with columns 'Order_Quantity' and 'Profit'
# Make sure to load your data or replace df with your actual DataFrame

# Streamlit App
    st.title('Scatter Plot: Order_Quantity vs. Profit')
    st.markdown("*We found:*\n"
            "*- Outliers, but after digging, the reason is the (Touring-1000-yellow 50).*\n"
            "*- Order_Quantity below 5 is the highest profit!*\n")
# Plotting with Plotly
    fig = px.scatter(df, x='Order_Quantity', y='Profit', title='Scatter Plot: Order_Quantity vs. Profit', labels={'Order_Quantity': 'Order Quantity', 'Profit': 'Profit'})
    fig.update_traces(marker=dict(symbol='x', size=10, color='blue'))

# Streamlit Display
    st.plotly_chart(fig)    
    
   # Assuming df is your DataFrame
# Make sure to load your data or replace df with your actual DataFrame

# Streamlit App
    st.title('Revenue and Revenue Adjustment Analysis per Year')

# Adding Revenue Adjustment column
    df['Revenue_Adjustment'] = df['Revenue'] + 50

# Group by 'Year' and calculate the sum of 'Revenue' and 'Revenue_Adjustment'
    revenue_per_year = df.groupby('Year')[['Revenue', 'Revenue_Adjustment']].sum().reset_index()

# Print or display the result
    st.subheader('Revenue per Year:')
    st.write(revenue_per_year)

# Plotting with Plotly
    fig = px.bar(revenue_per_year, x='Year', y=['Revenue', 'Revenue_Adjustment'],
             labels={'value': 'Total Revenue', 'variable': 'Metric'},
             title='Revenue & Revenue Adjustment Per Year Using a Bar Plot',
             color_discrete_map={'Revenue': 'skyblue', 'Revenue_Adjustment': 'orange'})

# Streamlit Display
    st.plotly_chart(fig) 
    
# Group by 'Customer_Gender' and calculate the sum of 'Revenue'
    sales_per_gender = df.groupby('Customer_Gender')['Revenue'].sum().reset_index()

# Sort the DataFrame in descending order based on the 'Revenue'
    sales_per_gender_descending = sales_per_gender.sort_values(by='Revenue', ascending=False)

# Plot Pie Chart using Plotly Express
    fig = px.pie(sales_per_gender_descending, values='Revenue', names='Customer_Gender', title='Sales Comparison by Gender')

# Display the Pie Chart in Streamlit app
    st.plotly_chart(fig)



# Group by 'Product_Category' and calculate the sum of 'Sales'
    sales_per_category = df.groupby('Product_Category')['Revenue'].sum().reset_index()

# Sort the DataFrame in descending order based on the 'Sales'
    sales_per_category_descending = sales_per_category.sort_values(by='Revenue', ascending=False)

# Streamlit App
    st.title('Sales Analysis Per Category')

# Display the result in Streamlit
    st.write(sales_per_category_descending)

# Pie plot with Plotly Express
    fig = px.pie(sales_per_category_descending, values='Revenue', names='Product_Category',
             title='Total Sales Per Category',
             labels={'Revenue': 'Total Revenue'},
             hole=0.3)

# Streamlit Display
    st.plotly_chart(fig)


# Sort the DataFrame in descending order based on 'Revenue' and get the top 5
    top_5_sales = df.sort_values('Revenue', ascending=False).head(5)

# Streamlit App
    st.title('Top-5 Sales with the Highest Revenue')

# Display the result in Streamlit
    st.write(top_5_sales)
    
# Find the sale with the highest revenue
    highest_revenue_sale = df[df['Revenue'] == df['Revenue'].max()]

# Streamlit App
    st.title('Highest Revenue Sale')

# Display the result in Streamlit
    st.write(highest_revenue_sale)

