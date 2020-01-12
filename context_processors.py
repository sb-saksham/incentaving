from home.models import Card
from blogs.models import Blog
from random import randint


def return_card():
    """
    :return: a random card object
    """
    cards = Card.objects.all()
    c = cards.count()
    try:
        ind = randint(0, (c-1))
        card_obj = cards[ind]
        return card_obj
    except ValueError:
        return None


def get_posts_list():
    posts_list = Blog.objects.all().order_by("-date_created")
    return posts_list[:3]


def cards_themes(request):

    context = {
        'posts_list': get_posts_list(),
        'card': return_card(),
    }
    return context
