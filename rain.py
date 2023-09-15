import os

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd


def plot_tampere_and_circles(tampere_lat, tampere_lon, circle_params_list, time=None, max_magnitude=None):
    plt.figure(figsize=(10, 8))
    # Create a Basemap centered around Tampere
    m = Basemap(
        projection='merc',
        llcrnrlat=59.5, urcrnrlat=63.5,
        llcrnrlon=20.0, urcrnrlon=29.0,
        resolution='i'
    )

    # Draw the coastlines and fill the continents
    m.drawcoastlines(color='gray')
    m.drawcountries()
    m.fillcontinents(color='#BFE1C7', lake_color='#A2BFF7')

    # Draw parallels and meridians
    m.drawparallels(range(59, 65, 1), labels=[1, 0, 0, 0])
    m.drawmeridians(range(20, 30, 1), labels=[0, 0, 0, 1])

    # Convert Tampere coordinates to Basemap coordinates
    x, y = m(tampere_lon, tampere_lat)

    # Plot a marker for Tampere
    m.plot(x, y, 'rH', markersize=8, label='Hannulankatu')

    # Plot each circle from the list
    for circle_params in circle_params_list:
        # Extract circle parameters from the dictionary
        data_lat = circle_params['data_lat']
        data_lon = circle_params['data_lon']
        radius = circle_params['magnitude']

        # Convert data coordinates to Basemap coordinates
        x_data, y_data = m(data_lon, data_lat)

        circle = plt.Circle((x_data, y_data), radius, color='b', alpha=0.5, label=circle_params['name'])
        plt.gca().add_patch(circle)

    # Add a title
    plt.title(f'Suurin sademäärä klo {time}: {max_magnitude} mm/h')
    plt.legend()
    plt.show()


# The wanted reference address
tampere_lat = 61.493375
tampere_lon = 23.885709

folder = 'rain_images'

places = ['harmala', 'hattula', 'juupajoki', 'tulkkila', 'lahti', 'jamsa']
harmala = pd.read_csv('raw_data/harmala.csv')
all_data = harmala[['Vuosi', 'Kk', 'Pv', 'Klo']].astype(str)
all_data['datetime'] = all_data['Pv'] + '.' + all_data['Kk'] + '.' + all_data['Vuosi'] + ' ' + all_data['Klo']

for place in places:
    df = pd.read_csv(f'raw_data/{place}.csv')
    all_data[f'rain_{place}'] = df['Sademäärä (mm)']

mag_cols = [col for col in all_data.columns if 'rain' in col]

for timestamp in all_data.index:
    circle_params_list = [
        {
            'data_lat': 61.4701,
            'data_lon': 23.7419,
            'magnitude': all_data.loc[timestamp, 'rain_harmala'] * 6000,
            'name': 'Harmala'
        },
        {
            'data_lat': 61.1187,
            'data_lon': 24.3399,
            'magnitude': all_data.loc[timestamp, 'rain_hattula'] * 6000,
            'name': 'Hattula'
        },
        {
            'data_lat': 61.8446,
            'data_lon': 24.2885,
            'magnitude': all_data.loc[timestamp, 'rain_juupajoki'] * 6000,
            'name': 'Juupajoki'
        },
        {
            'data_lat': 61.2583,
            'data_lon': 22.3551,
            'magnitude': all_data.loc[timestamp, 'rain_tulkkila'] * 6000,
            'name': 'Tulkkila'
        },
        {
            'data_lat': 60.9776,
            'data_lon': 25.6242,
            'magnitude': all_data.loc[timestamp, 'rain_lahti'] * 6000,
            'name': 'Lahti'
        },
        {
            'data_lat': 61.8587,
            'data_lon': 24.8195,
            'magnitude': all_data.loc[timestamp, 'rain_jamsa'] * 6000,
            'name': 'Jämsä'
        }
    ]
    t = all_data.loc[timestamp, 'Klo'][:2]
    m = int(all_data.loc[timestamp, mag_cols].max())
    plot_tampere_and_circles(tampere_lat, tampere_lon, circle_params_list, time=t, max_magnitude=m)
    # break  # this shows the first plot
    filename = os.path.join(folder, f'frame_{timestamp:04d}.png')
    plt.savefig(filename)
    plt.close()

print('Total rain of the day in mm')
print(all_data[mag_cols].sum())
