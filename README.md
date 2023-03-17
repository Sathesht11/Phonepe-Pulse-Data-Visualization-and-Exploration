# Phonepe-Pulse-Data-Visualization-and-Exploration

## Problem Statement:

The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.

## Approach:
* **Data extraction:** **Cloning** the **Github** using scripting to fetch the data from the **Phonepe pulse** Github repository and store it in a suitable format such as CSV
or JSON.
* **Data transformation:** Using a scripting language such as Python, along with libraries such as Pandas, to manipulate and pre-process the data. This may include **cleaning** the data, **handling missing values,** and transforming the data into a format suitable for analysis and visualization.
* **Database insertion:** Use the **"mysql-connector-python"** library in Python to connect to a **MySQL database** and insert the transformed data using SQL commands.
* **Dashboard creation:** Using the **Streamlit** and **Plotly** libraries in Python to create an interactive and visually appealing dashboard. Plotly's built-in geo map functions can be used to display the data on a map and Streamlit can be used to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.
* **Data retrieval:** Using the **"mysql-connector-python"** library to connect to the **MySQL** database and **fetch the data** into a **Pandas dataframe** and Using the data in the dataframe to **update the dashboard** dynamically.

## Packages:
* streamlit
* pandas
* pymongo
* streamlit_lottie
* mysql-connector-python
* plotly-express
* geopandas
* streamlit-option-menu

# Data
The data was cloned from https://github.com/PhonePe/pulse.git
