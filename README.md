# PVE-AUTOMATOR

Petit serveur HTTP/HTTPS en Python basé sur **aiohttp** permettant de retourner un fichier **TOML** en fonction des adresses **MAC** envoyées par un client (Proxmox Auto Install).

Le service peut fonctionner :

* **derrière un proxy HTTPS (NGINX)** → `PROXY=true`
* **en HTTPS natif** avec certificats TLS → `PROXY=false`

---

## 🧰 Préparation de l’ISO Proxmox

### Installation de l’assistant

```bash
apt install proxmox-auto-install-assistant
```

### Téléchargement de l’ISO

```bash
wget http://download.proxmox.com/iso/proxmox-ve_9.1-1.iso
```

---

### ISO pointant vers un service HTTPS avec certificat valide (proxy)

```bash
proxmox-auto-install-assistant prepare-iso \
    proxmox-ve_9.1-1.iso \
    --output proxmox-ve-auto_9.1-1.iso \
    --fetch-from http \
    --url "https://pve-automator.local.clinux.fr/answer"
```

---

### ISO pointant vers un service HTTPS auto-signé (SHA-256)

```bash
proxmox-auto-install-assistant prepare-iso \
    proxmox-ve_9.1-1.iso \
    --output proxmox-ve-auto-self_9.1-1.iso \
    --fetch-from http \
    --url "https://pve-automator.local.clinux.fr:8000/answer" \
    --cert-fingerprint "BE:40:80:2F:42:6E:AC:A7:97:DF:8B:56:40:15:17:39:42:02:E4:54:06:CD:C0:CA:6D:FE:96:08:C5:93:12:E7"
```

---

### Création d’une clé bootable (⚠️ disque effacé sans sommation)

```bash
lsblk
# dd if=proxmox-ve-auto_9.1-1.iso of=/dev/sdd bs=4M status=progress oflag=sync
```

---

## 📋 Prérequis API

* Python ≥ 3.10
* pip
* virtualenv
* NGINX (si mode proxy)

---

## 🧪 Création de l’environnement virtuel

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📄 Templates TOML

* `templates/default.toml.j2`
* `templates/mac/aa:bb:cc:dd:ee:ff.toml.j2`

---

## ⚙️ Configuration (.env)

### Mode proxy (recommandé)

```env
LISTENER_PORT=8000
PROXY=true
```

➡️ Le service écoute en **HTTP**, le TLS est géré par NGINX.

---

### Mode HTTPS natif (sans proxy)

```env
LISTENER_PORT=8000
PROXY=false
TLS_CERTIFICATE=_wildcard.local.clinux.fr.pem
TLS_KEY=_wildcard.local.clinux.fr-key.pem
```

➡️ Les certificats sont **obligatoires**, sinon le service refuse de démarrer.

---

## 🌐 Configuration NGINX minimale (PROXY=true)

```nginx
server {
    listen 443 ssl;
    server_name pve-automator.local.clinux.fr;

    ssl_certificate     /etc/letsencrypt/live/pve-automator.local.clinux.fr/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/pve-automator.local.clinux.fr/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

Redémarrage NGINX :

```bash
nginx -t && systemctl reload nginx
```

---

## 🚀 Démarrage du service

```bash
python app.py
```

* `PROXY=true`  → accès via `https://pve-automator.local.clinux.fr`
* `PROXY=false` → accès via `https://pve-automator.local.clinux.fr:8000`

---

## 🧠 Notes importantes

* Le HTTPS natif **ne recharge pas les certificats automatiquement**
* Le proxy NGINX est **fortement recommandé en production**
* Le mode natif est idéal pour lab / tests / environnements isolés
