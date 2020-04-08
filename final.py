from tkinter import *
import os
from tkinter import messagebox,filedialog,Menu,Scrollbar,font
PROGRAM_NAME = "Text Editor"
file_name = None

root = Tk()
menubar=Menu(root)
root.geometry('350x350')
root.title(PROGRAM_NAME)

def show_cursor_info_bar():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()


def update_cursor_info_bar(event=None):
    row, col = content_text.index(INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col) + 1)  # col starts at 0
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)

def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')

def on_content_changed(event=None):
    update_line_numbers()
    update_cursor_info_bar()


def get_line_numbers():
    output = ''
    if show_line_number.get():
        row, col = content_text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output


def display_about_messagebox(event=None):
    messagebox.showinfo("About", "{}{}".format(PROGRAM_NAME, "\nWe the best"))


def display_help_messagebox(event=None):
    messagebox.showinfo("Help", "Mail: xyz@gmail.com",icon='question')


def exit_editor(event=None):
    if messagebox.askokcancel("Do you really want to Quit?", "Seriously??"):
        root.destroy()


def new_file(event=None):
    root.title("Untitled")
    global file_name
    file_name = None
    content_text.delete(1.0, END)
    on_content_changed()


def open_file(event=None):
    input_file_name = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
        content_text.delete(1.0, END)
        with open(file_name) as _file:
            content_text.insert(1.0, _file.read())
        on_content_changed()


def write_to_file(file_name):
    try:
        content = content_text.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        messagebox.showwarning("Save", "Could not save the file.")


def save_as(event=None):
    input_file_name = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
    return "break"

def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"


def select_all(event=None):
    content_text.tag_add('sel', '1.0', 'end')
    return "break"

def cut():
    content_text.event_generate("<<Cut>>")
    on_content_changed()
    return "break"


def copy():
    content_text.event_generate("<<Copy>>")
    return "break"


def paste():
    content_text.event_generate("<<Paste>>")
    on_content_changed()
    return "break"


def undo():
    content_text.event_generate("<<Undo>>")
    on_content_changed()
    return "break"


def redo(event=None):
    content_text.event_generate("<<Redo>>")
    on_content_changed()
    return 'break'

def font_courier():
    global text
    text=content_text
    text.config(font="Courier")

def font_arial():
    global text
    text=content_text
    text.config(font="Arial")

def font_times():
    global text
    text=content_text
    text.config(font="Times")

def font_consoles():
    global text
    text=content_text
    text.config(font="Consoles")

def font_tahoma():
    global text
    text=content_text
    text.config(font="Tahoma")

#File Menu
filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="New",accelerator='Ctrl+N',compound='left',command=new_file)
filemenu.add_command(label="Open",accelerator='Crtl+O',compound='left',command=open_file)
filemenu.add_command(label="Save", accelerator='Crtl+S',compound='left',command=save)
filemenu.add_command(label="Save As",accelerator='Ctrl+Shift+S',compound='left', command=save_as)
filemenu.add_separator()
filemenu.add_command(label='Exit', accelerator='Alt+F4',command=exit_editor)
menubar.add_cascade(label='File', menu=filemenu)

#Edit Menu
edit_menu = Menu(menubar, tearoff=0)
edit_menu.add_command(label='Select All', underline=7,accelerator='Ctrl+A', command=select_all)
edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', compound='left',command=undo)
edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', compound='left', command=redo)
edit_menu.add_separator()
edit_menu.add_command(label='Cut', accelerator='Ctrl+X', compound='left',command=cut)
edit_menu.add_command(label='Copy', accelerator='Ctrl+C', compound='left',command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl+V', compound='left',command=paste)
edit_menu.add_separator()
menubar.add_cascade(label='Edit', menu=edit_menu)

#View Menu
view_menu = Menu(menubar, tearoff=0)
show_line_number = IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label='Show Line Number', variable=show_line_number,command=update_line_numbers)
show_cursor_info = IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(label='Show Cursor Location at Bottom', variable=show_cursor_info, command=show_cursor_info_bar)
menubar.add_cascade(label='View', menu=view_menu)

#Implementing Fonts
font_menu=Menu(menubar,tearoff=0)
text_font=StringVar()
text_font.set("Times")
    
font_menu.add_radiobutton(label="Times", variable=text_font, command=font_times)
font_menu.add_radiobutton(label="Arial", variable=text_font, command=font_arial)
font_menu.add_radiobutton(label="Consoles", variable=text_font, command=font_consoles)
font_menu.add_radiobutton(label="Courier", variable=text_font, command=font_courier)
font_menu.add_radiobutton(label="Tahoma", variable=text_font, command=font_tahoma)
menubar.add_cascade(label="Fonts",menu=font_menu)

#About Menu
about_menu = Menu(menubar, tearoff=0)
about_menu.add_command(label='About', command=display_about_messagebox)
about_menu.add_command(label='Help', command=display_help_messagebox)
menubar.add_cascade(label='About',  menu=about_menu)
root.config(menu=menubar)


line_number_bar = Text(root, width=4, padx=3, takefocus=0,  border=0,background='khaki', state='disabled',  wrap='none')
line_number_bar.pack(side='left',  fill='y')

content_text = Text(root, wrap='word', undo=1)
content_text.pack(expand='yes', fill='both')

scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)

scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side='right', fill='y')

cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')

content_text.bind('<KeyPress-F1>', display_help_messagebox)
content_text.bind('<Control-N>', new_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-S>', save)
content_text.bind('<Control-s>', save)
content_text.bind('<Control-A>', select_all)
content_text.bind('<Control-a>', select_all)
content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)
content_text.bind('<Any-KeyPress>', on_content_changed)

root.mainloop()