import os

X=os.listdir('/mnt/HDD2/Python/bot')

for item in X:
    if item.endswith('.webm'):
        os.remove(item)

for item in X:
    if item.endswith('.mp3'):
        os.remove(item)
