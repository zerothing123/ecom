from django import  template
register=template.Library()

@register.filter(name='get_def')
def get_def(dict,key):
    return dict.get(key)

