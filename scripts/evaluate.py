import argparse
import pathlib

import joblib
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def evaluate_model(
    df_path: pathlib.Path, model_path: pathlib.Path, encoder_path: pathlib.Path
) -> None:
    df = pd.read_csv(df_path)
    X = df.drop("class", axis=1).to_numpy()
    y = df["class"].to_numpy()

    encoder = joblib.load(encoder_path)
    X_str = X.astype(str)
    X_encoded = encoder.transform(X_str)

    model = joblib.load(model_path)

    _, x_test, _, y_test = train_test_split(
        X_encoded, y, test_size=0.25, random_state=8675309
    )

    y_pred = model.predict(x_test)

    print(f"Evaluation for Model: {model_path.name} on Data: {df_path.name} (Holdout Test Set)")
    print(classification_report(y_test, y_pred, target_names=["malignant", "benign"]))


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a trained model.")
    parser.add_argument("df", type=pathlib.Path, help="Path to df_ml.csv")
    parser.add_argument("model", type=pathlib.Path, help="Path to model.joblib")
    parser.add_argument("encoder", type=pathlib.Path, help="Path to encoder.joblib")

    args = parser.parse_args()
    evaluate_model(args.df, args.model, args.encoder)


if __name__ == "__main__":
    main()
