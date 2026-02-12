import random

from faker import Faker

faker = Faker()

class MovieDataGenerator:

    @staticmethod
    def movie_payload(**overrides):
        payload =  {
            'name': faker.sentence(nb_words=3),
            'imageUrl': faker.image_url(),
            'price': random.randint(100, 1000),
            'description': faker.text(max_nb_chars=200),
            'location': random.choice(['MSK', 'SPB']),
            'published': random.choice([True, False]),
            'genreId': random.randint(1, 5),
        }

        payload.update(overrides)
        return payload