import time
import threading
from pynput.mouse import Controller, Button, Listener
import random
import customtkinter

TOGGLE_KEY = Button.left
TOGGLE_KEY2 = Button.x2
click_times = []
fakeclicking = False
rightclicking = False
mouse = Controller()
stop_event = threading.Event()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("500x350")
root.title("AutoClicker")

def on_close():
    stop_event.set()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

def clicker():
    global fakeclicking, rightclicking
    while not stop_event.is_set():
        global click_times
        click_times = [t for t in click_times if t > time.time() - 1]
        if len(click_times) >= 4:
            fakeclicking = True
            mouse.click(Button.left, 1)
        time.sleep(random.uniform(0.035, 0.055))
        
        if rightclicking:
            mouse.click(Button.right, 1)
        time.sleep(random.uniform(0.001, 0.004))

def toggle_event(x, y, button, pressed):
    global fakeclicking, rightclicking
    if pressed:
        if button == TOGGLE_KEY:
            if fakeclicking:
                fakeclicking = False
            else:
                click_times.append(time.time())
        elif button == TOGGLE_KEY2:
            rightclicking = not rightclicking

click_thread = threading.Thread(target=clicker)
click_thread.start()

listener = Listener(on_click=toggle_event)
listener.start()

root.mainloop()

listener.stop()
click_thread.join()
