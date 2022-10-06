#import reverse_geocoder as rg
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import json
import streamlit as st

#st.write("Hello World")

df = pd.read_csv("Copy of Copy of NWH-CRU_tmp_1901-2020_month_50km.csv")
#month_df = df  
col_name = ['Longitude' , 'latitude']
month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
for i in range(1901,2021):
  for ii in range(12):
    col_name.append(str(i)+'_'+month[ii])

df.columns = col_name




def getLocationname_(*args):
  latitude = args[0]
  longitude = args[1]
  coordinates = (latitude,longitude)
  region_name,country=data[str(latitude)+'_'+str(longitude)]
  #results = rg.search(coordinates)
  return region_name,country


f = open('location.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)



def get_stat(*args):
    lat = args[0]
    long = args[1]
    ndf = df[df['Longitude'] == lat ]
    res = ndf[ndf['latitude'] == long]
    res = res.T
    res = res.reset_index()
    max_idx = res.iloc[2:-2,1].astype('float64').argmax()
    min_idx = res.iloc[2:-2,1].astype('float64').argmin()
    max_temp = res.iloc[max_idx,1]
    min_temp = res.iloc[min_idx,1]
    max_val = res['index'][max_idx]
    min_val = res['index'][min_idx]
    min_month_data = min_val.split('_')
    max_month_data = max_val.split('_')
    mean=res.iloc[2:-2,1].mean()
    median = res.iloc[2:-2,1].median()
    #long_lat = res.iloc[0:2,1].values    
    #st.write(f'At location {getLocationname_(long_lat)}')

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Highest Temperature", value=str(max_temp) +"°C")
        st.caption(f'Year: {max_month_data[0]} Month : {max_month_data[1]}')

    with col2:
        st.metric(label="Lowest Temperature", value=str(min_temp) +"°C")
        st.caption(f'Year {min_month_data[0]} Month {min_month_data[1]}')
    st.write(f"The Mean temp: {round(mean,2)} °C  and Median temp is {round(median,2)} °C")
    # number = st.sidebar.number_input('Insert a number')
    # st.write('The current number is ', number)
    fig, ax = plt.subplots()
    
    plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0.3),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 0.0, 0.0, 0.5),  # green with alpha = 50%
    "savefig.facecolor": (0.0, 0.0, 0.6, 0.2),  # blue  with alpha = 20%
    })
    labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    plt.rcParams['figure.figsize'] = [12, 4]
    ax.axhline(y = mean, color = 'r', linestyle = '--',label = 'Mean')
    ax.axhline(y = median, color = 'g', linestyle = '--',label = 'Median')
    ax.plot(res.iloc[2:-2,1][-12:],marker = 'o',color = 'cyan',label = 'Yr_2020')
    #ax.plot(res.iloc[2:-2,1][-24:-12],marker = '^',color = 'blue',label = 'Yr_2019')
    ax.grid("ON")
    plt.title(f"Year {2020}")
    #plt.legend(['Mean','Median',f'Year {2020}'],color='w')
    plt.xticks(res.iloc[2:-2,1][-12:].index,labels, rotation ='vertical')
    plt.ylabel('Temp in °C')
    leg = plt.legend(loc='best')
    for text in leg.get_texts():
        text.set_color("w")
    plt.show()
    st.pyplot(fig)





Lat = float(st.sidebar.text_input('Latitude','0.0'))
Long = float(st.sidebar.text_input('longitude','0.0'))
st.write('Latitude', Lat)
st.write('Longitude', Long)

if st.sidebar.button('Click'):
    ans = getLocationname_(Lat,Long)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Location: ")    
    with col2:
        st.subheader(f'{ans[0]} , {ans[1]}')
    get_stat(Lat,Long)



else:
    st.write('Goodbye')


# #######

# path = "/content/drive/MyDrive/Copy of NWH-CRU_pre_1901-2020_month_50km.csv"

# data_path = "/content/NWH-CRU_pre_1901-2020_month_50km (2).csv"

# #######









