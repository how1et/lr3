import matplotlib.pyplot as plt

# построение графиков
class Plotter:
    def __init__(self, years: list, gdp: list, gnp: list):
        self.years = years
        self.gdp = gdp
        self.gnp = gnp

    def plot_historical(self, frame): # исторический график
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(self.years, self.gdp, marker='o', label='ВВП', color='blue')
        ax.plot(self.years, self.gnp, marker='s', label='ВНП', color='green')
        ax.set_title('ВВП и ВНП России (2009–2023)')
        ax.set_xlabel('Год')
        ax.set_ylabel('Млрд руб.')
        ax.legend()
        ax.grid(True)
        return fig

    def plot_forecast(self, forecast_years,
                      gdp_forecast, gnp_forecast): # график с прогнозами
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(self.years, self.gdp, marker='o',
                label='ВВП (факт)', color='blue')
        ax.plot(self.years, self.gnp, marker='s',
                label='ВНП (факт)', color='green')
        ax.plot(forecast_years, gdp_forecast, marker='o', linestyle='--',
                label='ВВП (прогноз)', color='cornflowerblue')
        ax.plot(forecast_years, gnp_forecast, marker='s', linestyle='--',
                label='ВНП (прогноз)', color='lightgreen')
        ax.set_title('Прогноз ВВП и ВНП')
        ax.set_xlabel('Год')
        ax.set_ylabel('Млрд руб.')
        ax.legend()
        ax.grid(True)
        return fig