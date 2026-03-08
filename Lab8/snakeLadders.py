import tkinter as tk
import random
import time

BG = "#0F172A"
BOARD_LIGHT = "#E2E8F0"
BOARD_DARK = "#CBD5E1"
PLAYER_COLOR = "#EF4444"
AI_COLOR = "#22D3EE"
BTN_COLOR = "#10B981"
TEXT_COLOR = "#E2E8F0"

class SnakeLadderGame:
    def __init__(self):
        self.snakes = {16:6, 47:26, 49:11, 56:53, 62:19,
                       64:60, 87:24, 93:73, 95:75, 98:78}
        self.ladders = {1:38, 4:14, 9:31, 21:42,
                        28:84, 36:44, 51:67, 71:91, 80:100}

class FullGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Snake & Ladder - Full Game Mode")
        self.root.geometry("900x700")
        self.root.configure(bg=BG)

        self.game = SnakeLadderGame()

        self.player_pos = 1
        self.ai_pos = 1
        self.current_turn = "PLAYER"

        self.setup_ui()
        self.draw_board()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=600, height=600,
                                bg="white", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.info_label = tk.Label(self.root, text="Your Turn 🎮",
                                   bg=BG, fg=TEXT_COLOR,
                                   font=("Segoe UI", 14))
        self.info_label.pack()

        self.dice_label = tk.Label(self.root, text="🎲",
                                   bg=BG, fg="white",
                                   font=("Segoe UI", 40))
        self.dice_label.pack(pady=10)

        self.roll_btn = tk.Button(self.root, text="ROLL DICE",
                                  bg=BTN_COLOR, fg="white",
                                  font=("Segoe UI", 12, "bold"),
                                  command=self.roll_dice)
        self.roll_btn.pack(pady=10)

    def draw_board(self):
        size = 60
        for i in range(10):
            for j in range(10):
                x1 = j*size
                y1 = i*size
                x2 = x1+size
                y2 = y1+size

                color = BOARD_LIGHT if (i+j)%2==0 else BOARD_DARK
                self.canvas.create_rectangle(x1,y1,x2,y2,
                                            fill=color, outline="gray")

                num = (9-i)*10 + (j+1)
                self.canvas.create_text(x1+10,y1+15,
                                        text=str(num),
                                        font=("Arial",8))

        # DRAW LADDERS FIRST
        for start, end in self.game.ladders.items():
            self.draw_ladder(start, end)

        # DRAW SNAKES
        for start, end in self.game.snakes.items():
            self.draw_snake(start, end)

        self.player_token = self.canvas.create_oval(0,0,0,0,
                                                    fill=PLAYER_COLOR)
        self.ai_token = self.canvas.create_oval(0,0,0,0,
                                                fill=AI_COLOR)

        self.move_token(self.player_token, self.player_pos)
        self.move_token(self.ai_token, self.ai_pos)

    def draw_ladder(self, start, end):
        x1, y1 = self.get_coords(start)
        x2, y2 = self.get_coords(end)

        # Side rails
        self.canvas.create_line(x1-8, y1, x2-8, y2,
                                width=4, fill="#8B5E3C")
        self.canvas.create_line(x1+8, y1, x2+8, y2,
                                width=4, fill="#8B5E3C")

        # Steps
        steps = 8
        for i in range(steps):
            t = i/steps
            sx = x1 + (x2-x1)*t
            sy = y1 + (y2-y1)*t
            self.canvas.create_line(sx-8, sy, sx+8, sy,
                                    width=3, fill="#A47551")

    def draw_snake(self, start, end):
        x1, y1 = self.get_coords(start)
        x2, y2 = self.get_coords(end)

        mid_x = (x1 + x2) / 2 + 40
        mid_y = (y1 + y2) / 2

        # Shadow
        self.canvas.create_line(
            x1, y1, mid_x, mid_y, x2, y2,
            smooth=True, width=14, fill="#2E7D32"
        )

        # Body
        self.canvas.create_line(
            x1, y1, mid_x, mid_y, x2, y2,
            smooth=True, width=10, fill="#4CAF50"
        )

        # Head
        self.canvas.create_oval(x1-12, y1-12,
                                x1+12, y1+12,
                                fill="#1B5E20")

        # Eyes (white)
        self.canvas.create_oval(x1-6, y1-6,
                                x1-2, y1-2,
                                fill="white")
        self.canvas.create_oval(x1+2, y1-6,
                                x1+6, y1-2,
                                fill="white")

        # Pupils
        self.canvas.create_oval(x1-5, y1-5,
                                x1-3, y1-3,
                                fill="black")
        self.canvas.create_oval(x1+3, y1-5,
                                x1+5, y1-3,
                                fill="black")

        # Tongue
        self.canvas.create_line(x1, y1+8,
                                x1, y1+16,
                                fill="red", width=2)
        
    def glow_effect(self, pos):
        x, y = self.get_coords(pos)

        glow = self.canvas.create_oval(
            x-20, y-20, x+20, y+20,
            outline="#FFEB3B", width=4
        )

        for i in range(5):
            self.canvas.itemconfig(glow, width=4+i)
            self.root.update()
            time.sleep(0.05)

        self.canvas.delete(glow)


    def get_coords(self, pos):
        row = (pos-1)//10
        col = (pos-1)%10
        if row%2==1:
            col = 9-col
        x = col*60+30
        y = (9-row)*60+30
        return x,y

    def move_token(self, token, pos):
        x,y = self.get_coords(pos)
        self.canvas.coords(token, x-10, y-10, x+10, y+10)

    def roll_dice(self):
        if self.current_turn != "PLAYER":
            return

        self.animate_dice()

        dice = random.randint(1,6)
        self.dice_label.config(text=f"🎲 {dice}")

        self.player_pos = self.update_position(self.player_pos, dice, self.player_token)

        self.animate_move(self.player_token, self.player_pos)

        if self.check_win(self.player_pos, "🎉 YOU WIN!"):
            return

        self.current_turn = "AI"
        self.info_label.config(text="AI Thinking 🤖")
        self.root.after(800, self.ai_turn)

    def ai_turn(self):
        self.animate_dice()
        dice = random.randint(1,6)
        self.dice_label.config(text=f"🎲 {dice}")

        self.ai_pos = self.update_position(self.ai_pos, dice, self.ai_token)

        self.animate_move(self.ai_token, self.ai_pos)

        if self.check_win(self.ai_pos, "🤖 AI WINS!"):
            return

        self.current_turn = "PLAYER"
        self.info_label.config(text="Your Turn 🎮")

    def update_position(self, pos, dice, token):
        new_pos = pos + dice
        if new_pos > 100:
            return pos

        # Normal move first
        self.animate_move(token, new_pos)

        # LADDER
        if new_pos in self.game.ladders:
            target = self.game.ladders[new_pos]
            self.animate_special_move(token, new_pos, target, climb=True)
            return target

        # SNAKE
        if new_pos in self.game.snakes:
            target = self.game.snakes[new_pos]
            self.animate_special_move(token, new_pos, target, climb=False)
            return target

        return new_pos

    def animate_special_move(self, token, start_pos, end_pos, climb=True):
        x1, y1 = self.get_coords(start_pos)
        x2, y2 = self.get_coords(end_pos)

        steps = 20

        for i in range(steps):
            t = i / steps

            # Smooth curve for snake
            if not climb:
                mid_x = (x1 + x2) / 2 + 40
                mid_y = (y1 + y2) / 2

                x = (1-t)**2 * x1 + 2*(1-t)*t*mid_x + t**2 * x2
                y = (1-t)**2 * y1 + 2*(1-t)*t*mid_y + t**2 * y2
            else:
                # Straight line for ladder climb
                x = x1 + (x2 - x1) * t
                y = y1 + (y2 - y1) * t

            self.canvas.coords(token, x-10, y-10, x+10, y+10)
            self.root.update()
            time.sleep(0.02)

        # Snap to exact tile
        self.move_token(token, end_pos)

    def animate_dice(self):
        for _ in range(10):
            self.dice_label.config(text=f"🎲 {random.randint(1,6)}")
            self.root.update()
            time.sleep(0.05)

    def animate_move(self, token, target_pos):
        current_coords = self.canvas.coords(token)
        current_pos = self.get_position_from_coords(current_coords)

        step = 1 if target_pos > current_pos else -1

        for pos in range(current_pos+step, target_pos+step, step):
            self.move_token(token, pos)
            self.root.update()
            time.sleep(0.1)

    def get_position_from_coords(self, coords):
        x = (coords[0] + coords[2]) / 2
        y = (coords[1] + coords[3]) / 2
        row = 9 - int(y // 60)
        col = int(x // 60)
        if row % 2 == 1:
            col = 9 - col
        return row*10 + col + 1

    def check_win(self, pos, message):
        if pos == 100:
            self.info_label.config(text=message)
            self.roll_btn.config(state="disabled")
            return True
        return False


# ======================
# RUN
# ======================
if __name__ == "__main__":
    root = tk.Tk()
    app = FullGameGUI(root)
    root.mainloop()
