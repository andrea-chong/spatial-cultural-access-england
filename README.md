# Thesis repository

This repository contains data, analysis notebooks, and helper scripts for the thesis project. The notebooks live in the `research_notebooks/` folder and expect a conda environment created from `environment.yml` and several manually-downloaded datasets placed into the `data/` directory.

### Quick start**

- **Create environment:** `conda env create -f environment.yml -n thesis-env`
- **Activate environment:** `conda activate thesis-env`
- **Open notebooks:** `jupyter lab` or open the files in VS Code and select the `thesis-env` kernel.

### Environment setup

1. Ensure you have conda (Anaconda/Miniconda) installed.
2. From the repository root run:

```
conda env create -f environment.yml -n thesis-env
conda activate thesis-env
```

If you modify or add packages later you can update the environment with:

```
conda env update -f environment.yml -n thesis-env
```

### Required data (manual downloads - TBC insert links to original datasources)

Place the following datasets into the `data/` directory before running the notebooks. Files prefixed with `[dep]` are deprecated and should be ignored.

- Local Authority District boundaries (GeoJSON): [data/Local_Authority_Districts_December_2023_Boundaries_UK_BFE_7168133065712352501.geojson](data/Local_Authority_Districts_December_2023_Boundaries_UK_BFE_7168133065712352501.geojson)
- Output Areas (CSV): [data/Output_Areas_2021_EW_BFC_V8_4917697649103143030.csv](data/Output_Areas_2021_EW_BFC_V8_4917697649103143030.csv)
- Output Area → Local Authority District lookup (CSV): [data/Output_Area_to_Local_Authority_District_(April_2023)_Lookup_in_England_and_Wales.csv](data/Output_Area_to_Local_Authority_District_(April_2023)_Lookup_in_England_and_Wales.csv)
- OA population centroids (GeoJSON): [data/OA_PopCentroids_EW_2021_V4.geojson](data/OA_PopCentroids_EW_2021_V4.geojson)

#### Intermediary saved data
- Small helper/validation files used in examples: [data/manual_validation_sample_labelled.csv](data/manual_validation_sample_labelled.csv)
- Pilot LAD (small GeoJSON): [data/pilot_lad.geojson](data/pilot_lad.geojson)
- UK Data Archive extract (tab folder): [data/UKDA-9350-tab](data/UKDA-9350-tab)

If any of the above are missing, the notebooks will indicate which file is required. Where possible the notebooks include small sample files under `data/` for quicker tests, but for full analyses you must supply the official datasets as listed above.

### Research notebooks

All notebooks are in the [research_notebooks](research_notebooks) folder. Deprecated notebooks are prefixed with `[dep]` and are not described below.

- [research_notebooks/01_google_places_new_data_collection.ipynb](research_notebooks/01_google_places_new_data_collection.ipynb): Collects and aggregates new Google Places data for points-of-interest. Includes rate-limited API collection routines and initial quality checks.
- [research_notebooks/02_eda_validation.ipynb](research_notebooks/02_eda_validation.ipynb): Exploratory data analysis and validation of the collected place data against ground truth and known metadata; produces summary tables and diagnostic plots used in the report.
- [research_notebooks/03_osm_validation.ipynb](research_notebooks/03_osm_validation.ipynb): Validates Google Places results against OpenStreetMap (OSM) extracts and compares coverage/attributes between sources.
- [research_notebooks/04_variable_construction.ipynb](research_notebooks/04_variable_construction.ipynb): Implements spatial joins, aggregation procedures, and constructs the predictor variables used for modelling (distance/proximity metrics, typologies, counts, etc.).
- [research_notebooks/05_modelling.ipynb](research_notebooks/05_modelling.ipynb): Contains model training, evaluation, and result summarisation. Reproducible training pipelines and performance metrics are included.

Each notebook has execution hints and the kernel dropdown points to the conda environment created from `environment.yml`.

### Scripts

The `scripts/` folder contains utility scripts and modules used by notebooks and experiments. Deprecated scripts prefixed with `[dep]` are omitted.

- [scripts/cf_typology.py](scripts/cf_typology.py): Utilities for computing and applying the classification/typology used in analyses. Functions include grouping POI types, creating categorical mappings, and summary helpers.
- [scripts/google_places_search.py](scripts/google_places_search.py): Thin wrapper around Google Places API calls used to search and retrieve place results. Includes retry logic, rate-limiting considerations, and helper functions to normalise API output for downstream processing.

**Reproducing results and tips**

- Run the notebooks in order if you're following the full pipeline: data collection → EDA → validation → variable construction → modelling.
- Large intermediate outputs (distance matrices, spatial caches) are kept in `data/` subfolders such as `dist_matrix/` and `cache/`. These are large and are typically created once — they are often omitted from version control.

## Contact / licence

If you have questions about the code or data placement, open an issue or contact the author listed in the thesis cover page. The repository does not include restricted datasets; obtain them from the original data providers and place them into `data/` as described above.

