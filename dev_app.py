import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import json
import streamlit as st
import plotly.express as px

df = pd.read_csv("Copy of Copy of NWH-CRU_tmp_1901-2020_month_50km.csv")
#month_df = df  
col_name = ['lon' , 'lat']
month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
for i in range(1901,2021):
  for ii in range(12):
    col_name.append(str(i)+'_'+month[ii])

df.columns = col_name
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
#ndf = df[['lat','lon']]

def stprint(period):
    st.write(f"I am here {period}")

st.title("This Page is  Under-Development - Only select CRU50KM")

option = st.sidebar.selectbox(
    'Select a Data-set: ',
    ('','CRU 50KM', 'CRU 25KM', 'IMDAA 12KM','CHIRP 5KM'))

st.sidebar.write('You selected:', option)

period = st.sidebar.slider('Select a time Period', 1901, 2020)
#st.sidebar.write(f'The Time Period is {period}')
endperiod = st.sidebar.slider('Select a Ending Period', period, 2020)
st.sidebar.write(f'The Time Period is {period}  to {endperiod}')
#st.write("Debug", type(endperiod))

cols = ['lat','lon']
for i in df.columns[2:]:
  if  int(i[:4]) in range(period,endperiod+1):#yr1 >= i[:4] and i[:4] <=yr2:
    cols.append(i)

sdf = df[cols]


df.columns = col_name
ndf = pd.DataFrame()
ndf['lat'] = df['lat']
ndf['lon'] = df['lon']
ndf['Min'] = sdf.iloc[:,2:].min(axis = 1)
ndf['Max'] = sdf.iloc[:,2:].max(axis = 1)
ndf['Mean'] = sdf.iloc[:,2:].mean(axis = 1)
ndf['Q1'] = sdf.iloc[:,2:].quantile(0.25,axis = 1)
ndf['Q2'] = sdf.iloc[:,2:].quantile(0.50,axis = 1)
ndf['Q3'] = sdf.iloc[:,2:].quantile(0.75,axis = 1)
ndf['Q4'] = sdf.iloc[:,2:].quantile(1,axis = 1)
ndf['IQR'] = ndf['Q3'] - ndf['Q1']
ndf['Skewness'] = sdf.iloc[:,2:].skew(axis = 1)
ndf['Kurtosis'] = sdf.iloc[:,2:].kurtosis(axis = 1)
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
    ('','Min', 'Max', 'Mean','Quartiles','IQR','Rel-Incr','Percentiles','Skewness','Kurtosis','Stationarity','correlations','outliers'))

st.write('You selected:', st_option)


if st_option == 'Min':
        
    fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Min', radius=15,
                            center=dict(lat=31.25, lon=77.25), zoom=4,
                            mapbox_style="carto-positron" )

    st.plotly_chart(fig, use_container_width=True)


if st_option == 'Max':
        
    fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Max', radius=15,
                            center=dict(lat=31.25, lon=77.25), zoom=4,
                            mapbox_style="carto-positron" )

    st.plotly_chart(fig, use_container_width=True)
if st_option == 'Mean':
        
    fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Mean', radius=15,
                            center=dict(lat=31.25, lon=77.25), zoom=4,
                            mapbox_style="carto-positron" )

    st.plotly_chart(fig, use_container_width=True)

if st_option == 'Quartiles':
        
    fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Q3', radius=15,
                            center=dict(lat=31.25, lon=77.25), zoom=4,
                            mapbox_style="carto-positron" )

    st.plotly_chart(fig, use_container_width=True)


if st_option == 'IQR':
        
    fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='IQR', radius=15,
                            center=dict(lat=31.25, lon=77.25), zoom=4,
                            mapbox_style="carto-positron" )

    st.plotly_chart(fig, use_container_width=True)



if st_option == 'Skewness':
        
    fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Skewness', radius=15,
                            center=dict(lat=31.25, lon=77.25), zoom=4,
                            mapbox_style="carto-positron" )

    st.plotly_chart(fig, use_container_width=True)


if st_option == 'Kurtosis':
        
    fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Kurtosis', radius=15,
                            center=dict(lat=31.25, lon=77.25), zoom=4,
                            mapbox_style="carto-positron" )

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
