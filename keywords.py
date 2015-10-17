import os
import pandas as pd
import collections

class csvs:
    def __init__(self,path,filename):
        self.filename = filename
        self.path = path
        self.duplicates = []
        self.result = ""
        self.new_csv = ""
        self.get_new_csv()
    def get_new_csv(self):
        files = os.listdir(self.path)
        Files = []
        for file in files:
            df = pd.read_csv(path + str(file))
            Files.append(df)
            Columns = df.columns.values

        self.result = pd.concat(Files)
        self.result = self.result.sort_index(by='Keyword Rank', ascending=1)
        self.result = self.result[Columns]
        
        Keywords = self.result["Keyword"].tolist()
        
        lowest = []
        highest = []
        average = []
        delta = []
        WordRank = []

        for Keyword in Keywords:
            df_keyword = self.result[self.result["Keyword"]==Keyword]
            ranks = df_keyword["Word Rank"].tolist()
            if len(ranks) > 1:
                lowest.append(min(ranks))
                highest.append(max(ranks))
                average.append(sum(ranks)/float(len(ranks)))
                delta.append(max(ranks)-min(ranks))
                WordRank.append(None)
                if Keyword not in self.duplicates:
                    self.duplicates.append(Keyword)
            else:
                lowest.append(None)
                highest.append(None)
                average.append(None)
                delta.append(None)  
                WordRank.append(ranks[0])
        self.result["Highest"] = lowest
        self.result["Lowest"] = highest
        self.result["Average"] = average
        self.result["Delta"] = delta
        self.result["Word Rank"] = WordRank
        self.new_csv = self.result.drop_duplicates(subset="Keyword")
        self.new_csv.to_csv(self.filename)
    def export_keywords(self,ignore_list,txt_path):
        ignore_list = [word.lower() for word in ignore_list]
        Keywords = [keyword for keyword in self.new_csv["Keyword"].tolist() if keyword not in ignore_list]
        
        with open(txt_path,"w") as f:
            for Keyword in Keywords:
                f.write(str(Keyword) + "\n")
    def export_duplicates(self,ignore_list,txt_path):
        ignore_list = [word.lower() for word in ignore_list]
        Keywords = [keyword for keyword in self.duplicates if keyword not in ignore_list]
        with open(txt_path,"w") as f:
            for Keyword in Keywords:
                f.write(str(Keyword) + "\n")
    def export_duplicates_by_delta(self,ignore_list,txt_path):
        ignore_list = [word.lower() for word in ignore_list]
        
        df_list = []
        for Keyword in self.duplicates:
            df_list.append(self.new_csv[self.new_csv["Keyword"]==Keyword])
        df = pd.concat(df_list)
        df = df.sort_index(by='Delta', ascending=1)
        Keywords = [keyword for keyword in df["Keyword"].tolist() if keyword not in ignore_list]
        with open(txt_path,"w") as f:
            for Keyword in Keywords:
                f.write(str(Keyword) + "\n")
    def export_uniques(self,ignore_list,txt_path):
        ignore_list = [word.lower() for word in ignore_list]
        
        Keywords = []
        for keyword in self.new_csv["Keyword"].tolist():
            if keyword not in self.duplicates:
                if keyword not in ignore_list:
                    Keywords.append(keyword)
        
        with open(txt_path,"w") as f:
            for Keyword in Keywords:
                f.write(str(Keyword) + "\n")
