from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


DATA_ROOT = Path("Data")


def _read_csv(rel: str) -> pd.DataFrame:
    return pd.read_csv(DATA_ROOT / rel)


def _prune_by_mac(df: pd.DataFrame, mac: str) -> pd.DataFrame:
    idx = df[((df["HW_dst"] != mac) & (df["Hw_src"] != mac))].index
    df.drop(idx, inplace=True)
    return df


def _label(df: pd.DataFrame, is_malicious: int) -> pd.DataFrame:
    df.insert(7, "Is_malicious", is_malicious)
    return df


def load_dataset() -> Dict[int, pd.DataFrame]:
    """Load and return the same set of DataFrames used by the original notebook.

    Returns a mapping keyed by the dataset integer id used in the notebook.
    """
    # malicious
    df1 = _label(_prune_by_mac(_read_csv("malicious/WebOS_binary.csv"), "18:56:80:17:d0:ef"), 1)
    df2 = _label(_prune_by_mac(_read_csv("malicious/Server_Binary.csv"), "a4:bb:6d:ac:e1:fd"), 1)
    df3 = _label(_prune_by_mac(_read_csv("malicious/Raspberry_Webmine_Robust.csv"), "dc:a6:32:67:66:4b"), 1)
    df4 = _label(_prune_by_mac(_read_csv("malicious/Raspberry_Binary.csv"), "dc:a6:32:68:35:8a"), 1)
    df5 = _label(_prune_by_mac(_read_csv("malicious/Raspberry_Webmine_Aggressive.csv"), "dc:a6:32:67:66:4b"), 1)
    df6 = _label(_prune_by_mac(_read_csv("malicious/Raspberry_WebminePool_Aggressive.csv"), "dc:a6:32:67:66:4b"), 1)
    df7 = _label(_prune_by_mac(_read_csv("malicious/Server_WebminePool_Aggressive.csv"), "a4:bb:6d:ac:e1:fd"), 1)
    df32 = _label(_prune_by_mac(_read_csv("malicious/Server_WebminePool_Robust.csv"), "a4:bb:6d:ac:e1:fd"), 1)
    df33 = _label(_prune_by_mac(_read_csv("malicious/Raspberry_WebminePool_Stealthy.csv"), "dc:a6:32:67:66:4b"), 1)
    df34 = _label(_prune_by_mac(_read_csv("malicious/Raspberry_WebminePool_Robust.csv"), "dc:a6:32:68:35:8a"), 1)
    df35 = _label(_prune_by_mac(_read_csv("malicious/Desktop_WebminePool_Aggressive.csv"), "d8:3b:bf:8f:ba:ba"), 1)

    # benign (benign-1 used in original all_scenarios_1)
    df8 = _label(_read_csv("benign-1/interactive_01.csv"), 0)
    df9 = _label(_read_csv("benign-1/interactive_02.csv"), 0)
    df10 = _label(_read_csv("benign-1/interactive_03.csv"), 0)
    df11 = _label(_read_csv("benign-1/interactive_04.csv"), 0)
    df12 = _label(_read_csv("benign-1/interactive_05.csv"), 0)
    df13 = _label(_read_csv("benign-1/interactive_06.csv"), 0)
    df14 = _label(_read_csv("benign-1/web_1page_01.csv"), 0)
    df15 = _label(_read_csv("benign-1/web_1page_02.csv"), 0)
    df16 = _label(_read_csv("benign-1/web_1page_03.csv"), 0)
    df17 = _label(_read_csv("benign-1/web_1page_04.csv"), 0)
    df18 = _label(_read_csv("benign-1/web_1page_05.csv"), 0)
    df19 = _label(_read_csv("benign-1/bulk_xs_04.csv"), 0)
    df20 = _label(_read_csv("benign-1/bulk_xs_05.csv"), 0)
    df21 = _label(_read_csv("benign-1/video_180s480p_01.csv"), 0)
    df22 = _label(_read_csv("benign-1/video_180s480p_02.csv"), 0)
    df23 = _label(_read_csv("benign-1/video_x1_04.csv"), 0)
    df24 = _label(_read_csv("benign-1/web_multiple_04.csv"), 0)
    df25 = _label(_read_csv("benign-1/bulk_xs_01.csv"), 0)
    df26 = _label(_read_csv("benign-1/bulk_xs_09.csv"), 0)
    df27 = _label(_read_csv("benign-1/bulk_xs_06.csv"), 0)
    df28 = _label(_read_csv("benign-1/bulk_xs_03.csv"), 0)
    df29 = _label(_read_csv("benign-1/web_multiple_03.csv"), 0)
    df30 = _label(_read_csv("benign-1/web_multiple_05.csv"), 0)
    df31 = _label(_read_csv("benign-1/web_multiple_06.csv"), 0)

    mapping = {
        1: df1,
        2: df2,
        3: df3,
        4: df4,
        5: df5,
        6: df6,
        7: df7,
        8: df8,
        9: df9,
        10: df10,
        11: df11,
        12: df12,
        13: df13,
        14: df14,
        15: df15,
        16: df16,
        17: df17,
        18: df18,
        19: df19,
        20: df20,
        21: df21,
        22: df22,
        23: df23,
        24: df24,
        25: df25,
        26: df26,
        27: df27,
        28: df28,
        29: df29,
        30: df30,
        31: df31,
        32: df32,
        33: df33,
        34: df34,
        35: df35,
    }
    return mapping
