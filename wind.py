import os

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd


def plot_southern_finland_with_tampere_and_arrows(tampere_lat, tampere_lon, arrow_params_list, time=None, max_magnitude=None):
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

    # Plot each arrow from the list
    for arrow_params in arrow_params_list:
        # Extract arrow parameters from the dictionary
        data_lat = arrow_params['data_lat']
        data_lon = arrow_params['data_lon']
        direction = arrow_params['direction']
        magnitude = arrow_params['magnitude']

        # Convert data coordinates to Basemap coordinates
        x_data, y_data = m(data_lon, data_lat)

        # Calculate the endpoint of the arrow in Basemap coordinates
        arrow_end_x = x_data + np.sin(np.deg2rad(direction)) * magnitude
        arrow_end_y = y_data + np.cos(np.deg2rad(direction)) * magnitude

        # Plot the arrow
        m.quiver(
            x_data, y_data, arrow_end_x - x_data, arrow_end_y - y_data, angles='xy', scale_units='xy', scale=1,
            color='black', label=arrow_params['name'], width=0.01)

    # Add a title
    plt.title(f'Suurin tuulen nopeus klo {time}: {max_magnitude} m/s')
    plt.legend()
    # plt.show()


# The wanted reference address
tampere_lat = 61.493375
tampere_lon = 23.885709


folder = 'images'

places = ['siilinkari', 'pirkkala', 'katinen', 'halli']

# Initialize
siilinkari = pd.read_csv('raw_data/siilinkari.csv')
all_data = siilinkari[['Vuosi', 'Kk', 'Pv', 'Klo']].astype(str)
all_data['datetime'] = all_data['Pv'] + '.' + all_data['Kk'] + '.' + all_data['Vuosi'] + ' ' + all_data['Klo']

for place in places:
    df = pd.read_csv(f'raw_data/{place}.csv')
    all_data[f'direction_{place}'] = df['Tuulen suunta (deg)']
    all_data[f'magnitude_{place}'] = df['Tuulen nopeus (m/s)']

mag_cols = [col for col in all_data.columns if 'magnitude' in col]

for timestamp in all_data.index:
    arrow_params_list = [
        {
            'data_lat': 61.5177,
            'data_lon': 23.7542,
            'direction': all_data.loc[timestamp, 'direction_siilinkari'],
            'magnitude': all_data.loc[timestamp, 'magnitude_siilinkari'] * 20000,
            'name': 'Siilinkari'
        },
        {
            'data_lat': 61.4148,
            'data_lon': 23.6047,
            'direction': all_data.loc[timestamp, 'direction_pirkkala'],
            'magnitude': all_data.loc[timestamp, 'magnitude_pirkkala'] * 20000,
            'name': 'Pirkkala'
        },
        {
            'data_lat': 60.9987,
            'data_lon': 24.4987,
            'direction': all_data.loc[timestamp, 'direction_katinen'],
            'magnitude': all_data.loc[timestamp, 'magnitude_katinen'] * 20000,
            'name': 'Katinen'
        },
        {
            'data_lat': 61.8629,
            'data_lon': 24.8189,
            'direction': all_data.loc[timestamp, 'direction_halli'],
            'magnitude': all_data.loc[timestamp, 'magnitude_halli'] * 20000,
            'name': 'Halli'
        }
    ]
    t = all_data.loc[timestamp, 'Klo'][:2]
    m = int(all_data.loc[timestamp, mag_cols].max())
    plot_southern_finland_with_tampere_and_arrows(tampere_lat, tampere_lon, arrow_params_list, time=t, max_magnitude=m)
    break  # this shows the first plot
    filename = os.path.join(folder, f'frame_{timestamp:04d}.png')
    plt.savefig(filename)
    plt.close()
