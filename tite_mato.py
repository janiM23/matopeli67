# to run 'pip install PySide6' is required

import sys
import random
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMenu 
from PySide6.QtGui import QPainter, QPen, QBrush, QFont
from PySide6.QtCore import Qt, QTimer

# Constants
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15

class SnakeGame(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)

        # starting game by button
        self.game_started = False
        self.init_screen()

    def keyPressEvent(self, event):
        key = event.key()
        if not self.game_started:
            if key == event.key():
                self.game_started = True
                self.scene().clear()
                self.start_game()

        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            # Only update direction if the new direction is not opposite to the current direction
            if key == Qt.Key_Left and self.direction != Qt.Key_Right:
                self.direction = key
            elif key == Qt.Key_Right and self.direction != Qt.Key_Left:
                self.direction = key
            elif key == Qt.Key_Up and self.direction != Qt.Key_Down:
                self.direction = key
            elif key == Qt.Key_Down and self.direction != Qt.Key_Up:
                self.direction = key
    
    def update_game(self):
        head_x, head_y = self.snake[0]

        if self.direction == Qt.Key_Left:
            new_head = (head_x - 1, head_y)
        elif self.direction == Qt.Key_Right:
            new_head = (head_x + 1, head_y)
        elif self.direction == Qt.Key_Up:
            new_head = (head_x, head_y - 1)
        elif self.direction == Qt.Key_Down:
            new_head = (head_x, head_y + 1)

        #pdate_game metodiin suuntien tarkistuksen jälkeen
        # board limits

        if new_head in self.snake or not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
            self.timer.stop()
            return

        self.snake.insert(0, new_head)
  
        if new_head == self.food:
            self.food = self.spawn_food()
            self.score += 1
        else:
            self.snake.pop()   

        self.print_game()


    def print_game(self):
        self.scene().clear()

        for segment in self.snake:
            x, y = segment
            self.scene().addRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.black), QBrush(Qt.black))
            self.scene().addText(f"Score: {self.score}", QFont("Arial", 12)) 

    def start_game(self):
        self.direction = Qt.Key_Right
        self.snake = [(5, 5), (5, 6), (5, 7)]

        self.timer.start(300)
        self.score = 0

    # Aloitusruudun metodi
    def init_screen(self):
        start_text = self.scene().addText("Press any key to start", QFont("Arial", 18))
        text_width = start_text.boundingRect().width()
        text_x = (self.width() - text_width) / 5
        start_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2)

    # Aloitusruudun metodi
    def init_screen(self):
        start_text = self.scene().addText("Press any key to start", QFont("Arial", 18))
        text_width = start_text.boundingRect().width()
        text_x = (self.width() - text_width) / 5
        start_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2)
        
    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return x, y
        
            fx, fy = self.food
            self.scene().addRect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.black), QBrush(Qt.red))
def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()