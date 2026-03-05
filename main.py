import arcade
import random
import math

WIDTH = 1000
HEIGHT = 700
PLAYER_SPEED = 5
BULLET_SPEED = 12
BASE_ENEMY_SPEED = 1.5

STATE_MENU = 0
STATE_GAME = 1
STATE_GAME_OVER = 2

class ZombieGame(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Zombie Survival: Wave Defense")
        arcade.set_background_color(arcade.color.OLIVE)

        self.state = STATE_MENU
        self.player_list = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.player = None
        self.score = 0
        self.health = 100
        self.wave = 1
        self.spawn_timer = 0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.score = 0
        self.health = 100
        self.wave = 1
        self.spawn_timer = 0

        # Player
        self.player = arcade.Sprite("assets/player.png", scale=0.25)
        self.player.center_x = WIDTH // 2
        self.player.center_y = HEIGHT // 2
        self.player_list.append(self.player)

        self.state = STATE_GAME

    def on_draw(self):
        self.clear()

        if self.state == STATE_MENU:
            arcade.draw_text("ZOMBIE SURVIVAL", WIDTH // 2, HEIGHT // 2 + 50,
                             arcade.color.RED, 50, anchor_x="center")
            arcade.draw_text("Press ENTER to Start", WIDTH // 2, HEIGHT // 2 - 20,
                             arcade.color.WHITE, 20, anchor_x="center")

        elif self.state == STATE_GAME:
            self.player_list.draw()
            self.bullets.draw()
            self.enemies.draw()
            arcade.draw_text(f"Score: {self.score}  Health: {self.health}  Wave: {self.wave}", 
                             20, HEIGHT - 40, arcade.color.WHITE, 18)

        elif self.state == STATE_GAME_OVER:
            arcade.draw_text("GAME OVER", WIDTH // 2, HEIGHT // 2 + 50,
                             arcade.color.RED, 50, anchor_x="center")
            arcade.draw_text(f"Final Score: {self.score}", WIDTH // 2, HEIGHT // 2,
                             arcade.color.WHITE, 25, anchor_x="center")
            arcade.draw_text("Press ENTER to Restart", WIDTH // 2, HEIGHT // 2 - 50,
                             arcade.color.WHITE, 20, anchor_x="center")

    def on_update(self, delta_time):
        if self.state != STATE_GAME:
            return

        self.player_list.update()
        self.bullets.update()
        self.enemies.update()

        
        mouse_x = self._mouse_x
        mouse_y = self._mouse_y
        
       
        self.player.angle = math.degrees(math.atan2(mouse_y - self.player.center_y, 
                                                   mouse_x - self.player.center_x)) - 90

        
        self.spawn_timer += 1
        if self.spawn_timer > max(60 - self.wave * 5, 20):
            #Zombie
            enemy = arcade.Sprite("assets/zombie.png", scale=0.07)
            if random.random() > 0.5:
                enemy.center_x = random.choice([0, WIDTH])
                enemy.center_y = random.randint(0, HEIGHT)
            else:
                enemy.center_x = random.randint(0, WIDTH)
                enemy.center_y = random.choice([0, HEIGHT])
            self.enemies.append(enemy)
            self.spawn_timer = 0

        
        for enemy in self.enemies:
            dx = self.player.center_x - enemy.center_x
            dy = self.player.center_y - enemy.center_y
            angle = math.atan2(dy, dx)
            enemy.angle = math.degrees(angle) - 90
            speed = BASE_ENEMY_SPEED + self.wave * 0.3
            enemy.center_x += speed * math.cos(angle)
            enemy.center_y += speed * math.sin(angle)

        #Attack
        hit_list = arcade.check_for_collision_with_list(self.player, self.enemies)
        for hit in hit_list:
            hit.remove_from_sprite_lists()
            self.health -= 10

        
        for bullet in self.bullets:
            if bullet.bottom > HEIGHT or bullet.top < 0 or bullet.right < 0 or bullet.left > WIDTH:
                bullet.remove_from_sprite_lists()
                continue

            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()
                    self.score += 1

        if self.score >= self.wave * 10:
            self.wave += 1

        if self.health <= 0:
            self.state = STATE_GAME_OVER

    def on_key_press(self, key, modifiers):
        if (self.state == STATE_MENU or self.state == STATE_GAME_OVER) and key == arcade.key.ENTER:
            self.setup()
        elif self.state == STATE_GAME:
            if key == arcade.key.W: self.player.change_y = PLAYER_SPEED
            elif key == arcade.key.S: self.player.change_y = -PLAYER_SPEED
            elif key == arcade.key.A: self.player.change_x = -PLAYER_SPEED
            elif key == arcade.key.D: self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S): self.player.change_y = 0
        if key in (arcade.key.A, arcade.key.D): self.player.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if self.state != STATE_GAME:
            return
        
        bullet = arcade.Sprite("assets/bullet.png", scale=0.2)
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y
        angle = math.atan2(y - self.player.center_y, x - self.player.center_x)
        bullet.change_x = BULLET_SPEED * math.cos(angle)
        bullet.change_y = BULLET_SPEED * math.sin(angle)
        self.bullets.append(bullet)

def main():
    game = ZombieGame()
    arcade.run()

if __name__ == "__main__":
    main()
