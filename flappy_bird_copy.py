import tkinter as tk
from time import sleep
from random import randint





class Background:
    
    def create_grid(self):

        for i in range(0, window_width, 100):
            c.create_line([(i, 0), (i, window_height)], tag='grid_line')
    
        for i in range(0, window_height, 100):
            c.create_line([(0, i), (window_width, i)], tag='grid_line')


class Flappy: 

    def create(self):
        
        global body, distance_left, flappy_width
        body = c.create_rectangle(distance_left, (window_height-flappy_height)/2, distance_left+flappy_width, (window_height+flappy_height)/2, tags="flappy", fill="black")

    def key_move(self):
        
        global flappy_move, jump_strength, jump_cooldown
        if (flappy_move > jump_cooldown) == False:
            flappy_move = jump_strength

        
            
class Pipes:

    def create(self):
 
            global window_width, window_height, open_height, min_pipe_length,  existing_pipes,min_pipe_distance, max_pipe_distance
            
            for i in range(1, len(existing_pipes)+2):
                if "p"+str(i) not in existing_pipes:
                    name_pipe = "p"+str(i)
                    pass
            rand_length = randint(min_pipe_length, window_height-min_pipe_length)
            c.create_rectangle(window_width+0,0,window_width+pipe_width,rand_length-open_height/2, tags=name_pipe, fill="black")
            c.create_rectangle(window_width+0,rand_length+(open_height/2),window_width+pipe_width,window_height, tags=name_pipe,fill="black")
            existing_pipes.append(name_pipe)
            
           
            
            
    def move_check_pipe(self): 
        global distance_left, score, existing_pipes, pipe_speed, open_height,death, body, death, edge_kill_space, window_height , pipe_kill_space, flappy_move, gravity      
        body_coords = c.coords(body)
        for pair in existing_pipes:
            pair_coords = c.coords(pair)
            #kill flappy when tuching pipe
            if (pair_coords[0] - body_coords[2]) < 0+pipe_kill_space and (pair_coords[2] - body_coords[0]) > 0-pipe_kill_space:
                potential = 1
                if (pair_coords[3] - body_coords[1]) > 0-pipe_kill_space or ((pair_coords[3] + open_height) -body_coords[3]) < 0+pipe_kill_space:
                    death = 1
            #move pipes
            c.move(pair, -pipe_speed, 0)  
        #delete pipes at end
        try:
            oldest_pipe = existing_pipes[0]
            if c.coords(oldest_pipe)[2] < 0:
                c.delete(oldest_pipe)
                existing_pipes.remove(oldest_pipe)
            #score showing
            if distance_left > c.coords(oldest_pipe)[2] > distance_left - pipe_speed -1:
                score += 1
                c.delete("score")
                score_showing = c.create_text(250, 50, text=score, tags="score", fill="black", font=("New Courier", 30))
        except: 
            pass
        #kill flappy when tuching edge
        if body_coords[1] < edge_kill_space:

            death = 1

        elif body_coords[3] > (window_height-edge_kill_space):
            
            death = 1
            
        #gravity on flappy and move
        flappy_move -= gravity
        c.move("flappy", 0, -flappy_move)


                        
    

root = tk.Tk()
root.title("flap.py")


#settings -----------------------------------------------------------------

window_width = 1000 # width of window
window_height = 600 # height of window
update_time = 0.04 # in which intervals the canvas updates

gravity = 1 # how fast flappy is accelerating downwards
jump_height = 50 # how high flappy jumps if you press key
jump_strength = 0.5*((gravity**0.5)*((gravity+8*jump_height)**0.5)+gravity) # don't change
jump_cooldown = -(0.3 * gravity / update_time - jump_strength) # just change number at the begin (in sec)

edge_kill_space = 5 # if flappy's distance to edge is lower than this, it will die
jump_key = "space" # which key you can use to jump
pipe_kill_space = 5 # if flappy's distance to any pipe is lower than this, it will die

distance_left = 85 # distance between flappy and left edge
flappy_width = 30 # width of flappy
flappy_height = 30 # height of flappy

pipe_width = 100 # width of pipes
open_height = 150 # height of opening in pipes, where flappy can jump thruogh without dying
min_pipe_length = 100 + open_height/2 # minimal pipe height
pipe_speed = 10 # pipe speed
min_pipe_distance = int((200 + pipe_width) / pipe_speed) # minimal distance between two pipes
max_pipe_distance = int((600 + pipe_width) / pipe_speed) # maximal distance between two pipes

#--------------------------------------------------------------------------------------



c = tk.Canvas(root, height=window_height, width=window_width)
c.pack()
root.bind("<{}>".format(jump_key), Flappy.key_move)

    
while True:
    #setup until sleep
    death = 0
    flappy_move = 0
    existing_pipes = []
    creating_counter = 0
    score = 0
    rand_distance = randint(min_pipe_distance, max_pipe_distance)
    c.delete("all")
    flap_object = Flappy()
    flap_object.create()
    pipes_object = Pipes()
    bg_object = Background()
    bg_object.create_grid()
    score_showing = c.create_text(250, 50, text=score, tags="score", fill="black", font=("New Courier", 30))
    root.update()
    sleep(3)    
    while death == 0:
        if creating_counter == rand_distance:
            pipes_object.create()
            rand_distance = randint(min_pipe_distance, max_pipe_distance)
            creating_counter = 0
        else: 
            creating_counter += 1
        pipes_object.move_check_pipe()
        root.update() 
        sleep(update_time)
        
    
root.mainloop()    



        
