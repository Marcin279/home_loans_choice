import src.gui as gui
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    # print('rsm', calculator.rsm_result)
    # dataRSM = calculator.rsm_result
    # dataSPCS = calculator.spcs_result
    # dataTopsis = calculator.topsis_result
    # dataUTA = calculator.uta_result
    app = gui.GuiDesignerApp(root)
    calculator = gui.RankingCalculations()
    # print(app.data_RSM)
    # print(dataSPCS.keys())
    app.run()
