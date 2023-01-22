from stores_sales.exception import Sales_Exception
from stores_sales.entity.config_entity import DataIngestionConfig
from stores_sales.entity.artifact_entity import DataIngestionArtifact
from stores_sales.logger import logging 
from stores_sales.constant import *
from stores_sales.config.configuration import Configuration
import sys, os
from stores_sales.entity.config_entity import DataIngestionConfig
import shutil
import pandas as pd 
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit


class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig ):
            try:
                logging.info(f"{'=='*20}Data Ingestion log started.{'='*20} ")
                self.data_ingestion_config = data_ingestion_config

            except Exception as e:
                raise Sales_Exception(e,sys) from e

    def download_sales_data(self,):
        try:
            download_location = self.data_ingestion_config.dataset_download_location

            #folder location to download file 
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            os.makedirs(raw_data_dir,exist_ok=True)

            sales_file_name = os.path.basename(download_location)

            raw_file_path = os.path.join(raw_data_dir, sales_file_name)
            logging.info(f"Downloading file from :[{download_location}] into :[{raw_file_path}]")

            shutil.copy(r'D:\Python Project\stores_sales_prediction\data\stores_sales.csv', raw_file_path)

            logging.info(f"File :[{raw_file_path}] has been downloaded successfully.")
            return raw_file_path

        except Exception as e:
            raise Sales_Exception(e,sys) from e


    def split_data_as_train_test(self,) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            sales_file_path = os.path.join(raw_data_dir,file_name)


            logging.info(f"Reading csv file: [{sales_file_path}]")
            sales_data_frame = pd.read_csv(sales_file_path)

            sales_data_frame["Item_MRP_cat"] = pd.cut(
                sales_data_frame["Item_MRP"],
                bins=[30,50,70,90,110,130,150,170,190,210,230,250,np.inf],
                labels=[1,2,3,4,5,6,7,8,9,10,11,12])
            

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index,test_index in split.split(sales_data_frame, sales_data_frame["Item_MRP_cat"]):
                strat_train_set = sales_data_frame.loc[train_index].drop(["Item_MRP_cat"],axis=1)
                strat_test_set = sales_data_frame.loc[test_index].drop(["Item_MRP_cat"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise Sales_Exception(e,sys) from e
    
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            tgz_file_path =  self.download_sales_data()
            return self.split_data_as_train_test()
        except Exception as e:
            raise Sales_Exception(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")

