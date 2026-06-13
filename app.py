from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Database configuration (Update with your MySQL password if needed)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'EcommerceSystem'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

# DISPLAY & INSERT Records for Product
@app.route('/api/products', methods=['GET', 'POST'])
def manage_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Product")
        records = cursor.fetchall()
        conn.close()
        return jsonify(records)
        
    elif request.method == 'POST':
        data = request.json
        cursor.execute(
            "INSERT INTO Product (product_id, name, price, stock, category_id) VALUES (%s, %s, %s, %s, %s)",
            (data['product_id'], data['name'], data['price'], data['stock'], data['category_id'])
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Product record inserted successfully.'})

# UPDATE & DELETE Records for Product
@app.route('/api/products/<int:prod_id>', methods=['PUT', 'DELETE'])
def update_delete_product(prod_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE Product SET price = %s WHERE product_id = %s", (data['price'], prod_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Product pricing information updated.'})
        
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM Product WHERE product_id = %s", (prod_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Product record deleted from system backend.'})

# EXECUTE STORED PROCEDURE (GenerateInvoice)
@app.route('/api/invoice/<int:order_id>', methods=['GET'])
def get_invoice(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Safely calling the custom procedure matching your table keys
    cursor.callproc('GenerateInvoice', [order_id])
    
    result = []
    for cur in cursor.stored_results():
        result.extend(cur.fetchall())
        
    conn.close()
    return jsonify(result)

# TRIGGER DEMONSTRATION TRANS-BRIDGE (Order_Detail Insertions)
@app.route('/api/order-detail', methods=['POST'])
def create_order_detail():
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    try:
        # Inserts directly into your exact Order_Detail table name
        cursor.execute(
            "INSERT INTO Order_Detail (order_detail_id, order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s, %s)",
            (data['order_detail_id'], data['order_id'], data['product_id'], data['quantity'], data['price'])
        )
        conn.commit()
        msg = "Order detail successfully registered. Inventory automatically reduced via database trigger."
    except mysql.connector.Error as err:
        msg = f"Database Trigger Intercepted Operation: {err.msg}"
    finally:
        conn.close()
    return jsonify({'message': msg})

if __name__ == '__main__':
    app.run(debug=True)