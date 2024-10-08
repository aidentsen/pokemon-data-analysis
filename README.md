# Pokémon Data Analysis Project

## Description
An independent Python data science project, starting with data collection and collation. All stages will be logged on GitHub as the project progresses

Stages of the project thus far:
- v0.1: attempts to use the data from [Rounak Banik's The Complete Pokémon Dataset](https://www.kaggle.com/datasets/rounakbanik/pokemon)
- v0.2: independent dataset creation using [Greg Hilmes' pokebase](https://github.com/PokeAPI/pokebase), which is an interface for the RESTful Pokémon API, [PokeAPI](https://pokeapi.co/)

## Post-dataset creation questions to explore

Exploratory
- Stats by Pokémon type and by evolutionary stage
- What are the Pokémon with the greatest/fewest number of type weaknesses?
- What are the Pokémon with the greatest number of immunities/4x type weaknesses? - account for potential abilities
- Which type has the best coverage overall?
- Which Pokémon types/type combinations are the weakest and strongest defensively, when:
  - Just looking at each type, weighting all equally?
  - Weighting by type distribution, operating under the assumption that each Pokémon learns a STAB move?
- When accounting for the distribution of the different types of attacking moves among all the various Pokémon species, which type is weakest defensively, and which is strongest?

Predictive
- Can you predict if a Pokémon is a pseudo/legendary/mythical/baby/starter/etc?
- Based on a Pokémon's stats and known evolutionary stage, can you predict the Pokémon's type?
- Based on a Pokémon's stats, can you predict its evolutionary stage?

Generative: given certain parameters, can you generate a sample stat spread?
E.g. "Give me a stat spread for a base form Electric-Type Pokémon"

Displaying findings on GitHub Pages

## Installation and technologies
Python code written in Python 3.12

External libraries installed and used (can be installed with pip):
- Pandas: v2.2.2
- Matplotlib: v3.9.2
- Seaborn: v0.13.2

Data collection was done with [Greg Hilmes' pokebase](https://github.com/PokeAPI/pokebase) (can be installed with `pip install pokebase` for a version that supports Python 3.6 onward), which is an interface for the RESTful Pokémon API, [PokeAPI](https://pokeapi.co/)

## License
Copyright 2024 Aiden Tsen. Licensed under the Educational Community License, Version 2.0 (the “License”); you may not use this file except in compliance with the License. You may obtain a copy of the License at [https://www.osedu.org/licenses/ECL-2.0](https://www.osedu.org/licenses/ECL-2.0). Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.