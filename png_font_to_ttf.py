from __future__ import print_function
import sys
import fontforge
from PIL import Image

if len(sys.argv) != 5:
    print('usage: %s <output.otf> <input.png> <char-width> <char-height>' % sys.argv[0], file=sys.stderr)
    sys.exit(1)

output = sys.argv[1]
image = Image.open(sys.argv[2])
width = int(sys.argv[3])
height = int(sys.argv[4])

factor = 10 # size factor so that coords are in range [16, 65536]
private_range = 0xe000 # starting codepoint of private copy
background = (0, 0, 0) # background RGB color

font = fontforge.font() 
font.ascent = height * factor
font.descent = 0 * factor
font.encoding = 'UnicodeFull' # required encoding to access private range

pixels = image.load()

for j in range(image.height // height):
    for i in range(image.width // width):
      offset = i + j * (image.width // width)

      # generate two copies of char, in 0-256 and in private range
      for codepoint in [offset, private_range + offset]:
          char = font.createChar(codepoint)
          char.width = width * factor
          pen = char.glyphPen()

          # draw each non-background pixel as a square
          for y in range(height):
              for x in range(width):
                  pixel = pixels[i * width + x, j * height + y]
                  if pixel != background:
                      pen.moveTo((x * factor, (height - y) * factor)) # draw a pixel
                      pen.lineTo(((x + 1) * factor, (height - y) * factor))
                      pen.lineTo(((x + 1) * factor, (height - y - 1) * factor))
                      pen.lineTo((x * factor, (height - y - 1) * factor))
                      pen.closePath()

# export to font 
font.generate(output, flags=('opentype'))
