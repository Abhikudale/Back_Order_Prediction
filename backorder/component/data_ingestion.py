
import shutil
import tarfile
from sklearn.model_selection import StratifiedShuffleSplit
from six.moves import urllib
from backorder.entity.config_entity import DataIngestionConfig
from backorder.exception import BackOrderException
from backorder.entity.artifact_entity import DataIngestionArtifact
from backorder.logger import logging
import pandas as pd
import numpy as np
import os, sys
from imblearn.over_sampling import SMOTE 
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise BackOrderException(e,sys) from e

    def download_backorder_data(self,) -> str:
        try:
            #extract remote url to download dataset
            
            download_url = self.data_ingestion_config.dataset_download_url
            #download_url = os.path.join(os.curdir, download_url)
            #folder location to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            
            os.makedirs(tgz_download_dir,exist_ok=True)
            backorder_file_name = os.path.basename(download_url)

            tgz_file_path = os.path.join(tgz_download_dir,backorder_file_name)
            logging.info(f"Copied file from :[{download_url}] in to :[{tgz_file_path}]")
            shutil.copy(src=download_url,dst=tgz_file_path)
            #urllib.request.urlretrieve(download_url,tgz_file_path)
            logging.info(f"File:[{tgz_file_path}] has been received successfully")

            return tgz_file_path

        except Exception as e:
            raise BackOrderException(e,sys) from e

    def extract_tgz_file(self,tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info("Copy file from tgz file: [{tgz_file_path}] in to dir: [{raw_data_dir}]")
            #shutil.copy(src=tgz_file_path,dst=raw_data_dir)
            #shutil.copy(src=tgz_file_path,dst=raw_data_dir)
            with tarfile.open(tgz_file_path) as backorder_tgz_file_obj:
                backorder_tgz_file_obj.extractall(path=raw_data_dir)
            logging.info(f"File copying completed")
            
        
        except Exception as e:
            raise BackOrderException(e,sys) from e

    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            
            file_name = os.listdir(raw_data_dir)[0]
            
            backorder_file_path = os.path.join(raw_data_dir,file_name)
            
            logging.info(f"Reading csv file:[{backorder_file_path}]")

            backorder_data_frame = pd.read_csv(backorder_file_path)

            backorder_data_frame = backorder_data_frame.head(10000)
            
            
            logging.info(f"Splitting data in to Train and Test dataset")
            train_set = None
            test_set = None
            
            backorder_data_frame_Yes = backorder_data_frame.loc[backorder_data_frame['went_on_backorder'] == 'Yes']
            row_size_yes = backorder_data_frame_Yes.shape[0]
            
            backorder_data_frame_No = backorder_data_frame.loc[backorder_data_frame['went_on_backorder'] == 'No']
            backorder_data_frame_No = backorder_data_frame_No.sample(row_size_yes)

            # Concatenate the rows from the Yes dataset and No dataset into the backorder_data_frame.
            backorder_data_frame = None
            frames = [backorder_data_frame_No, backorder_data_frame_Yes]
            backorder_data_frame = pd.concat(frames)
            
            backorder_data_frame.reset_index(drop=True,inplace=True)
            backorder_data_frame.reset_index()
            
            X = backorder_data_frame.iloc[:,:-1]
            y = backorder_data_frame.iloc[:,-1]

            X_train, X_test, y_train, y_test = train_test_split(X , y, test_size=0.2, random_state=42)
            train_set = X_train
            train_set['went_on_backorder'] = y_train
            test_set = X_test
            test_set['went_on_backorder'] = y_test

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            if train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training dataset in to file:[{train_file_path}]")
                train_set.to_csv(train_file_path,index=False)
                
            if test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f"Exporting testing dataset in to file:[{test_file_path}]")
                test_set.to_csv(test_file_path,index=False)
                
            data_ingestion_artifact = DataIngestionArtifact(train_file_path = train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data ingestion Artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise BackOrderException(e,sys) from e

    def initiate_data_ingestion(self) ->DataIngestionArtifact:
        try:
            tgz_file_path = self.download_backorder_data()

            self.extract_tgz_file(tgz_file_path=tgz_file_path)

            return self.split_data_as_train_test()

        except Exception as e:
            raise BackOrderException(e,sys) from e

    def __del__(self):
        logging.info(f"{'='*20}Data Ingestion log completed.{'='*20}\n\n")
