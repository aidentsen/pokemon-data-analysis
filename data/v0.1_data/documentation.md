# v0.1 Data Documentation

Documentation for posterity from the initial stages of the project, where I intended to analyse [Rounak Banik's The Complete Pokémon Dataset](https://www.kaggle.com/datasets/rounakbanik/pokemon)

## Description of tasks
- [Reindexing of columns](https://github.com/aidentsen/pokemon-data-analysis/blob/main/data/v0.1_data/reindexing.py) to an order I find more understandable (dataset columns are alphabetically ordered, rather than in a way that would make sense to a human viewer)
- [Initial attempts at exploratory data analysis](https://github.com/aidentsen/pokemon-data-analysis/blob/main/data/v0.1_data/initial_eda.py) in the form of exploring the Base Stat Total spread of the starter type Pokémon

![Histogram of the Base Stat Total spreads of Grass, Fire, Water and Electric-Type Pokémon](http://url/to/https://github.com/aidentsen/pokemon-data-analysis/blob/main/data/v0.1_data/starter_type_bst_proportions.png)

## Reasons for changes to next version

At this point, I realised that the dataset was not suitable for my purposes, because it:
- It only covers up to the end of Gen 7, thus lacking a great deal of info for analysis (as of Gen 9, there are 1025 unique species)
- It lacked some information I wanted, such as baby status, evolution information, mythical status etc
- It seemed like I was going to have to do a lot of data cleaning anyway due to improper handling of Regional Formes etc

As a result, the scope of this project now includes making use of APIs and API interfaces to construct a suitable dataset for my purposes entirely on my own, with the help of:
- [PokeAPI](https://pokeapi.co/)
- [pokebase: a Python interface for PokeAPI](https://github.com/PokeAPI/pokebase)