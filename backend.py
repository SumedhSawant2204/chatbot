from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Database setup
def init_db():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL,
                    stock INTEGER
                )''')

    # Populate database with mock data
    c.executemany('''INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)''',
                  [("Laptop", "High performance laptop", 1000.00, 10),
                   ("Smartphone", "Latest model smartphone", 800.00, 15),
                   ("Headphones", "Noise-cancelling headphones", 200.00, 20),
                   ("Monitor", "4K Ultra HD monitor", 300.00, 5),
                   ("Keyboard", "Mechanical keyboard", 100.00, 25)])

    conn.commit()
    conn.close()

@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('query', '')
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM products WHERE name LIKE ? OR description LIKE ?''', (f'%{query}%', f'%{query}%'))
    products = c.fetchall()
    conn.close()

    result = [
        {
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],
            'stock': product[4]
        } for product in products
    ]

    return jsonify(result)

@app.route('/chat', methods=['POST'])
def chatbot_response():
    user_message = request.json.get('message', '').lower()

    # Debugging output for checking user input
    print(f"User message: {user_message}")

    # Create a dictionary mapping product names to URLs
    product_urls = {
        "laptop": "https://www.amazon.com/s?k=laptop",
        "smartphone": "https://www.amazon.com/s?k=smartphone",
        "headphones": "https://www.amazon.com/s?k=headphones",
        "monitor": "https://www.amazon.com/s?k=monitor",
        "keyboard": "https://www.amazon.com/s?k=keyboard"
    }

    # Default response if no keyword is found
    response = "I am here to help with your queries. Try asking for product recommendations!"

    # If the message contains a recognized product keyword
    for product in product_urls:
        if product in user_message:
            # Retrieve product details from the database
            conn = sqlite3.connect('ecommerce.db')
            c = conn.cursor()
            c.execute('''SELECT name, description, price FROM products WHERE name LIKE ? LIMIT 3''', (f'%{product}%',))
            products = c.fetchall()
            conn.close()

            # Format response with product details and shopping URLs
            if products:
                response = f"Here are some {product}s you can purchase online:\n"
                for product_item in products:
                    name, description, price = product_item
                    url = product_urls.get(product, "No URL available")
                    response += f"\n- {name}: {description}\nPrice: ${price}\nBuy it here: {url}\n"
            else:
                response = f"Sorry, I couldn't find any {product}s in our database. But you can try looking online: {product_urls[product]}"
            break

    return jsonify({'response': response})



if __name__ == '__main__':
    init_db()
    app.run(debug=True)
