import pygame, random
from math import inf
pygame.init()

color = pygame.Color('black'), pygame.Color('red'), pygame.Color('yellow')
EMPTY, HUMAN, AI = range(len(color))
ROWS, COLS, WIN = 6, 7, 4
board = [[EMPTY] * COLS for row in range(ROWS)]

SQ = 100
width, height = COLS * SQ, ROWS * SQ
RADIUS = SQ//2 - 5
screen = pygame.display.set_mode((width, height + SQ))
myfont = pygame.font.SysFont('monospace', 75)
turn = random.choice([HUMAN, AI])

def is_valid_location(board, col): return board[ROWS-1][col] == 0

def make_move(board, player, col):
    new_board = [*map(list.copy, board)]
    for row in new_board:
        if row[col] == EMPTY:
            row[col] = player
            return new_board

def won(board, piece): return score_position(board, piece) == inf

def evaluate_window(window, piece):
    score = 0
    if window.count(piece) == 4: score = inf
    elif window.count(piece) == 3 and window.count(EMPTY) == 1: score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2: score += 2
    if window.count(3 - piece) == 3 and window.count(EMPTY) == 1: score -= 4
    return score

def score_position(board, piece):
    score = 0
    for row in board:
        if row[COLS//2] == piece: score += 3
    for row in board:
        for c in range(COLS - WIN + 1):
            score += evaluate_window(row[c:c+WIN], piece)
    for col in zip(*board):
        for r in range(ROWS - WIN + 1):
            score += evaluate_window(col[r:r+WIN], piece)
    for r in range(ROWS - WIN + 1):
        for c in range(COLS - WIN + 1):
            nw_se = [board[r+i][c+i] for i in range(WIN)]
            sw_ne = [board[r+3-i][c+i] for i in range(WIN)]
            score += evaluate_window(nw_se, piece) + evaluate_window(sw_ne, piece)
    return score

def minimax(board, depth, α, β, aggregate):
    valid_locations = get_valid_locations(board)
    if won(board, AI): return None, inf
    elif won(board, HUMAN): return None, -inf
    elif not valid_locations: return None, 0
    elif not depth: return None, score_position(board, AI)
    elif aggregate is max:
        value = None
        for col in valid_locations:
            new_score = minimax(make_move(board, AI, col), depth-1, α, β, min)[1]
            if depth == 5: print('max', col, new_score)
            if value is None or new_score > value:
                column, value = col, new_score
                if value > α:
                    α = value
                    if α >= β: break
        return column, value
    elif aggregate is min:
        value = None
        for col in valid_locations:
            new_score = minimax(make_move(board, HUMAN, col), depth-1, α, β, max)[1]
            if depth == 4: print(col, new_score, end='\t')
            if value is None or new_score < value:
                column, value = col, new_score
                if value < β:
                    β = value
                    if β <= α: break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def erase_strip_above(draw_player):
    pygame.draw.rect(screen, color[EMPTY], pygame.Rect(0, 0, width, SQ))
    if draw_player: pygame.draw.circle(screen, color[HUMAN], (pygame.mouse.get_pos()[0], SQ//2), RADIUS)
    pygame.display.update()

def draw_board():
    print(*board[::-1], sep='\n')
    print('_' * 21)
    erase_strip_above(False)
    pygame.draw.rect(screen, pygame.Color('blue'), pygame.Rect(0, SQ, width, height))
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.circle(screen, color[board[r][c]], (c*SQ+SQ//2, height-r*SQ+SQ//2), RADIUS)
    pygame.display.update()

def game_over(player):
    draw_board()
    label = myfont.render(f'Player {player} wins!', 1, color[player])
    screen.blit(label, (40, 10))
    pygame.display.flip()
    pygame.time.wait(player * 1_000)
    pygame.quit()
    raise SystemExit

draw_board()
while ...:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: game_over(EMPTY)
        if turn == AI: continue
        if event.type == pygame.MOUSEMOTION: erase_strip_above(True)
        if event.type == pygame.MOUSEBUTTONDOWN:
            erase_strip_above(False)
            col = event.pos[0] // SQ
            if is_valid_location(board, col):
                board = make_move(board, HUMAN, col)
                draw_board()
                if won(board, HUMAN): game_over(HUMAN)
                turn = AI
    if turn == AI:
        col, minimax_score = minimax(board, 5, -inf, inf, max)
        if is_valid_location(board, col):
            board = make_move(board, AI, col)
            draw_board()
            if won(board, AI): game_over(AI)
            turn = HUMAN
            erase_strip_above(True)
