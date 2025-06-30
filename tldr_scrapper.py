import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import os
import json

def scrape_tldr_tech(date=None):
    """
    Scrape le rapport quotidien de tldr.tech pour une date donnée.
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    try:
        datetime.strptime(date, '%Y-%m-%d')
        year, month, day = date.split('-')
        url = f"https://tldr.tech/tech/{year}-{month}-{day}"
    except ValueError:
        return {
            "status": "error",
            "message": "Format de date invalide. Utilisez le format YYYY-MM-DD."
        }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code in [404, 307]:
            return {
                "status": "not_available",
                "message": f"Le rapport pour la date {date} n'est pas disponible (Code: {response.status_code})."
            }
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        title_element = soup.find('h1', class_='text-center')
        title = title_element.text.strip() if title_element else "Titre non trouvé"

        subtitle_element = soup.find('h2', class_='text-xl')
        subtitle = subtitle_element.text.strip() if subtitle_element else ""

        articles = []
        sections = soup.find_all('section')

        for section in sections:
            if not section.find('article'):
                continue

            section_header = section.find('h3', class_='text-center')
            section_title = section_header.text.strip() if section_header else "Section sans titre"

            for article_elem in section.find_all('article'):
                try:
                    link_elem = article_elem.find('a', class_='font-bold')
                    if not link_elem:
                        continue

                    article_url = link_elem.get('href', '')
                    article_title = link_elem.find('h3').text.strip() if link_elem.find('h3') else "Titre non trouvé"

                    content_div = article_elem.find('div', class_='newsletter-html')
                    article_content = content_div.get_text(strip=True) if content_div else ""

                    is_sponsored = "(Sponsor)" in article_title

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

def summarize_and_prepare_tts(text, model="adrienbrault/nous-hermes2pro:Q3_K_M"):
    """
    Utilise Ollama en streaming pour générer un résumé TTS clair et concis.
    """
    url = "http://localhost:11434/api/chat"
    prompt = (
        "Tu es un assistant qui résume les articles techniques "
        "et prépare le résumé pour une lecture claire en text-to-speech. "
        "Sois concis et clair.\n\n"
        f"Texte original : {text}\n\n"
        "Résumé et préparation pour TTS :"
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Assistant de résumé technique et préparation TTS."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        with requests.post(url, json=payload, stream=True) as response:
            response.raise_for_status()
            summary_parts = []
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        content_piece = chunk.get("message", {}).get("content", "")
                        if content_piece:
                            summary_parts.append(content_piece)
                        if chunk.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
            return "".join(summary_parts).strip()
    except Exception as e:
        print(f"Erreur lors de l'appel LLM pour résumé : {e}")
        return ""


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Scraper TLDR Tech + résumé avec Nous Hermes 2 + préparation TTS')
    parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='Date YYYY-MM-DD')
    parser.add_argument('--json', action='store_true', help='Exporter en JSON')
    parser.add_argument('--output', type=str, help='Fichier de sortie JSON')
    parser.add_argument('--silent', action='store_true', help='Mode silencieux')
    parser.add_argument('--category', type=str, help='Filtrer par catégorie')
    parser.add_argument('--no-sponsor', action='store_true', help='Exclure sponsorisés')
    parser.add_argument('--summarize', action='store_true', help='Faire résumé + préparation TTS avec Nous Hermes 2')

    args = parser.parse_args()

    result = scrape_tldr_tech(args.date)

    if result["status"] == "success":
        print(f"Titre: {result['title']}")
        if result.get('subtitle'):
            print(f"Sous-titre: {result['subtitle']}")
        print(f"Date: {result['date']}")
        print(f"URL: {result['url']}")
        print(f"Nombre d'articles: {result['article_count']}")

        filtered_articles = []
        for article in result['articles']:
            if args.no_sponsor and article['is_sponsored']:
                continue
            if args.category and args.category.lower() not in article['category'].lower():
                continue

            if args.summarize:
                # Appel résumé + préparation TTS
                article['summary_tts'] = summarize_and_prepare_tts(article['content'])
            else:
                article['summary_tts'] = None

            filtered_articles.append(article)

        filtered_result = result.copy()
        filtered_result['articles'] = filtered_articles
        filtered_result['article_count'] = len(filtered_articles)

        if args.json:
            export_to_json(filtered_result, args.output)

        if not args.silent:
            print("\nArticles:")
            print("=" * 80)

            categories = {}
            for article in filtered_articles:
                cat = article['category']
                categories.setdefault(cat, []).append(article)

            if not categories:
                print("\nAucun article ne correspond aux critères.")
            else:
                for cat, arts in categories.items():
                    if args.category and cat != args.category:
                        continue
                    print(f"\n## {cat}")
                    print("-" * 80)
                    for i, art in enumerate(arts, 1):
                        if args.no_sponsor and art['is_sponsored']:
                            continue
                        sponsor_tag = "[SPONSOR]" if art['is_sponsored'] else ""
                        print(f"{i}. {art['title']} {sponsor_tag}")
                        print(f"   URL: {art['url']}")
                        print(f"   {art['content'][:150]}..." if len(art['content']) > 150 else art['content'])
                        if args.summarize and art['summary_tts']:
                            print(f"\n   Résumé & préparation TTS:\n   {art['summary_tts']}\n")
    else:
        print(f"Erreur: {result['message']}")

if __name__ == "__main__":
    main()
