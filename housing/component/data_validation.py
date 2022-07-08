
from cgi import test
from email import message
import os
import sys
from housing.constant import DATA_INGESTION_ARTIFACT_DIR
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import pandas as pd
import json

class DataValidation:
    


    def __init__(self, data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise HousingException(e,sys) from e

    def is_train_test_file_exist(self)->bool:
        try:
            logging.info(f"Checking if training and test file is available")
            is_train_file_exist=False
            is_test_file_exist=False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)
            
            is_available = is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exist?-> {is_available}")

            is_available = self.is_train_test_file_exist()
            
            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message=f"Training File: {training_file} or Testing File: {testing_file}\
                is not present"
                raise Exception(message)
                validation_status=self.validate_dataset_schema()


        except Exception as e:
            raise HousingException(e,sys) from e

    def get_train_and_test_df(self):
        try:
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df=self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report = json.load(profile.json())

            report_file_path=self.data_validation_config.report_file_path

            report_dir=os.path.dirname(report_file_path)

            os.makedirs(report_dir,exist_ok=True)
            
            with open(self.data_validation_config.report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)

        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, test_df=self.get_train_and_test_df()
            dashboard.calculate()
            
            report_page_file_path=self.data_validation_config.report_file_path

            report_page_dir=os.path.dirname(report_page_file_path)

            os.makedirs(report_page_dir,exist_ok=True)
            
            dashboard.save(report_page_file_path)

        except Exception as e:
            raise HousingException(e,sys) from e

    def is_data_drift_found(self):
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            self.is_train_test_file_exist()
            self.validate_dataset_schema()
            self.is_data_drift_found()
            data_validation_artifact=DataValidationArtifact(
                schema_file_path=self.data_validation_config.scheme_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation Performed Successfully."
            )
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            
            return data_validation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e

    def validate_dataset_schema(self)->bool:
        try:
            validation_status = False

            #Validate Training and Testing dataset using schema file
            #1. Number of column
            #2. Check the values of ocean proximity
            # acceptable values <1H OCEAN
            # INLAND
            # ISLAND
            # NEAR BAY
            # NEAR OCEAN
            #3. Check column names


            validation_status = True

            return validation_status
        except Exception as e:
            raise HousingException(e,sys) from e