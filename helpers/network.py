import logging

def extract_mac(payload):
    interfaces = payload.get("network_interfaces", [])

    if not interfaces:
        logging.warning("No network_interfaces in payload")
        return None

    for idx, nic in enumerate(interfaces):
        mac = nic.get("mac")
        logging.debug(
            "NIC #%s: raw=%s",
            idx,
            nic
        )
        if mac:
            logging.info("MAC detected: %s", mac.lower())
            return mac.lower()

    logging.warning("No MAC address found in network_interfaces")
    return None
