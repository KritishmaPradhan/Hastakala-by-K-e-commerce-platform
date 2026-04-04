from django.core.management.base import BaseCommand
from hasta_app.models import Product


class Command(BaseCommand):
    help = 'Populate initial products/gallery items into the database'

    # Data from the original GALLERY_ITEMS and carousel items
    INITIAL_PRODUCTS = [
        # Carousel items (gallery4-12)
        {
            'name': 'Fruit Collection',
            'image_path': 'images/gallery4.jpeg',
            'description': 'colorful fruit collection crochet pieces',
            'category': 'flower',
            'price': 349.99,
            'color': 'Multicolor',
            'material': 'Yarn',
            'stock_quantity': 6,
            'is_featured': True,
        },
        {
            'name': 'Puffed flower',
            'image_path': 'images/gallery5.jpeg',
            'description': 'beautiful puffed flower design',
            'category': 'clip',
            'price': 329.99,
            'color': 'Pink',
            'material': 'Yarn',
            'stock_quantity': 5,
            'is_featured': True,
        },
        {
            'name': 'Flower Vine',
            'image_path': 'images/gallery6.jpeg',
            'description': 'elegant flower vine for various uses',
            'category': 'flower',
            'price': 399.99,
            'color': 'Green, White',
            'material': 'Yarn',
            'stock_quantity': 4,
            'is_featured': True,
        },
        {
            'name': 'Red flower Brooch',
            'image_path': 'images/gallery7.jpeg',
            'description': 'stunning red flower brooch',
            'category': 'clip',
            'price': 279.99,
            'color': 'Red',
            'material': 'Yarn',
            'stock_quantity': 7,
            'is_featured': True,
        },
        {
            'name': 'White daisy keyring',
            'image_path': 'images/gallery8.jpeg',
            'description': 'delicate white daisy keyring',
            'category': 'keyring',
            'price': 219.99,
            'color': 'White',
            'material': 'Yarn',
            'stock_quantity': 9,
            'is_featured': True,
        },
        {
            'name': 'Blue Flower Keyring',
            'image_path': 'images/gallery9.jpeg',
            'description': 'vibrant blue flower keyring',
            'category': 'keyring',
            'price': 219.99,
            'color': 'Blue',
            'material': 'Yarn',
            'stock_quantity': 8,
            'is_featured': True,
        },
        {
            'name': 'Lavender Keyring',
            'image_path': 'images/gallery10.jpeg',
            'description': 'soothing lavender colored keyring',
            'category': 'keyring',
            'price': 219.99,
            'color': 'Lavender',
            'material': 'Yarn',
            'stock_quantity': 7,
            'is_featured': True,
        },
        {
            'name': 'Rose Coaster',
            'image_path': 'images/gallery11.jpeg',
            'description': 'decorative rose coaster for home',
            'category': 'other',
            'price': 179.99,
            'color': 'Red, Pink',
            'material': 'Yarn',
            'stock_quantity': 10,
            'is_featured': True,
        },
        # Original product items (gallery12-25)
        {
            'name': 'Kalesi aurat Angry clip',
            'image_path': 'images/gallery12.jpeg',
            'description': 'red yarn crochet clip for hair depicting angry women',
            'category': 'clip',
            'price': 299.99,
            'color': 'Red',
            'material': 'Yarn',
            'stock_quantity': 5,
        },
        {
            'name': 'White Flower vine',
            'image_path': 'images/gallery13.jpeg',
            'description': 'flower vine for hair braiding, curtain holder, or as a room decor',
            'category': 'flower',
            'price': 399.99,
            'color': 'White',
            'material': 'Yarn',
            'stock_quantity': 3,
        },
        {
            'name': 'Puffed sunflower',
            'image_path': 'images/gallery14.jpeg',
            'description': 'sunflower clip for women',
            'category': 'clip',
            'price': 349.99,
            'color': 'Yellow',
            'material': 'Yarn',
            'stock_quantity': 4,
        },
        {
            'name': 'White pink daisy',
            'image_path': 'images/gallery15.jpeg',
            'description': 'big flower daisy clip; can be used as brooch',
            'category': 'clip',
            'price': 449.99,
            'color': 'White, Pink',
            'material': 'Yarn',
            'stock_quantity': 6,
        },
        {
            'name': 'Purple puffed',
            'image_path': 'images/gallery16.jpeg',
            'description': 'puffed flower clip for women',
            'category': 'clip',
            'price': 329.99,
            'color': 'Purple',
            'material': 'Yarn',
            'stock_quantity': 5,
        },
        {
            'name': 'Pink puffed',
            'image_path': 'images/gallery17.jpeg',
            'description': 'puffed pink flower clip for women',
            'category': 'clip',
            'price': 329.99,
            'color': 'Pink',
            'material': 'Yarn',
            'stock_quantity': 5,
        },
        {
            'name': 'Blue puffed',
            'image_path': 'images/gallery18.jpeg',
            'description': 'puffed blue flower clip for women',
            'category': 'clip',
            'price': 329.99,
            'color': 'Blue',
            'material': 'Yarn',
            'stock_quantity': 5,
        },
        {
            'name': 'Twin octo',
            'image_path': 'images/gallery19.jpeg',
            'description': 'cute octopus keyring happy face',
            'category': 'keyring',
            'price': 199.99,
            'color': 'Multicolor',
            'material': 'Yarn',
            'stock_quantity': 8,
        },
        {
            'name': 'Happy sad octo',
            'image_path': 'images/gallery20.jpeg',
            'description': 'octopus keyring in pair as per your mood',
            'category': 'keyring',
            'price': 249.99,
            'color': 'Multicolor',
            'material': 'Yarn',
            'stock_quantity': 7,
        },
        {
            'name': 'White daisy',
            'image_path': 'images/gallery21.jpeg',
            'description': 'daisy keyring in size big for schoolbags, totebags, side bags',
            'category': 'keyring',
            'price': 229.99,
            'color': 'White',
            'material': 'Yarn',
            'stock_quantity': 10,
        },
        {
            'name': 'Sunflower',
            'image_path': 'images/gallery22.jpeg',
            'description': 'stuffed sunflower keyring with vibrant yellow color',
            'category': 'keyring',
            'price': 239.99,
            'color': 'Yellow',
            'material': 'Yarn',
            'stock_quantity': 9,
        },
        {
            'name': 'Bow Pair',
            'image_path': 'images/gallery23.jpeg',
            'description': 'bow keyring for bags and purses',
            'category': 'keyring',
            'price': 219.99,
            'color': 'Multicolor',
            'material': 'Yarn',
            'stock_quantity': 8,
        },
        {
            'name': 'Cute chicken',
            'image_path': 'images/gallery24.jpeg',
            'description': 'miniature chicken toy holding a flower can be used as showpiece',
            'category': 'toy',
            'price': 279.99,
            'color': 'Yellow, Brown',
            'material': 'Yarn',
            'stock_quantity': 4,
        },
        {
            'name': 'The Queen Rose',
            'image_path': 'images/gallery25.jpeg',
            'description': 'red rose that never fades, can be customized into bouquets',
            'category': 'flower',
            'price': 599.99,
            'color': 'Red',
            'material': 'Yarn',
            'stock_quantity': 2,
            'customizable': True,
        },
    ]

    def handle(self, *args, **options):
        """Populate products from initial data"""
        created_count = 0
        updated_count = 0
        
        for product_data in self.INITIAL_PRODUCTS:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {product.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'∼ Already exists: {product.name}')
                )

        total = created_count + updated_count
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Complete! Created: {created_count}, Already existed: {updated_count}, Total: {total}')
        )
