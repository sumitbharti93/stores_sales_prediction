from stores_sales.config.configuration import Configuration
from stores_sales.exception import Sales_Exception
from stores_sales.logger import logging 
from stores_sales.pipeline.pipeline import Pipeline




def main():
    config = Configuration()
    pipeline = Pipeline(config=config)
    pipeline.start_data_ingestion()

if __name__ == "__main__":
    main()