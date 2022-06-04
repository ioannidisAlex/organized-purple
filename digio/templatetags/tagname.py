from django import template

register = template.Library()

@register.filter
def get_item(dictionary,k):
    return dictionary.get("pullmeout"+str(k))

@register.filter
def get_element(array, k):
    return array[k]

@register.filter
def get_range(value):
    return range(value)