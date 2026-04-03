from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

# Sample data for products/gallery
GALLERY_ITEMS = [
    {
        'image_path': 'images/gallery12.jpeg',
        'name': 'Kalesi aurat Angry clip',
        'description': 'red yarn crochet clip for hair depicting angry women'
    },
    {
        'image_path': 'images/gallery13.jpeg',
        'name': 'White Flower vine',
        'description': 'flower vine for hair braiding, curtain holder, or as a room decor'
    },
    {
        'image_path': 'images/gallery14.jpeg',
        'name': 'Puffed sunflower',
        'description': 'sunflower clip for women'
    },
    {
        'image_path': 'images/gallery15.jpeg',
        'name': 'White pink daisy',
        'description': 'big flower daisy clip; can be used as brooch'
    },
    {
        'image_path': 'images/gallery16.jpeg',
        'name': 'Purple puffed',
        'description': 'puffed flower clip for women'
    },
    {
        'image_path': 'images/gallery17.jpeg',
        'name': 'Pink puffed',
        'description': 'puffed pink flower clip for women'
    },
    {
        'image_path': 'images/gallery18.jpeg',
        'name': 'Blue puffed',
        'description': 'puffed blue flower clip for women'
    },
    {
        'image_path': 'images/gallery19.jpeg',
        'name': 'Twin octo',
        'description': 'cute octopus keyring happy face'
    },
    {
        'image_path': 'images/gallery20.jpeg',
        'name': 'Happy sad octo',
        'description': 'octopus keyring in pair as per your mood'
    },
    {
        'image_path': 'images/gallery21.jpeg',
        'name': 'White daisy',
        'description': 'daisy keyring in size big for schoolbags, totebags, side bags'
    },
    {
        'image_path': 'images/gallery22.jpeg',
        'name': 'Sunflower',
        'description': 'stuffed sunflower keyring with vibrant yellow color'
    },
    {
        'image_path': 'images/gallery23.jpeg',
        'name': 'Bow Pair',
        'description': 'bow keyring for bags and purses'
    },
    {
        'image_path': 'images/gallery24.jpeg',
        'name': 'Cute chicken',
        'description': 'miniature chicken toy holding a flower can be used as showpiece'
    },
    {
        'image_path': 'images/gallery25.jpeg',
        'name': 'The Queen Rose',
        'description': 'red rose that never fades, can be customized into bouquets'
    },
]

def home(request):
    """Home page view with all sections"""
    context = {
        'motto': 'Loops of love in every stitch',
        'about_intro': 'Welcome to Hastakala by K, where every stitch tells a story of love and creativity. Founded by Kritishma Pradhan, our passion is to create beautiful, handmade crochet items that bring warmth and joy to your life.',
        'about_description': 'Each piece is carefully crafted with attention to detail and made with high-quality yarns to ensure durability and comfort.',
        'products': GALLERY_ITEMS,
        'owner_email': 'pradhankritishma@gmail.com',
    }
    return render(request, 'store/index.html', context)
