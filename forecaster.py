# програзирование методом скользящей средней
class Forecaster:
    def __init__(self, values, window):
        self.values = list(values)
        self.window = window

    def forecast(self, n_steps): # список из n_steps значений по прогнозу
        result = []
        data = self.values.copy()
        for _ in range(n_steps):
            avg = sum(data[-self.window:]) / self.window
            result.append(round(avg, 2))
            data.append(avg)
        return result