#==================================== Instructions =======================================
#Change the name on the read_csv file to change between the files data1.csv and data2.csv.
#Sometimes you need to clear you terminal before running the code or it wont work.
# When pressing on a dot, be carful to press exactly on the one you want to press,
# not next to it or the plot will go bananas. This is only when pressing the first time,
# the second click (the get the plot to go back to its original) you can press wherever.
#=========================================================================================

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

#find min and max values
x_min, x_max = min(x_values), max(x_values)
y_min, y_max = min(y_values), max(y_values)

#get the range of values
#range_x = round(max(abs(x_min), abs(x_max)))
#range_y = round(max(abs(y_min), abs(y_max)))

padding = 50
canvas_width = 700
canvas_height = 700

#calculating origo based on input data
orig_x = padding + abs(x_min) / (x_max - x_min) * (canvas_width - (2 * padding))
orig_y = canvas_height - (padding + abs(y_min) / (y_max - y_min) * (canvas_height - (2 * padding)))

#=====================================================================================================
class MyApp:
    def __init__(self, window, canvas_width=700, canvas_height=700, padding=50):
        self.window = window
        self.window.title("TNM111 - assignment 2")

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.padding = padding

        self.original_coords = {}
        self.original_colors = {}
        self.translated1 = False
        self.latest_move = [0, 0]

        self.canvas = tk.Canvas(window, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side=tk.LEFT)

        self.canvas.bind('<Button-1>', self.object_left_click_event)
        self.canvas.bind('<Button-2>', self.object_right_click_event)

        # Draw x- and y-axis with extended length
        self.canvas.create_line(padding / 2, orig_y, canvas_width - (padding / 2), orig_y, fill="black", arrow=tk.BOTH)
        self.canvas.create_line(orig_x, canvas_height - (padding / 2), orig_x, padding / 2, fill="black", arrow=tk.BOTH)

        # Draw marks and values along x-axis
        for x_tick in range(int(x_min), int(x_max) + 1, int((x_max - x_min) / 10)):
            scaled_x = padding + (x_tick - x_min) / (x_max - x_min) * (canvas_width - 2 * padding)
            self.canvas.create_line(scaled_x, orig_y - 5, scaled_x, orig_y + 5, fill="black")
            self.canvas.create_text(scaled_x, orig_y + 10, text=str(x_tick), anchor=tk.N)

        # Draw tick marks and tick values along y-axis
        for y_tick in range(int(y_min), int(y_max), int((y_max - y_min) / 10)):
            scaled_y = canvas_height - (padding + (y_tick - y_min) / (y_max - y_min) * (canvas_height - 2 * padding))
            self.canvas.create_line(orig_x - 5, scaled_y, orig_x + 5, scaled_y, fill="black")
            self.canvas.create_text(orig_x - 10, scaled_y, text=str(y_tick), anchor=tk.E)

        # Create legend
        self.create_legend()

    #================ LEGEND =====================================================================================
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
                               'baz': {'color': 'grey', 'shape': 'hexagon'}}

        legend_canvas.create_text(50, 20, text="Categories:", fill="black")
        radius = 4

        for i, category in enumerate(set(type_values)):
            y = 50 + 20 * i
            legend_canvas.create_text(35, y, text=category, anchor=tk.W)
            x = 20
            if category_properties[category]['shape'] == 'circle':
                legend_canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                          fill=category_properties[category]['color'], outline="black")
            elif category_properties[category]['shape'] == 'square':
                legend_canvas.create_rectangle(x - radius, y - radius, x + radius, y + radius,
                                               fill=category_properties[category]['color'], outline="black")
            elif category_properties[category]['shape'] == 'triangle':
                legend_canvas.create_polygon(x, y - radius, x - radius, y + radius, x + radius, y + radius,
                                             fill=category_properties[category]['color'], outline="black")
            elif category_properties[category]['shape'] == 'diamond':
                legend_canvas.create_polygon(x, y - radius, x - radius, y, x, y + radius, x + radius, y,
                                             fill=category_properties[category]['color'], outline="black")
            elif category_properties[category]['shape'] == 'pentagon':
                legend_canvas.create_polygon(x, y - radius, x - radius, y - radius // 2, x - radius // 2, y + radius,
                                             x + radius // 2, y + radius, x + radius, y - radius // 2,
                                             fill=category_properties[category]['color'], outline="black")
            elif category_properties[category]['shape'] == 'hexagon':
                legend_canvas.create_polygon(x - radius // 2, y - radius, x - radius, y, x - radius // 2, y + radius,
                                             x + radius // 2, y + radius, x + radius, y, x + radius // 2, y - radius,
                                             fill=category_properties[category]['color'], outline="black")

    #================ LEFT CLICK =====================================================================================
    def object_left_click_event(self, event):
        points = self.canvas.find_withtag("point")

        if self.translated1:
            self.translated1 = False

            # Move all points back to their original positions and restore original colors
            for i in range(len(points)):
                # Move the points back to their original positions
                original_coords = self.original_coords[i]
                self.canvas.move(points[i], -original_coords[0], -original_coords[1])

                # Restore the original color
                original_color = self.original_colors[i]
                self.canvas.itemconfig(points[i], fill=original_color)

        else:
            self.translated1 = True

            # Calculate the move required to bring the points to the origin
            move_x = orig_x - event.x
            move_y = orig_y - event.y
            self.latest_move = [move_x, move_y]

            # Store the original colors before moving the points
            for i in range(len(points)):
                # Store the original color in the dictionary if not already stored
                if i not in self.original_colors:
                    self.original_colors[i] = self.canvas.itemcget(points[i], "fill")

            # Loop through all points with the tag "point"
            for i in range(len(points)):
                # Store the original coordinates before moving the point
                self.original_coords[i] = (move_x, move_y)

                # Move the points to the origin
                self.canvas.move(points[i], move_x, move_y)

                # Change color based on the quadrant
                p = self.canvas.coords(points[i])
                if p[0] > orig_x and p[1] > orig_y:
                    self.canvas.itemconfig(points[i], fill="red")
                elif p[0] > orig_x and p[1] < orig_y:
                    self.canvas.itemconfig(points[i], fill="blue")
                elif p[0] < orig_x and p[1] < orig_y:
                    self.canvas.itemconfig(points[i], fill="black")
                elif p[0] < orig_x and p[1] > orig_y:
                    self.canvas.itemconfig(points[i], fill="orange")

                # Change the color of the clicked point to yellow (works for data2 but not data1)
                if i == event.widget.find_withtag("current")[0]:
                    self.canvas.itemconfig(i, fill="yellow")

    
    #================ RIGHT CLICK =====================================================================================
    def object_right_click_event(self, event):
        points = self.canvas.find_withtag("point")

        # Calculate the distance between the right-clicked point and all other points
        clicked_x, clicked_y = event.x, event.y
        distances = [(abs(clicked_x - self.canvas.coords(point)[0]), abs(clicked_y - self.canvas.coords(point)[1]),
                    point) for point in points]

        # Sort points based on distance from the right-clicked point
        distances.sort(key=lambda d: (d[0] ** 2 + d[1] ** 2))

        # Exclude the clicked point from the list of highlighted points
        highlighted_points = [(point, self.canvas.itemcget(point, "fill")) for point in points if
                            self.canvas.itemcget(point, "fill") == "yellow" and point != event.widget.find_withtag("current")[0]]

        # If there are highlighted points, un-highlight them
        if highlighted_points:
            for point_id, prev_color in highlighted_points:
                self.canvas.itemconfig(point_id, fill=self.original_coords.get(point_id))  # Restore previous color
        else:
            # Highlight the nearest 5 points (excluding the clicked point)
            highlighted_points = []
            for i in range(1, min(6, len(distances))):
                point = distances[i][2]
                prev_color = self.canvas.itemcget(point, "fill")  # Store previous color
                self.original_coords[point] = prev_color  # Store original color
                self.canvas.itemconfig(point, fill='yellow')
                highlighted_points.append((point, prev_color))

#================ PLOT EVERYTHING =====================================================================================

# Create a Tkinter window
window = tk.Tk()

app = MyApp(window)

# Plot data points with different colors and shapes based on type_values
for point in points:
    scaled_x = padding + (point.x - x_min) / (x_max - x_min) * (canvas_width - 2 * padding)
    scaled_y = canvas_height - (padding + (point.y - y_min) / (y_max - y_min) * (canvas_height - 2 * padding))

    if point.type_val == 'a':
        app.canvas.create_oval(scaled_x - 3, scaled_y - 3, scaled_x + 3, scaled_y + 3, fill="green", outline="black",
                               tags=("point", "a"))
    elif point.type_val == 'b':
        app.canvas.create_rectangle(scaled_x - 3, scaled_y - 3, scaled_x + 3, scaled_y + 3, fill="blue", outline="black",
                                    tags=("point", "b"))
    elif point.type_val == 'c':
        app.canvas.create_polygon(scaled_x, scaled_y - 3, scaled_x - 3, scaled_y + 3, scaled_x + 3, scaled_y + 3,
                                  fill="magenta", outline="black", tags=("point", "c"))
    elif point.type_val == 'foo':
        app.canvas.create_polygon(scaled_x, scaled_y - 3, scaled_x - 3, scaled_y, scaled_x, scaled_y + 3,
                                  scaled_x + 3, scaled_y, fill="orange",outline="black", tags=("point", "foo"))
    elif point.type_val == 'bar':
        app.canvas.create_oval(scaled_x - 3, scaled_y - 3, scaled_x + 3, scaled_y + 3, fill="purple", outline="black",
                               tags=("point", "bar"))
    elif point.type_val == 'baz':
        app.canvas.create_polygon(scaled_x - 2, scaled_y - 3, scaled_x - 3, scaled_y, scaled_x - 2, scaled_y + 3,
                                  scaled_x + 2, scaled_y + 3, scaled_x + 3, scaled_y, scaled_x + 2, scaled_y - 3,
                                  fill="grey", outline="black", tags=("point", "baz"))

window.mainloop()  # Show the canvas window
