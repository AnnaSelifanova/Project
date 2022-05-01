import psycopg2
from tkinter import *

root = Tk()
root.title("Statistics")
root.geometry('250x250')

table_name_label = Label(root, text="Table name", width=10)
table_name_label.grid(column=1, row=0)

statistics_label = Label(root, text="Statistics", width=10)
statistics_label.grid(column=2, row=0)

country_label = Label(root, text="Country", width=10)
country_label.grid(column=3, row=0)

year_label = Label(root, text="Year", width=10)
year_label.grid(column=4, row=0)

default_table_name = StringVar()
table_name_options = OptionMenu(root, default_table_name, "life___expectancy")
table_name_options.grid(column=1, row=1)

default_statistics = StringVar()
statistics_options = OptionMenu(root, default_statistics, "life_expectancy")
statistics_options.grid(column=2, row=1)

default_country = StringVar()
country_options = OptionMenu(root, default_country, "Afghanistan", "Russia", "China")
country_options.grid(column=3, row=1)

default_year = IntVar()
year_options = OptionMenu(root, default_year, 1960)
year_options.grid(column=4, row=1)


def getInfo(statistics, table_name, country, year):
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
    result_info = getInfo(default_statistics.get(), default_table_name.get(), default_country.get(), default_year.get())
    result_label = Label(root, text=f"{result_info}", width=10)
    result_label.grid(column=1, row=6)


button = Button(root, text="See the results", command=getInfoButton)
button.grid(column=1, row=5)

root.mainloop()
 