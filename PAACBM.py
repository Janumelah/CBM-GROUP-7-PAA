import random
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import ttk

big_building_image = Image.open("big_building.png").convert("RGBA")
medium_building_image = Image.open("medium_building.png").convert("RGBA")
small_building_image = Image.open("small_building.png").convert("RGBA")
house_image = Image.open("house.png").convert("RGBA")
bush_image = Image.open("bush.png").convert("RGBA")
tree_image = Image.open("tree.webp").convert("RGBA")
cross_road = Image.open("+_road.png").convert("RGBA")
horizontal_road = Image.open("horizontal_road.png").convert("RGBA")
vertical_road = Image.open("vertical_road.png").convert("RGBA")
t_down = Image.open("troad_turn_down.png").convert("RGBA")
t_up = Image.open("troad_turn_up.png").convert("RGBA")
t_left = Image.open("troad_turn_left.png").convert("RGBA")
t_right = Image.open("troad_turn_right.png").convert("RGBA")
left_up = Image.open("down_turn_left.png").convert("RGBA")
left_down = Image.open("turn_left.png").convert("RGBA")
right_down = Image.open("turn_right.png").convert("RGBA")
right_up = Image.open("down_turn_right.png").convert("RGBA")

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
resized_tree = tree_image.resize((1 * map_scale, 1 * map_scale))
resized_cross_road = cross_road.resize((1 * map_scale, 1 * map_scale))
resized_horizontal_road = horizontal_road.resize((1 * map_scale, 1 * map_scale))
resized_vertical_road = vertical_road.resize((1 * map_scale, 1 * map_scale))
resized_t_down = t_down.resize((1 * map_scale, 1 * map_scale))
resized_t_up = t_up.resize((1 * map_scale, 1 * map_scale))
resized_t_right = t_right.resize((1 * map_scale, 1 * map_scale))
resized_t_left = t_left.resize((1 * map_scale, 1 * map_scale))
resized_left_up = left_up.resize((1 * map_scale, 1 * map_scale))
resized_left_down = left_down.resize((1 * map_scale, 1 * map_scale))
resized_right_up = right_up.resize((1 * map_scale, 1 * map_scale))
resized_right_down = right_down.resize((1 * map_scale, 1 * map_scale))

def generate_map(cell_size, map_scale):
    canvas = Image.new("RGB", (cell_size * map_scale, cell_size * map_scale), "lightgreen")
    draw = ImageDraw.Draw(canvas)
    size = cell_size
    road_cells = set()
    building_cells = set()
    bush_cells = set()
    tree_cells = set()
    vertice = []
    count = 0

    masks = {
        "horizontal": resized_horizontal_road.split()[3],
        "vertical": resized_vertical_road.split()[3],
        "cross": resized_cross_road.split()[3],
        "t_down": resized_t_down.split()[3],
        "t_up": resized_t_up.split()[3],
        "t_left": resized_t_left.split()[3],
        "t_right": resized_t_right.split()[3],
        "left_up": resized_left_up.split()[3],
        "left_down": resized_left_down.split()[3],
        "right_up": resized_right_up.split()[3],
        "right_down": resized_right_down.split()[3],
    }

    def is_intersection(cell):
        x, y = cell
        top_cell = (x, y - 1)
        bottom_cell = (x, y + 1)
        left_cell = (x - 1, y)
        right_cell = (x + 1, y)
        
        has_top = top_cell in road_cells
        has_bottom = bottom_cell in road_cells
        has_left = left_cell in road_cells
        has_right = right_cell in road_cells
        
        return has_top, has_bottom, has_left, has_right

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
                road_image = resized_horizontal_road if arah == "x" else resized_vertical_road
                mask = road_image.split()[3]
                if arah == "x":
                    for i in range(xDraw[0], xDraw[1], 10):
                        canvas.paste(road_image, (i, y), mask)
                else:
                    for i in range(yDraw[0], yDraw[1], 10):
                        canvas.paste(road_image, (x, i), mask)
                
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
        
        for cell in road_cells:
            has_top, has_bottom, has_left, has_right = is_intersection(cell)
            road_image = None
            mask = None
            if has_top and has_bottom and has_left and has_right:
                road_image = resized_cross_road
                mask = masks["cross"]
            elif has_top and has_bottom and has_left and not has_right:
                road_image = resized_t_left
                mask = masks["t_left"]
            elif has_top and has_bottom and has_right and not has_left:
                road_image = resized_t_right
                mask = masks["t_right"]
            elif has_bottom and has_right and has_left and not has_top:
                road_image = resized_t_down
                mask = masks["t_down"]
            elif has_top and has_right and has_left and not has_bottom:
                road_image = resized_t_up
                mask = masks["t_up"]
            elif has_left and has_top and not has_right and not has_bottom:
                road_image = resized_left_up
                mask = masks["left_up"]
            elif has_right and has_top and not has_left and not has_bottom:
                road_image = resized_right_up
                mask = masks["right_up"]
            elif has_right and has_bottom and not has_left and not has_top:
                road_image = resized_right_down
                mask = masks["right_down"]
            elif has_left and has_bottom and not has_right and not has_top:
                road_image = resized_left_down
                mask = masks["left_down"]
            if road_image:
                canvas.paste(road_image, (cell[0] * map_scale, cell[1] * map_scale), mask)

    def generate_buildings():
        def place_building(image, x, y, width, height):
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            mask = image.split()[3]
            canvas.paste(image, (x * map_scale, y * map_scale), mask)
            for i in range(width):
                for j in range(height):
                    building_cells.add((x + i, y + j))
                    
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

        def get_direction_to_road(x, y, width, height):
            adjacent_deltas = {
                'left': (-1, 0),
                'right': (1, 0),
                'up': (0, -1),
                'down': (0, 1)
            }
            for direction, (dx, dy) in adjacent_deltas.items():
                for i in range(width):
                    for j in range(height):
                        if (x + i + dx, y + j + dy) in road_cells:
                            return direction
            return None
        
        def rotate_building(image, direction):
            if direction == 'left':
                return image.rotate(-90, expand=True)
            elif direction == 'right':
                return image.rotate(90, expand=True)
            if direction == 'up':
                return image.rotate(180, expand=True)
            elif direction == 'down':
                return image
            return image
                
        def get_new_dimensions(width, height, direction):
            if direction == 'left' or direction == 'right':
                return height, width
            return width, height
        
        building_specs = [
            (resized_big_building, 10, 5, 90),
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
                        direction = get_direction_to_road(x, y, width, height)
                        rotated_image = rotate_building(image, direction)
                        new_width, new_height = get_new_dimensions(width, height, direction)
                        if can_place_building(x, y, new_width, new_height):
                            place_building(rotated_image, x, y, new_width, new_height)
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

    def generate_tree():
        for x in range(size):
            for y in range(size):
                if (x, y) not in road_cells and (x, y) not in building_cells:
                    if random.random() < 0.01:
                        canvas.paste(resized_tree, (x * map_scale, y * map_scale), resized_tree.split()[3])
                        for i in range(10):
                            for j in range(10):
                                tree_cells.add((x + i, y + j))

    generate_roads()
    generate_buildings()
    generate_bush()
    generate_tree()
    
    return canvas

def update_map():
    global canvas_image, canvas_tk, new_map
    new_map = generate_map(cell_size, map_scale)
    new_map.save("hasil_map.png")
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
root.title("IKN City Map")
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