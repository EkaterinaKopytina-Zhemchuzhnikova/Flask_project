import matplotlib.pyplot as plt


def plot_graph():
    left = [1, 2, 3, 4, 5]
    # heights of bars
    height = [10, 24, 36, 40, 5]
    # labels for bars
    tick_label = ['one', 'two', 'three', 'four', 'five']
    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['#4682B4', '#B0C4DE'])
    # naming the y-axis
    plt.ylabel('Количество посещений')
    # naming the x-axis
    plt.xlabel('Месяц')
    # plot title
    plt.title('Ваша статистика посещаемости по месяцам')
    plt.savefig("static/img/plot.png")

