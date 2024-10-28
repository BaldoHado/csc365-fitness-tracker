import polars as pl

def read_data(path: str):
    df = pl.read_excel(path)
    return df.select("Name").to_series().to_list()