from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
CORS(app)

@app.route('/login', methods=['POST'])
def login_admin():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, role FROM admin WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    if user:
        user_id = user[0]
        role = user[1]
        if role == 'admin':
            return jsonify({'message': 'Login successful', 'user_id': user_id, 'role': role})
        else:
            return jsonify({'message': 'Access denied. Only admins can log in here.'}), 403
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
    
@app.route('/loginuser', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, role FROM admin WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    if user:
        user_id = user[0]
        role = user[1]
        if role == 'user':
            return jsonify({'message': 'Login successful', 'user_id': user_id, 'role': role})
        else:
            return jsonify({'message': 'Access denied. Only admins can log in here.'}), 403
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin WHERE username = %s", (username,))
    existing_user = cur.fetchone()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409
    cur.execute("INSERT INTO admin (username, password, role) VALUES (%s, %s, 'admin')", (username, password))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/registeruser', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin WHERE username = %s", (username,))
    existing_user = cur.fetchone()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409
    cur.execute("INSERT INTO admin (username, password, role) VALUES (%s, %s, 'user')", (username, password))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password FROM admin")
    rows = cur.fetchall()
    cur.close()
    users = []
    for row in rows:
        users.append({'id': row[0], 'username': row[1], 'password': row[2]})
    return jsonify(users)

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password FROM admin WHERE id = %s", (id,))
    row = cur.fetchone()
    cur.close()
    if row:
        user = {'id': row[0], 'username': row[1], 'password': row[2]}
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (username, password))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User added successfully'}), 201

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    username = data.get('username')
    password = data.get('password')
    cur = mysql.connection.cursor()
    cur.execute("UPDATE admin SET username = %s, password = %s WHERE id = %s", (username, password, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User updated successfully'})

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM admin WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User deleted successfully'})

@app.route('/surat', methods=['GET'])
def get_surat():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nama_surat, no_surat, pihak_pertama, pihak_kedua, tanggal_masuk, tanggal_keluar, keterangan, file FROM surat")
    rows = cur.fetchall()
    cur.close()
    surat_list = []
    for row in rows:
        surat_list.append({
            'id': row[0],
            'nama_surat': row[1],
            'no_surat': row[2],
            'pihak_pertama': row[3],
            'pihak_kedua': row[4],
            'tanggal_masuk': row[5],
            'tanggal_keluar': row[6],
            'keterangan': row[7],
            'file': row[8]
        })
    return jsonify(surat_list)

@app.route('/surat', methods=['POST'])
def add_surat():
    data = request.json
    nama_surat = data.get('nama_surat')
    no_surat = data.get('no_surat')
    pihak_pertama = data.get('pihak_pertama')
    pihak_kedua = data.get('pihak_kedua')
    tanggal_masuk = data.get('tanggal_masuk')
    tanggal_keluar = data.get('tanggal_keluar')
    keterangan = data.get('keterangan')
    file = data.get('file')
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO surat (nama_surat, no_surat, pihak_pertama, pihak_kedua, tanggal_masuk, tanggal_keluar, keterangan, file) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (nama_surat, no_surat, pihak_pertama, pihak_kedua, tanggal_masuk, tanggal_keluar, keterangan, file))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Surat added successfully'}), 201

@app.route('/surat/<int:id>', methods=['PUT'])
def update_surat(id):
    data = request.json
    nama_surat = data.get('nama_surat')
    no_surat = data.get('no_surat')
    pihak_pertama = data.get('pihak_pertama')
    pihak_kedua = data.get('pihak_kedua')
    tanggal_masuk = data.get('tanggal_masuk')
    tanggal_keluar = data.get('tanggal_keluar')
    keterangan = data.get('keterangan')
    file = data.get('file')
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE surat 
        SET nama_surat = %s, no_surat = %s, pihak_pertama = %s, pihak_kedua = %s, tanggal_masuk = %s, tanggal_keluar = %s, keterangan = %s, file = %s
        WHERE id = %s
    """, (nama_surat, no_surat, pihak_pertama, pihak_kedua, tanggal_masuk, tanggal_keluar, keterangan, file, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Surat updated successfully'})

@app.route('/surat/<int:id>', methods=['DELETE'])
def delete_surat(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM surat WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Surat deleted successfully'})

@app.route('/user', methods=['GET'])
def user_page():
    return render_template('user.html')

@app.route('/admin', methods=['GET'])
def admin_page():
    return render_template('admin.html')

@app.route('/login_page', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/loginuser', methods=['GET'])
def login_user_page():
    return render_template('loginuser.html')

@app.route('/register', methods=['GET'])
def regis_page():
    return render_template('register.html')

@app.route('/registeruser', methods=['GET'])
def regis_user_page():
    return render_template('registeruser.html')

if __name__ == '__main__':
    app.run(debug=True)
