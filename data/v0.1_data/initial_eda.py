import pandas as pd
from matplotlib import pyplot as plt
# import seaborn as sns

df = pd.read_csv('pokemon_reindex.csv')

alpha_val = 0.4


def df_mons_of_a_given_type(pokemon_type):
    return df[(df['type1'] == pokemon_type) | (df['type2'] == pokemon_type)]


grass_mons = df_mons_of_a_given_type('grass')
fire_mons = df_mons_of_a_given_type('fire')
water_mons = df_mons_of_a_given_type('water')
electric_mons = df_mons_of_a_given_type('electric')

plt.hist(grass_mons.base_total, color='green', alpha=alpha_val, label='Grass', density=True)
plt.hist(water_mons.base_total, color='blue', alpha=alpha_val, label='Water', density=True)
plt.hist(fire_mons.base_total, color='red', alpha=alpha_val, label='Fire', density=True)
plt.hist(electric_mons.base_total, color='yellow', alpha=alpha_val, label='Electric', density=True)

plt.title('BST proportions for the starter types')
plt.xlabel('Base Stat Total')
plt.ylabel('Proportion')
plt.axis((160, 800, 0, 0.005))

plt.legend()
plt.savefig('starter_type_bst_proportions.png')
plt.show()
plt.close()
