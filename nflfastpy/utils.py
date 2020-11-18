import codecs
import numpy as np

def convert_to_gsis_id(new_id):
    """
    Convert new player id columns to old gsis id
    """
    if type(new_id) == float:
        return new_id
        
    return codecs.decode(new_id[4:-8].replace('-',''),"hex").decode('utf-8')