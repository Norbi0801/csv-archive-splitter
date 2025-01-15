# CSV-Based File Filtering and Zipping Script

## Description

This Python script is designed to create filtered ZIP files based on a list of filenames provided in a CSV file. It splits large CSV files into smaller chunks and generates corresponding ZIP files containing only the files listed in each CSV chunk. The script is particularly useful for managing large ZIP archives and extracting specific files based on dynamic criteria.

## Features

- Splits a large CSV file into smaller chunks of specified size.
- Creates ZIP files that only include the files listed in each CSV chunk.
- Supports progress tracking using `tqdm`.
- Handles errors gracefully, including invalid ZIP files or missing CSV columns.

## Requirements

- Python 3.6+
- `tqdm` library for progress tracking

Install `tqdm` using pip if it's not already installed:

```bash
pip install tqdm
```

## Usage

Run the script using the following command:

```bash
python3 script.py --source_zip <source_zip_path> --csv_file <csv_file_path> --column_name <csv_column_name> --n <rows_per_chunk>
```

### Arguments

| Argument      | Description                                                                         |
|---------------|-------------------------------------------------------------------------------------|
| `--source_zip`  | Path to the source ZIP file.                                                        |
| `--csv_file`    | Path to the CSV file containing the list of filenames to include in the ZIP files.  |
| `--column_name` | Name of the column in the CSV file that contains the filenames (default: `filename`). |
| `--n`           | Maximum number of rows (excluding the header) in each split CSV file.               |

### Example

```bash
python3 script.py --source_zip source.zip --csv_file files_to_extract.csv --column_name filename --n 100
```

This command will:

- Split the `files_to_extract.csv` into multiple chunks of 100 rows each.
- Create corresponding filtered ZIP files from `source.zip` for each chunk.

## How It Works

1. **CSV Splitting**: The script reads the provided CSV file and splits it into smaller CSV files, each containing up to `n` rows.
2. **Filtered ZIP Creation**: For each chunk, the script reads the filenames from the CSV and creates a new ZIP file containing only the specified files.
3. **Progress Tracking**: The script uses `tqdm` to display a progress bar while copying files to the new ZIP.

## Error Handling

- The script checks if the source ZIP file and CSV file exist before proceeding.
- If the CSV does not contain the specified column name, the script exits with an error message.
- If the source ZIP file is invalid, the script handles it gracefully and displays an appropriate error message.

## Dependencies

- Python 3.6+
- tqdm

To install `tqdm`, run:

```bash
pip install tqdm
```

## License

This script is provided under the MIT License. Feel free to use, modify, and distribute it as needed.