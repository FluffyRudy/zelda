import pygame


class Upgrade:
    def __init__(self, player: pygame.sprite.Sprite):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.max_player_attrs = len(player.STATS)
        self.font = pygame.font.Font("graphics/font/joystix.ttf", 24)

        self.selection_index = 0
        self.selection_time = None
        self.cooldown = 300
        self.can_move = True

        font = pygame.font.Font("graphics/font/joystix.ttf", 25)
        UpgradeBox.set_font(font=font)
        self.upgrade_box_height = self.display_surface.get_height() * 0.8
        self.upgrade_box_width = (
            self.display_surface.get_width() - 100
        ) // self.max_player_attrs
        self.start_pos_x = (
            self.display_surface.get_width()
            - self.upgrade_box_width * self.max_player_attrs
            - self.max_player_attrs * 10
        ) // 2

        self.create_upgrade_box()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_RIGHT]:
                self.selection_index += 1
            elif keys[pygame.K_LEFT]:
                self.selection_index -= 1
            if keys[pygame.K_SPACE]:
                self.upgrade_box_list[self.selection_index].trigger_action(self.player)
            self.selection_index = max(
                0,
                min(self.selection_index, self.max_player_attrs - 1),
            )

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= self.cooldown:
                self.can_move = True

    def create_upgrade_box(self):
        self.upgrade_box_list = []
        attrs_names = list(self.player.STATS.keys())
        attrs_values = list(self.player.STATS.values())

        for i in range(self.max_player_attrs):
            top = self.display_surface.get_height() * 0.1
            left = self.start_pos_x + i * self.upgrade_box_width + (i * 10)
            upgrade_box = UpgradeBox(
                (top, left),
                (self.upgrade_box_width, self.upgrade_box_height),
                i,
            )
            self.upgrade_box_list.append(upgrade_box)

    def display(self):
        self.get_input()
        self.selection_cooldown()
        for index, upgrade_box in enumerate(self.upgrade_box_list):
            attribute_stat = self.player.get_stat_by_index(index)
            upgrade_box.display(
                self.display_surface, self.selection_index, attribute_stat
            )


class UpgradeBox:
    def __init__(
        self,
        topleft: tuple[int, int],
        size: tuple[int, int],
        index: int,
    ):
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill((96, 125, 139, 200))
        self.position = topleft[1], topleft[0]
        self.rect = self.image.get_rect(topleft=(self.position))
        self.radius_pos = topleft[1] - 5, topleft[0] - 5
        self.radius_size = size[0] + 10, size[1] + 10
        self.index = index

    @classmethod
    def set_font(self, font: pygame.font.Font):
        self.font = font

    def trigger_action(self, player: pygame.sprite.Sprite):
        selected_attr = list(player.STATS.keys())[self.index]
        required_cost = player.STATS[list(player.STATS.keys())[self.index]]

    def display(
        self,
        display_surface: pygame.Surface,
        selection_index: int,
        attribute_stat: dict,
    ):
        label = self.font.render(str(attribute_stat["attr"]), True, "yellow")
        value = self.font.render(str(attribute_stat["value"]["amount"]), True, "yellow")
        max_value = self.font.render(
            str(attribute_stat["value"]["max_value"]), True, "red"
        )

        display_surface.blit(self.image, self.position)
        self.display_bar(display_surface, attribute_stat["value"])

        display_surface.blit(
            label,
            (
                self.position[0] + (self.image.get_width() - label.get_width()) // 2,
                self.position[1] - label.get_height(),
            ),
        )
        display_surface.blit(
            value,
            (
                self.position[0] + (self.image.get_width() - value.get_width()) // 2,
                self.rect.bottom - value.get_height(),
            ),
        )
        display_surface.blit(
            max_value, ((self.rect.centerx - max_value.get_width() // 2), self.rect.top)
        )
        if self.index == selection_index:
            pygame.draw.rect(
                display_surface,
                (0, 255, 208),
                (self.radius_pos, self.radius_size),
                5,
                5,
            )
            self.image.fill((96, 125, 139))
        else:
            self.image.fill((96, 125, 139, 200))

    def display_bar(self, display_surface: pygame.Surface, attribute_stat: dict):
        midtop = self.rect.centerx, self.rect.top + 60
        midbottom = self.rect.centerx, self.rect.bottom - 60
        full_height = midbottom[1] - midtop[1]
        relative_height = (
            attribute_stat["amount"] / attribute_stat["max_value"]
        ) * full_height

        # just hardcoded since code is already long
        value_rect = (midtop[0] - 15, midbottom[1] - relative_height - 5, 30, 10)
        pygame.draw.rect(display_surface, "white", value_rect)
        pygame.draw.line(display_surface, "white", midtop, midbottom, 4)
