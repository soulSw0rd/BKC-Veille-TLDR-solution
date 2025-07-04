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
- 🤖 **Résumé intelligent avec LLM** (Ollama + nous-hermes2pro)
- 🎤 **Préparation pour Text-to-Speech** (TTS)
- ⚡ **Streaming en temps réel** des résumés

## Installation

1. **Installez Ollama et le modèle LLM :**
```bash
# Installation d'Ollama (voir https://ollama.ai)
# Téléchargez le modèle nous-hermes2pro
ollama pull adrienbrault/nous-hermes2pro:Q3_K_M

# Démarrez Ollama
ollama serve
```

2. **Clonez le repository :**
```bash
git clone <repository-url>
cd BKC-Veille-TLDR-solution
```

3. **Installez les dépendances :**
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

# 🤖 NOUVEAU : Résumé intelligent avec LLM
python tldr_scrapper.py --summarize

# Combinaison d'options avec résumé LLM
python tldr_scrapper.py --date 2024-12-20 --json --no-sponsor --category "SCIENCE & FUTURISTIC TECHNOLOGY" --summarize
```

### Utilisation comme module Python

```python
from tldr_scrapper import scrape_tldr_tech, export_to_json, summarize_and_prepare_tts

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
        
        # 🤖 NOUVEAU : Générer un résumé intelligent avec LLM
        if article['content']:
            summary = summarize_and_prepare_tts(article['content'])
            print(f"  Résumé LLM: {summary}")
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
            "is_sponsored": false,
            "summary_tts": "Résumé intelligent généré par LLM (si --summarize utilisé)"
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
| `--summarize` | **NOUVEAU** : Résumé intelligent avec LLM | `--summarize` |

## Exemples d'utilisation

### 🤖 Analyse intelligente avec résumé LLM
```bash
# Générer des résumés intelligents pour tous les articles
python tldr_scrapper.py --summarize

# Résumé + export JSON pour analyse
python tldr_scrapper.py --date 2024-12-20 --summarize --json --output analyse_ia.json

# Résumé par catégorie (ex: articles scientifiques uniquement)
python tldr_scrapper.py --category "SCIENCE" --summarize --no-sponsor
```

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

## Configuration LLM

### Ollama et nous-hermes2pro
Le projet utilise **Ollama** avec le modèle **adrienbrault/nous-hermes2pro:Q3_K_M** pour :
- Générer des résumés intelligents des articles
- Préparer le texte pour la synthèse vocale (TTS)
- Offrir une analyse contextuelle des contenus tech

**Configuration par défaut :**
```python
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "adrienbrault/nous-hermes2pro:Q3_K_M"
```

**Installation du modèle :**
```bash
# Télécharger le modèle (environ 2.3GB)
ollama pull adrienbrault/nous-hermes2pro:Q3_K_M

# Vérifier l'installation
ollama list
```

## 🤖 Fonctionnalités LLM Avancées

### Résumé intelligent
Le système utilise **nous-hermes2pro** pour générer des résumés concis et clairs des articles techniques :

```python
# Exemple d'utilisation programmatique
from tldr_scrapper import summarize_and_prepare_tts

article_content = "Long article technique..."
summary = summarize_and_prepare_tts(article_content)
print(f"Résumé : {summary}")
```

### Préparation Text-to-Speech
Les résumés sont optimisés pour la synthèse vocale :
- **Phrases courtes** et claires
- **Suppression du jargon** technique complexe
- **Prononciation facilitée** des termes techniques
- **Structure narrative** adaptée à l'écoute

### Streaming en temps réel
Les résumés sont générés en streaming pour une réactivité optimale :
- **Réponse progressive** dès les premiers mots
- **Pas de timeout** sur les longs contenus
- **Gestion d'erreur** robuste en cas de problème réseau

## Licence

Ce projet est sous licence GNU. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

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

### Problèmes de scraping
1. Vérifiez que toutes les dépendances sont installées
2. Vérifiez votre connexion internet
3. Assurez-vous que la date est au bon format (YYYY-MM-DD)
4. Consultez les messages d'erreur pour plus de détails

### Problèmes LLM/Ollama
1. **Ollama non accessible :**
   ```bash
   # Vérifiez qu'Ollama est en cours d'exécution
   ollama serve
   
   # Testez la connexion
   curl http://localhost:11434/api/tags
   ```

2. **Modèle non trouvé :**
   ```bash
   # Téléchargez le modèle
   ollama pull adrienbrault/nous-hermes2pro:Q3_K_M
   
   # Vérifiez qu'il est installé
   ollama list
   ```

3. **Timeout ou erreurs de streaming :**
   - Vérifiez que le port 11434 n'est pas bloqué
   - Redémarrez Ollama si nécessaire
   - Le modèle peut prendre du temps lors du premier chargement

4. **Résumés de mauvaise qualité :**
   - Le modèle nous-hermes2pro est optimisé pour les tâches techniques
   - Essayez d'autres modèles si disponibles : `ollama list`
