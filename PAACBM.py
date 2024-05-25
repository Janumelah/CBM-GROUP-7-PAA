from PIL import Image, ImageDraw
import tkinter

size = 1500

canvas = Image.new("RGB", (720,720) , color="pink")

maps = ImageDraw.Draw(canvas)

canvas.show()
canvas.save("maps.png")
