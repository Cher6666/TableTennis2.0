#Importing the modules needed
import simplegui
import random

# initialize globals 

WIDTH = 600 #canvas width
HEIGHT = 400  #canas height     
BALL_RADIUS = 20 #ball radius
PAD_WIDTH = 8 #width of the paddle
PAD_HEIGHT = 80 #height of the paddle
SCORE1_POS = [WIDTH/2 - 100,80] #defining pos where score1 is drawn
SCORE2_POS = [WIDTH/2 + 100,80] #defining pos where score2 is drawn
#initial positions of two paddles
paddle1_pos, paddle2_pos = (HEIGHT-PAD_HEIGHT)/2, (HEIGHT-PAD_HEIGHT)/2


# helper function to set the initial ball and direction properties
def spawn_ball(direction):
    global ball_pos, ball_vel,ball_dir
    
    #selects a random ball velocity to start the game with
    ball_vel= [random.randrange(2,4),random.randrange(1,3)]
    
    #positioning ball at the center of the canvas
    ball_pos = [WIDTH/2,HEIGHT/2]
    
    #if the parameter passed is True, the game starts with 
    #ball moving to the right side
    #else ball moves to left side
    if direction:
        ball_dir = 1 # ball_dir doesnt change the 
                     # x component of velocity vector
    else:
        ball_dir = -1 # ball_dir used to reverse the x component
                      # of velocity vector
    

# helper function to set new game properties
def new_game():
    #declare and initialize globals
    global paddle1_vel, paddle2_vel 
    global PADDLE1_VER_MOVE,PADDLE2_VER_MOVE, score1, score2, DIRECTION
    global ACCELERATION,count
        
    #declares that at the start of the game paddles have no vertical movement
    PADDLE1_VER_MOVE,PADDLE2_VER_MOVE  = None,None
    
    #variable to store number of hits on paddles(combined)
    count = 0
    
    #acceleration of ball is set to 1 during the start of game
    ACCELERATION = 1
    
    #velocities of paddles are set to 0 during the start of game
    paddle1_vel,paddle2_vel = 0,0
    
    #scores of players are set to zero
    score1,score2 = 0, 0
    
    #logic to randomly select a ball direction during the start of game
    directions = [True,False]
    DIRECTION = directions[random.randrange(0,2)]
    
    #call to place the ball in the table and move the ball 
    #to selected side
    spawn_ball(DIRECTION)
    

# helper function respawn the ball if the ball goes into a gutter    
def respawn():
    global DIRECTION, ACCELERATION,count
    #resets the acceleration and count of hit on paddles
    ACCELERATION,count = 1,0
    
    #selects the opposite side as direction
    DIRECTION = not DIRECTION
    
    #call to place the ball in the middle of table and move the ball
    #to the direction set
    spawn_ball(DIRECTION)
    

# helper function to reflect the ball if ball collides with paddle    
def reflect_from_paddle():
    global DIRECTION, ACCELERATION,count
    
    #registers the number of hits on the paddle(combined)
    count +=1
    
    #increases the accleration of the ball by 10% for first 20 hits on
    #the paddle. If acceleration is increased uncontrollebly
    #it reaches a state in which we can't even see the ball
    #which is drawn on canvas
    if count<=20:
        ACCELERATION *= 1.1
        
    #JUST IN CASE if the players are too good
    #to make it a bit more challenging
    if count>=35 and count<40:
        ACCELERATION *=1.1
    
    #reverses the direction
    ball_vel[0]*=-1  
    
    #globally set to which direction the ball is moving now
    #True means Right side
    #False means Left side
    DIRECTION = not DIRECTION
    
    
#handler which draws the game on canvas
def draw(canvas):
    #declare globals used
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos
    global ball_vel,ball_dir,DIRECTION  
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
   
    
    # update ball
    
    #logic to reverse direction when ball hits on the walls
    if ball_pos[1]<=BALL_RADIUS or ball_pos[1]>=HEIGHT-1-BALL_RADIUS:
        ball_vel[1]*=-1 #reverses the direction along y axis
        
    
    #logic to check whether ball fell into gutter or collided 
    #with the paddle
    if ball_pos[0]<=PAD_WIDTH+BALL_RADIUS or ball_pos[0]>=WIDTH-1-BALL_RADIUS-PAD_WIDTH:
        
        #if the ball is moving to left side
        if not DIRECTION:
            #logic to check whether paddle is behind the ball
            if (ball_pos[1]>=paddle1_pos and ball_pos[1]<=paddle1_pos+PAD_HEIGHT):
                #calls function to reverse the direction of the ball
                reflect_from_paddle()
            else:
                #ball fall into gutter.
                #updates the score of the opponent in the right side
                score2+=1
                
                #call to respawn the ball in the middle and move
                #the ball to right side
                respawn()
                
        #if the ball is moving to right side        
        elif DIRECTION:
            #logic to check whether paddle is behind the ball 
            if (ball_pos[1]>=paddle2_pos and ball_pos[1]<=paddle2_pos+PAD_HEIGHT):
                #calls function to reverse the direction of the ball
                reflect_from_paddle()
            else:
                #ball fall into gutter
                #updates the score of the opponent in the left side
                score1+=1
                
                #call to respawn the ball in the middle and move
                #the ball to left side
                respawn()
       
    #logic to set the current position of the ball
    ball_pos[0] = ball_pos[0] + ACCELERATION*ball_dir*ball_vel[0]
    ball_pos[1] = ball_pos[1] - ACCELERATION*ball_vel[1]
    
    # draws the ball on the canvas
    canvas.draw_circle(ball_pos,BALL_RADIUS,1,"White","White")    
    
    # update paddle's vertical position, keep paddle on the screen
    
    # if PADDLE1_VER_MOVE is True, paddle1 is moving up
    if PADDLE1_VER_MOVE:
        #logic to check if whole paddle remains in canvas
        #when move upwards
        if paddle1_pos-paddle1_vel>=0:
                #if yes, redraws the paddle by going paddle1_vel pixels upwards
                paddle1_pos = paddle1_pos - paddle1_vel
        #if not, set the position of paddle to the top of canvas
        else:
                #if not, set the position of paddle to the top of canvas
                paddle1_pos = 0
            
    #if paddle1 is moving downwards
    elif not PADDLE1_VER_MOVE:
        if paddle1_pos+PAD_HEIGHT+paddle1_vel<=HEIGHT:
                #if yes, redraws the paddle by goind paddle1_vel pixels downwards
                paddle1_pos = paddle1_pos + paddle1_vel
        else:
                #if not, sets the position of paddle to the 
                #canvas_height - paddle_height position
                #so the the paddle can be drawn completely
                paddle1_pos = HEIGHT-PAD_HEIGHT
                
    
    #same logic of paddle1 follows for paddle2
    if PADDLE2_VER_MOVE:
        if paddle2_pos-paddle2_vel>=0:
                paddle2_pos = paddle2_pos - paddle2_vel
        else:
                paddle2_pos = 0
            
    elif not PADDLE2_VER_MOVE:
        if paddle2_pos+PAD_HEIGHT+paddle2_vel<=HEIGHT:
                paddle2_pos = paddle2_pos + paddle2_vel
        else:
                paddle2_pos = HEIGHT-PAD_HEIGHT
        
   
    # draw paddles
    canvas.draw_polygon([(0,paddle1_pos),(PAD_WIDTH,paddle1_pos),(PAD_WIDTH,paddle1_pos+PAD_HEIGHT),(0,paddle1_pos+PAD_HEIGHT)],1,"White","White")
    canvas.draw_polygon([(WIDTH,paddle2_pos),(WIDTH-PAD_WIDTH,paddle2_pos),(WIDTH-PAD_WIDTH,paddle2_pos+PAD_HEIGHT),(WIDTH,paddle2_pos+PAD_HEIGHT)],1,"White","White")
    
    # draw scores
    canvas.draw_text(str(score1),SCORE1_POS,50,"White")
    canvas.draw_text(str(score2),SCORE2_POS,50,"White")
        
#event handler to handle key press
def keydown(key):
    global paddle1_vel, paddle2_vel
    global PADDLE1_VER_MOVE, PADDLE2_VER_MOVE
    current_key = chr(key)
    
    #logic to set paddle movement
    if current_key == 'W':
        #True - paddle1 moves upwards
        PADDLE1_VER_MOVE = True 
    elif current_key == 'S':
        #False - paddle1 moves downwards
        PADDLE1_VER_MOVE = False
        
    #logic to set paddle velocity if only these two keys are pressed
    if PADDLE1_VER_MOVE != None:
        paddle1_vel = 5
        
    #logic of paddle1 applies here also
    if key == simplegui.KEY_MAP["up"]:
        PADDLE2_VER_MOVE = True
    elif key == simplegui.KEY_MAP["down"]:
        PADDLE2_VER_MOVE = False
    if PADDLE2_VER_MOVE != None:
        paddle2_vel = 5
     
   
#event handler to handle key release
def keyup(key):
    global paddle1_vel, paddle2_vel
    global PADDLE1_VER_MOVE,PADDLE2_VER_MOVE
    current_key = chr(key)
    
    #if the released key is either 'W' or 'S'
    #sets the paddle velocity as 0
    #and sets the status of vertical movement as None
    if current_key == 'W' or current_key == 'S':
        paddle1_vel = 0
        PADDLE1_VER_MOVE = None
        
    #logic of paddle1 applies here also
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]: 
        paddle2_vel = 0
        PADDLE2_VER_MOVE = None

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
#adds restart button, event handler set as new_game() function
frame.add_button("Restart",new_game,100)
#sets frame's draw handler
frame.set_draw_handler(draw)

#registers keydown() function as keydown event handler
frame.set_keydown_handler(keydown)

#regiseters keyup() function as keyup event handler
frame.set_keyup_handler(keyup)

#invokes new_game()
new_game()
# starts frame
frame.start()