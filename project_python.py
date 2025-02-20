# Projeto Python- Andressa Lopes, Bernardo Marta, Daniela Esmeraldino.
 
import requests
import json
from mysql.connector import connect, Error
import beaupy
from functions import *

importDataCategories()
exportJsonProducts()
importDataProducts()
exportJsonProducts()
exportJsonReviews()
importDataReviews()
menu()
