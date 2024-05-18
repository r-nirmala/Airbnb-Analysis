import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import PIL
from PIL import Image
import warnings
warnings.filterwarnings("ignore")


#streamlit page configuration

st.set_page_config(page_title= "Airbnb Data Visualization",layout= "wide",
                   initial_sidebar_state= "expanded")
st.sidebar.header(":wave: :rainbow[**Welcome to the dashboard!**]")
with st.sidebar:

    selected = option_menu(menu_title="", options=["Home", "Visualization","About"], 
                          icons=['house','bar-chart','exclamation-circle'],
                          styles={  
                             "nav-link": {"font-size": "20px", "text-align": "left", "margin": "-3px", "--hover-color": "grey"},
                            "nav-link-selected": {"background-color": "orange"}}
                              )

#------------------------Home page------------------------------
if selected=='Home':
    
  img = Image.open(r"C:\Users\rnirm\OneDrive\Desktop\image\airbnb_banner.jpg")
  size = (350,85)
  Img = img.resize(size)
  st.image(Img, use_column_width=False)

  st.markdown(f'<h1 style="text-align: center;">Airbnb Analysis</h1>',
              unsafe_allow_html=True)
  
  st.markdown("##### Airbnb, Inc. is an :red[***American San Francisco-based company***] operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking.")
  st.markdown('##### :orange[The company was founded in :green[**2008**] by :green[***Brian Chesky, Nathan Blecharczyk, and Joe Gebbia***]. Airbnb is a shortened version of its original name, :green[***AirBedandBreakfast.com***]]')
  st.markdown('##### The airbnb app allows hosts to list their properties for lease,and enables guests to rent or lease on a short-term basis,which includes vacation rentals, apartment rentals, homestays, castles,tree houses and hotel rooms.')
  st.markdown('##### :blue[Airbnb is headquartered in :orange[***San Francisco, California, the US***.]]')
  st.write('')
  st.write('')
  st.subheader(':red[Skills take away:]')
  st.markdown('##### :green[Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI or Tableau]')
  st.subheader(":violet[**Domain:**] Travel Industry, Property Management and Tourism") 

#--------------------------------Visualisation page-----------------------------

def file():
  df = pd.read_csv(r"E:\Guvi Data Science - MDE86\Guvi Projects\Project 2_4\Airbnb_csv")
  return df

df = file()

if selected == "Visualization":
  tab1, tab2, tab3 = st.tabs(['#### ***Explore listings***','#### ***:red[Price Analysis]***', '#### ***:blue[Availability and Location Analysis]***'])
 
  with tab1:
    cntry = st.selectbox(':green[Select a country]',sorted(df.country.unique()))
    col1,col2 = st.columns(2, gap="medium")
    with col1:  
      query = f"country == '{cntry}' "
      df1 = df.query(query).groupby(["property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)
      fig = px.bar(df1,
                  title='Total Listings of Property Types',
                  x='Listings',
                  y='property_type',
                  orientation='h',
                  color='Listings',height = 500, 
                  color_continuous_scale=px.colors.sequential.Agsunset)
      st.plotly_chart(fig,use_container_width=True) 
    with col2:
      query = f"country == '{cntry}'"
      df2 = df.query(query).groupby(["room_type"]).size().reset_index(name="Listings")
      fig = px.pie(df2,
                  title='Total Listings of Room Types',
                  names='room_type',
                  values='Listings',height = 500,
                  color_discrete_sequence=px.colors.sequential.RdBu)
      fig.update_traces(textposition='inside', textinfo='value+label')
      st.plotly_chart(fig,use_container_width=True)
   
    col3,col4 = st.columns(2, gap="medium")
    with col3:
      query = f"country == '{cntry}'"
      df3 = df.query(query).groupby(['host_name']).size().reset_index(name = 'Listings').sort_values(by = 'Listings', ascending=False)[:10]
      fig = px.bar(df3, 
                    title = "Top 10 hosts with highest number of Listings",
                    x='host_name',
                    y='Listings',
                  orientation='v',
                color='Listings',height = 500,
                color_continuous_scale=px.colors.sequential.RdPu)
      st.plotly_chart(fig,use_container_width=True)  
    with col4:
      df4 = df.groupby(["country"]).size().reset_index(name= "Total_Listings").sort_values(by= "Total_Listings",ascending=False)
      fig = px.choropleth(df4,
                          title='Total Listings in each Country',
                          locations='country',
                          locationmode='country names',
                          color='Total_Listings',height = 700,
                          color_continuous_scale=px.colors.sequential.Plasma)                    
      st.plotly_chart(fig,use_container_width=False)
  with tab2:   
    col1,col2 = st.columns(2,gap='medium')
    with col1:
      cntry = st.selectbox(':blue[Select a country]',sorted(df.country.unique()))
      
      query = f"country == '{cntry}'"
      pr_df = df.query(query).groupby('property_type',as_index=False).agg({'country':'first','price':'mean','number_of_reviews':'sum'})
      fig = px.bar(pr_df, y='property_type', x= "price",
                title= f"Average Price on Property Types for {cntry} ",
            hover_data=["number_of_reviews"],orientation='h',
            color_discrete_sequence=px.colors.sequential.Agsunset_r, width=600, height=700)
      st.plotly_chart(fig,use_container_width=True)

    with col2:
      cntry = st.selectbox(':violet[Select a country]',sorted(df.country.unique()))
      property = st.selectbox(' :violet[Select a property type]',sorted(df.property_type.unique()))
      
      query = f"country=='{cntry}' & property_type=='{property}'"
      ro_df = df.query(query).groupby('room_type',as_index=False).agg({'price':'mean','number_of_reviews':'sum'})
      fig = px.pie(ro_df, values="price", names= "room_type",
                            hover_data=["number_of_reviews"],
                            color_discrete_sequence=px.colors.sequential.BuGn_r,
                            title="Average Price for Room types",
                            width= 600, height= 500)
      fig.update_traces(textposition='inside', textinfo='value+label')
      st.plotly_chart(fig,use_container_width=True)

    cntry = st.selectbox(':orange[Select a country]',sorted(df.country.unique()))
    property = st.selectbox(' :orange[Select a property type]',sorted(df.property_type.unique()))
    room = st.selectbox(' :orange[Select a room type]',sorted(df.room_type.unique()))
   
    col3,col4 = st.columns(2,gap='medium')
   
    with col3:
      query = f"country == '{cntry}' & property_type == '{property}' & room_type =='{room}'"
      h_res = pd.DataFrame(df.query(query).groupby('host_response_time',as_index=False).agg({'price':'mean','accommodates':'sum'}))
      fig = px.pie(h_res, values="price", names= "host_response_time",
                            hover_data=["accommodates"],
                            color_discrete_sequence=px.colors.sequential.BuPu_r,
                            title="Average Price based on Host Response Time",
                            width= 600, height= 500)
      fig.update_traces(textposition='inside', textinfo='value+label')
      st.plotly_chart(fig,use_container_width=True)
    with col4:
      query = f"country == '{cntry}' & property_type == '{property}' & room_type =='{room}'"
      nts = pd.DataFrame(df.query(query).groupby('bed_type').agg({'bed_type':'first','minimum_nights':'sum','maximum_nights':'sum','price':'mean'}))
      fig = px.bar(nts, x='bed_type', y=['minimum_nights', 'maximum_nights'], 
            title='Price for Minimum and Maximum Nights based on bed_type',hover_data="price",
            barmode='group',color_discrete_sequence=px.colors.sequential.Rainbow_r, width=600, height=500)
      st.plotly_chart(fig,use_container_width=True)
    
    query = f"country == '{cntry}' & property_type == '{property}' & room_type =='{room}'"
    country_df = df.query(query).groupby('country',as_index=False)['price'].mean()
    fig = px.scatter_geo(data_frame=country_df,
                                locations='country',
                                color= 'price', height=500,
                                hover_data=['price'],
                                locationmode='country names',
                                size='price',
                                title= 'Avg Price in each Country',
                                color_continuous_scale='agsunset')
    st.plotly_chart(fig, use_container_width=True)
  with tab3:  
    cntry_key = 'country_selectbox'
    prop_key = 'property_type_selectbox'
    room_key = 'room_type_selectbox'

    cntry = st.selectbox(':violet[Select a country]',sorted(df.country.unique()),key=cntry_key)
    prop = st.selectbox(' :green[Select a property type]',sorted(df.property_type.unique()),key=prop_key)
    room = st.selectbox(' :orange[Select a room type]',sorted(df.room_type.unique()),key=room_key)
    
    st.write("")
    st.write('##### :green[Availability based on Host Neighbourhood]')
    
    col1, col2, col3, col4 = st.columns(4,gap='small')
    
    with col1:
      query = f"country == '{cntry}' & property_type == '{prop}' & room_type =='{room}'"
      agg = df.query(query).groupby('host_neighbourhood',as_index=False).agg({'country':'first','room_type':'first','bed_type':'first','availability_30':'sum'})
      rc = agg[agg['host_neighbourhood']!='Not Specified']
      sort = rc.sort_values(by='availability_30',ascending=False)
      avail = sort.head(10)
      
      fig = px.sunburst(avail, path=['room_type','bed_type','host_neighbourhood'], 
            values="availability_30",width=500,height=500,
            title="Availability of next 30 days",
            color_discrete_sequence=px.colors.sequential.Rainbow)
      st.plotly_chart(fig, use_container_width=True)
    
    with col2:
      query = f"country == '{cntry}' & property_type == '{prop}' & room_type =='{room}'"
      agg = df.query(query).groupby('host_neighbourhood',as_index=False).agg({'country':'first','room_type':'first','bed_type':'first','availability_60':'sum'})
      rc = agg[agg['host_neighbourhood']!='Not Specified']
      sort = rc.sort_values(by='availability_60',ascending=False)
      avail = sort.head(10)
      
      fig = px.sunburst(avail, path=['room_type','bed_type','host_neighbourhood'], 
            values="availability_60",width=500,height=500,
            title="Availability of next 60 days",
            color_discrete_sequence=px.colors.sequential.RdBu)
      st.plotly_chart(fig, use_container_width=True)
    
    with col3:
      query = f"country == '{cntry}' & property_type == '{prop}' & room_type =='{room}'"
      agg = df.query(query).groupby('host_neighbourhood',as_index=False).agg({'country':'first','room_type':'first','bed_type':'first','availability_90':'sum'})
      rc = agg[agg['host_neighbourhood']!='Not Specified']
      sort = rc.sort_values(by='availability_90',ascending=False)
      avail = sort.head(10)
      
      fig = px.sunburst(avail, path=['room_type','bed_type','host_neighbourhood'], 
            values="availability_90",width=500,height=500,
            title="Availability of next 90 days",
            color_discrete_sequence=px.colors.sequential.Cividis)
      st.plotly_chart(fig, use_container_width=True)
    
    with col4:
      query = f"country == '{cntry}' & property_type == '{prop}' & room_type =='{room}'"
      agg = df.query(query).groupby('host_neighbourhood',as_index=False).agg({'country':'first','room_type':'first','bed_type':'first','availability_365':'sum'})
      rc = agg[agg['host_neighbourhood']!='Not Specified']
      sort = rc.sort_values(by='availability_365',ascending=False)
      avail = sort.head(10)
      
      fig = px.sunburst(avail, path=['room_type','bed_type','host_neighbourhood'], 
            values="availability_365",width=500,height=500,
            title="Availability of next 365 days",
            color_discrete_sequence=px.colors.sequential.Agsunset)
      st.plotly_chart(fig, use_container_width=True)
    
    
    st.write('##### :green[Box plot Analysis]')
    col1,col2,col3,col4 = st.columns([6.5,6.5,6.5,6.5],gap='small')
    with col1:
      query = f"country == '{cntry}' & property_type == '{prop}' & room_type =='{room}'"
      dat = df.query(query).groupby('room_type',as_index=False).apply(lambda x: x[['country','room_type','availability_30']])
      fig = px.box(data_frame=dat,
                             x='room_type',
                             y=['availability_30'],
                             color='room_type',height=400,width=300,
                             title='Availability_30'
                            )
      st.plotly_chart(fig,use_container_width=False)
    with col2:
      query = f"country == '{cntry}' & property_type == '{prop}' & room_type =='{room}'"
      dat = df.query(query).groupby('room_type',as_index=False).apply(lambda x: x[['country','room_type','availability_60']])
      fig = px.box(data_frame=dat,
                             x='room_type',
                             y=['availability_60'],height=400,width=300,
                             color='room_type',
                             title='Availability_60'
                            )
      st.plotly_chart(fig,use_container_width=False)
    with col3:
      query = f"country == '{cntry}' & property_type == '{prop}' & room_type =='{room}'"
      dat = df.query(query).groupby('room_type',as_index=False).apply(lambda x: x[['country','room_type','availability_90']])
      fig = px.box(data_frame=dat,
                             x='room_type',
                             y=['availability_90'],height=400,width=300,
                             color='room_type',
                             title='Availability_90')
      st.plotly_chart(fig,use_container_width=False)
    with col4:
      query = f"country == '{cntry}' & property_type == '{prop}' & room_type =='{room}'"
      dat = df.query(query).groupby('room_type',as_index=False).apply(lambda x: x[['country','room_type','availability_365']])
      fig = px.box(data_frame=dat,
                             x='room_type',
                             y=['availability_365'],height=400,width=300,
                             color='room_type',
                             title='Availability_365')
      st.plotly_chart(fig,use_container_width=False)

    fig_g = px.scatter_mapbox(df, lat='latitude', lon='longitude', color='accommodates', size='accommodates',
                        color_continuous_scale= "rainbow",hover_data ={'name':True,'host_neighbourhood':True},
                        range_color=(0,49000), mapbox_style="carto-positron",zoom=1)
    fig_g.update_layout(width=900,height=650,title='Geospatial Distribution of Listings using Latitude and Longitude')
    st.plotly_chart(fig_g, use_container_width=True)
    
if selected == 'About':
  st.subheader('About Project')
  st.write('##### :orange[This project helps to analyse and visualize :violet[Airbnb data] to learn more about _pricing variations_, _booking trends_, and _location-based trends_.]')
  st.write("")
  st.write('##### Steps involved in this project:- ')
  st.write("##### -->_:red[Data Collection]_ : :green[From MongoDB Atlas or any other sources]")
  st.write("##### -->_:red[Cleaning and Preprocessing]_ : :green[For handling missing values,duplicates and converting data types]")
  st.write("##### -->_:red[Exploratory Data Analysis]_ :  :green[To understand the distribution and patterns in the data, to explore relationships between variables]")
  st.write("##### -->_:red[Visualization]_ : :green[Use of charts, graphs and maps to get better insights. :violet[Plotly] is used to visualize this data]")
  st.write("")
  st.write("")
  st.subheader(" :rainbow[Thanks for Exploring! Visit Again!]")