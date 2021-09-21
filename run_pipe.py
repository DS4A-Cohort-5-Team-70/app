from utils.model import pipeline_model
from utils.preprocessing import pipeline_data


def run_whole_pipe(path_raw_csv: str, path_clean_data: str, path_to_model: str='', retrain: bool = False) -> None:
    # Data
    df = pipeline_data.load_data(path_raw_csv)
    df = pipeline_data.preprocessing(df)
    df = pipeline_data.impute_cols(df)
    df = pipeline_data.feature_eng(df)
    pipeline_data.dump_data(df, path_clean_data)

    # Modeling
    if retrain:
        df = pipeline_model.load_data(path_clean_data)
        df = pipeline_model.preprocess(df)
        pipeline_model.training(df, path_to_model)
        pipeline_model.inference(path_clean_data)


# run_whole_pipe('./data/data/ingestion/asesor.csv', './data/data/process/df_clean.parquet', './data/model/model/trained_model.pickle', True)

