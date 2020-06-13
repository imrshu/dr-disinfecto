from django.core.management.base import BaseCommand
from product.models import Review


class Command(BaseCommand):
    help = "populate fake reivews for disinfecto in production"

    def handle(self, *args, **kwargs):
        self.stdout.write('Script started')

        Review.objects.create(
            customer_name='Garima Sachdeva',
            review_text='Excellent Sanitization by Disinfecto',
            ratings=5
        )

        Review.objects.create(
            customer_name='Rishabh Verma',
            review_text='PPE Kits quality is really good.',
            ratings=4
        )

        Review.objects.create(
            customer_name='Ajay Kumar',
            review_text='Nice service by Disinfecto.',
            ratings=5
        )

        Review.objects.create(
            customer_name='Neha Malhotra',
            review_text='Good work guys.I have experienced the finest services by you.',
            ratings=5
        )

        Review.objects.create(
            customer_name='Mahesh Singh',
            review_text='Sanitizers contain proper alcohol quantity',
            ratings=4
        )

        Review.objects.create(
            customer_name='Karan Jha',
            review_text='Nice promo offers by disinfecto',
            ratings=5
        )

        Review.objects.create(
            customer_name='Ashok Dinda',
            review_text='Work place sanitization was awesome.',
            ratings=4
        )

        Review.objects.create(
            customer_name='Sudhir Chaudary',
            review_text='Awesome Service',
            ratings=4
        )

        self.stdout.write('Script end')
