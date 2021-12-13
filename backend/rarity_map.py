"""
Generate HTML from CSV.

@author: EJacobsen
@author: mdigi14
@date: 12/12/2021

pip install --upgrade matplotlib

"""

import pandas
import matplotlib.pyplot as plt
import os


"""
Helper Functions
"""
# Generate Plot.
def save_graph(FILE, TOKEN_COL, FILE_PATH, SAVE_PATH):
    RARITY_DB = pandas.read_csv(FILE_PATH)
    RARITY_DB = RARITY_DB[RARITY_DB['TOKEN_ID'].duplicated() == False]
    if TOKEN_COL == 'TOKEN_NAME':
        RARITY_DB['TOKEN_ID'] = RARITY_DB['TOKEN_NAME'].str.split('#').str[1].astype(int)

    # Get upper & lower bounds.
    UPPER_BOUND = RARITY_DB.shape[0]
    LOWER_BOUND = RARITY_DB.iloc[RARITY_DB.sort_values('TOKEN_ID').index[0]].TOKEN_ID
    print (LOWER_BOUND)

    ax = RARITY_DB.plot.scatter(x='TOKEN_ID', y='Rank', grid=True, alpha=.25, title= "{} - Token ID vs Rank (low rank is more rare)".format(FILE), figsize=(14, 7))
    ax.set_xlabel("Token ID")
    ax.set_ylabel("Rarity Rank")

    plt.xlim(LOWER_BOUND, UPPER_BOUND)
    plt.ylim(0, UPPER_BOUND)
    plt.savefig(SAVE_PATH)

# Process rarity maps for folder.
def save_graphs(DATA_FOLDER, SAVE_FOLDER):
    for FILENAME in os.listdir(DATA_FOLDER):
        if FILENAME.endswith(".csv"):
            FILE = FILENAME.replace('_raritytools.csv', '')
            SAVE_PATH = f'{SAVE_FOLDER}\\{FILE}_scatterplot.png'
            save_graph(FILE, 'TOKEN_ID', os.path.join(DATA_FOLDER, FILENAME), SAVE_PATH)


"""
Update Parameters Here
"""
FILE = "quaks"
TOKEN_COL = 'TOKEN_ID'
WORKING_FOLDER = f'C:\\Users\\ejacobsen\\Downloads\\EJacobsen\\crypto_tools\\Convex Labs\\honestnft-shenanigans'
FILE_PATH = f'{WORKING_FOLDER}\\metadata\\rarity_data\\{FILE}_raritytools.csv'
SAVE_PATH = f'{WORKING_FOLDER}\\fair_drop\\scatterplots\\{FILE}_scatterplot.png'
DATA_FOLDER = f'{WORKING_FOLDER}\\metadata\\rarity_data'
SAVE_FOLDER = f'{WORKING_FOLDER}\\fair_drop\\scatterplots'

#save_graph(FILE, TOKEN_COL, FILE_PATH, SAVE_PATH)
save_graphs(DATA_FOLDER, SAVE_FOLDER)
