# Bibliothèque de quartier — Django

Application pédagogique de bibliothèque réalisée en équipe : catalogue, comptes utilisateurs et cycle de réservation.

## Fonctionnalités

- Accueil avec sélection de 4 livres et navigation commune.
- Catalogue avec recherche par titre/auteur/année/genre, filtre par genre et pagination (24 livres).
- Fiche détaillée, quantité d'exemplaires, nombre de copies disponibles et bouton de demande.
- Inscription, connexion par e-mail et déconnexion, avec contrôle des droits.
- Réservation réservée aux utilisateurs connectés ; limite de 3 demandes actives par personne, et exemplaires limités par livre.
- Mes demandes, annulation admissible et gestion des transitions par un gestionnaire.
- Interface responsive avec feuilles CSS dédiées, messages et formulaires CSRF.

## Architecture

| Application | Usage |
|---|---|
| `app` | Modèles `Livre` et `Genre` liés aux tables existantes `app_livre`, `app_genre` |
| `catalogue` | `ListView`, `DetailView`, recherche, filtre et pages HTML |
| `users` | `Emprunteur` (modèle utilisateur personnalisé), inscription et authentification |
| `reservation` | Modèle et vues de réservation, droits, transitions |

Technologies : Python, Django 6.1.3, SQLite, ORM Django, HTML/CSS. Vues orientées objet pour les parcours principaux. Les fichiers CSV de démonstration sont dans `donnees/`.

## Installation (Windows / PowerShell)

1. Ouvrir un terminal **dans le dossier contenant `manage.py`**.
2. Créer et activer l'environnement depuis Ubuntu :

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Vérifier Django
python manage.py check

# Créer les tables
python manage.py migrate

# Charger les données de démonstration
python manage.py charger_demo

# Lancer le serveur
python manage.py runserver

   ```Avec powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```
3. Copier `.env.example` vers `.env`, définir une vraie `SECRET_KEY` et garder `DEBUG=True` pour le développement.
4. **Faire une copie de sauvegarde de la base avant toute migration.** La base historique est conservée sous `db_avant_integration.sqlite3.bak` (300 livres, 12 genres). Elle n’est volontairement pas utilisée comme base active : son historique de migrations correspond à l’ancien modèle utilisateur. La première migration crée une nouvelle `db.sqlite3`, puis `charger_demo` réimporte les données CSV.
5. ```powershell
   python manage.py check
   python manage.py migrate
   python manage.py charger_demo
   python manage.py runserver
   ```

6. Ouvrir <http://127.0.0.1:8000/>.

L'import `charger_demo` utilise les CSV fournis pour ajouter ou mettre à jour les 12 genres, les 300 livres, les 20 utilisateurs et les réservations, et conserver les dates historiques. Les utilisateurs de démonstration importés lors de leur création reçoivent le mot de passe local `DEFAULT_PASSWORD` (par défaut `demo1234`) : **ne jamais utiliser ces identifiants en production**.

**Important pour le projet fusionné :** les migrations historiques créent un ancien `app.Emprunteur`, tandis que le code actuel utilise `users.Emprunteur`. Une migration de fusion `app/0004_merge_models.py` réunit les deux branches `0003`. La copie reçue possédait seulement les migrations historiques `app` appliquées. La base historique est préservée, tandis que le démarrage se fait sur une base neuve pour éviter l’incohérence d’historique liée au changement de `AUTH_USER_MODEL`. Si `migrate` échoue, ne supprimez rien : fournir le traceback à l’équipe avant toute nouvelle opération.

## Routes principales

| URL | Description |
|---|---|
| `/` | Accueil |
| `/catalogue/` | Liste, recherche et genre |
| `/catalogue/<id>/` | Fiche détaillée |
| `/inscription/`, `/connexion/`, `/deconnexion/` | Authentification |
| `/mes-demandes/` | Réservations personnelles |
| `/gestion/` | Traitement réservé aux gestionnaires |
| `/admin/` | Administration Django |

## Réservations : règles métier

- `en_attente → prete` ou `annulee`
- `prete → empruntee` ou `annulee`
- `empruntee → rendue`
- Un adhérent peut annuler `en_attente` ou `prete`.
- États actifs : `en_attente`, `prete`, `empruntee`.
- Maximum 3 réservations actives pour un adhérent ; au plus `livre.exemplaires` réservations actives par livre.
- Les actions modifiant les données utilisent POST + `{% csrf_token %}` ; les transitions sont contrôlées côté serveur.

## Contrôles avant soutenance

1. `python manage.py check` et `python manage.py migrate --plan`.
2. Connexion, déconnexion et inscription d'un adhérent.
3. Recherche « Hugo », filtre « roman », puis fiche `/catalogue/10/`.
4. Réservation d'un livre, affichage dans « Mes demandes », annulation.
5. Connexion gestionnaire et transitions successives, tentative d'accès interdit d'un adhérent.
6. Tester les limites d'exemplaires et de 3 réservations et le rechargement des CSV.

## Notes d'équipe

Ne pas modifier `AUTH_USER_MODEL` sur une base existante sans migration de données coordonnée. Les migrations d'origine sont conservées, avec un fichier de fusion de leurs deux branches `0003`. Ne pas faire de `reset --hard` dans le dépôt collaboratif sans sauvegarde.
