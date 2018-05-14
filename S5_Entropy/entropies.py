# Possible template to start TP5

"""Compute the entropy of different models for text
            
Usage: compress [-m <model>] [-f <file>] [-o <order>]

Options:
-h --help      Show the description of the program
-f <file> --filename <file>  filename of the text to compress [default: Dostoevsky.txt]
-o <order> --order <order>  order of the model
-m <model> --model <model>  model for compression [default: IIDModel]
"""

import argparse, re
import numpy as np
import math
from collections import Counter 

class IIDModel:
    """An interface for the text model"""
    def __init__(self, order=2):
        print("Creation of the model")
        self.order = order
        # ...
        
    def process(self,text):
        self.dict_symbols={}
        for i in range(len(text)-self.order):
            symbol=text[i:i+self.order]
            self.dict_symbols[symbol] = self.dict_symbols.get(symbol,0)+1
        self.dict_symbols
        pass

    def getEntropy(self):
        count_symbols=sum(self.dict_symbols.values())
        dict_proba={}
        list_symbols=[k for k,v in self.dict_symbols.items()]
        for symbol in list_symbols:
            dict_proba[symbol] = float(self.dict_symbols[symbol])/count_symbols
        return sum([ v*np.log2(1/v) for k,v in dict_proba.items()])

    def getCrossEntropy(self, text): #text = "target" text here!
        
        target_dict_symbols = {}
        for i in range(len(text)-self.order):
            symbol = text[i:i+self.order]
            target_dict_symbols[symbol] = target_dict_symbols.get(symbol,0)+1

        # Compute Entropy for target text
        count = sum(target_dict_symbols.values())
        new_proba={}
        target_symbols=[k for k,v in target_dict_symbols.items()]
        for symbol in target_symbols:
            new_proba[symbol] = float(target_dict_symbols[symbol])/count
        Entropy = sum([ v*np.log2(1/v) for k,v in new_proba.items()])
        
        # Compute Cross-entropy
        CrossEntropy = 0
        KL = 0
        for symbol in target_dict_symbols:
            p = float(target_dict_symbols[symbol]) / sum(target_dict_symbols.values()) 
            if symbol in self.dict_symbols: 
                q = float(self.dict_symbols[symbol]) / sum(self.dict_symbols.values()) 
                KL += p * np.log2(p / q)
            else:
                KL += p * np.log2(p / 0.00000001)
        CrossEntropy = Entropy + KL
        return CrossEntropy


class MarkovModel:
    """An interface for the text model"""
    def __init__(self, order=2):
        print("Creation of the model")
        self.order = order
        # ...

    def process(self, text):
        # ...
        self.src_text = text #.replace('\n','').replace(' ','').lower()
        
        self.Current_dict = {}
        for i in range(len(self.src_text)-self.order):
            symbol = self.src_text[i : i+self.order]
            self.Current_dict[symbol] = self.Current_dict.get(symbol,0)+1

        self.Past_dict = {}
        for i in range(len(self.src_text)-self.order):
            symbol = self.src_text[i : i+self.order-1]
            self.Past_dict[symbol] = self.Past_dict.get(symbol,0)+1
        
        #return (self.Current_symbol , self.Past_dict)
        pass
    
    def getEntropy(self):
        # ...

        total = sum(self.Current_dict.values())
        
        E=0
        for symbol in self.Current_dict:
            symbol_key = str(symbol)
            past_symbol = symbol_key[:self.order-1]
            proba_cond = float(self.Current_dict[symbol])/float(self.Past_dict[past_symbol])
            proba = float(self.Current_dict[symbol])/total
            E -= proba*np.log2(proba_cond)
        return E
    
    def getCrossEntropy(self, text):
        # ...
        target_Curr_dict = {}
        target_Past_dict = {}
        
        for i in range(len(text)-self.order):
            symbol = text[i : i+self.order]
            target_Curr_dict[symbol] = target_Curr_dict.get(symbol,0)+1

        for i in range(len(text)-self.order):
            symbol = text[i : i+self.order-1]
            target_Past_dict[symbol] = target_Past_dict.get(symbol,0)+1
        
        total =sum(target_Curr_dict.values())
        
        # Compute Entropy for target text

        E=0
        for symbol in target_Curr_dict:
            symbol_key = str(symbol)
            past_symbol = symbol_key[:self.order-1]
            proba_cond = float(target_Curr_dict[symbol])/float(target_Past_dict[past_symbol])
            proba = float(target_Curr_dict[symbol])/total
            E -= proba*np.log2(proba_cond)
        target_Entropy = E

        cross_entropy = 0
        KL = 0
        
        for symbol in target_Curr_dict:

            past_symbol=symbol[:self.order-1]

            cond_p = float(target_Curr_dict[symbol]) / float(target_Past_dict[past_symbol])      
            cross_p = float(target_Curr_dict[symbol]) / total
            
            if symbol in self.Current_dict: 
                cond_q = float(self.Current_dict[symbol]) / float(self.Past_dict[past_symbol])
                KL += cross_p * np.log2(cond_p / cond_q)
            else:
                KL += cross_p * np.log2(cond_p / 0.000000001)
        cross_entropy = target_Entropy + KL
        #return (cross_entropy,KL)
        return cross_entropy
    
def preprocess(text):
    text = re.sub("\s\s+", " ", text)
    text = re.sub("\n", " ", text)
    return text

# Experiencing encoding issues due to UTF8 (on possibly other texts)? Consider:
#  f.read().decode('utf8')
#  blabla.join(u'dgfg')
#              ^
'''
def plot_entropy(Entropy,dep_list):
    plt.figure(figsize=(15,10))
    plt.plot(Entropy)
    plt.title("Question 1 - Plot Entropy for IID model", size=25)
    plt.ylabel('Entropy', size=20)
    plt.xlabel('Order of dependency', size=20)
    row_labels = ['Order k', 'Entropy']
    Entropy=[round(k,2) for k in Entropy]
    table_vals=[dep_list,Entropy]
    table=plt.table(cellText=table_vals,
                      colWidths = [0.08]*10,
                      rowLabels=row_labels,
                      loc='lower right')
    table.auto_set_font_size(False)
    table.set_fontsize(16)
    table.scale(1, 2.5)
    plt.show()
    pass
'''


if __name__ == '__main__':    
    from docopt import docopt

    # Retrieve the arguments from the command-line
    args = docopt(__doc__)
    print(args)

    # Read and preprocess the text
    src_text = preprocess(open(args["--filename"]).read())
    #src_text = preprocess(open("Dostoevsky.txt").read())
    target_text = preprocess(open("Goethe.txt").read())

    
    # Create the model
    if(args["--model"]=="IIDModel"):
    #    model = IIDModel(int(args["--order"]))
        model = IIDModel(int(2))
    elif(args["--model"]=="MarkovModel"):
    #    model = MarkovModel(int(args["--order"]))
        model = MarkovModel(int(2))

    #model = MarkovModel(int(2))
    model.process(src_text)
    print(model.getEntropy())
    print(model.getCrossEntropy(target_text))
    
