import re


def is_valid_ip(ip):
    """Validates IP addresses.
    """
    resp = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)
    return resp is not None
