from django import template
import re


register = template.Library()

WORDS = ['нежелательное', 'слово', 'еще_одно', 'редиска', 'экспедиции']

@register.filter()
def censor(value):
    if not isinstance(value, str):
        return value
    
    for w in WORDS:
        pattern = re.compile(r'\b' + re.escape(w) + r'\b', re.IGNORECASE)
        value = pattern.sub(w[0] + '*' * (len(w) - 1), value)
    return value