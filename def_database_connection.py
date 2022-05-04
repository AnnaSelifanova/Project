import psycopg2
import matplotlib.pyplot as plt
from tkinter import *

root = Tk()
root.title("Statistics")
root.geometry('250x250')


def getInfoEelement(statistics, table_name, country, year):
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
    result_info = getInfoEelement(default_statistics.get(), default_table_name.get(), default_country.get(), default_year.get())
    result_label = Label(root, text=f"{result_info}", width=10)
    result_label.grid(column=1, row=6)


def getCountriesInTable(table_name):
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



statistics_label = Label(root, text="Statistics", width=10)
statistics_label.grid(column=1, row=0)

country_label = Label(root, text="Country", width=10)
country_label.grid(column=2, row=0)

default_statistics = StringVar()
statistics_options = OptionMenu(root, default_statistics, "life_expectancy")
statistics_options.grid(column=1, row=1)

countries = getCountriesInTable("life_expectancy")

default_country = StringVar()
country_options = OptionMenu(root, default_country, *countries)
country_options.grid(column=2, row=1)


def getRealNumberStatistics(statistics, country):
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
    return list(map(float,[stats.strip("(").strip(")").strip(",") for stats in list(map(str,cur.fetchall()))]))

def getYears(statistics, country):
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


def plotData(years,statistics,country,statistics_name):
    plt.bar(years,statistics)
    plt.xlim(1950, 2025)
    plt.xlabel("Year")
    plt.ylabel("Statistics")
    plt.title(f"{country} {statistics_name}")
    plt.show()

def plotDataButton():
    years = getYears(default_statistics.get(),default_country.get())
    statistics = getRealNumberStatistics(default_statistics.get(),default_country.get())
    plotData(years,statistics,default_country.get(),default_statistics.get())

button = Button(root, text="Visualize Data", command=plotDataButton)
button.grid(column=1, row=8)

root.mainloop()

 
