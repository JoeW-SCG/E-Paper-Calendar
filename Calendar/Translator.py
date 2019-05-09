from Dictionary import default_language, dictionary_collection
from settings import language

'''Looks up a phrase in a given dictionary-collection
and returns the translated phrase'''

def translate(phrase, target_lang = language, dictionary_collection = dictionary_collection) :
    dictionary = find_dictionary(dictionary_collection, phrase)

    if dictionary == None:
        return phrase

    if target_lang in dictionary.keys():
        return dictionary[target_lang]
    else:
        return dictionary[default_language]


def find_dictionary(dictionary_collection, phrase):
    for dictionary in dictionary_collection:
        if phrase in dictionary.values():
            return dictionary
    return None