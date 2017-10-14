"""Client for Area Trainers"""

import os, sys
import random, time, threading
import math  # For area calculations
import tkinter as tk
import json
from time import gmtime, strftime

from PIL import Image
from PIL import ImageTk

import areaTrainer as at

# Global username and password
username = password = login_time = None
# Location and name of file
file = "{}/logins.json".format(os.path.dirname(os.path.abspath(__file__)))
# Make file if it does not exist
if not os.path.exists(file):
    at.Users().save(file)

# Open the database
database = at.Users().load(file)


# Images directory
image_dir = "{}/assets/shapes/".format(os.path.dirname(os.path.abspath(__file__)))
images = os.listdir(image_dir)

shape_data = {
    'circle': {
        'latex': r'\pi r^2',
        'formula': "3.14159265 * {var1}**2",
        'variable': "radius — r = {var1}",
        'formula-image': '{}/../formula/circle.gif'.format(image_dir),

        'info': ' '.join("""
            Where \u03c0 is `pi` which is a constant of half the diameter
            of circle with radius 1, and `r` is the radius of the circle.
        """.split()).replace('\t', '').strip()
    },
    'regular-polygon': {
        'latex': r'\frac{n s^2}{4 \tan(\frac{180}{n})}',
        'formula': "({var1} * {var2}**2) / (4 * math.tan(math.radians(180/{var1})))",
        'variable': "number of sides — n = {var1}\n length of one side — s = {var2}",
        'formula-image': '{}/../formula/regular-polygon.gif'.format(image_dir),

        'info': ' '.join("""
            To find the area of any regular n-sided polygon, with
            certain side length, plug in the number of sides `n` and
            the length of one side `s`, in to the equation.
            It uses the formula of multiplying the apothem (shortest length from centre
            to side of polygon) by the perimeter and dividing it all by 2.
            The equation for the apothem is `s / 2tan(180/n)` multiplied by the
            perimeter (`s * n`), and all over 2, results in this formula.
        """.split()).replace('\t', '').strip()
    },
    'square': {
        'latex': r'l^2',
        'formula': "{var1}**2",
        'variable': "side length — l = {var1}",
        'formula-image': '{}/../formula/square.gif'.format(image_dir),

        'info': ' '.join("""
            The area of a square is always a square number (hence the name).
            It is found by multiplying the two sides: `l * l` or as it
            may also be writen as `l\u00b2`.
        """.split()).replace('\t', '').strip()
    },
    'right-angle-triangle': {
        'latex': r'\frac{1}{2} a b',
        'formula': "({var1} * {var2}) / 2",
        'variable': "leg — a = {var1}\nleg — b = {var2}",
        'formula-image': '{}/../formula/right-angle-triangle.gif'.format(image_dir),

        'info': ' '.join("""
            Get the length of the two legs (not the hypotenuse)
            and multiply them together, then divide it all by 2.
            If you have the length of the hypotenuse and missing one of
            the legs, then you can use the pythagorean theorem (`√(c\u00b2 - a\u00b2) = b`)
            where `c` is the hyptenuse and `a` and `b` are the legs, then when you
            have the missing leg, use the formula.
        """.split()).replace('\t', '').strip()
    },
    'triangle': {
        'latex': r'\frac{1}{2} a c \cdot \sin(B)',
        'formula': "({var1} * {var2} / 2) * math.sin({var3})",
        'variable': "side adjacent to the angle — a = {var1}\nside joining other side — c = {var2}\nangle between two sides — B = {var3}",
        'formula-image': '{}/../formula/triangle.gif'.format(image_dir),

        'info': ' '.join("""
            `a` and `c` are sides of the triangle and `B` is the angle they form
            when joining. Substitute in these variables to find the area.
        """.split()).replace('\t', '').strip()
    },
    'trapezium': {
        'latex': r'frac{1}{2} h(a + b)',
        'formula': "({var1}/2) * ({var2} + {var3})",
        'variable': "height — h = {var1}\nlength of top — a = {var2}\nlength of base — b = {var3}",
        'formula-image': '{}/../formula/trapezium.gif'.format(image_dir),

        'info': ' '.join("""
            To calculate the area of a trapezium, get the length
            of the base plus the top of the trapezium, them multiply all that by the
            trapezium's height, and then half that result.
            If you do not have the height and rather one of the slanted sides,
            use the pythagorean theorem to find the height, by imagining a right
            angle triangle.
        """.split()).replace('\t', '').strip()
    },
}

def get_user_index():
    for user_dict in database:
        if user_dict['username'] == username:
            return database.index(user_dict)
    return None

class Score(tk.IntVar):
    def __init__(self, start=None, reward=2, punishment=1):
        super().__init__(master=None)
        self.start = 0
        self.reward = reward
        self.punishment = punishment
        if start is not None:
            self.start = start

        self.score = self.start

    def correct(self):
        self.score += self.reward
        super().set(self.score)
        return self.score

    def wrong(self):
        self.score -= self.punishment
        super().set(self.score)
        return self.score

    def get(self):
        return super().get()

    def set(self, val):
        super().set(val)
        self.score = val
        return self.get()

    # Alias functions:
    reward = correct
    punish = wrong

# Start Tkinter GUI
root = tk.Tk()
width, height = 400, 300
root.resizable(False, False)
root.configure(background='white')

login_frame = tk.Frame(root, background='white')
register_frame = tk.Frame(root, background='white')

index_frame = tk.Frame(root, background='white')
index_frame.pack(padx=20, pady=20)


def switch_login():
    """Swith to login screen"""
    global login_frame, index_frame
    login_frame.pack(side=tk.TOP, pady=20, padx=20)
    index_frame.pack_forget()

index_login = tk.Button(
    index_frame,
    text='Login',
    background='white',
    command=switch_login
)
index_login.pack(side=tk.LEFT)
tk.Label(index_frame, text=' or ', background='white').pack(side=tk.LEFT)


def switch_register():
    """Switch to register screen"""
    register_frame.pack(side=tk.TOP, pady=20, padx=20)
    index_frame.pack_forget()

index_register = tk.Button(
    index_frame, 
    text='Register',
    background='white',
    command=switch_register
)
index_register.pack(side=tk.RIGHT)

# Login screen
login_name_frame = tk.Frame(login_frame, background='white')
login_name_frame.pack(side=tk.TOP, pady=5)

login_name_label = tk.Label(login_name_frame, text="Username", background='white')
login_name_label.pack(side=tk.LEFT, padx=(0, 10))
login_name_entry = tk.Entry(login_name_frame, bd=5, background='white', text='default')
login_name_entry.pack(side=tk.RIGHT)

login_pass_frame = tk.Frame(login_frame, background='white')
login_pass_frame.pack(side=tk.TOP, pady=(5, 15))

login_pass_label = tk.Label(login_pass_frame, text="Password ", background='white')
login_pass_label.pack(side=tk.LEFT, padx=(0, 11))
login_pass_entry = tk.Entry(login_pass_frame, bd=5, background='white', show='•')
login_pass_entry.pack(side=tk.RIGHT)


login_message = tk.StringVar()
login_message.set('')
login_label = tk.Label(login_frame, textvariable=login_message, background='white', pady=5)

interface  = tk.Frame(root, bg='white')
show_frame = tk.Frame(root, bg='white')
quiz_frame = tk.Frame(root, bg='white')

correct = False
attempts = 2
attempts_count = attempts
attempts_var = tk.StringVar()
attempts_var.set("[{}] attempts left.\n".format(attempts_count))
score = Score(start=0, reward=2, punishment=1)  # Set to last score in `access` function

def check_answer(right=None, var=None):
    global correct, attempts_count, attempts_var

    correct = int(right) == var.get()
    if correct:
        attempts_count = attempts
        attempts_var.set("[{}] attempts left.\n".format(attempts_count))
    else:
        attempts_count -= 1
        attempts_var.set("Wrong! Try again,\n[{}] attempts left.\n".format(attempts_count))

    return correct


def back_inteface():
    show_frame.destroy()
    interface.pack()


def show_shape(name, file):
    """Show the selected shape"""
    # Log selected shape
    global attempts_count, attempts_var
    attempts_count = attempts
    attempts_var.set("[{}] attempts left.\n".format(attempts_count))

    user_index = get_user_index()

    if name not in sum(database[user_index]['shapes'], []):
        database[user_index]['shapes'].append([name, 1])

    for shape_count in database[user_index]['shapes']:
        if shape_count == []: break
        if shape_count[0] == name:
            shape_count[1] += 1  # Add one to times viewed if exists
            break

    global show_frame, quiz_frame
    quiz_frame = tk.Frame(root, bg='white', padx=20, pady=10)
    quiz_frame.pack()
    show_frame = tk.Frame(root, bg='white')
    interface.pack_forget()

    data = shape_data[name]

    max_var = 40
    var1, var2, var3, var4 = [random.randint(1, max_var) for _ in range(4)]
    right_answer = eval(data['formula'].format(var1=var1, var2=var2, var3=var3, var4=var4))
    answers = [eval(data['formula'].format(
        var1=random.randint(1, max_var),
        var2=random.randint(1, max_var),
        var3=random.randint(1, max_var),
        var4=random.randint(1, max_var))) for _ in range(3)]

    answers.append(right_answer)
    random.shuffle(answers)
    right_index = answers.index(right_answer)

    radio_int = tk.IntVar()
    radio_int.set(0)

    attempts_label = tk.Label(quiz_frame, textvariable=attempts_var, bg='white')
    attempts_label.grid(row=0, column=0)
    values_label = tk.Label(quiz_frame, pady=20, text=data['variable'].format(var1=var1, var2=var2, var3=var3, var4=var4), bg='white')
    values_label.grid(row=1, column=0)
    a_check = tk.Radiobutton(quiz_frame, pady=5, padx=5, text="{:.2f}".format(answers[0]).zfill(10), variable=radio_int, value=answers[0], bg='white')
    a_check.grid(row=2, column=0)
    b_check = tk.Radiobutton(quiz_frame, pady=5, padx=5, text="{:.2f}".format(answers[1]).zfill(10), variable=radio_int, value=answers[1], bg='white')
    b_check.grid(row=3, column=0)
    c_check = tk.Radiobutton(quiz_frame, pady=5, padx=5, text="{:.2f}".format(answers[2]).zfill(10), variable=radio_int, value=answers[2], bg='white')
    c_check.grid(row=4, column=0)
    d_check = tk.Radiobutton(quiz_frame, pady=5, padx=5, text="{:.2f}".format(answers[3]).zfill(10), variable=radio_int, value=answers[3], bg='white')
    d_check.grid(row=5, column=0)

    tk.Label(quiz_frame, text='', pady=2.5, padx=2.5, bg='white').grid(row=6)

    check_button = tk.Button(
        quiz_frame,
        text='Submit',
        bg='white',
        command=(lambda r=right_answer, v=radio_int: check_answer(right=r, var=v))
    )
    check_button.grid(row=7, column=0)

    def wrong_event():
        quiz_frame.destroy()
        show_frame.pack()
        shape_frame = tk.Frame(show_frame, bg='white')
        shape_frame.pack(side=tk.TOP)

        too_wrong = tk.Label(shape_frame, text="Sorry, too many wrong answers,\nHere's an explanation:", bg='white', pady=10)
        too_wrong.pack(side=tk.TOP)

        image = Image.open("{}/{}".format(image_dir, file))
        image = image.resize((175, 175), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        photo_label = tk.Label(
            shape_frame,
            image=photo,
            compound=tk.TOP,
            borderwidth=2, relief="groove",
            bg='white'
        )
        photo_label.image = photo
        photo_label.pack(side=tk.TOP, padx=40, pady=(40, 20))

        desc_frame = tk.Frame(show_frame, bg='white')
        desc_frame.pack(side=tk.BOTTOM)

        formula_image = Image.open(data['formula-image'])
        formula_photo = ImageTk.PhotoImage(formula_image)
        formula_label = tk.Label(
            desc_frame,
            image=formula_photo,
            bg='white'
        )
        formula_label.image = formula_photo
        formula_label.pack(side=tk.TOP)

        info_label = tk.Label(desc_frame, text=data['info'], bg='white', justify=tk.LEFT, wraplength=200)
        info_label.pack(side=tk.TOP, pady=(30, 20))

        back_frame = tk.Frame(desc_frame, bg='white')
        back_frame.pack(side=tk.BOTTOM, pady=20)
        back_button = tk.Button(
            back_frame,
            text='Back',
            bg='white',
            command=back_inteface
        )
        back_button.pack(side=tk.BOTTOM)

    def correct_event():
        quiz_frame.destroy()
        congrats = tk.Label(
            root,
            text='Correct Answer\nYour score has increased!',
            bg='white',
            padx=30,
            pady=30
        )
        congrats.pack()
        time.sleep(3)
        congrats.pack_forget()
        back_inteface()

    def answer_event():
        global attempts_count, correct
        while True:
            time.sleep(1)
            if correct:
                correct = False  # Set back to assume wrong
                attempts_count = attempts
                score.correct()
                correct_event()
                break

            if attempts_count < 1:
                attempts_count = attempts
                score.punish()
                wrong_event()
                break

    answer_thread = threading.Thread(target=answer_event)
    answer_thread.start()


def access():
    """Run when logged in to present AT interface"""
    global correct, score
    root.title("Area Training")
    score.set(database[get_user_index()]['score'])
    correct = False  # Reset correctness when on home screen
    score_frame = tk.Frame(root, bg='white')
    score_frame.pack(side=tk.TOP, pady=(20, 20))

    score_indicate = tk.Label(score_frame, text='Score:', bg='white')
    score_label = tk.Label(score_frame, textvariable=score, bg='white')
    score_label.pack(side=tk.RIGHT)
    score_indicate.pack(side=tk.LEFT)


    index_frame.pack_forget()  # Unpack the index interface
    login_frame.pack_forget()
    show_frame.pack_forget()
    register_frame.pack_forget()

    interface.pack(side=tk.TOP, pady=(0, 30), padx=30)
    interface_message = tk.Label(interface, text='Click on a shape to practise:', bg='white')
    interface_message.pack(side=tk.TOP)
    canvas = tk.Canvas(
        interface,
        bg='white',
        width=300,
        height=300,
        border=2,
        relief="groove",
        scrollregion=(0, 0, 500, 1000)
    )

    # scrollbar = tk.Scrollbar(interface, bg='white', orient=tk.VERTICAL)
    # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    # scrollbar.config(command=canvas.yview)
    # canvas.config(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH, pady=20, padx=20)

    col = 0
    row = 0
    grid_width = 2  # How many columns - 1 (0 index)
    for image_file in images:
        image = Image.open("{}/{}".format(image_dir, image_file))
        image = image.resize((150, 150), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image)

        shape_name = ".".join(image_file.split('.')[:-1]).lower()
        shape_title = ".".join(image_file.split('.')[:-1]).replace('-', ' ').title()

        shape = tk.Label(
            canvas,
            text=shape_title,
            image=tk_photo,
            compound=tk.TOP,
            bg='white'
        )
        shape.image = tk_photo
        shape.grid(row=row, column=col, sticky='ns', padx=20, pady=20)
        shape.bind(
            "<Button-1>", 
            (lambda event, name=shape_name, file=image_file: show_shape(name, file))
        )

        col += 1
        if col > grid_width:
            row += 1
            col = 0


def login():
    """Login to a user"""
    global username, password, login_time
    root.title("Login to Area Trainer")
    login_object = at.Login(login_name_entry.get(), login_pass_entry.get(), database)
    if not login_object.exists():
        login_message.set('No such username!')
        login_label.pack()
        return False

    if not login_object.login():
        login_message.set('Incorrect password!')
        login_label.pack()
        return False

    login_message.set('Success')
    # Login time
    login_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    login_label.pack()

    username, password = login_name_entry.get(), login_pass_entry.get()
    access()
    return True


def login_back():
    """Switch to register screen"""
    root.title("Register or Login")
    global login_frame, index_frame
    index_frame.pack(side=tk.TOP, padx=20, pady=20)
    login_frame.pack_forget()

login_back_button = tk.Button(
    login_frame, 
    text='Back',
    background='white',
    command=login_back
)
login_back_button.pack(side=tk.LEFT)


login_button = tk.Button(
    login_frame,
    text='Login',
    background='white',
    command=login
)
login_button.pack(side=tk.RIGHT)

# Register frame

reg_name_frame = tk.Frame(register_frame, background='white')
reg_name_frame.pack(side=tk.TOP, pady=5)

reg_name_label = tk.Label(reg_name_frame, text="Username", background='white')
reg_name_label.pack(side=tk.LEFT, padx=(0, 15))
reg_name_entry = tk.Entry(reg_name_frame, bd=5, background='white')
reg_name_entry.pack(side=tk.RIGHT)

reg_pass_frame = tk.Frame(register_frame, background='white')
reg_pass_frame.pack(side=tk.TOP, pady=5)

reg_pass_label = tk.Label(reg_pass_frame, text="Password", background='white')
reg_pass_label.pack(side=tk.LEFT, padx=(0, 20))
reg_pass_entry = tk.Entry(reg_pass_frame, bd=5, background='white', show='•')
reg_pass_entry.pack(side=tk.RIGHT)


reg_repass_frame = tk.Frame(register_frame, background='white')
reg_repass_frame.pack(side=tk.TOP, pady=(5, 15))

reg_repass_label = tk.Label(reg_repass_frame, text="Re-enter ", background='white')
reg_repass_label.pack(side=tk.LEFT, padx=(0, 21))
reg_repass_entry = tk.Entry(reg_repass_frame, bd=5, background='white', show='•')
reg_repass_entry.pack(side=tk.RIGHT)

register_message = tk.StringVar()
register_message.set('')
register_label = tk.Label(register_frame, textvariable=register_message, background='white', pady=7)


def register():
    """Register user and log in"""
    root.title("Sign up to Area Trainer")
    global username, password, login_time
    registerer = at.Register(reg_name_entry.get(), reg_pass_entry.get(), database)

    validity = registerer.validate()
    if not validity['valid']:
        register_message.set(validity['error'])
        register_label.pack()
        return validity['valid']

    register_message.set('Success')
    register_label.pack()
    registerer.add()
    registerer.save(file)

    username, password = reg_name_entry.get(), reg_pass_entry.get()
    # Login time
    login_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    access()
    return True

regsiter_button = tk.Button(
    register_frame,
    text='Register',
    background='white',
    command=register
)
regsiter_button.pack(side=tk.RIGHT)


def register_back():
    """Switch to register screen"""
    root.title("Register or Login")
    index_frame.pack(side=tk.TOP, padx=20, pady=20)
    register_frame.pack_forget()

reg_back_button = tk.Button(
    register_frame, 
    text='Back',
    background='white',
    command=register_back
)
reg_back_button.pack(side=tk.LEFT)

root.resizable(width=False, height=False)
root.title("Register or Login")
#root.geometry('{}x{}'.format(width, height))
root.mainloop()

# Take closing time and add start time
user_index = get_user_index()
database[user_index]['sessions'].append(
    [
        login_time,
        strftime("%Y-%m-%d %H:%M:%S", gmtime())
    ]
)
# Store the score
database[get_user_index()]['score'] = score.get()
# Save info generated:
at.Users(database).save(file)
# Verbose extra database output
# print('Users saved, user database: ')
# print(at.Users().load(file))
