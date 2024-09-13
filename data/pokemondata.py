import pokebase as pb


class PokemonData:
    # Hardcoded, arbitrary details. Subject to change/personal interpretation, so here for ease of editing
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
    non_standard_starters = ["pikachu", "pikachu-starter", "eevee", "eevee-starter"]
    pseudo_base_forms = [
        'dratini', 'larvitar', 'bagon', 'beldum', 'gible', 'deino', 'goomy', 'jangmo-o', 'dreepy', 'frigibax'
    ]

    def __init__(self, pokemon, error_log_file):
        # The Pokédex number (413) and specific Pokémon name (e.g. 'wormadam-grass') both work

        # For logging errors during the process
        self.error_log_file = error_log_file

        try:
            # Set the Pokémon, Species and name, since these are important properties
            self.pokemon_data = pb.pokemon(pokemon)
            self.species_data = pb.pokemon_species(self.pokemon_data.species.name)
            self.name = self.pokemon_data.name
        except AttributeError:
            self.pokemon_data = "missing"
            self.species_data = "missing"
            self.name = pokemon
            self.log_error("initialisation")

        # Basic useful Pokémon information
        self.dex_num = self.safe_get_attr('id', self.species_data)
        self.name = self.safe_get_attr('name', self.pokemon_data)
        self.species = self.safe_get_attr('name', self.species_data)
        self.generation = self.safe_get_method(self.get_generation)
        self.types = self.safe_get_list('types', self.pokemon_data, lambda t: t.type.name)
        self.abilities, self.hidden_ability = self.safe_get_method(self.get_abilities, is_list=True)
        self.varieties = self.safe_get_method(self.get_varieties)

        # Supplemental Pokémon information
        self.female_rate = self.safe_get_attr('gender_rate', self.species_data)  # In eighths, genderless is -1
        self.has_gender_differences = self.safe_get_attr('has_gender_differences', self.species_data)
        self.capture_rate = self.safe_get_attr('capture_rate', self.species_data)
        self.growth_rate = self.safe_get_attr('growth_rate', self.species_data)
        self.base_happiness = self.safe_get_attr('base_happiness', self.species_data)

        # Egg information
        self.hatch_counter = self.safe_get_attr('hatch_counter', self.species_data)
        self.egg_groups = self.safe_get_list('egg_groups', self.species_data, lambda e: e.name)

        # Stats, including Base Stat Total
        self.hp, self.attack, self.defense, self.sp_attack, self.sp_defense, self.speed = self.safe_get_stats()
        try:
            self.bst = sum([self.hp, self.attack, self.defense, self.sp_attack, self.sp_defense, self.speed])
        except TypeError:
            self.bst = 'missing'

        # Evolution data - note evolutionary stage is -1 for single-stage, 0 for unevolved etc
        self.evolves_from = self.safe_get_attr('evolves_from_species', self.species_data)  # Can legally be None
        self.evolutionary_stage = self.safe_get_method(self.get_evolutionary_stage)

        # Category markers
        self.is_starter = self.safe_get_method(self.id_is_starter)
        self.is_pseudo = self.safe_get_method(self.id_is_pseudo)
        self.is_legendary = self.safe_get_attr('is_legendary', self.species_data)
        self.is_mythical = self.safe_get_attr('is_mythical', self.species_data)
        self.is_baby = self.safe_get_attr('is_baby', self.species_data)
        self.is_ultra_beast = self.safe_get_method(self.id_is_ultra_beast)
        self.is_paradox = self.safe_get_method(self.id_is_paradox)
        self.is_mega = "-mega" in self.name
        self.is_totem = "-totem" in self.name
        self.is_gmax = "-gmax" in self.name

        # Appearance - cannot legally be None, hence usage of is_obj even though name gets pulled by default
        self.color = self.safe_get_attr('color', self.species_data, is_obj=True)
        self.shape = self.safe_get_attr('shape', self.species_data, is_obj=True)

        # Dimensions: need to be evaluated before dividing for units
        self.height_m = self.safe_get_attr('height', self.pokemon_data)
        if self.height_m != 'missing':
            self.height_m /= 10.0
        self.weight_kg = self.safe_get_attr('weight', self.pokemon_data)
        if self.weight_kg != 'missing':
            self.weight_kg /= 10.0

    # Logging method for errors
    def log_error(self, field):
        if self.pokemon_data != "missing":  # Shouldn't run if there was an initialisation error
            with open(self.error_log_file, 'a') as log_file:
                log_file.write(f"Error with {self.name}: {field} could not be parsed\n")

    # Start of helper functions to log errors
    def safe_get_attr(self, attr, obj, is_obj=False):
        try:
            return getattr(obj, attr).name if is_obj else getattr(obj, attr)
        except AttributeError:
            self.log_error(attr)
            return "missing attribute"

    def safe_get_method(self, method, is_list=False):
        try:
            result = method()
            return result
        except AttributeError:
            self.log_error(method.__name__)
            return "missing attribute" if not is_list else ("missing attribute", "missing attribute")

    def safe_get_list(self, attr, obj, transform):
        try:
            return [transform(item) for item in getattr(obj, attr)]
        except AttributeError:
            self.log_error(attr)
            return "missing attribute"

    def safe_get_stat(self, index):
        try:
            return self.pokemon_data.stats[index].base_stat
        except AttributeError:
            self.log_error(f"stat_{index}")
            return "missing attribute"

    def safe_get_stats(self):
        try:
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
        except AttributeError:
            self.log_error("stats")
            return ["missing attribute"] * 6

    # Start of functions needed to get attributes
    def get_generation(self):  # Return the numerical Generation number
        generation_string = self.species_data.generation.name
        return PokemonData.generation_dict[generation_string]

    def get_abilities(self):  # Returns both normal and hidden Abilities
        normal_abilities = []
        hidden_ability = None

        for pokemon_ability in self.pokemon_data.abilities:
            if not pokemon_ability.is_hidden:  # Hidden Abilities are processed separately
                normal_abilities.append(pokemon_ability.ability.name)
            else:
                hidden_ability = pokemon_ability.ability.name

        return normal_abilities, hidden_ability

    def get_varieties(self):  # Find all the other varieties of the Pokémon
        varieties = []
        varieties_data = self.species_data.varieties
        for variety in varieties_data:
            if self.name != variety.pokemon.name:  # Excludes the variety of Pokémon already present
                pokemon_id = int(variety.pokemon.url.strip('/').split('/')[-1])
                pokemon_name = pb.pokemon(pokemon_id).name
                varieties.append(pokemon_name)
        return varieties

    def get_primary_ability(self):  # Used internally to help identify some Pokémon categories
        return self.pokemon_data.abilities[0].ability.name

    def get_evolutionary_stage(self):
        # Get details on the Pokémon's evolutionary chain
        evo_chain_id = self.species_data.evolution_chain.id
        evo_chain = pb.evolution_chain(evo_chain_id)

        if not self.evolves_from:  # Either a single-stage or unevolved Pokémon
            if not evo_chain.chain.evolves_to:  # Single-stage Pokémon
                return -1
            else:  # Unevolved Pokémon
                return 0
        else:  # First or second evolution
            first_evolution_names = [evolution.species.name for evolution in evo_chain.chain.evolves_to]
            if self.species in first_evolution_names:  # First evolution
                return 1
            else:  # Only second evolution Mons remaining, since there are no four-stage evolutions
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
        # Get the unevolved form of the Pokémon
        evolution_chain_id = self.species_data.evolution_chain.id
        unevolved_form_name = pb.evolution_chain(evolution_chain_id).chain.species.name

        # Determine if the unevolved form is in the list of unevolved pseudo-legendary Pokémon
        return unevolved_form_name in PokemonData.pseudo_base_forms

    def id_is_ultra_beast(self):
        # All UBs have Beast Boost as their primary Ability, and no Mons with other Abilities are counted
        return self.get_primary_ability() == "beast-boost"

    def id_is_paradox(self):
        # Koraidon and Miraidon count as Paradox Mons, so their Abilities are also included here
        return self.get_primary_ability() in ("protosynthesis", "quark-drive", "orichalcum-pulse", "hadron-engine")

    # Lots of repetition when handling attributes that can be lists, so turning it into a function
    def process_list_attr(self, attr):
        if isinstance(attr, list):
            return " ".join(attr)
        else:
            return attr

    # Returns a dictionary of all meaningful attributes. Any lists are converted into space-separated strings
    def to_dict(self):
        return {
            'dex_num': self.dex_num,
            'name': self.name,
            'species': self.species,
            'generation': self.generation,
            'types': self.process_list_attr(self.types),
            'abilities': self.process_list_attr(self.abilities),
            'hidden_ability': self.hidden_ability,
            'varieties': self.process_list_attr(self.varieties),

            'female_rate': self.female_rate,
            'has_gender_differences': self.has_gender_differences,
            'capture_rate': self.capture_rate,
            'growth_rate': self.growth_rate,
            'base_happiness': self.base_happiness,

            'hatch_counter': self.hatch_counter,
            'egg_groups': self.process_list_attr(self.egg_groups),

            'bst': self.bst,
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
            'is-totem': self.is_totem,
            'is_gmax': self.is_gmax,

            'color': self.color,
            'shape': self.shape,
            'height_m': self.height_m,
            'weight_kg': self.weight_kg
        }
