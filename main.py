from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import messagebox
import string, time, pygame
from random import randint, choice

pygame.mixer.init()

def generate_random_string(length):
    chars = string.ascii_letters
    return ''.join(choice(chars) for _ in range(length)).lower()

def update_time_color(event = None):
    value = time_scale.get()
    ratio = (value - 1) / (120 - 1)

    r = int(255 * (1 - ratio))
    g = int(255 * ratio)
    b = 0

    color = f'#{r:02x}{g:02x}{b:02x}'

    time_scale.config(
        troughcolor = color,
        bg = '#dcf7e0',
        activebackground = color
    )

def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def check_rules(event = None):
    global rules, game_over
    password = entry_password.get()
    length_label.config(text = str(len(password)))

    rules_conditions = [
        sum(1 for c in password if c.isupper()) == random_rules_data[0],
        sum(1 for c in password if c.isdigit()) == random_rules_data[1],
        sum(int(c) for c in password if c.isdigit()) == random_rules_data[2],
        sum(1 for c in password if c in string.punctuation) == random_rules_data[3],
        random_rules_data[4] in password.lower(),
        len(password) == random_rules_data[5],
    ]
    
    rules = dict(zip(rules_text, rules_conditions))

    for rule, label in rule_labels.items():
        label = rule_labels.get(rule)
        frame = rule_frames.get(rule)
        if label and frame:
            if rules[rule]:
                label.config(text = f'✔ {rule}', fg = 'green', bg = '#d4edda')
                frame.config(bg = 'green')
            else:
                label.config(text = f'✖ {rule}', fg = 'red', bg = '#f8d7da')
                frame.config(bg = 'red')

    passed = sum(rules.values())
    progress['value'] = passed

    if all(rules.values()) and not game_over:
        game_over = True
        entry_password.config(state = 'disabled')
        play_sound('win_sound.mp3')
        messagebox.showinfo('the password game', 'you win!!!!!!!')

def start_timer():
    global start_time
    start_time = time.time()
    update_timer_real()

def update_timer_real():
    global time_left, game_over
    if not game_over:
        elapsed = time.time() - start_time
        remaining = max(time_left - elapsed, 0)
        timer_label.config(text = f'thời gian: {remaining:.1f}')
        if remaining > 0:
            root.after(100, update_timer_real)
        else:
            entry_password.config(state = 'disabled')
            game_over = True
            if not all(rules.values()) or not rules:
                play_sound('losing_sound.mp3')
                messagebox.showerror('the password game', 'you lose!!!!!!!')

def start_game(event = None):
    global random_rules_data, rules_text, time_left, game_over, rule_frames
    
    random_rules_data = [
        randint(1, 10),
        randint(10, 20),
        randint(20, 90),
        randint(5, 20),
        generate_random_string(randint(5, 15)),
        None
    ]
    l = random_rules_data[0] + random_rules_data[1] + random_rules_data[2] + len(random_rules_data[4])
    random_rules_data[5] = randint(l, l + 20)
    rules_text = [
        f'Chính xác {random_rules_data[0]} chữ hoa',
        f'Chính xác {random_rules_data[1]} số',
        f'Tổng các số phải bằng {random_rules_data[2]}',
        f'Chính xác {random_rules_data[3]} ký tự đặc biệt',
        f'Chứa từ \'{random_rules_data[4]}\'',
        f'Độ dài password bằng {random_rules_data[5]}'
    ]

    create_rule_widgets()
    
    time_left = float(time_scale.get())
    game_over = False

    menu_frame.pack_forget()
    game_frame.pack(fill = 'both', expand = True)

    entry_password.config(state = 'normal')
    entry_password.delete(0, END)
    progress['value'] = 0
        
    start_timer()
    
def back_to_menu():
    global game_over
    game_over = True
    game_frame.pack_forget()
    menu_frame.pack(fill = 'both', expand = True)
    
def create_rule_widgets():
    global progress, rule_labels, rule_frames
    
    for widget in frame_rules.winfo_children():
        widget.destroy()
        
    rule_labels = {}
    rule_frames = {}

    for rule in rules_text:
        frame = Frame(frame_rules, bg = 'red', padx = 1, pady = 1)
        frame.pack(pady = 3, fill = 'x')
        label = Label(frame, text = f'✖ {rule}', fg = 'red', bg = '#f8d7da', font = ('Arial', 10), width = 40, anchor = 'w', padx = 10, pady = 3)
        label.pack(fill = 'x')
        rule_frames[rule] = frame
        rule_labels[rule] = label
        
    progress = Progressbar(game_frame, length = 400, maximum = len(rules_text))
    progress.pack(pady = 20)

root = Tk()
root.title('the password game')
root.resizable(0, 0)
root.configure(bg = '#dcf7e0')

width = 500
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (width / 2)) - 20
y = int((screen_height / 2) - (height / 2)) - 20

root.geometry(f'{width}x{height}+{x}+{y}')

time_left = 0.0
game_over = False
start_time = 0

menu_frame = Frame(root, bg = '#dcf7e0', width = 500, height = 500)
menu_frame.pack(fill = 'both', expand = True)

game_frame = Frame(root, bg = '#dcf7e0', width = 500, height = 500)

Label(menu_frame, text = 'The Password Game', font = ('Arial', 24, 'bold'), bg = '#dcf7e0').pack(pady = 40)
selected_difficulty = StringVar(value = 'Medium')
Label(menu_frame, text = 'Đặt thời gian bắt đầu: (giây):', font = ('Arial', 14), bg = '#dcf7e0').pack(pady = 10)

time_scale = Scale(menu_frame, from_ = 30, to = 120, orient = HORIZONTAL, length = 300, font = ('Arial', 12), bg = '#dcf7e0')
time_scale.set(100)
time_scale.pack(pady = 10)
time_scale.bind('<B1-Motion>', update_time_color)
time_scale.bind('<ButtonRelease-1>', update_time_color)
update_time_color()

Button(menu_frame, text = 'bắt đầu game', font = ('Arial', 14, 'bold'), command = lambda: start_game(selected_difficulty.get())).pack(side = 'bottom', pady = 30)

Label(game_frame, text = 'The Password Game', font = ('Arial', 18, 'bold'), bg = '#dcf7e0').pack(pady = 10)
Label(game_frame, text = 'Chọn password:', font = ('Arial', 12), bg = '#dcf7e0').pack()

frame_input = Frame(game_frame, bg = '#dcf7e0')
frame_input.pack(pady = 15)

entry_password = Entry(frame_input, width = 30, font = ('Arial', 12))
entry_password.pack(side = 'left', padx = 5)
entry_password.bind('<KeyRelease>', check_rules)

length_label = Label(frame_input, text = '0', font = ('Arial', 12), bg ='#dcf7e0')
length_label.pack(side = 'left')

timer_label = Label(game_frame, text = 'thời gian: 0.0', font = ('Arial', 12), bg = '#dcf7e0')
timer_label.place(x = 5, y = 5, anchor = NW)

frame_rules = Frame(game_frame, bg = '#dcf7e0')
frame_rules.pack()

rule_labels = {}
rule_frames = {}
# for rule in rules_text:
#     frame = Frame(frame_rules, bg = 'red', padx = 1, pady = 1)
#     frame.pack(pady = 3, fill = 'x')
#     label = Label(frame, text = f'✖ {rule}', fg = 'red', bg = '#f8d7da', font = ('Arial', 10), width = 40, anchor = 'w', padx = 10, pady = 3)
#     label.pack(fill = 'x')
#     rule_frames[rule] = frame
#     rule_labels[rule] = label

# progress = Progressbar(game_frame, length = 400, maximum = len(rules_text))
# progress.pack(pady = 20)

buttons_frame = Frame(game_frame, bg = '#dcf7e0')
buttons_frame.pack(side = 'bottom', pady = 20)

Button(buttons_frame, text = 'chơi lại', font = ('Arial', 12, 'bold'), command = start_game).pack(side = 'left', padx = 10)
Button(buttons_frame, text = 'quay lại menu', font = ('Arial', 12, 'bold'), command = back_to_menu).pack(side = 'left', padx = 10)

root.mainloop()