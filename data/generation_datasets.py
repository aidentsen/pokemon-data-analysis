import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from pokemondata import PokemonData

# Initialise a lock for thread-safe file writing
log_lock = Lock()


def setup_logging(generation):
    """
    Sets up the logging structure with start time and log files for a specific generation
    """
    start_time = datetime.now()
    error_log_file = f'pokemon_errors_gen{generation}.txt'
    processing_log_file = f'pokemon_processing_gen{generation}.txt'
    output_file = f'pokemon_data_gen{generation}.csv'

    print(f"Processing for generation {generation} started at {start_time}")

    return start_time, error_log_file, processing_log_file, output_file


def process_pokemon_batch(dex_nums, error_file, process_varieties=True):
    """
    Processes a batch of Pokémon by dex numbers, including their varieties if process_varieties is set
    This function handles multiple Pokémon in one batch to reduce overhead
    """
    pokemon_data = []
    log_messages = []

    for dex_num in dex_nums:
        try:
            start_message = f"{datetime.now()}: starting {dex_num}"
            log_messages.append(start_message)
            print(start_message)

            original_variety = PokemonData(dex_num, error_file)
            pokemon_data.append(original_variety.to_dict())

            end_message = f"{datetime.now()}: finished {dex_num}"
            log_messages.append(end_message)
            print(end_message)

            if process_varieties:
                for variety in original_variety.varieties:
                    start_message = f"{datetime.now()}: starting {dex_num} {variety}"
                    log_messages.append(start_message)
                    print(start_message)

                    # Passes the original variety's species_data in order to avoid duplicated API calls
                    additional_variety = PokemonData(variety, error_file, original_variety.species_data)
                    pokemon_data.append(additional_variety.to_dict())

                    end_message = f"{datetime.now()}: finished {dex_num} {variety}"
                    log_messages.append(end_message)
                    print(end_message)

        except Exception as e:
            error_message = f"Error processing {dex_num}: {str(e)}"
            log_messages.append(error_message)
            print(error_message)

    return pokemon_data, log_messages


def process_pokemon_in_batches(start, end, error_log, process_varieties, batch_size=10):
    """
    Manages multithreading to process Pokémon in batches concurrently
    Each thread will handle a batch of Pokémon to reduce thread management overhead
    """

    results = []
    log_buffer = []

    # Split Pokémon into batches
    dex_nums = list(range(start, end))
    batches = [dex_nums[i:i + batch_size] for i in range(0, len(dex_nums), batch_size)]

    with ThreadPoolExecutor(max_workers=8) as executor:  # Limit to 8 threads for Pokémon processing
        futures = {executor.submit(process_pokemon_batch, batch, error_log, process_varieties): batch for batch in
                   batches}

        for future in as_completed(futures):
            pokemon_data, logs = future.result()
            results.extend(pokemon_data)
            log_buffer.extend(logs)

    return results, log_buffer


def write_logs(log_messages, log_file):
    """
    Writes log messages to the log file
    """
    with log_lock:
        with open(log_file, 'a') as file_manager:
            file_manager.write("\n".join(log_messages) + "\n")


def save_to_csv(pokemon_list, output_file):
    """
    Saves the Pokémon data to a CSV file
    """
    df = pd.DataFrame(pokemon_list).sort_values('dex_num')
    df.to_csv(output_file, index=False)


def process_generation(generation, handle_varieties=True, batch_size=10):
    """
    Processes a given Pokémon generation by running the necessary functions for that generation
    Includes exception handling to ensure issues don't crash the entire program
    """

    try:
        # Get the first and last dex number for the generation
        first_num = PokemonData.generation_start_dict[generation]
        final_num = PokemonData.generation_start_dict.get(generation + 1, 1026)  # Default value is 1025 + 1

        # Setup logging for this generation
        start_time, error_log_file, processing_log_file, output_file = setup_logging(generation)

        # Process Pokémon in batches using multithreading
        pokemon_list, log_buffer = process_pokemon_in_batches(first_num, final_num, error_log_file, handle_varieties,
                                                              batch_size)

        finish_time = f"Finished generation {generation} in {datetime.now() - start_time}"
        print(finish_time)
        log_buffer.append(finish_time)

        # Write logs and save results to CSV
        write_logs(log_buffer, processing_log_file)
        save_to_csv(pokemon_list, output_file)

    except Exception as e:
        # Log the error specific to this generation
        error_message = f"Error processing generation {generation}: {str(e)}"
        print(error_message)

        # Ensure the error is written to the generation-specific error log file
        with open(f'pokemon_errors_gen{generation}.txt', 'a') as error_file:
            error_file.write(f"{datetime.now()}: {error_message}\n")


def process_multiple_generations_in_parallel(generations, handle_varieties=True, batch_size=10, max_workers=4):
    """
    Processes multiple generations of Pokémon in parallel using threading
    Each generation is processed independently, with exceptions handled locally
    The number of threads for generations is controlled by max_workers
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:  # Limit the number of threads for generations
        futures = {executor.submit(process_generation, generation, handle_varieties, batch_size): generation for
                   generation in generations}

        for future in as_completed(futures):
            generation = futures[future]
            try:
                future.result()  # This will raise any exception encountered during processing
                print(f"Generation {generation} completed successfully.")
            except Exception as e:
                print(f"Error processing generation {generation}: {e}")


if __name__ == "__main__":
    # generations_to_process = [3, 4]
    # process_multiple_generations_in_parallel(generations_to_process, batch_size=10, max_workers=2)

    process_generation(3)
