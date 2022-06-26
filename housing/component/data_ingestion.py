

from cmath import e
import logging
import sys
from housing.entity.config_entity import DataIngestionConfig
from housing.exception import HousingException


class DataInhestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20}")
        except Exception as e:
            raise HousingException(e,sys) from e


    def initiate_data_ingestion(self) ->DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e