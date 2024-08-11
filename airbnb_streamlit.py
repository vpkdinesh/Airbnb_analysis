#-------------------------------------------------------------------------#
# Processed data will be used for data visulization using streamlit       #
#-------------------------------------------------------------------------#
# Import all the required components                                      #
#-------------------------------------------------------------------------#
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

#-------------------------------------------------------------------------#
# Define Streamlit page information                                      #
#-------------------------------------------------------------------------#
st.set_page_config(page_title= "Airbnb Data Visualization | By Dinesh P K",
                   page_icon="./media/airbnb_logo.jpg",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by Dinesh P K
                                        Data has been gathered from json files"""}
                  )


#-------------------------------#
# Sidebar                       #
#-------------------------------#
with st.sidebar:
    selected = option_menu("Menu", ["Home","Overview","Explore"], 
                           icons=["house","graph-up-arrow","bar-chart-line"],
                           menu_icon= "menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}}

                          )

#-------------------------------------------------------------------------#
# Read preprocessed csv file as data frame                               #
#-------------------------------------------------------------------------#
df = pd.read_csv("D:/Study/Guvi/MDTM33/Projects/1 03 Airbnb/sample_airbnb.csv")

#-------------------------------#
# Home                          #
#-------------------------------#
if selected == "Home":
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("./media/airbnb.png", width=150)

    st.divider()
    st.write("## :blue[Domain] : Travel Industry, Property Management and Tourism")
    st.divider()
    st.write("## :blue[Technologies used] : Python, Pandas, Plotly, Streamlit")
    st.divider()
    st.write("## :blue[Overview] : To analyze Airbnb data using json file, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
    st.divider()

#-------------------------------#
# Overview                      #
#-------------------------------#
if selected == "Overview":

    #Tab names
    tab1,tab2 =st.tabs(["$\huge 𝄜 DATA $", "$\huge📈 INSIGHTS $"])

    price = st.sidebar.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
    country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property Type',sorted(df.Property_Type.unique()),sorted(df.Property_Type.unique()))
    room = st.sidebar.multiselect('Select Room Type',sorted(df.Room_Type.unique()),sorted(df.Room_Type.unique()))

    query = f'Country in {country} & Room_Type in {room} & Property_Type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    with tab1:
        # DATA FRAME FETCHED FROM CSV FILE
        st.write("Preprocessed data in csv file as Data Frame")
        df1 = df.query(query).reset_index()
        df2 = df1.drop(['index'], axis=1)
        st.write(df2)
        st.write("Total No. of Listings : ", str(df2.shape[0]))

    with tab2:
        # TOP 10 PROPERTY TYPES BAR CHART
        df1 = df.query(query).groupby(["Property_Type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
        fig = px.bar(df1,
                    title='Top 10 Property Types',
                    x='Listings',
                    y='Property_Type',
                    orientation='h',
                    color='Property_Type')
        st.plotly_chart(fig,use_container_width=True) 
        
        # TOP 10 HOSTS BAR CHART
        df2 = df.query(query).groupby(["Host_Name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
        fig = px.bar(df2,
                    title='Top 10 Hosts with Highest number of Listings',
                    x='Listings',
                    y='Host_Name',
                    orientation='h',
                    color='Host_Name')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
    
        # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
        df1 = df.query(query).groupby(["Room_Type"]).size().reset_index(name="counts")
        fig = px.pie(df1,
                    title='Total Listings in each Room_types',
                    names='Room_Type',
                    values='counts',
                    color_discrete_sequence=px.colors.sequential.Aggrnyl
                    )
        fig.update_traces(textposition='outside', textinfo='value+label')
        st.plotly_chart(fig,use_container_width=True)
            
        # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
        country_df = df.query(query).groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name' : 'Total_Listings'})
        fig = px.choropleth(country_df,
                            title='Total Listings in each Country',
                            locations='Country',
                            locationmode='country names',
                            color='Total_Listings',
                            color_continuous_scale=px.colors.sequential.Aggrnyl
                            )
        st.plotly_chart(fig,use_container_width=True)

#-------------------------------#
# Explore                       #
#-------------------------------#
if selected == "Explore":
    st.write("## Explore more about the Airbnb data")
    st.divider()

    # GETTING USER INPUTS
    price = st.sidebar.slider('Select Price Range',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
    country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property Type',sorted(df.Property_Type.unique()),sorted(df.Property_Type.unique()))
    room = st.sidebar.multiselect('Select Room Type',sorted(df.Room_Type.unique()),sorted(df.Room_Type.unique()))

    query = f'Country in {country} & Room_Type in {room} & Property_Type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    col1, col2, col3 = st.columns(3)
    with col2:
        st.write("## Price Analysis")
    
    # AVG PRICE BY ROOM TYPE BARCHART
    pr_df = df.query(query).groupby('Room_Type',as_index=False)['Price'].mean().sort_values(by='Price')
    fig = px.bar(data_frame=pr_df,
                x='Room_Type',
                y='Price',
                color='Price',
                title='Avg Price in each Room type'
                )
    st.plotly_chart(fig,use_container_width=True)

    # AVG PRICE IN COUNTRIES SCATTER GEO
    country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
    fig = px.scatter_geo(data_frame=country_df,
                        locations='Country',
                        color= 'Price', 
                        hover_data=['Price'],
                        locationmode='country names',
                        size='Price',
                        title= 'Avg Price in each Country',
                        color_continuous_scale='Aggrnyl'
                        )
    st.plotly_chart(fig,use_container_width=True)
        
    # BLANK SPACE
    st.markdown("#   ")
    st.divider()
    st.markdown("#   ")

    col1, col2, col3 = st.columns(3)
    with col2:
        st.write("## Availablity Analysis")

    # AVAILABILITY BY ROOM TYPE BOX PLOT
    fig = px.box(data_frame=df.query(query),
                x='Room_Type',
                y='Availability_365',
                color='Room_Type',
                title='Availability by Room_type'
                )
    st.plotly_chart(fig,use_container_width=True)
        
    # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
    country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
    country_df.Availability_365 = country_df.Availability_365.astype(int)
    fig = px.scatter_geo(data_frame=country_df,
                        locations='Country',
                        color= 'Availability_365', 
                        hover_data=['Availability_365'],
                        locationmode='country names',
                        size='Availability_365',
                        title= 'Avg Availability in each Country',
                        color_continuous_scale='Aggrnyl'
                        )
    st.plotly_chart(fig,use_container_width=True)
    st.divider()