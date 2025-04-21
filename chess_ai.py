import random

# Giá trị các quân cờ
piece_values = {
    'P': 100,   # Tốt
    'N': 320,   # Mã
    'B': 330,   # Tượng
    'R': 500,   # Xe
    'Q': 900,   # Hậu
    'K': 20000  # Vua
}

# Bảng giá trị vị trí cho từng quân cờ
pawn_scores = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

knight_scores = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

bishop_scores = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5,  5,  5,  5,  5,-10],
    [-10,  0,  5,  0,  0,  5,  0,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

rook_scores = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

queen_scores = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

king_scores_middle_game = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

king_scores_end_game = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
]

piece_position_scores = {
    'P': pawn_scores,
    'N': knight_scores,
    'B': bishop_scores,
    'R': rook_scores,
    'Q': queen_scores,
    'K': king_scores_middle_game
}

# Hằng số để kiểm tra giai đoạn cuối game
ENDGAME_MATERIAL_THRESHOLD = 3000  # Ngưỡng vật liệu tổng cộng để xác định giai đoạn cuối game

CHECKMATE_SCORE = 10000
STALEMATE_SCORE = 0
DEPTH = 3

def find_random_move(valid_moves):
    return random.choice(valid_moves)

def find_best_move(game_state, valid_moves, return_queue=None):
    """
    Tìm nước đi tốt nhất sử dụng thuật toán alpha-beta.
    """
    global next_move, position_history
    next_move = None
    # Reset lịch sử vị trí khi tìm nước đi mới
    position_history = {}
    random.shuffle(valid_moves)
    
     # Tính tổng vật liệu để xác định giai đoạn của game
    total_material = 0
    for row in range(8):
        for col in range(8):
            piece = game_state.board[row][col]
            if piece != "--" and piece[1] != 'K':
                total_material += piece_values[piece[1]]
    
    # Điều chỉnh độ sâu tìm kiếm dựa trên giai đoạn trò chơi
    current_depth = DEPTH
    if total_material < ENDGAME_MATERIAL_THRESHOLD:
        current_depth += 1  # Tăng độ sâu trong giai đoạn cuối
    
    # Dùng alpha-beta để tìm nước đi tốt nhất
    find_move_alpha_beta(game_state, valid_moves, current_depth, -float('inf'), float('inf'), 
                        1 if game_state.white_to_move else -1)
    
    if return_queue is not None:
        return_queue.put(next_move)
    return next_move

def find_move_alpha_beta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    """
    Thuật toán minimax với alpha-beta pruning.
    """
    global next_move
    
    if depth == 0:
        random_noise = random.uniform(-5, 5)
        return turn_multiplier * score_board(game_state) + random_noise
    
    max_score = -float('inf')
    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        score = -find_move_alpha_beta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        game_state.undo_move()
        
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        
        alpha = max(alpha, score)
        if alpha >= beta:
            break
            
    return max_score

position_history = {}

def score_board(game_state):
    """
    Đánh giá trạng thái bàn cờ.
    Điểm số dương có lợi cho bên trắng, điểm số âm có lợi cho bên đen.
    """
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE_SCORE  # Đen chiếu bí
        else:
            return CHECKMATE_SCORE  # Trắng chiếu bí
    elif game_state.stalemate:
        return STALEMATE_SCORE  # Hòa

    score = 0
    total_material = 0

    # Tính tổng vật liệu để xác định giai đoạn của game
    for row in range(8):
        for col in range(8):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_type = piece[1]
                if piece_type != 'K':
                    total_material += piece_values[piece_type]

    is_endgame = total_material < ENDGAME_MATERIAL_THRESHOLD

    for row in range(8):
        for col in range(8):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_type = piece[1]
                piece_score = piece_values[piece_type]

                if piece_type == 'K' and is_endgame:
                    position_table = king_scores_end_game
                else:
                    position_table = piece_position_scores[piece_type]

                if piece[0] == 'w':
                    position_score = position_table[row][col]
                    score += piece_score + position_score
                else:
                    position_score = position_table[7 - row][col]
                    score -= piece_score + position_score

    # Các đánh giá bổ sung
    score += evaluate_mobility(game_state)
    score += evaluate_pawn_structure(game_state)
    score += evaluate_king_safety(game_state, is_endgame)
    score += evaluate_pawn_promotion(game_state, is_endgame)
    score += evaluate_king_activity_endgame(game_state, is_endgame)

    board_hash = str(game_state.board)
    if board_hash in position_history:
        position_history[board_hash] += 1
        if position_history[board_hash] >= 3:  # Nếu vị trí xuất hiện từ 3 lần trở lên
            return STALEMATE_SCORE  # Coi như hòa
        else:
            score -= 50 * position_history[board_hash]  # Giảm điểm theo số lần xuất hiện
    else:
        position_history[board_hash] = 1
        
    return score

def evaluate_mobility(game_state):
    """
    Đánh giá khả năng di chuyển của các quân cờ.
    """
    original_turn = game_state.white_to_move
    
    # Đếm nước đi của trắng
    game_state.white_to_move = True
    white_moves = len(game_state.get_valid_moves())
    
    # Đếm nước đi của đen
    game_state.white_to_move = False
    black_moves = len(game_state.get_valid_moves())
    
    # Khôi phục lượt đi
    game_state.white_to_move = original_turn
    
    return (white_moves - black_moves) * 10

def evaluate_pawn_structure(game_state):
    """
    Đánh giá cấu trúc tốt: tốt cô lập, tốt đôi, tốt bảo vệ...
    """
    score = 0
    
    # Vị trí của tất cả các quân tốt
    white_pawns = []
    black_pawns = []
    
    for row in range(8):
        for col in range(8):
            piece = game_state.board[row][col]
            if piece == "wP":
                white_pawns.append((row, col))
            elif piece == "bP":
                black_pawns.append((row, col))
    
    # Đánh giá tốt cô lập (không có tốt đồng minh ở cột liền kề)
    white_isolated = count_isolated_pawns(white_pawns)
    black_isolated = count_isolated_pawns(black_pawns)
    score -= white_isolated * 15
    score += black_isolated * 15
    
    # Đánh giá tốt đôi (cùng cột)
    white_doubled = count_doubled_pawns(white_pawns)
    black_doubled = count_doubled_pawns(black_pawns)
    score -= white_doubled * 20
    score += black_doubled * 20
    
    # Đánh giá tốt được bảo vệ bởi tốt khác
    white_protected = count_protected_pawns(game_state, white_pawns, "w")
    black_protected = count_protected_pawns(game_state, black_pawns, "b")
    score += white_protected * 10
    score -= black_protected * 10
    
    return score

def evaluate_pawn_promotion(game_state, is_endgame):
    """
    Đánh giá khả năng phong hậu của các quân tốt
    """
    score = 0
    
    # Hệ số nhân cho giá trị phong hậu trong cuối game
    endgame_multiplier = 2.0 if is_endgame else 1.0
    
    for row in range(8):
        for col in range(8):
            piece = game_state.board[row][col]
            
            # Đánh giá tốt trắng
            if piece == "wP":
                # Khoảng cách đến hàng phong hậu
                distance_to_promotion = row
                # Điểm cộng thêm càng gần hàng phong hậu
                promotion_value = (7 - distance_to_promotion) * (7 - distance_to_promotion) * 5
                
                # Kiểm tra xem có đường đi thông thoáng không
                path_clear = True
                for i in range(1, distance_to_promotion + 1):
                    if row - i >= 0 and game_state.board[row - i][col] != "--":
                        path_clear = False
                        break
                
                if path_clear:
                    promotion_value *= 2  # Nhân đôi giá trị nếu đường đi thông thoáng
                
                # Kiểm tra xem có quân địch có thể chặn không
                can_be_blocked = False
                for enemy_row in range(row-1, -1, -1):
                    if col > 0 and game_state.board[enemy_row][col-1] == "bP":
                        can_be_blocked = True
                        break
                    if col < 7 and game_state.board[enemy_row][col+1] == "bP":
                        can_be_blocked = True
                        break
                
                if not can_be_blocked:
                    promotion_value *= 1.5  # Tăng giá trị nếu khó bị chặn
                
                score += promotion_value * endgame_multiplier
            
            # Đánh giá tốt đen
            elif piece == "bP":
                # Khoảng cách đến hàng phong hậu
                distance_to_promotion = 7 - row
                # Điểm cộng thêm càng gần hàng phong hậu
                promotion_value = (7 - distance_to_promotion) * (7 - distance_to_promotion) * 5
                
                # Kiểm tra xem có đường đi thông thoáng không
                path_clear = True
                for i in range(1, distance_to_promotion + 1):
                    if row + i < 8 and game_state.board[row + i][col] != "--":
                        path_clear = False
                        break
                
                if path_clear:
                    promotion_value *= 2  # Nhân đôi giá trị nếu đường đi thông thoáng
                
                # Kiểm tra xem có quân địch có thể chặn không
                can_be_blocked = False
                for enemy_row in range(row+1, 8):
                    if col > 0 and game_state.board[enemy_row][col-1] == "wP":
                        can_be_blocked = True
                        break
                    if col < 7 and game_state.board[enemy_row][col+1] == "wP":
                        can_be_blocked = True
                        break
                
                if not can_be_blocked:
                    promotion_value *= 1.5  # Tăng giá trị nếu khó bị chặn
                
                score -= promotion_value * endgame_multiplier
    
    return score

def count_isolated_pawns(pawns):
    """
    Đếm số lượng tốt cô lập (không có tốt đồng minh ở cột liền kề)
    """
    isolated_count = 0
    pawn_columns = [col for _, col in pawns]
    
    for _, col in pawns:
        is_isolated = True
        for adjacent_col in [col-1, col+1]:
            if 0 <= adjacent_col < 8 and adjacent_col in pawn_columns:
                is_isolated = False
                break
        if is_isolated:
            isolated_count += 1
    
    return isolated_count

def count_doubled_pawns(pawns):
    """
    Đếm số lượng tốt đôi (nhiều tốt trên cùng một cột)
    """
    columns = [col for _, col in pawns]
    doubled_count = 0
    
    for col in range(8):
        pawns_in_col = columns.count(col)
        if pawns_in_col > 1:
            doubled_count += pawns_in_col - 1
    
    return doubled_count

def count_protected_pawns(game_state, pawns, color):
    """
    Đếm số lượng tốt được bảo vệ bởi tốt khác
    """
    protected_count = 0
    for row, col in pawns:
        # Tốt trắng được bảo vệ bởi tốt ở hàng dưới và cột liền kề
        if color == "w":
            protectors = [(row+1, col-1), (row+1, col+1)]
        # Tốt đen được bảo vệ bởi tốt ở hàng trên và cột liền kề
        else:
            protectors = [(row-1, col-1), (row-1, col+1)]
        
        for p_row, p_col in protectors:
            if 0 <= p_row < 8 and 0 <= p_col < 8:
                piece = game_state.board[p_row][p_col]
                if piece == color + "P":
                    protected_count += 1
                    break
    
    return protected_count

def evaluate_king_safety(game_state, is_endgame):
    """
    Đánh giá an toàn của vua
    """
    score = 0
    
    # Trong giai đoạn cuối, vua nên tích cực
    if is_endgame:
        return 0  # Đã tính trong bảng giá trị vị trí
    
    # Kiểm tra an toàn vua trắng
    w_king_row, w_king_col = game_state.white_king_location
    w_king_safety = 0
    
    # Kiểm tra các ô xung quanh vua có quân bảo vệ không
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for d_row, d_col in directions:
        row, col = w_king_row + d_row, w_king_col + d_col
        if 0 <= row < 8 and 0 <= col < 8:
            piece = game_state.board[row][col]
            if piece[0] == 'w':  # Quân trắng bảo vệ
                w_king_safety += 5
    
    # Kiểm tra nhập thành và cấu trúc tốt bảo vệ
    if w_king_col in [0, 1, 2, 6, 7] and w_king_row == 7:  # Vua đã nhập thành
        w_king_safety += 30
        
        # Kiểm tra các tốt bảo vệ vua
        pawn_shield_positions = []
        if w_king_col < 3:  # Nhập thành bên hậu
            pawn_shield_positions = [(6, 0), (6, 1), (6, 2)]
        else:  # Nhập thành bên vua
            pawn_shield_positions = [(6, 5), (6, 6), (6, 7)]
            
        for pos in pawn_shield_positions:
            if game_state.board[pos[0]][pos[1]] == "wP":
                w_king_safety += 10
    
    # Kiểm tra an toàn vua đen (tương tự như vua trắng)
    b_king_row, b_king_col = game_state.black_king_location
    b_king_safety = 0
    
    for d_row, d_col in directions:
        row, col = b_king_row + d_row, b_king_col + d_col
        if 0 <= row < 8 and 0 <= col < 8:
            piece = game_state.board[row][col]
            if piece[0] == 'b':  # Quân đen bảo vệ
                b_king_safety += 5
    
    if b_king_col in [0, 1, 2, 6, 7] and b_king_row == 0:  # Vua đã nhập thành
        b_king_safety += 30
        
        pawn_shield_positions = []
        if b_king_col < 3:  # Nhập thành bên hậu
            pawn_shield_positions = [(1, 0), (1, 1), (1, 2)]
        else:  # Nhập thành bên vua
            pawn_shield_positions = [(1, 5), (1, 6), (1, 7)]
            
        for pos in pawn_shield_positions:
            if game_state.board[pos[0]][pos[1]] == "bP":
                b_king_safety += 10
    
    score += w_king_safety - b_king_safety
    return score

KING_ACTIVITY_ENDGAME_WEIGHT = 10  # Trọng số cho hoạt động của vua trong cuối game

def evaluate_king_activity_endgame(game_state, is_endgame):
    """
    Đánh giá hoạt động của vua trong giai đoạn cuối game
    """
    if not is_endgame:
        return 0
    
    score = 0
    w_king_row, w_king_col = game_state.white_king_location
    b_king_row, b_king_col = game_state.black_king_location
    
    # Khuyến khích vua di chuyển đến trung tâm trong cuối game
    w_king_center_distance = abs(w_king_row - 3.5) + abs(w_king_col - 3.5)
    b_king_center_distance = abs(b_king_row - 3.5) + abs(b_king_col - 3.5)
    
    # Vua càng gần trung tâm càng tốt trong cuối game
    score += (4 - w_king_center_distance) * KING_ACTIVITY_ENDGAME_WEIGHT
    score -= (4 - b_king_center_distance) * KING_ACTIVITY_ENDGAME_WEIGHT
    
    return score