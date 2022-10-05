import regex as re
from torch import index_add

# def replaceWordContinous(text):

def combineNumber(text):
    words = text.split()
    for index, word in enumerate(words):
        if word.isdecimal():
            index_decimal = index
            while index_decimal < len(words):
                if words[index_decimal].isdecimal():
                    print(word + " " + words[index_decimal])
                    index_decimal += 1
                    if index_decimal == len(words):
                        print("End")
                        break

combineNumber(" 0 9 8 7 1 ")