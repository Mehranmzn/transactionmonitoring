import os
import sys
import json
import pandas as pd
from dotenv import load_dotenv
import pymongo
import certifi
from src.exception.exception import SrcException
from src.logging.logger import logging




load_dotenv()
certified = certifi.where()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class TransactionMonitoringExtract():
    def __init__(self):

        try:
            pass
        except Exception as e:
            raise SrcException(e,sys)
        

    def csv_to_json(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise SrcException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL, 
                                                  tls=True,
                                                  tlsAllowInvalidCertificates=True)
            self.database = self.mongo_client[self.database]
            
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise SrcException(e,sys)
        
if __name__=='__main__':
    FILE_PATH="TMdata/transactiondata.csv"
    DATABASE="transactionmonitoring"
    Collection="TM"
    tmobj=TransactionMonitoringExtract()
    records=tmobj.csv_to_json(file_path=FILE_PATH)
    #print(records)
    no_of_records=tmobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)
        



