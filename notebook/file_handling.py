import tkinter as tk
from tkinter.filedialog import askopenfile, asksaveasfile
from notebook.data_converter import *
from notebook.tag import set_text_by_tag_dump


def file_open(self):
    """Open a file with text."""
    file_to_open = askopenfile(mode='r')
    if file_to_open is None:
        return
    file_new(self)
    self.filename = file_to_open.name
    document = Document(self.filename)
    tag_dump = create_tag_dump_from_document_data(document)
    set_text_by_tag_dump(self.text, tag_dump)


def file_save_as(self, dump):
    """Save the file as a new file."""
    asked_file = asksaveasfile(mode='w', defaultextension='.docx')
    if asked_file is None:
        return
    self.filename = asked_file.name
    create_document_from_tag_dump(dump).save(self.filename)


def file_save(self, dump):
    """Save the file as an existing file."""
    if self.filename == '':
        file_save_as(self, dump)
    else:
        create_document_from_tag_dump(dump).save(self.filename)


def file_new(self):
    """Clear the current text to create the text of a new file."""
    self.text.delete('1.0', tk.END)
    self.filename = ''
