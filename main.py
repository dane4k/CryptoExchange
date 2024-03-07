import pandas as pd
from tkinter import *
from tkinter import ttk, font
import matplotlib.pyplot as plt
import requests

btc_prices = [('2023-01', '16531.83'), ('2023-02', '23127.15'), ('2023-03', '23144.37'), ('2023-04', '28475.41'),
              ('2023-05', '29240.49'), ('2023-06', '27221.54'), ('2023-07', '30466.73'), ('2023-08', '29230.61'),
              ('2023-09', '25931.51'), ('2023-10', '26961'), ('2023-11', '34656.38'), ('2023-12', '37732.27')]

eth_prices = [('2023-01', '1195.25'), ('2023-02', '1585.32'), ('2023-03', '1605.59'), ('2023-04', '1822.11'),
              ('2023-05', '1870.67'), ('2023-06', '1874.08'), ('2023-07', '1933.7'), ('2023-08', '1856.09'),
              ('2023-09', '1645.58'), ('2023-10', '1670.84'), ('2023-11', '1815.14'), ('2023-12', '2053.08')]

xrp_prices = [('2023-01', '0.34015834304606346'), ('2023-02', '0.4065546810013903'), ('2023-03', '0.37717355677551107'),
              ('2023-04', '0.5384916303359293'), ('2023-05', '0.4725237240113901'), ('2023-06', '0.5174223209025567'),
              ('2023-07', '0.4742306595302564'), ('2023-08', '0.6976'), ('2023-09', '0.5109'), ('2023-10', '0.5138'),
              ('2023-11', '0.5998'), ('2023-12', '0.666')]


def create_dataframe(prices, crypto):
    return pd.DataFrame({'Дата': [col[0] for col in prices], 'Цена': [float(col[1]) for col in prices]},
                        index=[crypto] * len(prices))


btc_df = create_dataframe(btc_prices, 'BTC')
eth_df = create_dataframe(eth_prices, 'ETH')
xrp_df = create_dataframe(xrp_prices, 'XRP')

coins_prices = {'Дата': [col[0] for col in btc_prices], 'BTC': [float(col[1]) for col in btc_prices],
                'ETH': [float(col[1]) for col in eth_prices], 'XRP': [round(float(col[1]), 4) for col in xrp_prices]}
df = pd.DataFrame(coins_prices)


def show_graph(df, crypto):
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.plot(df['Дата'], df['Цена'])
    ax.set_xlabel('Дата')
    ax.set_ylabel('Цена')
    ax.set_title(f'График цены для криптовалюты {crypto}')
    plt.show()


url = 'https://api.binance.com/api/v3/ticker/price'


def get_current_price(symbol):
    response = requests.get(url, params={'symbol': f'{symbol}USDT'}).json()
    return round(float(response['price']), 2)


btc = get_current_price('BTC')
eth = get_current_price('ETH')
xrp = get_current_price('XRP')

root = Tk()

root.title('Криптовалютная биржа')

root.geometry('800x900')

style = ttk.Style()
style.theme_use('default')
style.configure('Blue.Treeview',
                background='#99f',  # красный цвет фона
                foreground='black',  # белый цвет текста
                fieldbackground='#99f')  # красный цвет фона поля

tree = ttk.Treeview(root, style='Blue.Treeview')
tree['columns'] = list(df.columns)  # установка столбцов
tree['show'] = 'headings'  # отображение только заголовков столбцов

# заголовки и выравнивание по центру
for column in df.columns:
    tree.heading(column, text=column)
    tree.column(column, anchor='center')

# добавление данных в виджет Treeview
df.apply(lambda row: tree.insert('', 'end', values=row.tolist()), axis=1)

tree.pack()


def text_color(btc_price, eth_price, xrp_price):
    btc_old = float(btc_prices[-1][1])
    eth_old = float(eth_prices[-1][1])
    xrp_old = float(xrp_prices[-1][1])

    color_mapping = {
        'green': '#6f6',
        'red': 'red'
    }

    btc_color = color_mapping['green'] if btc_price > btc_old else color_mapping['red']
    btc_change = round(btc_price - btc_old, 2)
    btc_arrow = '↑' if btc_change > 0 else '↓'
    eth_color = color_mapping['green'] if eth_price > eth_old else color_mapping['red']
    eth_change = round(eth_price - eth_old, 2)
    eth_arrow = '↑' if eth_change > 0 else '↓'
    xrp_color = color_mapping['green'] if xrp_price > xrp_old else color_mapping['red']
    xrp_change = round(xrp_price - xrp_old, 2)
    xrp_arrow = '↑' if xrp_change > 0 else '↓'

    return (btc_color, eth_color, xrp_color), (btc_change, eth_change, xrp_change), (btc_arrow, eth_arrow, xrp_arrow)


result = text_color(btc, eth, xrp)

btcnow = f'Цена Bitcoin на данный момент - {btc} USD ({result[1][0]} {result[2][0]} с начала месяца)'
ethnow = f'Цена Ethereum на данный момент - {eth} USD ({result[1][1]} {result[2][1]} с начала месяца)'
xrpnow = f'Цена Ripple на данный момент - {xrp} USD ({result[1][2]} {result[2][2]} с начала месяца)'

font_for_prices = font.Font(size=10)

labelbtc = Label(root, text=btcnow, bg=text_color(btc, eth, xrp)[0][0], font=font_for_prices)
labeleth = Label(root, text=ethnow, bg=text_color(btc, eth, xrp)[0][1], font=font_for_prices)
labelxrp = Label(root, text=xrpnow, bg=text_color(btc, eth, xrp)[0][2], font=font_for_prices)

labelbtc.pack(anchor='center', pady=(13, 2))
labeleth.pack(anchor='center', pady=(0, 2))
labelxrp.pack(anchor='center', pady=(0, 2))


def show_btc_graph():
    show_graph(btc_df, 'Bitcoin')


def show_eth_graph():
    show_graph(eth_df, 'Ethereum')


def show_xrp_graph():
    show_graph(xrp_df, 'Ripple')


show_graph_btc_button = Button(root, text='Показать график Bitcoin', command=show_btc_graph, font=font_for_prices)
show_graph_btc_button.pack(pady=(30, 0))

show_graph_btc_button = Button(root, text='Показать график Ethereum', command=show_eth_graph, font=font_for_prices)
show_graph_btc_button.pack(pady=(10, 0))

show_graph_btc_button = Button(root, text='Показать график Ripple', command=show_xrp_graph, font=font_for_prices)
show_graph_btc_button.pack(pady=(10, 0))

custom_font = font.Font(size=17)

calculate_label = Label(root, text='Расчёт потенциальных потерь/прибыли', font=custom_font)

calculate_label.pack(anchor='center', pady=(40, 2))


def on_cryptocurrency_select(value):
    selected_cryptocurrency.set(value)


label_cryptocurrency = Label(root, text='Выберите криптовалюту:', font=font.Font(size=13), pady=10)
label_cryptocurrency.pack()

selected_cryptocurrency = StringVar()


# Создаем функции-обработчики для каждой криптовалюты
def on_bitcoin_select():
    on_cryptocurrency_select('Bitcoin')


def on_ethereum_select():
    on_cryptocurrency_select('Ethereum')


def on_ripple_select():
    on_cryptocurrency_select('Ripple')


# Создаем кнопки с использованием Radiobutton
bitcoin_button = Radiobutton(root, text='Bitcoin', variable=selected_cryptocurrency, value='Bitcoin',
                             command=on_bitcoin_select, font=font_for_prices)
bitcoin_button.pack()

ethereum_button = Radiobutton(root, text='Ethereum', variable=selected_cryptocurrency, value='Ethereum',
                              command=on_ethereum_select, font=font_for_prices)
ethereum_button.pack()

ripple_button = Radiobutton(root, text='Ripple', variable=selected_cryptocurrency, value='Ripple',
                            command=on_ripple_select, font=font_for_prices)
ripple_button.pack()

label_amount = Label(root, text='Укажите количество:', font=font_for_prices, pady=5)
label_amount.pack()

amount_entry = Entry(root)
amount_entry.pack()

label_date = Label(root, text='Укажите дату покупки:', font=font_for_prices, pady=5)
label_date.pack()

date_entry = Entry(root)
date_entry.pack()


def calculate_losses():
    cryptocurrency = selected_cryptocurrency.get()

    if cryptocurrency == 'Bitcoin':
        selected_df = btc_df
        price_now = btc
    elif cryptocurrency == 'Ethereum':
        selected_df = eth_df
        price_now = eth
    elif cryptocurrency == 'Ripple':
        selected_df = xrp_df
        price_now = xrp

    amount = float(amount_entry.get())
    date = date_entry.get()
    date_price = selected_df.loc[selected_df['Дата'] == date, 'Цена'].values

    if len(date_price) > 0:
        date_price = date_price[0]
        outcome = amount * (price_now - date_price)
        if outcome > 0:
            plus_or_minus = 'Вы бы получили выгоду в'
        else:
            plus_or_minus = 'Вы бы потеряли'
        result_label.config(text=f'{plus_or_minus} ${round(abs(outcome), 2)}')
    else:
        result_label.config(text='Дата не найдена в данных.')


result_label = Label(root, text='', pady=10, font=font_for_prices)
result_label.pack()

submit_button = Button(root, text='Рассчитать', command=calculate_losses, font=font_for_prices)
submit_button.pack()

root.mainloop()
