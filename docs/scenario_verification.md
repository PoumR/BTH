# Scénario de vérification — Bibliothèque de quartier

## Préparation

- Démarrer le serveur Django.
- Disposer d'un compte adhérent et d'un compte gestionnaire.
- Utiliser une base de test contenant les données CSV.

## Tests automatiques

Commande :

`python manage.py test`

Résultat : 
Found 7 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.......
----------------------------------------------------------------------
Ran 7 tests in 1.239s

OK
Destroying test database for alias 'default'...

**7 tests exécutés, 7 réussis, 0 échec.**

## Tests fonctionnels

- [x] **T01 — Catalogue :** afficher les livres, effectuer une recherche et filtrer par genre.
- [x] **T02 — Disponibilité :** vérifier qu'un livre ayant une réservation active affiche moins d'exemplaires disponibles que d'exemplaires totaux.
- [x] **T03 — Inscription :** créer un nouveau compte adhérent.
- [x] **T04 — Authentification :** se connecter puis se déconnecter.
- [x] **T05 — Réservation :** réserver un livre et vérifier qu'il apparaît dans « Mes demandes ».
- [x] **T06 — Annulation :** annuler une réservation autorisée et vérifier son nouvel état.
- [x] **T07 — Limite de trois :** créer trois réservations actives et vérifier que la quatrième est refusée.
- [x] **T08 — Stock épuisé :** vérifier qu'un livre sans exemplaire disponible ne peut plus être réservé.
- [x] **T09 — Gestionnaire :** passer une réservation de « En attente » à « Prête », puis à « Empruntée » et « Rendue ».
- [x] **T10 — Accès anonyme :** vérifier que `/mes-demandes/` redirige vers la connexion.
- [x] **T11 — Accès interdit :** vérifier qu'un adhérent reçoit une erreur 403 sur `/gestion/`.
- [x] **T12 — Formulaires invalides :** essayer une inscription avec des champs manquants et une adresse e-mail déjà utilisée.
- [ ] **T13 — Import :** sur une base de test, exécuter deux fois le chargement des CSV, puis vérifier l'absence de doublons et la conservation des dates.

## Bilan

12 tests fonctionnels validés sur 13.
Test T13 (réimportation des CSV) restant à vérifier.


## Anomalies constatées et corrections

//
