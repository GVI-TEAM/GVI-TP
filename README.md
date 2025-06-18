# GVI-TP

## 🌟 Objectif général

Vous devez concevoir en équipe une API REST permettant de gérer des **réservations de salles** dans un établissement.

Ce projet met en œuvre :

* le versioning de code via **Git Flow**
* le **versionnement sémantique** des livraisons
* les **pull requests** et **revues de code**
* les **tests unitaires**
* la création de **releases GitHub**

Les groupes sont totalement autonomes dans leur organisation, mais la **parallélisation des tâches** est une compétence clé évaluée dans ce TP.

---

## 🔧 Étape 1 – MVP (`v1.0.0`)

Votre objectif est de livrer une première version fonctionnelle de l’API en **1 heure maximum**.

### Fonctionnalités attendues :

1. **Gestion des salles**

   * Création, consultation, modification, suppression
   * Champs : nom, capacité, localisation

2. **Réservation**

   * Création et consultation de réservations
   * Réservation sur une salle donnée, un jour et une heure précise (durée = 1h fixe)
   * Un utilisateur est associé à chaque réservation

3. **Contrainte métier**

   * Une salle ne peut pas être réservée plusieurs fois sur le même créneau horaire

### Contraintes :

* Base de données SQLite (SQLAlchemy + Alembic)
* Tests unitaires minimum
* Une première **release GitHub `v1.0.0`** est attendue à l’issue du MVP

---

## 🧩 Étape 2 – Lot de fonctionnalités (`v1.1.0`)

Ajoutez **4 fonctionnalités simples et indépendantes**, pouvant être développées en parallèle.

### Fonctionnalités proposées :

1. Ajouter un champ `disponible` (booléen) sur les salles
2. Permettre de filtrer les salles par disponibilité (`GET /salles?disponible=true`)
3. Ajouter la suppression de réservation (`DELETE /reservations/{id}`)
4. Ajouter un champ `commentaire` (texte libre) dans les réservations

Une nouvelle **release GitHub `v1.1.0`** est attendue à la fin du lot.

---

## 🥮 Tests attendus

* Tests unitaires sur les fonctionnalités du MVP
* Tests sur les 4 fonctionnalités du lot

---

## 🔁 Git et collaboration

* Utilisez **Git Flow** pour organiser les branches
* Chaque fonctionnalité doit faire l’objet d’une **branche dédiée**
* Toute intégration passe par une **pull request avec revue**
* L’historique Git doit rester propre et structuré

---

## 🚀 Releases

* Une **release GitHub** est attendue pour chaque version stable :

  * `v1.0.0` à la fin du MVP
  * `v1.1.0` à la fin du lot 1
* Un changelog minimal doit être inclus

---

## 📊 Modèle de données

### Salle

| Champ        | Type    | Description                      |
| ------------ | ------- | -------------------------------- |
| id           | UUID    | Identifiant unique               |
| nom          | string  | Nom de la salle                  |
| capacité     | integer | Nombre maximal de personnes      |
| localisation | string  | Description ou code du bâtiment  |
| disponible   | boolean | Optionnel (ajouté dans `v1.1.0`) |

### Réservation

| Champ       | Type      | Description                           |
| ----------- | --------- | ------------------------------------- |
| id          | UUID      | Identifiant unique                    |
| salle\_id   | UUID (FK) | Référence vers une salle              |
| date        | date      | Date de la réservation                |
| heure       | time      | Heure de début de la réservation (1h) |
| utilisateur | string    | Identifiant ou nom de l’utilisateur   |
| commentaire | string    | Optionnel (ajouté dans `v1.1.0`)      |