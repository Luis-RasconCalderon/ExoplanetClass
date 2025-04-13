import requests
from bs4 import BeautifulSoup
import csv
import json

# URL con el GET endpoint. Se obtiene al inspeccionar la página del NASA Exoplanet Catalog. 
base_url = "https://science.nasa.gov/wp-json/smd/v1/content-list/"

# Parámetros del Payload luego de aplicar el filtro en el tipo de planeta. La variable que nos importa es "meta_fields"
meta_field = 'like' # Se especifica el valor que tendrá este campo. Dependiendo del valor, buscará el tipo de planeta. Los valores son: {Terrestres: 'Terrestrial', Super Tierras: 'Super Earth', Neptunianos: 'like', Gigantes Gaseosos: 'Gas Giant'}
payload_params = {
    "exclude_child_pages": "false",
    "layout": "grid",
    "listing_page": "no",
    "listing_page_category_id": 2013,
    "number_of_items": 15, 
    "order": "DESC",
    "orderby": "date",
    "requesting_id": 199043,
    "science_only": "false",
    "show_content_type_tags": "no",
    "show_excerpts": "no",
    "show_pagination": "true",
    "show_readtime": "no",
    "show_thumbnails": "yes",
    "response_format": "html",
    "show_drafts": "false",
    "post_types": "exoplanet",
    "meta_fields": json.dumps({"planet_type": [f'{meta_field}']}),  # En esta variable se especifíca el filtro que se esta utilizando. 
}

# Lista que contendrá el nombre de los planetas
all_type_planets = []

# Loop que busca en todas las páginas del filtro aplicado
current_page = 1
while True:
    print(f"Buscando en página # {current_page}...")
    payload_params["current_page"] = current_page
    response = requests.get(base_url, params=payload_params)

    content_html = response.json().get("content", "")
    soup = BeautifulSoup(content_html, "html.parser")

    # Extracción de nombres de tipo de exoplanetas especificado
    exoplanet_items = soup.find_all(class_="hds-content-item content-list-item-exoplanet")
    if not exoplanet_items:
        print("No se encontraron más exoplanetas. ")
        break

    for item in exoplanet_items:
        name_tag = item.find(class_="hds-a11y-heading-22")
        if name_tag:
            all_type_planets.append(name_tag.get_text(strip=True))

    current_page += 1

# Guardando en un csv. El archivo contiene solamente los nombres, se agregó el tipo manualmente. La unión de todos los nombres y tipos en un solo archivo también se hizo manualmente. 
with open(f"{meta_field}_exoplanets.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Exoplanet Name"])
    for name in all_type_planets:
        writer.writerow([name])

print(f"Se obtuvieron {len(all_type_planets)} nombres de planetas de tipo {meta_field}.")
