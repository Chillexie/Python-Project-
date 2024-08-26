import uvage
import random

screen_width = 800
screen_height = 600
camera = uvage.Camera(screen_width, screen_height)
score = 0

court = uvage.from_image(screen_width //2, screen_height //2, "uva_court.jpg")
court.scale_by(3)
court.rotate(90)

def draw_scenery():
    camera.draw(court)

def tick():
    camera.clear("black")
    draw_scenery()
    camera.display()

interactives = []
num_balls = 15
balls = []

for i in range(num_balls):
    x = random.rnadrange(sideline_width, screen_width - sideline_width)
uvage.timer_loop(30, tick)