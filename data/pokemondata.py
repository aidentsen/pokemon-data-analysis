import pokebase as pb


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
    generation_start_dict = {
        1: 1,
        2: 152,
        3: 252,
        4: 387,
        5: 494,
        6: 650,
        7: 722,
        8: 810,
        9: 906
    }
    non_standard_starters = ["pikachu", "eevee"]
    pseudo_base_forms = [
        'dratini', 'larvitar', 'bagon', 'beldum', 'gible', 'deino', 'goomy', 'jangmo-o', 'dreepy', 'frigibax'
    ]

    def __init__(self, dex_num, pokemon_variety=None):
        # Set the Pokémon and Pokémon Species endpoints, since most other properties are derived from them
        if pokemon_variety is None:
            self.pokemon_data = pb.pokemon(dex_num)
            self.species_data = pb.pokemon_species(dex_num)
        else:  # For when a Pokémon ID is given, helpful for alternate variations
            self.pokemon_data = pb.pokemon(pokemon_variety)
            self.species_data = pb.pokemon_species(self.pokemon_data.species.name)

        # Basic useful Pokémon information
        self.dex_num = dex_num
        self.name = self.pokemon_data.name
        self.generation = self.get_generation()
        self.types = [pokemon_type.type.name for pokemon_type in self.pokemon_data.types]
        self.abilities, self.hidden_ability = self.get_abilities()
        self.varieties = self.get_varieties()

        # Supplemental Pokémon information
        self.female_rate = self.species_data.gender_rate  # Note: in eighths, genderless Mons will give the value -1
        self.has_gender_differences = self.species_data.has_gender_differences
        self.capture_rate = self.species_data.capture_rate
        self.growth_rate = self.species_data.growth_rate
        self.base_happiness = self.species_data.base_happiness

        # Egg information
        self.hatch_counter = self.species_data.hatch_counter
        self.egg_groups = [egg_group.name for egg_group in self.species_data.egg_groups]

        # Stats
        self.hp, self.attack, self.defense, self.sp_attack, self.sp_defense, self.speed = self.get_stats()

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
        self.is_mega = "mega" in self.name
        self.is_gmax = "gmax" in self.name

        # Appearance and dimensions
        self.color = self.species_data.color.name
        self.shape = self.species_data.shape.name
        self.height_m = self.pokemon_data.height / 10.0
        self.weight_kg = self.pokemon_data.weight / 10.0

    def get_generation(self):
        generation_string = self.species_data.generation.name
        return PokemonData.generation_dict[generation_string]

    def get_abilities(self):
        normal_abilities = []
        hidden_ability = None

        for pokemon_ability in self.pokemon_data.abilities:
            if not pokemon_ability.is_hidden:
                normal_abilities.append(pokemon_ability.ability.name)
            else:
                hidden_ability = pokemon_ability.ability.name
        return normal_abilities, hidden_ability

    def get_varieties(self):
        varieties = []
        varieties_data = self.species_data.varieties
        for variety in varieties_data:
            if self.name != variety.pokemon.name:  # We don't want to include the variety of Pokémon already present
                pokemon_id = int(variety.pokemon.url.strip('/').split('/')[-1])
                pokemon_name = pb.pokemon(pokemon_id).name
                varieties.append(pokemon_name)
        return varieties

    def get_primary_ability(self):
        return self.pokemon_data.abilities[0].ability.name

    def get_stats(self):
        stat_dict = dict()
        stat_object = self.pokemon_data.stats
        for stat in stat_object:
            stat_dict[stat.stat.name] = stat.base_stat
        return (
            stat_dict['hp'],
            stat_dict['attack'],
            stat_dict['defense'],
            stat_dict['special-attack'],
            stat_dict['special-defense'],
            stat_dict['speed']
        )

    def get_evolutionary_stage(self):
        # Get details on the Pokémon's evolutionary chain
        evo_chain_id = self.species_data.evolution_chain.id
        evo_chain = pb.evolution_chain(evo_chain_id)

        if self.evolves_from is None:  # Either a single-stage or unevolved Pokémon
            if not evo_chain.chain.evolves_to:  # Single-stage Pokémon
                return -1
            else:  # Unevolved Pokémon
                return 0
        else:  # First evolution or second evolution
            first_evolution_names = [evolution.species.name for evolution in evo_chain.chain.evolves_to]
            if self.name in first_evolution_names:  # First evolution
                return 1
            else:  # There are only second evolution Pokémon remaining, since there are no four-stage evolution lines
                return 2

    def id_is_starter(self):
        # Need to account for non-standard starters (e.g. Pikachu and Eevee)
        if self.name in PokemonData.non_standard_starters:
            return True

        # Find the first Pokémon in the same Generation as this Mon
        generation_dex_num_start = PokemonData.generation_start_dict[self.generation]
        if self.generation == 5:  # Account for Victini
            generation_dex_num_start += 1

        position_in_generation = self.dex_num - generation_dex_num_start
        return 0 <= position_in_generation <= 8  # The standard starters are always in the first nine Mons of a Gen

    def id_is_pseudo(self):
        evolution_chain_id = self.species_data.evolution_chain.id
        unevolved_form_name = pb.evolution_chain(evolution_chain_id).chain.species.name
        return unevolved_form_name in PokemonData.pseudo_base_forms

    def id_is_ultra_beast(self):
        # All UBs have Beast Boost as their primary Ability, and no Mons with other Abilities are counted
        return self.get_primary_ability() == "beast-boost"

    def id_is_paradox(self):
        # Koraidon and Miraidon count as Paradox Mons, so their Abilities are also included here
        return self.get_primary_ability() in ("protosynthesis", "quark-drive", "orichalcum-pulse", "hadron-engine")

    def to_dict(self):
        return {
            'dex_num': self.dex_num,
            'name': self.name,
            'generation': self.generation,
            'types': " ".join(self.types),
            'abilities': self.abilities,
            'varieties': " ".join(self.varieties),

            'female_rate': self.female_rate,
            'has_gender_differences': self.has_gender_differences,
            'capture_rate': self.capture_rate,
            'growth_rate': self.growth_rate,
            'base_happiness': self.base_happiness,

            'hatch_counter': self.hatch_counter,
            'egg_groups': " ".join(self.egg_groups),

            'hp': self.hp,
            'attack': self.attack,
            'defense': self.defense,
            'sp_attack': self.sp_attack,
            'sp_defense': self.sp_defense,
            'speed': self.speed,

            'evolves_from': self.evolves_from,
            'evolutionary_stage': self.evolutionary_stage,

            'is_starter': self.is_starter,
            'is_pseudo': self.is_pseudo,
            'is_legendary': self.is_legendary,
            'is_mythical': self.is_mythical,
            'is_baby': self.is_baby,
            'is_ultra_beast': self.is_ultra_beast,
            'is_paradox': self.is_paradox,
            'is_mega': self.is_mega,
            'is_gmax': self.is_gmax,

            'color': self.color,
            'shape': self.shape,
            'height_m': self.height_m,
            'weight_kg': self.weight_kg
        }
