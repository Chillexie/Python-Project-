import uvage
import random
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

FPS = 30
GRAVITY = 3
X_SPEED = 3
PLATFORM_SPEED = 2
DIST_BETWEEN_PLATFORMS = 140
camera = uvage.Camera(SCREEN_WIDTH, SCREEN_WIDTH)
# pyImage = uvage.from_image(300,300,"https://www.python.org/static/img/python-logo@2x.png")


box = uvage.from_color((SCREEN_WIDTH/2), SCREEN_HEIGHT, 'yellow', SCREEN_WIDTH, 0.05*(SCREEN_HEIGHT))
platforms = []
player = uvage.from_color(30, 30, 'white', 30, 30)
score = 0
frames = 0
score_text = uvage.from_text(580, 20, str(score), 40, 'white')
game_over = False
game_over_text = uvage.from_text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 'GAME OVER', 100, 'red')

restart_button_height = .1*(SCREEN_HEIGHT)
restart_button_width = .2*(SCREEN_WIDTH)
restart_button = uvage.from_color(game_over_text.x, game_over_text.y + game_over_text.height*0.5 + .5*restart_button_height + 15, 'turquoise', restart_button_width, restart_button_height)
restart_text= uvage.from_text(game_over_text.x, game_over_text.y + game_over_text.height*0.5 + .5*restart_button_height + 15, 'RESTART', 20 , 'white')
PLAYER_START_X = 30
uvage.from_text
PLAYER_START_y = 30
def create_platform( y, width):
    global platforms
    hole = random.randint(0 + width/2, SCREEN_WIDTH - (width/2))
    if hole is width/2:
        x = SCREEN_WIDTH/2 + width
        right_platform = uvage.from_color(x , y, 'light blue', SCREEN_WIDTH - width, 0.05*SCREEN_HEIGHT)
        platforms.append(right_platform)
        return
    if hole is SCREEN_WIDTH - (width/2):
        x = SCREEN_WIDTH/2 + width
        left_platform = uvage.from_color(x, y, 'light blue', SCREEN_WIDTH - width, 0.05*SCREEN_HEIGHT)
        platforms.append(left_platform)
        return
    else:
        left_width =(hole - (width/2))
        x_left = left_width/2
        left = uvage.from_color(x_left, y, 'pink', left_width, 0.05*SCREEN_HEIGHT)
        right_width = (SCREEN_WIDTH - (hole + (width/2)))
        x_right = (hole + (width/2)) + right_width/2
        right = uvage.from_color(x_right, y, 'pink', right_width, 0.05*SCREEN_HEIGHT)
    platforms.append(left)
    platforms.append(right)

def update_platform():
    global platforms
    platforms_past_threshold = True
    if platforms:
        for platform in platforms:
            platform.speedy = - PLATFORM_SPEED
            platform.move_speed()
            if platform.y > SCREEN_HEIGHT - DIST_BETWEEN_PLATFORMS:
                platforms_past_threshold = False
    if platforms_past_threshold:
        create_platform(SCREEN_HEIGHT, 50)

def check_collision(dynamic_body, static_body):
    if not dynamic_body.bottom_touches(static_body):
        dynamic_body.speedy = GRAVITY
    if dynamic_body.bottom_touches(static_body):
        dynamic_body.y = static_body.y - static_body.height / 2 - dynamic_body.height / 2
        dynamic_body.speedy = 0

def check_collision_platforms(dynamic_body):
    global platforms
    for platform in platforms:
        check_collision(dynamic_body, platform)
    return

def player_movement():
    player.speedx = 0
    if uvage.is_pressing('r'):
        player.speedx += X_SPEED
    if uvage.is_pressing('l'):
        player.speedx -= X_SPEED
    if player.x - (player.width / 2) <= 0:
        if player.speedx < 0:
            player.speedx = 0
        player.x = 0 + (player.width / 2)
    elif player.x + (player.width / 2) >= SCREEN_WIDTH:
        if player.speedx > 0:
            player.speedx = 0
        player.x = SCREEN_WIDTH - (player.width / 2)
    if player.y + player.height/2 <= 0:
        global game_over
        game_over = True

    check_collision_platforms(player)
    player.move_speed()
    if player.y + player.height/2 > SCREEN_HEIGHT:
        player.y = SCREEN_HEIGHT - player.height/2

def update_score():
    global score
    global score_text
    if frames % FPS == 0:
        score +=1
        score_text = uvage.from_text(580, 20, str(score), 40, 'white')
        score_text.x = (SCREEN_WIDTH - score_text.width/2) - 10

def run_game():
    global speed
    global frames
    frames += 1

    update_platform()
    player_movement()
    update_score()
    global platforms
    for platform in platforms:
        camera.draw(platform)
    camera.draw(player)
    camera.draw(score_text)

def mouse_collision(body):
    x, y = uvage.pygame.mouse.get_pos()
    if body.x + (body.width/2) > x > body.x - (body.width/2):
        if body.y + (body.height/2) > y > body.y - (body.height/2):
            return True
    return False

def show_endscreen():
    camera.draw(game_over_text)
    camera.draw(restart_button)
    camera.draw(restart_text)

    # mouse_collision(restart_button)
    if uvage.pygame.mouse.get_pressed()[0] and mouse_collision(restart_button):
        global game_over
        global score
        global platforms
        score = 0
        game_over = False
        player.x = PLAYER_START_X
        player.y = PLAYER_START_y
        platforms = []

def tick():
    camera.clear("black")
    if not game_over:
        run_game()
    else:
        show_endscreen()

    camera.display()

uvage.timer_loop(FPS, tick)