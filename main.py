import tkinter as tk
from tkinter import ttk


SAMPLE_DATA = [
    (2019, 109241, 107380, "—",       "—"),
    (2020, 106968, 105310, "-2.1%",   "-1.9%"),
    (2021, 131015, 128650, "+22.5%",  "+22.2%"),
    (2022, 151455, 148870, "+15.6%",  "+15.7%"),
    (2023, 171041, 168310, "+12.9%",  "+13.1%"),
]

STATS = [
    "ВВП — максимальный рост: 2021 год (+22.5%)",
    "ВВП — максимальное падение: 2020 год (-2.1%)",
    "ВНП — максимальный рост: 2021 год (+22.2%)",
    "ВНП — максимальное падение: 2020 год (-1.9%)",
]

GDP_VALUES = [109241, 106968, 131015, 151455, 171041]
GNP_VALUES = [107380, 105310, 128650, 148870, 168310]
YEARS      = [2019,   2020,   2021,   2022,   2023]


class MockupApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Анализ ВВП и ВНП России")
        self.geometry("950x700")
        self.resizable(False, False)
        self._build_ui()

    # Верхняя панель управления
    def _build_ui(self):
        ctrl = tk.Frame(self, pady=6)
        ctrl.pack(fill='x', padx=10)

        tk.Button(ctrl, text="Открыть файл",).pack(side='left', padx=4)

        tk.Label(ctrl, text="Период скользящей средней (n):").pack(
            side='left', padx=(20, 4))
        n_var = tk.IntVar(value=3)
        tk.Spinbox(ctrl, from_=2, to=10, textvariable=n_var,
                   width=4).pack(side='left')

        tk.Label(ctrl, text="Прогноз на N лет:").pack(
            side='left', padx=(20, 4))
        fc_var = tk.IntVar(value=3)
        tk.Spinbox(ctrl, from_=1, to=10, textvariable=fc_var,
                   width=4, state='disabled').pack(side='left')

        tk.Button(ctrl, text="Построить прогноз").pack(side='left', padx=20)

        #  Вкладки
        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=True, padx=10, pady=6)

        tab_table    = tk.Frame(nb)
        tab_chart    = tk.Frame(nb)
        tab_forecast = tk.Frame(nb)
        tab_stats    = tk.Frame(nb)

        nb.add(tab_table,    text="Таблица")
        nb.add(tab_chart,    text="График")
        nb.add(tab_forecast, text="Прогноз")
        nb.add(tab_stats,    text="Статистика")

        self._fill_table(tab_table)


    # Таблица
    def _fill_table(self, frame):
        cols = ("Год", "ВВП (млрд руб.)", "ВНП (млрд руб.)",
                "Рост ВВП %", "Рост ВНП %")
        tv = ttk.Treeview(frame, columns=cols, show='headings', height=15)
        for c in cols:
            tv.heading(c, text=c)
            tv.column(c, anchor='center', width=160)

        for row in SAMPLE_DATA:
            tv.insert('', 'end', values=row)

        sb = ttk.Scrollbar(frame, orient='vertical', command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        tv.pack(side='left', fill='both', expand=True, padx=6, pady=6)
        sb.pack(side='left', fill='y', pady=6)



if __name__ == "__main__":
    MockupApp().mainloop()