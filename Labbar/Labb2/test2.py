
#here the second function (highliting the nearest 5 points) works but not the first.


import tkinter as tk
import pandas as pd

class Point:
    def __init__(self, x, y, type_val):
        self.x = x
        self.y = y
        self.type_val = type_val

# Read data from CSV file
data = pd.read_csv('data1.csv', header=None)

# Create a list of Point instances
points = [Point(x, y, type_val) for x, y, type_val in zip(data.iloc[:, 0], data.iloc[:, 1], data.iloc[:, 2])]

# Determine the range of x and y values
x_values = data.iloc[:, 0].tolist()
y_values = data.iloc[:, 1].tolist()
type_values = data.iloc[:, 2].tolist()

x_min, x_max = min(x_values), max(x_values)
y_min, y_max = min(y_values), max(y_values)

range_x = round(max(abs(x_min), abs(x_max)))
range_y = round(max(abs(y_min), abs(y_max)))

padding = 50  
canvas_width = 700
canvas_height = 700

orig_x = padding + abs(x_min) / (x_max - x_min) * (canvas_width - (2 * padding))
orig_y = canvas_height - (padding + abs(y_min) / (y_max - y_min) * (canvas_height - (2 * padding)))

class MyApp:
    def __init__(self, window, canvas_width=700, canvas_height=700, padding=50):
        self.window = window
        self.window.title("TNM111 - assignment 2")
        
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.padding = padding
        
        self.original_coords = {}
        self.translated = False
        self.latest_move = [0, 0]
        
        self.canvas = tk.Canvas(window, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side=tk.LEFT)

        self.canvas.bind('<Button-1>', self.object_left_click_event)
        self.canvas.bind('<Button-2>', self.object_right_click_event)  # Bind right-click event

        # Draw x- and y-axis with extended length
        self.canvas.create_line(padding/2, orig_y, canvas_width - (padding/2), orig_y, fill="black", arrow=tk.BOTH)
        self.canvas.create_line(orig_x, canvas_height - (padding/2), orig_x, padding/2, fill="black", arrow=tk.BOTH)

        # Draw marks and values along x-axis
        for x_tick in range(int(x_min), int(x_max) + 1, int((x_max - x_min) / 6)):
            scaled_x = padding + (x_tick - x_min) / (x_max - x_min) * (canvas_width - 2 * padding)
            self.canvas.create_line(scaled_x, orig_y - 5, scaled_x, orig_y + 5, fill="black")
            self.canvas.create_text(scaled_x, orig_y + 10, text=str(x_tick), anchor=tk.N)

        # Draw tick marks and tick values along y-axis
        for y_tick in range(int(y_min), int(y_max), int((y_max - y_min) / 6)):
            scaled_y = canvas_height - (padding + (y_tick - y_min) / (y_max - y_min) * (canvas_height - 2 * padding))
            self.canvas.create_line(orig_x - 5, scaled_y, orig_x + 5, scaled_y, fill="black")
            self.canvas.create_text(orig_x - 10, scaled_y, text=str(y_tick), anchor=tk.E)

        # Create legend
        self.create_legend()
        
        # Save original coordinates for all points
        for i, point in enumerate(points):
            scaled_x = padding + (point.x - x_min) / (x_max - x_min) * (canvas_width - 2 * padding)
            scaled_y = canvas_height - (padding + (point.y - y_min) / (y_max - y_min) * (canvas_height - 2 * padding))
            self.original_coords[i] = (scaled_x, scaled_y)

    def create_legend(self):
        legend_frame = tk.Frame(self.window)
        legend_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        legend_canvas = tk.Canvas(legend_frame, width=100, height=100, bg="white")
        legend_canvas.pack()

        category_properties = {'a': {'color': 'green', 'shape': 'circle'},
                               'b': {'color': 'blue', 'shape': 'square'},
                               'c': {'color': 'magenta', 'shape': 'triangle'},
                               'foo': {'color': 'orange', 'shape': 'diamond'},
                               'bar': {'color': 'purple', 'shape': 'circle'},  
                               'baz': {'color': 'red', 'shape': 'hexagon'}}

        legend_canvas.create_text(50, 20, text="Categories:", fill="black")
        radius = 4

        for i, category in enumerate(set(type_values)):
            y = 50 + 20 * i
            legend_canvas.create_text(35, y, text=category, anchor=tk.W)
            x = 20
            if category_properties[category]['shape'] == 'circle':
                legend_canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=category_properties[category]['color'], outline="")
            elif category_properties[category]['shape'] == 'square':
                legend_canvas.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill=category_properties[category]['color'], outline="")
            elif category_properties[category]['shape'] == 'triangle':
                legend_canvas.create_polygon(x, y - radius, x - radius, y + radius, x + radius, y + radius, fill=category_properties[category]['color'], outline="")
            elif category_properties[category]['shape'] == 'diamond':
                legend_canvas.create_polygon(x, y - radius, x - radius, y, x, y + radius, x + radius, y, fill=category_properties[category]['color'], outline="")
            elif category_properties[category]['shape'] == 'pentagon':
                legend_canvas.create_polygon(x, y - radius, x - radius, y - radius // 2, x - radius // 2, y + radius, x + radius // 2, y + radius, x + radius, y - radius // 2, fill=category_properties[category]['color'], outline="")
            elif category_properties[category]['shape'] == 'hexagon':
                legend_canvas.create_polygon(x - radius // 2, y - radius, x - radius, y, x - radius // 2, y + radius, x + radius // 2, y + radius, x + radius, y, x + radius // 2, y - radius, fill=category_properties[category]['color'], outline="")

    def object_left_click_event(self, event):
        points = self.canvas.find_withtag("point")
        if not self.translated:
            # Move all points back to their original positions
            for point_id in points:
                try:
                    original_x, original_y = self.original_coords[int(point_id)]  # Convert point_id to int
                except KeyError:
                    continue  # Skip if point_id not found
                current_x, current_y = self.canvas.coords(point_id)
                move_x = original_x - current_x
                move_y = original_y - current_y
                self.canvas.move(point_id, move_x, move_y)
                color_tag = self.canvas.gettags(point_id)[1]
                self.canvas.itemconfig(point_id, fill=color_tag)
            
            self.translated = True
        else:
            # Move points to the translated positions
            for point_id in points:
                move_x, move_y = self.latest_move
                self.canvas.move(point_id, move_x, move_y)
                
                p = self.canvas.coords(point_id)
                if p[0] > orig_x and p[1] > orig_y:
                    self.canvas.itemconfig(point_id, fill="red")
                elif p[0] > orig_x and p[1] < orig_y:
                    self.canvas.itemconfig(point_id, fill="blue")                
                elif p[0] < orig_x and p[1] < orig_y:
                    self.canvas.itemconfig(point_id, fill="black")
                elif p[0] < orig_x and p[1] > orig_y:
                    self.canvas.itemconfig(point_id, fill="orange")
            
            self.translated = False

            current = event.widget.find_withtag("current")[0]
            self.canvas.itemconfig(current, fill='yellow')


    def object_right_click_event(self, event):
        points = self.canvas.find_withtag("point")

        # Calculate the distance between the right-clicked point and all other points
        clicked_x, clicked_y = event.x, event.y
        distances = [(abs(clicked_x - self.canvas.coords(point)[0]), abs(clicked_y - self.canvas.coords(point)[1]), point) for point in points]

        # Sort points based on distance from the right-clicked point
        distances.sort(key=lambda d: (d[0] ** 2 + d[1] ** 2))

        # Check if points are already highlighted
        highlighted_points = [point for point in points if self.canvas.itemcget(point, "fill") == "yellow"]

        # If there are highlighted points, un-highlight them
        if highlighted_points:
            for point_id in highlighted_points:
                self.canvas.itemconfig(point_id, fill='color')  # Change fill color back to black
        else:
            # Highlight the nearest 5 points
            for i in range(min(5, len(distances))):
                point = distances[i][2]
                self.canvas.itemconfig(point, fill='yellow')



# Create a Tkinter window
window = tk.Tk()

app = MyApp(window)

# Plot data points with different colors and shapes based on type_values
for point in points:
    scaled_x = padding + (point.x - x_min) / (x_max - x_min) * (canvas_width - 2 * padding)
    scaled_y = canvas_height - (padding + (point.y - y_min) / (y_max - y_min) * (canvas_height - 2 * padding))
    if point.type_val == 'a':
        app.canvas.create_oval(scaled_x - 3, scaled_y - 3, scaled_x + 3, scaled_y + 3, fill="green", tags=("point", "a"))
    elif point.type_val == 'b':
        app.canvas.create_rectangle(scaled_x - 3, scaled_y - 3, scaled_x + 3, scaled_y + 3, fill="blue", tags=("point", "b"))
    elif point.type_val == 'c':
        app.canvas.create_polygon(scaled_x, scaled_y - 3, scaled_x - 3, scaled_y + 3, scaled_x + 3, scaled_y + 3, fill="magenta", tags=("point", "c"))
    elif point.type_val == 'foo':
        app.canvas.create_polygon(scaled_x, scaled_y - 3, scaled_x - 3, scaled_y, scaled_x, scaled_y + 3, scaled_x + 3, scaled_y, fill="orange", tags=("point", "foo"))
    elif point.type_val == 'bar':
        app.canvas.create_oval(scaled_x - 3, scaled_y - 3, scaled_x + 3, scaled_y + 3, fill="purple", tags=("point", "bar"))
    elif point.type_val == 'baz':
        app.canvas.create_polygon(scaled_x - 2, scaled_y - 3, scaled_x - 3, scaled_y, scaled_x - 2, scaled_y + 3, scaled_x + 2, scaled_y + 3, scaled_x + 3, scaled_y, scaled_x + 2, scaled_y - 3, fill="red", tags=("point", "baz"))

window.mainloop()  # Show the canvas window
