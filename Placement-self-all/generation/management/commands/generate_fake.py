from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from generation.models import Details
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate fake data for testing'

    def add_arguments(self, parser):
        parser.add_argument('--c', type=int, default=3, help='Number of fake profiles to generate')

    def generate_phone_number(self, fake):
        """
        Generate a more genuine phone number with international dialing codes.
        """
        international_dialing_codes = ['+1', '+91', '+44', '+49', '+61', '+81', '+86', '+31', '+64', '+65']
        dialing_code = fake.random_element(elements=international_dialing_codes)
        if dialing_code == '+1':
            phone_number = fake.numerify(text='##########')  # US phone number
        elif dialing_code == '+91':
            phone_number = fake.numerify(text='##########')  # India phone number
        elif dialing_code == '+44':
            phone_number = fake.numerify(text='##########')  # UK phone number
        elif dialing_code == '+49':
            phone_number = fake.numerify(text='###########')  # Germany phone number
        elif dialing_code == '+61':
            phone_number = fake.numerify(text='#########')  # Australia phone number
        elif dialing_code == '+81':
            phone_number = fake.numerify(text='##########')  # Japan phone number
        elif dialing_code == '+86':
            phone_number = fake.numerify(text='############')  # China phone number
        elif dialing_code == '+31':
            phone_number = fake.numerify(text='#########')  # Netherlands phone number
        elif dialing_code == '+64':
            phone_number = fake.numerify(text='########')  # New Zealand phone number
        elif dialing_code == '+65':
            phone_number = fake.numerify(text='########')  # Singapore phone number
        else:
            phone_number = fake.numerify(text='##########')  # Default to 10 digits
        return dialing_code + phone_number

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['c']

        # Define more email domains
        email_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com', 'icloud.com', 'mail.com', 'protonmail.com', 'zoho.com', 'yandex.com']

        # Define more elements for random selection
        company_names = [
            'Microsoft', 'Google', 'Facebook', 'Amazon', 'Apple', 'IBM', 'Intel', 'Oracle', 'Cisco', 'Samsung',
            'General Motors', 'Toyota', 'Volkswagen', 'Ford', 'Honda', 'BMW', 'Mercedes-Benz', 'Tesla', 'Nissan', 'Audi',
            'Coca-Cola', 'PepsiCo', 'Nestle', 'McDonalds', 'Starbucks', 'KFC', 'Walmart', 'Target', 'IKEA', 'LVMH',
            'Nike', 'Adidas', 'Sony', 'Panasonic', 'LG', 'Canon', 'HP', 'Dell', 'Lenovo', 'Netflix', 'Disney',
            'Boeing', 'Airbus', 'SpaceX', 'Lockheed Martin', 'Booz Allen Hamilton', 'Raytheon Technologies', 'Northrop Grumman',
            'Pfizer', 'Johnson & Johnson', 'Novartis', 'GlaxoSmithKline', 'Merck & Co.', 'Abbott Laboratories', 'Bayer'
        ]
        degree_types = ['Bachelor', 'Master', 'PhD', 'Associate', 'Certificate', 'Diploma', 'MBA', 'JD', 'MD', 'DDS']
        fields_of_study = ['Computer Science', 'Engineering', 'Mathematics', 'Physics', 'Biology', 'Psychology', 'Business', 'Chemistry', 'Sociology', 'Economics']
        school_names = [
            'Stanford University', 'Massachusetts Institute of Technology', 'Harvard University', 'California Institute of Technology',
            'University of Oxford', 'University of Cambridge', 'ETH Zurich', 'University of Toronto', 'University of Tokyo', 'University of Melbourne'
        ]
        tech_stacks = [
            'PostgreSQL', 'React', 'Express.js', 'JavaScript', 'MERN', 'Django', 'Spring Boot', 'Angular', 'Vue.js', 'Ruby on Rails',
            'Laravel', 'Flask', 'ASP.NET', 'Node.js', 'TensorFlow', 'Keras', 'PyTorch', 'Scikit-learn', 'Kubernetes', 'Docker'
        ]

        for _ in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name()
            email = fake.email(domain=fake.random_element(elements=email_domains))
            password = 'password'
            user = User.objects.create(username=username,
                                       email=email,
                                       password=password)
            profile = Details.objects.create(user=user,
                                             first_name=first_name,
                                             last_name=last_name,
                                             email=email,
                                             picture=fake.image_url(),
                                             bio=fake.sentence(nb_words=10),
                                             phone_number=self.generate_phone_number(fake),
                                             address=fake.address(),
                                             title=fake.job(),
                                             techstack=fake.random_element(elements=tech_stacks),
                                             company=fake.random_element(elements=company_names),
                                             degree=fake.random_element(elements=degree_types),
                                             field_of_study=fake.random_element(elements=fields_of_study),
                                             school=fake.random_element(elements=school_names))
            
        return 'successfully generated'
