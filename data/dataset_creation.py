import pokebase as pb
import pandas as pd

from pokemondata import PokemonData

rows_list = []

final_gen_1_mon_in_dataset = 151

for dex_num in range(1, final_gen_1_mon_in_dataset + 1):
    print(dex_num)
    original_variety = PokemonData(dex_num)
    rows_list.append(original_variety.to_dict())
    for variety in original_variety.varieties:
        print(dex_num, variety)
        additional_variety = PokemonData(variety)
        rows_list.append(additional_variety.to_dict())

df = pd.DataFrame(rows_list)
df.to_csv('gen_1_data.csv')
