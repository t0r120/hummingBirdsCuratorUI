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

## Repository Structure
 
### Scripts
 
| Script | Description |
|---|---|
| `data_retrieving/01_data_acquisition.py` | Initial harvesting and taxonomic backbone establishment. |
| `data_retrieving/02_matrix_expansion.py` | Generation of the comprehensive 14-region phenotypic matrix (47,320 data points). |
| `data_retrieving/03_semantic_color_dictionary.py` | Integration of the HBW/BirdLife color standards with Wikidata. |
| `core/interactive_curator.py` | Expert-in-the-loop tool for real-time validation of phenotypic traits against in vivo records. |

 
### Data
 
| File | Description |
|---|---|
| `data/massive_thinned_observations.csv` | The bias-corrected analytical dataset (Big Data scale). |
| `data/color_dictionary_hbw_wikidata.csv` | The curated 641-color master list. |
| `data/TKG_Evidence_Annotation_N-Obs.csv` | Curated phenotypic assertions with evidence links. |
| `data/tkg_hummingbirds_research_grade.csv` | Validated research-grade occurrences. |
| `data/Wikidata_colors.csv` | Raw Wikidata color entities before biocentric sanitization. |
 
## Key Methodology: Spatial & Taxonomic Integrity
 
To ensure FAIR principles and scientific rigor, the TKG implements:
 
- **Spatial Thinning:** Mitigation of the "smartphone proximity effect" via a 0.03° resolution grid to ensure biodiversity hotspots reflect biological presence rather than observer density.
- **14-Region Anatomy:** Detailed curation of: Gorget, Crest, Nape, Crown, Bill, Breast, Flanks, Rectrices, Rump, Remiges, Chin, Belly, Tail Coverts, and Back.
- **LOD Integration:** Mapping of all phenotypic traits to unique Wikidata QIDs for machine-readable interoperability.
## Requirements
 
- R ≥ 4.2 or rpy2 3.6.7
  
- Key packages: `tidyverse`, `sf`, `rinat`, `WikidataR` (or `SPARQL`), `ggplot2`, `rnaturalearth`
- A SPARQL endpoint connection (for `wikidata_biocentric_color_lexicon.sparql`)
```r
install.packages(c("tidyverse", "sf", "rinat", "ggplot2", "rnaturalearth", "SPARQL"))
```
 
 
## Getting Started
 
1. Clone the repository.
2. Run `data_retrieving/01_data_acquisition.py` to establish the core taxa.
3. Run `data_retrieving/02_matrix_expansion.py` to build the 14-region phenotypic matrix.
4. Run `data_retrieving/03_semantic_color_dictionary.py` to generate the Wikidata-linked color dictionary.
6. Execute `core/interactive_curator.py` for the expert validation phase.

## Citation
 
If you use this pipeline or dataset, please cite:
 
```bibtex
@misc{tkg2026,
  author    = {[Israel Muñoz-Velasco, Layla Michán-Aguirre]},
  title     = {Trochilidae Knowledge Graph (TKG): Biodata Curation},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/[org]/[repo]}
}
```
 
## Authors
 
- **[Israel Muñoz-Velasco]** — Project Lead, Bio-curation & Annotation Lead — *[National Autonomous University of Mexico (UNAM)]*
- **[Layla Michán Aguirre]** — Project Lead, Bio-curation & Annotation Lead — *[National Autonomous University of Mexico (UNAM)]*
## License
 
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
 
        
