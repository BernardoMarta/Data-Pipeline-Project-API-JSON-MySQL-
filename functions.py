# Projeto Python- Andressa Lopes, Bernardo Marta, Daniela Esmeraldino.
 
import requests
import json
from mysql.connector import connect, Error
import beaupy
 
#Global variables
 
ENDPOINT= "https://dummyjson.com/products?limit=0"
menu_width=70

#Functions

def extractData():
    """ Extrai dados de produtos da API e retorna uma lista de dicionários contendo as informações de cada produto."""
    productsList=[]
    response = requests.get(url= ENDPOINT)
    if response.status_code == 200:
        whole_data = response.json().get('products')
        for item in whole_data:
            productsList.append({
                'title': (item.get('title').title()),
                'description': item.get('description'),
                'category': (item.get('category').title()),
                'price' : item.get('price'),
                'rating' : item.get('rating'),
                'stock' : item.get('stock'),
                'brand' : (item.get('brand','NA').title())
            })
        return productsList
    else:
        print("\nErro: Não é possível aceder ao API\n")
 
def extractCategories():
    """ Extrai as categorias únicas dos produtos e retorna uma lista. """
    categories = set()
    response = requests.get(url=ENDPOINT)
    if response.status_code == 200:
        whole_data = response.json().get('products')
        for item in whole_data:
            categories.add(item.get('category').title())
    return list(categories)
 
def exportJsonCategories():
    """ Exporta as categorias para um arquivo JSON. """
    categories = extractCategories()
    with open("categories.json", "w", encoding="utf-8") as file_json:
        json.dump(categories, file_json, indent=4, ensure_ascii=False)
       
def importDataCategories():
    """ Importa as categorias do arquivo JSON para o banco de dados (antes dos produtos). """
    try:
        connector = connect(
            host='localhost',
            user='root',
            database='project_python'
        )
        cursor = connector.cursor()
        with open('categories.json', 'r', encoding='utf-8') as file:
            dataCategories = json.load(file)
        for category in dataCategories:
            cursor.execute(
                'INSERT INTO category (name) VALUES (%s)',
                (category,)
            )
        connector.commit()
        cursor.close()
        connector.close()
        print('\nDados das categorias exportados para a base de dados com sucesso\n')
    except Error as err:
        print('\nNão foi possível exportar os dados das categorias para a base de dados\n')
        print(f'{err.errno} - {err.msg}')
       
def importDataProducts():
    """ Importa produtos do JSON para o banco de dados. """
    try:
        connector=connect(
            host= 'localhost',
            user='root',
            database='project_python'
        )
        cursor=connector.cursor()
       
        with open('products.json','r',encoding='utf-8') as file:
            dataProducts = json.load(file)
           
        for product in dataProducts:
            # Buscar o ID da categoria pelo nome
            cursor.execute(
                "SELECT id FROM category WHERE name = %s",
                (product['category'],)
            )
            category_id = cursor.fetchone()
            if category_id is None:
                print(f"Erro: Categoria '{product['category']}' não encontrada na tabela 'category'.")
                continue  
            category_id = category_id[0]
 
            cursor.execute(
                'INSERT INTO product (title, description, category, price, rating, stock, brand) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                (product['title'],product['description'],category_id,product['price'],product['rating'],product['stock'],product['brand'])
            )
       
        connector.commit()
        cursor.close()
        connector.close()
       
        print('\nDados dos produtos exportados para a base de dados com sucesso\n')
    except Error as err:
        print('\nNão foi possível exportar os dados dos produtos para a base de dados\n')
        print(f'{err.errno} - {err.msg}')              
 
def extractReview():
    """ Extrai dados de avaliações dos produtos da API. """
    productsReview=[]
    response = requests.get(url= ENDPOINT)
    if response.status_code == 200:
        whole_data = response.json().get('products')
        for item in whole_data:
            for review in item['reviews']:
                productsReview.append({
                    'title': item.get('title'),
                    'rating' : review.get('rating'),
                    'comment' : review.get('comment'),
                    'date' : review.get('date'),
                    'reviewerName' : review.get('reviewerName'),
                    'reviewerEmail' : review.get('reviewerEmail')
                })
        return productsReview
    else:
        print("\nErro: Não é possível aceder ao API\n")
 
def exportJsonProducts():
    """ Exporta produtos para arquivo JSON """
    productsList=extractData()
    with open("products.json", "w", encoding="utf-8") as file_json:
        json.dump(productsList, file_json, indent=4, ensure_ascii=False)      
       
def exportJsonReviews():
    """ Exporta avaliações para arquivo JSON."""
    productsReview=extractReview()
    with open("reviews.json", "w", encoding="utf-8") as file_json:
        json.dump(productsReview, file_json, indent=4, ensure_ascii=False)  
 
def importDataReviews():
    """ Importa avaliações do JSON para o banco de dados."""
    try:
        connector=connect(
            host= 'localhost',
            user='root',
            database='project_python'
        )
        cursor=connector.cursor()
       
        with open('reviews.json','r',encoding='utf-8') as file:
            dataReviews = json.load(file)
           
        for review in dataReviews:
            cursor.execute(
                'INSERT INTO review (title, rating, comment, date, reviewerName, reviewerEmail) VALUES (%s,%s,%s,%s,%s,%s)',
                (review['title'],review['rating'],review['comment'],review['date'],review['reviewerName'],review['reviewerEmail'])
            )
       
        connector.commit()
        cursor.close()
        connector.close()
       
        print('\nDados das reviews exportados para a base de dados com sucesso\n')
    except Error as err:
        print('\nNão foi possível exportar os dados das reviews para a base de dados\n')
        print(f'{err.errno} - {err.msg}')
 
def listProductByCategory():
    """ Lista produtos organizados por categoria."""
    prodList = extractData()
    categories=[]
    for product in prodList:
        if product['category'] not in categories:
            categories.append(product['category'])
    for category in categories:
        counter=1
        print('-'*40)
        print(f'CATEGORY: {category}'.center(40))
        print('-'*40)
        for product in prodList:
            if product['category'] == category:
                print(f'{counter}. {product['title']}')
                counter += 1
 
def printProductDetails(product_name):
    """ Mostra detalhes completos de um produto específico."""
    print()
    products= extractData()
    for product in products:
        if product['title'] == product_name:
            for a,b in product.items():
                print(f'{a.upper()}: {b}')
 
def mostExpensiveProd():
    """ Identifica e mostra o produto mais caro."""
    products=extractData()
    price_list=[]
    for product in products:
        if product['price'] not in price_list:
            price_list.append(product['price'])
    max_price=max(price_list)
    for product in products:
        if product['price'] == max_price:
            print(f'The most expensive product is: {product['title']}.')
    print(f'It costs {max_price}')
 
def leastExpensiveProd():
    """ Identifica e mostra o produto mais barato. """
    products=extractData()
    price_list=[]
    for product in products:
        if product['price'] not in price_list:
            price_list.append(product['price'])
    min_price=min(price_list)
    for product in products:
        if product['price'] == min_price:
            print(f'The cheapest product is: {product['title']}.')
    print(f'It costs {min_price}')
 
def worstRating():
    """ Mostra o produto com a pior avaliação."""
    products=extractData()
    rating_list=[]
    for product in products:
        if product['rating'] not in rating_list:
            rating_list.append(product['rating'])
    min_rating=min(rating_list)
    for product in products:
        if product['rating'] == min_rating:
            print(f'The worst rating is about: {product['title']}.')
    print(f"It's worst rating is {min_rating}")
 
def BestRating():
    """ Mostra o produto com a melhor avaliação."""
    products=extractData()
    rating_list=[]
    for product in products:
        if product['rating'] not in rating_list:
            rating_list.append(product['rating'])
    max_rating=max(rating_list)
    for product in products:
        if product['rating'] == max_rating:
            print(f'The best rating is about: {product['title']}.')
    print(f"It's best rating is {max_rating}")
 
def AveragePriceByCateg():
    """ Calcula e mostra preço médio por categoria."""
    products=extractData()
    soma=0
    counter=0
    categories=[]
    for product in products:
        if product['category'] not in categories:
            categories.append(product['category'])
    options = products
    choice = beaupy.select(
        options=[f"{category.title()}" for category in (categories)],  # The options you want to present
        cursor_style='green1'
    )
   
   
    for product in products:
        if product['price'] !=0 and product['category']== choice:
            soma+=product['price']
            counter+=1
           
    average=soma/counter
    print(f"The average price of the products in the category {choice} is: {average:.2f}")
 
def menuStatistics():
    """ Menu de opções para estatísticas dos produtos."""
    options_menu_statistics = [
        "Verificar o produto mais caro e mais barato",
        "Verificar a média de preço por categoria",
        "Verificar o produto com melhor e pior avaliação",
        "Sair"
    ]
   
    choice1 = beaupy.select(
        options=[f"{i + 1}. {option}" for i, option in enumerate( options_menu_statistics)],
        cursor_style='green1'
    )
   
    return choice1
 
def menu():
    """ Menu principal do programa."""
    print('-'*menu_width)
    print(f'MENU'.center(menu_width))
    print('-'*menu_width,'\n')
    options = [
        "Listar todos os produtos organizados por categoria",
        "Consultar os detalhes de um produto específico, incluindo suas avaliações",
        "Exibir estatísticas relacionadas aos produtos",
        "Sair"
    ]
   
    choice = beaupy.select(
        #message="Escolha uma opção",
        options=[f"{i + 1}. {option}" for i, option in enumerate(options)],  # The options you want to present
        cursor_style='green1'
        #default=0,  # Default option (first one)
    )
 
    if choice == '1. Listar todos os produtos organizados por categoria':
        choice=menu_categories()
        productsCategory(choice)
        print()
        menu()
    elif choice == '2. Consultar os detalhes de um produto específico, incluindo suas avaliações':
        choice=menu_categories()
        choice=menu_productByCategory(choice)
        printProductDetails(choice)
        pass
        print()
        menu()
    elif choice == '3. Exibir estatísticas relacionadas aos produtos':
        print()
        choice1=menuStatistics()
        if choice1== "1. Verificar o produto mais caro e mais barato":
            mostExpensiveProd()
            leastExpensiveProd()
        elif choice1== "2. Verificar a média de preço por categoria":
            AveragePriceByCateg()
        elif choice1== "3. Verificar o produto com melhor e pior avaliação":
            worstRating()
            BestRating()
        pass
        print()
                                 
        menu()
    elif choice == '4. Sair':

        connection = connect(
            host='localhost',
            user='root',
            database='project_python'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute("TRUNCATE TABLE review;")
            cursor.execute("TRUNCATE TABLE product;")
            cursor.execute("TRUNCATE TABLE category;")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

            print()
            print("Adeus!")
            print()
            exit()
 
def menu_categories():
    """Menu de seleção de categorias."""
    prodList = extractData()
    categories=[]
    for product in prodList:
        if product['category'] not in categories:
            categories.append(product['category'])
    options = categories
    choice = beaupy.select(
        options=[f"{category}" for category in (categories)],  # The options you want to present
        cursor_style='green1'
    )
    return choice
 
def menu_productByCategory(category):
    """ Menu de seleção de produtos por categoria. """
    prodList = extractData()
    products=[]
    for product in prodList:
        if product['category'] == category:
            products.append(product['title'])
    options = products
    choice = beaupy.select(
        options=[f"{product.title()}" for product in (products)],  # The options you want to present
        cursor_style='green1'
    )
    return choice
   
def productsCategory(category):
    """ Lista produtos de uma categoria específica. """
    print('-'*menu_width)
    print(f'CATEGORY: {category}'.center(menu_width))
    print('-'*menu_width)
    counter=1
    prodList = extractData()
    for product in prodList:
        if product['category'] == category:
            print(f'{counter}. {product['title']}')
            counter += 1
 
