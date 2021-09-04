from utils.model import pipeline_model
from utils.preprocessing import pipeline_data


def run_whole_pipe() -> None:
    # Data
    df = pipeline_data.load_data()
    df = pipeline_data.preprocessing(df)
    df = pipeline_data.impute_cols(df)
    df = pipeline_data.feature_eng(df)
    pipeline_data.dump_data(df, './data/data/process/df_clean.parquet')

    # Modeling
    df = pipeline_model.load_data()
    df = pipeline_model.preprocess(df)
    pipeline_model.training(df)
    pipeline_model.inference()


run_whole_pipe()

