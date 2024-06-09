import random
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import ttk

big_building_image = Image.open("paatest/big_building.png").convert("RGBA")
medium_building_image = Image.open("paatest/medium_building.png").convert("RGBA")
small_building_image = Image.open("paatest/small_building.png").convert("RGBA")
house_image = Image.open("paatest/house.png").convert("RGBA")
bush_image = Image.open("paatest/bush.png").convert("RGBA")

INITIAL_WIDTH = 500
INITIAL_HEIGHT = 400
viewport_x = 0
viewport_y = 0
viewport_width = 700
viewport_height = 600
zoom_factor = 1.0

cell_size = 150
map_scale = 10

# Resize building images only once
resized_big_building = big_building_image.resize((10 * map_scale, 5 * map_scale))
resized_medium_building = medium_building_image.resize((5 * map_scale, 3 * map_scale))
resized_small_building = small_building_image.resize((2 * map_scale, 2 * map_scale))
resized_house = house_image.resize((1 * map_scale, 2 * map_scale))
resized_bush = bush_image.resize((1 * map_scale, 1 * map_scale))

def generate_map(cell_size, map_scale):
    canvas = Image.new("RGB", (cell_size * map_scale, cell_size * map_scale), "green")
    draw = ImageDraw.Draw(canvas)
    size = cell_size
    road_cells = set()
    building_cells = set()
    bush_cells = set()
    vertice = []
    count = 0

    def generate_roads():
        nonlocal count
        x, y = 0, 100
        directionsY = [(0, 150), (0, -150)]
        directionsX = [(150, 0), (-150, 0)]
        arah = "x"
        for _ in range(2000):
            count += 1
            if 0 <= x < 1500 and 0 <= y < 1500:
                vertice.append((x, y))
                road_cells.add((x // map_scale, y // map_scale))
                current_direction = random.choice(directionsX if arah == "x" else directionsY)
                xDraw = sorted([x, x + current_direction[0]])
                yDraw = sorted([y, y + current_direction[1]])
                draw.rectangle(((xDraw[0], yDraw[0]), (xDraw[1] + 10, yDraw[1] + 10)), "gray")
                for i in range(xDraw[0], xDraw[1] + 1, map_scale):
                    for j in range(yDraw[0], yDraw[1] + 1, map_scale):
                        road_cells.add((i // map_scale, j // map_scale))
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

    def place_building(image, x, y, width, height):
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        mask = image.split()[3]
        canvas.paste(image, (x * map_scale, y * map_scale), mask)
        for i in range(width):
            for j in range(height):
                building_cells.add((x + i, y + j))

    def generate_buildings():
        def can_place_building(x, y, width, height):
            for i in range(width):
                for j in range(height):
                    if (x + i, y + j) in road_cells or (x + i, y + j) in building_cells:
                        return False
            return True

        def is_adjacent_to_road(x, y, width, height):
            adjacent_deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for i in range(width):
                for j in range(height):
                    for dx, dy in adjacent_deltas:
                        if (x + i + dx, y + j + dy) in road_cells:
                            return True
            return False

        building_specs = [
            (resized_big_building, 10, 5, 80),
            (resized_medium_building, 5, 3, 100),
            (resized_small_building, 2, 2, 100),
            (resized_house, 1, 2, 100)
        ]

        for image, width, height, num in building_specs:
            for _ in range(num):
                placed = False
                attempts = 0
                while not placed and attempts < 250:
                    attempts += 1
                    x = random.randint(0, size - width)
                    y = random.randint(0, size - height)
                    if can_place_building(x, y, width, height) and is_adjacent_to_road(x, y, width, height):
                        place_building(image, x, y, width, height)
                        placed = True

    def generate_bush():
        for x in range(size):
            for y in range(size):
                if (x, y) not in road_cells and (x, y) not in building_cells:
                    if random.random() < 0.1:
                        canvas.paste(resized_bush, (x * map_scale, y * map_scale), resized_bush.split()[3])
                        for i in range(10):
                            for j in range(10):
                                bush_cells.add((x + i, y + j))

    generate_roads()
    generate_buildings()
    generate_bush()
    
    return canvas

def update_map():
    global canvas_image, canvas_tk, new_map
    new_map = generate_map(cell_size, map_scale)
    cropped_map = new_map.crop((viewport_x, viewport_y, viewport_x + viewport_width, viewport_y + viewport_height))
    resized_map = cropped_map.resize((INITIAL_WIDTH, INITIAL_HEIGHT))
    canvas_tk = ImageTk.PhotoImage(resized_map)
    canvas_widget.create_image(0, 0, anchor='nw', image=canvas_tk)
    canvas_widget.image = canvas_tk
    canvas_widget.config(scrollregion=(0, 0, new_map.width, new_map.height))

def update():
    global new_map, canvas_tk
    cropped_map = new_map.crop((int(viewport_x * zoom_factor), int(viewport_y * zoom_factor), int(viewport_x * zoom_factor + viewport_width * zoom_factor), int(viewport_y * zoom_factor + viewport_height * zoom_factor)))
    resized_map = cropped_map.resize((INITIAL_WIDTH, INITIAL_HEIGHT))
    canvas_tk = ImageTk.PhotoImage(resized_map)
    canvas_widget.create_image(0, 0, anchor='nw', image=canvas_tk)
    canvas_widget.image = canvas_tk
    canvas_widget.config(scrollregion=(0, 0, new_map.width * zoom_factor, new_map.height * zoom_factor))

def zoom_out():
    global zoom_factor
    if zoom_factor < 5.0:
        zoom_factor += 0.1
        update()

def zoom_in():
    global zoom_factor
    if zoom_factor > 0.5:
        zoom_factor -= 0.1
        update()

def scroll(event):
    global viewport_x, viewport_y
    if event.delta > 0:
        viewport_y -= 20
    else:
        viewport_y += 20
    update()

# Tkinter UI
root = tk.Tk()
root.title("City Map Generator")
root.configure(bg="lightpink")

mainframe = ttk.Frame(root, padding="10 10 10 10", style="My.TFrame")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

canvas_frame = ttk.Frame(mainframe, style="My.TFrame")
canvas_frame.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.N + tk.S))

canvas_widget = tk.Canvas(canvas_frame, width=INITIAL_WIDTH, height=INITIAL_HEIGHT, bg="white")
canvas_widget.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.N + tk.S))

hbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas_widget.xview, bg="lightgrey")
hbar.grid(row=1, column=0, sticky=(tk.W + tk.E))
vbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas_widget.yview, bg="lightgrey")
vbar.grid(row=0, column=1, sticky=(tk.N + tk.S))

canvas_widget.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

button_frame = ttk.Frame(mainframe, style="My.TFrame")
button_frame.grid(row=0, column=1, padx=10, sticky=(tk.N))

generate_button = ttk.Button(button_frame, text="Generate Map", command=update_map, style="My.TButton")
generate_button.grid(row=0, column=0, pady=(0, 10))

zoom_in_button = ttk.Button(button_frame, text="Zoom In", command=zoom_in, style="My.TButton")
zoom_in_button.grid(row=1, column=0, pady=(0, 10))

zoom_out_button = ttk.Button(button_frame, text="Zoom Out", command=zoom_out, style="My.TButton")
zoom_out_button.grid(row=2, column=0, pady=(0, 10))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
canvas_frame.columnconfigure(0, weight=1)
canvas_frame.rowconfigure(0, weight=1)

canvas_widget.bind("<MouseWheel>", scroll)

style = ttk.Style()
style.configure("My.TFrame", background="lightpink")
style.configure("My.TButton", background="lightgrey", foreground="black")

update_map()
root.mainloop()
