class Univariate():
    def QuanQual(dataset):
        Quan=[]
        Qual=[]
        for ColumnName in dataset.columns:
            print(ColumnName)
            if(dataset[ColumnName].dtypes=="O"):
                #print("Qual")
                Qual.append(ColumnName)
            else:
                #print("Quan")
                Quan.append(ColumnName)
        return Quan,Qual

    
    def UniVariate(dataset, Quan):
        import pandas as pd
        import numpy as np 
        descriptive = pd.DataFrame(index=["Mean", "Median", "Mode", "Q1:25%", "Q2:50%", "Q3:75%", "99%", "Q4:100%", "IQR", "1.5rule", 
                                          "Lesser", "Greater", "Min", "Max", "Skewness", "Kurtosis", "Variance", "Standard_Deviation"],
                                   columns=Quan)
        for ColumnName in Quan:
            descriptive.loc["Mean", ColumnName] = dataset[ColumnName].mean()
            descriptive.loc["Median", ColumnName] = dataset[ColumnName].median()
            descriptive.loc["Mode", ColumnName] = dataset[ColumnName].mode()[0]
            descriptive.loc["Q1:25%", ColumnName] = dataset.describe()[ColumnName]["25%"]
            descriptive.loc["Q2:50%", ColumnName] = dataset.describe()[ColumnName]["50%"]
            descriptive.loc["Q3:75%", ColumnName] = dataset.describe()[ColumnName]["75%"]
            descriptive.loc["99%", ColumnName] = np.percentile(dataset[ColumnName], 99)
            descriptive.loc["Q4:100%", ColumnName] = dataset.describe()[ColumnName]["max"]
            descriptive.loc["IQR", ColumnName] = descriptive.loc["Q3:75%", ColumnName] - descriptive.loc["Q1:25%", ColumnName]
            descriptive.loc["1.5rule", ColumnName] = 1.5 * descriptive.loc["IQR", ColumnName]
            descriptive.loc["Lesser", ColumnName] = descriptive.loc["Q1:25%", ColumnName] - descriptive.loc["1.5rule", ColumnName]
            descriptive.loc["Greater", ColumnName] = descriptive.loc["Q3:75%", ColumnName] + descriptive.loc["1.5rule", ColumnName]
            descriptive.loc["Min", ColumnName] = dataset[ColumnName].min()
            descriptive.loc["Max", ColumnName] = dataset[ColumnName].max()
            descriptive.loc["Skewness", ColumnName] = dataset[ColumnName].skew()
            descriptive.loc["Kurtosis", ColumnName] = dataset[ColumnName].kurtosis()
            descriptive.loc["Variance", ColumnName] = dataset[ColumnName].var()
            descriptive.loc["Standard_Deviation", ColumnName] = dataset[ColumnName].std()
        return descriptive


    def FindingOutlier(Quan,descriptive):
        Lesser=[]
        Greater=[]
        for ColumnName in Quan:
            if(descriptive[ColumnName]["Min"]<descriptive[ColumnName]["Lesser"]):
                Lesser.append(ColumnName)
            if(descriptive[ColumnName]["Max"]>descriptive[ColumnName]["Greater"]):
                Greater.append(ColumnName)
        return Lesser,Greater

    def ReplacingOutliers(dataset, descriptive, Quan, Lesser, Greater):
        for ColumnName in Lesser:
            dataset.loc[dataset[ColumnName] < descriptive[ColumnName]["Lesser"], ColumnName] = descriptive[ColumnName]["Lesser"]
        for ColumnName in Greater:
            dataset.loc[dataset[ColumnName] > descriptive[ColumnName]["Greater"], ColumnName] = descriptive[ColumnName]["Greater"]
        return dataset

    def FreqTable(ColumnName, dataset):
        import pandas as pd
        FreqTable = pd.DataFrame(columns=["Unique_Values", "Frequency", "Relative_Frequency", "Cummulative_Frequency or cumsum"])
        FreqTable["Unique_Values"] = dataset[ColumnName].value_counts().index
        FreqTable["Frequency"] = dataset[ColumnName].value_counts().values
        total_count = len(dataset[ColumnName])
        FreqTable["Relative_Frequency"] = FreqTable["Frequency"] / total_count
        FreqTable["Cummulative_Frequency or cumsum"] = FreqTable["Relative_Frequency"].cumsum()
        return FreqTable