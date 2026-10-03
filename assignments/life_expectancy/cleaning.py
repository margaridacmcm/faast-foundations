"Assignment 1: Data Cleaning"
from pathlib import Path

import argparse
import pandas as pd
from life_expectancy import DATA_DIR

def clean_data(region: str = "PT"):
    """Clean the EU life expectancy data and filter for Portugal."""
    input_file: Path = DATA_DIR / "eu_life_expectancy_raw.tsv"
    output_file: Path = DATA_DIR / "pt_life_expectancy.csv"

    # Load
    raw_df = pd.read_csv(input_file, sep="\t")
    raw_df.columns = raw_df.columns.str.strip()
    df = raw_df.copy()

    # Clean
    id_col = df.columns[0]
    df[["unit", "sex", "age", "region"]] = df[id_col].str.split(",", expand=True)
    df = df.drop(columns=id_col)
    df = df.melt(
        id_vars=["unit", "sex", "age", "region"],
        var_name="year",
        value_name="value",
    )

    df["year"] = df["year"].astype(str).str.strip().astype(int)

    df["value"] = pd.to_numeric(
        df["value"].astype(str).str.extract(r"(\d+\.?\d*)")[0],
        errors="coerce",
    )
    df = df.dropna(subset=["value"])

    #Filter
    df = df[df["region"] == region]

    #Save
    df.to_csv(output_file, index=False)
    return df

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description="Clean EU life expectancy data.")
    parser.add_argument(
        "--region",
        default="PT",
        help="Country code to filter on (default: PT)",
    )
    args = parser.parse_args()
    clean_data(region=args.region)
