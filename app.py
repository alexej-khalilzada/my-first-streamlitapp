###### Import modules
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import geojson
import pandas as pd
import os

######  Define functions
@st.cache # Function decorator to memoize function executions
def load_geojson(path):
    """load_geojson(path)
       loads geojson data from file in 'path'.

    Args:
        path (string): Path to the GeoJSON file

    Returns:
        gj: geojson data frame
    """
    gj = geojson.load(path)
    return gj    

###### Set title and header
st.title("Internet usage per country in percentage")
st.header("Data Exploration")

###### Read Geo JSON data from file
#with open('/Users/alexejkhalilzada/Dokumente/Data_Science/SIT_Learning/repos/Alexej/alexej-khalilzada/03_Visualization/day3-4/my-first-streamlitapp/GeoJSON/countries.geojson') as f:
with open('countries.geojson') as f:
    countries = geojson.load(f)

##### Read dataset from CSV file
# internet_share_df = pd.read_csv('/Users/alexejkhalilzada/Dokumente/Data_Science/SIT_Learning/repos/Alexej/alexej-khalilzada/03_Visualization/day3-4/my-first-streamlitapp/dataset/share-of-individuals-using-the-internet.csv')
internet_share_df = pd.read_csv('share-of-individuals-using-the-internet.csv')

##### Rename column
internet_share_df.rename(columns={'Individuals using the Internet (% of population)':'usage_internet'}, inplace=True)

##### Check if checkbox is selected
if st.checkbox("Show data frame containing raw data"):
    st.subheader("Data set from raw data:")
    st.dataframe(data=internet_share_df)

##### Define columns
# left_column, middle_column, right_column = st.columns([3, 1, 1])
year_column = st.columns([3])

###### Select a year for the visualization
years_sorted = sorted(pd.unique(internet_share_df['Year']))
year_selected = year_column.selectbox("Select Year", years_sorted)

##### Chloropleth map
fig = px.choropleth(internet_share_df[internet_share_df['Year'] == year_selected], 
                    geojson=countries, locations='Code', 
                    color='usage_internet',
                    color_continuous_scale="rainbow",
                    scope='world',
                    featureidkey="properties.ISO_A3",
                    labels={'usage_internet':'Individuals using the Internet in %'},
                    width=800, 
                    height=800
                          )

st.plotly_chart(fig, width=800, height=800)

fig_1 = px.bar(internet_share_df[internet_share_df['Entity'] == 'Zimbabwe'], x="Year", y="usage_internet", title='Overall Internet usage for Zimbabwe') # ZWE == Zimbabwe
fig_2 = px.bar(internet_share_df[internet_share_df['Entity'] == 'Afghanistan'], x="Year", y="usage_internet", title='Overall Internet usage for Afghanistan') # AFG == Afghanistan
fig_3 = px.bar(internet_share_df[internet_share_df['Entity'] == 'Euro area'], x="Year", y="usage_internet", title='Overall Internet usage for the Euro area')

st.plotly_chart(fig_1)
st.plotly_chart(fig_2)
st.plotly_chart(fig_3)
