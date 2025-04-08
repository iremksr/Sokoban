import heapq
import time
import random
from collections import deque
from constants import ROWS, COLS

class GameState:
    def __init__(self, player_pos, box_positions, path=[]):
        self.player_pos = player_pos  # (row, col)
        self.box_positions = tuple(sorted(box_positions))  # hashable
        self.path = path  # list of directions

    def __hash__(self):
        return hash((self.player_pos, self.box_positions))

    def __eq__(self, other):
        return (self.player_pos == other.player_pos and
                self.box_positions == other.box_positions)

def is_goal_state(state, targets):
    for box in state.box_positions:
        box_pos = box   # Box nesnesinin pozisyonunu al
        return all(box_pos in targets for box_pos in state.box_positions)

def move_pos(pos, direction):
    row, col = pos
    if direction == "UP": return (row-1, col)
    if direction == "DOWN": return (row+1, col)
    if direction == "LEFT": return (row, col-1)
    if direction == "RIGHT": return (row, col+1)

def bfs_solve(initial_state, targets):
    visited = set()
    queue = deque([initial_state])

    while queue:
        state = queue.popleft()

        # Debug: Şu anki durum
        print(f"Checking state with player at {state.player_pos} and box positions {state.box_positions}")

        # Hedef durumu kontrol et
        if is_goal_state(state, targets):
            print("Goal state found!")
            return state.path

        # Eğer bu durum daha önce ziyaret edildiyse, atla
        if state in visited:
            print(f"State with player at {state.player_pos} already visited, skipping...")
            continue
        visited.add(state)

        # Her yön için hareket et
        for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
            new_player_pos = move_pos(state.player_pos, direction)

            # Hareketin geçerli olup olmadığını kontrol et
            if not (0 <= new_player_pos[0] < ROWS and 0 <= new_player_pos[1] < COLS):
                print(f"Move {direction} out of bounds, skipping...")
                continue

            new_box_positions = list(state.box_positions)

            if new_player_pos in new_box_positions:
                box_index = new_box_positions.index(new_player_pos)
                new_box_pos = move_pos(new_box_positions[box_index], direction)

                # Kutunun geçerli alana yerleşip yerleşemeyeceğini kontrol et
                if (not (0 <= new_box_pos[0] < ROWS and 0 <= new_box_pos[1] < COLS)) or (new_box_pos in new_box_positions):
                    print(f"Move {direction} blocked by another box or out of bounds, skipping...")
                    continue

                new_box_positions[box_index] = new_box_pos

            # Yeni durumu oluştur ve kuyruğa ekle
            new_state = GameState(new_player_pos, new_box_positions, state.path + [direction])
            print(f"Adding new state with player at {new_player_pos} and box positions {new_box_positions}")
            queue.append(new_state)

    print("No solution found.")
    return None

def astar_search(initial_player, initial_boxes, targets):
    start_state = (initial_player.row, initial_player.col,
                   tuple(sorted((box.row, box.col) for box in initial_boxes)))
    print("A* Başlangıç Durumu:", start_state)
    h = simple_heuristic(initial_player, initial_boxes, targets)
    open_set = []
    heapq.heappush(open_set, (h, 0, start_state, [], initial_player.clone(), [box.clone() for box in initial_boxes]))
    visited = {start_state: 0}

    while open_set:
        f, g, state, path, player, boxes = heapq.heappop(open_set)
        # Kısa bir sleep ekleyerek CPU kontrolünü bırakabiliriz.
        time.sleep(0.0005)
        if is_boxes_in_targets(boxes, targets):
            print("A* Çözüm Bulundu! Path:", path)
            return path
        for move in ["UP", "DOWN", "LEFT", "RIGHT"]:
            new_player = player.clone()
            new_boxes = [box.clone() for box in boxes]
            collision_box = new_player.collision(move, new_boxes)
            valid_move = False
            if collision_box:
                if collision_box.can_push(move, new_boxes):
                    collision_box.simulate_move(move)
                    new_player.simulate_move(move)
                    valid_move = True
            else:
                new_player.simulate_move(move)
                valid_move = True
            if not valid_move:
                continue
            new_state = (new_player.row, new_player.col,
                         tuple(sorted((box.row, box.col) for box in new_boxes)))
            new_g = g + 1
            if new_state in visited and visited[new_state] <= new_g:
                continue
            visited[new_state] = new_g
            new_h = simple_heuristic(new_player, new_boxes, targets)
            new_f = new_g + new_h
            new_path = path + [move]
            heapq.heappush(open_set, (new_f, new_g, new_state, new_path, new_player, new_boxes))
    print("A* algoritması çözüm bulamadı!")
    return None

def is_boxes_in_targets(boxes, targets):
    """Her kutu hedef pozisyonda mı kontrol eder."""
    return all((box.row, box.col) in targets for box in boxes)

def simple_heuristic(player, boxes, targets):
    """
    Aday kutu–hedef çifti üzerinden hesaplar:
    (oyuncunun seçilen kutuya mesafesi) + (kutunun hedefe mesafesi)
    """
    candidate_box, candidate_target = get_candidate_box_target(player, boxes, targets)
    if candidate_box is None or candidate_target is None:
        return 0
    dist_player_box = abs(player.row - candidate_box.row) + abs(player.col - candidate_box.col)
    dist_box_target = abs(candidate_box.row - candidate_target[0]) + abs(candidate_box.col - candidate_target[1])
    return dist_player_box + dist_box_target

def get_candidate_box_target(player, boxes, targets):
    """Henüz tamamlanmamış kutulardan oyuncuya en yakın olanı ve onun en yakın hedefini seçer."""
    candidate_boxes = []
    best_dist = float("inf")
    for box in boxes:
        if not box.target_reached:
            d = abs(player.row - box.row) + abs(player.col - box.col)
            if d < best_dist:
                best_dist = d
                candidate_boxes = [box]
            elif d == best_dist:
                candidate_boxes.append(box)
    if not candidate_boxes:
        return None, None
    chosen_box = random.choice(candidate_boxes)
    best_target_dist = float("inf")
    chosen_target = None
    for target in targets:
        d = abs(chosen_box.row - target[0]) + abs(chosen_box.col - target[1])
        if d < best_target_dist:
            best_target_dist = d
            chosen_target = target
    return chosen_box, chosen_target

def compute_push_direction(box, target):
    """Belirler: eğer hedef kutunun üstündeyse push yönü 'UP', altındaysa 'DOWN', solundaysa 'LEFT', sağındaysa 'RIGHT'."""
    if target[0] < box.row:
        return "UP"
    elif target[0] > box.row:
        return "DOWN"
    elif target[1] < box.col:
        return "LEFT"
    elif target[1] > box.col:
        return "RIGHT"
    else:
        return None

def compute_ideal_tile(box, push_direction):
    """
    Push yönüne göre, oyuncunun ideal konumu:
      - Eğer push 'UP' ise oyuncu kutunun altında (box.row+1)
      - Eğer push 'DOWN' ise oyuncu kutunun üstünde (box.row-1)
      - Eğer push 'LEFT' ise oyuncu kutunun sağında (box.col+1)
      - Eğer push 'RIGHT' ise oyuncu kutunun solunda (box.col-1)
    """
    if push_direction == "UP":
         return (box.row + 1, box.col)
    elif push_direction == "DOWN":
         return (box.row - 1, box.col)
    elif push_direction == "LEFT":
         return (box.row, box.col + 1)
    elif push_direction == "RIGHT":
         return (box.row, box.col - 1)
    else:
         return (box.row, box.col)

def find_path_to_tile(player, boxes, target_tile):
    """
    Oyuncunun (player.row, player.col) konumundan target_tile (row, col) konumuna
    kutuları engel olarak görerek BFS ile bir yol bulur.
    """
    start = (player.row, player.col)
    if start == target_tile:
        return [start]

    box_positions = set((b.row, b.col) for b in boxes)
    visited = set([start])
    queue = deque()
    queue.append((start, [start]))

    while queue:
        (cur_r, cur_c), path = queue.popleft()
        for (nr, nc) in [(cur_r-1, cur_c), (cur_r+1, cur_c),
                         (cur_r, cur_c-1), (cur_r, cur_c+1)]:
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if (nr, nc) not in box_positions:
                    if (nr, nc) not in visited:
                        visited.add((nr, nc))
                        new_path = path + [(nr, nc)]
                        if (nr, nc) == target_tile:
                            return new_path
                        queue.append(((nr, nc), new_path))
    return None

def get_adaptive_reposition_move(player, ideal_tile, boxes):
    """
    Oyuncunun, kutuları engel kabul ederek ideal_tile konumuna doğru
    BFS ile bir yol bulmasını sağlar.
    """
    path = find_path_to_tile(player, boxes, ideal_tile)
    
    if path is None:
        print("Bu harita çözülemez!")
        pygame.quit()
        sys.exit()

    if len(path) < 2:
        return None

    next_r, next_c = path[1]
    dr = next_r - player.row
    dc = next_c - player.col

    if dr == -1 and dc == 0:
        return "UP"
    elif dr == 1 and dc == 0:
        return "DOWN"
    elif dr == 0 and dc == -1:
        return "LEFT"
    elif dr == 0 and dc == 1:
        return "RIGHT"
    return None

def get_best_move(player, boxes, targets, move_count):
    candidate_box, candidate_target = get_candidate_box_target(player, boxes, targets)
    if candidate_box is None or candidate_target is None:
        return None
    push_dir = compute_push_direction(candidate_box, candidate_target)
    ideal_tile = compute_ideal_tile(candidate_box, push_dir)
    
    if (player.row, player.col) != ideal_tile:
         reposition = get_adaptive_reposition_move(player, ideal_tile, boxes)
         if reposition is not None:
              return reposition
    if candidate_box.can_push(push_dir, boxes):
         return push_dir
         
    best_move = None
    best_score = float("inf")
    possible_moves = ["UP", "DOWN", "LEFT", "RIGHT"]
    for move in possible_moves:
        sim_player = player.clone()
        sim_boxes = [box.clone() for box in boxes]
        collision_box = sim_player.collision(move, sim_boxes)
        valid_move = False
        if collision_box:
            if collision_box.can_push(move, sim_boxes):
                collision_box.simulate_move(move)
                sim_player.simulate_move(move)
                valid_move = True
        else:
            sim_player.simulate_move(move)
            valid_move = True
        if valid_move:
            score = simple_heuristic(sim_player, sim_boxes, targets) + move_count * 0.5 + random.uniform(0, 0.5)
            if score < best_score:
                best_score = score
                best_move = move
    return best_move 