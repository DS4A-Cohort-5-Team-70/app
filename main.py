from utilities.cleaning import pipeline

def run():
    if __name__ == '__main__':
        df = pipeline.load_data()
        df = pipeline.preprocessing(df)
        pipeline.load_data(df)
    
