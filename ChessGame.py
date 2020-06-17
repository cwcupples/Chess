import pygame

# set some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DBROWN = (133, 87, 35)
LBROWN = (185, 156, 107)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLUE = (0, 0, 128)
PRIMARY = DBROWN
SECONDARY = LBROWN

# some sizes
SQUARE = 40
size = [SQUARE * 8 + 6, SQUARE * 10 + 6]
screen = pygame.display.set_mode(size)

# start the game
pygame.init()
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

# load the white pieces
wking = pygame.image.load("images/wKing.png")
wqueen = pygame.image.load("images/wQueen.png")
wbishop = pygame.image.load("images/wBishop.png")
wknight = pygame.image.load("images/wKnight.png")
wrook = pygame.image.load("images/wRook.png")
wpawn = pygame.image.load("images/wPawn.png")
# load the black pieces
bking = pygame.image.load("images/bKing.png")
bqueen = pygame.image.load("images/bQueen.png")
bbishop = pygame.image.load("images/bBishop.png")
bknight = pygame.image.load("images/bKnight.png")
brook = pygame.image.load("images/bRook.png")
bpawn = pygame.image.load("images/bPawn.png")
# load smaller black pieces for graveyard
sbking = pygame.image.load("images/bKing_small.png")
sbqueen = pygame.image.load("images/bQueen_small.png")
sbbishop = pygame.image.load("images/bBishop_small.png")
sbknight = pygame.image.load("images/bKnight_small.png")
sbrook = pygame.image.load("images/bRook_small.png")
sbpawn = pygame.image.load("images/bPawn_small.png")
# load smaller white pieces for graveyard
swking = pygame.image.load("images/wKing_small.png")
swqueen = pygame.image.load("images/wQueen_small.png")
swbishop = pygame.image.load("images/wBishop_small.png")
swknight = pygame.image.load("images/wKnight_small.png")
swrook = pygame.image.load("images/wRook_small.png")
swpawn = pygame.image.load("images/wPawn_small.png")


# switch case to easily convert from letters to numbers
def switch(argument):
    switcher = {
        6: "K", 5: "Q", 4: "B", 3: "N", 2: "R", 1: "P",  # Player 1's pieces
        0: ".",  # Empty squares
        -1: "p", -2: "r", -3: "n", -4: "b", -5: "q", -6: "k"  # Player 2's pieces
    }
    return switcher.get(argument)


# switch case to easily store images
def image_switch(argument):
    switcher = {
        6: wking, 5: wqueen, 4: wbishop, 3: wknight, 2: wrook, 1: wpawn,  # Player 1's pieces
        -1: bpawn, -2: brook, -3: bknight, -4: bbishop, -5: bqueen, -6: bking  # Player 2's pieces
    }
    return switcher.get(argument)


# switch for the small images
def small_image_switch(argument):
    switcher = {
        6: swking, 5: swqueen, 4: swbishop, 3: swknight, 2: swrook, 1: swpawn,  # Player 1's pieces
        -1: sbpawn, -2: sbrook, -3: sbknight, -4: sbbishop, -5: sbqueen, -6: sbking  # Player 2's pieces
    }
    return switcher.get(argument)


# make sure that the knight moves correctly
def knight(move, loc):
    row1, col1 = loc
    row2, col2 = move
    if (abs(row1-row2) == 1 and abs(col1-col2) == 2) or (abs(row1-row2) == 2 and abs(col1-col2) == 1):
        return True
    else:
        return False


# checks king move
def king(move, loc):
    if (abs(move[0] - loc[0]) > 1) or (abs(move[1] - loc[1]) > 1):
        return False
    return True


# welcome message to start the game
def welcome():
    screen.fill(BLACK)
    font = pygame.font.Font('freesansbold.ttf', 16)
    text1 = font.render("Welcome to 2 person chess!", True, GREEN, BLUE)
    text2 = font.render("The border tells you who's turn it is", True, GREEN, BLUE)
    text3 = font.render("Click anywhere on the screen to begin", True, GREEN, BLUE)
    textrect1 = text1.get_rect()
    textrect2 = text2.get_rect()
    textrect3 = text3.get_rect()
    textrect1.center = ((SQUARE * 8 + 6) // 2, (SQUARE * 8 + 6) // 2 - 21)
    textrect2.center = ((SQUARE * 8 + 6) // 2, (SQUARE * 8 + 6) // 2)
    textrect3.center = ((SQUARE * 8 + 6) // 2, (SQUARE * 8 + 6) // 2 + 21)
    screen.blit(text1, textrect1)
    screen.blit(text2, textrect2)
    screen.blit(text3, textrect3)
    clock.tick(10)
    pygame.display.update()
    # Loop so game doesn't start until they click
    done = False
    while not done:
        for event in pygame.event.get():  # User did something
            # get row and column of the piece to move
            if event.type == pygame.MOUSEBUTTONDOWN:
                done = True
            if event.type == pygame.QUIT:  # If user clicked close
                quit()


# board class
class ChessBoard:
    # initialize the game board
    def __init__(self):
        self.__a = [2, 1, 0, 0, 0, 0, -1, -2]  # Create game board lists of rows
        self.__b = [3, 1, 0, 0, 0, 0, -1, -3]
        self.__c = [4, 1, 0, 0, 0, 0, -1, -4]
        self.__d = [5, 1, 0, 0, 0, 0, -1, -5]
        self.__e = [6, 1, 0, 0, 0, 0, -1, -6]
        self.__f = [4, 1, 0, 0, 0, 0, -1, -4]
        self.__g = [3, 1, 0, 0, 0, 0, -1, -3]
        self.__h = [2, 1, 0, 0, 0, 0, -1, -2]
        self.__screen = pygame.display.set_mode(size)
        # combine all the lists into one master list
        self.__chess = [self.__a, self.__b, self.__c, self.__d, self.__e, self.__f, self.__g, self.__h]

    # define method to get specific item on board
    def __getitem__(self, tup):
        row, col = tup
        return self.__chess[row][col]

    # define method to set specific item on board
    def __setitem__(self, key, value):
        row, col = key
        self.__chess[row][col] = value

    # print out the board
    def print_board(self):
        for t in range(0, 8):
            if t % 2 == 1:
                x = SECONDARY
                y = PRIMARY
            else:
                x = PRIMARY
                y = SECONDARY
            pygame.draw.rect(screen, x, [3, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(screen, y, [43, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(screen, x, [83, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(screen, y, [123, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(screen, x, [163, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(screen, y, [203, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(screen, x, [243, SQUARE * t + 3, SQUARE, SQUARE])
            pygame.draw.rect(screen, y, [283, SQUARE * t + 3, SQUARE, SQUARE])
            for i in range(0, 8):
                pic = self.__chess[t][i]
                if pic != 0:
                    screen.blit(image_switch(pic), [9 + i * SQUARE, 5 + t * SQUARE])
        pygame.draw.rect(screen, WHITE, [3, 3 + SQUARE * 8, SQUARE * 4, SQUARE * 2])
        pygame.draw.rect(screen, BLACK, [3 + SQUARE * 4, 3 + SQUARE * 8, SQUARE * 4, SQUARE * 2])


# game class
class ChessGame:
    # initialize the game
    def __init__(self):
        self.__board = ChessBoard()
        self.turn = 1  # keeps track of whose turn it is
        self._p1_taken = []  # keeps track of which pieces player 1 has taken
        self._p2_taken = []  # keeps track of which pieces player 2 has taken
        self._winner = None

    # this is how we actually play
    def play_ball(self):
        welcome()
        while not self._winner:
            self.print()
            self.player_turn(self.turn)
            if self.turn == 1:
                # check to see if player 2 king in player 1 graveyard
                if -6 in self._p1_taken:
                    self._winner = "Player 1"
                self.turn += 1
            else:
                # check to see if player 1 king in player 2 graveyard
                if 6 in self._p2_taken:
                    self._winner = "Player 2"
                self.turn -= 1
        self.print()
        self.print_winner()
        while True:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    quit()

    # call this to print the current game board
    def print(self):
        if self.turn == 1:
            screen.fill(WHITE)
        else:
            screen.fill(BLACK)
        self.__board.print_board()
        self.print_taken()
        clock.tick(10)
        pygame.display.update()

    # print all of the pieces taken by each other
    def print_taken(self):
        for i in range(len(self._p1_taken)):
            pic = self._p1_taken[i]
            if i < 6:
                screen.blit(small_image_switch(pic), [5 + i * 26, 325])
            elif i < 12:
                screen.blit(small_image_switch(pic), [5 + (i-6) * 26, 351])
            else:
                screen.blit(small_image_switch(pic), [5 + (i - 12) * 26, 372])
        for i in range(len(self._p2_taken)):
            pic = self._p2_taken[i]
            if i < 6:
                screen.blit(small_image_switch(pic), [165 + i * 26, 325])
            elif i < 12:
                screen.blit(small_image_switch(pic), [165 + (i - 6) * 26, 351])
            else:
                screen.blit(small_image_switch(pic), [165 + (i - 12) * 26, 377])

    # print the winner on the screen
    def print_winner(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(self._winner + " win's!!", True, GREEN, BLUE)
        textrect = text.get_rect()
        textrect.center = ((SQUARE * 8 + 6) // 2, (SQUARE * 8 + 6) // 2)
        screen.blit(text, textrect)
        clock.tick(10)
        pygame.display.update()

    # function that runs the players turn
    def player_turn(self, player):
        while True:
            # get and set the piece to move
            loc_piece_move = self.player_piece(player)
            self.print()
            pygame.draw.rect(screen, GREEN, [loc_piece_move[1] * 40 + 3, loc_piece_move[0] * 40 + 3, SQUARE, SQUARE], 4)
            piece_to_move = self.__board[loc_piece_move[0], loc_piece_move[1]]
            clock.tick(10)
            pygame.display.flip()
            # get and set the place to move
            move_to = self.player_move(loc_piece_move, piece_to_move, player)
            piece_taken = self.__board[move_to[0], move_to[1]]
            # this is here in case the player selects a piece that has no moves
            if move_to != [-1, -1]:
                break
            else:
                pygame.draw.rect(screen, RED, [loc_piece_move[1] * 40 + 3, loc_piece_move[0] * 40 + 3, SQUARE, SQUARE], 4)
                pygame.display.flip()
        # move the pieces
        if piece_to_move == 1 and move_to[1] == 7:
            piece_to_move = 5
        if piece_to_move == -1 and move_to[1] == 0:
            piece_to_move = -5
        self.__board[loc_piece_move[0], loc_piece_move[1]] = 0
        self.__board[move_to[0], move_to[1]] = piece_to_move
        # add a taken piece to the graveyard
        if piece_taken != 0:
            if player == 1:
                self._p1_taken.append(piece_taken)
            else:
                self._p2_taken.append(piece_taken)

    # get the piece that player wants to move
    def player_piece(self, player):
        # Make shift do-while loop top get the piece to move
        while True:
            for event in pygame.event.get():  # User did something
                # get row and column of the piece to move
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    col = (position[0] - 3) // 40
                    row = (position[1] - 3) // 40
                    # make sure that they clicked on the board
                    if row > 7 or row < 0 or col < 0 or col > 7:
                        # do nothing
                        continue
                    else:
                        # store the location of the piece
                        piece_loc = [row, col]
                        # make sure they are selecting one of their pieces
                        if self.__board[row, col] > 0 and player == 1:
                            # return it's location
                            return piece_loc
                        elif self.__board[row, col] < 0 and player == 2:
                            return piece_loc
                if event.type == pygame.QUIT:  # If user clicked close
                    quit()

    # get the place that player 1 wants to move to
    def player_move(self, location, piece, player):
        # Make shift do-while loop top get the piece to move
        while True:
            for event in pygame.event.get():  # User did something
                # get row and column of the piece to move
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    col = (position[0] - 3) // 40
                    row = (position[1] - 3) // 40
                    # make sure that the row and column entered are on the board
                    if row > 7 or row < 0 or col < 0 or col > 7:
                        # do nothing
                        continue
                    else:
                        # store the location of the piece
                        move_loc = [row, col]
                        curr_piece = self.__board[row, col]
                        # make sure they aren't moving to a space occupied by their own piece
                        if (curr_piece > 0 and player == 1) or (curr_piece < 0 and player == 2):
                            return [-1, -1]
                        # make sure the move is valid
                        elif self.move_switch(move_loc, location, piece):
                            # return it's location
                            return move_loc
                        else:
                            return [-1, -1]
                if event.type == pygame.QUIT:  # If user clicked close
                    quit()

    # switch case to determine if projected move is valid
    def move_switch(self, move, loc, piece):
        if abs(piece) == 1:
            # pawn
            return self.pawn(move, loc, piece)
        elif abs(piece) == 2:
            # rook
            return self.rook(move, loc)
        elif abs(piece) == 3:
            # knight
            return knight(move, loc)
        elif abs(piece) == 4:
            # bishop
            return self.bishop(move, loc)
        elif abs(piece) == 5:
            # the queen
            return self.rook(move, loc) or self.bishop(move, loc)
        else:
            # dat boi king
            return king(move, loc)

    # determines if pawn move was legal
    def pawn(self, move, loc, player):
        # move is where we move to, loc is where we move from, piece is the piece that is moving
        # get piece at where we move to, if one exists
        p_move_to = self.__board[move[0], move[1]]
        # this means its player 1
        if player > 0:
            # see if player decided to use the move 2 spaces
            if loc[1] == 1 and move[1] == 3 and move[0] == loc[0] and p_move_to == 0 and self.__board[move[0], 2] == 0:
                return True
        elif player < 0:
            # same as above, but for player 2
            if loc[1] == 6 and move[1] == 4 and move[0] == loc[0] and p_move_to == 0 and self.__board[move[0], 5] == 0:
                return True
        # make sure pawn only moves 1 space at a time
        if move[1] != loc[1] + 1 and player > 0:
            return False
        if move[1] != loc[1] - 1 and player < 0:
            return False
        # pawn can't change rows unless attacking
        elif p_move_to == 0 and move[0] != loc[0]:
            return False
        # if pawn is attacking, can only move one space diagonally
        elif p_move_to != 0:
            if move[0] == loc[0]:
                return False
            if move[0] != loc[0] + 1 and move[0] != loc[0] - 1:
                return False
            else:
                return True
        else:
            return True

    def rook(self, move, loc):
        # player 1 and player 2 are exactly the same
        # can only move in one row or column
        if move[0] != loc[0] and move[1] != loc[1]:
            return False
        elif move[0] == loc[0]:
            # right
            if move[1] > loc[1]:
                for t in range(1, move[1]-loc[1]):
                    if self.__board[move[0], loc[1]+t] != 0:
                        return False
            # left
            if move[1] < loc[1]:
                for t in range(1, loc[1]-move[1]):
                    if self.__board[move[0], loc[1]-t] != 0:
                        return False
        elif move[1] == loc[1]:
            # down
            if move[0] > loc[0]:
                for t in range(1, move[0]-loc[0]):
                    if self.__board[move[0]-t, loc[1]] != 0:
                        return False
            # up
            if move[0] < loc[0]:
                for t in range(1, loc[0] - move[0]):
                    if self.__board[move[0] + t, loc[1]] != 0:
                        return False
        return True

    def bishop(self, move, loc):
        # player 1 and 2 will be the same
        if abs(move[0]-loc[0]) != abs(move[1]-loc[1]):
            return False
        else:
            # down right
            if move[0]-loc[0] > 0 and move[1] - loc[1] > 0:
                for t in range(1, abs(move[0]-loc[0])):
                    if self.__board[loc[0] + t, loc[1] + t] != 0:
                        return False
            # down left
            elif move[0]-loc[0] > 0 > move[1] - loc[1]:
                for t in range(1, abs(move[0] - loc[0])):
                    if self.__board[loc[0] + t, loc[1] - t] != 0:
                        return False
            # up right
            elif move[0] - loc[0] < 0 < move[1] - loc[1]:
                for t in range(1, abs(move[0]-loc[0])):
                    if self.__board[loc[0] - t, loc[1] + t] != 0:
                        return False
            # up left
            else:
                for t in range(1, abs(move[0]-loc[0])):
                    if self.__board[loc[0] - t, loc[1] - t] != 0:
                        return False
            return True


game = ChessGame()
game.play_ball()



