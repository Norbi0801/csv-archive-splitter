#!/usr/bin/env python3
import argparse
import csv
import zipfile
import sys
import os

try:
    from tqdm import tqdm
except ImportError:
    print("The 'tqdm' library is not installed. Install it using: pip install tqdm")
    sys.exit(1)


def create_filtered_zip(
        source_zip_path: str,
        csv_path: str,
        output_zip_path: str,
        csv_column_name: str = "filename"
):
    """
    Creates a new ZIP file containing only the files listed in
    the column 'csv_column_name' from the CSV file.

    :param source_zip_path: Path to the original ZIP file
    :param csv_path: Path to the CSV file with the list of files
    :param output_zip_path: Path to the new ZIP file to be created
    :param csv_column_name: Name of the column in the CSV file containing the list of files (default 'filename')
    """

    if not os.path.isfile(source_zip_path):
        print(f"Error: ZIP file not found: {source_zip_path}")
        sys.exit(1)

    if not os.path.isfile(csv_path):
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)

    files_to_extract = set()
    try:
        with open(csv_path, mode='r', encoding='utf-8', newline='') as csv_file:
            # Set delimiter based on CSV format (e.g., ',' or ';')
            reader = csv.DictReader(csv_file, delimiter=',')
            for row in reader:
                filename = row[csv_column_name].strip()
                if filename:
                    files_to_extract.add(filename)
    except KeyError:
        print(f"Error: CSV file does not contain column '{csv_column_name}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    try:
        with zipfile.ZipFile(source_zip_path, 'r') as source_zip, \
                zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as target_zip:

            all_files_in_zip = source_zip.namelist()
            # Filter only those files that exist in the ZIP and are listed in the CSV
            files_filtered = [f for f in all_files_in_zip if f in files_to_extract]

            extracted_count = 0

            # Copy files to the new ZIP with a progress bar
            with tqdm(total=len(files_filtered), desc="Copying files", unit="file") as pbar:
                for zip_member in files_filtered:
                    data = source_zip.read(zip_member)
                    target_zip.writestr(zip_member, data)
                    extracted_count += 1
                    pbar.update(1)

    except zipfile.BadZipFile:
        print(f"Error: {source_zip_path} is not a valid ZIP file.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing ZIP file: {e}")
        sys.exit(1)

    print(f"\nCreated new ZIP file: {output_zip_path}")
    print(f"Number of extracted files: {extracted_count}")


def main():
    parser = argparse.ArgumentParser(
        description="Creates multiple ZIP files containing only selected files from split CSV."
    )
    parser.add_argument(
        "--source_zip",
        required=True,
        help="Path to the source ZIP file (e.g., source.zip)"
    )
    parser.add_argument(
        "--csv_file",
        required=True,
        help="Path to the CSV file with list of files (e.g., files_to_extract.csv)"
    )
    parser.add_argument(
        "--column_name",
        default="filename",
        help="The name of the CSV column containing the filenames (default 'filename')"
    )
    parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="Maximum number of rows (excluding header) in each split CSV file"
    )

    args = parser.parse_args()

    with open(args.csv_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        rows = list(reader)

    total_rows = len(rows)
    num_files = (total_rows + args.n - 1) // args.n

    for i in range(1, num_files + 1):
        start_index = (i - 1) * args.n
        end_index = i * args.n
        chunk = rows[start_index:end_index]

        csv_filename = f"{i}.csv"
        zip_filename = f"{i}.zip"

        with open(csv_filename, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)
            writer.writerows(chunk)

        create_filtered_zip(
            source_zip_path=args.source_zip,
            csv_path=csv_filename,
            output_zip_path=zip_filename,
            csv_column_name=args.column_name
        )

    print(f"Created {num_files} pairs of CSV and ZIP files.")


if __name__ == "__main__":
    main()
