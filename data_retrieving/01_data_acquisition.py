# ========================
#   DATA RETRIEVER
# ========================


# ==============================================================================
# PROJECT: Trochilidae Knowledge Graph (TKG)
# STEP 01: Taxonomic Alignment and Data Harvesting
# Output file -> tkg_hummingbirds_research_grade_193_383.rds"
# SYSTEM ARCHITECT: Isra | BIO-CURATION LEAD: Layla
# ==============================================================================
from rpy2 import robjects

robjects.r('''

# --- 3. TAXONOMIC BACKBONE ---
target_family <- "Trochilidae"
check_name <- name_backbone(name = target_family, rank = "family")
if(is.null(check_name$usageKey)) stop("Family 'Trochilidae' not found in GBIF Backbone.")

# Harvest Accepted Species (TROCHILIDAE GBIF ID: 5289)
species_taxonomy <- name_lookup(higherTaxonKey = 5289, rank = "SPECIES", limit = 1000)
master_list <- species_taxonomy$data %>%
  filter(taxonomicStatus == "ACCEPTED") %>%
  select(scientificName, canonicalName, key) %>%
  distinct(canonicalName, .keep_all = TRUE)

# 1. BATCH RESTRICTION | useful when you want to divide the work up between co-workers (From n to len(m) (193 to 383))
master_list <- master_list %>% slice(193:383)
# No batch restriction
# master_list <- master_list


# Rename output file :)
#write.csv(master_list, "data/Trochilidae_Master_List.csv", row.names = FALSE)
write.csv(master_list, "data/Trochilidae_Master_List_193_383.csv", row.names = FALSE)

# ==========================================
# 2. CHECKPOINT
# ==========================================
log_file <- "data/harvest_log_lote2.txt" # Log independiente para tu parte
csv_file <- "data/tkg_hummingbirds_research_grade_193_383.csv"


if(file.exists(log_file)){
  especies_procesadas <- readLines(log_file)
  master_list <- master_list %>% filter(!(canonicalName %in% especies_procesadas))
  message(paste("Checkpoint detected.", length(especies_procesadas), "batch species read."))
} else {
  file.create(log_file)
}

total_restante <- nrow(master_list)
message(paste("Iniciando recolección para las", total_restante, "especies restantes de tu lote..."))

# --- 4. iNATURALIST HARVESTING ---
if(total_restante > 0) {
  for(i in 1:total_restante){
    species_name <- master_list$canonicalName[i]
    message(paste("Harvesting:", species_name, "( Faltan:", total_restante - i, ")"))
    
    obs <- tryCatch({ get_inat_obs(query = species_name) }, error = function(e) return(NULL))
    
    if(!is.null(obs) && is.data.frame(obs) && nrow(obs) > 0){
      obs_filtered <- obs %>%
        filter(quality_grade == "research") %>%
        head(10)
      
      if(nrow(obs_filtered) > 0){
        obs_filtered$search_name <- species_name
        
        
        write.table(obs_filtered, file = csv_file, sep = ",", append = TRUE, 
                    row.names = FALSE, col.names = !file.exists(csv_file))
      }
    }
    
    # Save progress
    write(species_name, file = log_file, append = TRUE)
    Sys.sleep(0.5) 
  }
} else {
  message("Tu lote del 193 al 383 está completo.")
}

# --- 5. CONSOLIDATION ---
if(file.exists(csv_file)){
  final_inat_data <- read.csv(csv_file)
  saveRDS(final_inat_data, "data/tkg_hummingbirds_research_grade_193_383.rds")
  cat("\nDone. Records and checkpoints saved.\n")
}
    
''')


