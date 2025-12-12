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

# Create output directory
mkdir -p "$OUTPUT_DIR"

# === Run R code ===
Rscript -e "
results_dir <- '$RESULTS_DIR'
output_dir  <- '$OUTPUT_DIR'

nAb_data_processing <- function(address, output_address) {
    files <- list.files(address, pattern='\\\\.txt$', full.names=TRUE)
    conc_list <- list()
    all_fit_names <- character(0)

    for (file_name in files) {
        lines <- readLines(file_name)
        header_row <- grep('^Time[0-9]*', lines)[1]

        if (is.na(header_row)) {
            message('Skipping (no Time header): ', basename(file_name))
            next
        }

        # Read tab-separated, fill extra columns with NA
        df <- read.table(file_name,
                         header=TRUE,
                         sep='\t',
                         fill=TRUE,
                         skip=header_row-1,
                         stringsAsFactors=FALSE,
                         check.names=FALSE)

        time_cols <- grep('^Time[0-9]*', colnames(df))
        empty_list <- list()
        fit_names <- character(0)

        # extract (Time, Data, Fit) blocks
        for (i in seq_along(time_cols)) {
            t_col <- time_cols[i]
            d_col <- t_col + 1
            f_col <- t_col + 2

            if (f_col > ncol(df)) next

            temp <- df[, c(t_col, d_col, f_col)]
            colnames(temp) <- c('Time', 'Data', 'Fit')

            # normalize Time
            temp$Time <- temp$Time - min(temp$Time, na.rm=TRUE)

            # skip empty Fit blocks
            if (all(is.na(temp$Fit) | temp$Fit == '')) next

            fit_name <- colnames(df)[f_col]
            empty_list[[fit_name]] <- temp
            fit_names <- c(fit_names, fit_name)
        }

        conc_list[[basename(file_name)]] <- empty_list
        all_fit_names <- unique(c(all_fit_names, fit_names))
    }

    # === Merge only Data and Fit columns, no Time columns ===
    for (fit_name in all_fit_names) {

        fit_data_list <- lapply(conc_list, function(x) x[[fit_name]])
        present <- !sapply(fit_data_list, is.null)
        if (!any(present)) next

        fit_data_list <- fit_data_list[present]
        src_names <- names(fit_data_list)
        if (is.null(src_names)) src_names <- seq_along(fit_data_list)

        # pad rows to equal length
        max_rows <- max(sapply(fit_data_list, nrow))
        cols_list <- list()

        for (src in src_names) {
            df_src <- fit_data_list[[src]]

            if (nrow(df_src) < max_rows) {
                n_missing <- max_rows - nrow(df_src)
                df_src <- rbind(df_src,
                                data.frame(Time=rep(NA, n_missing),
                                           Data=rep(NA, n_missing),
                                           Fit=rep(NA, n_missing)))
            }

            # extract ONLY Data and Fit, never Time
            data_col <- df_src\$Data
            fit_col  <- df_src\$Fit

            # safe source name
            safe_src <- gsub('[^A-Za-z0-9_\\\\.-]', '_', src)

            cols_list[[paste0('Data_', safe_src)]] <- data_col
            cols_list[[paste0('Fit_',  safe_src)]] <- fit_col
        }

        merged_df <- as.data.frame(cols_list, stringsAsFactors=FALSE)

        write.csv(merged_df,
                  file=file.path(output_address, paste0(fit_name, '.csv')),
                  row.names=FALSE)
    }
}

nAb_data_processing(results_dir, output_dir)
message('Data processing complete.')
"
