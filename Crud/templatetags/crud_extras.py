from django import template
import json

register = template.Library()

@register.filter
def pretty_json(value):
    """Formatea un valor JSON de manera legible."""
    try:
        if isinstance(value, dict):
            return json.dumps(value, indent=2, ensure_ascii=False)
        elif isinstance(value, str):
            # Intentar parsear como JSON
            parsed = json.loads(value)
            return json.dumps(parsed, indent=2, ensure_ascii=False)
        else:
            return str(value)
    except:
        return str(value)

@register.filter
def get_item(dictionary, key):
    """Obtiene un elemento de un diccionario por clave."""
    return dictionary.get(key) 