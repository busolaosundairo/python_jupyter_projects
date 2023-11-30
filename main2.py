#project: p7
#for loops depends on 
#fit and predict
#processing of input data by myself
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
import pandas as pd
import numpy as np

class UserPredictor:
    def __init__(self):
        self.model= LinearRegression()
        self.final=pd.DataFrame()
        print(self.model)
    
    def fit(self,users,logs,labels):
       
        tl=logs[logs.url.isin(['/laptop.html'])]
        del tl['date']
        tl2 = tl.groupby('user_id').sum()
        
        self.final=pd.merge(tl2, users, left_index=True, right_index=True)
        
        self.model.fit(self.final[["past_purchase_amt"]],self.final["seconds"])

        
    def predict(self,users,log):
        del users['age']
        del users['badge']
        del users['names']
        test_logs = log.groupby('user_id').sum()
        test_users=users.set_index(["user_id"])
        final2=pd.merge(test_logs,test_users, left_index=True, right_index=True)
        #model.predict(final2[["seconds"]])
        final2=test_users.join(log)
        final2.fillna(0, inplace=True)
        return self.model.predict(final2[["past_purchase_amt"]])

        
        
        
        
        
        
        
        
        