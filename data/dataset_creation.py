import pokebase as pb
import numpy as np
# import pandas as pd


class PokemonData:
    # Details subject to change with personal definition/time as more games come out, so here for ease of editing
    generation_dict = {
        "generation-i": 1,
        "generation-ii": 2,
        "generation-iii": 3,
        "generation-iv": 4,
        "generation-v": 5,
        "generation-vi": 6,
        "generation-vii": 7,
        "generation-viii": 8,
        "generation-ix": 9
    }
    non_standard_starters = ["pikachu", "eevee"]
    pseudo_base_forms = [
        'dratini', 'larvitar', 'bagon', 'beldum', 'gible', 'deino', 'goomy', 'jangmo-o', 'dreepy', 'frigibax'
    ]

    def __init__(self, dex_num):
        # Set the Pokémon and Pokémon Species endpoints, since most other properties are derived from them
        # Note that these are NOT the same! 413 gives Wormadam and Wormadam-G, respectively
        self.species_data = pb.pokemon_species(dex_num)
        self.pokemon_data = pb.pokemon(dex_num)

        # Basic useful Pokémon information
        self.dex_num = dex_num
        self.name = self.pokemon_data.name
        self.generation = self.get_generation()
        self.types = np.array([pokemon_type.type.name for pokemon_type in self.pokemon_data.types])
        self.abilities, self.hidden_ability = self.get_abilities()
        self.varieties = self.get_varieties()

        # Supplemental Pokémon information
        self.female_rate = self.species_data.gender_rate  # Note: genderless Mons will give the value -1
        self.has_gender_differences = self.species_data.has_gender_differences
        self.capture_rate = self.species_data.capture_rate
        self.growth_rate = self.species_data.growth_rate
        self.base_happiness = self.species_data.base_happiness

        # Egg information
        self.hatch_counter = self.species_data.hatch_counter
        self.egg_groups = np.array([egg_group.name for egg_group in self.species_data.egg_groups])

        # Stats
        STATS

        # Evolution data
        self.evolves_from = self.species_data.evolves_from_species
        self.evolutionary_stage = self.get_evolutionary_stage()

        # Category markers - methods written where the data is not naturally present in the API
        self.is_starter = self.id_is_starter()
        self.is_pseudo = self.id_is_pseudo()
        self.is_legendary = self.species_data.is_legendary
        self.is_mythical = self.species_data.is_mythical
        self.is_baby = self.species_data.is_baby
        self.is_ultra_beast = self.id_is_ultra_beast()
        self.is_paradox = self.id_is_paradox()

        # Appearance and dimensions
        self.colors = self.species_data.colors
        self.shape = self.species_data.shape
        self.height_m = self.pokemon_data.height / 10.0
        self.weight_kg = self.pokemon_data.weight / 10.0

    def get_generation(self):
        generation_string = self.species_data.generation.name
        return PokemonData.generation_dict[generation_string]

    def get_abilities(self):
        normal_abilities = np.array([])
        hidden_ability = None

        for pokemon_ability in self.pokemon_data.abilities:
            if not pokemon_ability.is_hidden:
                np.append(normal_abilities, pokemon_ability.ability.name)
            else:
                hidden_ability = pokemon_ability.ability.name
        return normal_abilities, hidden_ability

    def get_primary_ability(self):
        return self.pokemon_data.abilities[0].ability.name

    def get_evolutionary_stage(self):
        # Essentially go back through the evolves_from tree. There will be some need to also go forward
        pass

    def id_is_starter(self):
        # Need to account for non-standard starters (e.g. Pikachu and Eevee)
        if self.name in PokemonData.non_standard_starters:
            return True

        # Find the first Pokémon in the same Generation as this Mon
        generation_dex_num_start = pb.generation(self.generation).pokemon_species[0].id
        if self.generation == 5:  # Account for Victini
            generation_dex_num_start += 1

        position_in_generation = self.dex_num - generation_dex_num_start
        return 0 <= position_in_generation <= 8  # The standard starters are always in the first nine Mons of a Gen

    def id_is_pseudo(self):
        evolution_chain = self.species_data.evolution_chain.url
        base_form_id = int(evolution_chain.strip('/').split('/')[-1])  # Isolate the base from Dex Number
        return pb.pokemon(base_form_id).name in PokemonData.pseudo_base_forms

    def id_is_ultra_beast(self):
        # All UBs have Beast Boost as their primary Ability, and no Mons with other Abilities are counted
        return self.get_primary_ability() == "beast-boost"

    def id_is_paradox(self):
        # Koraidon and Miraidon count as Paradox Mons, so their Abilities are also included here
        return self.get_primary_ability() in ("protosynthesis", "quark-drive", "orichalcum-pulse", "hadron-engine")
