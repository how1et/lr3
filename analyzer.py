# класс для обработки данных
class Analyzer:
    def __init__(self, years, gdp, gnp):
        self.years = years
        self.gdp = gdp
        self.gnp = gnp

    def max_growth_percent(self, values): # возвращает год с наибольшим ростом
        best_year, best_pct = None, -10 ** 9
        for i in range(1, len(values)):
            pct = (values[i] - values[i - 1]) / values[i - 1] * 100
            if pct > best_pct:
                best_pct = pct
                best_year = self.years[i]
        return best_year, round(best_pct, 2)

    def max_fall_percent(self, values): # возвращает год с наименьшим падением
        worst_year, worst_pct = None, 10 ** 9
        for i in range(1, len(values)):
            pct = (values[i] - values[i - 1]) / values[i - 1] * 100
            if pct < worst_pct:
                worst_pct = pct
                worst_year = self.years[i]
        return worst_year, round(worst_pct, 2)