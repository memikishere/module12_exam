# ВНИМАНИЕ!!! ДЛЯ ПОЛНОЦЕННОЙ РАБОТЫ ПРОГРАММЫ НУЖНО УСТАНОВИТЬ БИБЛИОТЕКУ matplotlib.
# ДЛЯ ЭТОГО ВОСПОЛЬЗУЙТЕСЬ КОМАНДОЙ "pip install matplotlib" В КОМАНДНОЙ СТРОКЕ.

data_path = 'data.txt' # Путь к файлу с данными о продажах.

# Получение данных продаж из файла в формате списков состоящих из словарей, где 1 продажа - 1 словарь.
# В каждом таком словаре информация о наименовании продукта, кол-ве, стоимость за 1 шт, дата продажи.
def read_sales_data(file_path):
    # Переменные file(входной файл) и result(отдаваемый список)
    file = open(file_path, 'r', encoding='UTF-8')
    result = []
    
    # Алгоритм чтения строк из файла, преобразования данных к нормальному виду и заполнения списка result
    for i in file.readlines():
        j = i.split(', ')
        result.append({
            'product_name': j[0],
            'quantity': int(j[1]),
            'price': int(j[2]),
            'date': j[3].replace('\n','')        
        })

    file.close()
    return result


# Функция для подсчета всей выручки по каждому виду товаров.
def total_sales_per_product(sales_data):
    result = {}

    for data in sales_data: # Перебор всех продаж.
        if data['product_name'] not in result: # Если очередного товара еще нет в словаре result, он туда добавляется со значением (кол-во * стоимость за штуку).
            result[f'{data['product_name']}'] = data['price'] * data['quantity']
        else: # Если очередной товар уже есть в словаре result, к его значению добавляется (кол-во * стоимость за штуку) очередного товара.
            result[f'{data['product_name']}'] += data['price'] * data['quantity']
    
    return result


# Функция для подсчета всей выручки по каждому дню.
def sales_over_time(sales_data):
    result = {}

    for data in sales_data: # Перебор всех продаж.
        if data['date'] not in result: # Если очередного дня еще нет в словаре result, он туда добавляется со значением (кол-во * стоимость за штуку).
            result[f'{data['date']}'] = data['price'] * data['quantity']
        else: # Если очередной день уже есть в словаре result, к его значению добавляется (кол-во * стоимость за штуку) очередного дня.
            result[f'{data['date']}'] += data['price'] * data['quantity']
    return result


# Функция для поиска наибольшего значения в переданном словаре (может использоваться как для наименований, так и для дат)
def find_key_of_max_value(data):
    max_value = 0
    for i in data:
        if data[i] > max_value:
            max_value = data[i]
            key_of_max_value = i
    return (key_of_max_value, max_value)


sales_data = read_sales_data(data_path) # Преобразование данных к формату списка со словарями.


tspp = total_sales_per_product(sales_data) # Записываем в переменную данные о выручке по каждому продукту.
sot = sales_over_time(sales_data) # Записываем в переменную данные о выручке по каждому дню.


max_sales_over_titles = find_key_of_max_value(tspp) # Записываем в переменную данные о максимальной выручке по каждому продукту.
max_sales_over_time = find_key_of_max_value(sot) # Записываем в переменную данные о максимальной выручке по каждому дню.


# Вывод информации о максимальных выручках.
clr = {
    'red': '\033[31m\033[1m',
    'white': '\033[37m\033[0m'
} # Просто баловался с цветами для вывода :) Подсвечивать данные красным кажется классной идеей!
print(f'Наибольшую вырочку принес продукт {clr['red']}"{max_sales_over_titles[0]}"{clr['white']}. Выручка по этому продукту составляет {clr['red']}{max_sales_over_titles[1]}{clr['white']}')
print(f'Наибольшая выручка была {clr['red']}{max_sales_over_time[0]}{clr['white']}. Выручка в этот день составила {clr['red']}{max_sales_over_time[1]}{clr['white']}')


# Здесь рисуем графики
import matplotlib.pyplot as plt # Импортируем pyplot.
fig, axs = plt.subplots(nrows= 2 , ncols= 1) # Создаем 2 графика.

# Алгоритм сортировки данных в порядке возростания по датам, для того что бы на графике даты не стояли в разброс.
some_list = []
for i in sorted(sot):
    some_list.append((i, sot[i]))
plot_list_date = list(i[0] for i in some_list)
plot_list_values = list(i[1] for i in some_list)
axs[0].plot(plot_list_date, plot_list_values)


# Такой же алгоритм как предыдущий, только для графика по наименованиям продуктов.
some_list = []
for i in sorted(tspp):
    some_list.append((i, tspp[i]))
plot_list_titles = list(i[0] for i in some_list)
plot_list_values = list(i[1] for i in some_list)
axs[1].plot(plot_list_titles, plot_list_values)


plt.show()