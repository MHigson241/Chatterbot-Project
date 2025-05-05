# -*- coding: utf-8 -*-
"""

###### TRAINING DATA CLEANER ######

"""

import pandas as pd

dataDF = pd.read_csv("raw_data.csv")


trainingDF = pd.DataFrame()

index = 0
for message in dataDF:
    date = dataDF.at[index, "date"]
    name = dataDF.at[index, "author.global_name"]
    content = dataDF.at[index, "content"]
    messageDF = pd.DataFrame({"date": [date], "name": [name], "content": [content]})
    trainingDF = pd.concat([trainingDF, messageDF])
    index += 1
    
trainingDF.to_csv("training_data.csv", index = False, header = False)