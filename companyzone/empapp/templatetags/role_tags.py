from django import template

# You must create an instance of the Library class first
register = template.Library()

# Then use that specific instance as your decorator
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()