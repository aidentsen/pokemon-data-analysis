"""
Purpose: The Complete Pokémon Dataset (https://www.kaggle.com/datasets/rounakbanik/pokemon)...
1. Is not, in fact, complete for the purposes of what I would like to analyse
2. Has its columns in a way that I find unintuitive and confusing

This script addresses (2) by reindexing the columns, and is here to serve as documentation

Changes made:
1. Columns reindexed
2. japanese_name column dropped as not needed for my purposes
"""

import pandas as pd

df = pd.read_csv('pokemon.csv')

desired_order_columns = [
    'pokedex_number', 'generation', 'name', 'type1', 'type2', 'classification', 'abilities',
    'percentage_male', 'capture_rate', 'base_egg_steps', 'base_happiness', 'height_m', 'weight_kg',
    'base_total', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed',
    'against_bug', 'against_dark', 'against_dragon',
    'against_electric', 'against_fairy', 'against_fight', 'against_fire',
    'against_flying', 'against_ghost', 'against_grass', 'against_ground',
    'against_ice', 'against_normal', 'against_poison', 'against_psychic',
    'against_rock', 'against_steel', 'against_water'
]

df = df.reindex(desired_order_columns, axis=1)
print(df.columns)  # To confirm that the columns have been correctly reordered
print(df.head())

df.to_csv('pokemon_reindex.csv', index=False)
