# MNT
import re

# FUNC
class Board():
	def __init__(self, board_id):
		self.board_id = board_id
		self.board = [
			'⋅', '⋅', '⋅',
			'⋅', '⋅', '⋅',
			'⋅', '⋅', '⋅'
		]
		self.board_winner = None
		self.turns_taken = 0
		self.last_move = None
		self.board_status = 0

	winning_combos = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]

	conv = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')

	def rh(self, num):
		if self.board[num] == '⋅': return num
		else: return self.board[num]

	def render(self): 
		print(f"Board {self.conv[self.board_id]}\n", 
			" ——— ——— ———\n",
			f"| {self.rh(0)} | {self.rh(1)} | {self.rh(2)} |\n",
			" ——— ——— ———\n",
			f"| {self.rh(3)} | {self.rh(4)} | {self.rh(5)} |\n",
			" ——— ——— ———\n",
			f"| {self.rh(6)} | {self.rh(7)} | {self.rh(8)} |\n",
			" ——— ——— ———",
			"\n")

	def mark_cell(self, player, cell):
		if not re.search(r'^\d$', cell):
			print("Invalid Input! Enter a number from 0-8 corresponding to an unmarked cell.")
			return False
		if not self.board[int(cell)] == '⋅':
			print("Invalid Input! Cell must not be marked.")
			return False
		self.board[int(cell)] = player
		self.turns_taken +=1
		self.last_move = int(cell)
		print(f"Player plays cell {cell}")
		return True
	
	def handle_winner(self, player, combo):
		print(f"\n\nBOARD {self.board_id} HAS A WINNER!")
		self.render()
		print(f"PLAYER {player} WINS BOARD {self.board_id} WITH ", combo, "\n")

	def check_status(self, player):
		if self.turns_taken == 9:
			print(f"\n\nBOARD {self.board_id} IS A DRAW!\nThis board is no longer in play.")
			return -1
		for combo in self.winning_combos:
			if self.board[combo[0]] == player and self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]:
				self.handle_winner(player, combo)
				return 1
		return 0

	def play(self, player):
		self.render()
		while True: 
			res = input(f"'{player}'s Turn. Enter 0-8: ")
			if res == 'q': exit()
			if self.mark_cell(player, res): break
		self.board_status = self.check_status(player)
		return [self.last_move, self.board_status]
	
	def reset(self):
		self.turns_taken = 0
		for idx,cell in enumerate(self.board):
			self.board[idx] = '⋅'
		self.turn = self.p1
		return
	
	def __str__(self):
		self.render()
		return str(self.board_id)
	

class MainBoard(Board):
	def __init__(self, p1, p2):
		super().__init__(10)
		self.p1 = p1
		self.p2 = p2
		self.turn = p1
		self.sub_boards = []
		for num in range(0, 9):
			self.sub_boards.append(Board(num))
		self.active_board = None
		self.game_winner = None

	def rh(self, board, cell):
		if self.sub_boards[board].board[cell] == '⋅': 
			return f"{self.conv[board]}{cell}"
		else: return f"{self.sub_boards[board].board[cell]} "

	def rhm(self, board):
		match self.sub_boards[board].board_status:
			case 1: return self.sub_boards[board].board_winner
			case -1: return "&"
			case 0: return "⋅"

	def render(self):
		print(f"Full Board View:\n",
		"⟔====⫧====⫧====✜✜====⫧====⫧====✜✜====⫧====⫧====⋋\n",
		f"| {self.rh(0,0)} | {self.rh(0,1)} | {self.rh(0,2)} || {self.rh(1,0)} | {self.rh(1,1)} | {self.rh(1,2)} || {self.rh(2,0)} | {self.rh(2,1)} | {self.rh(2,2)} |\n",
		"|————✜————✜————||————✜————✜————||————✜————✜————|\n",
		f"| {self.rh(0,3)} | {self.rh(0,4)} | {self.rh(0,5)} || {self.rh(1,3)} | {self.rh(1,1)} | {self.rh(1,4)} || {self.rh(2,3)} | {self.rh(2,4)} | {self.rh(2,5)} |\n",
		"|————✜————✜————||————✜————✜————||————✜————✜————|\n",
		f"| {self.rh(0,6)} | {self.rh(0,7)} | {self.rh(0,8)} || {self.rh(1,6)} | {self.rh(1,7)} | {self.rh(1,8)} || {self.rh(2,6)} | {self.rh(2,7)} | {self.rh(2,8)} |\n",
		"|====⫩====⫩====✜✜====⫩====⫩====✜✜====⫩====⫩====|\n",
		f"| {self.rh(3,0)} | {self.rh(3,1)} | {self.rh(3,2)} || {self.rh(4,0)} | {self.rh(4,1)} | {self.rh(4,2)} || {self.rh(5,0)} | {self.rh(5,1)} | {self.rh(5,2)} |\n",
		"|————✜————✜————||————✜————✜————||————✜————✜————|\n",
		f"| {self.rh(3,3)} | {self.rh(3,4)} | {self.rh(3,5)} || {self.rh(4,3)} | {self.rh(4,4)} | {self.rh(4,5)} || {self.rh(5,3)} | {self.rh(5,4)} | {self.rh(5,5)} |\n",
		"|————✜————✜————||————✜————✜————||————✜————✜————|\n",
		f"| {self.rh(3,6)} | {self.rh(3,7)} | {self.rh(3,8)} || {self.rh(4,6)} | {self.rh(4,7)} | {self.rh(4,8)} || {self.rh(5,6)} | {self.rh(5,7)} | {self.rh(5,8)} |\n",
		"|====⫩====⫩====✜✜====⫩====⫩====✜✜====⫩====⫩====|\n",
		f"| {self.rh(6,0)} | {self.rh(6,1)} | {self.rh(6,2)} || {self.rh(7,0)} | {self.rh(7,1)} | {self.rh(7,2)} || {self.rh(8,0)} | {self.rh(8,1)} | {self.rh(8,2)} |\n",
		"|————✜————✜————||————✜————✜————||————✜————✜————|\n",
		f"| {self.rh(6,3)} | {self.rh(6,4)} | {self.rh(6,5)} || {self.rh(7,3)} | {self.rh(7,4)} | {self.rh(7,5)} || {self.rh(8,3)} | {self.rh(8,4)} | {self.rh(8,5)} |\n",
		"|————✜————✜————||————✜————✜————||————✜————✜————|\n",
		f"| {self.rh(6,6)} | {self.rh(6,7)} | {self.rh(6,8)} || {self.rh(7,6)} | {self.rh(7,1)} | {self.rh(7,8)} || {self.rh(8,6)} | {self.rh(8,1)} | {self.rh(8,8)} |\n",
		"⦜====⫨====⫨====✜✜====⫨====⫨====✜✜====⫨====⫨====⟓\n",
	   "\n")
		return None
	
	def render_mini(self):
		print("Full Board Overview\n", 
			"⟔===⫧===⫧===⋋\n",
			f"| {self.rhm(0)} | {self.rhm(1)} | {self.rhm(2)} |\n",
			"|===⫩===⫩===|\n",
			f"| {self.rhm(3)} | {self.rhm(4)} | {self.rhm(5)} |\n",
			"|===⫩===⫩===|\n",
			f"| {self.rhm(6)} | {self.rhm(7)} | {self.rhm(8)} |\n",
			"⦜===⫨===⫨===⟓\n",
			"\n")
		return None
	
	def switch_player(self): 
		self.turn = self.p2 if self.turn == self.p1 else self.p1
		print(f"\n'{self.turn}'s turn")
		return None
		
	def set_active_board(self, **kwargs):
		self.active_board = self.conv.index(kwargs['letter']) if kwargs.get('letter') else kwargs['num']
		return self.active_board

	def choose_active_board(self):
		while True:
			letter = input("Which Board would you like to play? Select a-i: ").upper()
			if letter == 'Q': exit()
			if letter in self.conv:
				if not self.active_board: self.set_active_board(letter=letter)
				if self.sub_boards[self.active_board].board_status == 0: break
				else: print("Choose an active board that has not been won or tied.")
			else: print("Invalid key pressed!")
		self.set_active_board(letter=letter)
		return self.active_board
	
	def determine_active_board(self, last_move, board_status):
		if board_status == 0:
			return self.set_active_board(num=last_move)
		else: return self.choose_active_board()

	def handle_winner(self, player, combo):
		print("\n\nA WINNER HATH BEEN FOUND!")
		self.render()
		self.render_mini()
		print(f"PLAYER {player} WINS BOARD THE game WITH BOARDS: ", combo, "\n")
		return

	def check_status(self, player):
		count = 8
		for board in self.sub_boards:
			if board.board_status != 0: count -=1
		if count == 0: 
			print(f"\n\nIS A DRAW!\n")
			return True
		for combo in self.winning_combos:
			if self.board[combo[0]] == player and self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]:
				self.handle_winner(player, combo)
				return True
		return False
		
	def play(self):
		self.render()
		print(f"'{self.turn}'s turn")
		self.choose_active_board()
		while not self.game_winner:
			self.render()
			play = self.sub_boards[self.active_board].play(self.turn)
			if self.check_status(self.turn): break
			self.determine_active_board(play[0], play[1])
			self.switch_player()
		return self.reset()
	
	def reset(self):
		self.turns_taken = 0
		self.game_winner = None
		for idx,cell in enumerate(self.board):
			self.board[idx] = '⋅'
		self.turn = self.p1
		self.active_board = None
		for board in self.sub_boards:
			board.reset()
		return
	
	def __str__(self):
		self.render()
		return str(self.game_status)

# RUN
def run():
	print("\nUltimate Tic-Tac-Toe\n")
	print("HOW TO PLAY\n",
	   "- Every turn, you will play a cell in one of the 9 sub-boards.\n",
	   "- The next player must then play their move on the sub-board corresponding\n to the relative position of the cell played on the previous move.\n",
	   "  i.e. Let's say p1 plays 'E2'; p2 must then play on the 'C' board.\n  Then, let's say p2 plays 'C7'; p1 must then play on the 'H' board, etc.\n",
	   "- The goal is to win tic-tac-toe 3-in-a-row on the full-board by\n winning tic-tac-toe 3-in-a-row on each sub-board.\n",
	   "- Any boards that result in a draw do not count towards a win.",
	   "\n")
	print("INSTRUCTIONS\nWhen prompted, type either the number or letter of an open board or cell\n(LtR, a-i/0-8) followed by 'Enter' to mark a cell.\nType 'q' at any time to quit.\n")
	print("Example Full Board View:\n",
		"⟔====⫧====⫧====✜✜====⫧====⫧====✜✜====⫧====⫧====⋋\n",
		"| A0 | A1 | A2 || B0 | B1 | B2 || C0 | C1 | C2 |\n",
		"|————✜————✜————||————✜————✜————||————✜————✜————|\n",
		"| A3 | A4 | A5 || B3 | B4 | B5 || C3 | C4 | C5 |\n",
		"|————✜————✜————||————✜————✜————||————✜————✜————|\n",
		"| A6 | A7 | A8 || B6 | B7 | B8 || C6 | C7 | C8 |\n",
		"|====⫩====⫩====✜✜====⫩====⫩====✜✜====⫩====⫩====|\n",
		"| D0 | D1 | D2 || E0 | E1 | E2 || F0 | F1 | F2 |\n",
		"|————✜————✜————||————✜————✜————||————✜————✜————|\n",
		"| D3 | D4 | D5 || E3 | E4 | E5 || F3 | F4 | F5 |\n",
		"|————✜————✜————||————✜————✜————||————✜————✜————|\n",
		"| D6 | D7 | D8 || E6 | E7 | E8 || F6 | F7 | F8 |\n",
		"|====⫩====⫩====✜✜====⫩====⫩====✜✜====⫩====⫩====|\n",
		"| G0 | G1 | G2 || H0 | H1 | H2 || I0 | I1 | I2 |\n",
		"|————✜————✜————||————✜————✜————||————✜————✜————|\n",
		"| G3 | G4 | G5 || H3 | H4 | H5 || I3 | I4 | I5 |\n",
		"|————✜————✜————||————✜————✜————||————✜————✜————|\n",
		"| G6 | G7 | G8 || H6 | H7 | H8 || I6 | I7 | I8 |\n",
		"⦜====⫨====⫨====✜✜====⫨====⫨====✜✜====⫨====⫨====⟓\n",
	   "\n")
	print("Example Sub-Board View:\n Board Q:\n",
		" ——— ——— ———\n",
		"| 0 | 1 | 2 |\n",
		" ——— ——— ———\n",
		"| 3 | 4 | 5 |\n",
		" ——— ——— ———\n",
		"| 6 | 7 | 8 |\n",
		" ——— ——— ———",
	   "\n")
	
	print("Ready?")
	
	print("\nGAME CONFIG\nChoose Player Symbols:\n",
	   	" ——————————— ——————— ——————— ——————— ——————— ——————— \n",
		"| 0: custom | 1: ♚♔ | 2: ♛♕ | 3: ♞♘ | 4: ♠︎♧ | 5: ♥︎♡ |\n",
		" ——————————— ——————— ——————— ——————— ——————— ——————— ",
	   "\n")
	res = input("Type the corresponding number to choose your symbol-set OR\nPress Enter to start a new game with 'X' & 'O' or q to quit: ").lower()
	match res:
		case 'q': exit()
		case '0': 
			p1 = input("Enter a symbol for p1. (cannot be '⋅')")
			p2 = input("Enter a symbol for p2. (cannot be '⋅')")
		case '1': p1 = '♚'; p2 = '♔'
		case '2': p1 = '♛'; p2 = '♕'
		case '3': p1 = '♞'; p2 = '♘'
		case '4': p1 = '♠︎'; p2 = '♣︎'
		case '5': p1 = '♥︎'; p2 = '♦︎'
		case _: p1 = 'x'; p2 = 'o'

	if p1 == '⋅': return
	game = MainBoard(p1, p2)

	while True:
		print("\n\n\nBEGIN NEW GAME\n")
		game.play()
		res = input("Would you like to play again? (y|yes|n|no) ").lower()
		if res == 'q': exit()
		if 'n' in res: break
	return

run()