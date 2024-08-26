import uvage
camera = uvage.Camera(800,600)
walker_images = uvage.load_sprite_sheet("walk_stand.png", 1, 6)
walker = uvage.from_image(600,300, walker_images[-1])
def move_walker():
    global walking_frame
    if uvage.is_pressing("right arrow"):
        walker.x += 3
    if uvage.is_pressing('left arrow'):
        walker.x -= 3
    if walking_frame >= 4.7:
        walking_frame = 0
    else:
        walking_frame += 0.3
    walker.image = walker_images[walking_frame]
    camera.draw(walker)
def tick():
    camera.clear("white")
    move_walker()
    camera.display()

uvage.timer_loop(30, tick)