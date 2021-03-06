import psycopg2
import matplotlib.pyplot as plt
from tkinter import *

root = Tk()
root.title("Statistics")
root.geometry('440x350')
root.resizable(width=0, height=0)
root["bg"] = "#AFFBC7"
root.iconbitmap('dino.ico')


def getInfoEelement(statistics, table_name, country, year): #Функция возращает статистический показатель страны за определенный год
    hostname = 'localhost'
    database = 'University Project'
    username = 'postgres'
    pwd = '11121977'
    port_id = '5433'

    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    cur = conn.cursor()
    getInfo_script = f"SELECT {statistics} FROM {table_name} WHERE country = '{country}' AND year = {year};"
    cur.execute(getInfo_script)
    return (cur.fetchone()[0])


def getInfoButton():
    result_info = ""
    result_info = getInfoEelement(default_statistics.get(), default_statistics.get(), default_country.get(),
                                  default_year.get())
    result_label = Label(root, text=f"{result_info}", width=10)
    result_label.place(x=10, y=200)



def getCountriesInTable(table_name):  #функция возвращает список всех стран, информация о которых есть в таблице с названием "table_name"
    hostname = 'localhost'
    database = 'University Project'
    username = 'postgres'
    pwd = '11121977'
    port_id = '5433'

    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    cur = conn.cursor()
    getInfo_script = f"SELECT DISTINCT country FROM {table_name}"
    cur.execute(getInfo_script)
    return ["".join(country).strip("(").strip(")").strip(",").strip("'") for country in cur.fetchall()]


statistics_label = Label(root, text="Statistics", font="Broadway 12", width=11, fg="#3C8B57")
statistics_label.grid(column=0, row=0, ipadx=1, ipady=2, padx=12, pady=10)

country_label = Label(root, text="Country", font="Broadway 12", width=10, fg="#3C8B57")
country_label.grid(column=1, row=0, ipadx=2, ipady=2, padx=11, pady=10)

default_statistics = StringVar()

options = ["life_expectancy", "people_below_poverty_line", "gdp_per_capita"]

statistics_options = OptionMenu(root, default_statistics, *options)

statistics_options.grid(column=0, row=1)
statistics_options.config(bg="#EDFFF3")
statistics_options.config(width=14)
statistics_options.config(height=1)

year_label = Label(root, text="Year", font="Broadway 12", width=10, fg="#3C8B57")
year_label.grid(column=2, row=0, ipadx=2, ipady=2, padx=11, pady=10)

default_year = StringVar()
entry_year = Entry(root, textvariable=default_year)
entry_year.grid(column=2, row=1, ipadx=0, ipady=0, padx=0, pady=0)
entry_year.config(bg="#EDFFF3")
entry_year.config(width=20)

countries = getCountriesInTable("life_expectancy")

default_country = StringVar()
country_options = OptionMenu(root, default_country, *countries)
country_options.grid(column=1, row=1)
country_options.config(bg="#EDFFF3")
country_options.config(width=13)
country_options.config(height=1)


def getRealNumberStatistics(statistics, country): #функция возвращает статистические данные конкретной страны за весь период, содержащийся в таблице
    hostname = 'localhost'
    database = 'University Project'
    username = 'postgres'
    pwd = '11121977'
    port_id = '5433'

    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    cur = conn.cursor()
    getInfo_script = f"SELECT {statistics} FROM {statistics} WHERE country = '{country}';"
    cur.execute(getInfo_script)
    return list(map(float, [stats.strip("(").strip(")").strip(",") for stats in list(map(str, cur.fetchall()))]))


def getYears(statistics, country): #функция возвращает спиосок всех годов ,содержащихся в таблице для конкретной страны
    hostname = 'localhost'
    database = 'University Project'
    username = 'postgres'
    pwd = '11121977'
    port_id = '5433'

    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    cur = conn.cursor()
    getInfo_script = f"SELECT year FROM {statistics} WHERE country = '{country}';"
    cur.execute(getInfo_script)
    return list(map(int, [years.strip("(").strip(")").strip(",") for years in list(map(str, cur.fetchall()))]))


def plotData(years, statistics, country, statistics_name): #функция визуализирует ход изменения статистических показателей конкретной страны за весь период
    plt.bar(years, statistics)
    plt.xlim(1950, 2025)
    plt.xlabel("Year")
    plt.ylabel("Statistics")
    plt.title(f"{country} {statistics_name}")
    plt.show()


def plotDataButton():
    years = getYears(default_statistics.get(), default_country.get())
    statistics = getRealNumberStatistics(default_statistics.get(), default_country.get())
    plotData(years, statistics, default_country.get(), default_statistics.get())


button_v = Button(root, text="Visualize Data", font="Broadway 16", bg="white", fg="PaleGreen4",
                  activebackground="snow2", command=plotDataButton)
button_v.place(x=10, y=100)

button_y = Button(root, text="Statistics Per Year", font="Broadway 16", bg="white", fg="PaleGreen4",
                  activebackground="snow2", command=getInfoButton)
button_y.place(x=10, y=150)

def on_closing():
    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        root.destroy()
        root.protocol("WM_DELETE_WINDOW", on_closing)
button_quit = Button(text = "Quit", command = on_closing,font = "Broadway 16", bg = "white", fg = "PaleGreen4", activebackground = "snow2")
button_quit.place(x=183, y =200)

def getBest25(): #функция находит 25 стран с лучшим выбранным статистическим показателем и визулизирует их на графике
    statistics = default_statistics.get()
    year = default_year.get()
    hostname = 'localhost'
    database = 'University Project'
    username = 'postgres'
    pwd = '11121977'
    port_id = '5433'

    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    cur = conn.cursor()
    getInfo_script = f"SELECT {statistics},country FROM {statistics} WHERE year = {year};"
    cur.execute(getInfo_script)
    data = list(map(eval, [line.strip('(').strip(')') for line in list(map(str, cur.fetchall()))]))
    data.sort(key=lambda y: y[0])
    data = data[-25:]
    x_points = [x[0] for x in data]
    y_points = [y for y in range(0, len(x_points) * 10000, 10000)]
    names = [x[1] for x in data]
    plt.scatter(x_points, y_points)
    plt.yticks(y_points, names)
    plt.xlabel(f"{statistics} in {year}")
    plt.title(f"25 countries with the best statistics in {statistics} in {year}")
    plt.show()


def getWorst25():  #функция находит 25 стран с худшим выбранным статистическим показателем и визулизирует их на графике
    statistics = default_statistics.get()
    year = default_year.get()
    hostname = 'localhost'
    database = 'University Project'
    username = 'postgres'
    pwd = '11121977'
    port_id = '5433'

    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    cur = conn.cursor()
    getInfo_script = f"SELECT {statistics},country FROM {statistics} WHERE year = {year};"
    cur.execute(getInfo_script)
    data = list(map(eval, [line.strip('(').strip(')') for line in list(map(str, cur.fetchall()))]))
    data.sort(key=lambda y: y[0])
    data = data[:25]
    x_points = [x[0] for x in data]
    y_points = [y for y in range(0, len(x_points) * 10000, 10000)]
    names = [x[1] for x in data]
    plt.scatter(x_points, y_points)
    plt.yticks(y_points, names)
    plt.xlabel(f"{statistics} in {year}")
    plt.title(f"25 countries with the worst statistics in {statistics} in year {year}")
    plt.show()

button_b = Button(root, text="25 Countries With The Best Statistics",font = "Broadway 14", bg = "white", fg = "PaleGreen4", activebackground = "snow2", command=getBest25)
button_b.place(x=10, y =200)

button_w = Button(root, text="25 Countries With The Worst Statistics",font = "Broadway 14", bg = "white", fg = "PaleGreen4", activebackground = "snow2", command=getWorst25)
button_w.place(x=10, y =250)

root.mainloop()
