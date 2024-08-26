import uvage
import random
screen_x = 600
screen_y = 600

camera = uvage.Camera(screen_x,screen_y)
x_speed = 7
gravity = 3
game_over = False
frames = 0
game_over_text = uvage.from_text(screen_x/2, screen_y/2, 'GAME OVER', 120, 'red')
restart_text = uvage.from_text(screen_x/2, screen_y/1.5, 'press space bar to restart', 30, 'white')
platforms = []
distance_between_platforms = 140
platform_speed = 2
player = uvage.from_color(30,30,"white",30,30)
start_x = 30
start_y = 30

def create_platform(y, width):
    global platforms
    space = random.randint(0 + width/2, screen_x - (width/2))
    if space == width/2:
        x = screen_x/2 + width
        right_platform = uvage.from_color(x , y, 'black', screen_x - width, 0.05*screen_y)
        platforms.append(right_platform)
        return
    if space == screen_x - (width/2):
        x = screen_x/2 + width
        left_platform = uvage.from_color(x , y, 'black', screen_x - width, 0.05*screen_y)
        platforms.append(left_platform)
        return
    else:
        left_width = (space - (width/2))
        x_left = left_width / 2
        left = uvage.from_color(x_left, y, 'pink', left_width, 0.05 * screen_y)
        right_width = (screen_x - (space + (width / 2)))
        x_right = (space + (width/2)) + right_width/2
        right = uvage.from_color(x_right, y, 'pink', right_width, 0.05 * screen_y)
    platforms.append(left)
    platforms.append(right)

def update_platform():
    global platforms
    platforms_past_threshold = True
    if platforms:
        for platform in platforms:
            platform.speedy = - platform_speed
            platform.move_speed()
            if platform.y > screen_y - distance_between_platforms:
                platforms_past_threshold = False
    if platforms_past_threshold:
        create_platform(screen_y, 50)
def check_collision(dynamic_body, static_body):
    if not dynamic_body.bottom_touches(static_body):
        dynamic_body.speedy = gravity
    if dynamic_body.bottom_touches(static_body):
        dynamic_body.y = static_body.y - static_body.height / 2 - dynamic_body.height / 2
        dynamic_body.speedy = 0

def check_collision_platforms(dynamic_body):
    global platforms
    for platform in platforms:
        check_collision(dynamic_body, platform)
    return

def movement():
    if uvage.is_pressing('left arrow'):
        player.x -= x_speed
    if uvage.is_pressing("right arrow"):
        player.x += x_speed
    if player.x - (player.width / 2) <= 0:
        if player.speedx < 0:
            player.speedx = 0
        player.x = 0 + (player.width / 2)
    elif player.x + (player.width / 2) >= screen_x:
        if player.speedx > 0:
            player.speedx = 0
        player.x = screen_x - (player.width / 2)
    if player.y + player.height/2 <= 0:
        global game_over
        game_over = True

    check_collision_platforms(player)
    player.move_speed()
    if player.y + player.height / 2 > screen_y:
        player.y = screen_x - player.height / 2

def start():
    global x_speed
    global frames
    frames += 1

    update_platform()
    movement()
    global platforms
    for platform in platforms:
        camera.draw(platform)
    camera.draw(player)

def show_endscreen():
    camera.draw(game_over_text)
    camera.draw(restart_text)
    if uvage.is_pressing("space"):
        global game_over
        global score
        global platforms
        score = 0
        game_over = False
        player.x = start_x
        player.y = start_y
        platforms = []


def tick():
    camera.clear("black")
    if not game_over:
        start()
    else:
        show_endscreen()

    camera.display()

uvage.timer_loop(30, tick)
