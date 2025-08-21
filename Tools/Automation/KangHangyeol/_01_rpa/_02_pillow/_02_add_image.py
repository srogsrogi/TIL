# 엑셀에 이미지 저장하기

import openpyxl as op
from openpyxl.drawing.image import Image
from PIL import Image as PILImage
# openpyxl의 Image는 pillow에 의존하고 있어서 사용하려면 pillow 설치 필요

img_name = 'molang.png'
path = '이미지.xlsx'

wb = op.Workbook()
ws = wb.active

# 이미지 크기 변환
pi_img = PILImage.open(img_name)

resized_img = pi_img.resize ((100,100))
resized_img.save('resized_molang', 'PNG', quality =95) # quality default 75, maximum 95

# 이미지 객체 생성
img_name = 'resized_molang.png'
img = Image(img_name)
print(type(img),img)

# 이미지 추가
ws.add_image(img, 'B2')




wb.save(path)