import yaml
import sys 
from stores_sales.exception import Sales_Exception
from stores_sales.logger import logging



def read_yaml_file(file_path:str)->dict:
    '''
    except file path as a parameter and return dictionary as output 
    '''
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise Sales_Exception(e, sys)  from e