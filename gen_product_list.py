from collections import defaultdict
import json
import mysql.connector
import os

# Define the database connection URL
db_url = f"mysql+mysqlconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Parse the URL to extract connection parameters
from sqlalchemy.engine.url import make_url
url = make_url(db_url)

def gen_product_list():
    # Establish a connection to the database
    connection = mysql.connector.connect(
        user=url.username,
        password=url.password,
        host=url.host,
        port=url.port or 3306,
        database=url.database,

        charset='utf8mb4'
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Define the query you want to execute
    query = '''SELECT
        p.ProductID,
        p.ProductName,
        p.productPrice,
        p.ProductDescription,
        ps.SizeID,
        ps.SizeName,
        pq.Quantity
    FROM
        product p
    LEFT JOIN
        productsize ps ON p.ProductID = ps.ProductID
    LEFT JOIN
        productquantity pq ON ps.ProductID = pq.ProductID AND ps.SizeID = pq.SizeID
    ORDER BY
        p.ProductID, ps.SizeID;
    '''

    # Execute the query
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()

    # Organize results into a nested dictionary
    products = defaultdict(lambda: {
        "ProductID": None,
        "ProductName": None,
        "productPrice": None,
        "ProductDescription": None,
        "Sizes": []
    })

    for row in results:
        product_id = row[0]
        if not products[product_id]['ProductID']:
            products[product_id].update({
                "ProductID": row[0],
                "ProductName": row[1],
                "productPrice": row[2],
                "ProductDescription": str(row[3]),
            })

        products[product_id]['Sizes'].append({
            "SizeName": row[5],
            "Quantity": row[6]
        })

    # Convert the dictionary to a list of products
    product_list = list(products.values())

    # Convert the result to JSON
    json_result = json.dumps(product_list, indent=4, ensure_ascii=False)

    # Print the JSON result
    with open("product_list.json", "w") as w:
        w.write(json_result)

    # Close the cursor and connection
    cursor.close()
    connection.close()
