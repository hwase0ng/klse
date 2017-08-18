'''
Created on Jul 30, 2017

@author: hwase
'''
import Main.settings as S
import pandas as pd
from Download import downloadBursa as bursa

bursa_csv = S.WORK_DIR+"bursa.csv"
df = pd.read_csv(bursa_csv)

#for i in range(0,len(df)):
for i in range(0,1):
    cashtag = df['cashtag'][i]
    bursa.downloadBursa(cashtag)
    
if __name__ == '__main__':
    pass