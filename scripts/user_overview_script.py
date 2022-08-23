import pandas as pd

class UserOverviewScript():
    def __init__(self, df) -> None:
        self.df = df.copy()


    def get_top_handsets(self,  num):
        top_handset = self.df['Handset Type'].value_counts().head(num)
        return top_handset


    def get_top_manufacturers(self,  num):
        top_handset = self.df['Handset Manufacturer'].value_counts().head(num)
        return top_handset

    
    def get_handset_group(self):
        top_3_manufacturers = self.get_top_manufacturers(3)

        manufacturers = self.df.groupby("Handset Manufacturer")

        for column in top_3_manufacturers.index:
            result = manufacturers.get_group(column).groupby("Handset Type")['MSISDN/Number'].nunique().nlargest(5)
            print(f">>>> { column } <<<<")
            print(result)
            print() 

    def convert_bytes_to_megabytes(self, column):
        """
            This function takes the dataframe and the column which has the bytes values
            returns the megabytesof that value            
        """        
        megabyte = 1*10e+5
        Total_MB = []
        for i in column.values:
            i = i / megabyte
            Total_MB.append(i)

        return Total_MB


    def convert_bytes_to_kbytes(self, column):
        """
            This function takes the dataframe and the column which has the bytes values
            returns the kilobytes of that value            
        """        
        Total_kb = []
        for i in column.values:
            i = i / 1024
            Total_kb.append(i)

        return Total_kb


    def convert_ms_to_sec(self, column):
        """
            This function takes the dataframe and the millisecond column values
            returns the second equivalence          
        """        
        
        Total_sec = []
        for i in column.values:
            i = (i / 1000) % 60
            Total_sec.append(i)

        return Total_sec