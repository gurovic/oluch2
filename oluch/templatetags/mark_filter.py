from django import template
from oluch.settings import marks
register = template.Library()

def mark(value): 

    if value != '' and int(value) >= 0:
        return marks[int(value)]
    else:
        return ''
        
register.filter('mark', mark)