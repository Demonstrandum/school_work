"""Client for Area Trainers"""

import os
import tkinter as tk
import json
from time import gmtime, strftime

from PIL import Image
from PIL import ImageTk

import areaTrainer as at

# Global username and password
username = password = login_time = None
# Location and name of file
file = "{}/logins.json".format(os.path.dirname(__file__))
# Make file if it does not exist
if not os.path.exists(file):
    at.Users().save(file)

# Open the database
database = at.Users().load(file)


# Images directory
image_dir = "{}/assets/shapes/".format(os.path.dirname(__file__))
images = os.listdir(image_dir)

shape_data = {
    'circle': {
        'formula': r"\pi r^2",
        'formula-image': '{}/../formula/circle.png'.format(image_dir),
        
        'info': ' '.join("""
            Where \u03c0 is `pi` which is a constant of half the diameter
            of circle with radius 1, and `r` is the radius of the circle.
        """.split()).replace('\t', '').strip()
    }
}

# Start Tkinter GUI
root = tk.Tk()
width, height = 400, 300
root.title("Register or Login")
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


def back_inteface():
    show_frame.destroy()
    interface.pack()


def show_shape(name, file):
    """Show the selected shape"""
    # Log selected shape
    user_index = None
    for user_dict in database:
        if user_dict['username'] == username:
            user_index = database.index(user_dict)
            break

    if name not in sum(database[user_index]['shapes'], []):
        database[user_index]['shapes'].append([name, 1])

    for shape_count in database[user_index]['shapes']:
        if shape_count == []: break
        if shape_count[0] == name:
            shape_count[1] += 1  # Add one to times viewed if exists
            break

    global show_frame
    show_frame = tk.Frame(root, bg='white')
    data = shape_data[name]

    show_frame.pack()
    interface.pack_forget()
    shape_frame = tk.Frame(show_frame, bg='white')
    shape_frame.pack(side=tk.TOP)

    image = Image.open("{}/{}".format(image_dir, file))
    image = image.resize((350, 350), Image.ANTIALIAS)
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
    # image = image.resize((350, 350), Image.ANTIALIAS)
    formula_photo = ImageTk.PhotoImage(formula_image)
    # formula_photo = tk.PhotoImage(file=data['formula-image'])
    formula_label = tk.Label(
        desc_frame,
        image=formula_photo,
        bg='white'
    )
    formula_label.image = formula_photo
    formula_label.pack(side=tk.TOP)

    info_label = tk.Label(desc_frame, text=data['info'], bg='white', wraplength=400)
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


def access():
    """Run when logged in to present AT interface"""
    index_frame.pack_forget()  # Unpack the index interface
    login_frame.pack_forget()
    show_frame.pack_forget()
    register_frame.pack_forget()

    interface.pack(side=tk.TOP, pady=30, padx=30)

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
    global username, password, login_time
    registerer = at.Register(reg_name_entry.get(), reg_pass_entry.get(), database)

    validity = registerer.validate()
    print(reg_name_entry.get(), validity)
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
#root.geometry('{}x{}'.format(width, height))
root.mainloop()

# Take closing time and add start time
user_index = None
for user_dict in database:
    if user_dict['username'] == username:
        user_index = database.index(user_dict)
        break
database[user_index]['sessions'].append(
    [
        login_time,
        strftime("%Y-%m-%d %H:%M:%S", gmtime())
    ]
)
# Save info generated
at.Users(database).save(file)
# Verbose extra database output
print('Users saved, user database: ')
print(at.Users().load(file))
