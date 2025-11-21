# 🌋 Toward an Integrated Particulate Load Metric for Human Exposure in Hawai‘i

> Modeling multi-source particulate burdens from volcanoes, wildfires, urban pollution, and plastics — across air, water, and behavioral pathways.


<img width="1080" height="668" alt="image" src="https://github.com/user-attachments/assets/5fde9d47-7c6a-4c4e-b83d-238475817b6b" />

## 🧪 Project Overview

This project develops a prototype **Particulate Load Index (PLI)** to quantify cumulative human exposure to airborne and ingestible particulate matter in Hawai‘i. Using open-source geospatial, environmental, and demographic data, we model how **volcanic emissions (VOG), wildfire smoke, urban air pollution, and marine microplastics** contribute to health risk — across multiple routes: **inhalation, ingestion, and dermal contact**.

Built for research, reproducibility, and public impact.

---

## 🔬 Research Objectives

- 📡 Ingest and harmonize multi-source environmental particulate data (VOG, PM2.5, microplastics)
- 🧍 Integrate demographic & behavioral exposure modifiers by age, occupation, housing, and mobility
- 🧠 Develop a machine-learning-based **Particulate Load Index (PLI)** to quantify cumulative burden
- 🗺️ Visualize spatial variations in PLI across Hawai‘i, enabling community and scientific insight

---

## 📊 Data Sources

| Source | Description |
|--------|-------------|
| 🛰️ **NASA FIRMS** | Wildfire and smoke plume detection |
| 🧯 **AirNow & PurpleAir** | PM2.5, SO₂, and AQI from ground monitors |
| 🌋 **USGS HVO** | Volcanic SO₂ flux (Kīlauea, Mauna Loa) |
| 🌊 **JAMSTEC** | Global microplastic ocean models |
| 🏘️ **U.S. Census & ACS** | Demographics, housing, occupation |
| 🌴 **BRFSS (HI)** | Health behaviors and outdoor activity |
| 🏨 **Tourism Authority** | Visitor density & transient exposure |
| 🛰️ **NLCD / LandSat** | Land use and impervious surfaces |

> See [data/README.md](data/README.md) for full metadata and access instructions.

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| `R` / `tidyverse` | Data wrangling, modeling, reproducibility |
| `sf`, `terra`     | Geospatial vector and raster analysis |
| `xgboost`, `DALEX` | Machine learning + explainability |
| `targets`, `renv` | Pipeline management + reproducibility |
| `Shiny` / `mapgl` | Interactive exploration dashboard |
| Docker + GitHub Actions | Optional: reproducible deployment |

---

## 🌍 Project Structure

```bash
📦 Particulate-Load-Index
├── 📁 data/              # Raw and cleaned datasets
├── 📁 R/                 # Scripts and modular functions
├── 📁 notebooks/         # RMarkdown/Quarto analysis notebooks
├── 📁 dashboard/         # Shiny or Streamlit app (to be developed)
├── 📁 figures/           # Output plots and maps
├── 📄 README.md          # You are here
└── 📄 LICENSE            # MIT



