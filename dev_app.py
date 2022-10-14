import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import json
import streamlit as st
import plotly.express as px
import os

from zmq import RADIO

ZOOM = 3
OPE = 0.75
RADIUS = 18
def preprocessor(file):
    col_name = ['lon','lat']
    mon = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    for i in range(1901,2022):
        for ii in range(12):
            col_name.append(str(i)+"_"+mon[ii])
    read_path = file
    try:
        df = pd.read_csv(read_path)
    except:
        df = pd.read_excel(read_path)

    try:
        df.columns = col_name
    except:
        print("Already have columns Name")
        df.rename(columns = {'Long':'lon','Lat':'lat'}, inplace = True)
        df.columns = col_name[:-2]

    return df


# df = pd.read_csv("Copy of Copy of NWH-CRU_tmp_1901-2020_month_50km.csv")
# month_df = df  
# col_name = ['lon' , 'lat']
# month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
# for i in range(1901,2021):
#   for ii in range(12):
#     col_name.append(str(i)+'_'+month[ii])

# df.columns = col_name
def action(df):
    ndf = pd.DataFrame()
    ndf['lat'] = df['lat']
    ndf['lon'] = df['lon']
    ndf['Min'] = df.iloc[:,2:].min(axis = 1)
    ndf['Max'] = df.iloc[:,2:].max(axis = 1)
    ndf['Mean'] = df.iloc[:,2:].mean(axis = 1)
    ndf['Q1'] = df.iloc[:,2:].quantile(0.25,axis = 1)
    ndf['Q2'] = df.iloc[:,2:].quantile(0.50,axis = 1)
    ndf['Q3'] = df.iloc[:,2:].quantile(0.75,axis = 1)
    ndf['Q4'] = df.iloc[:,2:].quantile(1,axis = 1)
    ndf['IQR'] = ndf['Q3'] - ndf['Q1']
    ndf['Skewness'] = df.iloc[:,2:].skew(axis = 1)
    ndf['Kurtosis'] = df.iloc[:,2:].kurtosis(axis = 1)
    return ndf
#ndf = df[['lat','lon']]

def stprint(period):
    st.write(f"I am here {period}")

st.title("This Page is  Under-Development - Only select CRU50KM")

option = st.sidebar.selectbox(
    'Select a Data-set: ',
    ('','CRU 50KM', 'CRU 25KM', 'IMDAA 12KM','CHIRP 5KM'))

st.sidebar.write('You selected:', option)

if option == 'CRU 50KM':
    base_path = "./CRU_50km_monthly_1901-2020-20221013T040033Z-001/CRU_50km_monthly_1901-2020"
    files = os.listdir(base_path)
    select_data = []
    for i in files:
        if '.csv' in i:
            select_data.append(i)
    st_option = st.selectbox(
    'Select Dataset from 50KM',
    np.array(select_data))

    file_name =  st_option
    #st.write('Full path is ',base_path + file_name)
    df = preprocessor(os.path.join(base_path,file_name))
    ndf = action(df)

    

if option == 'CRU 25KM':
    base_path = "./CRU_25km_Regrid-20221013T040132Z-001/CRU_25km_Regrid"
    files = os.listdir(base_path)
    select_data = []
    for i in files:
        if '.csv' in i:
            select_data.append(i)
    st_option = st.selectbox(
    'Select Dataset from 25KM',
    np.array(select_data))

    file_name =  st_option
    #st.write('Full path is ',base_path + file_name)
    df = preprocessor(os.path.join(base_path,file_name))
    ndf = action(df)

if option == 'IMDAA 12KM':
    pass
if option == 'CHIRP 5KM':
    pass

period = st.sidebar.slider('Select a time Period', 1901, 2020)
#st.sidebar.write(f'The Time Period is {period}')
endperiod = st.sidebar.slider('Select a Ending Period', period+1, 2020)
st.sidebar.write(f'The Time Period is {period}  to {endperiod}')
#st.write("Debug", type(endperiod))

# cols = ['lat','lon']
# for i in df.columns[2:]:
#   if  int(i[:4]) in range(period,endperiod+1):#yr1 >= i[:4] and i[:4] <=yr2:
#     cols.append(i)

# sdf = df[cols]


# df.columns = col_name
# ndf = pd.DataFrame()
# ndf['lat'] = df['lat']
# ndf['lon'] = df['lon']
# ndf['Min'] = sdf.iloc[:,2:].min(axis = 1)
# ndf['Max'] = sdf.iloc[:,2:].max(axis = 1)
# ndf['Mean'] = sdf.iloc[:,2:].mean(axis = 1)
# ndf['Q1'] = sdf.iloc[:,2:].quantile(0.25,axis = 1)
# ndf['Q2'] = sdf.iloc[:,2:].quantile(0.50,axis = 1)
# ndf['Q3'] = sdf.iloc[:,2:].quantile(0.75,axis = 1)
# ndf['Q4'] = sdf.iloc[:,2:].quantile(1,axis = 1)
# ndf['IQR'] = ndf['Q3'] - ndf['Q1']
# ndf['Skewness'] = sdf.iloc[:,2:].skew(axis = 1)
# ndf['Kurtosis'] = sdf.iloc[:,2:].kurtosis(axis = 1)
# col1, col2, col3 , col4 , col5 , col6 = st.columns(6)

# with col1:
#    st.button('Min',on_click= stprint(endperiod))

# with col2:
#    st.button('Max')
# with col3:
#    st.button('Mean')
# with col4:
#    st.button('Quartiles')
# with col5:
#    st.button('IQR')
# with col6:
#    st.button('Rel-Incr')




# col7, col8, col9 , col10 , col11 , col12 = st.columns(6)

# with col7:
#    st.button('Percentiles')

# with col8:
#    st.button('Skewness')
# with col9:
#    st.button('Kurtosis')
# with col10:
#    st.button('Stationarity')
# with col11:
#    st.button('correlations')
# with col12:
#    st.button('outliers')


st_option = st.selectbox(
    'Select a statistic to be displayed as Spatial Plot',
    ('','Min', 'Max', 'Mean','Quartiles','IQR','Relative Increment','Percentiles','Skewness','Kurtosis','Stationarity','correlations','outliers'))

st.write('You selected:', st_option)

if st_option:
    if st_option == 'Min':
            
        # fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Min', radius=RADIUS,
        #                         center=dict(lat=31.25, lon=77.25), zoom=ZOOM,
        #                         mapbox_style="carto-positron",title = f"Stat: {st_option} Between Year {period} - {endperiod}"
        #                         ,opacity=OPE )
        fig = px.density_mapbox(ndf, lat="lat", lon="lon",  hover_data=["Min"],
                         zoom=3,width = 500, height=400)
        fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://api.mapbox.com/styles/v1/mapbox/dark-v10/static/79.2616,32.7587,4.45,0/500x400?access_token=pk.eyJ1IjoicmFqYW4zMnMiLCJhIjoiY2w5ODd5enV5MDBtajNzbzZ1a3ZjMnVxcSJ9.c2CycsFb8nHLlMwFE2-7iA"
                ]
            }
        ])
       # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        # fig.layout.xaxis.fixedrange = False
        # fig.layout.yaxis.fixedrange = False
        st.plotly_chart(fig)#, use_container_width=True)


    if st_option == 'Max':
            
        fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Max', radius=RADIUS,
                                center=dict(lat=31.25, lon=77.25), zoom=ZOOM,
                                mapbox_style="carto-positron",title = f"Stat: {st_option} Between Year {period} - {endperiod}" 
                                ,opacity=OPE)

        st.plotly_chart(fig, use_container_width=True)
    if st_option == 'Mean':
            
        fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Mean', radius=RADIUS,
                                center=dict(lat=31.25, lon=77.25), zoom=ZOOM,
                                mapbox_style="carto-positron",title = f"Stat: {st_option} Between Year {period} - {endperiod}" 
                                ,opacity=OPE)

        st.plotly_chart(fig, use_container_width=True)

    if st_option == 'Quartiles':
        genre = st.radio(
        "Select A Quartile",
        ('Q1', 'Q2', 'Q3','Q4'))
            
        fig = px.density_mapbox(ndf, lat='lat', lon='lon', z=genre, radius=RADIUS,
                                center=dict(lat=31.25, lon=77.25), zoom=ZOOM,
                                mapbox_style="carto-positron",title = f"Stat: {st_option} Between Year {period} - {endperiod}" ,
                                opacity=OPE)
        
        st.plotly_chart(fig, use_container_width=True)


    if st_option == 'IQR':
            
        fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='IQR', radius=RADIUS,
                                center=dict(lat=31.25, lon=77.25), zoom=ZOOM,
                                mapbox_style="carto-positron",title = f"Stat: {st_option} Between Year {period} - {endperiod}" 
                                ,opacity=OPE)


        st.plotly_chart(fig, use_container_width=True)



    if st_option == 'Skewness':
            
        fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Skewness', radius=RADIUS,
                                center=dict(lat=33.25, lon=76.25), zoom=ZOOM,
                                mapbox_style="stamen-toner",title = f"Stat: {st_option} Between Year {period} - {endperiod}"
                                ,opacity=OPE )

        st.plotly_chart(fig, use_container_width=True)
    #stamen-toner

    if st_option == 'Kurtosis':
            
        fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Kurtosis', radius=RADIUS,
                                center=dict(lat=31.25, lon=77.25), zoom=ZOOM,
                                mapbox_style="carto-positron",title = f"Stat: {st_option} Between Year {period} - {endperiod}" 
                                ,opacity=OPE)

        st.plotly_chart(fig, use_container_width=True)


    if st_option == 'Relative Increment':
        options = st.multiselect(
        'Select a Month (Multiple Selections)',
        ['jan', 'feb', 'mar', 'apr','may','jun','jul','jug','sep','oct','nov','dec']
        )
    #   st.write("debug:" )
        if len(options) ==2:
            baseY = str(period)+"_"+options[0]
            compareY = str(endperiod)+"_"+options[1]
            nndf = pd.DataFrame()
            nndf['lat'] = df['lat']
            nndf['lon'] = df['lon']
            nndf['Incr'] = (df[compareY] - df[baseY])/df[baseY] * 100
            fig = px.density_mapbox(nndf, lat='lat', lon='lon', z='Incr', radius=RADIUS,
                                    center=dict(lat=31.25, lon=77.25), zoom=ZOOM,
                                    mapbox_style="carto-positron",title = f"Stat: {st_option} Between Year {period} - {endperiod}",
                                    opacity=OPE )

            st.plotly_chart(fig, use_container_width=True)









#    x = ndf['lat']
 #   y = ndf['lon']


    #heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
    #extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

  #  fig, ax = plt.subplots()
   # ax.scatter(x,y,c = df['2000_Jan'],cmap='viridis')
    #fig = ax.colorbar()
    #plt.clf()
    #ax.imshow(heatmap.T, extent=extent, origin='lower')
    #plt.show()


    #ax.hist(arr, bins=20)

    #st.pyplot(fig)


# df = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

#st.map(ndf)


# Lat range is 26.20 to 35.40
# Long ranfge is 74.50 to 95.40

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')
