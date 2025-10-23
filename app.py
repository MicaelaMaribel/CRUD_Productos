from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Crear la conexion a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="*****",
    database="bd_productos"
)

# Ruta principal: listar productos
@app.route('/')
def listar():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()

    return render_template('listar.html', productos=productos)

# Ruta para mostrar el formulario de agregar producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']

        cursor = conexion.cursor()
        sql = "INSERT INTO productos (nombre, precio) VALUES (%s, %s)"
        cursor.execute(sql, (nombre, precio))
        conexion.commit()
        cursor.close()

        return redirect(url_for('listar'))

    return render_template('formulario.html')


# Ruta para editar un producto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    cursor.close()

    if not producto:
        return "Producto no encontrado"

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']

        cursor = conexion.cursor()
        cursor.execute("UPDATE productos SET nombre=%s, precio=%s WHERE id=%s", (nombre, precio, id))
        conexion.commit()
        cursor.close()

        return redirect(url_for('listar'))

    return render_template('editar.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/eliminar/<int:id>')
def eliminar(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conexion.commit()
    cursor.close()
    return redirect(url_for('listar'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

