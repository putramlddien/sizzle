from django import template

register = template.Library()

@register.filter(name='concat_slug')
def concat_slug(value, arg):
    slug = arg.lower().replace(' ', '-')
    return f"{value}-{slug}"