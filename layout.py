EXPECTED_LAYOUT = [
    ["ルーク", "ナイト", "ビショップ", "クイーン", "キング", "ビショップ", "ナイト", "ルーク"],
    ["ポーン"] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    ["ポーン"] * 8,
    ["ルーク", "ナイト", "ビショップ", "クイーン", "キング", "ビショップ", "ナイト", "ルーク"],
]


def check_board_setup(board):
    feedback = []
    for row in range(8):
        for col in range(8):
            expected = EXPECTED_LAYOUT[row][col]
            placed = board[row][col]
            if expected != placed:
                feedback.append(f"{row+1}行{col+1}列：{expected or 'なし'} をおいてね！")
    return feedback if feedback else ["ばっちり！ぜんぶ正しいよ！"]
