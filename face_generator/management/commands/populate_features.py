from django.core.management.base import BaseCommand
from face_generator.models import FaceFeatureCategory, FaceFeature

class Command(BaseCommand):
    help = 'Populate database with comprehensive Indian facial features'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating facial features database...')

        # Define comprehensive feature set optimized for Indian faces
        features_data = {
            'Face Shape': {
                'order': 1,
                'description': 'Overall facial structure',
                'features': [
                    ('Oval', 'smooth oval-shaped face with balanced proportions'),
                    ('Round', 'round face with full cheeks and soft jawline'),
                    ('Square', 'strong square jawline with broad forehead'),
                    ('Rectangular', 'long rectangular face with high forehead'),
                    ('Diamond', 'diamond-shaped face with prominent cheekbones'),
                    ('Heart-shaped', 'heart-shaped face with pointed chin'),
                    ('Triangular', 'triangular face with narrow forehead'),
                ]
            },
            'Complexion': {
                'order': 2,
                'description': 'Skin tone',
                'features': [
                    ('Very Fair', 'very fair Indian skin tone, wheatish complexion'),
                    ('Fair', 'fair skin with warm undertones'),
                    ('Medium', 'medium brown skin tone, typical Indian complexion'),
                    ('Dusky', 'dusky brown skin with golden undertones'),
                    ('Dark', 'dark brown skin tone'),
                    ('Very Dark', 'very dark complexion with deep brown tones'),
                ]
            },
            'Forehead': {
                'order': 3,
                'description': 'Forehead characteristics',
                'features': [
                    ('Broad & High', 'broad high forehead, prominent'),
                    ('Narrow', 'narrow forehead'),
                    ('Medium', 'average forehead size'),
                    ('Receding', 'receding hairline, high forehead'),
                    ('Lined', 'forehead with prominent horizontal wrinkles'),
                ]
            },
            'Eyes': {
                'order': 4,
                'description': 'Eye shape and characteristics',
                'features': [
                    ('Large Almond', 'large almond-shaped eyes, expressive'),
                    ('Small Round', 'small round eyes'),
                    ('Deep-set', 'deep-set eyes with prominent brow ridge'),
                    ('Hooded', 'hooded eyelids, partially covered'),
                    ('Wide-set', 'eyes set far apart'),
                    ('Close-set', 'eyes set close together'),
                    ('Droopy', 'droopy eyes with downturned outer corners'),
                    ('Squinting', 'narrow squinting eyes'),
                ]
            },
            'Eyebrows': {
                'order': 5,
                'description': 'Eyebrow shape and thickness',
                'features': [
                    ('Thick & Straight', 'thick straight eyebrows, bushy'),
                    ('Thin & Arched', 'thin arched eyebrows'),
                    ('Unibrow', 'connected eyebrows meeting in center'),
                    ('Sparse', 'sparse thin eyebrows'),
                    ('Bushy & Curved', 'thick bushy curved eyebrows'),
                    ('Angular', 'sharp angular eyebrows'),
                ]
            },
            'Nose': {
                'order': 6,
                'description': 'Nose shape and size',
                'features': [
                    ('Broad & Flat', 'broad flat nose with wide nostrils'),
                    ('Long & Narrow', 'long narrow nose bridge'),
                    ('Hooked', 'hooked aquiline nose with prominent bridge'),
                    ('Bulbous', 'bulbous rounded nose tip'),
                    ('Thin & Pointed', 'thin pointed nose'),
                    ('Crooked', 'crooked or deviated nose'),
                    ('Flared Nostrils', 'wide flared nostrils'),
                    ('Button', 'small button nose, slightly upturned'),
                ]
            },
            'Cheekbones': {
                'order': 7,
                'description': 'Cheekbone prominence',
                'features': [
                    ('High & Prominent', 'high prominent cheekbones'),
                    ('Flat', 'flat cheeks without prominent bones'),
                    ('Full & Round', 'full round cheeks'),
                    ('Hollow', 'hollow sunken cheeks'),
                    ('Average', 'average cheekbone structure'),
                ]
            },
            'Mouth & Lips': {
                'order': 8,
                'description': 'Mouth shape and lip characteristics',
                'features': [
                    ('Full Lips', 'full thick lips, both upper and lower'),
                    ('Thin Lips', 'thin lips'),
                    ('Wide Mouth', 'wide mouth with stretched corners'),
                    ('Small Mouth', 'small narrow mouth'),
                    ('Uneven Lips', 'asymmetrical lips, upper thinner than lower'),
                    ('Downturned', 'downturned mouth corners, frowning'),
                    ('Prominent Upper Lip', 'thick prominent upper lip'),
                ]
            },
            'Jaw & Chin': {
                'order': 9,
                'description': 'Jawline and chin structure',
                'features': [
                    ('Strong Square Jaw', 'strong square masculine jawline'),
                    ('Weak Chin', 'receding weak chin'),
                    ('Prominent Chin', 'prominent protruding chin'),
                    ('Pointed Chin', 'sharp pointed chin'),
                    ('Double Chin', 'double chin with excess fat'),
                    ('Cleft Chin', 'cleft chin with vertical indentation'),
                    ('Round Jaw', 'soft round jawline'),
                ]
            },
            'Facial Hair': {
                'order': 10,
                'description': 'Facial hair patterns',
                'features': [
                    ('Clean Shaven', 'clean shaven, no facial hair'),
                    ('Full Beard', 'thick full beard covering jaw and chin'),
                    ('Stubble', 'short stubble, 2-3 day growth'),
                    ('Goatee', 'goatee beard on chin only'),
                    ('Mustache Only', 'thick mustache without beard'),
                    ('Handlebar Mustache', 'curled handlebar mustache'),
                    ('Patchy Beard', 'sparse patchy facial hair growth'),
                    ('Sideburns', 'long sideburns extending down'),
                ]
            },
            'Hair': {
                'order': 11,
                'description': 'Hairstyle and hair characteristics',
                'features': [
                    ('Short & Straight', 'short straight black hair, crew cut'),
                    ('Medium Wavy', 'medium length wavy hair'),
                    ('Receding Hairline', 'receding hairline, balding at temples'),
                    ('Bald', 'completely bald head'),
                    ('Partially Bald', 'bald on top with hair on sides'),
                    ('Long Hair', 'long hair past shoulders'),
                    ('Curly', 'thick curly hair'),
                    ('Slicked Back', 'hair combed and slicked back'),
                    ('Messy', 'unkempt messy hair'),
                ]
            },
            'Distinctive Marks': {
                'order': 12,
                'description': 'Scars, marks, and other features',
                'features': [
                    ('No Marks', 'no visible distinctive marks'),
                    ('Forehead Scar', 'visible scar on forehead'),
                    ('Mole on Cheek', 'prominent mole on cheek'),
                    ('Pockmarks', 'acne scars and pockmarks on face'),
                    ('Facial Scar', 'noticeable scar across face'),
                    ('Birthmark', 'visible birthmark on face'),
                    ('Missing Tooth', 'visible gap from missing front tooth'),
                    ('Crooked Nose', 'nose appears broken or crooked'),
                ]
            },
            'Age Features': {
                'order': 13,
                'description': 'Age-related characteristics',
                'features': [
                    ('Young 20s', 'youthful appearance, early 20s, smooth skin'),
                    ('Late 20s-30s', 'mature face, late 20s to 30s'),
                    ('40s', 'middle-aged, some wrinkles, 40s'),
                    ('50s+', 'aged appearance, deep wrinkles, 50s or older'),
                    ('Wrinkled Skin', 'heavily wrinkled and weathered skin'),
                    ('Eye Bags', 'prominent bags under eyes'),
                ]
            },
        }

        # Clear existing data
        FaceFeature.objects.all().delete()
        FaceFeatureCategory.objects.all().delete()

        # Populate database
        for category_name, category_data in features_data.items():
            category = FaceFeatureCategory.objects.create(
                name=category_name,
                order=category_data['order'],
                description=category_data['description']
            )

            for idx, (feature_name, prompt_text) in enumerate(category_data['features']):
                FaceFeature.objects.create(
                    category=category,
                    name=feature_name,
                    description=f'{category_name}: {feature_name}',
                    prompt_text=prompt_text,
                    order=idx
                )

            self.stdout.write(
                self.style.SUCCESS(f'Created category: {category_name} with {len(category_data["features"])} features')
            )

        total_features = FaceFeature.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully populated {total_features} facial features across {len(features_data)} categories')
        )
