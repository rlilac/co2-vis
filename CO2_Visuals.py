#Rena L - May 10, 2025
#This code  uses pandas and matplot to plot CO2 emissions data collected by Our World In Data. The first plot shows the top 10 countries
#with the highest emissions, not including land-use change emissions. The second plot shows the per capita CO2 emissions of the top 5 CO2 
#emitters (and Canada for comparison) over a period of 2 decades.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#read csv data from Our World In Data CO2 Emissions GitHub
url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
df = pd.read_csv(url)

#clean up the data by stripping any whitespace and extra characters
df['iso_code'] = (df['iso_code'].astype(str).str.strip().str.replace("'", "", regex=False).str.upper())

#filter out regions and aggregates which have NAN or long codes
#country codes usually have 3-letter codes
countries = df[(df['iso_code'].str.len() == 3) & (df['iso_code'] != 'NAN')] 

latestYear = countries['year'].max() #find the most recent year that data is available, which is 2023

top10 = countries[countries['year'] == latestYear]
top10 = top10.sort_values('co2', ascending=False).head(10) #sort values in descending order and take top 10

#part 2 of the project: focus on top 5 emittors + add Canada into the mix :)
target = ['United States', 'China', 'India', 'Russia', 'Japan', 'Canada']

#filter dataframe for entries from target countries spanning the last 2 decades
df_filtered = df[df['country'].isin(target) & (df['year'] >= 2003)]

#pivot per capita CO2 data
pivot_df = df_filtered.pivot(index='year', columns='country', values='co2_per_capita')

#place both plots into the same window
figure, axis = plt.subplots(2, 1)

#plot top 10 CO2 emitters in the most recent year of data
#note: the variable used for comparison here does not include land-use change (e.g. increasing deforestation)
axis[0].bar(top10['country'], top10['co2'], color='purple')
axis[0].set_title(f'Top 10 CO₂ Emitters in {latestYear}')
axis[0].set_ylabel('Emissions (million tonnes)')

#plot change in co2 emissions over last 2 decades of countries of interest
axis[1].xaxis.set_major_locator(ticker.MaxNLocator(integer=True)) #make sure ticks are ints
pivot_df.plot(marker='o', linewidth=2, ax=axis[1])
axis[1].set_title("CO₂ Emissions Per Capita — 2003 to 2023")
axis[1].set_xlabel("Year")
axis[1].set_ylabel("CO₂ Emissions (tonnes per person)")
axis[1].grid(True, linestyle='--', alpha=0.5)
axis[1].legend(title="Country")

plt.tight_layout()
plt.show()
