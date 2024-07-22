import tkinter as tk
import time
import random

animationLength = 16

FALL = -2
DRAG = -1
WALK_R = 0
IDLE = 1
WALK_L = 2
SLEEP = 3
CUTE = 4
POOP = 5
LAND = 6
EAT = 7
SCRATCH = 8

class cat():
    def __init__(self):
        self.window = tk.Tk()
        self.MOVEMENT_SPEED = 3

        self.movement_choices = [WALK_R, IDLE, WALK_L, SLEEP, CUTE, POOP]
        self.movement_probability = [0.2, 0.1, 0.2, 0.4, 0, 0.1]
        self.movement_probability_left = [0.4, 0.3, 0, 0.3, 0, 0]
        self.movement_probability_right = [0, 0.1, 0.3, 0.1, 0.5, 0]

        self.sleep_length_choices = [1, 2, 3]
        self.sleep_length_probability = [0.2, 0.3, 0.5]
        self.curr_sleep_length = -1
        self.start_sleep = True
        self.end_sleep = False

        self.walking_right = self.LoadImages("walk_right", 8)
        self.walking_left = self.LoadImages("walk_left", 8)
        self.sleep_out = self.LoadImages("sleep_out", 4)
        self.sleep_in = self.LoadImages("sleep_in", 4)
        self.deep_sleep = self.LoadImages("deep_sleep", 8)
        self.act_cute = self.LoadImages("cute", 16)
        self.idle = self.LoadImages("idle", 16)
        self.landing = self.LoadImages("landing", 16)
        self.pooping = self.LoadImages("pooping", 16)
        self.eating = self.LoadImages("eating", 16)
        self.scratching = self.LoadImages("scratching", 4)

        self.pick_up = tk.PhotoImage(file='assets/pick-up.png')
        self.falling = tk.PhotoImage(file='assets/falling.png')

        self.falling_speed = 1

        self.frame_index = 0
        self.img = self.walking_right[self.frame_index]

        self.movement_type = WALK_R

        # timestamp to check whether to advance frame
        self.timestamp = time.time()

        # set focus highlight to black when the window does not have focus
        self.window.config(highlightbackground='black')
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', 'black')
        self.label = tk.Label(self.window, bd=0, bg='black')
        self.label.configure(image=self.img)
        self.label.pack()

        self.x = 0
        self.y = 760
        self.window.geometry('64x64+{x}+0'.format(x=str(self.x)))

        self.window.bind('<Button-1>', self.SaveLastClickPos)
        self.window.bind('<B1-Motion>', self.Dragging)
        self.window.bind('<ButtonRelease-1>', self.Fall)
        self.window.bind('<Button-3>', self.Feed)
        self.window.bind('<Motion>', self.Scratch)

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.Update)
        self.window.mainloop()

    def LoadImages(self, directory, num):
        list = []

        for i in range(1, int(animationLength / num + 1)):
            for j in range(1, num + 1):
                list.append(tk.PhotoImage(file='assets/' + directory + '/' + str(j)+ '.png'))

        return list

    def SaveLastClickPos(self,event):
        global lastClickX, lastClickY
        lastClickX = event.x
        lastClickY = event.y

    def Dragging(self, event):
        self.x, self.y = event.x - lastClickX + self.window.winfo_x(), event.y - lastClickY + self.window.winfo_y()
        self.window.geometry("+%s+%s" % (self.x, self.y))
        self.movement_type = DRAG
        self.img = self.pick_up

    def Fall(self,event):
        self.y += self.falling_speed
        self.movement_type = FALL
        self.img = self.falling

    def Feed(self, event):
        self.movement_type = EAT

    def Scratch(self, event):
        if self.y==760:
            self.movement_type = SCRATCH

    def Update(self):
        if self.movement_type == DRAG:
            self.img = self.pick_up
        elif self.movement_type == FALL:
            self.img = self.falling
            self.y+=self.falling_speed
            self.falling_speed=self.falling_speed+2

            if (self.y >= 745):
                self.movement_type = 6
                self.falling_speed = 1
        else:
            self.y = 760
            if self.movement_type == WALK_R: # right
                self.x += self.MOVEMENT_SPEED

            if self.movement_type == WALK_L: #left
                self.x -= self.MOVEMENT_SPEED

            if time.time() > self.timestamp + 0.1: # 50 ms
                self.timestamp = time.time()
                self.frame_index = (self.frame_index + 1) % animationLength

                if self.frame_index == 0:

                    if self.movement_type == SLEEP and self.curr_sleep_length > 0:
                        self.curr_sleep_length -= 1
                    elif self.movement_type == SLEEP and self.curr_sleep_length == 0:
                        self.start_sleep = True
                        self.end_sleep = False
                        self.curr_sleep_length = -1
                        self.movement_type = IDLE
                    elif self.movement_type == SLEEP and self.curr_sleep_length == -1:
                        self.curr_sleep_length = random.choices(self.sleep_length_choices, self.sleep_length_probability)[0]
                    elif self.movement_type == POOP:
                        self.movement_type = IDLE
                    elif self.x >= 1470:
                        self.movement_type = random.choices(self.movement_choices, self.movement_probability_right)[0]
                    elif self.x <= 50:
                        self.movement_type = random.choices(self.movement_choices, self.movement_probability_left)[0]
                    else:
                        self.movement_type = random.choices(self.movement_choices, self.movement_probability)[0]

                if self.movement_type == WALK_R:
                    self.img = self.walking_right[self.frame_index]

                elif self.movement_type == IDLE:
                    self.img = self.idle[self.frame_index]

                elif self.movement_type == WALK_L:
                    self.img = self.walking_left[self.frame_index]

                elif self.movement_type == SLEEP:
                    if self.start_sleep:
                        self.img = self.sleep_in[self.frame_index]
                        if self.frame_index == 8:
                            self.start_sleep = False
                            self.end_sleep = True
                            self.frame_index = -1

                    elif self.curr_sleep_length == 0:
                        self.img = self.sleep_out[self.frame_index]
                        if self.frame_index == 8:
                            self.end_sleep = True
                            self.start_sleep = True
                            self.frame_index = -1
                    else:
                        self.img = self.deep_sleep[self.frame_index]

                elif self.movement_type == CUTE:
                    self.img = self.act_cute[self.frame_index]

                elif self.movement_type == POOP:
                    self.img = self.pooping[self.frame_index]
                    if self.frame_index > 8:
                        self.x -= self.MOVEMENT_SPEED
                elif self.movement_type == LAND:
                    self.img = self.landing[self.frame_index]
                elif self.movement_type == EAT:
                    self.img = self.eating[self.frame_index]
                elif self.movement_type == SCRATCH:
                    self.img = self.scratching[self.frame_index]

        self.window.geometry('+{x}+{y}'.format(x=str(self.x), y=str(self.y)))  # moves the window @ indicated x value
        self.label.configure(image=self.img)
        self.label.pack()

        self.window.after(60, self.Update)

if __name__ == '__main__':
    cat()