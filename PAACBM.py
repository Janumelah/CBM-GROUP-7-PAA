import random
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import ttk
from numpy import sort

big_building_image = Image.new("RGB", (10, 5), "red")
medium_building_image = Image.new("RGB", (5, 3), "blue")
small_building_image = Image.new("RGB", (2, 2), "yellow")
house_image = Image.new("RGB", (1, 2), "white")

def generate_map(map_size, cell_size):
    canvas = Image.new("RGB", (map_size * cell_size, map_size * cell_size), "green")
    draw = ImageDraw.Draw(canvas)
    size = map_size
    road_cells = set()
    building_cells = set()

    vertice = []

    count = 0

    def place_building(image, x, y, width, height):
        building = image.resize((width * cell_size, height * cell_size))
        canvas.paste(building, (x * cell_size, y * cell_size))
        for i in range(width):
            for j in range(height):
                building_cells.add((x + i, y + j))

    def generate_roads():
        nonlocal count
        x, y = 0, 100
        directionsY = [(0, 150), (0, -150)]
        directionsX = [(150, 0), (-150, 0)]
        arah = "x"
        for _ in range(5500):  # worst case
            count += 1
            if count >= 5000 and (x <= 0 or x >= 1500 or y <= 0 or y >= 1500): 
                break  # best case kurang dari worst case
            if 0 <= x < 1500 and 0 <= y < 1500:
                vertice.append((x, y))
                road_cells.add((x, y))
                current_direction = random.choice(directionsX if arah == "x" else directionsY)
                xDraw = sort([x, x + current_direction[0]])
                yDraw = sort([y, y + current_direction[1]])
                draw.rectangle(((xDraw[0], yDraw[0]), (xDraw[1] + 10, yDraw[1] + 10)), "gray")
               
                x += current_direction[0]
                y += current_direction[1]
                if x <= 0: 
                    x = 1500
                if x >= 1500: 
                    x = 0
                if y <= 0: 
                    y = 1500
                if y >= 1500: 
                    y = 0
                arah = "x" if arah == "y" else "y"

    def generate_buildings():
        def can_place_building(x, y, width, height):
            for i in range(width):
                for j in range(height):
                    if (x + i, y + j) in road_cells or (x + i, y + j) in building_cells:
                        return False
            return True

        def is_green(x, y, width, height):
            for i in range(width):
                for j in range(height):
                    if canvas.getpixel(((x + i) * cell_size + 5, (y + j) * cell_size + 5)) != (0, 128, 0):
                        return False
            return True

        # Place large buildings
        for _ in range(20):
            placed = False
            while not placed:
                x = random.randint(0, size - 10)
                y = random.randint(0, size - 5)
                if can_place_building(x, y, 10, 5) and is_green(x, y, 10, 5):
                    place_building(big_building_image, x, y, 10, 5)
                    placed = True

        # Place medium buildings
        for _ in range(40):
            placed = False
            while not placed:
                x = random.randint(0, size - 5)
                y = random.randint(0, size - 3)
                if can_place_building(x, y, 5, 3) and is_green(x, y, 5, 3):
                    place_building(medium_building_image, x, y, 5, 3)
                    placed = True

        # Place small buildings
        for _ in range(40):
            placed = False
            while not placed:
                x = random.randint(0, size - 2)
                y = random.randint(0, size - 2)
                if can_place_building(x, y, 2, 2) and is_green(x, y, 2, 2):
                    place_building(small_building_image, x, y, 2, 2)
                    placed = True

        # Place houses
        for _ in range(40):
            placed = False
            while not placed:
                x = random.randint(0, size - 1)
                y = random.randint(0, size - 2)
                if can_place_building(x, y, 1, 2) and is_green(x, y, 1, 2):
                    place_building(house_image, x, y, 1, 2)
                    placed = True

    def generate_tree():
        for x in range(size):
            for y in range(size):
                if (x, y) not in road_cells and (x, y) not in building_cells and canvas.getpixel((x * cell_size + 5, y * cell_size + 5)) == (0, 128, 0):
                    if random.random() < 0.1:
                        draw.ellipse([x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size], fill="darkgreen")

    generate_roads()
    generate_buildings()
    generate_tree()
    
    return canvas

def update_map():
    global count
    count = 0
    map_size = 150
    cell_size = 10
    canvas_image = generate_map(map_size, cell_size)
    canvas_tk = ImageTk.PhotoImage(canvas_image)
    canvas_widget.create_image(0, 0, anchor='nw', image=canvas_tk)
    canvas_widget.image = canvas_tk
    canvas_widget.config(scrollregion=(0, 0, canvas_image.width, canvas_image.height))

def zoom(event):
    scale = 1.1 if event.delta > 0 else 0.9
    canvas_widget.scale("all", event.x, event.y, scale, scale)
    canvas_widget.configure(scrollregion=canvas_widget.bbox("all"))

def zoom_in():
    canvas_widget.scale("all", canvas_widget.winfo_width() // 2, canvas_widget.winfo_height() // 2, 1.1, 1.1)
    canvas_widget.configure(scrollregion=canvas_widget.bbox("all"))

def zoom_out():
    canvas_widget.scale("all", canvas_widget.winfo_width() // 2, canvas_widget.winfo_height() // 2, 0.9, 0.9)
    canvas_widget.configure(scrollregion=canvas_widget.bbox("all"))

# Tkinter UI
root = tk.Tk()
root.title("City Map Generator")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

canvas_frame = ttk.Frame(mainframe)
canvas_frame.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.N + tk.S))

canvas_widget = tk.Canvas(canvas_frame, width=800, height=600, bg="white")
canvas_widget.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.N + tk.S))

hbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas_widget.xview)
hbar.grid(row=1, column=0, sticky=(tk.W + tk.E))
vbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas_widget.yview)
vbar.grid(row=0, column=1, sticky=(tk.N + tk.S))

canvas_widget.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

generate_button = ttk.Button(mainframe, text="Generate Map", command=update_map)
generate_button.grid(row=0, column=1, padx=10, sticky=tk.N)

zoom_in_button = ttk.Button(mainframe, text="Zoom In", command=zoom_in)
zoom_in_button.grid(row=1, column=1, padx=10, sticky=tk.N)

zoom_out_button = ttk.Button(mainframe, text="Zoom Out", command=zoom_out)
zoom_out_button.grid(row=2, column=1, padx=10, sticky=tk.N)

canvas_widget.bind("<MouseWheel>", zoom)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
