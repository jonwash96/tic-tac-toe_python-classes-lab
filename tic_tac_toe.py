# MNT
import re

# FUNC
class Board():
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2
		self.turn = p1

	board = [
		'⋅', '⋅', '⋅',
		'⋅', '⋅', '⋅',
		'⋅', '⋅', '⋅'
	]

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

	turns_taken = 0

	def rh(self, num):
		if self.board[num] == '⋅': return num
		else: return self.board[num]

	def render(self): 
		print("\n", 
			" ——— ——— ———\n",
			f"| {self.rh(0)} | {self.rh(1)} | {self.rh(2)} |\n",
			" ——— ——— ———\n",
			f"| {self.rh(3)} | {self.rh(4)} | {self.rh(5)} |\n",
			" ——— ——— ———\n",
			f"| {self.rh(6)} | {self.rh(7)} | {self.rh(8)} |\n",
			" ——— ——— ———",
			"\n")

	def switch_player(self): 
		self.turn = self.p2 if self.turn == self.p1 else self.p1

	def mark_cell(self, player, cell):
		if not re.search(r'^\d$', cell):
			print("Invalid Input! Enter a number from 0-8 corresponding to an unmarked cell.")
			return False
		if not self.board[int(cell)] == '⋅':
			print("Invalid Input! Cell must not be marked.")
			return False
		self.board[int(cell)] = player
		self.turns_taken +=1
		print(f"Player plays cell {cell}")
		return True
	
	def handle_winner(self, player, combo):
		print("\n\nA WINNER HATH BEEN FOUND!")
		self.render()
		print(f"PLAYER {player} WINS WITH ", combo, "\n")

	def check_status(self, player):
		if self.turns_taken == 9:
			print("It's A draw.")
			return True
		for combo in self.winning_combos:
			if self.board[combo[0]] == player and self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]:
				self.handle_winner(player, combo)
				return True
		return False

	def play(self):
		game_over = False
		while not game_over:
			self.render()
			while True: 
				res = input(f"'{self.turn}'s Turn. Enter 0-8: ")
				if res == 'q': exit()
				if self.mark_cell(self.turn, res): break
			game_over = self.check_status(self.turn)
			self.switch_player()
		return self.reset()
	
	def reset(self):
		self.turns_taken = 0
		for idx,cell in enumerate(self.board):
			self.board[idx] = '⋅'
		self.turn = self.p1
		return


# RUN
def run():
	print("Tic-Tac-Toe")
	print("\n\nInstructions\nType the number of an open cell (LtR, 0-8)\nfollowed by 'Enter' to mark a cell.\nType 'q' at any time to quit.\n")
	print("Board Cells:\n",
		" ——— ——— ———\n",
		"| 0 | 1 | 2 |\n",
		" ——— ——— ———\n",
		"| 3 | 4 | 5 |\n",
		" ——— ——— ———\n",
		"| 6 | 7 | 8 |\n",
		" ——— ——— ———",
	   "\n")
	print("Choose Player Symbols:\n",
	   	" ——————————— ——————— ——————— ——————— ——————— ——————— \n",
		"| 0: custom | 1: ♚♔ | 2: ♛♕ | 3: ♞♘ | 4: ♠︎♧ | 5: ♥︎♡ |\n",
		" ——————————— ——————— ——————— ——————— ——————— ——————— \n",
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
	game = Board(p1, p2)

	while True:
		print("\n\n\nBEGIN NEW GAME\n")
		game.play()
		res = input("Would you like to play again? (y|yes|n|no) ").lower()
		if res == 'q': exit()
		if 'n' in res: break
	return

run()