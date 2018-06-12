import logging
from tkinter import ttk


logger = logging.getLogger(__name__)


class BoardStylist:
    def __init__(self, organisms):
        self.styles = []

        ttk.Style().configure(
            "Board.TButton",
            padding=1,
            width=2,
            height=15,
            relief="flat",
            background="#ffffff",
        )
        for organism in organisms:
            logger.debug("Generated {}.Board.TButton".format(organism.__name__))
            self.styles.append(
                ttk.Style().configure(
                    "{}.Board.TButton".format(organism.__name__), foreground="black"
                )
            )
