#Import library
import os
import pandas as pd

#Read path of file
os.path.dirname(os.path.realpath('__file__'))

def dataCountryCode():
    #Read country code data
    dfcountrycode = pd.read_json('kode_negara_lengkap.json')
    
    #Rename some column
    colrename     = {'name': 'countryname', 'alpha-3': 'countrycode', 'sub-region': 'subregion'}
    dfcountrycode = dfcountrycode.rename(columns = colrename)
    
    #Cleaning process
    clean = {'\(.+': ''}
    for pat, repl in clean.items():
        dfcountrycode['countryname'] = dfcountrycode['countryname'].str.replace(pat, repl, regex = True)
    
    #Select only the required column
    dfcountrycode = dfcountrycode[['countryname', 'countrycode', 'region', 'subregion']]
    
    return dfcountrycode

def readData():
    #Read oil production data in the world
    dfoilprod = pd.read_csv('produksi_minyak_mentah.csv')

    #Rename some column
    colrename = {'kode_negara': 'countrycode', 'tahun': 'year', 'produksi': 'oilproduction'}
    dfoilprod = dfoilprod.rename(columns = colrename)
    
    #Round 2 for oilproduction value
    dfoilprod['oilproduction'] = dfoilprod['oilproduction'].round(2)

    #Read data country code
    dfcountrycode = dataCountryCode()

    #Merge data oil production and country code
    data = dfoilprod.merge(dfcountrycode, how = 'inner', on = ['countrycode'])
    
    #Sort data by countrycode and year
    data = data.sort_values(by = ['countrycode', 'year']).reset_index(drop = 'True')

    return data

def getFilterDashboard(df):
    #Get unique value from year
    years   = sorted(list(df['year'].unique()))
    #Get unique value from countrycode
    country = list((df['countrycode'] + ' - ' + df['countryname']).unique())

    return years, country
