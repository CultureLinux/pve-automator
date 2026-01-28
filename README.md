# PVE-AUTOMATOR

Petit serveur HTTP en Python basé sur **aiohttp** permettant de retourner
un fichier TOML en fonction des adresses MAC envoyées par un client.

## 🧰 Préparation de l'iso proxmox
### Installation de l'assistant

```bash
apt install proxmox-auto-install-assistant
```

### Téléchargement de l'iso 

```bash
wget http://download.proxmox.com/iso/proxmox-ve_9.1-1.iso
```

### Modification de l'iso

```bash
proxmox-auto-install-assistant prepare-iso \
    proxmox-ve_9.1-1.iso \
    --output proxmox-ve-auto_9.1-1.iso \
    --fetch-from http \
    --url "https://pve-automator.local.clinux.fr/answer"
```

### Création d'une clé bootable avec l'iso modifiée (💥 attention à choisir le bon disque à effacer)

```bash
lsblk
# dd if=/root/proxmox-ve-auto_9.1-1.iso of=/dev/sdd bs=4M status=progress oflag=sync
```

### 

## 📋 Prérequis api

- Python >= 3.10
- pip
- virtualenv

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

