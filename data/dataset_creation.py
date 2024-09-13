import pandas as pd
from datetime import datetime

from pokemondata import PokemonData

pokemon_list = []
final_mon_dex_num = 1025

start_time = datetime.now()

for dex_num in range(1, final_mon_dex_num + 1):
    print(dex_num)  # For logging dataset collation progress

    original_variety = PokemonData(dex_num)
    pokemon_list.append(original_variety.to_dict())

    for variety in original_variety.varieties:  # Logs Pokémon varieties (e.g. Wormadam-Grass, Mega Evolutions)
        print(dex_num, variety)  # For logging dataset collation progress

        additional_variety = PokemonData(variety)
        pokemon_list.append(additional_variety.to_dict())

df = pd.DataFrame(pokemon_list)
df.to_csv('pokemon_data.csv')

print(f"Total time taken: {datetime.now() - start_time}")
