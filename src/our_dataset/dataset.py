import itertools
import pathlib
from dataclasses import dataclass
from typing import ClassVar, Iterator
import pandas as pd


@dataclass(frozen=True)
class CryptojackingDataset:
    bitcoin_iloc: tuple[int,int]
    bytecoin_iloc: tuple[int,int]
    monero_iloc: tuple[int,int]
    office_iloc: tuple[int,int]
    skype_iloc: tuple[int,int]
    youtube_iloc: tuple[int,int]
    df:pd.DataFrame

    FEATURES: ClassVar[list[str]] = ["interarrival", "size", "direction"]
    METADATA: ClassVar[list[str]] = ["activity", "vpn", "is_malicious"]

    def __post_init__(self):
        assert set(self.FEATURES + self.METADATA) == set(list(self.df.columns))


def _load_file_pair(ingoing: pathlib.Path, outgoing: pathlib.Path) -> pd.DataFrame:
    """Loads a pair of ingoing/outgoing CSV files, adding the direction column."""
    df = pd.read_csv(ingoing, sep=r"\s+", header=None, names=["interarrival", "size"])
    df["direction"] = "ingoing"

    dfo = pd.read_csv(outgoing, sep=r"\s+", header=None, names=["interarrival", "size"])
    dfo["direction"] = "outgoing"
    return pd.concat([df, dfo]).sort_values("interarrival").reset_index(drop=True)


def _load_dir(dir: pathlib.Path, vpns: list[str] = ["expressvpn", "novpn", "nordvpn"]) -> Iterator[pd.DataFrame]:
    """Yields one DataFrame per VPN, adding the vpn column."""
    traffic = {v: [] for v in vpns}
    for f in dir.iterdir():
        if not f.is_file():
            continue
        parts = f.with_suffix("").name.split("_")
        if not parts:
            continue
        vpn = parts[-1]
        if vpn in vpns:
            traffic[vpn].append(f)

    for vpn in traffic:
        if not traffic[vpn]:
            continue
        out = next(f for f in traffic[vpn] if "outgoing" in f.name)
        ingoing = next(f for f in traffic[vpn] if "ingoing" in f.name)
        df = _load_file_pair(ingoing, out)
        df["vpn"] = vpn
        yield df


def _activity_loader(dir: pathlib.Path, activity: str) -> pd.DataFrame:
    """Concatenates the VPN traffic DataFrames, aligns timelines, and adds the activity column."""
    children = list(dir.iterdir())

    if "Miner" in [c.name for c in children]:
        dfs = _load_dir(dir / "Miner")
    else:
        dfs = _load_dir(dir)

    bigdf = next(dfs)
    for df in dfs:
        df["interarrival"] += bigdf.iloc[-1]["interarrival"]
        bigdf = pd.concat([bigdf, df], ignore_index=True)

    bigdf["activity"] = activity
    return bigdf


def load_dataset(base_path: pathlib.Path = pathlib.Path("Data/Cryptojacking Network Traffic 2021")) -> CryptojackingDataset:
    """Loads all cryptojacking dataset scenarios into a dataclass, each with the keys [interarrival, activity, vpn, direction, size ]"""
    
    dfs = [
        _activity_loader(base_path / "Youtube", "youtube"),
        _activity_loader(base_path / "Bitcoin", "bitcoin"),
        _activity_loader(base_path / "Bytecoin", "bytecoin"),
        _activity_loader(base_path / "Monero", "monero"),
        _activity_loader(base_path / "Office", "office"),
        _activity_loader(base_path / "Skype", "skype")
    ]

    for df in dfs:
        df["is_malicious"] = df["activity"].isin(["bitcoin", "bytecoin", "monero"]).astype(int)

    ilocs = [0]
    for df in dfs:
        ilocs.append(ilocs[-1] + len(df))
    
    return CryptojackingDataset(
        youtube_iloc=(ilocs[0], ilocs[1]),
        bitcoin_iloc=(ilocs[1], ilocs[2]),
        bytecoin_iloc=(ilocs[2], ilocs[3]),
        monero_iloc=(ilocs[3], ilocs[4]),
        office_iloc=(ilocs[4], ilocs[5]),
        skype_iloc=(ilocs[5], ilocs[6]),
        df=pd.concat(dfs).reset_index(drop=True)
    )