#Nama : Richi Sastra Samudra 
#NIM : 122200097
#Tugas Besar UAS 
import re
import ReadData
import plotLine
import plotBarh
import plotBubble
import numpy as np
import streamlit as st

dataproduction = ReadData.readData()
year, country  = ReadData.getFilterDashboard(dataproduction)
minyear, maxyear = min(year), max(year)

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout = "wide")

#LAYING OUT THE TOP SECTION OF THE APP
strtitle1 = "Global Oil Production by Countries in {} - {}".format(minyear, maxyear)
st.title(strtitle1)
st.markdown(
    """
    This page displays a table with actual values, consensus figures, forecasts, statistics and historical data charts for - Crude Oil Production.
    This page provides values for Crude Oil Production reported in several countries. 
    The table has current values for Crude Oil Production, previous releases, historical highs and record lows, release frequency, reported unit and currency plus links to historical data charts.
    """)

#LAYING OUT THE SECOND TOP SECTION OF THE APP
st.write('\n\n\n')
row2_1, row2_2 = st.columns((2,3))

with row2_1:
    strtitle2 = 'Oil Production Data in {} - {}'.format(minyear, maxyear)
    st.subheader(strtitle2)
    st.write(
    """
    Data disamping menjelaskan tentang produksi minyak dari setiap negara dari tahun 1971 sampai 2015  
    """)

with row2_2:
    dataproduction1 = dataproduction
    dataproduction1.index = dataproduction1.index + 1
    st.dataframe(dataproduction1)

#LAYING OUT THE SECOND TOP SECTION OF THE APP
st.sidebar.title("Setting")
T = st.sidebar.selectbox("Select Year", year)
C = st.sidebar.selectbox("Select Country", country)
B = st.sidebar.slider("How many countries, will be showing?", 1, len(country), value = 5)
N = re.sub('.+- ', '', C)

st.write('\n\n\n')
row3_1, row3_2 = st.columns((3,2))

#QUESTION 1
fig1, ax1, m1 = plotLine.plotOilsDataProduction(dataproduction, countryname = N)

with row3_1:
    st.write('\n')
    st.pyplot(fig1)

with row3_2:
    dfplot = dataproduction[dataproduction['countryname'].str.contains(N)]
    yearoptimum = plotLine.MinMaxOilProduction(dfplot, countryname = N)['year'].tolist()
    prodoptimum = plotLine.MinMaxOilProduction(dfplot, countryname = N)['oilproduction'].tolist()
    
    if(len(yearoptimum) == 1):
        yearoptimum.append(0)
        prodoptimum.append(0)

    strtitle3 = '{}\'s Oil Production Data in {} - {}'.format(N, dfplot['year'].min(), dfplot['year'].max())
    st.subheader(strtitle3)
    if(m1 != 0):
        row3line = "Produksi minyak di Negara {} mengalami titik terendahnya pada tahun {} yang hanya memproduksi\
                   minyak sebesar {} barrel, sedangkan produksi paling tinggi terjadi pada tahun {}\
                   dengan banyak produksi minyak sebesar {} barrel. ".format(N, yearoptimum[0], prodoptimum[0], yearoptimum[1], prodoptimum[1])
        if (m1 < 0):
            row3line = row3line + "Berdasarkan perhitungan trend maka diperkirakan produksi minyak di negara ini akan mengalami penurunan pada tahun - tahun berikutnya."
        elif(m1 > 0):
            row3line = row3line + "Berdasarkan perhitungan trend maka diperkirakan produksi minyak di negara ini akan mengalami kenaikan pada tahun - tahun berikutnya."
    else:
        row3line = "Negara {} tidak menghasilkan minyak sama sekali sampai dengan tahun {}".format(N, yearoptimum[0])
    st.write(row3line)

#QUESTION 2
st.write('\n\n\n\n')
row4_1, row4_2 = st.columns((2,3))

fig2, ax2 = plotBarh.plotMostOilProducing(dataproduction, current_year = T, limit = B)

dfsort = dataproduction[dataproduction['year'].eq(T)].sort_values(by = 'oilproduction', ascending=False).head(B)
dfsort = dfsort[['countryname','oilproduction']]
dfsort = dfsort.reset_index(drop = True)
dfsort.index = dfsort.index + 1

with row4_1:
    row4header = '{} Most Oil Producing Countries in {}'.format(B, T)
    st.subheader(row4header)
    row4line = 'Top {} negara penghasil minyak terbanyak pada tahun {} disajikan pada tabel berikut :\n'.format(B,T)
    st.write(row4line)
    st.dataframe(dfsort)

with row4_2:
    st.write('\n')
    st.pyplot(fig2)

#QUESTION 3
st.write('\n\n\n\n')
row5_1, row5_2 = st.columns((3,2))
fig3, ax3 = plotBubble.plotMostOilProducinginCumulative(dataproduction, limit = B, yearrange = (minyear, maxyear))

with row5_1:
    st.write('\n')
    st.pyplot(fig3)

with row5_2:
    row5header = '{} Most Oil Producing Countries in Cumulative From {} - {}'.format(B, minyear, maxyear)
    st.subheader(row5header)
    row4line = 'Top {} negara penghasil minyak terbanyak secara kumulatif pada tahun {} - {} disajikan pada tabel berikut :\n'.format(B, minyear, maxyear)
    dfcumulative = plotBubble.SortingCumulativeProduction(dataproduction, limit = B)
    dfcumulative.index = dfcumulative.index + 1
    st.write(row4line)
    st.dataframe(dfcumulative)

#QUESTION 4
dfprodmorethan0 = dataproduction[dataproduction['oilproduction'] > 0]
dfprodeq0       = dataproduction[dataproduction['oilproduction'] == 0].sort_values(by = ['countryname', 'year']).reset_index(drop = True)
dfmaxprod       = dfprodmorethan0[dfprodmorethan0.groupby(['year'])['oilproduction'].transform(max) == dfprodmorethan0['oilproduction']]\
                            .sort_values(by = ['year']).reset_index(drop = True)
dfminprod       = dfprodmorethan0[dfprodmorethan0.groupby(['year'])['oilproduction'].transform(min) == dfprodmorethan0['oilproduction']]\
                            .sort_values(by = ['year']).reset_index(drop = True)

st.write('\n\n')
row6_1, row6_2 = st.columns((1,1))

with row6_1:
    row6header = 'The Country that Produces the Most Oil per year From {} - {}'.format(minyear, maxyear)
    st.subheader(row6header)
    st.write('Negara yang menghasilkan minyak paling banyak tiap satuan tahun disajikan pada tabel berikut:')
    st.dataframe(dfmaxprod)

with row6_2:
    row7header = 'The Country that Produces the Lowest Oil per year From {} - {}'.format(minyear, maxyear)
    st.subheader(row7header)
    st.write('Negara yang menghasilkan minyak paling sedikit tiap satuan tahun disajikan pada tabel berikut:')
    st.dataframe(dfminprod)

st.write('\n\n')
row8header = 'The Country that Produces the Zeros Oil per year From {} - {}'.format(minyear, maxyear)
st.subheader(row8header)
st.write('Negara yang tidak menghasilkan minyak tiap satuan tahun disajikan pada tabel berikut:')
st.dataframe(dfprodeq0)
