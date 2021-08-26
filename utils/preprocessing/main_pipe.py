from . import pipeline


def run():
    df = pipeline.load_data()
    df = pipeline.preprocessing(df)
    pipeline.load_data(df)
