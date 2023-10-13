from PIL import Image

img = Image.open('icons/white_bg.png')
img = img.resize((150, 100), Image.ANTIALIAS)
img.save('icons/white_bg.png')