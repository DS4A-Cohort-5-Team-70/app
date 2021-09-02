from . import pipeline


def run_pipeline():
    df = pipeline.load_data()
    df = pipeline.preprocessing(df)
    pipeline.dump_data(df, './data/data/process/df_clean.parquet')
