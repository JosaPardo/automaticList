import urllib.request
import requests
from bs4 import BeautifulSoup as bs
import re
import csv
import sqlite3

#Funcion  que obtiene el nombre de los productos de la pagina 
def nombres_productos():
    global soup
    productos = soup.body.findAll("h2")
    array_productos = []
    for producto in productos:
        producto = producto.text.replace('\n', '').lstrip().rstrip()
        array_productos.append(producto)
    return array_productos[1:]

#Funcion que obtiene el precio de los productos de la pagina 
def precios_productos():
    global soup
    precios = soup.body.findAll("span", attrs = {"data-label": "con iva"})
    array_precios = []
    for precio in precios:
        precio = precio.text.replace('\n', '').lstrip().rstrip()
        
        array_precios.append(precio)
    return array_precios

#Funcion para crear la base de datos y insertar los archivos del csv en la tabla
def insert_data():
    conn = sqlite3.connect("basedate.db")
    cursor = conn.cursor()
    #query = 'CREATE TABLE product (id INTEGER PRIMARY KEY, producto TEXT COLLATE NOCASE, precio REAL)'
    #cursor.execute(query)
    
    query = '''DROP TABLE IF EXISTS product'''
    cursor.execute(query)
    query = '''CREATE TABLE product (id INTEGER PRIMARY KEY, producto TEXT COLLATE NOCASE, precio REAL )'''
    cursor.execute(query)

    with open('datos.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            cursor.execute("INSERT INTO product (producto, precio) VALUES (?, ?)", line)
            print(line)
    conn.commit()

    f.close()
    conn.close()
#Funcion en la que se hace el webscraping y se inicia la los algoritmos para crear archivo csv y insertalos en SQL
def main():
    csvfile = open('datos.csv', 'a', newline='', encoding='utf-8')
    writer = csv.writer(csvfile)
    writer.writerow(['Nombre', 'Precio'])
    contador = 1 
    while contador < 3: 
        url = "https://maxiconsumo.com/sucursal_capital/almacen.html?p=" + str(contador) + "&product_list_limit=96"
        pagina = urllib.request.urlopen(url)
        global soup 
        soup = bs(pagina, "html.parser", from_encoding="utf-8")
        r = requests.get(url)
        if r.status_code == 200:
            products = nombres_productos()
            prices = precios_productos()
            for i in range(len(products)):
                if i < len(nombres_productos()) and i < len(precios_productos()):
                    writer.writerow([nombres_productos()[i], precios_productos()[i]])
                else:
                    print("No se puede escribir el elemento con índice", i, "en el archivo CSV, ya que no existe en alguna de las listas")
            print("paguina", contador , "guardada")             
        else:
            print("Error de conexión. No se pudo conectar a la página.")
        contador = int(contador) +1

main()
insert_data()