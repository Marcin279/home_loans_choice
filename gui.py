import pathlib
import pygubu
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from typing import List, Tuple, Dict
import pandas as pd
# import matplotlib
# matplotlib.use('TkAgg')
from typing import List, Tuple, Optional, Union, Dict
import uta_star

# PROJECT_PATH = pathlib.Path(__file__).parent
# PROJECT_UI = PROJECT_PATH / "gui_designer.ui"

kryteria = ["Marża", "Prowizja", "RRSO", "Koszt miesięczny", "Wkład własny", 'Opinie']
metody = ["Topsis", "SP-CS", "RSM", "UTA"]


class Kryteria:
    marza = False
    prowizja = False
    RRSO = False
    wklad_wlasny = False
    kryt1 = False
    kryt2 = False


class Metody:
    topsis = False
    sp_cs = False
    rsm = False
    odniesienia = False


class Kryteria:
    marza = False
    prowizja = False
    RRSO = False
    wklad_wlasny = False
    kryt1 = False
    kryt2 = False


class Metody:
    topsis = False
    sp_cs = False
    rsm = False
    odniesienia = False


class Point:
    """
    class representing Point
    """

    def __init__(self, marza=None, prowizja=None, RRSO=None, wklad_wlasny=None, kryt_1=None, kryt_2=None):
        self.marza = marza
        self.prowizja = prowizja
        self.RRSO = RRSO
        self.wklad_wlasny = wklad_wlasny
        self.kryt_1 = kryt_1
        self.kryt_2 = kryt_2

        self.count = 0

    # def __repr__(self):
    #     if self.marza is not None and self.prowizja is not None and self.RRSO is not None:
    #         return f'{self.marza}, {self.prowizja}, {self.RRSO}'
    #
    #     elif self.marza is not None and self.prowizja is not None and self.wklad_wlasny is not None:
    #         return f'{self.marza}, {self.prowizja}, {self.wklad_wlasny}'
    #
    #     elif self.marza is not None and self.prowizja is not None and self.kryt_1 is not None:
    #         return f'{self.marza}; {self.prowizja}, {self.kryt_1}'
    #
    #     elif self.marza is not None and self.prowizja is not None and self.kryt_2 is not None:
    #         return f'{self.marza}; {self.prowizja}, {self.kryt_2}'
    #
    #     elif

    def check_which_are_not_none(self):
        tmp = [self.marza, self.prowizja, self.RRSO, self.wklad_wlasny, self.kryt_1, self.kryt_2]
        return [elem for elem in tmp if elem is not None]

    def __repr__(self):
        tmp = self.check_which_are_not_none()
        if len(tmp) == 3:
            return f'{tmp[0]}, {tmp[1]}, {tmp[2]}'
        elif len(tmp) == 2:
            return f'{tmp[0]}, {tmp[1]}'
        else:
            return 'Error'


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

        self.chbut_status = {}

        self.window = tk.Frame(master)
        self.wybor_kryteriow = None
        self.wybor_metody = None
        self.labelframe1 = None
        self.labelframe2 = None
        self.labelframe3 = None
        self.labelframe4 = None
        # self.label3 = None

        self.active_crits_num = 0
        self.active_meths_num = 0

        self.window.configure(height='900', width='1600')
        self.window.pack(padx='40', pady='20', side='top')
        #self.window.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height

        # Main widget
        self.mainwindow = self.window

    def create_ui_main(self):
        """
        This Function create all LabelFrames in gui app

        :return:
        """
        # Część kodu odpowiadająca za wybór kryteriów
        self.wybor_kryteriow = tk.LabelFrame(self.window)

        # Nwm po co to ale na wszelki wypadek zostawiłem
        # self.label3 = tk.Label(self.wybor_kryteriow)
        # self.label3.configure(text='label3')
        # self.label3.pack(side='top')

        # Uzupełnianie słownika do przechowywania stanów checkbuttonów
        liczba_kryt = len(kryteria)
        liczba_metod = len(metody)
        for i in range(liczba_kryt + liczba_metod):
            self.chbut_status[i] = tk.IntVar()

        self.checkbutton0 = tk.Checkbutton(self.wybor_kryteriow, text=kryteria[0], variable=self.chbut_status[0],
                                           command=lambda: self.update_check())
        self.checkbutton0.pack(side='top', anchor='w')
        self.checkbutton1 = tk.Checkbutton(self.wybor_kryteriow, text=kryteria[1], variable=self.chbut_status[1],
                                           command=lambda: self.update_check())
        self.checkbutton1.pack(side='top', anchor='w')
        self.checkbutton2 = tk.Checkbutton(self.wybor_kryteriow, text=kryteria[2], variable=self.chbut_status[2],
                                           command=lambda: self.update_check())
        self.checkbutton2.pack(side='top', anchor='w')
        self.checkbutton3 = tk.Checkbutton(self.wybor_kryteriow, text=kryteria[3], variable=self.chbut_status[3],
                                           command=lambda: self.update_check())
        self.checkbutton3.pack(side='top', anchor='w')
        self.checkbutton4 = tk.Checkbutton(self.wybor_kryteriow, text=kryteria[4], variable=self.chbut_status[4],
                                           command=lambda: self.update_check())
        self.checkbutton4.pack(side='top', anchor='w')
        self.checkbutton5 = tk.Checkbutton(self.wybor_kryteriow, text=kryteria[5], variable=self.chbut_status[5],
                                           command=lambda: self.update_check())
        self.checkbutton5.pack(side='top', anchor='w')

        self.wybor_kryteriow.configure(height='50', text='KRYTERIA', width='40', labelanchor='n')
        self.wybor_kryteriow.grid(column='0', padx='5', pady='5', row='1', sticky='n')

        # częśc kodu odpowiadająca za wybór metody
        self.wybor_metody = tk.LabelFrame(self.window)

        # To samo co przy label 3
        # self.label4 = tk.Label(self.wybor_metody)
        # self.label4.configure(text='label4')
        # self.label4.pack(side='top')

        self.checkbutton6 = tk.Checkbutton(self.wybor_metody, text=metody[0], variable=self.chbut_status[6])
        self.checkbutton6.pack(side='top', anchor='w')
        self.checkbutton7 = tk.Checkbutton(self.wybor_metody, text=metody[1], variable=self.chbut_status[7])
        self.checkbutton7.pack(side='top', anchor='w')
        self.checkbutton8 = tk.Checkbutton(self.wybor_metody, text=metody[2], variable=self.chbut_status[8])
        self.checkbutton8.pack(side='top', anchor='w')
        self.checkbutton9 = tk.Checkbutton(self.wybor_metody, text=metody[3], variable=self.chbut_status[9])
        self.checkbutton9.pack(side='top', anchor='w')

        self.wybor_metody.configure(height='50', relief='raised', text='METODY', width='25', labelanchor='n')
        self.wybor_metody.grid(column='1', padx='5', pady='5', row='1', sticky='n')

        # Ta część kodu odopowiada za przełączenie się na wybrany ekran metody
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
        self.button8.configure(cursor='arrow', font='{Arial CE} 12 {bold}', text='Licz', command=self.licz_button)
        self.button8.pack(side='top')
        self.labelframe4.configure(height='200', width='200')
        self.labelframe4.grid(column='1', row='3')

    def update_check(self):
        conv_crits_status = [status.get() for status in list(self.chbut_status.values())][:-4]

        self.plot_current_data()

        if conv_crits_status.count(1) == 3:
            if conv_crits_status[0] == 0:
                self.checkbutton0.configure(state='disabled')
            if conv_crits_status[1] == 0:
                self.checkbutton1.configure(state='disabled')
            if conv_crits_status[2] == 0:
                self.checkbutton2.configure(state='disabled')
            if conv_crits_status[3] == 0:
                self.checkbutton3.configure(state='disabled')
            if conv_crits_status[4] == 0:
                self.checkbutton4.configure(state='disabled')
            if conv_crits_status[5] == 0:
                self.checkbutton5.configure(state='disabled')
        else:
            self.checkbutton0.configure(state='normal')
            self.checkbutton1.configure(state='normal')
            self.checkbutton2.configure(state='normal')
            self.checkbutton3.configure(state='normal')
            self.checkbutton4.configure(state='normal')
            self.checkbutton5.configure(state='normal')

    def licz_button(self):
        conv_crits_status = [status.get() for status in list(self.chbut_status.values())]
        if conv_crits_status[:-4].count(1) == 0 and conv_crits_status[6:].count(1) == 0:
            messagebox.showerror('Błąd', 'Musisz wybrać przynajmniej jedno kryterium oraz metodę!')
        elif conv_crits_status[:-4].count(1) == 0:
            messagebox.showerror('Błąd', 'Musisz wybrać przynajmniej jedno kryterium!')
        elif conv_crits_status[6:].count(1) == 0:
            messagebox.showerror('Błąd', 'Musisz wybrać przynajmniej jedną metodę!')
        else:
            status_dict = self.give_statusdict()
            print(status_dict)
            calculator.start_calculations(status_dict)

        chart = FigureCanvasTkAgg(self.figure, self.labelframe3)
        self.print_ranking(data)
        chart.get_tk_widget().pack()

    def run(self):
        """
        Run application
        :return:
        """
        self.create_ui_main()
        self.mainwindow.mainloop()

    def plot_current_data(self):
        conv_crits_status = [status.get() for status in list(self.chbut_status.values())][:-4]

        columns_names = {0:'Marża [%]', 1:'Prowizja [%]', 2:'RRSO [%]', 3:'Koszt miesięczny [PLN]', 4:'Wkład własny [%]', 5:'Opinie[pkt. Max. 5]'}
        crits = []
        for i in range(len(conv_crits_status)):
            if conv_crits_status[i]:
                crits.append(columns_names[i])
        no_of_crits = len(crits)  
        crits.append('Punkt')

        self.labelframe3.destroy()
        self.labelframe3 = tk.LabelFrame(self.window)
        self.labelframe3.configure(height='300', text='Wykres', width='300')



        self.labelframe3.grid(column='1', padx='10', pady='10', row='2')

        self.labelframe3.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        
        
        if no_of_crits != 0:
            df = pd.read_excel(io='dane.xlsx', sheet_name='Arkusz3', index_col=0, usecols=crits)  
  
            indexes = list(df.index)
            values = list(df.values.tolist())
            points = dict(zip(indexes, values))

            if no_of_crits == 1:
                self.figure = self.plot_1d(points)
                pass
            elif no_of_crits == 2:
                self.figure = self.plot_2d(points)
                pass
            elif no_of_crits == 3:
                self.figure = self.plot_3d(points)
                pass
        else:
            pass

    def plot_1d(self, data: Dict):

        x = data.values()
        y = [0] * len(x)

        figure1 = plt.Figure(figsize=(2,3), dpi=100)
        fig = figure1.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure1, master = self.labelframe3)
        canvas.get_tk_widget().pack(fill='both')
        
        fig.grid()
        fig.plot(x, y, 'o')
        canvas.draw()
        
        fig.clear()
        plt.close('all')

    def plot_2d(self, data: Dict):

        x = [tab[0] for tab in list(data.values())]
        y = [tab[1] for tab in list(data.values())]

        figure1 = plt.Figure(figsize=(2,3), dpi=100)
        fig = figure1.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure1, master = self.labelframe3)
        canvas.get_tk_widget().pack(fill='both')
        
        fig.grid()
        fig.plot(x, y, 'o')
        canvas.draw()
        
        fig.clear()
        plt.close('all')


    def plot_3d(self, data: Dict):
        """
        Plot 3 dimensional chart
        :param data:
        :return:
        """
        x = [tab[0] for tab in list(data.values())]
        y = [tab[1] for tab in list(data.values())]
        z = [tab[2] for tab in list(data.values())]

        figure1 = plt.Figure(figsize=(2,3), dpi=100)
        fig = figure1.add_subplot(111)
        fig.axes(projection="3d")
        canvas = FigureCanvasTkAgg(figure1, master = self.labelframe3)
        canvas.get_tk_widget().pack(fill='both')
        
        fig.grid()
        for i in range(len(x)):
            fig.scatter(x[i], y[i], z[i], color='b')
            #fig.text(x[i], y[i], z[i], (key_lst[i]), size=8, zorder=1)
        canvas.draw()
        
        fig.clear()
        plt.close('all')

 
    # def plot_2d(self, data: Dict[str, Point]):
    #     """
    #     Plot 2 dimensional chart
    #     args: data: List[Point]
    #     :return:
    #     """
    #     figure1, ax1 = plt.subplots(figsize=(5, 3), dpi=100)
    #     # data: Dict[str, Point] = self.data_RSM

    #     x = [elem.marza for p, elem in data.items()]
    #     y = [elem.prowizja for p, elem in data.items()]
    #     ax1.scatter(x, y)
    #     for key, coords in data.items():
    #         ax1.annotate(key, (coords.marza, coords.prowizja))
    #     figure1.show()
    #     return figure1

    # def plot_3d(self, data: Dict[str, Point]):
    #     """
    #     Plot 3 dimensional chart
    #     :param data:
    #     :return:
    #     """
    #     figure1 = plt.figure(figsize=(6, 4), dpi=100)
    #     ax1 = plt.axes(projection="3d")

    #     x = [elem.marza for p, elem in data.items()]
    #     y = [elem.prowizja for p, elem in data.items()]
    #     z = [elem.RRSO for p, elem in data.items()]
    #     key_lst = list(data.keys())

    #     for i in range(len(x)):
    #         ax1.scatter(x[i], y[i], z[i], color='b')
    #         ax1.text(x[i], y[i], z[i], (key_lst[i]), size=8, zorder=1)

    #     figure1.show()
    #     return figure1

    def plot_values(self, data):
        """
        Function to plot chart by type of chart
        which we pass to them

        Using then in button operation
        :param data:
        :return:
        """
        if data['Point0'].RRSO is None:
            self.figure = self.plot_2d(data)
        else:
            self.figure = self.plot_3d(data)

        chart = FigureCanvasTkAgg(self.figure, self.labelframe3)
        self.print_ranking(data)
        chart.get_tk_widget().pack()

    def reformat_ranking(self, data: Dict[str, Point]) -> str:
        """
        Function to reformat ranking by that pattern
        'Point name: coords'
        :param data:
        :return: str
        """
        S = ''
        if data['Point0'].RRSO is None:
            for point_name, elem in data.items():
                S += f'{point_name}: ({elem.marza}, {elem.prowizja})\n'
        else:
            for point_name, elem in data.items():
                S += f'{point_name}: ({elem.marza}, {elem.prowizja}, {elem.RRSO})\n'
        return S

    def print_ranking(self, data: Dict[str, Point]) -> None:
        self.string_to_ranking = self.reformat_ranking(data)
        self.text4.insert(tk.INSERT, self.string_to_ranking)

    def refresh(self) -> None:
        """
        This function refresh all app using refresh_button
        :return:
        """
        self.wybor_kryteriow.destroy()
        self.wybor_metody.destroy()
        self.labelframe3.destroy()
        self.labelframe2.destroy()
        self.labelframe1.destroy()
        self.labelframe4.destroy()

        self.create_ui_main()

    def give_statusdict(self):
        return self.chbut_status


class RankingCalculations:
    def __init__(self):
        self.chosen_methods = []
        self.chosen_criteria = []

        self.topsis_result = []
        self.topsis_time = []
        self.spcs_result = []
        self.spcs_time = []
        self.rsm_result = []
        self.rsm_time = []
        self.uta_result = []
        self.uta_time = []

    def start_calculations(self, checkbutton_status: Dict):
        # Konwersja ze słownia do listy samych wartości
        status_list = [status.get() for status in list(checkbutton_status.values())]

        self.chosen_methods = []
        self.chosen_criteria = []

        # Wypełnienie list metod i kryteriów
        for i in range(len(kryteria)):
            self.chosen_criteria.append(status_list.pop(0))
        for i in range(len(metody)):
            self.chosen_methods.append(status_list.pop(0))

        print(self.chosen_methods)
        print(self.chosen_criteria)

        # Wywołanie wybranego algorytmu obliczającego ranking
        if self.chosen_methods[0] == 1:
            self.run_topsis()
        if self.chosen_methods[1] == 1:
            self.run_spcs()
        if self.chosen_methods[2] == 1:
            self.run_rsm()
        if self.chosen_methods[3] == 1:
            self.run_uta()

        print("Obliczenia rozpoczęte")

    def run_topsis(self):
        # self.topsis_result =
        pass

    def run_spcs(self):
        # self.spcs_result =
        pass

    def run_rsm(self):
        if self.rsm_result != []:
            self.rsm_result = []

        columns_names = {0: 'Marża [%]', 1: 'Prowizja [%]', 2: 'RRSO [%]', 3: 'Koszt miesięczny [PLN]',
                         4: 'Wkład własny [%]', 5: 'Opinie[pkt. Max. 5]'}

        crits

    def run_uta(self):

        if self.uta_result != []:
            self.uta_result = []
        columns_names = {0: 'Marża [%]', 1: 'Prowizja [%]', 2: 'RRSO [%]', 3: 'Koszt miesięczny [PLN]',
                         4: 'Wkład własny [%]', 5: 'Opinie[pkt. Max. 5]'}
        crits = []
        for i in range(len(self.chosen_criteria)):
            if self.chosen_criteria[i]:
                crits.append(columns_names[i])
        self.uta_result = uta_star.run(crits)

    def give_results(self):
        results = []
        if self.chosen_methods[0] == 1 and self.topsis_result != []:
            results.append(self.topsis_result)
        if self.chosen_methods[1] == 1 and self.spcs_result != []:
            self.run_spcs(self.spcs_result)
        if self.chosen_methods[2] == 1 and self.topsis_result != []:
            self.run_rsm(self.rsm_result)
        if self.chosen_methods[3] == 1 and self.rsm_result != []:
            self.run_uta(self.uta_result)
        return results

    def reset_selfvals(self):

        pass


def test_Point():
    p = Point(marza=15, RRSO=25, wklad_wlasny=12)
    print(p)


def test_gui():
    root = tk.Tk()
    dataRSM = generete_data()
    dataSPCS = generete_data(dim3=True)
    dataTopsis = generete_data()
    app = GuiDesignerApp(root, data_RSM=dataRSM, data_SP_CS=dataSPCS, data_TOPSIS=dataTopsis)
    calculator = RankingCalculations()
    # print(app.data_RSM)
    # print(dataSPCS.keys())
    app.run()


if __name__ == '__main__':
    # test_Point()
    root = tk.Tk()
    dataRSM = generete_data()
    dataSPCS = generete_data(dim3=True)
    dataTopsis = generete_data()
    app = GuiDesignerApp(root, data_RSM=dataRSM, data_SP_CS=dataSPCS, data_TOPSIS=dataTopsis)
    calculator = RankingCalculations()
    # print(app.data_RSM)
    # print(dataSPCS.keys())
    app.run()
