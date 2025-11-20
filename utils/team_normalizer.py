import unicodedata
import re

def normalize_name(name: str) -> str:
    """
    Normaliza nome de liga/time para usar em IDs e filenames.
    Ex.: 'Real Madrid CF' -> 'real-madrid'
    """
    if not name:
        return ""
    name = str(name).strip().lower()

    # remove acentos
    name = unicodedata.normalize("NFD", name)
    name = "".join(ch for ch in name if unicodedata.category(ch) != "Mn")

    # remove sufixos comuns de time
    remove_words = ["fc", "cf", "sc", "afc", "u19", "u20", "u21"]
    parts = [p for p in re.split(r"\s+", name) if p not in remove_words]

    name = "-".join(parts)
    name = re.sub(r"[^a-z0-9\-]+", "", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name
