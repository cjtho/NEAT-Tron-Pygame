from common import Common
import pygame


class GamePlayerVsPlayer(Common):

    def handle_control_input(self, key):
        for player_id, controls in self.player_controls.items():
            player = self.player_group[player_id]
            if key in controls["directions"]:
                player.change_direction(controls["directions"][key])
                break
            elif key in controls["powers"]:
                for _ in range(5):
                    if player.boosts > 0:
                        player.move(teleport=True)
                player.boosts -= 1

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            self.handle_control_input(event.key)
