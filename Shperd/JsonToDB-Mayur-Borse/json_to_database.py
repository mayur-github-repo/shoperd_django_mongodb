import json
import csv
import os

import mysql.connector

product_csv_filename = 'csv_files/products_csv.csv'
images_csv_filename = 'csv_files/images_csv.csv'
variants_csv_filename = 'csv_files/variants_csv.csv'
options_csv_filename = 'csv_files/options_csv.csv'


def addProductTitlesInCSV(jsonfilename):
    with open(jsonfilename) as f:
        data = json.load(f)
        title = []
        for key in data['products'][0].keys():
            if key != 'images' and key != 'variants' and key != 'options':
                title.append(key)
        with open(product_csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(title)

        imgTitle = []
        for key in data['products'][0]['images'][0]:
            imgTitle.append(key)
        with open(images_csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(imgTitle)

        varTitle = []
        for key in data['products'][0]['variants'][0]:
            varTitle.append(key)
        with open(variants_csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(varTitle)

        optionsTitle = []
        for key in data['products'][0]['options'][0]:
            optionsTitle.append(key)
        with open(options_csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(optionsTitle)


def export_csv(jsonfilename):
    with open(jsonfilename) as f:
        mainList = []
        data = json.load(f)
        excluded_keys = ['images', 'variants', 'options']
        for product in data['products']:
            val = []
            for key in product.keys():
                if key != 'images' and key != 'variants' and key != 'options':
                    val.append(product[key])
            mainList.append(val)

        for row in mainList[1:]:
            row[-1] = ', '.join(row[-1])

        with open(product_csv_filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in mainList[:-1]:
                csv_writer.writerow(row)

        # =============creating images csv file============================================================
        imgList = []
        for product in data['products']:
            for image in product['images']:
                row = []
                for val in image.values():
                    row.append(val)
                imgList.append(row)

        with open(images_csv_filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in imgList[:-1]:
                csv_writer.writerow(row)

        # =================== variants csv =======================
        variantList = []
        for product in data['products']:
            for variant in product['variants']:
                row = []
                for val in variant.values():
                    row.append(val)
                variantList.append(row)

        with open(variants_csv_filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in variantList[:-1]:
                csv_writer.writerow(row)

        # ===============options csv ===================================
        optionsList = []
        for product in data['products']:
            for option in product['options']:
                row = []
                for val in option.values():
                    row.append(val)
                optionsList.append(row)

        for row in optionsList[1:]:
            row[-1] = ', '.join(row[-1])

        with open(options_csv_filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in optionsList:
                csv_writer.writerow(row)


def create_table():
    global connection, cursor
    db_config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'port': 3306,
        'database': 'slick',
        # 'local_infile': 1
    }

    # ============================= product table========================================
    # id BIGINT PRIMARY KEY & id BIGINT AUTO_INCREMENT PRIMARY KEY

    create_table_query = """CREATE TABLE IF NOT EXISTS products (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    handle VARCHAR(255),
    body_html TEXT,
    published_at DATETIME,
    created_at DATETIME,
    updated_at DATETIME,
    vendor VARCHAR(255),
    product_type VARCHAR(255),
    tags TEXT  
    )"""
    product_insert_query = ("INSERT INTO products (id, title, handle, body_html, published_at, created_at, "
                            "updated_at, vendor, product_type, tags) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, "
                            "%s)")

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    drop_table_query = "DROP TABLE IF EXISTS products"
    cursor.execute(drop_table_query)
    cursor.execute(create_table_query)

    with open(product_csv_filename, 'r', encoding='utf-8-sig') as csv_file:

        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            cursor.execute(product_insert_query, row)

    # =================================================images db =======================
    create_images_table_query = """
    CREATE TABLE IF NOT EXISTS images (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        created_at DATETIME,
        position INT,
        updated_at DATETIME,
        product_id BIGINT,
        variant_ids TEXT,
        src VARCHAR(255),
        width INT,
        height INT
    )
    """
    drop_table_query = "DROP TABLE IF EXISTS images"
    cursor.execute(drop_table_query)
    cursor.execute(create_images_table_query)
    images_insert_query = (
        "INSERT INTO images (id, created_at, position, updated_at, product_id, variant_ids, src, width, height) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    with open(images_csv_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for row in csv_reader:
            cursor.execute(images_insert_query, row)

    # ======================================== Variant table=============================================

    create_variants_table_query = """
    CREATE TABLE IF NOT EXISTS variants (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        option1 VARCHAR(255),
        option2 VARCHAR(255),
        option3 VARCHAR(255),
        sku VARCHAR(255),
        requires_shipping BOOLEAN,
        taxable BOOLEAN,
        featured_image TEXT,
        available BOOLEAN,
        price DECIMAL(10, 2),
        grams INT,
        compare_at_price DECIMAL(10, 2),
        position INT,
        product_id BIGINT,
        created_at DATETIME,
        updated_at DATETIME
    )
    """
    drop_table_query = "DROP TABLE IF EXISTS variants"
    cursor.execute(drop_table_query)
    cursor.execute(create_variants_table_query)

    variants_insert_query = (
        "INSERT INTO variants (id, title, option1, option2, option3, sku, requires_shipping, taxable, "
        "featured_image, available, price, grams, compare_at_price, position, product_id, created_at, updated_at) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    with open(variants_csv_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            # print(row[6])
            row[6] = 1 if row[6] == 'True' else 0
            row[7] = 1 if row[7] == 'True' else 0
            row[9] = 1 if row[9] == 'True' else 0
            compare_at_price = row[12]
            if not compare_at_price or compare_at_price == '':
                row[12] = 0.0

            cursor.execute(variants_insert_query, row)

    # ========================== Options table=======================================

    create_options_table_query = """
    CREATE TABLE IF NOT EXISTS options (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        position INT,
        option_values TEXT
    )
    """

    drop_table_query = "DROP TABLE IF EXISTS options"
    cursor.execute(drop_table_query)
    cursor.execute(create_options_table_query)

    options_insert_query = (
        "INSERT INTO options (name, position, option_values) "
        "VALUES (%s, %s, %s)"
    )

    with open(options_csv_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for row in csv_reader:
            cursor.execute(options_insert_query, (row[0], int(row[1]), row[2]))

    connection.commit()
    cursor.close()
    connection.close()


addProductTitlesInCSV("data_json/mcaffeine_products.json")
export_csv("data_json/mcaffeine_products.json")
export_csv("data_json/kopari_products.json")
export_csv("data_json/plum_products.json")
export_csv("data_json/yogabars_products.json")
create_table()
