from Dictionary import default_language, dictionary_collection
from settings import language

'''Looks up a phrase in a given dictionary-collection
and returns the translated phrase'''

def translate(phrase, target_lang = language, dictionary_collection = dictionary_collection) :
    dictionary = find_dictionary(phrase, dictionary_collection)

    if dictionary == None:
        return phrase

    if target_lang in dictionary.keys():
        return dictionary[target_lang]
    elif '_' in target_lang and target_lang.split('_')[0] in dictionary.keys():
        return dictionary[target_lang.split('_')[0]]
    else:
        return dictionary[default_language]

def find_dictionary(phrase, dictionary_collection = dictionary_collection):
    for dictionary in dictionary_collection:
        if phrase in dictionary.values():
            return dictionary
    return None