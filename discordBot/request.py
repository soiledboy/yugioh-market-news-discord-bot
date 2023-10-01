import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates

def get_prices(productId, date_range,rarity = None ):


    if rarity:
        url = f'https://tier1marketspace.pythonanywhere.com/prices/{productId}/{int(date_range)}/{rarity}'
    else:
        url = f'https://tier1marketspace.pythonanywhere.com/prices/{productId}/{int(date_range)}'


    # Define the URL for the endpoint
    #url = 'https://tier1marketspace.pythonanywhere.com/prices/%s/%s' % (productId, int(date_range))
    print(url)

    # Make a GET request to the API
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON data from the response
        data = json.loads(response.text)
        df = pd.DataFrame(data)
        if df['market'].notna().any():
            # Extract imageUrl and tcgUrl from the DataFrame
            imageUrl = df.at[0, 'imageurl']  # assuming the URL is in the first row
            tcgUrl = df.at[0, 'tcgurl']  # assuming the URL is in the first row
            name = df.at[0,'name']


            ###MAKE PNG###

            df['date'] = pd.to_datetime(df['date'])

            # Calculate moving average with a window of 3
            df['ma'] = df['market'].rolling(window=3).mean()

            # Plotting
            fig, ax = plt.subplots(figsize=(10, 6))

            # Plot smoothed curve using moving average
            ax.plot(df['date'], df['ma'], color='royalblue', linewidth=3)

            # Adjusting tick label size
            ax.tick_params(axis='both', which='major', labelsize=14)

            # Format y-axis on the right side
            ax.yaxis.tick_right()
            formatter = FuncFormatter(lambda y, _: f"${y:.2f}")
            ax.yaxis.set_major_formatter(formatter)

            # Format x-axis for month and day
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

            # Turn off grid lines
            ax.grid(False)

            # Aesthetic modifications
            ax.set_facecolor('white')
            fig.set_facecolor('white')
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_color('#DDDDDD')
            ax.spines['right'].set_color('#DDDDDD')

            # Save as PNG
            plt.savefig('/home/tier1marketspace/discordBot/plots/%s_%d.png' % (productId,int(date_range)), dpi=300, bbox_inches='tight')
            #plt.show()

            print("done with plotting")

            png_path = '/home/tier1marketspace/discordBot/plots/%s_%d.png' % (productId, int(date_range))
            return {
                'type': 'pricing',
                'data': {
                    'png_path': png_path,
                    'imageUrl': imageUrl,
                    'tcgUrl': tcgUrl,
                    'name': name
                }
            }

        else:
            # We have multiple matching numbers
            print("matching values")
            return {
                'type': 'matching_numbers',
                'data': df
            }
    else:
        print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")









