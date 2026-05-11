import logging
import pathlib
from timeit import default_timer as timer

import pandas as pd

from iotcryptojacking.dataset import load_dataset
from iotcryptojacking.utils import run_process

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)


def run_experiments() -> None:
    """Run all imbalanced dataset experiments."""
    base_storage_folder = pathlib.Path("./data/imbalanced_dataset_experiments")
    base_storage_folder.mkdir(parents=True, exist_ok=True)

    df_results = pd.DataFrame()
    (
        df1,
        df2,
        df3,
        df4,
        df5,
        df6,
        df7,
        df8,
        df9,
        df10,
        df11,
        df12,
        df13,
        df14,
        df15,
        df16,
        df17,
        df18,
        df19,
        df20,
        df21,
        df22,
        df23,
        df32,
        df33,
        df34,
        df35,
    ) = load_dataset()

    ## Imbalanced: 4 minutes of timely balanced dataset

    df_malicious = pd.DataFrame(
        pd.concat(
            [
                df1[:2832],
                df2[:4680],
                df3[:271],
                df4[:48],
                df5[:69],
                df6[:72],
                df7[:170],
                df32[:175],
                df33[:76],
                df34[:48],
                df35[:1300],
            ]
        )
    )

    df_benign = pd.DataFrame(
        pd.concat(
            [
                df8[:422784],
                df9[:44376],
                df10[:14784],
                df11[:3576],
                df12[:34728],
                df13[:269400],
                df14[:73],
                df15[:24144],
                df16[:7320],
                df17[:21240],
                df18[:544416],
                df19[:2664],
                df20[:27480],
                df21[:30888],
                df22[:12168],
                df23[:174648],
            ]
        )
    )

    print(f"malicious: {len(df_malicious)}")
    print(f"benign: {len(df_benign)}")

    print(f"{len(df_malicious[df_malicious.isna().any(axis=1)])} NAN in malicious!")
    print(f"{len(df_benign[df_benign.isna().any(axis=1)])} NAN in benign!")

    df_malicious = df_malicious.dropna()
    df_benign = df_benign.dropna()

    print("After droppping NAN rows: ")
    print(f"malicious: {len(df_malicious)}")
    print(f"benign: {len(df_benign)}")

    start = timer()

    results_all_combined_imbalanced_df_ml, results_all_combined_imbalanced_df_ml_res = (
        run_process(df_malicious, df_benign, df_results)
    )
    results_all_combined_imbalanced_df_ml_res.to_csv(
        base_storage_folder / "results_all_combined_imbalanced_df_ml.csv", index=False
    )
    results_all_combined_imbalanced_df_ml.to_csv(
        base_storage_folder / "results_all_combined_imbalanced_ml_res.csv", index=False
    )
    logging.info(
        "Finished extracting and saved timely balanced results_all_combined_imbalanced"
    )

    end = timer()
    print(f"Took {end - start}")

    ## Imbalanced: 4 minutes of timely balanced dataset with oversampling

    df_malicious = pd.DataFrame(
        pd.concat([df1, df2, df3, df4, df5, df6, df7, df32, df33, df34, df35])
    )

    df_benign = pd.DataFrame(
        pd.concat(
            [
                df8,
                df9,
                df10,
                df11,
                df12,
                df13,
                df14,
                df15,
                df16,
                df17,
                df18,
                df19,
                df20,
                df21,
                df22,
                df23,
            ]
        )
    )

    # sampling
    df_malicious = df_malicious.sample(len(df_benign), replace=True)

    print(f"malicious: {len(df_malicious)}")
    print(f"benign: {len(df_benign)}")

    print(f"{len(df_malicious[df_malicious.isna().any(axis=1)])} NAN in malicious!")
    print(f"{len(df_benign[df_benign.isna().any(axis=1)])} NAN in benign!")

    df_malicious = df_malicious.dropna()
    df_benign = df_benign.dropna()

    print("After droppping NAN rows: ")
    print(f"malicious: {len(df_malicious)}")
    print(f"benign: {len(df_benign)}")

    start = timer()

    _, timely_oversampling_results_all_combined_imbalanced = run_process(
        df_malicious, df_benign, df_results
    )
    timely_oversampling_results_all_combined_imbalanced.to_csv(
        base_storage_folder / "timely_oversampling_results_all_combined_imbalanced.csv",
        index=False,
    )
    logging.info(
        "Finished extracting and saving timely_oversampling_results_all_combined_imbalanced"
    )

    end = timer()
    print(f"took {end - start}")

    ## Imbalanced: Server

    df_malicious = pd.DataFrame(pd.concat([df2, df7, df32]))

    df_benign = pd.DataFrame(pd.concat([df19, df20, df21, df22]))

    print(f"malicious: {len(df_malicious)}")
    print(f"benign: {len(df_benign)}")

    print(f"{len(df_malicious[df_malicious.isna().any(axis=1)])} NAN in malicious!")
    print(f"{len(df_benign[df_benign.isna().any(axis=1)])} NAN in benign!")

    df_malicious = df_malicious.dropna()
    df_benign = df_benign.dropna()

    print("After droppping NAN rows: ")
    print(f"malicious: {len(df_malicious)}")
    print(f"benign: {len(df_benign)}")

    start = timer()

    _, server_results_all_combined_imbalanced = run_process(
        df_malicious, df_benign, df_results
    )
    server_results_all_combined_imbalanced.to_csv(
        base_storage_folder / "server_results_all_combined_imbalanced.csv", index=False
    )
    logging.info("Finished extracting and saving server_results_all_combined_imbalanced")
    end = timer()
    print(f"took {end - start}")

    ## Imbalanced: Laptop

    df_malicious = pd.DataFrame(pd.concat([df35]))

    df_benign = pd.DataFrame(pd.concat([df8, df9, df10, df11, df12]))

    print(f"malicious: {len(df_malicious)}")
    print(f"benign: {len(df_benign)}")

    print(f"{len(df_malicious[df_malicious.isna().any(axis=1)])} NAN in malicious!")
    print(f"{len(df_benign[df_benign.isna().any(axis=1)])} NAN in benign!")

    df_malicious = df_malicious.dropna()
    df_benign = df_benign.dropna()

    print("After droppping NAN rows: ")
    print(f"malicious: {len(df_malicious)}")
    print(f"benign: {len(df_benign)}")

    start = timer()

    _, laptop_results_all_combined_imbalanced = run_process(
        df_malicious, df_benign, df_results
    )
    laptop_results_all_combined_imbalanced.to_csv(
        base_storage_folder / "laptop_results_all_combined_imbalanced.csv", index=False
    )
    logging.info("Finished extracting and saving laptop_results_all_combined_imbalanced")
    end = timer()
    print(f"took {end - start}")

    ## Imbalanced: Raspberry

    df_malicious = pd.DataFrame(pd.concat([df3, df4, df5, df6, df33, df34]))

    df_benign = pd.DataFrame(pd.concat([df13, df14, df15, df16, df17]))

    print(f"malicious: {len(df_malicious)}")
    print(f"benign: {len(df_benign)}")

    print(f"{len(df_malicious[df_malicious.isna().any(axis=1)])} NAN in malicious!")
    print(f"{len(df_benign[df_benign.isna().any(axis=1)])} NAN in benign!")

    df_malicious = df_malicious.dropna()
    df_benign = df_benign.dropna()

    print("After droppping NAN rows: ")
    print(f"malicious: {len(df_malicious)}")
    print(f"benign: {len(df_benign)}")

    start = timer()

    _, raspberry_results_all_combined_imbalanced = run_process(
        df_malicious, df_benign, df_results
    )
    raspberry_results_all_combined_imbalanced.to_csv(
        base_storage_folder / "raspberry_results_all_combined_imbalanced.csv", index=False
    )
    logging.info("Finished extracting and saving raspberry_results_all_combined_imbalanced")
    end = timer()
    print(f"took {end - start}")

    ## Imbalanced: WebOS

    df_malicious = pd.DataFrame(pd.concat([df1]))

    df_benign = pd.DataFrame(pd.concat([df23]))

    print(f"malicious: {len(df_malicious)}")
    print(f"benign: {len(df_benign)}")

    print(f"{len(df_malicious[df_malicious.isna().any(axis=1)])} NAN in malicious!")
    print(f"{len(df_benign[df_benign.isna().any(axis=1)])} NAN in benign!")

    df_malicious = df_malicious.dropna()
    df_benign = df_benign.dropna()

    print("After droppping NAN rows: ")
    print(f"malicious: {len(df_malicious)}")
    print(f"benign: {len(df_benign)}")

    start = timer()

    _, webos_results_all_combined_imbalanced = run_process(df_malicious, df_benign, df_results)
    webos_results_all_combined_imbalanced.to_csv(
        base_storage_folder / "webos_results_all_combined_imbalanced.csv", index=False
    )
    logging.info("Finished extracting and saving webos_results_all_combined_imbalanced")

    end = timer()
    print(f"took {end - start}")


if __name__ == "__main__":
    run_experiments()

