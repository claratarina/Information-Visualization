# one point moves back and forth

import tkinter as tk
import pandas as pd

# Read data from CSV file
data = pd.read_csv('data1.csv', header=None)

# Extracting the first column as x values, the second column as y values, and the third as type_values

x_values = data.iloc[:, 0].tolist()
y_values = data.iloc[:, 1].tolist()
type_values = data.iloc[:, 2].tolist()

# Determine the range of x and y values
x_min, x_max = min(x_values), max(x_values)
y_min, y_max = min(y_values), max(y_values)

# Calculate canvas dimensions and origin based on the range of x and y values
padding = 50  # Padding around the canvas edges
canvas_width = 700
canvas_height = 700

orig_x = padding + abs(x_min) / (x_max - x_min) * (canvas_width - (2 * padding))
orig_y = canvas_height - (padding + abs(y_min) / (y_max - y_min) * (canvas_height - (2 * padding)))

# Create a Tkinter window
window = tk.Tk()
window.title("TNM111 - assignment 2")

# Create a frame for the legend and place it outside the canva 
legend_frame = tk.Frame(window)
legend_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Create a canvas to the left of the legend 
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white")
canvas.pack(side=tk.LEFT)

# Draw x- and y-axis with extended length
canvas.create_line(padding/2, orig_y, canvas_width - (padding/2), orig_y, fill="black", arrow=tk.BOTH)
canvas.create_line(orig_x, canvas_height - (padding/2), orig_x, padding/2, fill="black", arrow = tk.BOTH)


# Draw marks and values along x-axis
for x_tick in range(int(x_min), int(x_max) +1, int((x_max - x_min) / 6)):
    scaled_x = padding + (x_tick - x_min) / (x_max - x_min) * (canvas_width - 2 * padding)
    canvas.create_line(scaled_x, orig_y - 5, scaled_x, orig_y + 5, fill="black")
    canvas.create_text(scaled_x, orig_y + 10, text=str(x_tick), anchor=tk.N)

# Draw tick marks and tick values along y-axis
for y_tick in range(int(y_min), int(y_max), int((y_max - y_min) / 6)):
    scaled_y = canvas_height - (padding + (y_tick - y_min) / (y_max - y_min) * (canvas_height - 2 * padding))
    canvas.create_line(orig_x - 5, scaled_y, orig_x + 5, scaled_y, fill="black")
    canvas.create_text(orig_x - 10, scaled_y, text=str(y_tick), anchor=tk.E)


# Define color and shape for each type_values
category_properties = {'a': {'color': 'green', 'shape': 'circle'},
                       'b': {'color': 'blue', 'shape': 'square'},
                       'c': {'color': 'magenta', 'shape': 'triangle'},
                       'foo': {'color': 'orange', 'shape': 'diamond'},
                       'bar': {'color': 'purple', 'shape': 'circle'},  
                       'baz': {'color': 'red', 'shape': 'hexagon'}}

# Create a small legend 
legend = tk.Canvas(legend_frame, width=100, height=100, borderwidth=5, bg="white")
legend.pack()

# Draw legend text and shapes
legend.create_text(50, 20, text="Categories:", fill="black")
radius = 4

for i, category in enumerate(set(type_values)):
    y = 50 + 20 * i
    legend.create_text(35, y, text=category, anchor=tk.W)
    x = 20
    if category_properties[category]['shape'] == 'circle':
        legend.create_oval(x - radius, y - radius, x + radius, y + radius, fill=category_properties[category]['color'], outline="")
    elif category_properties[category]['shape'] == 'square':
        legend.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill=category_properties[category]['color'], outline="")
    elif category_properties[category]['shape'] == 'triangle':
        legend.create_polygon(x, y - radius, x - radius, y + radius, x + radius, y + radius, fill=category_properties[category]['color'], outline="")
    elif category_properties[category]['shape'] == 'diamond':
        legend.create_polygon(x, y - radius, x - radius, y, x, y + radius, x + radius, y, fill=category_properties[category]['color'], outline="")
    elif category_properties[category]['shape'] == 'pentagon':
        legend.create_polygon(x, y - radius, x - radius, y - radius // 2, x - radius // 2, y + radius, x + radius // 2, y + radius, x + radius, y - radius // 2, fill=category_properties[category]['color'], outline="")
    elif category_properties[category]['shape'] == 'hexagon':
        legend.create_polygon(x - radius // 2, y - radius, x - radius, y, x - radius // 2, y + radius, x + radius // 2, y + radius, x + radius, y, x + radius // 2, y - radius, fill=category_properties[category]['color'], outline="")





#============   LEFT CLICK    =============================================================================================================================================
selected_point = None
original_coords = {}
translated = False
latest_move = [0, 0]

def leftClick(event):
    global selected_point, original_coords, translated, latest_move
    
    # Get the coordinates of the clicked point
    x, y = event.x, event.y

    # Check if a point is clicked
    item = canvas.find_closest(x, y)
    if item:
        # Highlight the selected point
        selected_point = item
        canvas.itemconfig(selected_point, outline="yellow", width=5)
        
        if translated:
            # Move the point back to its original position
            canvas.move(selected_point, -latest_move[0], -latest_move[1])
            translated = False
            canvas.itemconfig(selected_point, outline="", width=1)

        else:
            # Save the original coordinates of the point
            original_coords[selected_point] = canvas.coords(selected_point)[:2]  # Store only x, y coordinates
            # Move the point to a new position
            latest_move = [orig_x - event.x, orig_y - event.y]
            canvas.move(selected_point, latest_move[0], latest_move[1])
            translated = True
            

        # Reset selected_point
        selected_point = None



    

# Bind left click event to leftClick function
canvas.bind('<Button-1>', leftClick)       

#============   PLOT THE DATA    =============================================================================================================================================
# Plot data points with different colors and shapes based on type_values
for x, y, type_val in zip(x_values, y_values, type_values):
    properties = category_properties.get(type_val, {'color': 'black', 'shape': 'circle'})
    color = properties['color']
    scaled_x = padding + (x - x_min) / (x_max - x_min) * (canvas_width - 2 * padding)
    scaled_y = canvas_height - (padding + (y - y_min) / (y_max - y_min) * (canvas_height - 2 * padding))

    if properties['shape'] == 'circle':
        canvas.create_oval(scaled_x - 3, scaled_y - 3, scaled_x + 3, scaled_y + 3, fill=color)
    elif properties['shape'] == 'square':
        canvas.create_rectangle(scaled_x - 3, scaled_y - 3, scaled_x + 3, scaled_y + 3, fill=color)
    elif properties['shape'] == 'triangle':
        canvas.create_polygon(scaled_x, scaled_y - 3, scaled_x - 3, scaled_y + 3, scaled_x + 3, scaled_y + 3, fill=color)
    elif properties['shape'] == 'diamond':
        canvas.create_polygon(scaled_x, scaled_y - 3, scaled_x - 3, scaled_y, scaled_x, scaled_y + 3, scaled_x + 3, scaled_y, fill=color)
    elif properties['shape'] == 'pentagon':
        canvas.create_polygon(scaled_x, scaled_y - 3, scaled_x - 2, scaled_y, scaled_x - 3, scaled_y + 3, scaled_x + 3, scaled_y + 3, scaled_x + 2, scaled_y, fill=color)
    elif properties['shape'] == 'hexagon':
        canvas.create_polygon(scaled_x - 2, scaled_y - 3, scaled_x - 3, scaled_y, scaled_x - 2, scaled_y + 3, scaled_x + 2, scaled_y + 3, scaled_x + 3, scaled_y, scaled_x + 2, scaled_y - 3, fill=color)





window.mainloop()  # Show the canvas window

