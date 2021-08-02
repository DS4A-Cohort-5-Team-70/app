from . import preprocessing


def run() -> None:
    df = preprocessing.load_data()
    df = preprocessing.transform(df)
    metrics_dict = preprocessing.training(df)
    # TODO: Implement subsequent steps
