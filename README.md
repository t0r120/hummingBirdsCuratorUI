![Static Badge](https://img.shields.io/badge/status-active-51B870?style=flat-square) ![Static Badge](https://img.shields.io/badge/license-MIT-D92323?style=flat-square)
 ![Static Badge](https://img.shields.io/badge/R-%E2%89%A54.2-6BAFD1?style=flat-square&logo=r&logoColor=6BAFD1)
![Static Badge](https://img.shields.io/badge/Python-3.12-276DC3?style=flat-square&logo=python&logoColor=F5B027)
![Static Badge](https://img.shields.io/badge/rpy2-3.6.7-235DD9?style=flat-square)
![Static Badge](https://img.shields.io/badge/Streamlit-1.56.0-D9233B?style=flat-square&logo=Streamlit)

---
## Project Overview

This repository contains the end-to-end computational pipeline for the Trochilidae Knowledge Graph (TKG). The project integrates massive citizen science data  ([iNaturalist](https://www.inaturalist.org/)), expert taxonomic authorities (Howard & Moore / HBW), and semantic web technologies (Wikidata/RDF) to generate a high-resolution phenotypic matrix of hummingbird plumage across 14 precise anatomical regions.

The pipeline is designed for reproducible, FAIR-compliant biocuration: from raw occurrence harvesting, through spatial bias correction, to expert-validated, semantically annotated phenotypic traits ready for Linked Open Data (LOD) publication.

```
01_data_acquisition.py
        │  (taxonomic backbone + initial harvest)
        ▼
[tkg_hummingbirds_research_grade.rds]
        │  
        ▼
02_matrix_expansion.py
        │    (14-region phenotypic matrix, 47,320 data points)
        ▼
   massive_thinned_observations.csv
        |
        ▼
03_semantic_color_dictionary.R
        │  (HBW/BirdLife ↔ Wikidata color mapping)
        ▼
   color_dictionary_hbw_wikidata.csv
        ▼
04_interactive_curator.py
```
        
