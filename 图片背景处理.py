from PIL import Image

img = Image.open("d3.png")
x, y = img.size

try:
  # 使用白色来填充背景 from：www.jb51.net
  # (alpha band as paste mask).
  p = Image.new('RGBA', img.size, (255, 255, 255))
  p.paste(img, (0, 0, x, y), img)
  p.save('jb51.png')

except:
  pass

