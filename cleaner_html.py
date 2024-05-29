import os
from os.path import isfile, join

folder_path = 'html'

def html_cleaner():
    
    files = sorted([f for f in os.listdir(folder_path) 
                    if os.path.isfile(os.path.join(folder_path, f))])
    
    if len(files) > 2:
        for i in range(len(files)-2):
            print(files[i])
            os.remove(f'{folder_path}/{files[i]}')

html_cleaner()