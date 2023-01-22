from stores_sales.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from stores_sales.config.configuration import Configuration
from stores_sales.exception import Sales_Exception
from stores_sales.logger import logging 
from stores_sales.component.data_ingestion import DataIngestion
from stores_sales.component.data_validation import DataValidation
import sys, os

class Pipeline:
    def __init__(self,config:Configuration)->None:
        try:            
            self.config=config
        except Exception as e:
            raise Sales_Exception(e,sys) from e
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise Sales_Exception(e, sys) from e

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config = self.config.get_data_validation_config(),
                                data_ingestion_artifact=data_ingestion_artifact)
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise Sales_Exception(e,sys) from e

    
    def run(self):
        data_ingestion_artifact = self.start_data_ingestion()
        self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)