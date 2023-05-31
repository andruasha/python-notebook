import tkinter as tk
from tkinter import ttk
import notebook.config as config
import notebook.context_menu as context_menu
import notebook.file_handling as file_handling
import notebook.tag as tag


class App(tk.Tk):
    """A class for forming a screen."""

    def __init__(self):
        """Initializing class fields."""
        super().__init__()
        self.filename = ''
        self.family = config.families[0]
        self.size = config.sizes[0]
        self.weight = config.weights[0]
        self.slant = config.slants[0]
        self.underline = config.underlines[0]
        self.text_color = config.color_codes.get(config.text_colors[0])
        self.back_color = config.color_codes.get(config.back_colors[0])
        self.last_cursor = '1.0'

        self.main_menu = tk.Menu(self)
        self.config(menu=self.main_menu)
        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.file_menu.add_command(label='Открыть', command=self.file_open)
        self.file_menu.add_command(label='Создать', command=self.file_new)
        self.file_menu.add_command(label='Сохранить', command=self.file_save)
        self.file_menu.add_command(label='Сохранить как',
                                   command=self.file_save_as)
        self.main_menu.add_cascade(label='Файл', menu=self.file_menu)

        self.toolbar = ttk.Label(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.font_family = tk.StringVar()
        self.font_box = ttk.Combobox(self.toolbar, width=30,
                                     textvariable=self.font_family, state='readonly')
        self.font_box['values'] = config.families
        self.font_box.current(config.families.index(self.family))
        self.font_box.grid(row=0, column=0, padx=5)
        self.font_box.bind('<<ComboboxSelected>>', self.change_family)

        self.size_list = tk.IntVar()
        self.font_size = ttk.Combobox(self.toolbar, width=4,
                                      textvariable=self.size_list, state='readonly')
        self.font_size['values'] = config.sizes
        self.font_size.current(config.sizes.index(self.size))
        self.font_size.grid(row=0, column=1, padx=5)
        self.font_size.bind('<<ComboboxSelected>>', self.change_size)

        self.txt_color_list = tk.IntVar()
        self.txt_color = ttk.Combobox(self.toolbar, width=10,
                                      textvariable=self.txt_color_list, state='readonly')
        self.txt_color['values'] = config.text_colors
        self.txt_color.current(0)
        self.txt_color.grid(row=0, column=2, padx=5)
        self.txt_color.bind('<<ComboboxSelected>>', self.change_text_color)

        self.bold_button = ttk.Button(self.toolbar, text='Жирный', )
        self.bold_button.grid(row=0, column=4, padx=5)
        self.bold_button.bind('<Button-1>', self.change_weight)

        self.italics_button = ttk.Button(self.toolbar, text='Курсив')
        self.italics_button.grid(row=0, column=6, padx=5)
        self.italics_button.bind('<Button-1>', self.change_slant)

        self.underline_button = ttk.Button(self.toolbar, text='Подчеркивание')
        self.underline_button.grid(row=0, column=8, padx=5)
        self.underline_button.bind('<Button-1>', self.change_underline)

        self.background_color_list = tk.IntVar()
        self.background_color = ttk.Combobox(self.toolbar, width=10,
                                             textvariable=self.background_color_list, state='readonly')
        self.background_color['values'] = config.back_colors
        self.background_color.current(0)
        self.background_color.grid(row=0, column=10, padx=5)
        self.background_color.bind(
            '<<ComboboxSelected>>', self.change_back_color)

        self.edit = tk.Menu(self, tearoff=0)
        self.edit.add_command(label='Копировать', command=self.copy)
        self.edit.add_command(label='Вставить', command=self.paste)
        self.edit.add_command(label='Вырезать', command=self.cut)

        self.text = tk.Text()
        self.title('Test')
        self.geometry('1005x500')
        self.text.config(wrap='word')
        self.text.focus_set()
        self.text.bind('<Button-3>', self.show)
        self.text.bind('<KeyRelease>', self.update_typing_text)
        self.text.bind('<Control-KeyPress>', self.keypress)

        self.install_tags()

        single_tag = self.form_tag()
        f, text_color, back_color = tag.parse_tag(single_tag)
        self.text.configure(font=f, foreground=text_color,
                            background=back_color)
        self.scrollbar = tk.Scrollbar(self, command=self.text.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.text['yscrollcommand'] = self.scrollbar.set

        self.text.pack(fill='both', expand=1)

    def keypress(self, event):
        context_menu.keypress(event)

    def change_family(self, *_):
        """Change the family."""
        self.family = self.font_box.get()
        self.update_selected_text(tag.FormatAction.FAMILY, self.family)

    def change_size(self, *_):
        """Change the size."""
        self.size = self.size_list.get()
        self.update_selected_text(tag.FormatAction.SIZE, self.size)

    def change_weight(self, *_):
        """Change the weight."""
        self.weight = 'bold' if self.weight == 'normal' else 'normal'
        self.update_selected_text(tag.FormatAction.WEIGHT, self.weight)

    def change_slant(self, *_):
        """Change the slant."""
        self.slant = 'roman' if self.slant == 'italic' else 'italic'
        self.update_selected_text(tag.FormatAction.SLANT, self.slant)

    def change_underline(self, *_):
        """Change the underline."""
        self.underline = '0' if self.underline == '1' else '1'
        self.update_selected_text(tag.FormatAction.UNDERLINE, self.underline)

    def change_text_color(self, *_):
        """Change the text color."""
        self.text_color = config.color_codes.get(self.txt_color.get())
        self.update_selected_text(tag.FormatAction.TEXT_COLOR, self.text_color)

    def change_back_color(self, *_):
        """Change background color."""
        self.back_color = config.color_codes.get(self.background_color.get())
        self.update_selected_text(tag.FormatAction.BACK_COLOR, self.back_color)

    def form_tag(self):
        """Create a tag with the current parameters."""
        return tag.create_tag(self.family, self.size, self.weight, self.slant,
                              self.underline, self.text_color, self.back_color)

    def update_selected_text(self, action, data):
        """Update the format of the selected text."""
        tag.update_selected_text(self.text, action, data)

    def update_typing_text(self, *_):
        """Update the format of the entered text."""
        cur_cursor = self.text.index('insert')
        if len(self.text.tag_ranges(tk.SEL)) != 0 or cur_cursor == self.last_cursor:
            return
        self.text.tag_add(self.form_tag(), self.last_cursor, cur_cursor)
        self.last_cursor = cur_cursor

    def install_tags(self):
        for t in tag.create_tags():
            f, text_color, back_color = tag.parse_tag(t)
            self.text.tag_configure(
                t, font=f, foreground=text_color, background=back_color)

    def show(self, event):
        context_menu.show(self, event)

    def cut(self):
        context_menu.cut(self)

    def copy(self):
        context_menu.copy(self)

    def paste(self):
        context_menu.paste(self)

    def delete(self):
        context_menu.delete(self)

    def file_open(self):
        file_handling.file_open(self)

    def file_save_as(self):
        file_handling.file_save_as(self, self.get_dump())

    def file_save(self):
        file_handling.file_save(self, self.get_dump())

    def file_new(self):
        file_handling.file_new(self)

    def get_dump(self):
        return self.text.dump('1.0', tk.END, tag=True, text=True)
