from django import template

register = template.Library()

@register.filter
def filter_rating(ratings, rating_value):
    """
    Filter ratings by rating value and return the count
    """
    return len([r for r in ratings if r.rating == int(rating_value)]) 