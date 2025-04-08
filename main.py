import pygame
import sys
import random
from player import Player
from box import Box
from game_map import GameMap
from game_ui import GameUI
from game_state import GameState, bfs_solve, astar_search, get_best_move
from constants import FPS, TILE_SIZE, ROWS, COLS, SCREEN_WIDTH, SCREEN_HEIGHT, OUTLINE_COLOR, OUTLINE_THICKNESS, NUM_BOXES

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    # Oyun nesnelerini oluştur
    game_ui = GameUI(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, OUTLINE_COLOR, OUTLINE_THICKNESS)
    
    while True:
        # Önce algoritma seçimi
        method = game_ui.choose_method()
        print("Seçilen yöntem:", method)

        # Sonra oyun haritasını oluştur
        game_map = GameMap(ROWS, COLS, TILE_SIZE)
        player = Player(ROWS // 2, COLS // 2, TILE_SIZE)
        targets = game_map.generate_targets(NUM_BOXES)
        boxes = game_map.generate_boxes(NUM_BOXES, targets)
        game_over = False
        move_count = 0
        end_counter = 0

        # A* çözümü
        if method == "astar":
            game_ui.draw(game_map, player, boxes)
            solution = astar_search(player, boxes, targets)
            if solution is None:
                print("A* ile çözüm bulunamadı!")
                pygame.quit()
                sys.exit()
            print("A* Çözümü:", solution)
            move_index = 0

        # BFS çözümü
        if method == "bfs":
            initial_box_positions = [box.position for box in boxes]
            initial_state = GameState(player.pos, initial_box_positions)
            solution = bfs_solve(initial_state, targets)
            if solution is None:
                print("BFS ile çözüm bulunamadı!")
                pygame.quit()
                sys.exit()
            print("BFS Çözümü:", solution)
            move_index = 0

        # Oyun döngüsü
        while not game_over:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_over = True
                        break

            if game_over:
                break

            if not player.is_moving:
                if method == "greedy":
                    ai_move = get_best_move(player, boxes, targets, move_count)
                    if ai_move:
                        collision_box = player.collision(ai_move, boxes)
                        if collision_box and not collision_box.target_reached and not collision_box.is_moving:
                            if collision_box.can_push(ai_move, boxes):
                                collision_box.move(ai_move, boxes, targets)
                                player.move(ai_move)
                        elif not collision_box:
                            player.move(ai_move)
                        move_count += 1
                elif method == "astar":
                    if move_index < len(solution):
                        current_move = solution[move_index]
                        print("A* seçilen hamle:", current_move)
                        collision_box = player.collision(current_move, boxes)
                        if collision_box:
                            if collision_box.can_push(current_move, boxes):
                                collision_box.move(current_move, boxes, targets)
                                player.move(current_move)
                        else:
                            player.move(current_move)
                        move_index += 1
                elif method == "bfs":
                    if move_index < len(solution):
                        current_move = solution[move_index]
                        print("BFS seçilen hamle:", current_move)
                        collision_box = player.collision(current_move, boxes)
                        if collision_box:
                            if collision_box.can_push(current_move, boxes):
                                collision_box.move(current_move, boxes, targets)
                                player.move(current_move)
                        else:
                            player.move(current_move)
                        move_index += 1

            player.update()
            for box in boxes:
                box.update()
                box.check_target(targets)

            if game_map.is_game_end():
                end_counter += 1
                if end_counter >= FPS // 1.5:
                    button_rect = game_ui.draw_success_screen()

                    # Kullanıcı tıklayana kadar bekle
                    waiting_for_restart = True
                    while waiting_for_restart:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if button_rect.collidepoint(event.pos):
                                    waiting_for_restart = False
                                    game_over = True
                                    break
                        pygame.display.update()
                    continue

            game_ui.draw(game_map, player, boxes)

if __name__ == "__main__":
    main()