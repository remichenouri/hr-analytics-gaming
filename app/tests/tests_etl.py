import pandas as pd
from utils.etl import extract, transform

def test_transform_removes_duplicates(tmp_path):
    sample = tmp_path / "s.csv"
    sample.write_text("id,val\n1,10\n1,10\n2,20")
    df_clean = transform(extract(sample))
    assert df_clean.shape[0] == 2

def test_transform_fills_na(tmp_path):
    sample = tmp_path / "s.csv"
    sample.write_text("id,department\n1,Design\n2,")
    df_clean = transform(extract(sample))
    assert df_clean["department"].isna().sum() == 0
