from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def validate_move(self, start, end, board):
        pass


class King(Piece):
    def validate_move(self, start, end, board):
        # King can move one square in any direction
        x_distance = abs(start[0] - end[0])
        y_distance = abs(start[1] - end[1])
        return x_distance <= 1 and y_distance <= 1


class Rook(Piece):
    def validate_move(self, start, end, board):
        # Rook can move horizontally or vertically any number of squares
        return start[0] == end[0] or start[1] == end[1]


class Knight(Piece):
    def validate_move(self, start, end, board):
        # Knight moves in an L shape: two squares in one direction, then one square perpendicular to that
        x_distance = abs(start[0] - end[0])
        y_distance = abs(start[1] - end[1])
        return (x_distance == 2 and y_distance == 1) or (x_distance == 1 and y_distance == 2)


class Bishop(Piece):
    def validate_move(self, start, end, board):
        # Bishop can move diagonally any number of squares
        x_distance = abs(start[0] - end[0])
        y_distance = abs(start[1] - end[1])
        return x_distance == y_distance


class Queen(Piece):
    def validate_move(self, start, end, board):
        # Queen can move horizontally, vertically, or diagonally any number of squares
        return Rook().validate_move(start, end, board) or Bishop().validate_move(start, end, board)


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.initial_row = 1 if color == 'white' else 6

    def validate_move(self, start, end, board):
        # Pawn moves forward one square, but captures diagonally
        direction = 1 if self.color == 'white' else -1
        x_distance = end[0] - start[0]
        y_distance = abs(end[1] - start[1])

        if x_distance == direction and y_distance == 0 and board.grid[end[0]][end[1]] is None:
            return True
        elif x_distance == direction and y_distance == 1 and board.grid[end[0]][end[1]] is not None:
            return True
        elif (x_distance == 2 * direction and y_distance == 0 and
              start[0] == self.initial_row and board.grid[end[0]][end[1]] is None):
            return True
        return False
