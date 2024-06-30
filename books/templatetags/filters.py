from django import template
from users.models import Favorite
register = template.Library()


@register.filter
def remove_spaces(value):
    return value.replace(' ', '-')


@register.filter(name='is_favorite')
def is_favorite(user, item):
    return Favorite.objects.filter(user=user, item=item).exists()


@register.filter
def del_comma(value):
    if value > 999:
        return str(value // 1000) + ' ' + str(value)[len(str(value // 1000)):]
    return value


@register.filter(name='app_name')
def app_name(model):
    return model._meta.app_label


@register.filter(name='model_name')
def model_name(model):
    return model._meta.model_name
