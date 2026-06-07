import logging
import pandas as pd
from typing import Sequence


def load_dataset() -> Sequence[pd.DataFrame]:
    """Load and preprocess all malicious and benign CSV files."""
    #################################################################
    #                                                               #
    #               malicious csv files import                      #
    #                                                               #
    #################################################################
    df1 = pd.read_csv("Data/malicious/WebOS_binary.csv")
    df2 = pd.read_csv("Data/malicious/Server_Binary.csv")
    df3 = pd.read_csv("Data/malicious/Raspberry_Webmine_Robust.csv")
    df4 = pd.read_csv("Data/malicious/Raspberry_Binary.csv")
    df5 = pd.read_csv("Data/malicious/Raspberry_Webmine_Aggressive.csv")
    df6 = pd.read_csv("Data/malicious/Raspberry_WebminePool_Aggressive.csv")
    df7 = pd.read_csv("Data/malicious/Server_WebminePool_Aggressive.csv")
    df32 = pd.read_csv("Data/malicious/Server_WebminePool_Robust.csv")
    df33 = pd.read_csv("Data/malicious/Raspberry_WebminePool_Stealthy.csv")
    df34 = pd.read_csv("Data/malicious/Raspberry_WebminePool_Robust.csv")
    df35 = pd.read_csv("Data/malicious/Desktop_WebminePool_Aggressive.csv")

    #################################################################
    #                                                               #
    #               benign csv files import                         #
    #                                                               #
    #################################################################
    df8 = pd.read_csv("Data/benign-2/Laptop/Laptop_download_benign.csv")
    df9 = pd.read_csv("Data/benign-2/Laptop/Laptop_idle_benign.csv")
    df10 = pd.read_csv("Data/benign-2/Laptop/Laptop_interactive_benign.csv")
    df11 = pd.read_csv("Data/benign-2/Laptop/Laptop_video_benign.csv")
    df12 = pd.read_csv("Data/benign-2/Laptop/Laptop_webbrowsing_benign.csv")

    df13 = pd.read_csv("Data/benign-2/Raspberry/Raspberry_download_benign.csv")
    df14 = pd.read_csv("Data/benign-2/Raspberry/Raspberry_idle_benign.csv")
    df15 = pd.read_csv("Data/benign-2/Raspberry/Raspberry_interactive_benign.csv")
    df16 = pd.read_csv("Data/benign-2/Raspberry/Raspberry_video_benign.csv")
    df17 = pd.read_csv("Data/benign-2/Raspberry/Raspberry_webbrowsing_benign.csv")

    df18 = pd.read_csv("Data/benign-2/Server/Server_download_benign.csv")
    df19 = pd.read_csv("Data/benign-2/Server/Server_idle_benign.csv")
    df20 = pd.read_csv("Data/benign-2/Server/Server_interactive_benign.csv")
    df21 = pd.read_csv("Data/benign-2/Server/Server_video_benign.csv")
    df22 = pd.read_csv("Data/benign-2/Server/Server_webbrowsing_benign.csv")

    df23 = pd.read_csv("Data/benign-2/WebOS/Webos_video(live&normal)_benign.csv")

    logging.info("Finished loading CSV files for malicious_benign_2 dataset")

    #################################################################
    #                                                               #
    #       prune malicious source rows by known HW_src / HW_dst      #
    #                                                               #
    #################################################################
    df1 = _prune_by_hw_address(df1, "18:56:80:17:d0:ef")
    df2 = _prune_by_hw_address(df2, "a4:bb:6d:ac:e1:fd")
    df3 = _prune_by_hw_address(df3, "dc:a6:32:67:66:4b")
    df4 = _prune_by_hw_address(df4, "dc:a6:32:68:35:8a")
    df5 = _prune_by_hw_address(df5, "dc:a6:32:67:66:4b")
    df6 = _prune_by_hw_address(df6, "dc:a6:32:67:66:4b")
    df7 = _prune_by_hw_address(df7, "a4:bb:6d:ac:e1:fd")
    df32 = _prune_by_hw_address(df32, "a4:bb:6d:ac:e1:fd")
    df33 = _prune_by_hw_address(df33, "dc:a6:32:67:66:4b")
    df34 = _prune_by_hw_address(df34, "dc:a6:32:68:35:8a")
    df35 = _prune_by_hw_address(df35, "d8:3b:bf:8f:ba:ba")

    #################################################################
    #                                                               #
    #                  label dataset rows                           #
    #                                                               #
    #################################################################
    malicious_dfs = [df1, df2, df3, df4, df5, df6, df7, df32, df33, df34, df35]
    benign_dfs = [df8, df9, df10, df11, df12, df13, df14, df15, df16, df17, df18, df19, df20, df21, df22, df23]
    _label_datasets(malicious_dfs, benign_dfs)

    return (*malicious_dfs, *benign_dfs)


def _prune_by_hw_address(df: pd.DataFrame, hw_address: str) -> pd.DataFrame:
    if "HW_dst" not in df.columns or "Hw_src" not in df.columns:
        logging.warning("Expected HW_dst/Hw_src columns not found in DataFrame. Skipping prune step.")
        return df
    return df[ (df["HW_dst"] == hw_address) | (df["Hw_src"] == hw_address) ].copy()


def _label_datasets(malicious_dfs: list[pd.DataFrame], benign_dfs: list[pd.DataFrame]) -> None:
    for df in malicious_dfs:
        df.insert(7, "Is_malicious", 1)
    for df in benign_dfs:
        df.insert(7, "Is_malicious", 0)


def get_dataset_dict() -> dict[int, pd.DataFrame]:
    # ordem deve bater com load_dataset():
    # maliciosos (df1..df7, df32..df35) depois benignos (df8..df23)
    keys = [1, 2, 3, 4, 5, 6, 7, 32, 33, 34, 35,
            8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23]
    return {k: v for k, v in zip(keys, load_dataset())}

