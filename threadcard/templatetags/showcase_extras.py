__author__ = 'leif'
from django import template
from threadcard.models import Category

register = template.Library()

@register.inclusion_tag("threadcard/cats.html")
def get_category_list(value):
    return {"cats" : Category.objects.all(),"catid":value}


@register.filter(name='addcss')
def addcss(field,cssclass):
    return field.as_widgt(attrs={'class':cssclass})
