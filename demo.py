from stores_sales.config.configuration import Configuration
from stores_sales.exception import Sales_Exception
from stores_sales.logger import logging 
from stores_sales.pipeline.pipeline import Pipeline




def main():
    pipeline = Pipeline()
    pipeline.start()
    print(pipeline.experiment.running_status)

if __name__ == "__main__":
    main()