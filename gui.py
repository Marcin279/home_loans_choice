import pathlib
import pygubu
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib
# matplotlib.use('TkAgg')
from typing import List, Tuple, Optional, Union, Dict


# PROJECT_PATH = pathlib.Path(__file__).parent
# PROJECT_UI = PROJECT_PATH / "gui_designer.ui"

class Point:
    def __init__(self, x, y, a=None):
        self.x = x
        self.y = y
        self.a = a
        # self.b = None
        # self.c = None
        # self.d = None
        # self.e = None
        # self.f = None
        # self.g = None
        # self.h = None

    def __repr__(self):
        if self.a is not None:
            return f'{self.x}, {self.y}, {self.a}'
        return f'{self.x}; {self.y}'


def generete_data(dim3=False):
    dct = {}
    lst_name = [f'Point{i}' for i in range(10)]
    if not dim3:
        x = [np.random.randint(0, 20) for _ in range(10)]
        y = [np.random.randint(0, 20) for _ in range(10)]

        lst = [Point(x[i], y[i]) for i in range(len(x))]
    else:
        x = [np.random.randint(0, 20) for _ in range(10)]
        y = [np.random.randint(0, 20) for _ in range(10)]
        a = [np.random.randint(0, 20) for _ in range(10)]

        lst = [Point(x[i], y[i], a[i]) for i in range(len(x))]
    for i in range(len(lst)):
        dct[lst_name[i]] = lst[i]
    return dct


class GuiDesignerApp:
    def __init__(self, master=None, data_RSM=None, data_TOPSIS=None, data_SP_CS=None):
        # build ui
        self.data_RSM: Optional[Dict[str, List[Point]], None] = data_RSM
        self.data_TOPSIS: Optional[Dict[str, List[Point]], None] = data_TOPSIS
        self.data_SP_CS: Optional[Dict[str, List[Point]], None] = data_SP_CS

        self.string_to_ranking: Optional[str, None] = None

        self.figure = None

        self.window = tk.Frame(master)
        self.wybor_kryteriow = None
        self.wybor_metody = None
        self.labelframe1 = None
        self.labelframe2 = None
        self.labelframe3 = None
        self.labelframe4 = None
        # self.label3 = None

        self.window.configure(height='900', width='1600')
        self.window.pack(padx='40', pady='20', side='top')

        # Main widget
        self.mainwindow = self.window

    def create_ui_main(self):
        self.wybor_kryteriow = tk.LabelFrame(self.window)
        self.label3 = tk.Label(self.wybor_kryteriow)
        self.label3.configure(text='label3')
        self.label3.pack(side='top')
        self.checkbutton3 = tk.Checkbutton(self.wybor_kryteriow)
        self.checkbutton3.configure(text='checkbutton3')
        self.checkbutton3.pack(side='top')
        self.checkbutton4 = tk.Checkbutton(self.wybor_kryteriow)
        self.checkbutton4.configure(text='checkbutton4')
        self.checkbutton4.pack(side='top')
        self.checkbutton5 = tk.Checkbutton(self.wybor_kryteriow)
        self.checkbutton5.configure(text='checkbutton5')
        self.checkbutton5.pack(side='top')
        self.checkbutton6 = tk.Checkbutton(self.wybor_kryteriow)
        self.checkbutton6.configure(text='checkbutton6')
        self.checkbutton6.pack(side='top')
        self.checkbutton7 = tk.Checkbutton(self.wybor_kryteriow)
        self.checkbutton7.configure(text='checkbutton7')
        self.checkbutton7.pack(side='top')
        self.checkbutton8 = tk.Checkbutton(self.wybor_kryteriow)
        self.checkbutton8.configure(text='checkbutton8')
        self.checkbutton8.pack(side='top')
        self.checkbutton9 = tk.Checkbutton(self.wybor_kryteriow)
        self.checkbutton9.configure(text='checkbutton9')
        self.checkbutton9.pack(side='top')
        self.checkbutton10 = tk.Checkbutton(self.wybor_kryteriow)
        self.checkbutton10.configure(text='checkbutton10')
        self.checkbutton10.pack(side='top')
        self.checkbutton11 = tk.Checkbutton(self.wybor_kryteriow)
        self.checkbutton11.configure(text='checkbutton11')
        self.checkbutton11.pack(side='top')
        self.checkbutton12 = tk.Checkbutton(self.wybor_kryteriow)
        self.checkbutton12.configure(text='checkbutton12')
        self.checkbutton12.pack(side='top')
        self.wybor_kryteriow.configure(height='50', text='wybor_kryteriow', width='40')
        self.wybor_kryteriow.grid(column='0', padx='5', pady='5', row='1', sticky='n')

        self.wybor_metody = tk.LabelFrame(self.window)
        self.label4 = tk.Label(self.wybor_metody)
        self.label4.configure(text='label4')
        self.label4.pack(side='top')

        self.checkbutton1 = tk.Checkbutton(self.wybor_metody)
        self.checkbutton1.configure(text='checkbutton1')
        self.checkbutton1.pack(side='top')
        self.checkbutton2 = tk.Checkbutton(self.wybor_metody)
        self.checkbutton2.configure(text='checkbutton2')
        self.checkbutton2.pack(side='top')
        self.checkbutton13 = tk.Checkbutton(self.wybor_metody)
        self.checkbutton13.configure(text='checkbutton13')
        self.checkbutton13.pack(side='top')
        self.checkbutton14 = tk.Checkbutton(self.wybor_metody)
        self.checkbutton14.configure(text='checkbutton14')
        self.checkbutton14.pack(side='top')

        self.wybor_metody.configure(height='50', relief='raised', text='wybor_metody', width='25')
        self.wybor_metody.grid(column='1', padx='5', pady='5', row='1', sticky='n')

        self.labelframe1 = tk.LabelFrame(self.window)

        self.text4 = tk.Text(self.labelframe1)
        self.text4.configure(blockcursor='false', height='10', relief='flat', takefocus=False)
        self.text4.configure(width='20')
        self.text4.grid(column='2', row='2', sticky='nw')

        self.labelframe1.configure(height='200', text='ranking', width='100')
        self.labelframe1.grid(column='2', row='1', sticky='n')
        self.labelframe2 = tk.LabelFrame(self.window)
        self.button2 = tk.Button(self.labelframe2)
        self.button2.configure(text='Dane')
        self.button2.pack(side='left')

        self.button3 = tk.Button(self.labelframe2, text='RSM')
        self.button3.configure(command=lambda: self.plot_values(self.data_RSM))
        self.button3.pack(side='left')

        self.button6 = tk.Button(self.labelframe2, text='SP-CS')
        self.button6.configure(command=lambda: self.plot_values(self.data_SP_CS))
        self.button6.pack(side='left')

        self.button7 = tk.Button(self.labelframe2, text='TOPSIS')
        self.button7.configure(command=lambda: self.plot_values(self.data_TOPSIS))
        self.button7.pack(side='left')

        self.refresh_button = tk.Button(self.labelframe2, text='Refresh')
        self.refresh_button.configure(command=self.refresh)
        self.refresh_button.pack(side='left')

        self.labelframe2.configure(height='200', text='MENU', width='200')
        self.labelframe2.grid(column='0', row='0', sticky='n')
        self.labelframe3 = tk.LabelFrame(self.window)

        self.labelframe3.configure(height='300', text='Wykres', width='300')
        self.labelframe3.grid(column='1', padx='10', pady='10', row='2')

        self.labelframe4 = tk.LabelFrame(self.window)
        self.button8 = tk.Button(self.labelframe4)
        self.button8.configure(cursor='arrow', font='{Arial CE} 12 {bold}', text='Licz')
        self.button8.pack(side='top')
        self.labelframe4.configure(height='200', width='200')
        self.labelframe4.grid(column='1', row='3')

    def run(self):
        self.create_ui_main()
        self.mainwindow.mainloop()

    def plot_2d(self, data):
        """
        args: data: List[Point]
        :return:
        """
        figure1, ax1 = plt.subplots(figsize=(5, 3), dpi=100)
        # data: Dict[str, Point] = self.data_RSM

        x = [elem.x for p, elem in data.items()]
        y = [elem.y for p, elem in data.items()]
        ax1.scatter(x, y)
        for key, coords in data.items():
            ax1.annotate(key, (coords.x, coords.y))
        figure1.show()
        return figure1

    def plot_3d(self, data):
        figure1 = plt.figure(figsize=(6, 4), dpi=100)
        ax1 = plt.axes(projection="3d")

        x = [elem.x for p, elem in data.items()]
        y = [elem.y for p, elem in data.items()]
        z = [elem.a for p, elem in data.items()]
        key_lst = list(data.keys())

        for i in range(len(x)):
            ax1.scatter(x[i], y[i], z[i], color='b')
            ax1.text(x[i], y[i], z[i], (key_lst[i]), size=8, zorder=1)

        figure1.show()
        return figure1

    def plot_values(self, data):
        if data['Point0'].a is None:
            self.figure = self.plot_2d(data)
        else:
            self.figure = self.plot_3d(data)

        chart = FigureCanvasTkAgg(self.figure, self.labelframe3)
        self.print_ranking(data)
        chart.get_tk_widget().pack()

    def reformat_ranking(self, data):
        S = ''
        if data['Point0'].a is None:
            for point_name, elem in data.items():
                S += f'{point_name}: ({elem.x}, {elem.y})\n'
        else:
            for point_name, elem in data.items():
                S += f'{point_name}: ({elem.x}, {elem.y}, {elem.a})\n'
        return S

    def print_ranking(self, data):
        self.string_to_ranking = self.reformat_ranking(data)
        self.text4.insert(tk.INSERT, self.string_to_ranking)

    def refresh(self):
        self.wybor_kryteriow.destroy()
        self.wybor_metody.destroy()
        self.labelframe3.destroy()
        self.labelframe2.destroy()
        self.labelframe1.destroy()
        self.labelframe4.destroy()

        self.create_ui_main()


if __name__ == '__main__':
    root = tk.Tk()
    dataRSM = generete_data()
    dataSPCS = generete_data(dim3=True)
    dataTopsis = generete_data()
    app = GuiDesignerApp(root, data_RSM=dataRSM, data_SP_CS=dataSPCS, data_TOPSIS=dataTopsis)
    # print(app.data_RSM)
    # app.plot_3d(dataSPCS)
    # print(dataSPCS.keys())
    app.run()
