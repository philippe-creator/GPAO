# GPAO V4 complète - Atelier électromécanique

Cette version ajoute les briques manquantes du cours :
- PDP / MPS (programme directeur de production) via `MPSItem`
- CBN / MRP temporel par semaines
- stock de sécurité
- point de commande
- EOQ / quantité économique
- classification ABC
- délais (lead time) et lancement décalé
- charge / capacité machine
- graphique des décalages
- OF / OT
- maintenance légère liée à la disponibilité machine

## Lancement Windows PowerShell

```powershell
cd gpao_v4_complete
py -3.13 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python start_gpao.py
```

Le script `start_gpao.py` exécute :
- makemigrations
- migrate
- seed_demo
- runserver

## Accès
- URL : http://127.0.0.1:8000/
- utilisateur : `admin`
- mot de passe : `admin123`

## Remarques
- Base de données : SQLite, créée automatiquement.
- L'admin Django permet de compléter ou corriger les données de démonstration.
- Le calcul MRP est temporel et exploite les délais et réceptions programmées, mais reste une version pédagogique et opérationnelle, pas un APS industriel avancé.
