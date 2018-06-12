import logging
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""

    def __init__(self, text_widget):
        """
        :param text_widget: Tkinter Text or ScrolledText widget
        """
        super(TextHandler, self).__init__()

        self.text = text_widget

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state="normal")
            self.text.insert(tk.END, msg + "\n", record.levelname)
            self.text.configure(state="disabled")
            # Autoscroll to the bottom
            self.text.yview(tk.END)

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


class LoggerScrolledText(ScrolledText):
    """Scrolled text preconfigured for logging with colors and helper methods"""

    def __init__(self, parent):
        super(LoggerScrolledText, self).__init__(parent)
        self.configure(font="TkDefaultFont", state="disabled")
        self.tag_config("INFO", foreground="black")
        self.tag_config("DEBUG", foreground="gray")
        self.tag_config("WARNING", foreground="orange")
        self.tag_config("ERROR", foreground="red")
        self.tag_config("CRITICAL", foreground="red", underline=1)

    def clear(self):
        """
        Clears ScrolledText
        """
        self.configure(state="normal")
        self.delete(1.0, tk.END)
        self.configure(state="disabled")

    def append(self, message, tag="INFO"):
        """
        Adds message, scrolls to the end
        :param message:
        :param tag:
        """
        self.configure(state="normal")
        self.insert(tk.END, message.strip() + "\n", tag)
        self.configure(state="disabled")
        self.yview(tk.END)
