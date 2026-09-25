import os
import pandas as pd

from sklearn.model_selection import train_test_split


INPUT_PATH = "data/processed/Mahi_final_preprocessed_dataset.csv"
OUTPUT_DIR = "data/processed/finetuning"

RANDOM_STATE = 42


def main():

    df = pd.read_csv(INPUT_PATH)

    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        stratify=df["shortlisted"],
        random_state=RANDOM_STATE
    )

    validation_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        stratify=temp_df["shortlisted"],
        random_state=RANDOM_STATE
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    train_df.to_csv(
        f"{OUTPUT_DIR}/train.csv",
        index=False
    )

    validation_df.to_csv(
        f"{OUTPUT_DIR}/validation.csv",
        index=False
    )

    test_df.to_csv(
        f"{OUTPUT_DIR}/test.csv",
        index=False
    )

    print("\n===== Fine-Tuning Dataset Split =====")
    print(f"Total rows      : {len(df)}")
    print(f"Training rows   : {len(train_df)}")
    print(f"Validation rows : {len(validation_df)}")
    print(f"Test rows       : {len(test_df)}")

    print("\nTraining labels:")
    print(train_df["shortlisted"].value_counts())

    print("\nValidation labels:")
    print(validation_df["shortlisted"].value_counts())

    print("\nTest labels:")
    print(test_df["shortlisted"].value_counts())

    print("\nSaved to:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()