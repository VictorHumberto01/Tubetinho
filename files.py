import os

X=os.listdir('path to the bot directory')

for item in X:
    if item.endswith('.webm'):
        os.remove(item)

for item in X:
    if item.endswith('.mp3'):
        os.remove(item)
        
# This script removes the old music files from the bot directory. It's necessary to change the path on the 3rd line.
