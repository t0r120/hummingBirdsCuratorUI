![Static Badge](https://img.shields.io/badge/status-active-51B870?style=flat-square) ![Static Badge](https://img.shields.io/badge/license-MIT-D92323?style=flat-square)
 ![Static Badge](https://img.shields.io/badge/R-%E2%89%A54.2-6BAFD1?style=flat-square&logo=r&logoColor=6BAFD1)
![Static Badge](https://img.shields.io/badge/Python-%E2%89%A53.12-276DC3?style=flat-square&logo=python&logoColor=F5B027)

---

## Project Overview

This repository contains the end-to-end computational pipeline for the Trochilidae Knowledge Graph (TKG). The project integrates massive citizen science data  ([iNaturalist](https://www.inaturalist.org/)), expert taxonomic authorities (Howard & Moore / HBW), and semantic web technologies (Wikidata/RDF) to generate a high-resolution phenotypic matrix of hummingbird plumage across 14 precise anatomical regions.

The pipeline is designed for reproducible, FAIR-compliant biocuration: from raw occurrence harvesting, through spatial bias correction, to expert-validated, semantically annotated phenotypic traits ready for Linked Open Data (LOD) publication.

```
01_data_acquisition.R
        │  (taxonomic backbone + initial harvest)
        ▼
01b_massive_geospatial_thinning.R
        │  (2020–2026 yearly pull + 10 km² grid thinning)
        ▼
   massive_thinned_observations.csv
        ▼
02_matrix_expansion.R
        │  (14-region phenotypic matrix, 47,320 data points)
        ▼
03_semantic_color_dictionary.R
        │  (HBW/BirdLife ↔ Wikidata color mapping)
        ▼
   color_dictionary_hbw_wikidata.csv
        ▼
04_tkg_interactive_curator.py
```
        
