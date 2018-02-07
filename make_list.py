#!/usr/bin/env python
from PyDictionary import PyDictionary

class NoDefinition(Exception):
    pass

def make_list(wordlist: list):
    """Makes a term: definiton list.
    
    make_list(wordlist) -> ([str, str, str], [str, str, str])"""
    terms, definitions = [], []
    dictionary = PyDictionary()
    
    for word in wordlist:
        terms.append(word)
        print(word)

        definition = ''
        defs = dictionary.meaning(word)

        if defs is None:
            definitions.append('No definition has been found for this term.')
            continue

        for wordtype in defs:
            definition += f'{wordtype}:\n'
            definition += f'  {defs[wordtype][0]} \n'

        definitions.append(definition)

    return (terms, definitions)
    