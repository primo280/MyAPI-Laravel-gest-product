import requests

BASE_URL = "http://127.0.0.1:8000/categories"

# Fonction pour afficher la réponse de manière lisible
def print_response(method, response):
    print(f"{method} Response:")
    if response.status_code in [200, 201]:
        try:
            print(response.json())
        except ValueError:
            print("No JSON response.")
    else:
        print(f"Status Code: {response.status_code}")
        print(response.text)
    print("-" * 50)

# Récupérer le jeton CSRF
def get_csrf_token():
    csrf_response = requests.get("http://127.0.0.1:8000/sanctum/csrf-cookie")
    if csrf_response.status_code == 200:
        return csrf_response.cookies['XSRF-TOKEN']
    else:
        print("Erreur lors de la récupération du jeton CSRF.")
        return None

# Ajouter le jeton CSRF aux en-têtes
def get_headers():
    csrf_token = get_csrf_token()
    if csrf_token:
        return {"X-CSRF-TOKEN": csrf_token}
    else:
        return {}

def list_categories():
    response = requests.get(BASE_URL)
    print_response("GET ALL", response)

def create_category():
    name = input("Entrez le nom de la catégorie : ")
    description = input("Entrez la description : ")
    headers = get_headers()  # Obtenir les en-têtes avec le jeton CSRF
    response = requests.post(BASE_URL, json={
        "name": name,
        "description": description
    }, headers=headers)  # Inclure les en-têtes
    print_response("POST", response)

def view_category():
    category_id = int(input("Entrez l'ID de la catégorie à afficher : "))
    response = requests.get(f"{BASE_URL}/{category_id}")
    print_response(f"GET ID {category_id}", response)

def update_category():
    category_id = int(input("Entrez l'ID de la catégorie à mettre à jour : "))
    name = input("Entrez le nouveau nom : ")
    description = input("Entrez la nouvelle description : ")
    headers = get_headers()  # Obtenir les en-têtes avec le jeton CSRF
    response = requests.put(f"{BASE_URL}/{category_id}", json={
        "name": name,
        "description": description
    }, headers=headers)  # Inclure les en-têtes
    print_response(f"PUT ID {category_id}", response)

def delete_category():
    category_id = int(input("Entrez l'ID de la catégorie à supprimer : "))
    headers = get_headers()  # Obtenir les en-têtes avec le jeton CSRF
    response = requests.delete(f"{BASE_URL}/{category_id}", headers=headers)  # Inclure les en-têtes
    print_response(f"DELETE ID {category_id}", response)

# Menu principal
def main():
    while True:
        print("\n--- Gestion des Catégories ---")
        print("1. Lister toutes les catégories")
        print("2. Créer une catégorie")
        print("3. Voir une catégorie spécifique")
        print("4. Mettre à jour une catégorie")
        print("5. Supprimer une catégorie")
        print("6. Quitter")
        
        choice = input("Choisissez une option : ")
        if choice == "1":
            list_categories()
        elif choice == "2":
            create_category()
        elif choice == "3":
            view_category()
        elif choice == "4":
            update_category()
        elif choice == "5":
            delete_category()
        elif choice == "6":
            print("Au revoir !")
            break
        else:
            print("Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
