import src.gui as gui
import tkinter as tk

if __name__ == '__main__':
    """
    Run application
    """
    root = tk.Tk()
    app = gui.GuiDesignerApp(root)
    calculator = gui.RankingCalculations()
    app.run()
