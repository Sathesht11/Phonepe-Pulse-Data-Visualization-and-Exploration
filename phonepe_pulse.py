
import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector as msql
from mysql.connector import Error
import plotly.express as px
import geopandas as gpd


# ----------------------------------MySQl server connection--------------------------------------------

try:
    conn = msql.connect(host='localhost',
                        database='Phonepe_Pulse',
                        user='root',
                        password='sathesh123')
    if conn.is_connected():
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM AggTransByStates")
        records1 = cursor.fetchall()
        AggTransByStates = pd.DataFrame(records1,
                           columns=[i[0] for i  in cursor.description])

        cursor.execute("SELECT * FROM AggUserByBrand")
        records2 = cursor.fetchall()
        AggUserByBrand = pd.DataFrame(records2,
                         columns=[i[0] for i in cursor.description])

        cursor.execute("SELECT * FROM mapTransByDistrict")
        records3 = cursor.fetchall()
        mapTransByDistrict = pd.DataFrame(records3,
                             columns=[i[0] for i in cursor.description])

        cursor.execute("SELECT * FROM mapUserByDistReg")
        records4 = cursor.fetchall()
        mapUserByDistReg = pd.DataFrame(records4,
                                          columns=[i[0] for i in cursor.description])


        conn.commit()
        cursor.close()
        conn.close()
except Error as e:
    pass
# ------------------------------------ MySQl server connection ---------------------------------------------

# Header or Title of the page
st.markdown("<h1 style='text-align:center; color:yellow;'"
            ">Phonepe Pulse Data Visualization and Exploration</h1>",
            unsafe_allow_html=True)

yearTuple = ('2018', '2019', '2020', '2021', '2022')
quaterTuple = ('Q1', 'Q2', 'Q3', 'Q4')

scatter_year = st.selectbox('Select the Year', yearTuple)
st.write(' ')
stateTuple= ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
             'assam', 'bihar', 'chandigarh', 'chhattisgarh',
             'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
             'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
             'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
             'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
             'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
             'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
             'uttarakhand', 'west-bengal')

state = st.selectbox('Select the State:', stateTuple, index=10)

mapUserByDistReg_filter = np.where((mapUserByDistReg['State'] == state)
                                 & (mapUserByDistReg['Year'] == int(scatter_year)))
mapUserByDistReg_filter = mapUserByDistReg.loc[mapUserByDistReg_filter]
dist_reg = mapUserByDistReg_filter.groupby(['District']).sum(numeric_only=True)[['Registered_user','App_opening']]
dist_reg = dist_reg.reset_index()

col1, col2 = st.columns([1, 1])
with col1:
    fig1 = px.bar(dist_reg,
                  x="District",
                  y=["Registered_user"],
                  color='District',
                  title=f"District wise Registered user in {state}:")
    fig1.update_traces(width=1)
    st.plotly_chart(fig1)


# ---------------------Streamlit Tabs for various analysis --------------------------------------------------

geoMapVisual, UserBrandInfo,UserBrandPercent = st.tabs(["Transaction Geo Visual",
                                                        "Mobile Brand Analysis",
                                                        "User Brand Percentage"])

# ----------------------------------Geo map visualization-----------------------------------------------------
state_lat_lon = pd.read_csv('state_lat_lon.csv')

with geoMapVisual:
    st.subheader(':pink[State Wise Transaction Details:]')
    st.write(' ')
    Year = st.radio('Please select the Year', yearTuple, horizontal=True)
    st.write(' ')
    Quarter = st.radio('Please select the Quarter', quaterTuple, horizontal=True)
    st.write(' ')

    AggTransByStates_filter = AggTransByStates.groupby(
                          ['State', 'Year', 'Quater']).sum(numeric_only=True)[['Transacion_count','Transacion_amount']]
    AggTransByStates_filter = AggTransByStates_filter.reset_index()

    yrQtrTrans_filter = AggTransByStates_filter[(AggTransByStates_filter['Year'] == int(Year))
                    & (AggTransByStates_filter['Quater'] == Quarter)]

    lat_lon_df = pd.merge(state_lat_lon, yrQtrTrans_filter)
    lat_lon_df = lat_lon_df.rename(columns={'State': 'state'})

    # getting some geojson for India.  Reduce complexity of geometry to make it more efficient
    url = "https://raw.githubusercontent.com/Subhash9325/GeoJson-Data-of-Indian-States/master/Indian_States"
    gdf = gpd.read_file(url)
    gdf["geometry"] = gdf.to_crs(gdf.estimate_utm_crs()).simplify(1000).to_crs(gdf.crs)
    india_states = gdf.rename(columns={"NAME_1": "ST_NM"}).__geo_interface__

    # create the scatter geo plot
    fig1 = px.scatter_geo(lat_lon_df,
                          lat="latitude",
                          lon="longitude",
                          color="Transacion_amount",
                          size=lat_lon_df["Transacion_count"],
                          hover_name="state",
                          hover_data=["state",
                                     'Transacion_amount',
                                     'Transacion_count',
                                     'Year',
                                     'Quater'],
                          title='State',
                          size_max=10,)

    fig1.update_traces(marker={'color': "#CC0044", 'line_width': 1})

    fig = px.choropleth(
          pd.json_normalize(india_states["features"])["properties.ST_NM"],
          locations="properties.ST_NM",
          geojson=india_states,
          featureidkey="properties.ST_NM",
          color_discrete_sequence=["lightgreen"],)

    fig.update_geos(fitbounds="locations", visible=False)
    fig.add_trace(fig1.data[0])

    fig.update_layout(height=500, width=600)

    # remove white background
    fig.update_geos(bgcolor='#F8F8F8', showland=True)

    st.plotly_chart(fig)
# ------------------------------------Geo map visualization end-----------------------------------------------------

# ------------------------------------User Mobile Brand analysis------------------------------------------------
with UserBrandInfo:
    st.subheader(':yellow[User Mobile Brand Analysis by State:]')
    StateBar = st.selectbox('Please select State', stateTuple, index=10)
    yearBar = st.radio('Please select the Year:', yearTuple, horizontal=True)
    QuaterBar = st.radio('Please select the Quarter:', quaterTuple, horizontal=True)

    UserByBrand_filter = AggUserByBrand[(AggUserByBrand['State'] == StateBar)
                                        & (AggUserByBrand['Year'] == int(yearBar))
                                        & (AggUserByBrand['Quater'] == QuaterBar)]

    userBrand = px.bar(UserByBrand_filter,
                       x='Brand',
                       y='Brand_count',
                       color='Brand',
                       title='User Mobile Brand Analysis ',
                       color_continuous_scale='magma', )

    st.plotly_chart(userBrand)

with UserBrandPercent:
    st.subheader(':violet[Mobile Brand in Percentage]')
    StatePie = st.selectbox('Please Choose State', stateTuple, index=10)
    yearPie = st.radio('Please Choose the Year:', yearTuple, horizontal=True)
    QuaterPie = st.radio('Please choose the Quarter:', quaterTuple, horizontal=True)

    UserByBrand_filterPie = AggUserByBrand[(AggUserByBrand['State'] == StatePie)
                                        & (AggUserByBrand['Year'] == int(yearPie))
                                        & (AggUserByBrand['Quater'] == QuaterPie)]

    BrandPercent = px.pie(UserByBrand_filterPie,
                       names='Brand',
                       values='Brand_percentage',
                       color='Brand',
                       template='plotly_dark',
                       title='User Mobile Brand in percentage ',
                       width=800,
                       height=600)

    BrandPercent.update_traces(textposition='inside',
                               textinfo='percent+label',
                               textfont_size=15,
                               insidetextorientation='radial',
                               pull=[0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               marker=dict(line=dict(color='#000000', width=2)))

    BrandPercent.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    st.plotly_chart(BrandPercent)


