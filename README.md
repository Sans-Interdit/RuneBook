# RuneBook

## Backend

### Outils et technologies

* **Poetry** pour gérer les environnements et les dépendances

  * `poetry lock`
  * `poetry install`
  * `poetry run python backend/app.py`
* **Flask** pour créer l’API
* **SQLAlchemy** comme ORM
* **PostgreSQL** pour la base de données

---

## Frontend

### Outils et structure

* **React** comme framework frontend

  * **AppContext** pour stocker les variables globales
  * **/pages** pour l'ensemble des pages principales
  * **/components** pour les composants d’interface réutilisables
  * **/api** pour toutes les requêtes vers le backend

![Architecture Backend](docs/images/backend.png)


* **TailwindCSS** pour le style et la mise en page
* **Vite** pour lancer et builder l’application

![Aperçu Frontend](docs/images/frontend.png)
