from dataclasses import dataclass
import math

G = 9.81
eps = 1000


@dataclass
class Model:
    pos_x = 0
    pos_y = 0
    start_pos_x: int
    start_pos_y: int
    velocity_ans: float = 0
    mu: float = 0.01
    alpha: float = 1.166667 * math.pi
    radius: float = 3
    weight: float = 2
    velocity: float = 8
    a: float = 0
    times = []
    xs = []
    ys = []
    velocities = []
    accelerations = []
    is_falls = []
    cur_a = 0
    cur_tg_acceleration = 0
    cur_centripetal_acceleration = 0

    is_fall = False
    time = 0
    dt = 1 / eps

    cur_v = velocity_ans
    cur_vx = cur_v
    cur_vy = 0

    def reset(self):
        self.xs = []
        self.ys = []
        self.times = []
        self.velocities = []
        self.accelerations = []
        self.is_falls = []

        self.cur_v = self.velocity
        self.cur_a = 0
        self.pos_x = self.start_pos_x
        self.pos_y = self.start_pos_y

    def fall(self):
        dt = 1 / eps
        time = 0
        alpha_cur = math.acos((-self.pos_y + self.start_pos_y + self.radius) / self.radius)

        while self.pos_x > self.start_pos_x:
            self.change_acceleration(alpha_cur, True)

            self.change_velocity()

            self.change_coords(True)
            alpha_cur = math.acos((-self.pos_y + self.start_pos_y + self.radius) / self.radius)

            time += dt

            self.times.append(self.time)
            self.accelerations.append(self.cur_a)
            self.velocities.append(self.cur_v)

            self.xs.append(self.pos_x)
            self.ys.append(self.pos_y)
            self.is_falls.append(True)

    def change_coords(self, is_fall=False):
        if is_fall:
            self.pos_x = max(self.pos_x + self.cur_vx * self.dt + self.cur_tg_acceleration * self.dt ** 2 / 2, 0)
            self.pos_y = max(self.pos_y + self.cur_vy * self.dt + self.cur_centripetal_acceleration * self.dt ** 2 / 2,
                             self.check())
        else:
            self.pos_x = max(self.pos_x + self.cur_vx * self.dt + self.cur_tg_acceleration * self.dt * self.dt / 2, 0)
            prev_pos_y = self.pos_y
            self.pos_y = max(self.pos_y + self.cur_vy * self.dt + self.cur_centripetal_acceleration * self.dt * self.dt / 2,
                             self.start_pos_y)

            return prev_pos_y

    def change_velocity(self):
        self.cur_vx += self.cur_tg_acceleration * self.dt
        self.cur_vy += self.cur_centripetal_acceleration * self.dt

        self.cur_v = math.sqrt(self.cur_vx ** 2 + self.cur_vy ** 2)

    def change_acceleration(self, alpha_cur, is_fall):
        if is_fall:
            centripetal_acceleration = self.cur_v ** 2 / self.radius
            tg_acceleration = -self.mu * (centripetal_acceleration + G * math.cos(alpha_cur)) - G * math.sin(
                alpha_cur)

            self.cur_centripetal_acceleration = math.cos(alpha_cur) * centripetal_acceleration + math.sin(
                alpha_cur) * tg_acceleration
            self.cur_tg_acceleration = -math.sin(alpha_cur) * centripetal_acceleration + math.cos(
                alpha_cur) * tg_acceleration
            self.cur_a = math.sqrt(self.cur_tg_acceleration ** 2 + self.cur_centripetal_acceleration ** 2)
        else:
            centripetal_acceleration = self.cur_v ** 2 / self.radius
            tg_acceleration = -self.mu * (centripetal_acceleration + G * math.cos(alpha_cur)) + G * math.sin(
                alpha_cur)

            self.cur_centripetal_acceleration = math.cos(alpha_cur) * centripetal_acceleration - math.sin(
                alpha_cur) * tg_acceleration
            self.cur_tg_acceleration = -math.sin(alpha_cur) * centripetal_acceleration - math.cos(
                alpha_cur) * tg_acceleration
            self.cur_a = math.sqrt(self.cur_tg_acceleration ** 2 + self.cur_centripetal_acceleration ** 2)

    def move_by_loop(self):
        dt = 1 / eps

        self.pos_x = self.start_pos_x
        self.pos_y = self.start_pos_y

        is_all_way = False
        alpha_cur = 0
        self.cur_vx = self.cur_v

        while True:
            self.change_acceleration(alpha_cur, False)
            centripetal_acceleration = self.cur_v ** 2 / self.radius

            self.change_velocity()
            prev_pos_y = self.change_coords()

            if self.pos_x > self.start_pos_x:
                alpha_cur = math.acos((-self.pos_y + self.start_pos_y + self.radius) / self.radius)
            else:
                alpha_cur = math.acos((self.pos_y - self.start_pos_y - self.radius) / self.radius) + math.pi

            if alpha_cur >= self.alpha:
                is_all_way = True
                break

            if prev_pos_y > self.pos_y and alpha_cur < math.pi:
                break

            self.time += dt

            self.times.append(self.time)
            self.accelerations.append(self.cur_a)
            self.velocities.append(self.cur_v)

            self.xs.append(self.pos_x)
            self.ys.append(self.pos_y)
            self.is_falls.append(False)

            N = self.weight * (centripetal_acceleration + G * math.cos(alpha_cur))

            if N <= 0 or alpha_cur == 0:
                break

        return is_all_way

    def arc_separation(self):
        dt = 1 / eps
        self.cur_a = -G

        while self.pos_y >= self.start_pos_y:

            self.cur_vy += self.cur_a * dt

            self.cur_v = math.sqrt(self.cur_vy ** 2 + self.cur_vx ** 2)

            self.pos_x = max(self.pos_x + self.cur_vx * dt, 0)
            self.pos_y = self.pos_y + self.cur_vy * dt + self.cur_a * dt ** 2 / 2

            if self.pos_y <= self.check():
                self.pos_y = self.check()
                self.times.append(self.time)
                self.accelerations.append(abs(self.cur_a))
                self.velocities.append(self.cur_v)

                self.xs.append(self.pos_x)
                self.ys.append(self.pos_y)
                self.is_falls.append(True)
                self.fall()
                break

            self.time += dt

            self.times.append(self.time)
            self.accelerations.append(abs(self.cur_a))
            self.velocities.append(self.cur_v)

            self.xs.append(self.pos_x)
            self.ys.append(self.pos_y)
            self.is_falls.append(True)

        return

    def start(self):
        self.pos_x = self.start_pos_x
        self.pos_y = self.start_pos_y
        self.time = 0
        self.reset()
        self.cur_vx = self.cur_v
        self.cur_vy = 0
        is_all_way = self.move_by_loop()
        self.arc_separation()
        return is_all_way

    def bin_search(self):
        left = 1
        right = 100
        while right - left > 0.00001:
            mid = (left + right) / 2
            self.velocity = mid
            if self.start():
                right = mid
            else:
                left = mid
        self.velocity_ans = right
        return right

    def check(self):
        if self.pos_x <= self.start_pos_x:
            return self.start_pos_y

        if self.pos_x <= self.start_pos_x + self.radius:
            alpha = math.asin((self.pos_x - self.start_pos_x) / self.radius)
            y = self.start_pos_y + self.radius - self.radius * math.cos(alpha)
            return y
        return 0
