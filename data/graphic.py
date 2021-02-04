import matplotlib.pyplot as plt
from data.work_with_db import count_data_for_graph


def plot_graph():
    left, height = [], []
    for k, v in count_data_for_graph().items():
        left.append(k)
        height.append(v)
    month = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь',
             'декабрь']
    tick_label = [month[mon - 1] for mon in left]
    plt.bar(left, height, tick_label=tick_label, color=['#4682B4', '#B0C4DE'])
    plt.ylabel('Количество посещений')
    plt.xlabel('Месяц')
    plt.title('Ваша статистика посещаемости по месяцам')
    plt.savefig("static/img/plot.png")
