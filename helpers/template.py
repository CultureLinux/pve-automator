import json
from dotenv import dotenv_values

import pathlib
import tomlkit
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

BASE_DIR = pathlib.Path(__file__).parents[1]

env_vars = dotenv_values(BASE_DIR / ".env")
proxmox_email = env_vars.get("PROXMOX_EMAIL")
proxmox_password = env_vars.get("PROXMOX_PASSWORD")
proxmox_ssh_keys = json.loads(env_vars.get("PROXMOX_SSH_KEYS", "[]"))

TEMPLATES_DIR = BASE_DIR / "templates"
DEFAULT_TEMPLATE = "default.toml.j2"

env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=False,
)

def find_template(mac):
    if mac:
        candidate = f"mac/{mac}.toml.j2"
        try:
            env.get_template(candidate)
            return candidate
        except TemplateNotFound:
            pass
    return DEFAULT_TEMPLATE

def build_context(payload, mac):
    return {
        "mac": mac or "unknown",
        "hostname": f"pve-{mac.replace(':','')[:6]}" if mac else "pve-node",
        "timezone": "Europe/Paris",
        "keyboard": "fr",
        "country": "FR",
        "proxmox_email" : proxmox_email,
        "proxmox_password": proxmox_password,
        "proxmox_ssh_keys": proxmox_ssh_keys,
    }

def render_template(template_name, context):
    template = env.get_template(template_name)


    rendered = template.render(context)
    
        
    
    print("----- RENDERED -----")
    print(rendered)
    print("--------------------")

    
    tomlkit.parse(rendered)
    return rendered
