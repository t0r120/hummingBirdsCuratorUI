# ==============================================================================
# PROJECT: Trochilidae Knowledge Graph (TKG)
# STEP 02: High-Throughput Matrix Expansion (Arizmendi Segmentation)
# Output file ->  TKG_Evidence_Annotation_N-Obs.csv
# SYSTEM ARCHITECT: Isra |  BIO-CURATION LEAD: Layla
# ==============================================================================

from rpy2 import robjects

robjects.r('''

library(dplyr)
library(tidyr)

# --- 1. DATA LOADING ---
rds_path <- "data/tkg_hummingbirds_research_grade.rds"
if (file.exists(rds_path)) {
  final_inat_data <- readRDS(rds_path)
} else {
  stop("Data file not found. Run Script 01 first.")
}

# --- 2. ARIZMENDI ANATOMICAL MODEL (14 UNITS - UPDATED) ---
anatomical_regions <- data.frame(
  region = c("Gorget", "Crest", "Nape", "Crown", "Bill", "Breast", "Flanks", 
             "Rectrices", "Rump", "Remiges", "Chin", "Belly", "Tail coverts", "Back"),
  region_qid = c("Q5586271", "Q1589150", "Q374727", "Q3321195", "Q31528", "Q21342622", "Q1427103", 
                 "Q475059", "Q1790261", "Q1433997", "Q82714", "Q3429717", "Q3178731", "Q2602751"),
  stringsAsFactors = FALSE
)

# --- 3. MATRIX EXPANSION ---

tkg_annotation_matrix <- final_inat_data %>%
  select(scientific_name, id, image_url) %>% 
  crossing(anatomical_regions) %>%
  mutate(
    is_visible = TRUE,
    sex_P21 = NA,             # 
    wikidata_color_Q = NA,    # 
    optical_property = NA,    # 
    confidence_score = 1.0,   #
    annotator_metadata = "Layla",
    timestamp = Sys.time()
  ) %>%
  arrange(scientific_name, id, region)

# --- 4. EXPORT ---
write.csv(tkg_annotation_matrix, "data/TKG_Evidence_Annotation_N-Obs.csv", row.names = FALSE)
cat("Expansion Complete.", nrow(tkg_annotation_matrix), "annotation points generated for all America.\n")
''')