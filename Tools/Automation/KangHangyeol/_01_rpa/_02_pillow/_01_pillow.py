# pillow : 이미지 전처리(편집, 필터처리 등 다양한 기능을 지원하는 패키지

from PIL import Image

img_name = './molang.png'
img = Image.open(img_name)
img.show()