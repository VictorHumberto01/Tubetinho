import os

X=os.listdir('Path to where the musics are being saved')

for item in X:
    if item.endswith('.webm'):
        os.remove(item)

for item in X:
    if item.endswith('.mp3'):
        os.remove(item)
        
# This script removes the old music files from the music directory. In linux servers the musics are located in the home directory. It's necessary to change the path on the 3rd line.
