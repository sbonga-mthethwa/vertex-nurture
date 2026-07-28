from __future__ import annotations

import csv
from decimal import (
    Decimal,
    localcontext,
)
from pathlib import Path

from app.schemas.growth_evaluation import (
    GrowthEvaluationResult,
)


class GrowthStandardService:
    """
    WHO Child Growth Standards Engine.

    Responsibilities
    ----------------
    • Load official WHO datasets
    • Cache datasets in memory
    • Retrieve WHO LMS values
    • Calculate z-scores
    • Calculate percentiles
    • Evaluate child growth
    """

    def __init__(self) -> None:
        """
        Loads every processed WHO dataset into memory.
        """

        self._data_directory = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "who"
            / "processed"
        )

        self._datasets: dict[
            str,
            dict[int, dict[str, Decimal]],
        ] = {}

        self._load_all_datasets()

    ####################################################################
    # Dataset Loading
    ####################################################################

    def _load_all_datasets(
        self,
    ) -> None:
        """
        Loads every processed WHO dataset into memory.
        """

        datasets = (
            "weight_for_age",
            "height_for_age",
            "bmi_for_age",
            "head_circumference",
        )

        genders = (
            "boys",
            "girls",
        )

        for gender in genders:
            for dataset in datasets:

                key = f"{gender}_{dataset}"

                self._datasets[key] = self._load_dataset(
                    gender=gender,
                    dataset=dataset,
                )

    def _load_dataset(
        self,
        gender: str,
        dataset: str,
    ) -> dict[int, dict[str, Decimal]]:
        """
        Loads one processed WHO dataset.

        Returns

        {
            0: {
                "L": ...,
                "M": ...,
                "S": ...,
                ...
            },

            1: {...},

            ...

            60: {...}
        }
        """

        file_path = (
            self._data_directory
            / gender
            / f"{dataset}.csv"
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"WHO dataset not found: {file_path}"
            )

        data: dict[
            int,
            dict[str, Decimal],
        ] = {}

        with file_path.open(
            mode="r",
            encoding="utf-8-sig",
            newline="",
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:

                month = int(row["Month"])

                data[month] = {
                    "L": Decimal(row["L"]),
                    "M": Decimal(row["M"]),
                    "S": Decimal(row["S"]),
                    "SD3neg": Decimal(row["SD3neg"]),
                    "SD2neg": Decimal(row["SD2neg"]),
                    "SD1neg": Decimal(row["SD1neg"]),
                    "SD0": Decimal(row["SD0"]),
                    "SD1": Decimal(row["SD1"]),
                    "SD2": Decimal(row["SD2"]),
                    "SD3": Decimal(row["SD3"]),
                }

        return data

    ####################################################################
    # WHO Reference Retrieval
    ####################################################################

    def _get_reference(
        self,
        gender: str,
        dataset: str,
        age_in_months: int,
    ) -> tuple[
        Decimal,
        Decimal,
        Decimal,
    ]:
        """
        Returns the WHO LMS values for a child.
        """

        key = f"{gender}_{dataset}"

        table = self._datasets.get(key)

        if table is None:
            raise ValueError(
                f"WHO dataset '{key}' not loaded."
            )

        reference = table.get(age_in_months)

        if reference is None:
            raise ValueError(
                f"No WHO reference for age "
                f"{age_in_months} months."
            )

        return (
            reference["L"],
            reference["M"],
            reference["S"],
        )

    ####################################################################
    # WHO Mathematics
    ####################################################################

    def _calculate_z_score(
        self,
        measurement: Decimal,
        l: Decimal,
        m: Decimal,
        s: Decimal,
    ) -> Decimal:
        """
        Calculates the WHO LMS z-score.

        WHO Formula
        -----------

        When L ≠ 0:

                    (X / M)^L - 1
            Z = -----------------------
                     L × S

        When L = 0:

                 ln(X / M)
            Z = ----------
                     S

        Parameters
        ----------
        measurement:
            Child's observed measurement.

        l:
            WHO Box-Cox power (L).

        m:
            WHO median (M).

        s:
            WHO coefficient of variation (S).

        Returns
        -------
        Decimal
            WHO z-score rounded to four decimal places.
        """

        if measurement <= 0:
            raise ValueError(
                "Measurement must be greater than zero."
            )

        if m <= 0:
            raise ValueError(
                "WHO median must be greater than zero."
            )

        if s <= 0:
            raise ValueError(
                "WHO coefficient of variation must be greater than zero."
            )

        with localcontext() as context:

            context.prec = 28

            ratio = measurement / m

            #
            # WHO Formula when L == 0
            #

            if l == Decimal("0"):
                z_score = ratio.ln() / s

            #
            # WHO Formula when L != 0
            #

            else:
                z_score = (
                    (ratio ** l) - Decimal("1")
                ) / (
                    l * s
                )

        return z_score.quantize(
            Decimal("0.0001"),
        )

    def _calculate_percentile(
        self,
        z_score: Decimal,
    ) -> Decimal:
        """
        Converts a WHO z-score into a percentile.

        The percentile is calculated using the cumulative
        distribution function (CDF) of the standard normal
        distribution.

        Parameters
        ----------
        z_score:
            WHO z-score.

        Returns
        -------
        Decimal
            Percentile between 0 and 100.
        """

        from math import erf
        from math import sqrt

        percentile = (
            (
                1
                + erf(
                    float(z_score)
                    / sqrt(2)
                )
            )
            / 2
        ) * 100

        return Decimal(
            str(percentile)
        ).quantize(
            Decimal("0.01"),
        )

    ####################################################################
    # WHO Classification
    ####################################################################

    def _classify_weight_for_age(
        self,
        z_score: Decimal,
    ) -> str:
        """
        Classifies Weight-for-Age using WHO standards.

        Parameters
        ----------
        z_score:
            WHO Weight-for-Age z-score.

        Returns
        -------
        str
            Clinical classification.
        """

        if z_score < Decimal("-3"):
            return "Severely Underweight"

        if z_score < Decimal("-2"):
            return "Underweight"

        if z_score <= Decimal("2"):
            return "Normal"

        return "Above Expected Weight"

    def _classify_height_for_age(
        self,
        z_score: Decimal,
    ) -> str:
        """
        Classifies Height-for-Age using WHO standards.

        Parameters
        ----------
        z_score:
            WHO Height-for-Age z-score.

        Returns
        -------
        str
            Clinical classification.
        """

        if z_score < Decimal("-3"):
            return "Severely Stunted"

        if z_score < Decimal("-2"):
            return "Stunted"

        if z_score <= Decimal("3"):
            return "Normal"

        return "Tall for Age"

    def _classify_bmi_for_age(
        self,
        z_score: Decimal,
    ) -> str:
        """
        Classifies BMI-for-Age using WHO standards.

        Parameters
        ----------
        z_score:
            WHO BMI-for-Age z-score.

        Returns
        -------
        str
            Clinical classification.
        """

        if z_score < Decimal("-3"):
            return "Severe Wasting"

        if z_score < Decimal("-2"):
            return "Wasting"

        if z_score <= Decimal("1"):
            return "Normal"

        if z_score <= Decimal("2"):
            return "Risk of Overweight"

        if z_score <= Decimal("3"):
            return "Overweight"

        return "Obese"

    def _classify_head_circumference(
        self,
        z_score: Decimal,
    ) -> str:
        """
        Classifies Head Circumference-for-Age using WHO standards.

        Parameters
        ----------
        z_score:
            WHO Head Circumference-for-Age z-score.

        Returns
        -------
        str
            Clinical classification.
        """

        if z_score < Decimal("-3"):
            return "Severe Microcephaly"

        if z_score < Decimal("-2"):
            return "Microcephaly"

        if z_score <= Decimal("2"):
            return "Normal"

        if z_score <= Decimal("3"):
            return "Macrocephaly"

        return "Severe Macrocephaly"

    ####################################################################
    # Internal Evaluation Engine
    ####################################################################

    def _evaluate_measurement(
        self,
        *,
        dataset: str,
        gender: str,
        age_in_months: int,
        measurement: Decimal,
        unit: str,
        classifier,
    ) -> GrowthEvaluationResult:
        """
        Performs a WHO growth evaluation.

        This method is the common evaluation pipeline used
        by every WHO growth indicator.
        """

        l, m, s = self._get_reference(
            gender=gender,
            dataset=dataset,
            age_in_months=age_in_months,
        )

        z_score = self._calculate_z_score(
            measurement=measurement,
            l=l,
            m=m,
            s=s,
        )

        percentile = self._calculate_percentile(
            z_score,
        )

        classification = classifier(
            z_score,
        )

        return GrowthEvaluationResult(
            measurement=dataset,
            gender=gender,
            age_in_months=age_in_months,
            measurement_value=measurement,
            unit=unit,
            z_score=z_score,
            percentile=percentile,
            classification=classification,
            l=l,
            m=m,
            s=s,
        )

    ####################################################################
    # Public API
    ####################################################################

    def evaluate_weight_for_age(
        self,
        gender: str,
        age_in_months: int,
        weight_kg: Decimal,
    ) -> GrowthEvaluationResult:
        """
        Evaluates Weight-for-Age using WHO standards.
        """

        if gender not in (
            "boys",
            "girls",
        ):
            raise ValueError(
                "Gender must be either 'boys' or 'girls'."
            )

        if not (
            0 <= age_in_months <= 60
        ):
            raise ValueError(
                "Age must be between 0 and 60 months."
            )

        if weight_kg <= 0:
            raise ValueError(
                "Weight must be greater than zero."
            )

        return self._evaluate_measurement(
            dataset="weight_for_age",
            gender=gender,
            age_in_months=age_in_months,
            measurement=weight_kg,
            unit="kg",
            classifier=self._classify_weight_for_age,
        )
    
    def evaluate_height_for_age(
        self,
        gender: str,
        age_in_months: int,
        height_cm: Decimal,
    ) -> GrowthEvaluationResult:
        """
        Evaluates Height-for-Age using WHO standards.
        """

        if gender not in (
            "boys",
            "girls",
        ):
            raise ValueError(
                "Gender must be either 'boys' or 'girls'."
            )

        if not (
            0 <= age_in_months <= 60
        ):
            raise ValueError(
                "Age must be between 0 and 60 months."
            )

        if height_cm <= 0:
            raise ValueError(
                "Height must be greater than zero."
            )

        return self._evaluate_measurement(
            dataset="height_for_age",
            gender=gender,
            age_in_months=age_in_months,
            measurement=height_cm,
            unit="cm",
            classifier=self._classify_height_for_age,
        )

    def evaluate_bmi_for_age(
        self,
        gender: str,
        age_in_months: int,
        bmi: Decimal,
    ) -> GrowthEvaluationResult:
        """
        Evaluates BMI-for-Age using WHO standards.
        """

        if gender not in (
            "boys",
            "girls",
        ):
            raise ValueError(
                "Gender must be either 'boys' or 'girls'."
            )

        if not (
            0 <= age_in_months <= 60
        ):
            raise ValueError(
                "Age must be between 0 and 60 months."
            )

        if bmi <= 0:
            raise ValueError(
                "BMI must be greater than zero."
            )

        return self._evaluate_measurement(
            dataset="bmi_for_age",
            gender=gender,
            age_in_months=age_in_months,
            measurement=bmi,
            unit="kg/m²",
            classifier=self._classify_bmi_for_age,
        )

    def evaluate_head_circumference(
        self,
        gender: str,
        age_in_months: int,
        head_circumference_cm: Decimal,
    ) -> GrowthEvaluationResult:
        """
        Evaluates Head Circumference-for-Age using WHO standards.
        """

        if gender not in (
            "boys",
            "girls",
        ):
            raise ValueError(
                "Gender must be either 'boys' or 'girls'."
            )

        if not (
            0 <= age_in_months <= 60
        ):
            raise ValueError(
                "Age must be between 0 and 60 months."
            )

        if head_circumference_cm <= 0:
            raise ValueError(
                "Head circumference must be greater than zero."
            )

        return self._evaluate_measurement(
            dataset="head_circumference",
            gender=gender,
            age_in_months=age_in_months,
            measurement=head_circumference_cm,
            unit="cm",
            classifier=self._classify_head_circumference,
        )