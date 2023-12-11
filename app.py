from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

conn = cursor = None

# Fungsi koneksi database
def openDb():
   global conn, cursor
   # Update the following connection parameters with your Azure SQL Database information
   server = 'dbserverkelompok2.database.windows.net'
   database = 'DB-Kelompok2'
   username = 'daffa'
   password = 'Nusantara45_'
   conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'
   conn = pyodbc.connect(conn_str)
   cursor = conn.cursor()

# Fungsi untuk menutup koneksi
def closeDb():
   global conn, cursor
   cursor.close()
   conn.close()

# Fungsi view index() untuk menampilkan data dari database
@app.route('/')
def index():
   openDb()
   container = []
   sql = "SELECT * FROM barang"
   cursor.execute(sql)
   results = cursor.fetchall()
   for data in results:
      container.append(data)
   closeDb()
   return render_template('index.html', container=container)

# Fungsi view tambah() untuk membuat form tambah
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
   if request.method == 'POST':
      nama = request.form['nama']
      harga = request.form['harga']
      stok = request.form['stok']
      openDb()
      sql = "INSERT INTO barang (nama_barang, harga, stok) VALUES (?, ?, ?)"
      val = (nama, harga, stok)
      cursor.execute(sql, val)
      conn.commit()
      closeDb()
      return redirect(url_for('index'))
   else:
      return render_template('tambah.html')

# Fungsi view edit() untuk form edit
@app.route('/edit/<id_barang>', methods=['GET', 'POST'])
def edit(id_barang):
   openDb()
   cursor.execute('SELECT * FROM barang WHERE id_barang=?', (id_barang,))
   data = cursor.fetchone()
   if request.method == 'POST':
      id_barang = request.form['id_barang']
      nama = request.form['nama']
      harga = request.form['harga']
      stok = request.form['stok']
      sql = "UPDATE barang SET nama_barang=?, harga=?, stok=? WHERE id_barang=?"
      val = (nama, harga, stok, id_barang)
      cursor.execute(sql, val)
      conn.commit()
      closeDb()
      return redirect(url_for('index'))
   else:
      closeDb()
      return render_template('edit.html', data=data)

# Fungsi untuk menghapus data
@app.route('/hapus/<id_barang>', methods=['GET', 'POST'])
def hapus(id_barang):
   openDb()
   cursor.execute('DELETE FROM barang WHERE id_barang=?', (id_barang,))
   conn.commit()
   closeDb()
   return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(debug=True)
