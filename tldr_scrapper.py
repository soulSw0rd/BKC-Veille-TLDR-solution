import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import os

def scrape_tldr_tech(date=None):
    """
    Scrape le rapport quotidien de tldr.tech pour une date donnée.
    
    Args:
        date (str, optional): Date au format YYYY-MM-DD. Par défaut, la date du jour.
    
    Returns:
        dict: Contient le titre, la date, le contenu et le statut du scraping
    """
    # Utiliser la date actuelle si aucune date n'est fournie
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    # Convertir la date au format YYYY-MM-DD en format YYYY-MM-DD pour l'URL
    try:
        if isinstance(date, str):
            # Vérifier le format de la date
            datetime.strptime(date, '%Y-%m-%d')
        year, month, day = date.split('-')
        url = f"https://tldr.tech/tech/{year}-{month}-{day}"
    except ValueError:
        return {
            "status": "error",
            "message": "Format de date invalide. Utilisez le format YYYY-MM-DD."
        }
    
    # En-têtes HTTP pour simuler un navigateur
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Faire la requête HTTP
        response = requests.get(url, headers=headers)
        
        # Vérifier les redirections (307) ou pages non trouvées (404)
        if response.status_code == 404 or response.status_code == 307:
            return {
                "status": "not_available",
                "message": f"Le rapport pour la date {date} n'est pas disponible (Code: {response.status_code})."
            }
        
        # Vérifier autres erreurs
        response.raise_for_status()
        
        # Parser le contenu HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraire le titre (la structure est maintenant plus précise)
        title_element = soup.find('h1', class_='text-center')
        title = title_element.text.strip() if title_element else "Titre non trouvé"
        
        # Extraire le sous-titre
        subtitle_element = soup.find('h2', class_='text-xl')
        subtitle = subtitle_element.text.strip() if subtitle_element else ""
        
        # Extraire les articles de chaque section
        articles = []
        sections = soup.find_all('section')
        
        for section in sections:
            # Ignorer les sections vides
            if not section.find('article'):
                continue
                
            # Extraire le titre de la section si présent
            section_header = section.find('h3', class_='text-center')
            section_title = section_header.text.strip() if section_header else "Section sans titre"
            
            # Extraire tous les articles de la section
            for article_elem in section.find_all('article'):
                try:
                    # Extraire le lien et le titre de l'article
                    link_elem = article_elem.find('a', class_='font-bold')
                    if not link_elem:
                        continue
                        
                    article_url = link_elem.get('href', '')
                    article_title = link_elem.find('h3').text.strip() if link_elem.find('h3') else "Titre non trouvé"
                    
                    # Extraire le contenu de l'article
                    content_div = article_elem.find('div', class_='newsletter-html')
                    article_content = content_div.get_text(strip=True) if content_div else ""
                    
                    # Vérifier si c'est un article sponsorisé
                    is_sponsored = "(Sponsor)" in article_title
                    
                    # Ajouter l'article à la liste
                    articles.append({
                        "title": article_title,
                        "url": article_url,
                        "content": article_content,
                        "category": section_title,
                        "is_sponsored": is_sponsored
                    })
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'un article: {e}")
                    continue
        
        return {
            "status": "success",
            "title": title,
            "subtitle": subtitle,
            "date": date,
            "articles": articles,
            "url": url,
            "article_count": len(articles)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Erreur lors de la requête: {str(e)}"
        }

def export_to_json(result, output_file=None):
    """
    Exporte les résultats du scraping au format JSON.
    
    Args:
        result (dict): Résultat du scraping
        output_file (str, optional): Chemin du fichier de sortie. Si None, utilise la date du rapport.
    
    Returns:
        str: Chemin du fichier JSON créé
    """
    import json
    
    if result["status"] != "success":
        print(f"Erreur: Impossible d'exporter des données invalides: {result['message']}")
        return None
    
    if output_file is None:
        output_file = f"tldr_tech_{result['date']}.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Données exportées avec succès vers {output_file}")
        return output_file
    except Exception as e:
        print(f"Erreur lors de l'export JSON: {e}")
        return None

def main():
    """Fonction principale pour exécuter le scraper depuis la ligne de commande."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scraper pour TLDR Tech')
    parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'),
                        help='Date au format YYYY-MM-DD (par défaut: date du jour)')
    parser.add_argument('--json', action='store_true', help='Exporter au format JSON')
    parser.add_argument('--output', type=str, help='Chemin du fichier de sortie pour l\'export JSON')
    parser.add_argument('--silent', action='store_true', help='Mode silencieux (n\'affiche pas les articles)')
    parser.add_argument('--category', type=str, help='Filtrer les articles par catégorie')
    parser.add_argument('--no-sponsor', action='store_true', help='Exclure les articles sponsorisés')
    
    args = parser.parse_args()
    
    result = scrape_tldr_tech(args.date)
    
    if result["status"] == "success":
        print(f"Titre: {result['title']}")
        if 'subtitle' in result:
            print(f"Sous-titre: {result['subtitle']}")
        print(f"Date: {result['date']}")
        print(f"URL: {result['url']}")
        print(f"Nombre d'articles: {result['article_count']}")
        
        # Filtrer les articles selon les critères
        filtered_articles = []
        for article in result['articles']:
            # Filtrer les articles sponsorisés si demandé
            if args.no_sponsor and article['is_sponsored']:
                continue
            
            # Filtrer par catégorie si demandé
            if args.category and args.category.lower() not in article['category'].lower():
                continue
                
            filtered_articles.append(article)
        
        # Mettre à jour le nombre d'articles après filtrage
        filtered_result = result.copy()
        filtered_result['articles'] = filtered_articles
        filtered_result['article_count'] = len(filtered_articles)
        
        # Exporter au format JSON si demandé
        if args.json:
            export_to_json(filtered_result, args.output)
        
        # Afficher les articles sauf en mode silencieux
        if not args.silent:
            print("\nArticles:")
            print("=" * 80)
            
            # Regrouper les articles par catégorie
            categories = {}
            for article in filtered_articles:
                category = article['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append(article)
            
            # Afficher les articles par catégorie
            if not categories:
                print("\nAucun article ne correspond aux critères de filtrage.")
            else:
                for category, articles in categories.items():
                # Filtrer par catégorie si spécifié
                    if args.category and category != args.category:
                        continue
                
                print(f"\n## {category}")
                print("-" * 80)
                
                for i, article in enumerate(articles, 1):
                    # Exclure les articles sponsorisés si demandé
                    if args.no_sponsor and article['is_sponsored']:
                        continue
                    
                    sponsor_tag = "[SPONSOR]" if article['is_sponsored'] else ""
                    print(f"{i}. {article['title']} {sponsor_tag}")
                    print(f"   URL: {article['url']}")
                    print(f"   {article['content'][:150]}..." if len(article['content']) > 150 else article['content'])
                    print()
    else:
        print(f"Erreur: {result['message']}")

if __name__ == "__main__":
    main()
