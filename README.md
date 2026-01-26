# PVE-AUTOMATOR

Petit serveur HTTP en Python basé sur **aiohttp** permettant de retourner
un fichier TOML en fonction des adresses MAC envoyées par un client.

## 📋 Prérequis

- Python >= 3.10
- pip
- virtualenv (recommandé)

## 🧪 Création de l’environnement virtuel (venv)

### 1. Créer le venv
```bash
python3.11 -m venv venv
```

### 2. Activer le venv
```bash
source venv/bin/activate
```

### 3. Installation des dépendances
```bash
pip install -r requirements.txt
```