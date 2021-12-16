import numpy as np
from matplotlib import pyplot as plt

def MinMaxOilProduction(df, countryname):
    #Filter data based on countryname
    df = df[df['countryname'].str.contains(countryname)]
    
    #drop duplicates oil productions value
    df = df.drop_duplicates(subset=['oilproduction'], keep = 'last')
    
    #Get min and max oil production data
    minmax = df[(df['oilproduction'].max() == df['oilproduction']) | (df['oilproduction'].min() == df['oilproduction'])]
    minmax = minmax.sort_values(by = ['oilproduction'])
                            
    return minmax.reset_index(drop = True)

def plotOilsDataProduction(df, countryname):
    #Data filter
    dfplot = df[df['countryname'].str.contains(countryname)]
    yearoptimum, prodoptimum  = MinMaxOilProduction(dfplot, countryname)['year'].tolist(), MinMaxOilProduction(dfplot, countryname)['oilproduction'].tolist()

    if(len(yearoptimum) == 1):
        yearoptimum.append(0)
        prodoptimum.append(0)

    #Initialize Abscissa and Ordinate 
    x, y = dfplot['year'], dfplot['oilproduction']

    fig, ax = plt.subplots(1, figsize=(15, 8))
    
    #Plot graph of oil production 
    ax.plot(x, y, color = '#ffb949', linestyle='-', marker='o') 

    #Give trend (linear regression)
    m, b = np.polyfit(x, y, 1)
    ax.plot(x, m*x + b, color = '#f3ce53', linestyle = '--', alpha = 0.6)

    #Delete frame
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    #Ordinate value limit
    if((prodoptimum[0] > 0) & (prodoptimum[0] < 5000)):
        ax.set_ylim(bottom = -1000, top = 1.2*prodoptimum[1])
    elif(prodoptimum[0] == 0):
        if(prodoptimum[1] > 0):
            ax.set_ylim(bottom = -100, top = 1.2*prodoptimum[1] + 100)
        else:
            ax.set_ylim(bottom = -100, top = 100)
    else:
        ax.set_ylim(bottom = 0.01*prodoptimum[0] - 5000, top = 1.2*prodoptimum[1])
    
    #Set title 
    ax.set_title('{}\'s Oil Production\nin {} - {}'
                  .format(countryname, dfplot['year'].min(), dfplot['year'].max()),
                   color = '#d04e02', fontsize = 18)
    
    #Give some label
    ax.legend(['Oil Production', 'Trend'])
    ax.set_xlabel("Year", labelpad = 12)
    ax.set_ylabel("Production (barrel)", labelpad = 12)

    #Give annotate labels just in max and min values
    for x, y in zip(dfplot['year'], dfplot['oilproduction']):
        if ((x in yearoptimum) & (y > 0)):
            label = "{:.2f}".format(y)
            if(x == yearoptimum[0]):
                ax.annotate(label + "\n(min in " + str(x) + ")", (x,y), textcoords = "offset points", xytext = (0, -31), ha='center')
            elif(x == yearoptimum[1]):
                ax.annotate(label + "\n(max in "+ str(x) + ")", (x,y), textcoords = "offset points", xytext = (0, 11), ha='center')
    return fig, ax, m