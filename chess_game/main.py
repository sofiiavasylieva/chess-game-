from fastapi import FastAPI, HTTPException
from models import Piece, King, Rook, Knight, Queen, Pawn, Bishop
from database import Database

app = FastAPI()
db = Database('game_history.db')


class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]

    def place_piece(self, piece, position):
        self.grid[position[0]][position[1]] = piece

    def move_piece(self, start, end):
        piece = self.grid[start[0]][start[1]]
        if piece is None:
            return False
        if not piece.validate_move(start, end, self):
            return False
        # Additional logic for move validation (e.g., obstacle checking)
        # This can be implemented based on the specific game rules
        # For simplicity, we are not implementing it here
        self.grid[end[0]][end[1]] = piece
        self.grid[start[0]][start[1]] = None
        return True


board = Board()


@app.post("/start_game")
def start_game():
    return {"message": "Game started."}


@app.post("/move")
def move(player: str, position_from: list[int], position_to: list[int]):
    piece = board.grid[position_from[0]][position_from[1]]
    if piece is None:
        raise HTTPException(
            status_code=400, detail="No piece at the starting position.")
    if piece.color != player:
        raise HTTPException(
            status_code=400, detail="You can't move opponent's piece.")
    if not board.move_piece(position_from, position_to):
        raise HTTPException(status_code=400, detail="Invalid move.")
    db.insert_move(player, position_from, position_to)
    return {"message": "Move successful."}


@app.post("/end_game")
def end_game():
    db.close()
    return {"message": "Game ended."}


@app.get("/get_board")
def get_board():
    return {"board": board.grid}
