import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse

def get_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    return response.text

def info_product(product):
    try:
        title = product.find("h3", class_="s-item__title").text if product.find("h3", class_="s-item__title") else "No title"
        
        price = product.find("span", class_="s-item__price").text if product.find("span", class_="s-item__price") else "No price"
        
        original_price = product.find("span", class_="s-item__original-price").text if product.find("span", class_="s-item__original-price") else None
        
        link = product.find("a", class_="s-item__link")["href"] if product.find("a", class_="s-item__link") else "No link"
        
        if original_price:
            price_comparison = f"Precio original: {original_price} | Precio con descuento: {price}"
        else:
            price_comparison = f"Precio: {price}"
        
        return {"title": title, "price": price_comparison, "link": link}
    
    except AttributeError:
        return None

def search(product_name):
    
    search_url = f"https://www.ebay.com/sch/i.html?_nkw={urllib.parse.quote(product_name)}&_ipg=240"
    html = get_url(search_url)
    soup = BeautifulSoup(html, 'html.parser')
    
    products = soup.find_all("li", class_="s-item")
    product_list = []
    
    # Limitar la búsqueda a 25 productos
    for index, product in enumerate(products):
        if index >= 25:
            break
        product_info = info_product(product)
        if product_info:
            product_list.append(product_info)
            
    return product_list

def archivo_excel(products, filename="productos.xlsx"):
    df = pd.DataFrame(products)
    df.to_excel(filename, index=False)

def main():
    product = input("Ingresa el producto que deseas buscar: ")
    
    products = search(product)
    
    if products:
        archivo_excel(products)
        print(f"Se han guardado {len(products)} productos en el archivo Excel.")
    else:
        print("No se encontraron productos.")

if __name__ == "__main__":
    main()
