import random
from random import *
from matplotlib import ticker as ticker
from matplotlib import colors as pltc
from matplotlib import pyplot as plt

def RandomColors(data):
  all_colors = [k for k, v in pltc.cnames.items()]
  for i in ['black', 'white', 'cyan', 'aqua']:
    all_colors.remove(i)

  dataregion  = data['region'].unique().tolist()
  colors = sample(all_colors, len(dataregion))

  colors = dict(zip(dataregion, colors))
  group_lk = data.set_index('countryname')['region'].to_dict()

  return colors, group_lk

def plotMostOilProducing(df, current_year, limit):
    if(limit < 10):
      fig, ax = plt.subplots(figsize=(10, 8))
    else:
      fig, ax = plt.subplots(figsize=(15, 12))
    colors, group_lk = RandomColors(df)

    dff = df[df['year'].eq(current_year)].sort_values(by='oilproduction', ascending=True).tail(limit)
    ax.clear()
    ax.barh(dff['countryname'], dff['oilproduction'], color=[colors[group_lk[x]] for x in dff['countryname']])
    dx = dff['oilproduction'].max() / 200
    for i, (oilproduction, countryname) in enumerate(zip(dff['oilproduction'], dff['countryname'])):
        ax.text(oilproduction, i,     countryname,           size=14, weight=600, ha='right', va='bottom')
        ax.text(oilproduction, i-.25, group_lk[countryname], size=10, color='#444444', ha='right', va='baseline')
        ax.text(oilproduction, i,     f' {oilproduction:,.2f}',  size=14, ha='left',  va='center')
    ax.text(1, 0, current_year, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='--')
    ax.set_axisbelow(True)
    ax.text(0, 1.1, str(limit) + ' Most Oil Producing Countries in '+ str(current_year),
            transform=ax.transAxes, size=15, weight=600, ha='left', va='top')
    plt.box(False)
    return fig, ax