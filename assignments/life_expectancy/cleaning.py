"Assignment 1: Data Cleaning"
from pathlib import Path

import argparse
import pandas as pd
from life_expectancy import DATA_DIR

def load_data(raw_filename: str) -> pd.DataFrame:
    """Load raw data from a TSV file into a pandas DataFrame."""
    df = pd.read_csv(DATA_DIR / raw_filename, sep="\t")
    return df

def clean_data(raw_data: pd.DataFrame, region: str = "PT") -> pd.DataFrame:
    """Clean raw life expectancy data for a specific region."""
    raw_data.columns = raw_data.columns.str.strip()
    data = raw_data.copy()

    id_col = data.columns[0]
    data[["unit", "sex", "age", "region"]] = data[id_col].str.split(",", expand=True)
    data = data.drop(columns=id_col)
    data = data.melt(
        id_vars=["unit", "sex", "age", "region"],
        var_name="year",
        value_name="value",
    )

    data["year"] = data["year"].astype(str).str.strip().astype(int)

    data["value"] = pd.to_numeric(
        data["value"].astype(str).str.extract(r"(\d+\.?\d*)")[0],
        errors="coerce",
    )
    data = data.dropna(subset=["value"])

    data = data[data["region"] == region]
    return data

def save_data(df: pd.DataFrame, output_filename: str):
    """Save the cleaned data to a CSV file."""
    output_file: Path = DATA_DIR / output_filename
    df.to_csv(output_file, index=False)

def main(region: str = "PT"):
    """Main function to load, clean, and save life expectancy data for a specific region."""
    raw_df = load_data("eu_life_expectancy_raw.tsv")
    clean_df = clean_data(raw_df, region=region)
    save_data(clean_df, "pt_life_expectancy.csv")

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description="Clean EU life expectancy data.")
    parser.add_argument(
        "--region",
        default="PT",
        help="Country code to filter on (default: PT)",
    )
    args = parser.parse_args()
    main(args.region)
