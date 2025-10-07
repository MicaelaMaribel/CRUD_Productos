from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista para guardar los productos temporalmente
productos = []
# Cada producto será un diccionario con id, nombre y precio

# Ruta principal: listar productos
@app.route('/')
def listar():
    return render_template('listar.html', productos=productos)

# Ruta para mostrar el formulario de agregar producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        # Capturamos los datos del formulario
        nombre = request.form['nombre']
        precio = request.form['precio']
        producto = {
            'id': len(productos)+1,  # ID automático
            'nombre': nombre,
            'precio': precio
        }
        productos.append(producto)  # Agregamos a la lista
        return redirect(url_for('listar'))  # Volvemos a la lista

    return render_template('formulario.html')  # GET muestra el formulario

# Ruta para editar un producto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    # Buscamos el producto por id
    producto = next((p for p in productos if p['id'] == id), None)
    if not producto:
        return "Producto no encontrado"

    if request.method == 'POST':
        # Actualizamos los datos
        producto['nombre'] = request.form['nombre']
        producto['precio'] = request.form['precio']
        return redirect(url_for('listar'))

    return render_template('editar.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/eliminar/<int:id>')
def eliminar(id):
    global productos
    productos = [p for p in productos if p['id'] != id]
    return redirect(url_for('listar'))

if __name__ == '__main__':
    app.run(debug=True)
