import os
import pandas as pd
from collections import Counter

class reader:
    def __init__(self,ignore_list,filename,top_number):
        self.ignore_list = [word.lower() for word in ignore_list]
        self.filename = filename
        self.top_number = top_number
        self.bag_of_words = []
        self.read()
    def read(self):
        with open(self.filename,"r") as f:
            for line in f:
                self.bag_of_words.append(line)
    def top_words(self):
        n = 1
        frequency_words = []
        
        occurrence_dictionary = {}
        for bag in self.bag_of_words:
            for word in bag.split(): 
                if word not in self.ignore_list:
                    if word not in frequency_words:
                        occurrence_dictionary[word] = n
                    frequency_words.append(word)
            n += 1
            
        counting = Counter(frequency_words)
        frequency = counting.most_common(self.top_number)
        
        occurrence_ordered = [(word_vab,freq_vab,occurrence_dictionary[word_vab]) for word_vab,freq_vab in frequency]
        occurrence_ordered = sorted(occurrence_ordered,key=lambda x: x[2])
        
        return frequency,occurrence_ordered
    def get_top_words(self,sort_indicator):
        frequency_variable,occurrence_variable = self.top_words()
        
        if sort_indicator == "frequency":
            return frequency_variable
        elif sort_indicator == "occurence":
            return occurrence_variable
        
    def get_frequency_of_word(self,word):
        n = 0
        for words in self.bag_of_words:
            if word in words:
                n += 1
        return n/float(len(self.bag_of_words))
    def get_first_occurrence(self,word):
        n = 1
        value = 0
        for line in self.bag_of_words:
            if word in line:
                value = n
                break
            n += 1
        return value
    def get_average_rank(self,word):
        n = 1
        sum = 0
        number_of_lines = 0
        for bag in self.bag_of_words:
            if word in bag:
                if word not in self.ignore_list:
                    sum = sum + n
                    number_of_lines += 1
            n += 1
        if number_of_lines > 0:
            return sum/float(number_of_lines)
        else:
            return "Word not present or ignored"
    def get_top_words_csv(self, file_ordered_by_frequency,file_ordered_by_occurence):
        frequency_variable,occurrence_variable = self.top_words()
        words = [word for word,freq in frequency_variable]
        frequency = [freq for word,freq in frequency_variable]
        average_rank = [self.get_average_rank(word) for word in words]
        first_occurrences = [self.get_first_occurrence(word) for word in words]
        
        df = pd.DataFrame({'Keywords': words,
                           'Frequency': frequency,
                           'Average Rank': average_rank,'First Occurrence': first_occurrences})
        
        #new_file_name has to include the absolute path to your new file
        df = df.sort_index(by='Frequency', ascending=0)
        df.to_csv(file_ordered_by_frequency)
        df = df.sort_index(by='First Occurrence', ascending=1)
        df.to_csv(file_ordered_by_occurence)
