# GPAO V4 - Gestion de Production Assistée par Ordinateur

**Système complet de gestion de production pour atelier électromécanique**

---

## 📋 Description du projet

GPAO V4 est une application web complète de gestion de production assistée par ordinateur, développée avec Django. Cette version intègre l'ensemble des fonctionnalités essentielles pour la gestion industrielle d'un atelier, depuis la planification de la production jusqu'au suivi des stocks et de la maintenance.

## ✨ Fonctionnalités principales

### 🏭 Gestion des Articles
- **Multi-types d'articles** : Matières premières, Composants, Semi-finis, Produits finis
- **Gestion des stocks** : Stock actuel, stock de sécurité, point de commande
- **Calculs automatiques** :
  - EOQ (Economic Order Quantity) / Quantité économique de commande
  - Point de commande suggéré
  - Classification ABC des articles
- **Délais d'approvisionnement** (Lead time) configurables

### 📊 Planification de la Production
- **PDP / MPS** (Programme Directeur de Production) via `MPSItem`
- **CBN / MRP** (Calcul des Besoins Nets) temporel par semaines
- **Réceptions programmées** avec gestion des dates d'échéance
- **Gammes de production** avec séquences d'opérations

### 🏗️ Nomenclatures (BOM)
- **Structure hiérarchique** des produits
- **Coefficients de rebut** (scrap rate) configurables
- **Gestion des liens parent/composant**

### 🔄 Gestion des Ordres
- **OF (Ordres de Fabrication)** avec statuts de suivi
- **OT (Ordres de Travail)** par opération
- **Commandes clients** avec lignes de commande
- **Suivi des statuts** : Planifié, Lancé, En cours, Terminé

### ⚙️ Gestion des Machines
- **Capacité hebdomadaire** configurable
- **Statuts de disponibilité** : Disponible, En panne, Maintenance
- **Calcul de la charge/capacité** machine
- **Graphiques des décalages** de production

### 📦 Gestion des Stocks
- **Mouvements de stock** : Entrées, Sorties, Ajustements
- **Historique des mouvements** avec références
- **Contrôle qualité** des articles produits

### 🔧 Maintenance
- **Tickets de maintenance** liés aux machines
- **Suivi des statuts** : Ouvert, En cours, Résolu
- **Impact sur la disponibilité** des équipements

### 📈 Indicateurs et Analyses
- **Classification ABC** des articles
- **Point de commande** automatique
- **Stock de sécurité** paramétrable
- **Délais et lancements décalés**

---

## 🚀 Installation et Lancement

### Prérequis
- Python 3.13
- PowerShell (Windows)

### Étapes d'installation

```powershell
# 1. Naviguer vers le répertoire du projet
cd gpao_v4_complete

# 2. Créer l'environnement virtuel
py -3.13 -m venv .venv

# 3. Activer l'environnement virtuel
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

# 4. Mettre à jour pip
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel

# 5. Installer les dépendances
python -m pip install -r requirements.txt

# 6. Lancer l'application
python start_gpao.py
```

Le script `start_gpao.py` exécute automatiquement :
- `makemigrations` - Création des migrations
- `migrate` - Application des migrations à la base de données
- `seed_demo` - Chargement des données de démonstration
- `runserver` - Démarrage du serveur de développement

---

## 🔐 Accès à l'application

- **URL** : http://127.0.0.1:8000/
- **Utilisateur** : `admin`
- **Mot de passe** : `admin123`

---

## 🏛️ Architecture Technique

- **Framework** : Django 5.2.12
- **Base de données** : SQLite (créée automatiquement)
- **Interface** : Templates Django avec HTML/CSS
- **Langage** : Python 3.13

### Structure du projet
```
gpao_v4_complete/
├── core/              # Application principale (modèles, vues, services)
├── gpao/              # Configuration Django
├── templates/         # Templates HTML
├── manage.py          # Script de gestion Django
├── start_gpao.py      # Script de lancement automatisé
└── requirements.txt   # Dépendances Python
```

---

## 👥 Équipe du Projet

Ce projet a été développé dans le cadre d'un projet collaboratif.

**Contributeurs :**
- [Ikram El Mazini](https://github.com/ELMAZINI-Ikram)
- [Loubna Ech-Chokhmany](https://github.com/Loubna-ECH-CHOKHMANY)

**Rôles :**
- Développement backend
- Modélisation des données
- Implémentation des algorithmes GPAO
- Tests et validation

---

## 📝 Remarques importantes

- La base de données SQLite est créée automatiquement au premier lancement
- L'interface d'administration Django permet de compléter ou corriger les données de démonstration
- Le calcul MRP est temporel et exploite les délais et réceptions programmées
- Cette version constitue une solution pédagogique et opérationnelle, adaptée à un atelier de taille moyenne
- Pour un usage industriel avancé, un APS (Advanced Planning System) serait recommandé

---

## 📄 Licence

Ce projet est destiné à un usage éducatif et opérationnel dans le cadre de la gestion de production.

---

**Version** : 4.0 (Complète)
**Date** : 2026
