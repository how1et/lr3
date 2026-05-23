import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from load_data import DataLoader
from analyzer import Analyzer
from forecaster import Forecaster
from plotter import Plotter

# главное приложение
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Анализ ВВП и ВНП России")
        self.geometry("950x700")
        self.data = None
        self._build_ui()

    def _build_ui(self):
        # Верхняя панель управления
        ctrl = tk.Frame(self, pady=6)
        ctrl.pack(fill='x', padx=10)

        tk.Button(ctrl, text="Открыть файл",
                  command=self._open_file).pack(side='left', padx=4)

        tk.Label(ctrl, text="Период скользящей средней (n):").pack(
            side='left', padx=(20, 4))
        self.n_var = tk.IntVar(value=3)
        tk.Spinbox(ctrl, from_=2, to=10,
                   textvariable=self.n_var, width=4).pack(side='left')

        tk.Label(ctrl, text="Прогноз на N лет:").pack(
            side='left', padx=(20, 4))
        self.forecast_n_var = tk.IntVar(value=3)
        tk.Spinbox(ctrl, from_=1, to=10,
                   textvariable=self.forecast_n_var, width=4).pack(side='left')

        tk.Button(ctrl, text="Построить прогноз",
                  command=self._show_forecast).pack(side='left', padx=20)

        # ── Вкладки ────────────────────────────────────────────────
        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=True, padx=10, pady=6)

        self.tab_table    = tk.Frame(nb)
        self.tab_chart    = tk.Frame(nb)
        self.tab_forecast = tk.Frame(nb)
        self.tab_stats    = tk.Frame(nb)

        nb.add(self.tab_table,    text="Таблица")
        nb.add(self.tab_chart,    text="График")
        nb.add(self.tab_forecast, text="Прогноз")
        nb.add(self.tab_stats,    text="Статистика")

    # ── Загрузка файла ─────────────────────────────────────────────
    def _open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")])
        if not path:
            return
        loader = DataLoader(path)
        self.data = loader.load()
        self._fill_table()
        self._fill_chart()
        self._fill_stats()

    # Таблица
    def _fill_table(self):
        for w in self.tab_table.winfo_children():
            w.destroy()

        cols = ("Год", "ВВП (млрд руб.)", "ВНП (млрд руб.)",
                "Рост ВВП %", "Рост ВНП %")
        tv = ttk.Treeview(self.tab_table, columns=cols,
                          show='headings', height=15)
        for c in cols:
            tv.heading(c, text=c)
            tv.column(c, anchor='center', width=160)

        years = self.data['годы']
        gdp   = self.data['ввп']
        gnp   = self.data['внп']

        for i, yr in enumerate(years):
            gdp_growth = ("—" if i == 0 else
                f"{(gdp[i]-gdp[i-1])/gdp[i-1]*100:+.1f}%")
            gnp_growth = ("—" if i == 0 else
                f"{(gnp[i]-gnp[i-1])/gnp[i-1]*100:+.1f}%")
            tv.insert('', 'end',
                      values=(yr, gdp[i], gnp[i], gdp_growth, gnp_growth))

        sb = ttk.Scrollbar(self.tab_table,
                           orient='vertical', command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        tv.pack(side='left', fill='both', expand=True, padx=6, pady=6)
        sb.pack(side='left', fill='y', pady=6)

    # Исторический график
    def _fill_chart(self):
        for w in self.tab_chart.winfo_children():
            w.destroy()
        plotter = Plotter(self.data['годы'],
                          self.data['ввп'], self.data['внп'])
        fig = plotter.plot_historical(self.tab_chart)
        FigureCanvasTkAgg(fig, self.tab_chart).get_tk_widget().pack(
            fill='both', expand=True)

    # Прогнозный график
    def _show_forecast(self):
        if not self.data:
            messagebox.showwarning("Нет данных", "Сначала откройте файл.")
            return
        for w in self.tab_forecast.winfo_children():
            w.destroy()

        n = self.n_var.get()
        steps = self.forecast_n_var.get()
        last_yr = self.data['годы'][-1]
        f_years = list(range(last_yr + 1, last_yr + steps + 1))

        gdp_fc = Forecaster(self.data['ввп'], n).forecast(steps)
        gnp_fc = Forecaster(self.data['внп'], n).forecast(steps)

        plotter = Plotter(self.data['годы'],
                          self.data['ввп'], self.data['внп'])
        fig = plotter.plot_forecast(f_years, gdp_fc, gnp_fc)
        FigureCanvasTkAgg(fig, self.tab_forecast).get_tk_widget().pack(
            fill='both', expand=True)

    # Статистика
    def _fill_stats(self):
        for w in self.tab_stats.winfo_children():
            w.destroy()
        an = Analyzer(self.data['годы'],
                      self.data['ввп'], self.data['внп'])

        lines = []
        yr, pct = an.max_growth_percent(self.data['ввп'])
        lines.append(f"ВВП — максимальный рост: {yr} год ({pct:+}%)")
        yr, pct = an.max_fall_percent(self.data['ввп'])
        lines.append(f"ВВП — максимальное падение: {yr} год ({pct:+}%)")
        yr, pct = an.max_growth_percent(self.data['внп'])
        lines.append(f"ВНП — максимальный рост: {yr} год ({pct:+}%)")
        yr, pct = an.max_fall_percent(self.data['внп'])
        lines.append(f"ВНП — максимальное падение: {yr} год ({pct:+}%)")

        for line in lines:
            tk.Label(self.tab_stats, text=line,
                     font=("Arial", 12), anchor='w').pack(
                fill='x', padx=20, pady=8)


if __name__ == "__main__":
    App().mainloop()