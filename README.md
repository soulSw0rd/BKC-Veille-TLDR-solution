# TLDR Tech Scraper

Un scraper Python pour extraire et analyser les rapports quotidiens de [TLDR Tech](https://tldr.tech).

## Description

Ce projet permet de récupérer automatiquement les articles du rapport quotidien TLDR Tech pour n'importe quelle date. Il extrait les titres, contenus, URLs et catégories des articles, avec des options de filtrage et d'export.

## Fonctionnalités

- 🗞️ Scraping des rapports quotidiens TLDR Tech
- 📅 Support de dates personnalisées (format YYYY-MM-DD)
- 🏷️ Extraction des catégories d'articles
- 💰 Détection des articles sponsorisés
- 🔍 Filtrage par catégorie
- 🚫 Exclusion des articles sponsorisés
- 📄 Export au format JSON
- 🔇 Mode silencieux
- 📊 Statistiques (nombre d'articles trouvés)

## Installation

1. Clonez le repository :
```bash
git clone <repository-url>
cd BKC-Veille-TLDR-solution
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Utilisation basique

Scraper le rapport du jour :
```bash
python tldr_scrapper.py
```

### Options avancées

```bash
# Scraper une date spécifique
python tldr_scrapper.py --date 2024-12-20

# Exporter au format JSON
python tldr_scrapper.py --json

# Exporter avec un nom de fichier personnalisé
python tldr_scrapper.py --json --output mon_rapport.json

# Mode silencieux (pas d'affichage des articles)
python tldr_scrapper.py --silent

# Filtrer par catégorie
python tldr_scrapper.py --category "BIG TECH & STARTUPS"

# Exclure les articles sponsorisés
python tldr_scrapper.py --no-sponsor

# Combinaison d'options
python tldr_scrapper.py --date 2024-12-20 --json --no-sponsor --category "SCIENCE & FUTURISTIC TECHNOLOGY"
```

### Utilisation comme module Python

```python
from tldr_scrapper import scrape_tldr_tech, export_to_json

# Scraper le rapport du jour
result = scrape_tldr_tech()

# Scraper une date spécifique
result = scrape_tldr_tech("2024-12-20")

# Vérifier le succès
if result["status"] == "success":
    print(f"Trouvé {result['article_count']} articles")
    
    # Accéder aux articles
    for article in result["articles"]:
        print(f"- {article['title']}")
        print(f"  Catégorie: {article['category']}")
        print(f"  URL: {article['url']}")
        print(f"  Contenu: {article['content'][:100]}...")
        print()
    
    # Exporter en JSON
    export_to_json(result, "rapport.json")
else:
    print(f"Erreur: {result['message']}")
```

## Structure des données

Le scraper retourne un dictionnaire avec la structure suivante :

```python
{
    "status": "success",
    "title": "TLDR",
    "subtitle": "Tech",
    "date": "2024-12-20",
    "url": "https://tldr.tech/tech/2024-12-20",
    "article_count": 15,
    "articles": [
        {
            "title": "Titre de l'article",
            "url": "https://example.com/article",
            "content": "Contenu de l'article...",
            "category": "BIG TECH & STARTUPS",
            "is_sponsored": false
        },
        // ... autres articles
    ]
}
```

## Catégories typiques

Les articles sont généralement classés dans ces catégories :
- **BIG TECH & STARTUPS** - Actualités des grandes entreprises tech et startups
- **SCIENCE & FUTURISTIC TECHNOLOGY** - Innovations et technologies d'avenir
- **PROGRAMMING, DESIGN & DATA SCIENCE** - Développement, design et data science
- **MISCELLANEOUS** - Divers

## Gestion des erreurs

Le scraper gère automatiquement plusieurs types d'erreurs :

- **404/307** : Rapport non disponible pour la date demandée
- **Format de date invalide** : Message d'erreur explicite
- **Erreurs réseau** : Gestion des timeouts et erreurs de connexion
- **Parsing HTML** : Validation de la structure des données

## Options de ligne de commande

| Option | Description | Exemple |
|--------|-------------|---------|
| `--date` | Date au format YYYY-MM-DD | `--date 2024-12-20` |
| `--json` | Exporter au format JSON | `--json` |
| `--output` | Nom du fichier de sortie JSON | `--output rapport.json` |
| `--silent` | Mode silencieux | `--silent` |
| `--category` | Filtrer par catégorie | `--category "BIG TECH"` |
| `--no-sponsor` | Exclure les articles sponsorisés | `--no-sponsor` |

## Exemples d'utilisation

### Analyse quotidienne automatisée
```bash
# Script pour analyser le rapport du jour et l'archiver
python tldr_scrapper.py --json --no-sponsor --output "archives/tldr_$(date +%Y-%m-%d).json"
```

### Recherche par catégorie
```bash
# Extraire uniquement les articles de science et technologie
python tldr_scrapper.py --category "SCIENCE" --no-sponsor
```

### Export pour analyse
```bash
# Exporter en mode silencieux pour traitement automatique
python tldr_scrapper.py --date 2024-12-20 --json --silent --output data.json
```

## Dépendances

- **requests** (>=2.31.0) : Requêtes HTTP
- **beautifulsoup4** (>=4.12.0) : Parsing HTML
- **lxml** (>=4.9.0) : Parser XML/HTML rapide

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Avertissements

- Respectez les conditions d'utilisation de TLDR Tech
- N'abusez pas du scraping (limitez la fréquence des requêtes)
- Ce scraper est à des fins éducatives et de veille technologique

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## Support

Si vous rencontrez des problèmes :
1. Vérifiez que toutes les dépendances sont installées
2. Vérifiez votre connexion internet
3. Assurez-vous que la date est au bon format (YYYY-MM-DD)
4. Consultez les messages d'erreur pour plus de détails
