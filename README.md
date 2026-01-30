# PVE-AUTOMATOR

Petit serveur HTTP en Python basé sur **aiohttp** sur le port 8000 permettant de retourner
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

### Modification de l'iso vers le service avec un certificat valide

```bash
proxmox-auto-install-assistant prepare-iso \
    proxmox-ve_9.1-1.iso \
    --output proxmox-ve-auto_9.1-1.iso \
    --fetch-from http \
    --url "https://pve-automator.local.clinux.fr/answer"
```

### Modification de l'iso vers le service avec un certificat auto signé

```bash
proxmox-auto-install-assistant prepare-iso \
    proxmox-ve_9.1-1.iso \
    --output proxmox-ve-auto-self_9.1-1.iso \
    --fetch-from http \
    --url "https://pve-automator.local.clinux.fr:8000/answer" \
    --cert-fingerprint "BE:40:80:2F:42:6E:AC:A7:97:DF:8B:56:40:15:17:39:42:02:E4:54:06:CD:C0:CA:6D:FE:96:08:C5:93:12:E7"
```


### Création d'une clé bootable avec l'iso modifiée (💥 attention à choisir le bon disque à effacer)

```bash
lsblk
# dd if=proxmox-ve-auto_9.1-1.iso of=/dev/sdd bs=4M status=progress oflag=sync
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

### 4. Edition des templates

* `templates/default.toml.j2`
* `templates/mac/aa:bb:cc:dd:ee:ff.toml.j2`

### 5. Démarrage du serveur

❗❗❗ Attention un proxy frontal avec certificat valide est nécessaire

```bash
./app.py
```


