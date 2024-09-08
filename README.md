# Pokémon Data Analysis Project

## Description
An independent Python data science project, which will be logged on GitHub as it develops, first from an exploratory angle

## Aspects to explore

Data collection and cleaning
- Possibly some things in the sample dataset that need to be handled
- Additional web scraping is required for information I would like, e.g.
  - Pseudo-legendary status
  - Evolutionary stage, including whether single stage
  - Evolution method

Exploratory
- Stats by Pokémon type
- What are the Pokémon with the greatest/fewest number of type weaknesses?
- What are the Pokémon with the greatest number of immunities/4x type weaknesses? - account for potential abilities

Predictive
- Can you predict if a Pokémon is a pseudo/legendary?
- Based on a Pokémon's stats and known evolutionary stage, can you predict the Pokémon's type?
- Based on a Pokémon's stats, can you predict its evolutionary stage?

Generative: given certain parameters (e.g. type and evolutionary stage), can you generate a sample stat spread?

Displaying findings on GitHub Pages

## Installation and technologies
Python code written in Python 3.12

External libraries installed and used (can be installed with pip):
- Pandas: v2.2.2
- Matplotlib: v3.9.2
- Seaborn: v0.13.2

Base dataset is [The Complete Pokémon Dataset by Rounak Banik](https://www.kaggle.com/datasets/rounakbanik/pokemon)

## License
Copyright 2024 Aiden Tsen. Licensed under the Educational Community License, Version 2.0 (the “License”); you may not use this file except in compliance with the License. You may obtain a copy of the License at [https://www.osedu.org/licenses/ECL-2.0](https://www.osedu.org/licenses/ECL-2.0). Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.