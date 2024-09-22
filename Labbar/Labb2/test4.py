
# clale106, salga107
# TNM111 Assignment 2 - part 3
import tkinter as tk
import math

# starting color for the a,b,c / bar,baz,foo categorys
COLORS = ["green", "red", "blue"]

#=============================== DOT ===================================
# class for creating the dots with coordinates and category
class Dot:
    def __init__(self, x, y, category):
        self.x = x
        self.y = y
        self.category = category

    def __str__(self):
        return f'{self.x}i{self.y:+}j'

#=============================== PLOTTER ===================================
# class for plotting and interacting with the scatter plot
class Plotter:
    def __init__(self, data):
        self.data = data
        self.pressed1 = False
        self.pressed2 = False
        self.latest_move = [0, 0]
        self.closest_dots = []

    def get_category(self, dot):
        return dot.category

    def draw_dots(self, x_range, y_range, categories):
        i = 0
        for dot in self.data:
            i += 1

            #Updates coordinates of the current dot object within the plot
            dot.x = 350 + dot.x * (300 / x_range)
            dot.y = 350 - dot.y * (300 / y_range)

            # determine shape etc for each category
            index = categories.index(dot.category)
            if index == 0:
                shape = "*"
            elif index == 1:
                shape = "+"
            else:
                shape = "o"

            element = self.canvas.create_text(dot.x, dot.y, text=shape, fill=COLORS[index], font=("Arial", 28),
                                              tags=["dot", f"shape{i}", f"{COLORS[index]}"])

            # Button 1 for left click, Button 2 for right click (Button 2  might be Button 3 for different soft/hardwere)
            self.canvas.tag_bind(element, '<Button-1>', self.left_click_event)
            self.canvas.tag_bind(element, '<Button-2>', self.right_click_event)




    #Create the scatterplot
    def create_scatter_plot(self):
        window = tk.Tk()
        window.title("TNM111, Assignment 2") #title
        self.canvas = tk.Canvas(window, width=700, height=700, bg="white")  #Width and height of window
        self.canvas.pack()

        


        #draw the axis
        self.canvas.create_line(50, 350, 650, 350, fill="black", width=2, arrow=tk.BOTH) #x-axis
        self.canvas.create_line(350, 650, 350, 50, fill="black", width=2, arrow=tk.BOTH) #y-axis


        # Finding the minimum and maximum x- and y-values
        x_min = min(self.data, key=lambda dot: dot.x)
        y_min = min(self.data, key=lambda dot: dot.y)
        x_max = max(self.data, key=lambda dot: dot.x)
        y_max = max(self.data, key=lambda dot: dot.y)

        #Determine the range of x and y based on max and min
        x_range = round(max(abs(x_min.x), abs(x_max.x)))
        y_range = round(max(abs(y_min.y), abs(y_max.y)))

        #Create marks every 6 steps on the x-axis
        for i in range(-x_range, x_range + 1, 6):
            x = round(350 + i * (300 / x_range))
            self.canvas.create_line(x, 340, x, 360, width=1)
            self.canvas.create_text(round(x), 375, text=str(i))

        #Create marks every 6 steps on y-axis
        for i in range(-y_range, y_range + 1, 6):
            y = round(350 - i * (300 / y_range))
            self.canvas.create_line(340, y, 360, y, width=1)
            self.canvas.create_text(375, y, text=str(i))

        # list catergorys
        categories = set(map(self.get_category, self.data))
        categories = list(categories)

        #Call function draw dot with arguments
        self.draw_dots(x_range, y_range, categories)

        for i in range(len(categories)):
            # Determine which shape is for each category 
            index = categories.index(categories[i])
            if index == 0:
                shape = "*"
            elif index == 1:
                shape = "+"
            else:
                shape = "o"
            
            tk.Label(window, text=f"{shape} : {categories[i]}").place(relx=0.95, rely=0.1 + 0.05 * i, anchor="ne")


        window.mainloop()


    # The events for the left click
    def left_click_event(self, event):
        #retrive all dots
        dots = self.canvas.find_withtag("dot")

    # Check if the dot have been clicked for the first or second time
        if self.pressed1:
            self.pressed1 = False # felse if second click

            #If dots were pressed, moves each dot back to original position
            for i in dots:
                self.canvas.move(i, -self.latest_move[0], -self.latest_move[1]) 
                color_tag = self.canvas.gettags(i)[2]
                self.canvas.itemconfig(i, fill=color_tag) #change back color
        else:
            self.pressed1 = True
            move_x = 350 - event.x #x-coordinate difference between the click and origin
            move_y = 350 - event.y #y-coordinate difference between the click and origin
            self.latest_move = [move_x, move_y] #Store differences as latest move

            for i in range(len(dots)):
                self.canvas.move(dots[i], move_x, move_y) #Moves each dot aswell

                p = self.canvas.coords(dots[i]) #new coordinates

                # changes the dots color depending on its position and the origin
                if p[0] > 350 and p[1] > 350:
                    self.canvas.itemconfig(dots[i], fill="purple")
                elif p[0] > 350 and p[1] < 350:
                    self.canvas.itemconfig(dots[i], fill="blue")
                elif p[0] < 350 and p[1] < 350:
                    self.canvas.itemconfig(dots[i], fill="pink")
                elif p[0] < 350 and p[1] > 350:
                    self.canvas.itemconfig(dots[i], fill="yellow")

            current = event.widget.find_withtag("current")[0] #retrive clicked dot
            self.canvas.itemconfig(current, fill='red') #change color of clicked dot


    #Events for right click
    def right_click_event(self, event):
        
        # Check if the dot have been clicked for the first or second time
        if self.pressed2:
            self.pressed2 = False # set pressed to false

            #find the previousley clicked and change back to original color
            for d in self.closest_dots:
                color_tag = self.canvas.gettags(d)[2]
                self.canvas.itemconfig(d, fill=color_tag)        
        else:   
            self.pressed2 = True #set pressed to true
            dots = self.canvas.find_withtag("dot")

            current = event.widget.find_withtag("current")[0] #find clicked dot
            active = self.canvas.coords(current) #get coordinates

            # Calculate distances between clicked dot and all other dots (not the clicked onde)
            distances_and_dots = [
                (math.sqrt((active[0] - co[0]) ** 2 + (active[1] - co[1]) ** 2), dot)
                for dot in dots
                if (co := self.canvas.coords(dot)) and dot != current #list dots and distance with tuples
            ]

            closest_dots = [dot for _, dot in sorted(distances_and_dots)[:5]] #sort list and select top 5

            #color all selected dots red
            for d in closest_dots:
                self.canvas.itemconfig(d, fill='red')   

            self.closest_dots = closest_dots #store dots for de-selection


#=============================== MAIN ===================================
#load the data 
def load_data(file_path): 
    data = []
    with open(file_path, "r") as file:
        for line in file:
            values = line.strip().split(",")
            data.append(Dot(float(values[0]), float(values[1]), values[2]))
    return data

# Runt the code and its functions
if __name__ == "__main__":
    data = load_data("data1.csv")
    scatter_plotter = Plotter(data)
    scatter_plotter.create_scatter_plot()
