from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_DATA_DIR = (
    Path(__file__).resolve().parent.parent
    / "app"
    / "data"
    / "who"
    / "raw"
)

PROCESSED_DATA_DIR = (
    Path(__file__).resolve().parent.parent
    / "app"
    / "data"
    / "who"
    / "processed"
)

EXPECTED_COLUMNS = [
    "Month",
    "L",
    "M",
    "S",
    "SD3neg",
    "SD2neg",
    "SD1neg",
    "SD0",
    "SD1",
    "SD2",
    "SD3",
]

OUTPUT_COLUMNS = [
    "Month",
    "L",
    "M",
    "S",
    "SD3neg",
    "SD2neg",
    "SD1neg",
    "SD0",
    "SD1",
    "SD2",
    "SD3",
]

DATASETS = {
    "weight_for_age": (
        "weight_birth_to_5.xlsx",
    ),
    "height_for_age": (
        "length_birth_to_2.xlsx",
        "height_2_to_5.xlsx",
    ),
    "bmi_for_age": (
        "bmi_birth_to_2.xlsx",
        "bmi_2_to_5.xlsx",
    ),
    "head_circumference": (
        "head_circumference.xlsx",
    ),
}


def load_excel(path: Path) -> pd.DataFrame:
    """
    Loads a WHO Excel dataset.
    """

    if not path.exists():
        raise FileNotFoundError(path)

    dataframe = pd.read_excel(path)

    dataframe.columns = [
        str(column).strip()
        for column in dataframe.columns
    ]

    missing = [
        column
        for column in EXPECTED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing:
        raise ValueError(
            f"{path.name} is missing columns: {missing}"
        )

    dataframe = dataframe[EXPECTED_COLUMNS]

    return dataframe


def merge_tables(
    *tables: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merges WHO tables into one dataset.
    """

    dataframe = pd.concat(
        tables,
        ignore_index=True,
    )

    dataframe = dataframe.drop_duplicates(
        subset="Month",
        keep="first",
    )

    dataframe = dataframe.sort_values(
        by="Month",
    )

    dataframe = dataframe.reset_index(
        drop=True,
    )

    return dataframe


def validate_dataset(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> None:
    """
    Validates the normalized dataset.
    """

    months = dataframe["Month"].tolist()

    expected = list(
        range(61),
    )

    if months != expected:
        missing = sorted(
            set(expected) - set(months),
        )

        extra = sorted(
            set(months) - set(expected),
        )

        raise ValueError(
            (
                f"{dataset_name} failed validation.\n"
                f"Missing months: {missing}\n"
                f"Unexpected months: {extra}"
            )
        )

    if dataframe[
        ["L", "M", "S"]
    ].isnull().any().any():
        raise ValueError(
            f"{dataset_name} contains empty LMS values."
        )


def save_dataset(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Saves the normalized dataset.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe = dataframe[
        OUTPUT_COLUMNS
    ]

    dataframe.to_csv(
        output_path,
        index=False,
    )


def process_gender(
    gender: str,
) -> None:
    """
    Processes every WHO dataset for a gender.
    """

    print(f"\nProcessing {gender}...")

    gender_input = RAW_DATA_DIR / gender
    gender_output = PROCESSED_DATA_DIR / gender

    for dataset_name, files in DATASETS.items():

        print(f"  -> {dataset_name}")

        tables = []

        for filename in files:
            tables.append(
                load_excel(
                    gender_input / filename,
                )
            )

        merged = merge_tables(
            *tables,
        )

        validate_dataset(
            merged,
            dataset_name,
        )

        save_dataset(
            merged,
            gender_output / f"{dataset_name}.csv",
        )

        print(
            f"     ✓ {len(merged)} rows"
        )


def main() -> None:
    """
    Entry point.
    """

    print(
        "Normalizing WHO Growth Standards..."
    )

    process_gender("boys")
    process_gender("girls")

    print(
        "\nWHO datasets normalized successfully."
    )


if __name__ == "__main__":
    main()