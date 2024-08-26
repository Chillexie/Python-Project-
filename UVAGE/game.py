# Xinwen Chen dkt4kr
# Jessica Li ahw6pq

# game description: This game will have one player, 30 black mini dots, 4 randomly placed yellow stars,
# and 3 randomly placed red bombs. The player can move by using the up, down, left, and right arrows.
# The goal for the player is to eat as much black dots as possible within 10 seconds, the timer is displayed
# to the left of the score display.  Once the player touches the black
# dot, the dot will disappear. The initial speed of the player is set at a fixed number,
# which will increase if the player touches the yellow star. If the player touches the red bomb, their
# hearts will -1, the amount of hearts is displayed in the upper right.  The game is over when all the hearts
# are gone or when the time is up, and then there will be a game over screen which the player can restart
# by pressing the space bar

# Basic features:
# 1. User Input: movement with up, down, left, and right arrows
# 2. Game Over: when the player's hearts are all gone or when the time is up.
# 3. Images: we'll use local image file to create the players

# Additional features:
# 1. Collectibles: we'll randomly add 4 yellow stars that will boost the speed the player
# 2. Restart: after the game is over, the player can replay by pressing the space bar
# 3. Timer: 10s count up timer
# 4. Another feature: if the player touches the red dot, their hearts will -1

import uvage
import random
screen_x = 1000
screen_y = 800
start_x = 50
start_y = 70
game_over = False
collected_dots = []

camera = uvage.Camera(screen_x,screen_y)
player = uvage.from_image(start_x, start_y, "player.png")
player.scale_by(0.035)

# we created a list of yellow stars that could increase the speed
star1 = uvage.from_image(600, 90, "star.png")
star1.scale_by(0.02)
star2 = uvage.from_image(310, 250, "star.png")
star2.scale_by(0.02)
star3 = uvage.from_image(600, 500, "star.png")
star3.scale_by(0.02)
star4 = uvage.from_image(200, 700, "star.png")
star4.scale_by(0.02)
stars = [star1, star2, star3, star4]

count = 0
player_speed = 2

FPS =  60
frames = 0
time = 0
time_text = uvage.from_text(300, 40, str(time), 40, 'black')
# we create a list of all the black dots that the players will collect
dot_list = [uvage.from_color(100, 200, "black", 20, 20),
            uvage.from_color(250, 150, "black", 20, 20),
            uvage.from_color(400, 200, "black", 20, 20),
            uvage.from_color(550, 150, "black", 20, 20),
            uvage.from_color(700, 200, "black", 20, 20),
            uvage.from_color(850, 150, "black", 20, 20),
            uvage.from_color(100, 200, "black", 20, 20),
            uvage.from_color(250, 300, "black", 20, 20),
            uvage.from_color(400, 200, "black", 20, 20),
            uvage.from_color(550, 300, "black", 20, 20),
            uvage.from_color(700, 200, "black", 20, 20),
            uvage.from_color(850, 300, "black", 20, 20),
            uvage.from_color(100, 400, "black", 20, 20),
            uvage.from_color(250, 450, "black", 20, 20),
            uvage.from_color(400, 400, "black", 20, 20),
            uvage.from_color(550, 450, "black", 20, 20),
            uvage.from_color(700, 400, "black", 20, 20),
            uvage.from_color(850, 450, "black", 20, 20),
            uvage.from_color(150, 500, "black", 20, 20),
            uvage.from_color(350, 500, "black", 20, 20),
            uvage.from_color(450, 500, "black", 20, 20),
            uvage.from_color(500, 500, "black", 20, 20),
            uvage.from_color(650, 500, "black", 20, 20),
            uvage.from_color(700, 500, "black", 20, 20),
            uvage.from_color(100, 600, "black", 20, 20),
            uvage.from_color(250, 550, "black", 20, 20),
            uvage.from_color(400, 600, "black", 20, 20),
            uvage.from_color(550, 650, "black", 20, 20),
            uvage.from_color(700, 600, "black", 20, 20),
            uvage.from_color(850, 700, "black", 20, 20),]

#game over screen
game_over_text = uvage.from_text(screen_x/2, screen_y/2, 'GAME OVER', 120, 'red')
restart_button_height = 100
restart_button_width = 200
restart_button = uvage.from_color(screen_x/2, screen_y/2 + game_over_text.height*0.5 + .5*restart_button_height + 15, 'black', restart_button_width, restart_button_height)
restart_text= uvage.from_text(game_over_text.x, game_over_text.y + game_over_text.height*0.5 + .5*restart_button_height + 15, 'Press Space to Restart', 40 , 'white')

# we created a list of 3 red bombs that will be randomly placed
bomb1 = uvage.from_image(random.randint(100, 700), random.randint(200, 700), "bomb.png")
bomb1.scale_by(0.1)
bomb2 = bomb1.copy_at(random.randint(random.randint(200, 700), 900), random.randint(200, 700))
bomb3 = bomb1.copy_at(random.randint(random.randint(200, 700), 900), random.randint(200, 700))
bombs = [bomb1, bomb2, bomb3]

# we created a list of 3 hearts
heart1 = uvage.from_image(810, 50, "heart.png")
heart1.scale_by(0.02)
heart2 = heart1.copy_at(880, 50)
heart3 = heart1.copy_at(950, 50)
hearts = [heart1, heart2, heart3]

# creates 30 black dots, if being touched, it will disappear from the screen, the score will update
def set_up_dots():
    global dot_list, count, player, collected_dots
    # draw  the rest of the dots
    for i in dot_list:
        camera.draw(i)
        # the dot will disappear once the player touches it
        if player.touches(i):
            i.move(-20000, -100)
            collected_dots.append(i)
            count += 1

# the player can control their movement by pressing arrows
def player_movement():
    global player, dot_list, player_speed
    # set up player's movement with keys
    if uvage.is_pressing("right arrow"):
        player.x += player_speed
    elif uvage.is_pressing("left arrow"):
        player.x -= player_speed
    elif uvage.is_pressing('up arrow'):
        player.y -= player_speed
    elif uvage.is_pressing('down arrow'):
        player.y += player_speed

# displays the amount of black dots collected in the upper middle
def score_display():
    global count
    # display the total number of dots the player has collected
    background = uvage.from_color(500, 20, "black", 200, 50)
    camera.draw(background)
    score = uvage.from_text(500, 25, str(count), 50, "red", bold = True)
    camera.draw(score)

# Player's speed will increase if they touched the star
def fast_speed():
    global stars, player,player_speed
    # The star will disappear when the player touches it
    for i in stars:
        camera.draw(i)
        if player.touches(i):
            i.move(-2000, -100)
            player_speed += 1.5

# creates 3 bombs and 3 hearts, hearts will -1 if player touches the bomb, and the game is over when all hearts are gone
def set_up_bombs():
    global bombs, hearts
    num = 0
    for i in hearts:
        camera.draw(i)
    for i in bombs:
        camera.draw(i)
        if player.touches(i):
            i.move(-1000, -100)
            hearts.pop(-1)
    global game_over
    if len(hearts) == 0:
        game_over = True

# count up to 10 seconds, if time is more than 10s, the game will end
def timer():
    global time,time_text, game_over
    time += .016
    time_text = uvage.from_text(300, 35, str(int(time)), 40, 'black', bold = True)
    if time >= 10:
        game_over = True
def run_game():
    player_movement()
    fast_speed()
    score_display()
    set_up_dots()
    set_up_bombs()
    timer()
    camera.draw(player)
    camera.draw(time_text)

# if the player presses space bar on the game over screen, the game will restart with everything back to what it was
def restart():
    global hearts, count, time, bombs, player_speed, start_x, start_y, dot_list, stars, collected_dots
    bomb1 = uvage.from_image(random.randint(100, 700), random.randint(200, 700), "bomb.png")
    bomb1.scale_by(0.1)
    bomb2 = bomb1.copy_at(random.randint(random.randint(200, 700), 900), random.randint(200, 700))
    bomb3 = bomb1.copy_at(random.randint(random.randint(200, 700), 900), random.randint(200, 700))
    bombs = [bomb1, bomb2, bomb3]

    heart1 = uvage.from_image(810, 50, "heart.png")
    heart1.scale_by(0.02)
    heart2 = heart1.copy_at(880, 50)
    heart3 = heart1.copy_at(950, 50)
    hearts = [heart1, heart2, heart3]

    star1 = uvage.from_image(600, 90, "star.png")
    star1.scale_by(0.02)
    star2 = uvage.from_image(310, 250, "star.png")
    star2.scale_by(0.02)
    star3 = uvage.from_image(600, 500, "star.png")
    star3.scale_by(0.02)
    star4 = uvage.from_image(200, 700, "star.png")
    star4.scale_by(0.02)
    stars = [star1, star2, star3, star4]

    dot_list = [uvage.from_color(100, 200, "black", 20, 20),
                uvage.from_color(250, 150, "black", 20, 20),
                uvage.from_color(400, 200, "black", 20, 20),
                uvage.from_color(550, 150, "black", 20, 20),
                uvage.from_color(700, 200, "black", 20, 20),
                uvage.from_color(850, 150, "black", 20, 20),
                uvage.from_color(100, 200, "black", 20, 20),
                uvage.from_color(250, 300, "black", 20, 20),
                uvage.from_color(400, 200, "black", 20, 20),
                uvage.from_color(550, 300, "black", 20, 20),
                uvage.from_color(700, 200, "black", 20, 20),
                uvage.from_color(850, 300, "black", 20, 20),
                uvage.from_color(100, 400, "black", 20, 20),
                uvage.from_color(250, 450, "black", 20, 20),
                uvage.from_color(400, 400, "black", 20, 20),
                uvage.from_color(550, 450, "black", 20, 20),
                uvage.from_color(700, 400, "black", 20, 20),
                uvage.from_color(850, 450, "black", 20, 20),
                uvage.from_color(150, 500, "black", 20, 20),
                uvage.from_color(350, 500, "black", 20, 20),
                uvage.from_color(450, 500, "black", 20, 20),
                uvage.from_color(500, 500, "black", 20, 20),
                uvage.from_color(650, 500, "black", 20, 20),
                uvage.from_color(700, 500, "black", 20, 20),
                uvage.from_color(100, 600, "black", 20, 20),
                uvage.from_color(250, 550, "black", 20, 20),
                uvage.from_color(400, 600, "black", 20, 20),
                uvage.from_color(550, 650, "black", 20, 20),
                uvage.from_color(700, 600, "black", 20, 20),
                uvage.from_color(850, 700, "black", 20, 20), ]

    # we moved the collected dots back to their ori position after the previous round of playing
    for i in collected_dots:
        i.move(20000, 100)

    player.x = start_x
    player.y = start_y
    time = 0
    count = 0
    player_speed = 2
    player_movement()
    fast_speed()
    timer()
    score_display()
    set_up_dots()
    set_up_bombs()
    camera.draw(player)
    camera.draw(time_text)
def endscreen():
    global game_over_text, restart_text, game_over
    camera.draw(game_over_text)
    camera.draw(restart_text)
    if uvage.is_pressing("space"):
        game_over = False
        restart()

def tick():
    camera.clear("orange")
    global game_over
    if not game_over:
        run_game()
    else:
        endscreen()
    camera.display()

uvage.timer_loop(FPS, tick)



