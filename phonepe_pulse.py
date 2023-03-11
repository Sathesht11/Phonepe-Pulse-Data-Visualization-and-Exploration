
import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector as msql
from mysql.connector import Error
import plotly.express as px


# ----------------------------------MySQl server connection----------------------------------------

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
#------------------------------------MySQl server connection---------------------------------------------


# Header or Title of the page
st.markdown("<h1 style='text-align:center; color:yellow;'"
            ">Phonepe Pulse Data Visualization and Exploration</h1>",
            unsafe_allow_html=True)

scatter_year = st.selectbox('Select the Year',
                            ('2018', '2019', '2020', '2021', '2022'))
st.write(' ')
scatter_state = st.selectbox('Select the State:',
                ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                 'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                 'uttarakhand', 'west-bengal'), index=10)

mapUserByDistReg_filter = np.where((mapUserByDistReg['State'] == scatter_state)
                                 & (mapUserByDistReg['Year'] == int(scatter_year)))
mapUserByDistReg_filter = mapUserByDistReg.loc[mapUserByDistReg_filter]
dist_reg = mapUserByDistReg_filter.groupby(['District']).sum(numeric_only=True)[['Registered_user','App_opening']]
dist_reg = dist_reg.reset_index()

#st.dataframe(dist_reg)

col1, col2 = st.columns([1, 1])
with col1:
    fig1 = px.bar(
    dist_reg,
    x="District",
    y=["Registered_user"],
    color='District',
    title="District wise Registered user and App_opening")
    fig1.update_traces(width=1)
    st.plotly_chart(fig1)
