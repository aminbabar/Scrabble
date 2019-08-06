"""
 *****************************************************************************
   FILE:  game.py

   AUTHOR: Amin Babar

   ASSIGNMENT: Scrabble

   DATE: 11/29/17

   DESCRIPTION: The game of scrabble with most of the rules implemented. Tiles
   on the board can still be moved after they are placed. This results in an
   error so the players should avoid the movement of tiles. The reset and the
   end turn buttons work fine, but when used along with the challenge word
   button, the game runs into a couple of problems. Double word and letter and
    triple word and letter scores have been implemented. Bingo scoring has also
    been implemented. Green squares tripple letter score, blue squares double
    letter score, red squares double word score and orange squares triple
    word score.

 *****************************************************************************
"""

from cs110graphics_v2 import *
import random


class Game(object):
    """ represents entire game of scrabble """

    def __init__(self, win):
        # creates racks, a bag, and a list for the boardunits
        self._win = win
        self._squares_grid = []
        self._last_tile_clicked = None
        self._bag = Bag(win, self)
        self._rack_p1 = Rack(win, self._bag, self)
        self._rack_p2 = Rack(win, self._bag, self)

        # fills up the racks with 7 tiles each
        self._rack_p1.fill_rack(win, 620)
        self._rack_p2.fill_rack(win, 100)

        # initializes the reset and endturn button. Also sets the first turn
        # as 1
        self._turn = 1
        self._button = Button(win, self)
        self._reset = Reset(win, self)


        self._score_tile = None
        self._score_word = 0
        self._last_bu_clicked = None
        self._p1_score = 0
        self._p2_score = 0

        self._tiles_clicked_p1 = 0
        self._tiles_clicked_p2 = 0

        self._pass = 1

        # displays the score of the players
        self._display_name_1 = Text(win, "Player 2:", 40, (1000, 150))
        self._display_name_1.set_depth(48)
        self._display_name_2 = Text(win, "Player 1:", 40, (1000, 500))
        self._display_name_2.set_depth(48)
        self._display_score_2 = Text(win, str(self._p1_score), 40, (1000, 200))
        self._display_score_1 = Text(win, str(self._p2_score), 40, (1000, 550))
        self._display_score_2.set_depth(48)
        self._display_score_1.set_depth(48)
        win.add(self._display_score_1)
        win.add(self._display_score_2)
        win.add(self._display_name_1)
        win.add(self._display_name_2)

        # hides the racks of the players when its not their turn
        self._hide_score_p2 = Rectangle(win, 400, 50, (660, 100))
        self._hide_score_p2.set_fill_color("navyblue")
        self._hide_score_p2.set_depth(48)
        win.add(self._hide_score_p2)
        self._hide_score_p1 = Rectangle(win, 400, 50, (660, 620))
        self._hide_score_p1.set_fill_color("navyblue")
        self._hide_score_p1.set_depth(48)

        # displays end game graphics
        self._end_game = Rectangle(win, 1050, 600, (600, 350))
        self._end_game.set_depth(48)
        self._end_text = Text(win, "Game Over", 50, (500, 200))
        self._end_text.set_depth(47)
        self._player_win_1 = Text(win, "Player 1 Won!", 50, (500, 350))
        self._player_win_2 = Text(win, "Player 2 Won!", 50, (500, 350))
        self._draw_text = Text(win, "It's a Draw", 50, (500, 350))
        self._player_win_1.set_depth(47)
        self._player_win_2.set_depth(47)
        self._draw_text.set_depth(47)

        self._tiles_placed = []
        self._board_unit_clicked = []

        # open the dictionary and then creates a list containing all the words
        # in the dictionary
        self._dictionary = open("scrabbleDictionary.txt", "r")
        self._word_played = ""
        self._my_dictionary = []
        self._challenge = Challenge(win, self)
        for word in self._dictionary:
            self._my_dictionary.append(word)

        # creates the squares in the board
        for r in range(16):
            row = []
            for c in range(16):
                new_square = Boardunit(win, 30, ((450 + (30 * c)), 150 + (r * 30)),
                                   (r, c), self)
                row.append(new_square)
            self._squares_grid.append(row)

        # activates the center tile
        self._squares_grid[7][7].activate_boardunit()


        # colors squares to orange(triple word score)
        for r in range(len(self._squares_grid)):
            if r == 0 or r == 7 or r == 14:
                for c in range(len(self._squares_grid[0])):
                    if c == 0 or c == 7 or c == 14:
                        self._squares_grid[r][c].coloring("orange")

        # colors squares to blue (double letter score)
        for r in range(len(self._squares_grid)):
            if r == 0 or r == 7 or r == 14:
                for c in range(len(self._squares_grid[0])):
                    if c == 3 or c == 11:
                        self._squares_grid[r][c].coloring("skyblue")
            if r == 2 or r == 12:
                for c in range(len(self._squares_grid[0])):
                    if c == 6 or c == 8:
                        self._squares_grid[r][c].coloring("skyblue")
            if r == 3 or r == 11:
                for c in range(len(self._squares_grid[0])):
                    if c == 0 or c == 7 or r == 14:
                        self._squares_grid[r][c].coloring("skyblue")
            if r == 6 or r == 8:
                for c in range(len(self._squares_grid[0])):
                    if c == 2 or c == 6 or c == 8 or c == 12:
                        self._squares_grid[r][c].coloring("skyblue")

        # colors squares to green (tripple letter score)
        for r in range(len(self._squares_grid)):
            if r == 5 or r == 9:
                for c in range(len(self._squares_grid[0])):
                    if c == 1 or c == 5 or c == 9 or c == 13:
                        self._squares_grid[r][c].coloring("green")
            if r == 1 or r == 13:
                for c in range(len(self._squares_grid[0])):
                    if c == 5 or c == 9:
                        self._squares_grid[r][c].coloring("green")

        # colors squares to red (double word score)
        for r in range(4):
            self._squares_grid[r + 1][r + 1].coloring("red")
            self._squares_grid[13 - r][13 - r].coloring("red")
            self._squares_grid[13 - r][r + 1].coloring("red")
            self._squares_grid[r + 1][13 - r].coloring("red")
        self._squares_grid[7][7].coloring("red")

        # corrects for the scoring error by removing the additional row and
        # column created at the end of the board
        for i in range(16):
            self._squares_grid[i][15].remove_body()

        for i in range(16):
            self._squares_grid[15][i].remove_body()

    # saves the last tile clicked to the game class
    def set_tile_clicked(self, tile_clicked):
        self._last_tile_clicked = tile_clicked

    # returns the value of the last tile clicked
    def return_tile_clicked(self):
        return self._last_tile_clicked

    # changes turns from player 1 to player 2 or vice versa. Also, fills up the
    # rack for the player who's about to play
    def change_turn(self):
        if self._turn == 1:
            self._turn = 2
        else:
            self._turn = 1
        if self._turn == 1:
            self._rack_p1.fill_rack(self._win, 620)
        else:
            self._rack_p2.fill_rack(self._win, 100)

    # returns the value 1 or 2 of the turn being played
    def get_turn(self):
        return self._turn

    # returns the rack class of the current player
    def get_rack(self):
        if self._turn == 1 or self._turn == 0:
            return self._rack_p1
        else:
            return self._rack_p2

    # reverses the word played by the player. Accounts for the error in the 
    # method used to get the word 
    def reverse_string(self):
        reverse = ""
        for letter in self._word_played:
            reverse = letter + reverse
        self._word_played = reverse

    # resets the last word played
    def reset_word_played(self):
        self._word_played = ""

# checks whether or not the word played is in the dictionary. If it is, then it
# continues with game, otherwise, it resets the last word played, returns tiles
# on board to the rack and resets the board units the tiles were placed on
    def check_word(self):
        for word in self._my_dictionary:
            if str(word.upper()[:-1]) == str(self._word_played.upper()):
                self.number_tiles_clicked()
                self.scoring()
                return
        else:
            self.reset_tiles()
            self.reset_word_played()
            self.reset_board_units_list()
            self.empty_tiles_placed_list()
            self.empty_board_units_list()


    # returns the last active boardunit clicked by the player
    def get_bu_clicked(self, bu_clicked):
        self._last_bu_clicked = bu_clicked

    # creates a list for the boardunits clicked on by the player
    def board_units_clicked(self, boardunitclicked):
        self._board_unit_clicked.append(boardunitclicked)

    # resets the boardunits used by the player
    def reset_board_units_list(self):
        for items in self._board_unit_clicked:
            items.reset_boardunit()

    # empties the list for the board units clicked on by the player
    def empty_board_units_list(self):
        self._board_unit_clicked = []



    # activates the tiles on the board as the player continues to play. 4 tiles 
    # surounding the tile played are activated so another tile can be placed
    def activate_surrounding_tiles(self, r, c):
        self._squares_grid[r + 1][c].activate_boardunit()
        self._squares_grid[r - 1][c].activate_boardunit()
        self._squares_grid[r][c + 1].activate_boardunit()
        self._squares_grid[r][c - 1].activate_boardunit()


    # gets the score of the last tile clicked by the player on the rack
    def score_tile(self):
        self._score_tile = self._last_tile_clicked.get_tile_score()

    # returns the value of the last tile clicked by the player
    def get_score_tile(self):
        return self._score_tile

    # finds out the last word played by the player
    def word_played(self):
        self._word_played = ""

        row = self._last_bu_clicked.get_id_num()[0]
        column = self._last_bu_clicked.get_id_num()[1]

        reverse_word = False

        for i in range(15):
            if self._squares_grid[row + i][column].get_tile_letter() is not None:
                self._word_played += self._squares_grid[row + i][column].get_tile_letter()
            else:
                break

        for i in range(1, 15):
            if self._squares_grid[row - i][column].get_tile_letter() is not None:
                self._word_played += self._squares_grid[row - i][column].get_tile_letter()
                reverse_word = True

        for i in range(1, 15):
            if self._squares_grid[row][column + i].get_tile_letter() is not None:
                self._word_played += self._squares_grid[row][column + i].get_tile_letter()
            else:
                break

        for i in range(1, 15):
            if self._squares_grid[row][column - i].get_tile_letter() is not None:
                self._word_played += self._squares_grid[row][column - i].get_tile_letter()
                reverse_word = True
            else:
                break

        # corrects for error with finding the word
        if reverse_word is True:
            self.reverse_string()

    # scores the last word word played. Goes in all directions from the last
    # boardunit clicked. It breaks if the boardunit in that direction has
    # a score value of none. 
    def score_word(self):
        row = self._last_bu_clicked.get_id_num()[0]
        column = self._last_bu_clicked.get_id_num()[1]
        reverse_word = False
        self._score_word = 0

        # The following 4 for loops determine whether or not the letter score
        # schould be trippled or doubled and then they score the word played
        # accordingly
        for i in range(15):
            if self._squares_grid[row + i][column].get_premium_letter() is not 0:
                self._score_word += self._squares_grid[row + i][column].get_premium_letter()
                self._squares_grid[row + i][column].reset_premium_letter()
            elif self._squares_grid[row + i][column].get_tile_score() is not None:
                self._score_word += self._squares_grid[row + i][column].get_tile_score()
            else:
                break

        for i in range(1, 15):
            if self._squares_grid[row - i][column].get_premium_letter() is not 0:
                self._score_word += self._squares_grid[row - i][column].get_premium_letter()
                self._squares_grid[row - i][column].reset_premium_letter()
            elif self._squares_grid[row - i][column].get_tile_score() is not None:
                self._score_word += self._squares_grid[row - i][column].get_tile_score()
            else:
                break

        for i in range(1, 15):
            if self._squares_grid[row][column + i].get_premium_letter() is not 0:
                self._score_word += self._squares_grid[row][column + i].get_premium_letter()
                self._squares_grid[row][column + i].reset_premium_letter()
                self._word_played += self._squares_grid[row][column + i].get_tile_letter()
            elif self._squares_grid[row][column + i].get_tile_score() is not None:
                self._score_word += self._squares_grid[row][column + i].get_tile_score()
            else:
                break

        for i in range(1, 15):
            if self._squares_grid[row][column - i].get_premium_letter() is not 0:
                self._score_word += self._squares_grid[row][column - i].get_premium_letter()
                self._squares_grid[row][column - i].reset_premium_letter()
            elif self._squares_grid[row][column - i].get_tile_score() is not None:
                self._score_word += self._squares_grid[row][column - i].get_tile_score()
            else:
                break

        # the following four for loops go over the word currently played
        # and decides whehter or not the word score needs to be doubled or
        # trippled
        for i in range(15):
            if self._squares_grid[row + i][column].get_tile_score() is not None:
                self._squares_grid[row + i][column].premium_word()
            else:
                break

        for i in range(1, 15):
            if self._squares_grid[row - i][column].get_tile_score() is not None:
                self._squares_grid[row - i][column].premium_word()
            else:
                break

        for i in range(1, 15):
            if self._squares_grid[row][column + i].get_tile_score() is not None:
                self._squares_grid[row][column + i].premium_word()
            else:
                break

        for i in range(1, 15):
            if self._squares_grid[row][column - i].get_tile_score() is not None:
                self._squares_grid[row][column - i].premium_word()
            else:
                break

        # bingo scoring: if all 7 tiles are played at once, the player gets
        # an additional socre of 50 points
        if self._turn == 1:
            if len(self._bag.get_bag_list()) != 0 and len(self._rack_p1.get_rack_list()) == 0:
                self._score_word += 50
        else:
            if len(self._bag.get_bag_list()) != 0 and len(self._rack_p2.get_rack_list()) == 0:
                self._score_word += 50

    # awards the score of the last word played to the player who just finished
    # their turn
    def score_players(self):
        if self._turn == 1:
            self._p1_score += self._score_word
            self._score_word = 0
        else:
            self._p2_score += self._score_word
            self._score_word = 0

    # diplays the score of both the players on the screen
    def display_score(self, win):
        win.remove(self._display_score_1)
        win.remove(self._display_score_2)
        self._display_score_2 = Text(win, str(self._p2_score), 40, (1000, 200))
        self._display_score_1 = Text(win, str(self._p1_score), 40, (1000, 550))

        win.add(self._display_score_1)
        win.add(self._display_score_2)

    # changes the score of the word based on the multiple. If tile placed on red
    # the word score is doubled, if tile placed on orange, the word score is 
    # trippled
    def change_score_word(self, multiple):
        self._score_word *= multiple

    # calculates the total number of tiles clicked for each turn
    def number_tiles_clicked(self):
        tiles_p1 = 0
        tiles_p2 = 0

        if self._turn == 1:
            for r in range(15):
                for c in range(15):
                    if self._squares_grid[r][c].get_tile_score() is not None:
                        tiles_p1 += 1
        else:
            if self._turn == 2:
                for r in range(15):
                    for c in range(15):
                        if self._squares_grid[r][c].get_tile_score() is not None:
                            tiles_p2 += 1
        if tiles_p1 != 0:
            self._tiles_clicked_p1 = tiles_p1
        elif tiles_p2 != 0:
            self._tiles_clicked_p2 = tiles_p2

    # returns true if the total number of tiles clicked differs between the two
    # turns, otherwise returns false
    def turn_check(self):
        if self._tiles_clicked_p1 != self._tiles_clicked_p2:
            return True
        else:
            return False

    # only counts the score of the last word played when there is a difference
    # between the tiles played in between the 2 turns. This ensures that the
    # score for a single word is not added multiple times when the player passes
    # his or her turn. If there is a difference between the tiles clicked, the
    # value of pass turn is reset
    def scoring(self):
        if self.turn_check() is True:
            self.score_word()
            self.score_players()
            self._pass = 0

    # hides the rack of the player who's not playing
    def hide_score(self):
        if self._turn == 1:
            self._win.remove(self._hide_score_p1)
            self._win.add(self._hide_score_p2)
        else:
            self._win.add(self._hide_score_p1)
            self._win.remove(self._hide_score_p2)

    # adds 1 to the variable self._pass
    def pass_turn(self):
        self._pass += 1

    # if both the players pass the turn consecutively twice, the total score is
    # calculated by subtracting the value of the tiles on the rack from the total score for both the players
    # Determines the winner based on the score. Also adds graphical objects for
    # the end of the game to the window
    def end_game(self):
        p1_score = self._p1_score
        p2_score = self._p2_score

        if self._pass >= 5:
            # If the player uses all his tiles, the value
            # of the other players tiles is awarded to him.
            if self._rack_p1.score_list() == 0:
                self._p1_score += self._rack_p2.score_list()
            elif self._rack_p2.score_list() == 0:
                self._p2_score += self._rack_p1.score_list()
            else:
                self._p1_score -= self._rack_p1.score_list()
                self._p2_score -= self._rack_p2.score_list()

            if self._p1_score > self._p2_score:
                self._win.add(self._player_win_1)
            elif self._p1_score < self._p2_score:
                self._win.add(self._player_win_2)
            elif self._p1_score == self._p2_score:
                if p1_score > p2_score:
                    self._win.add(sef._player_win_1)
                elif p1_score < p2_score:
                    self._win.add(self._player_win_2)
                else:
                    self._win.add(self._draw_text)

            self._win.remove(self._display_score_1)
            self._win.remove(self._display_score_2)
            self._win.add(self._display_score_1)
            self._win.add(self._display_score_2)
            self._win.add(self._end_text)

    # creates a list for the tiles placed by the player in their turn
    def tiles_placed(self, tile):
        self._tiles_placed.append(tile)

    # empties the list of tiles played for the turn
    def empty_tiles_placed_list(self):
        self._tiles_placed = []

    # allows the player to reset his tiles. If the player clicks on the reset
    # button, the tiles placed on the board in their turn go back to the rack
    def reset_tiles(self):
        if self._turn == 1:
            for tiles in self._tiles_placed:
                self._rack_p1.get_rack_list().append(tiles)
                self._rack_p1.display_reset_tiles(self._win, 620)
                self._tiles_placed = []
        else:
            for tiles in self._tiles_placed:
                self._rack_p2.get_rack_list().append(tiles)
                self._rack_p2.display_reset_tiles(self._win, 100)
                self._tiles_placed = []


class Tile(EventHandler):
    """represents an individual tile in the game"""
    def __init__(self, win, letter, score, length, center, game):

        EventHandler.__init__(self)

        self._letter = letter
        self._score = score
        self._length = length
        self._center = center
        self._body = Square(win, length, center)
        self._body.set_fill_color("beige")
        self._text = Text(win, letter)
        self._texts = Text(win, "      " + str(score), 8)
        self._text.set_depth(49)
        self._texts.set_depth(49)
        self._body.add_handler(self)
        self._text.add_handler(self)
        self._texts.add_handler(self)
        self._game = game

    # changes the center of the tile. Also moves the graphical opbject for the
    # tile
    def change_center_tile(self, center):
        self._center = center
        self._body.move_to(center)
        self._text.move_to(center)
        self._texts.move_to(center)

    def handle_mouse_release(self, _):
        # assigns the last tile clicked to a variable in game class
        self._game.set_tile_clicked(self)
    # assigns the score value of the last tile clicked to a variable in game
        # class
        self._game.score_tile()

    # returns the value of the letter on the tile
    def get_letter(self):
        return self._letter

    # displays and moves the the tile to a given center
    def display_tile(self, win, center):
        self._center = center
        self._body.move_to(center)
        self._text.move_to(center)
        self._texts.move_to(center)
        win.add(self._body)
        win.add(self._text)
        win.add(self._texts)

    # returns the score of the tile
    def get_tile_score(self):
        return self._score


class Rack(object):
    """ Represents the racks for each player """
    def __init__(self, win, bag, game):
        self._win = win
        self._rack_list = []
        self._bag = bag
        self._game = game

    # fills up and displays the rack if the tiles on the rack are less than 7
    def fill_rack(self, win, y_coordinate):
        while len(self._rack_list) < 7:
            self._rack_list.append(self._bag.get_tile())

        for i in range(len(self._rack_list)):
            self._rack_list[i].display_tile(win, ((550 + (30 * i)), y_coordinate))

    # displays the tiles that are sent back to the rack once the reset button
    # is clicked on
    def display_reset_tiles(self, win, y_coordinate):
        for i in range(len(self._rack_list)):
            self._rack_list[i].display_tile(win, ((550 + (30 * i)), y_coordinate))

    # removes a given tile from the rack list
    def remove_tile(self, tile):
        self._rack_list.remove(tile)

    # returns the rack list
    def get_rack_list(self):
        return self._rack_list

    # calculates the total score of the tiles on the rack. Used at the end of
    # the game
    def score_list(self):
        rack_score = 0
        for tile in self._rack_list:
            rack_score += tile.get_tile_score()

        return rack_score


class Boardunit(EventHandler):
    """ Represesnts the small square units on the scrabble board """

    def __init__(self, win, length, center, id_num, game):

        EventHandler.__init__(self)

        self._win = win
        self._id_num = id_num
        self._length = length
        self._center = center
        self._body = Square(win, length, center)
        win.add(self._body)
        self._body.add_handler(self)
        self._game = game
        self._active = False

        # the score value of the tile placed on the boardunit
        self._tile_score = None

        self._premium_letter = 0
        self._premium_word_use = False
        self._tile_letter = None

    def handle_mouse_release(self, _):

        if self._active:
            # last tile clicked by the player is returned
            tile = self._game.return_tile_clicked()
            # the center of the last tile clicked by the player is changed to
            # the center of the boardunit
            tile.change_center_tile(self._center)
            # the tile placed on the boardunit is reomoved from the rack list
            # in the game class
            self._game.get_rack().remove_tile(tile)
            # tiles surrounding the boardunit clicked are activated
            self._game.activate_surrounding_tiles(self._id_num[0], self._id_num[1])
            # the score of the tile placed is saved within the boardunit
            self._tile_score = self._game.get_score_tile()
            # the boardunit last clicked (current one) by the player is
            # returned to the game class
            self._game.get_bu_clicked(self)
            # the tripple letter and the double letter scores are applied
            self.premium_letter()
            # the tile placed on the boardunit is added to the tiles played for
            # the turn list
            self._game.tiles_placed(self._game.return_tile_clicked())
            # assigns the letter of the tile placed to a variable within the
            # boardunit
            self.add_tile_letter()
            # the boardunit is added to a list of boardunits clicked for the
            # current turn in the game class
            self._game.board_units_clicked(self)

    # colors the boardunit to the input color
    def coloring(self, color):
        self._body.set_fill_color(color)

    # returns the value of the tile score that was placed on the boardunit
    def get_tile_score(self):
        return self._tile_score

    def get_premium_letter(self):
        return self._premium_letter

    # activates the boardunit by changing the active status of the tile to
    # true
    def activate_boardunit(self):
        if self._active is False:
            self._active = True

    # returns the ID number of the tile
    def get_id_num(self):
        return self._id_num

    # multiplies the letter score of the score of the tile placed by 2 if the
    # color is skyblue and with 3 if the color is green and assigns the new
    # score to a new variable self._premium_letter
    def premium_letter(self):
        if self._body.get_fill_color() == "skyblue":
            self._premium_letter = 2 * self._tile_score
        elif self._body.get_fill_color() == "green":
            self._premium_letter = 3 * self._tile_score

    # resets the value of self._premium_letter. This ensures that the triple
    # letter and the double letter scores are counted for only once
    def reset_premium_letter(self):
        self._premium_letter = 0

    # doubles the word score if the word is places on red and triples the
    # word score if the word is placed on orange. Once used, the status turns
    # to true so that cannot be used again
    def premium_word(self):
        if self._body.get_fill_color() == "red" and not self._premium_word_use:
            self._game.change_score_word(2)
            self._premium_word_use = True
        elif self._body.get_fill_color() == "orange" and not self._premium_word_use:
            self._game.change_score_word(3)
            self._premium_word_use = True

    # removes the graphical body from the window
    def remove_body(self):
        self._win.remove(self._body)

    # assigns the letter of the tile placed to a variable within the boardunit
    # class
    def add_tile_letter(self):
        self._tile_letter = self._game.return_tile_clicked().get_letter()

    # returns the letter of the tile placed on the boardunit
    def get_tile_letter(self):
        return self._tile_letter

    # resets the board unit by assigning the value none to the letter and score
    # variable within the board unit class
    def reset_boardunit(self):
        self._tile_letter = None
        self._tile_score = None


class Button(EventHandler):
    """ This is the end turn button. All the required steps at the end of a
    turn are in this class"""

    def __init__(self, win, game):

        EventHandler.__init__(self)

        self._win = win
        self._body = Rectangle(win, 200, 100, (200, 200))
        self._body.set_fill_color("orange")
        self._text = Text(win, "End Turn", 36)
        self._text.set_depth(49)
        win.add(self._body)
        win.add(self._text)
        self._game = game

        self._body.add_handler(self)
        self._text.add_handler(self)

    def handle_mouse_release(self, _):
        # finds out the number of total tiles placed on the board. If the number
        # of total tiles placed on the board is similar to the last turn, the
        # last played word is not scored multiple times for the players
        self._game.number_tiles_clicked()
        # if the number of total tiles placed on the baord are different
        # compared to the last turn, the word is scored and the score of the
        # word is added to the current players score. If the scoring is done,
        # the pass variable is also reset to 0
        self._game.scoring()
        # the turn is changed and the rack for the current player, if less than
        # 7, is filled
        self._game.change_turn()
        # the score for both the players is displayed on the window
        self._game.display_score(self._win)
        # the rack of the other player is hidden with a navyblue rectangle
        self._game.hide_score()
        # 1 is added to the variable pass.
        self._game.pass_turn()
        # If the variable pass exceeds the variable pass by 4,
        # which happens when the players dont score a word in their turn, the
        # end game function determines a winner, and calculates the end scoring
        # as appropriate
        self._game.end_game()
        # the list of the tiles placed on the board in the current turn is
        # emptied
        self._game.empty_tiles_placed_list()
        # resets the variable _word_played in the game class to ""
        self._game.reset_word_played()
        # empties the list for the board units placed on the board in the
        # last turn
        self._game.empty_board_units_list()


class Reset(EventHandler):
    """ This button resets the last word played by sending the letters used in
    the last turn back to the rack"""

    def __init__(self, win, game):

        EventHandler.__init__(self)

        self._win = win
        self._game = game
        self._body = Rectangle(win, 200, 100, (200, 500))
        self._body.set_fill_color("Red")
        self._text = Text(win, "Reset", 36, (200, 500))
        self._text.set_depth(49)
        win.add(self._body)
        win.add(self._text)
        self._body.add_handler(self)
        self._text.add_handler(self)

    def handle_mouse_release(self, _):
        # appends the tile objects played in the current turn to the rack of
        # the player currently playing
        self._game.reset_tiles()
        # resets the variable word played to ""
        self._game.reset_word_played()
        # resets the variable values of letter and the tile score within the
        # boardunit ro none
        self._game.reset_board_units_list()
        # empties the list for boardunits clicked in the current turn in the
        # game class
        self._game.empty_board_units_list()


class Bag(object):
    """ This class has all the tile objects for the scrabble game"""
    def __init__(self, win, game):

        self._tiles = []

        for _ in range(9):
            tile_A = Tile(win, "A", 1, 30, (0, 0), game)
            self._tiles.append(tile_A)

        for _ in range(2):
            tile_B = Tile(win, "B", 3, 30, (0, 0), game)
            self._tiles.append(tile_B)

        for _ in range(2):
            tile_C = Tile(win, "C", 3, 30, (0, 0), game)
            self._tiles.append(tile_C)

        for _ in range(4):
            tile_D = Tile(win, "D", 2, 30, (0, 0), game)
            self._tiles.append(tile_D)

        for _ in range(12):
            tile_E = Tile(win, "E", 1, 30, (0, 0), game)
            self._tiles.append(tile_E)

        for _ in range(2):
            tile_F = Tile(win, "F", 4, 30, (0, 0), game)
            self._tiles.append(tile_F)

        for _ in range(3):
            tile_G = Tile(win, "G", 2, 30, (0, 0), game)
            self._tiles.append(tile_G)

        for _ in range(2):
            tile_H = Tile(win, "H", 4, 30, (0, 0), game)
            self._tiles.append(tile_H)

        for _ in range(9):
            tile_I = Tile(win, "I", 1, 30, (0, 0), game)
            self._tiles.append(tile_I)

        for _ in range(1):
            tile_J = Tile(win, "J", 8, 30, (0, 0), game)
            self._tiles.append(tile_J)

        for _ in range(1):
            tile_K = Tile(win, "K", 5, 30, (0, 0), game)
            self._tiles.append(tile_K)

        for _ in range(4):
            tile_L = Tile(win, "L", 1, 30, (0, 0), game)
            self._tiles.append(tile_L)

        for _ in range(2):
            tile_M = Tile(win, "M", 3, 30, (0, 0), game)
            self._tiles.append(tile_M)

        for _ in range(6):
            tile_N = Tile(win, "N", 1, 30, (0, 0), game)
            self._tiles.append(tile_N)

        for _ in range(8):
            tile_O = Tile(win, "O", 1, 30, (0, 0), game)
            self._tiles.append(tile_O)

        for _ in range(2):
            tile_P = Tile(win, "P", 3, 30, (0, 0), game)
            self._tiles.append(tile_P)

        for _ in range(1):
            tile_Q = Tile(win, "Q", 10, 30, (0, 0), game)
            self._tiles.append(tile_Q)

        for _ in range(6):
            tile_R = Tile(win, "R", 1, 30, (0, 0), game)
            self._tiles.append(tile_R)

        for _ in range(4):
            tile_S = Tile(win, "S", 1, 30, (0, 0), game)
            self._tiles.append(tile_S)

        for _ in range(6):
            tile_T = Tile(win, "T", 1, 30, (0, 0), game)
            self._tiles.append(tile_T)

        for _ in range(4):
            tile_U = Tile(win, "U", 1, 30, (0, 0), game)
            self._tiles.append(tile_U)

        for _ in range(2):
            tile_V = Tile(win, "V", 4, 30, (0, 0), game)
            self._tiles.append(tile_V)

        for _ in range(2):
            tile_W = Tile(win, "W", 4, 30, (0, 0), game)
            self._tiles.append(tile_W)

        for _ in range(1):
            tile_X = Tile(win, "X", 8, 30, (0, 0), game)
            self._tiles.append(tile_X)

        for _ in range(2):
            tile_Y = Tile(win, "Y", 4, 30, (0, 0), game)
            self._tiles.append(tile_Y)

        for _ in range(1):
            tile_Z = Tile(win, "Z", 10, 30, (0, 0), game)
            self._tiles.append(tile_Z)

        for _ in range(2):
            tile_blank = Tile(win, " ", 0, 30, (0, 0), game)
            self._tiles.append(tile_blank)

    # a tile from the tiles list in the bag class is removed if the length of
    # the list is greater than 0

    def get_tile(self):
        if len(self._tiles) != 0:
            tile = random.choice(self._tiles)
            self._tiles.pop(self._tiles.index(tile))
            return tile

    # returns the list of tiles in the bag class
    def get_bag_list(self):
        return self._tiles


class Challenge(EventHandler):

    def __init__(self, win, game):

        EventHandler.__init__(self)

        self._win = win
        self._game = game
        self._body = Rectangle(win, 200, 100, (200, 350))
        self._body.set_fill_color("Magenta")
        self._text = Text(win, "Challenge", 34, (200, 350))
        self._text.set_depth(49)
        win.add(self._body)
        win.add(self._text)
        self._body.add_handler(self)
        self._text.add_handler(self)

    def handle_mouse_release(self, _):
        # finds the word played in the last turn
        self._game.word_played()
        # checks the word against a dictionary. If correct, it scores the word,
        # otherwise it resets the tiles
        self._game.check_word()
        # the turn is changed and the rack for the current player, if less than
        # 7, is filled
        self._game.change_turn()
        # the score for both the players is displayed on the window
        self._game.display_score(self._win)
        # the rack of the other player is hidden with a navyblue rectangle
        self._game.hide_score()
        # the list of the tiles placed on the board in the current turn is
        # emptied
        self._game.empty_tiles_placed_list()
        # resets the variable _word_played in the game class to ""
        self._game.reset_word_played()
        # empties the list for the board units placed on the board in the
        # last turn
        self._game.empty_board_units_list()


def program(win):

    win.set_width(10000)
    win.set_height(10000)

    scrabble = Game(win)


def main():
    StartGraphicsSystem(program)


if __name__ == "__main__":
    main()
