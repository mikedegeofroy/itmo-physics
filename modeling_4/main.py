import pygame
import pygame_gui
import math
from gui import Gui
from model import Model

pygame.init()

WIDTH, HEIGHT = 1000, 600
FPS = 60

object_color = (0, 0, 255)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('loop')
window.fill((0, 0, 0))
clock = pygame.time.Clock()

start_v = 12
pos_start = 700
height = 500
coefficient = 60
rad = 5

object = Model(pos_start, height)
gui = Gui();

weight_input_box = gui.draw_input("3")
radius_input_box = gui.draw_input("2")
alpha_input_box = gui.draw_input("0.8333333333")
mu_input_box = gui.draw_input("0.01")
button = gui.draw_button("start")

def draw_base():
    window.fill((28, 30, 37))

    r = object.radius * coefficient + rad
    alpha = object.alpha
    pygame.draw.arc(window, (0, 0, 0), (pos_start - r, height + rad - 2 * r, 2 * r, 2 * r), 3 * math.pi / 2,
                    3 * math.pi / 2 + alpha, 3)

el = pygame.draw.circle(window, object_color, (pos_start, height), rad)

def draw():
    pos_x = pos_start
    pos_y = height

    object.velocity = start_v
    object.start()
    draw_base()
    pygame.draw.circle(window, object_color, (pos_x, pos_y), 5)

    for i in range(0, len(object.xs)):
        draw_base()

        for j in range(i):
            for_x = pos_x + (object.xs[j] - pos_x) * coefficient
            for_y = pos_y - (object.ys[j] - pos_y) * coefficient
            if for_x < -rad or for_y < -rad:
                continue

            if object.is_falls[j]:
                pygame.draw.circle(window, (255, 0, 0), (for_x, pos_y - (object.ys[j] - pos_y) * coefficient), 1)
            else:
                pygame.draw.circle(window, (0, 0, 255), (for_x, pos_y - (object.ys[j] - pos_y) * coefficient), 1)

        required_v = gui.render_text(f'required v0: {object.velocity_ans:.3f} м/с')
        window.blit(required_v, (10, HEIGHT - 24 * 1 - 10))

        text_t = f't: {object.times[i]:.2f} с'
        text_v = f'|v|: {object.velocities[i]:.2f} м/с'
        text_a = f'|a|: {object.accelerations[i]:.2f} м/с^2'

        window.blit(gui.render_text(text_t), (10, HEIGHT - 24 * 2 - 10))
        window.blit(gui.render_text(text_v), (10, HEIGHT - 24 * 3 - 10))
        window.blit(gui.render_text(text_a), (10, HEIGHT - 24 * 4 - 10))

        pygame.display.update()


while True:
    time_delta = clock.tick(FPS) / 1000.0

    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button:
                if weight_input_box.get_text():
                    weight = float(weight_input_box.get_text())
                if alpha_input_box.get_text():
                    alpha = float(alpha_input_box.get_text()) * math.pi
                if mu_input_box.get_text():
                    mu = float(mu_input_box.get_text())
                if radius_input_box.get_text():
                    radius = float(radius_input_box.get_text())

                object = Model(pos_start, height, 
                                mu=mu, 
                                alpha=alpha, 
                                radius=radius, 
                                velocity=start_v
                                )
                object.velocity_ans = object.bin_search()
                object.cur_v = object.velocity_ans
                draw()

        gui.gui_manager.process_events(event)

    gui.gui_manager.update(time_delta)

    draw_base()
    el = pygame.draw.circle(window, object_color, (pos_start, height), 1)

    required_v = gui.render_text(f'required v0: {object.velocity_ans:.3f} м/с')
    window.blit(required_v, (10, HEIGHT - 24 * 1 - 10))

    gui.gui_manager.draw_ui(window)

    pygame.display.flip()

