from __future__ import annotations
import logging
import pandas as pd
from typing import Sequence


def load_dataset() -> Sequence[pd.DataFrame]:
    #################################################################
    #               malicious csv files import                      #
    #################################################################
    df1  = pd.read_csv("Data/malicious/WebOS_binary.csv")
    df2  = pd.read_csv("Data/malicious/Server_Binary.csv")
    df3  = pd.read_csv("Data/malicious/Raspberry_Webmine_Robust.csv")
    df4  = pd.read_csv("Data/malicious/Raspberry_Binary.csv")
    df5  = pd.read_csv("Data/malicious/Raspberry_Webmine_Aggressive.csv")
    df6  = pd.read_csv("Data/malicious/Raspberry_WebminePool_Aggressive.csv")
    df7  = pd.read_csv("Data/malicious/Server_WebminePool_Aggressive.csv")
    df32 = pd.read_csv("Data/malicious/Server_WebminePool_Robust.csv")
    df33 = pd.read_csv("Data/malicious/Raspberry_WebminePool_Stealthy.csv")
    df34 = pd.read_csv("Data/malicious/Raspberry_WebminePool_Robust.csv")
    df35 = pd.read_csv("Data/malicious/Desktop_WebminePool_Aggressive.csv")

    #################################################################
    #               benign-1 csv files import                       #
    #################################################################
    df8  = pd.read_csv("Data/benign-1/interactive_01.csv")
    df9  = pd.read_csv("Data/benign-1/interactive_02.csv")
    df10 = pd.read_csv("Data/benign-1/interactive_03.csv")
    df11 = pd.read_csv("Data/benign-1/interactive_04.csv")
    df12 = pd.read_csv("Data/benign-1/interactive_05.csv")
    df13 = pd.read_csv("Data/benign-1/interactive_06.csv")
    df14 = pd.read_csv("Data/benign-1/web_1page_01.csv")
    df15 = pd.read_csv("Data/benign-1/web_1page_02.csv")
    df16 = pd.read_csv("Data/benign-1/web_1page_03.csv")
    df17 = pd.read_csv("Data/benign-1/web_1page_04.csv")
    df18 = pd.read_csv("Data/benign-1/web_1page_05.csv")
    df19 = pd.read_csv("Data/benign-1/bulk_xs_04.csv")
    df20 = pd.read_csv("Data/benign-1/bulk_xs_05.csv")
    df21 = pd.read_csv("Data/benign-1/video_180s480p_01.csv")
    df22 = pd.read_csv("Data/benign-1/video_180s480p_02.csv")
    df23 = pd.read_csv("Data/benign-1/video_x1_04.csv")
    df24 = pd.read_csv("Data/benign-1/web_multiple_04.csv")
    df25 = pd.read_csv("Data/benign-1/bulk_xs_01.csv")
    df26 = pd.read_csv("Data/benign-1/bulk_xs_09.csv")
    df27 = pd.read_csv("Data/benign-1/bulk_xs_06.csv")
    df28 = pd.read_csv("Data/benign-1/bulk_xs_03.csv")
    df29 = pd.read_csv("Data/benign-1/web_multiple_03.csv")
    df30 = pd.read_csv("Data/benign-1/web_multiple_05.csv")
    df31 = pd.read_csv("Data/benign-1/web_multiple_06.csv")

    logging.info("Finished loading CSV files for non_default_params dataset")

    #################################################################
    #       prune malicious rows by HW address                      #
    #################################################################
    df1  = _prune_by_hw_address(df1,  "18:56:80:17:d0:ef")
    df2  = _prune_by_hw_address(df2,  "a4:bb:6d:ac:e1:fd")
    df3  = _prune_by_hw_address(df3,  "dc:a6:32:67:66:4b")
    df4  = _prune_by_hw_address(df4,  "dc:a6:32:68:35:8a")
    df5  = _prune_by_hw_address(df5,  "dc:a6:32:67:66:4b")
    df6  = _prune_by_hw_address(df6,  "dc:a6:32:67:66:4b")
    df7  = _prune_by_hw_address(df7,  "a4:bb:6d:ac:e1:fd")
    df32 = _prune_by_hw_address(df32, "a4:bb:6d:ac:e1:fd")
    df33 = _prune_by_hw_address(df33, "dc:a6:32:67:66:4b")
    df34 = _prune_by_hw_address(df34, "dc:a6:32:68:35:8a")
    df35 = _prune_by_hw_address(df35, "d8:3b:bf:8f:ba:ba")

    #################################################################
    #               label dataset rows                              #
    #################################################################
    malicious_dfs = [df1, df2, df3, df4, df5, df6, df7, df32, df33, df34, df35]
    benign_dfs    = [df8, df9, df10, df11, df12, df13, df14, df15, df16, df17,
                     df18, df19, df20, df21, df22, df23, df24, df25, df26, df27,
                     df28, df29, df30, df31]
    _label_datasets(malicious_dfs, benign_dfs)

    return (*malicious_dfs, *benign_dfs)


def _prune_by_hw_address(df: pd.DataFrame, hw_address: str) -> pd.DataFrame:
    if "HW_dst" not in df.columns or "Hw_src" not in df.columns:
        logging.warning(
            "Expected HW_dst/Hw_src columns not found. Skipping prune step."
        )
        return df
    return df[(df["HW_dst"] == hw_address) | (df["Hw_src"] == hw_address)].copy()


def _label_datasets(
    malicious_dfs: list[pd.DataFrame],
    benign_dfs: list[pd.DataFrame],
) -> None:
    for df in malicious_dfs:
        df.insert(7, "Is_malicious", 1)
    for df in benign_dfs:
        df.insert(7, "Is_malicious", 0)


def get_dataset_dict() -> dict[int, pd.DataFrame]:
    # order must match load_dataset() return order:
    # malicious (1..7, 32..35) then benign (8..31)
    keys = [1, 2, 3, 4, 5, 6, 7, 32, 33, 34, 35,
            8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
            28, 29, 30, 31]
    return {k: v for k, v in zip(keys, load_dataset())}
