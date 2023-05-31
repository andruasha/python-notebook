import tkinter as tk


def show(self, event):
    """Show context menu."""
    self.edit.post(event.x_root, event.y_root)


def cut(self):
    """Cut text."""
    self.copy()
    self.delete()


def copy(self):
    """Copy text."""
    selection = self.text.tag_ranges(tk.SEL)
    if selection:
        self.clipboard_clear()
        self.clipboard_append(self.text.get(*selection))


def paste(self):
    """Paste text."""
    self.text.insert(tk.INSERT, self.clipboard_get())


def delete(self):
    """Delete the selected text."""
    selection = self.text.tag_ranges(tk.SEL)
    if selection:
        self.text.delete(*selection)


def keypress(e):
    """Process the action of keyboard keys on text operations."""
    if e.keycode == 86 and e.keysym != 'v':
        e.widget.event_generate('<<Paste>>')
    elif e.keycode == 67 and e.keysym != 'c':
        e.widget.event_generate('<<Copy>>')
    elif e.keycode == 88 and e.keysym != 'x':
        e.widget.event_generate('<<Cut>>')
    elif e.keycode == 65 and e.keysym != 'a':
        e.widget.event_generate('<<SelectAll>>')
