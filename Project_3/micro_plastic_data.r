library(dplyr)
library(tidyverse)
library(janitor)


particle_df <- read_csv("particle_data.csv")

particle_df

# What columns do I need the most?
# Names = Species, Year, In vitro/in vivo, Experiment Type, Exposure Route, Selected Dose, 
# Effect, Broad Endpoint Category, Specific Endpoint Category, Endpoint, Level of Biological Organization, Polymer, Shape,
# Particle Length, Size Category

# Move those columns into a single df

micro_plastic_exposure <- particle_df %>% 
  mutate(
    Humans = ifelse(Species == "(Human) Homo sapiens", "Human", "Not-Human")
  ) %>%
  filter(Humans == "Human") %>% 
  select(Humans, Year, `Experiment Type`, `Exposure Route`, `Selected Dose`, Effect, `Broad Endpoint Category`,
         `Specific Endpoint Category`, Endpoint, `Level of Biological Organization`, Polymer, Shape, `Particle Length (μm)`, 
         `Size Category`)

# Check to make sure its only humans in the dataset
micro_plastic_exposure %>% 
  tabyl(Humans)


# Exploratory Data Analysis

target_cat <- micro_plastic_exposure %>% 
  filter(`Experiment Type` == "Particle Only")
target_cat

ggplot(target_cat, aes(x = `Broad Endpoint Category`, fill = Effect)) +
  geom_bar() +
  theme(element_text(size = 7))

# Checking to see what effect polymer type has
polymer_df <- micro_plastic_exposure %>% 
  group_by(Polymer)

polymer_df %>% 
  tabyl(Polymer, Effect) %>% 
  adorn_percentages('row')

ggplot(target_cat, aes(x = Polymer, fill = Effect)) +
  geom_bar()

# Polystyrene most prominent polymer w/ count > 1000 and a effect rate of 37%

# NEXT!!!: Check to see polystyrene effect on immune system

polystyrene_df <- target_cat %>% 
  filter(Polymer == "Polystyrene") 
  

ggplot(polystyrene_df, aes(x = `Broad Endpoint Category`, fill = Effect)) +
  geom_bar()

polystyrene_percents <- polystyrene_df %>% 
  tabyl(`Broad Endpoint Category`, Effect) %>% 
  adorn_percentages("row") %>% 
  adorn_pct_formatting()


polystyrene_percents <- polystyrene_percents %>% 
  rename(
    `Polystyrene Broad Endpoint Category` = `Broad Endpoint Category`,
    "No_Effect" = "No", 
    "Effected" = "Yes"
  ) %>% 
  mutate(
    Yes_num = as.numeric(sub("%", "", Effected)),
    No_num  = as.numeric(sub("%", "", No_Effect))
  ) %>% 
  mutate(rank_by_effect = rank(-Yes_num)) %>%  # negative for descending
  arrange(rank_by_effect)

ggplot(polystyrene_percents, aes(x = `Polystyrene Broad Endpoint Category`, y = Yes_num)) +
  geom_col(fill = "steelblue") +
  coord_flip() +  
  ylab("Percentage Effected by Polystyrene") +
  xlab("Category") +
  theme_minimal()

polystyrene_df %>% 
  tabyl()



### Respiratory Broad Endpoint ###

# Effecting Zo1 protein expression and Transepithelial electric resistance 100% of time 
# (caveat: only 2 data points for each endpoint)
respiratory_df <- polystyrene_df %>% 
  filter(`Broad Endpoint Category` == "Respiratory")




### Circulatory Broad Endpoint ###

# assigning circulatory endpoint as df
circulatory_df <- polystyrene_df %>% 
  filter(`Broad Endpoint Category` == "Circulatory")


# of Hemolysis endpoint 67% showed an effect
circulatory_df %>% 
  filter(Endpoint == "Hemolysis") %>% 
  tabyl(Effect)

# effects cell adhesion, cell adhesion, and cell aggregation 100% of time
circulatory_df %>% 
  filter(Endpoint == "Cell Adhesion") %>% 
  tabyl(Effect)
ggplot(circulatory_df, aes(x = Endpoint, fill = Effect)) +
  geom_bar()



### Metabolism Broad Endpoint ###

metabolism_df <- polystyrene_df %>% 
  filter(`Broad Endpoint Category` == "Metabolism")

metabolism_oxidative_stress_df <- metabolism_df %>% 
  filter(`Specific Endpoint Category` == "Oxidative Stress")

ggplot(metabolism_oxidative_stress_df, aes(x = Endpoint, fill = Effect)) +
  geom_bar()

# reactive oxygen species production highest level of effect from polystyrene
metabolism_oxygen_species_production <- metabolism_oxidative_stress_df %>% 
  filter(Endpoint == "Reactive Oxygen Species Production" )

metabolism_oxygen_species_production %>% 
  tabyl(Effect, Shape) %>% 
  adorn_percentages("row")

# mitochondrial membrane potential









