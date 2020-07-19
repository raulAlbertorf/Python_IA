#!/usr/bin/env python3
# conteo_mapper.py
"""Maps lines of text to key-value pairs of word lengths and 1."""
import sys

def tokenize_input():
    """Split each line of standard input into a list of strings."""
    for line in sys.stdin:
        yield line.split()

# read each line in the the standard input and for every word 
# produce a key-value pair containing the word, a tab and 1
for line in tokenize_input():
    for word in line:
        print(str(len(word)) + '\t1')

