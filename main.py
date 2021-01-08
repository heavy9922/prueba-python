from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2 
app = Flask(__name__)

#Global constant
PSQL_HOST = "localhost"
PSQL_PORT = "5432"
PSQL_USER = "postgres"
PSQL_PASSWORD = "Skills2020"
PSQL_DB = "catalogo"

#connection ===================================================================
connection_address = """
host=%s port=%s user=%s password=%s dbname=%s
""" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASSWORD, PSQL_DB)
conexion = psycopg2.connect(connection_address)
cursor = conexion.cursor()
#==============================================================================
app.secret_key= 'mySecretKey'
#pagina de inicio
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home')
def home():
    return redirect(url_for('index'))


#==================================================================================    
#tabla de productos
@app.route('/productos')
def productos():
    cursor.execute('SELECT  productos.id ,nom_pro, marcas.marca, talla.talla , cantidad, fecha, observaciones FROM productos, marcas, talla WHERE marcas.id = marca_id AND talla.id = talla_id;')
    data = cursor.fetchall()
    return render_template('productos.html', products = data)
#formulario de agregar producto
@app.route('/add_p')
def add_p():
    cursor.execute('select * from marcas;')
    data = cursor.fetchall()
    cursor.execute('select * from talla;')
    data2 = cursor.fetchall()
    return render_template('form_product.html', marcas = data, tallas = data2)
#enviar datos a la DB
@app.route('/addP', methods=['POST'])
def addP():
    if request.method == 'POST':
        ndp = request.form['ndp']
        marca = request.form['marca']
        talla = request.form['talla']
        cantidad = request.form['cantidad']
        fecha = request.form['fecha']
        observaciones = request.form['observaciones']
        cursor.execute('INSERT INTO productos (nom_pro, marca_id, talla_id, cantidad, fecha, observaciones) VALUES (%s,%s,%s,%s,%s,%s)', (ndp, marca, talla, cantidad, fecha, observaciones))
        conexion.commit()
        flash('Se ha agregado con exito')
        return redirect(url_for('productos'))
#formulario de actualizar el producto
@app.route('/edit_p/<string:id>')
def get_p(id):
    cursor.execute('select * from marcas;')
    data = cursor.fetchall()
    cursor.execute('select * from talla;')
    data2 = cursor.fetchall()
    cursor.execute('SELECT  productos.id ,nom_pro, marca_id, marcas.marca, talla_id , talla.talla , cantidad, fecha, observaciones FROM productos, marcas, talla WHERE marcas.id = marca_id AND talla.id = talla_id AND productos.id = {0}'.format(id))
    data3 = cursor.fetchall()
    return render_template('form_up.html', marcas = data, tallas = data2 , product = data3[0] )
#enviar datos actualizados
@app.route('/updateP/<id>', methods=['POST'])
def updateP(id):
    if request.method == 'POST':
        ndp = request.form['ndp']
        marca = request.form['marca']
        talla = request.form['talla']
        cantidad = request.form['cantidad']
        fecha = request.form['fecha']
        observaciones = request.form['observaciones']
        cursor.execute('UPDATE productos SET nom_pro=%s , marca_id=%s , talla_id=%s , cantidad=%s , fecha=%s, observaciones = %s  WHERE id = %s',(ndp, marca, talla, cantidad, fecha, observaciones, id))
        conexion.commit()
        flash('Se ha  actualizado con exito')
        return redirect(url_for('productos'))
#eliminar datos de la tabla marcas
@app.route('/deleteP/<string:id>')
def deleteP(id):
     cursor.execute('delete from productos where id = {0}'.format(id))
     conexion.commit()
     flash('Eliminado con exito')
     return redirect(url_for('productos'))

#========================================================================================
#tabla de marcas
@app.route('/marcas')
def marcas():
    cursor.execute('select * from marcas;')
    data = cursor.fetchall()
    return render_template('marcas.html', marcas = data)
#formulario de agregar marcas 
@app.route('/add_m')
def add_m():
    return render_template('form_marca.html')
#enviar datos a la tabla de marca
@app.route('/addM', methods=['POST'] )
def addM():
    if request.method == 'POST':
        marca = request.form['marca']
        cursor.execute('INSERT INTO marcas (marca) VALUES (%s);', (marca,))
        conexion.commit()
        flash('Se ha agregado con exito')
        return redirect(url_for('marcas'))
#formulario de actualizar la marca 
@app.route('/edit_m/<string:id>')
def get_m(id):
    cursor.execute('select * from marcas where id = {0}'.format(id))
    data = cursor.fetchall()
    return render_template('form_um.html', marcas = data[0] )
#enviar datos actualizados
@app.route('/updateM/<id>', methods=['POST'])
def updateM(id):
    if request.method == 'POST':
        marca = request.form['marca']
        cursor.execute('update marcas set marca = %s where id = %s ', (marca, id))
        conexion.commit()
        flash('Se ha actualizado con exito')
        return redirect(url_for('marcas'))
#eliminar datos de la tabla marcas
@app.route('/deleteM/<string:id>')
def deleteM(id):
     cursor.execute('delete from marcas where id = {0}'.format(id))
     conexion.commit()
     flash('Eliminado con exito!')
     return redirect(url_for('marcas'))