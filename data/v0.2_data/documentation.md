# v0.2 Data Documentation

Documentation of the evolution of dataset creation based on data collection with [Greg Hilmes' pokebase](https://github.com/PokeAPI/pokebase), which is an interface for the RESTful Pokémon API, [PokeAPI](https://pokeapi.co/)

## Initial look at PokeAPI

Contains much more detail than is present in the dataset I was previously looking at, including well-separated details on Pokémon varieties. Notably, not all of it is straightforwardly accessible, requiring calls to either the Pokémon instance or the Pokémon_Species instance rather than just one. Still, much of what I'm interested in collecting can be relatively trivially accessed and formatted accordingly

That being said, there is still some data categories I will have to either collect or process myself, namely:
- Evolutionary stage
- Status markers for the following:
  - Starters
  - Pseudo-legendary Pokémon
  - Ultra Beasts
  - Paradox Pokémon

## Edits following creation of Generation 1 Dataset 1
- Reformatting `types`, `varieties` and `egg_groups` from lists to space-separated strings
- Change in logic for `abilities` - presently all Pokémon have an empty list rather than their actual Abilities
- Logical error when evaluating `evolutionary_stage`: due to evaluating a Pokémon's name rather than its species, stage 1 variants would be automatically classed as having `evolutionary_stage` 2 rather than their actual evolutionary stage

## Edits following creation of Generation 1 Dataset 2
- Reformatting of the `abilities` column from list to space-separated string - neglected to do in initial run-through intended after the first dataset
- Inclusion of a Hidden Ability column (despite the data having been generated and assigned as an attribute, I neglected to export it in `PokemonData.toDict`)
- Update to logic to evaluate `evolutionary_stage` and `evolves_from` - due to initial refactoring attempts converting `evolves_from` into a string (and therefore the value not being `None`/falsy, the evolutionary stage for base form Pokémon would be evaluated as 2 rather than 0)
- Addition of an `is_totem` marker after noticing multiple Totem Pokémon, which should also be filterable out from standard Pokémon

## Edits following creation of full Pokémon Dataset
TBD
