#!/bin/bash

# === Load R module ===
module load R

DIR="$1"
if [ -z "$DIR" ]; then
    echo "Usage: $0 /path/to/parent_folder"
    exit 1
fi

RESULTS_DIR="$DIR/Results"
OUTPUT_DIR="$DIR/Data"

# Check that Results folder exists
if [ ! -d "$RESULTS_DIR" ]; then
    echo "Results folder not found: $RESULTS_DIR"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Run R script
Rscript -e "
results_dir <- '$RESULTS_DIR'
output_dir <- '$OUTPUT_DIR'

nAb_data_processing <- function(address, output_address) {
    files <- list.files(address, pattern='\\.txt$', full.names=TRUE)
    conc_list <- list()
    all_fit_names <- character(0)
    
    for (file_name in files) {
        lines <- readLines(file_name)
        header_row <- grep('^Time[0-9]*', lines)[1]
        if (is.na(header_row)) {
            message('Skipping file (no Time header found): ', basename(file_name))
            next
        }
        
        df <- read.table(file_name, header=TRUE, sep='\t', fill=TRUE,
                         skip=header_row-1, stringsAsFactors=FALSE, check.names=FALSE)
        
        time_cols <- grep('^Time[0-9]*', colnames(df))
        empty_list <- list()
        fit_names <- character(0)
        
        for (i in seq_along(time_cols)) {
            t_col <- time_cols[i]
            d_col <- t_col + 1
            f_col <- t_col + 2
            if (f_col > ncol(df)) next
            
            temp <- df[, c(t_col, d_col, f_col)]
            colnames(temp) <- c('Time', 'Data', 'Fit')
            
            temp$Time <- temp$Time - min(temp$Time, na.rm=TRUE)
            
            if (all(is.na(temp$Fit) | temp$Fit == '')) next
            
            fit_name <- colnames(df)[f_col]
            empty_list[[fit_name]] <- temp
            fit_names <- c(fit_names, fit_name)
        }
        
        conc_list[[basename(file_name)]] <- empty_list
        all_fit_names <- unique(c(all_fit_names, fit_names))
    }
    
    for (fit_name in all_fit_names) {
        fit_data_list <- lapply(conc_list, function(x) {
            if (!is.null(x[[fit_name]])) x[[fit_name]] else {
                data.frame(Time=NA, Data=NA, Fit=NA)
            }
        })
        
        max_rows <- max(sapply(fit_data_list, nrow))
        fit_data_list <- lapply(fit_data_list, function(df) {
            if (nrow(df) < max_rows) {
                df <- rbind(df,
                            data.frame(Time=rep(NA, max_rows - nrow(df)),
                                       Data=rep(NA, max_rows - nrow(df)),
                                       Fit=rep(NA, max_rows - nrow(df))))
            }
            df
        })
        
        merged <- do.call(cbind, fit_data_list)
        
        # REMOVE ALL TIME COLUMNS
        merged <- merged[, !grepl('^Time', colnames(merged))]
        
        write.csv(merged,
                  file=file.path(output_address, paste0(fit_name, '.csv')),
                  row.names=FALSE)
    }
}

nAb_data_processing(results_dir, output_dir)
message('Data processing complete.')
"
