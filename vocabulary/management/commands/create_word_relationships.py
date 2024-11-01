from django.core.management.base import BaseCommand
from vocabulary.models import WordsBank, WordRelationship

class Command(BaseCommand):
    help = 'Create word relationships from existing synonym/antonym text fields'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would be created without actually creating')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No data will be created'))
        
        created_synonyms = 0
        created_antonyms = 0
        skipped = 0
        
        words = WordsBank.objects.all()
        total_words = words.count()
        
        self.stdout.write(f'Processing {total_words} words...')
        
        for i, word in enumerate(words, 1):
            if i % 100 == 0:
                self.stdout.write(f'Processed {i}/{total_words} words...')
            
            # Process synonyms
            if word.synonyms:
                synonym_list = [s.strip().lower() for s in word.synonyms.split(',') if s.strip()]
                for synonym_text in synonym_list:
                    try:
                        synonym_word = WordsBank.objects.get(word__iexact=synonym_text)
                        if not dry_run:
                            relationship, created = WordRelationship.objects.get_or_create(
                                word1=min(word, synonym_word, key=lambda w: w.id),
                                word2=max(word, synonym_word, key=lambda w: w.id),
                                relationship_type='synonym'
                            )
                            if created:
                                created_synonyms += 1
                        else:
                            created_synonyms += 1
                            self.stdout.write(f'Would create synonym: {word.word} ↔ {synonym_word.word}')
                    except WordsBank.DoesNotExist:
                        skipped += 1
                        if dry_run:
                            self.stdout.write(f'Synonym not found: "{synonym_text}" for word "{word.word}"')
            
            # Process antonyms
            if word.antonyms:
                antonym_list = [a.strip().lower() for a in word.antonyms.split(',') if a.strip()]
                for antonym_text in antonym_list:
                    try:
                        antonym_word = WordsBank.objects.get(word__iexact=antonym_text)
                        if not dry_run:
                            relationship, created = WordRelationship.objects.get_or_create(
                                word1=min(word, antonym_word, key=lambda w: w.id),
                                word2=max(word, antonym_word, key=lambda w: w.id),
                                relationship_type='antonym'
                            )
                            if created:
                                created_antonyms += 1
                        else:
                            created_antonyms += 1
                            self.stdout.write(f'Would create antonym: {word.word} ↔ {antonym_word.word}')
                    except WordsBank.DoesNotExist:
                        skipped += 1
                        if dry_run:
                            self.stdout.write(f'Antonym not found: "{antonym_text}" for word "{word.word}"')
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'SUMMARY:'))
        self.stdout.write(f'Synonym relationships created: {created_synonyms}')
        self.stdout.write(f'Antonym relationships created: {created_antonyms}')
        self.stdout.write(f'Words not found (skipped): {skipped}')
        self.stdout.write(f'Total relationships: {created_synonyms + created_antonyms}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\nThis was a DRY RUN. Run without --dry-run to actually create relationships.'))
        else:
            self.stdout.write(self.style.SUCCESS('\nWord relationships created successfully!'))