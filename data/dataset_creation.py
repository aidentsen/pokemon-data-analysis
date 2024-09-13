import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from pokemondata import PokemonData

final_mon_dex_num = 1025
pokemon_list = []
error_log_file = 'pokemon_errors.txt'

start_time = datetime.now()


# To process a Pokémon and its varieties by dex number
def process_pokemon(dex_num, log_file):
    print(dex_num)  # For logging dataset collation progress
    pokemon_data = []

    original_variety = PokemonData(dex_num, log_file)
    pokemon_data.append(original_variety.to_dict())

    for variety in original_variety.varieties:
        print(dex_num, variety)  # For logging dataset collation progress
        additional_variety = PokemonData(dex_num, log_file)
        pokemon_data.append(additional_variety.to_dict())

    return dex_num, pokemon_data


with ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_pokemon, dex_num, error_log_file) for dex_num in range(1, final_mon_dex_num+1)]

    # Collect all results and sort by dex_num after gathering
    results = []
    for future in futures:
        dex_num, data = future.result()
        results.append((dex_num, data))

results.sort(key=lambda x: x[0])  # Sort by dex_num to preserve the original order

# Flatten the results and append all Pokémon data to the final list
for _, data in results:
    pokemon_list.extend(data)

df = pd.DataFrame(pokemon_list)
df.to_csv('pokemon_data.csv')

print(f"Total time taken: {datetime.now() - start_time}")
