# Data Pipeline Project

## About the Project

This project automates the extraction of product and review data from an online API (dummyjson.com), transforms the data into a structured format, and loads it into a MySQL database. It includes features for extracting data from the API, exporting data to JSON files, importing data from JSON files into a database, and a menu-driven interface for data interaction. The project demonstrates data pipelining, API interaction, database management, and user-friendly interfaces.

This project was developed by:
* Andressa Lopes ([andressaclopes94](https://github.com/andressaclopes94))
* Bernardo Marta ([BernardoMarta](https://github.com/BernardoMarta))
* Daniela Esmeraldino ([danielaesmeraldino](https://github.com/danielaesmeraldino))
## How It Works

1.  **Data Extraction**: Extracts product and review data from the specified API endpoint.
2.  **JSON Export/Import**: Exports the extracted data into JSON files for storage and imports the JSON data into a MySQL database.
3.  **Database Management**: Manages the database schema, including tables for categories, products, and reviews.
4.  **Menu-Driven Interface**: Provides a text-based menu for users to interact with the data, including options to list products by category, view product details, and display product statistics.

## Getting Started

### Prerequisites

*   Python 3.x
*   Required Python libraries:
    *   `requests`
    *   `mysql-connector-python`
    *   `beaupy`
*   MySQL database server
*   Database credentials (host, user, password, database name)

Install the necessary Python libraries:

pip install requests mysql-connector-python beaupy

Set up the MySQL database:

1.  Create a database named `project_python`.
2.  Import the provided SQL schema (`project_python.sql`) to create the necessary tables.
3.  Update the database connection details in `project_python.py` and `functions.py`.

### Installation

1.  Clone the repository:

git clone https://github.com/BernardoMarta/Data_Pipeline_Project
cd Data_Pipeline_Project

2. Update the database credentials in `functions.py`.

connector = connect(
host='localhost',
user='root',
password='your_password',
database='project_python'
)

## Usage

Run the main script:

python project_python.py

Interact with the menu options to list products, view details, and display statistics.

## Data Flow

1.  Run `project_python.py`.
2.  The script will automatically:
    *   Import categories into the `category` table.
    *   Export products to `products.json`.
    *   Import products into the `product` table.
    *   Export reviews to `reviews.json`.
    *   Import reviews into the `review` table.
3.  Use the menu options to interact with the data:
    *   List products by category.
    *   View product details.
    *   Display product statistics (e.g., most expensive, cheapest, best rating, worst rating, average price by category).

## Features

*   Extracts product and review data from the API
*   Exports data to JSON format
*   Imports data into a MySQL database
*   Lists products by category
*   Shows product details
*   Displays product statistics
*   Menu-driven interface

## Contributing

Feel free to fork this repository and submit pull requests to <https://github.com/BernardoMarta/Data_Pipeline_Project>!

## License

This project is licensed under the MIT License.

## Acknowledgments

*   Thanks to the dummyjson.com for providing the API.
*   Thanks to the `requests`, `mysql-connector-python`, and `beaupy` libraries for enabling key functionalities.
