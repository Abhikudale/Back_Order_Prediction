import logging
from multiprocessing import Pipe
from unicodedata import name
from housing import pipeline
from housing.pipeline.pipeline import Pipeline

def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__=="__main__":
    main()
