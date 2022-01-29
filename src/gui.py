import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
from typing import List, Tuple, Optional, Union, Dict
import uta_star as uta_star
import rsm as rsm
import fuzzy_topsis as ftopsis
import sp_cs as sp_cs


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
    def __init__(self, master=None, data_RSM=None, data_TOPSIS=None, data_SP_CS=None, data_UTA=None):
        # build ui
        self.data_RSM: Optional[Dict[str, List[Point]], None] = data_RSM
        self.data_TOPSIS: Optional[Dict[str, List[Point]], None] = data_TOPSIS
        self.data_SP_CS: Optional[Dict[str, List[Point]], None] = data_SP_CS
        self.data_UTA: Optional[Dict[str, List[Point]], None] = data_UTA

        # Czy obiekt calculator ma być w tym miejscu?
        self.calculator = RankingCalculations()

        self.conv_crits_status = None

        self.string_to_ranking: Optional[str, None] = None

        self.figure = None

        self.chbut_status = {}
        self.spins_status = {}
        self.ranges = {}

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

        self.window.configure(height='1920', width='1080')
        self.window.pack(padx='40', pady='20', side='top')

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

        self.invisible_text = tk.Label(self.wybor_kryteriow, height='1', text=' ', font=("Arial", 10, 'bold'),
                                       width='1')
        self.invisible_text.pack(side='top', anchor='w')

        self.checkbutton0 = tk.Checkbutton(self.wybor_kryteriow, text=kryteria[0], variable=self.chbut_status[0],
                                           command=lambda: self.update_check())
        self.checkbutton0.pack(side='top', pady='3', padx='1', anchor='w')
        self.checkbutton1 = tk.Checkbutton(self.wybor_kryteriow, text=kryteria[1], variable=self.chbut_status[1],
                                           command=lambda: self.update_check())
        self.checkbutton1.pack(side='top', anchor='w')
        self.checkbutton2 = tk.Checkbutton(self.wybor_kryteriow, text=kryteria[2], variable=self.chbut_status[2],
                                           command=lambda: self.update_check())
        self.checkbutton2.pack(side='top', pady='3', padx='1', anchor='w')
        self.checkbutton3 = tk.Checkbutton(self.wybor_kryteriow, text=kryteria[3], variable=self.chbut_status[3],
                                           command=lambda: self.update_check())
        self.checkbutton3.pack(side='top', pady='3', padx='1', anchor='w')
        self.checkbutton4 = tk.Checkbutton(self.wybor_kryteriow, text=kryteria[4], variable=self.chbut_status[4],
                                           command=lambda: self.update_check())
        self.checkbutton4.pack(side='top', pady='3', padx='1', anchor='w')
        self.checkbutton5 = tk.Checkbutton(self.wybor_kryteriow, text=kryteria[5], variable=self.chbut_status[5],
                                           command=lambda: self.update_check())
        self.checkbutton5.pack(side='top', pady='3', padx='1', anchor='w')

        self.wybor_kryteriow.configure(height='215', relief='raised', text='KRYTERIA', font=("Arial", 10, 'bold'),
                                       width='150', labelanchor='n')
        self.wybor_kryteriow.grid(column='0', padx='40', pady='5', row='1', sticky='n')
        self.wybor_kryteriow.pack_propagate(0)

        # częśc kodu odpowiadająca za wybór metody
        self.wybor_metody = tk.LabelFrame(self.window)

        # To samo co przy label 3
        # self.label4 = tk.Label(self.wybor_metody)
        # self.label4.configure(text='label4')
        # self.label4.pack(side='top')

        self.invisible_text = tk.Label(self.wybor_metody, height='1', text=' ', font=("Arial", 10, 'bold'), width='1')
        self.invisible_text.pack(side='top', anchor='w')

        self.checkbutton6 = tk.Checkbutton(self.wybor_metody, text=metody[0], variable=self.chbut_status[6],
                                           command=lambda: self.update_check())
        self.checkbutton6.pack(side='top', pady='3', padx='1', anchor='w')
        self.checkbutton7 = tk.Checkbutton(self.wybor_metody, text=metody[1], variable=self.chbut_status[7],
                                           command=lambda: self.update_check())
        self.checkbutton7.pack(side='top', pady='3', padx='1', anchor='w')
        self.checkbutton8 = tk.Checkbutton(self.wybor_metody, text=metody[2], variable=self.chbut_status[8],
                                           command=lambda: self.update_check())
        self.checkbutton8.pack(side='top', pady='3', padx='1', anchor='w')
        self.checkbutton9 = tk.Checkbutton(self.wybor_metody, text=metody[3], variable=self.chbut_status[9],
                                           command=lambda: self.update_check())
        self.checkbutton9.pack(side='top', pady='3', padx='1', anchor='w')

        self.wybor_metody.configure(height='215', relief='raised', text='METODY', font=("Arial", 10, 'bold'),
                                    width='150', labelanchor='n')
        self.wybor_metody.grid(column='2', padx='40', pady='5', row='1', sticky='n')
        self.wybor_metody.pack_propagate(0)

        # Ta część kodu odopowiada za przełączenie się na wybrany ekran metody
        self.labelframe1 = tk.LabelFrame(self.window)
        self.text4 = tk.Text(self.labelframe1)
        self.text4.configure(blockcursor='false', height='10', relief='flat', takefocus=False)
        self.text4.configure(width='20')
        self.text4.grid(column='2', row='2', sticky='nw')

        self.labelframe1.configure(height='500', text='RANKING', font=("Arial", 10, 'bold'), width='250',
                                   labelanchor='n')
        self.labelframe1.grid(column='2', row='2', pady='20', padx='20', sticky='n')
        self.labelframe1.pack_propagate(0)

        self.labelframe2 = tk.LabelFrame(self.window)
        self.button2 = tk.Button(self.labelframe2)
        self.button2.configure(text='Dane')
        self.button2.pack(side='left')

        self.refresh_button = tk.Button(self.labelframe2, text='Refresh')
        self.refresh_button.configure(command=self.refresh)
        self.refresh_button.pack(side='left')

        self.labelframe2.configure(height='200', text='MENU', font=("Arial", 10, 'bold'), width='200')
        self.labelframe2.grid(column='0', row='0', sticky='n')

        self.labelframe3 = tk.LabelFrame(self.window)
        self.labelframe3.configure(height='400', text='WYKRES DANYCH', font=("Arial", 10, 'bold'), width='400',
                                   labelanchor='n')
        self.labelframe3.grid(column='0', padx='40', pady='20', row='2', columnspan='2', rowspan='2')

        self.labelframe4 = tk.LabelFrame(self.window)
        self.button8 = tk.Button(self.labelframe4)
        self.button8.configure(cursor='arrow', width='15', height='2', font='{Arial CE} 12 {bold}',
                               text='UTWÓRZ RANKING', command=self.licz_button)
        self.button8.pack(side='top')
        self.labelframe4.configure(height='200', width='200')
        self.labelframe4.grid(column='2', row='3', pady='90')

        self.labelframe5 = tk.LabelFrame(self.window)
        self.labelframe5.configure(height='700', relief='raised', text='DODATKOWE PARAMETRY',
                                   font=("Arial", 10, 'bold'), width='700', labelanchor='n')
        self.labelframe5.grid(column='1', row='1', padx='20', pady='5', sticky='n')

        # Obsługa spinboxów 
        columns_names = ['Marża [%]', 'Prowizja [%]', 'RRSO [%]', 'Koszt miesięczny [PLN]', 'Wkład własny [%]',
                         'Opinie[pkt. Max. 5]', 'Punkt']
        df = pd.read_excel(io='dane.xlsx', sheet_name='Arkusz3', index_col=0, usecols=columns_names)
        text_font = ("Courier", 14)

        for i, crit in enumerate(columns_names[:-1]):
            dec = 2
            if i == 0:
                crit1_text = tk.Label(master=self.labelframe5, text="[%]", font=text_font)
                crit1_text.grid(row='1', column='2')
            elif i == 1:
                crit2_text = tk.Label(master=self.labelframe5, text="[%]", font=text_font)
                crit2_text.grid(row='2', column='2')
            elif i == 2:
                crit3_text = tk.Label(master=self.labelframe5, text="[%]", font=text_font)
                crit3_text.grid(row='3', column='2')
            elif i == 3:
                crit4_text = tk.Label(master=self.labelframe5, text="[PLN]", font=text_font)
                crit4_text.grid(row='4', column='2')
                crit_vals = df[crit]
                min_val = crit_vals.min()
                max_val = crit_vals.max()
                first_range = (np.linspace(min_val, min_val + (max_val - min_val) / 2, 50)).astype('int')
                second_range = (np.linspace(min_val + (max_val - min_val) / 2, max_val, 50)).astype('int')
                self.ranges[i] = [tuple(first_range), tuple(second_range)]
                self.spins_status[i] = [tk.StringVar(), tk.StringVar()]
                continue
            elif i == 4:
                crit5_text = tk.Label(master=self.labelframe5, text="[%]", font=text_font)
                crit5_text.grid(row='5', column='2')
            elif i == 5:
                crit6_text = tk.Label(master=self.labelframe5, text="[-]", font=text_font)
                crit6_text.grid(row='6', column='2')
                crit_vals = df[crit]
                min_val = crit_vals.min()
                max_val = crit_vals.max()
                first_range = np.around(np.linspace(min_val, min_val + (max_val - min_val) / 2, 50), decimals=dec)
                second_range = np.around(np.linspace(min_val + (max_val - min_val) / 2, max_val, 50), decimals=dec)
                self.ranges[i] = [tuple(second_range), tuple(first_range)]
                self.spins_status[i] = [tk.StringVar(), tk.StringVar()]
                continue

            crit_vals = df[crit]
            min_val = crit_vals.min()
            max_val = crit_vals.max()
            first_range = np.around(np.linspace(min_val, min_val + (max_val - min_val) / 2, 50), decimals=dec)
            second_range = np.around(np.linspace(min_val + (max_val - min_val) / 2, max_val, 50), decimals=dec)
            self.ranges[i] = [tuple(first_range), tuple(second_range)]
            self.spins_status[i] = [tk.StringVar(), tk.StringVar()]
            # self.spins_status[i] = [tk.StringVar(value=str(first_range[49])), tk.StringVar(value=str(second_range[49]))]

        legend1_text = tk.Label(master=self.labelframe5, text="Punkt quo-1", font=("Arial", 8))
        legend1_text.grid(row='0', column='0')

        legend2_text = tk.Label(master=self.labelframe5, text="Punkt quo-2", font=("Arial", 8))
        legend2_text.grid(row='0', column='1')

        legend3_text = tk.Label(master=self.labelframe5, text="Jednostki", font=("Arial", 8))
        legend3_text.grid(row='0', column='2')

        self.spinbox0 = tk.Spinbox(master=self.labelframe5, width=5, values=self.ranges[0][0],
                                   textvariable=self.spins_status[0][0], command=lambda: self.update_spinbox())
        self.spinbox0.grid(row='1', column='0', padx='10', pady='5')

        self.spinbox1 = tk.Spinbox(master=self.labelframe5, width=5, values=self.ranges[0][1],
                                   textvariable=self.spins_status[0][1], command=lambda: self.update_spinbox())
        self.spinbox1.grid(row='1', column='1', padx='10', pady='5')

        self.spinbox2 = tk.Spinbox(master=self.labelframe5, width=5, values=self.ranges[1][0],
                                   textvariable=self.spins_status[1][0], command=lambda: self.update_spinbox())
        self.spinbox2.grid(row='2', column='0', padx='10', pady='5')

        self.spinbox3 = tk.Spinbox(master=self.labelframe5, width=5, values=self.ranges[1][1],
                                   textvariable=self.spins_status[1][1], command=lambda: self.update_spinbox())
        self.spinbox3.grid(row='2', column='1', padx='10', pady='5')

        self.spinbox4 = tk.Spinbox(master=self.labelframe5, width=5, values=self.ranges[2][0],
                                   textvariable=self.spins_status[2][0], command=lambda: self.update_spinbox())
        self.spinbox4.grid(row='3', column='0', padx='10', pady='5')

        self.spinbox5 = tk.Spinbox(master=self.labelframe5, width=5, values=self.ranges[2][1],
                                   textvariable=self.spins_status[2][1], command=lambda: self.update_spinbox())
        self.spinbox5.grid(row='3', column='1', padx='10', pady='5')

        self.spinbox6 = tk.Spinbox(master=self.labelframe5, width=5, values=self.ranges[3][0],
                                   textvariable=self.spins_status[3][0], command=lambda: self.update_spinbox())
        self.spinbox6.grid(row='4', column='0', padx='10', pady='5')

        self.spinbox7 = tk.Spinbox(master=self.labelframe5, width=5, values=self.ranges[3][1],
                                   textvariable=self.spins_status[3][1], command=lambda: self.update_spinbox())
        self.spinbox7.grid(row='4', column='1', padx='10', pady='5')

        self.spinbox8 = tk.Spinbox(master=self.labelframe5, width=5, values=self.ranges[4][0],
                                   textvariable=self.spins_status[4][0], command=lambda: self.update_spinbox())
        self.spinbox8.grid(row='5', column='0', padx='10', pady='5')

        self.spinbox9 = tk.Spinbox(master=self.labelframe5, width=5, values=self.ranges[4][1],
                                   textvariable=self.spins_status[4][1], command=lambda: self.update_spinbox())
        self.spinbox9.grid(row='5', column='1', padx='10', pady='5')

        self.spinbox10 = tk.Spinbox(master=self.labelframe5, width=5, values=self.ranges[5][0],
                                    textvariable=self.spins_status[5][0], command=lambda: self.update_spinbox())
        self.spinbox10.grid(row='6', column='0', padx='10', pady='5')

        self.spinbox11 = tk.Spinbox(master=self.labelframe5, width=5, values=self.ranges[5][1],
                                    textvariable=self.spins_status[5][1], command=lambda: self.update_spinbox())
        self.spinbox11.grid(row='6', column='1', padx='10', pady='5')

        self.update_spinbox()

    def update_spinbox(self):
        conv_crits_status = [status.get() for status in list(self.chbut_status.values())]

        if any(conv_crits_status[6:9]):
            if conv_crits_status[0]:
                self.spinbox0.config(state='normal')
                self.spinbox1.config(state='normal')
            else:
                self.spinbox0.config(state='disabled')
                self.spinbox1.config(state='disabled')
            if conv_crits_status[1]:
                self.spinbox2.config(state='normal')
                self.spinbox3.config(state='normal')
            else:
                self.spinbox2.config(state='disabled')
                self.spinbox3.config(state='disabled')
            if conv_crits_status[2]:
                self.spinbox4.config(state='normal')
                self.spinbox5.config(state='normal')
            else:
                self.spinbox4.config(state='disabled')
                self.spinbox5.config(state='disabled')
            if conv_crits_status[3]:
                self.spinbox6.config(state='normal')
                self.spinbox7.config(state='normal')
            else:
                self.spinbox6.config(state='disabled')
                self.spinbox7.config(state='disabled')
            if conv_crits_status[4]:
                self.spinbox8.config(state='normal')
                self.spinbox9.config(state='normal')
            else:
                self.spinbox8.config(state='disabled')
                self.spinbox9.config(state='disabled')
            if conv_crits_status[5]:
                self.spinbox10.config(state='normal')
                self.spinbox11.config(state='normal')
            else:
                self.spinbox10.config(state='disabled')
                self.spinbox11.config(state='disabled')
        else:
            self.spinbox0.config(state='disabled')
            self.spinbox1.config(state='disabled')
            self.spinbox2.config(state='disabled')
            self.spinbox3.config(state='disabled')
            self.spinbox4.config(state='disabled')
            self.spinbox5.config(state='disabled')
            self.spinbox6.config(state='disabled')
            self.spinbox7.config(state='disabled')
            self.spinbox8.config(state='disabled')
            self.spinbox9.config(state='disabled')
            self.spinbox10.config(state='disabled')
            self.spinbox11.config(state='disabled')

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

        self.update_spinbox()

    def licz_button(self):
        self.labelframe1 = tk.LabelFrame(self.window)
        self.text4 = tk.Text(self.labelframe1)
        self.text4.configure(blockcursor='false', height='10', relief='flat', takefocus=False)
        self.text4.configure(width='20')
        self.text4.grid(column='2', row='2', sticky='nw')

        self.labelframe1.configure(height='500', text='RANKING', font=("Arial", 10, 'bold'), width='250',
                                   labelanchor='n')
        self.labelframe1.grid(column='2', row='2', pady='20', padx='20', sticky='n')
        self.labelframe1.pack_propagate(0)

        conv_crits_status = [status.get() for status in list(self.chbut_status.values())]
        if conv_crits_status[:-4].count(1) == 0 and conv_crits_status[6:].count(1) == 0:
            messagebox.showerror('Błąd', 'Musisz wybrać przynajmniej jedno kryterium oraz metodę!')
        elif conv_crits_status[:-4].count(1) == 0:
            messagebox.showerror('Błąd', 'Musisz wybrać przynajmniej jedno kryterium!')
        elif conv_crits_status[6:].count(1) == 0:
            messagebox.showerror('Błąd', 'Musisz wybrać przynajmniej jedną metodę!')
        else:
            status_dict = self.give_statusdict()
            status_dict2 = self.give_statusdict2()
            self.calculator.start_calculations(status_dict, status_dict2)
            self.data_RSM = self.calculator.rsm_result
            self.data_UTA = self.calculator.uta_result
            self.data_SP_CS = self.calculator.spcs_result
            self.data_TOPSIS = self.calculator.topsis_result
        # chart = FigureCanvasTkAgg(self.figure, self.labelframe3)
        if conv_crits_status[6] == 1:
            self.print_ranking(self.data_TOPSIS)
            self.plot_values(self.data_TOPSIS)

        elif conv_crits_status[7] == 1:
            self.print_ranking(self.data_SP_CS)
            self.plot_values(self.data_SP_CS)

        elif conv_crits_status[8] == 1:
            self.print_ranking(self.data_RSM)
            self.plot_values(self.data_RSM)

        elif conv_crits_status[9] == 1:
            self.print_ranking(self.data_UTA)
            self.plot_values(self.data_UTA)

        # chart.get_tk_widget().pack()

    def run(self):
        """
        Run application
        :return:
        """
        self.create_ui_main()
        self.mainwindow.mainloop()

    def plot_current_data(self):
        conv_crits_status = [status.get() for status in list(self.chbut_status.values())][:-4]

        columns_names = {0: 'Marża [%]', 1: 'Prowizja [%]', 2: 'RRSO [%]', 3: 'Koszt miesięczny [PLN]',
                         4: 'Wkład własny [%]', 5: 'Opinie[pkt. Max. 5]'}
        crits = []
        for i in range(len(conv_crits_status)):
            if conv_crits_status[i]:
                crits.append(columns_names[i])
        no_of_crits = len(crits)
        crits.append('Punkt')

        self.labelframe3.destroy()
        self.labelframe3 = tk.LabelFrame(self.window)
        self.labelframe3.configure(height='400', text='WYKRES DANYCH', font=("Arial", 10, 'bold'), width='400',
                                   labelanchor='n')
        self.labelframe3.grid(column='0', padx='40', pady='20', row='2', columnspan='2', rowspan='2')

        self.labelframe3.pack_propagate(0)  # Don't allow the widgets inside to determine the frame's width / height

        if no_of_crits != 0:
            df = pd.read_excel(io='dane.xlsx', sheet_name='Arkusz3', index_col=0, usecols=crits)

            indexes = list(df.index)
            values = list(df.values.tolist())
            points = dict(zip(indexes, values))

            # if no_of_crits == 1:
            #     self.figure = self.plot_1d(points)
            # elif no_of_crits == 2:
            #     self.figure = self.plot_2d(points)
            # elif no_of_crits == 3:
            #     self.figure = self.plot_3d(points)
            #     pass
        else:
            pass

    # def plot_1d(self, data: Dict):
    #
    #     x = data.values()
    #     y = [0] * len(x)
    #
    #     figure1 = plt.Figure(figsize=(2, 4), dpi=100)
    #     fig = figure1.add_subplot(111)
    #     canvas = FigureCanvasTkAgg(figure1, master=self.labelframe3)
    #     canvas.get_tk_widget().pack(fill='both')
    #
    #     fig.grid()
    #     fig.plot(x, y, 'o')
    #     canvas.draw()
    #
    #     fig.clear()
    #     plt.close('all')

    # def plot_2d(self, data: Dict):
    #
    #     x = [tab[0] for tab in list(data.values())]
    #     y = [tab[1] for tab in list(data.values())]
    #
    #     figure1 = plt.Figure(figsize=(2, 4), dpi=100)
    #     fig = figure1.add_subplot(111)
    #     canvas = FigureCanvasTkAgg(figure1, master=self.labelframe3)
    #     canvas.get_tk_widget().pack(fill='both')
    #
    #     fig.grid()
    #     fig.plot(x, y, 'o')
    #     canvas.draw()
    #
    #     fig.clear()
    #     plt.close('all')

    # def plot_3d(self, data: Dict):
    #     """
    #     Plot 3 dimensional chart
    #     :param data:
    #     :return:
    #     """
    #     x = [tab[0] for tab in list(data.values())]
    #     y = [tab[1] for tab in list(data.values())]
    #     z = [tab[2] for tab in list(data.values())]
    #
    #     figure1 = plt.Figure(figsize=(2, 3), dpi=100)
    #     fig = figure1.add_subplot(111)
    #     fig.axes(projection="3d")
    #     canvas = FigureCanvasTkAgg(figure1, master=self.labelframe3)
    #     canvas.get_tk_widget().pack(fill='both')
    #
    #     fig.grid()
    #     for i in range(len(x)):
    #         fig.scatter(x[i], y[i], z[i], color='b')
    #         # fig.text(x[i], y[i], z[i], (key_lst[i]), size=8, zorder=1)
    #     canvas.draw()
    #
    #     fig.clear()
    #     plt.close('all')

    def plot_2d(self, data: Dict[str, List]):
        """
        Plot 2 dimensional chart
        args: data: List[Point]
        :return:
        """
        figure1, ax1 = plt.subplots(figsize=(5, 3), dpi=100)
        # data: Dict[str, Point] = self.data_RSM

        x = [tab[0] for tab in list(data.values())]
        y = [tab[1] for tab in list(data.values())]
        ax1.scatter(x, y)
        for key, coords in data.items():
            ax1.annotate(key, (coords[0], coords[1]))
        figure1.show()
        return figure1

    def plot_3d(self, data: Dict[str, List]):
        """
        Plot 3 dimensional chart
        :param data:
        :return:
        """
        figure1 = plt.figure(figsize=(6, 4), dpi=100)
        ax1 = plt.axes(projection="3d")

        x = [tab[0] for tab in list(data.values())]
        y = [tab[1] for tab in list(data.values())]
        z = [tab[2] for tab in list(data.values())]
        key_lst = list(data.keys())

        for i in range(len(x)):
            ax1.scatter(x[i], y[i], z[i], color='b')
            ax1.text(x[i], y[i], z[i], (key_lst[i]), size=8, zorder=1)

        figure1.show()
        return figure1

    def plot_values(self, data):
        """
        Function to plot chart by type of chart
        which we pass to them

        Using then in button operation
        :param data:
        :return:
        """
        values = list(data.values())
        print(values)
        if len(values[0]) == 3:
            self.figure = self.plot_3d(data)
        elif len(values[0]) == 2:
            self.figure = self.plot_2d(data)

        chart = FigureCanvasTkAgg(self.figure, self.labelframe3)
        chart.get_tk_widget().pack()

    def reformat_ranking(self, data: Dict[str, List]) -> str:
        """
        Function to reformat ranking by that pattern
        'Point name: coords'
        :param data:
        :return: str
        """
        S = ''
        if len(list(data.values())[0]) == 2:
            for point_name, elem in data.items():
                S += f'{point_name}: ({elem[0]}, {elem[1]})\n'
        else:
            for point_name, elem in data.items():
                S += f'{point_name}: ({elem[0]}, {elem[1]}, {elem[2]})\n'
        return S

    def print_ranking(self, data: Dict[str, List]) -> None:
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

    def give_statusdict2(self):
        return self.spins_status


class RankingCalculations:
    def __init__(self):
        self.chosen_methods = []
        # [data.columns]
        self.chosen_criteria = []
        self.quo1 = []
        self.quo2 = []

        self.topsis_result = {}
        self.topsis_time = []
        self.spcs_result = {}
        self.spcs_time = []
        self.rsm_result = {}
        self.rsm_time = []
        self.uta_result = {}
        self.uta_time = []

    def start_calculations(self, checkbutton_status: Dict, spiners_status: Dict):
        # Konwersja ze słownia do listy samych wartości
        status_list = [status.get() for status in list(checkbutton_status.values())]

        self.chosen_methods = []
        self.chosen_criteria = []
        self.quo1 = [float(stat[0].get()) for stat in spiners_status.values()]
        self.quo2 = [float(stat[1].get()) for stat in spiners_status.values()]
        # Wypełnienie list metod i kryteriów
        for i in range(len(kryteria)):
            self.chosen_criteria.append(status_list.pop(0))
        for i in range(len(metody)):
            self.chosen_methods.append(status_list.pop(0))

        # print(self.chosen_methods)
        # print(self.chosen_criteria)

        # Wywołanie wybranego algorytmu obliczającego ranking
        # if self.chosen_methods[0] == 1:
        #     self.run_topsis()
        # if self.chosen_methods[1] == 1:
        #     self.run_spcs()
        # if self.chosen_methods[2] == 1:
        #     self.run_rsm()
        # if self.chosen_methods[3] == 1:
        #     self.run_uta()
        self.give_results()

        print("Obliczenia rozpoczęte")

    def run_topsis(self):
        if self.topsis_result != {}:
            self.topsis_result = {}

        columns_names = {0: 'Marża [%]', 1: 'Prowizja [%]', 2: 'RRSO [%]', 3: 'Koszt miesięczny [PLN]',
                         4: 'Wkład własny [%]', 5: 'Opinie[pkt. Max. 5]'}

        crits = ['Punkt']
        chosen_quo1 = []
        chosen_quo2 = []
        for i in range(len(self.chosen_criteria)):
            if self.chosen_criteria[i]:
                crits.append(columns_names[i])
                chosen_quo1.append(self.quo1[i])
                chosen_quo2.append(self.quo2[i])
        self.topsis_result = ftopsis.run_topsis(chosen_quo1, chosen_quo2, crits)

    def run_spcs(self):
        if self.spcs_result != {}:
            self.spcs_result = {}

        columns_names = {0: 'Marża [%]', 1: 'Prowizja [%]', 2: 'RRSO [%]', 3: 'Koszt miesięczny [PLN]',
                         4: 'Wkład własny [%]', 5: 'Opinie[pkt. Max. 5]'}

        crits = ['Punkt']
        chosen_quo1 = []
        chosen_quo2 = []
        for i in range(len(self.chosen_criteria)):
            if self.chosen_criteria[i]:
                crits.append(columns_names[i])
                chosen_quo1.append(self.quo1[i])
                chosen_quo2.append(self.quo2[i])
        self.spcs_result = sp_cs.run_sp_cs(chosen_quo1, chosen_quo2, crits)

    def run_rsm(self):
        if self.rsm_result != {}:
            self.rsm_result = {}

        columns_names = {0: 'Marża [%]', 1: 'Prowizja [%]', 2: 'RRSO [%]', 3: 'Koszt miesięczny [PLN]',
                         4: 'Wkład własny [%]', 5: 'Opinie[pkt. Max. 5]'}

        crits = ['Punkt']
        chosen_quo1 = []
        chosen_quo2 = []
        for i in range(len(self.chosen_criteria)):
            if self.chosen_criteria[i]:
                crits.append(columns_names[i])
                chosen_quo1.append(self.quo1[i])
                chosen_quo2.append(self.quo2[i])
        self.rsm_result = rsm.run_rsm(chosen_quo1, chosen_quo2, crits)

    def run_uta(self):

        if self.uta_result != {}:
            self.uta_result = {}
        columns_names = {0: 'Marża [%]', 1: 'Prowizja [%]', 2: 'RRSO [%]', 3: 'Koszt miesięczny [PLN]',
                         4: 'Wkład własny [%]', 5: 'Opinie[pkt. Max. 5]'}
        # crits = ['Punkt']
        crits = []
        for i in range(len(self.chosen_criteria)):
            if self.chosen_criteria[i]:
                crits.append(columns_names[i])
        self.uta_result = uta_star.run(crits)

    def give_results(self):
        if self.chosen_methods[0] == 1:
            self.run_topsis()
        if self.chosen_methods[1] == 1:
            self.run_spcs()
        if self.chosen_methods[2] == 1:
            self.run_rsm()
        if self.chosen_methods[3] == 1:
            self.run_uta()

    def reset_selfvals(self):
        pass


# def test_gui():
#     root = tk.Tk()
#     dataRSM = generete_data()
#     dataSPCS = generete_data(dim3=True)
#     dataTopsis = generete_data()
#     app = GuiDesignerApp(root, data_RSM=dataRSM, data_SP_CS=dataSPCS, data_TOPSIS=dataTopsis)
#     calculator = RankingCalculations()
#     # print(app.data_RSM)
#     # print(dataSPCS.keys())
#     app.run()


if __name__ == '__main__':
    root = tk.Tk()
    # print('rsm', calculator.rsm_result)
    # dataRSM = calculator.rsm_result
    # dataSPCS = calculator.spcs_result
    # dataTopsis = calculator.topsis_result
    # dataUTA = calculator.uta_result
    app = GuiDesignerApp(root)
    calculator = RankingCalculations()
    # print(app.data_RSM)
    # print(dataSPCS.keys())
    app.run()
