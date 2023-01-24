from flask import Flask, render_template
import subprocess
import sqlite3

app = Flask(__name__)

@app.route('/main')
def main():
    """Esta funcion crea una coneccion con la base de datos, hace una consulta a la base y muestra todo el contenido de la 
tabla en la plantilla main.html"""
    conn = sqlite3.connect('basedate.db')
    c = conn.cursor()
    c.execute('SELECT * FROM product')
    products = c.fetchall()
    conn.close()
    return render_template('main.html', products=products)

@app.route("/")
def index():
    """Esta funcion mapea y devuelve el archivo index.html este es el manu para ejecutar el script y vizualizar
    el contenido de la tabla"""
    return render_template("index.html")

@app.route("/contacto")
def contacto():
    """Esta funcion mapea y dedvuelve el archivo contacto.html este tiene a disposicion la forma 
    de contactarse"""
    return render_template("contacto.html")

@app.route('/run_script', methods=['POST'])
def run_script():
    """Esta funcion se ejecuta cuando el boton del index es precionado, ejecuta el webscraping y añade 
    los datos a la base de datos"""
    subprocess.call(["python", "main.py"])

if __name__ == '__main__':
    app.run(debug=True)
