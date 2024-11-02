from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Keep existing models...

class WordRelationship(models.Model):
    RELATIONSHIP_TYPES = [
        ('synonym', 'Synonym'),
        ('antonym', 'Antonym'),
    ]
    
    word1 = models.ForeignKey('WordsBank', on_delete=models.CASCADE, related_name='relationships_as_word1')
    word2 = models.ForeignKey('WordsBank', on_delete=models.CASCADE, related_name='relationships_as_word2')
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_TYPES)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['word1', 'word2', 'relationship_type']
        indexes = [
            models.Index(fields=['word1', 'relationship_type']),
            models.Index(fields=['word2', 'relationship_type']),
        ]
    
    def save(self, *args, **kwargs):
        # Ensure word1.id < word2.id to avoid duplicate relationships
        if self.word1.id > self.word2.id:
            self.word1, self.word2 = self.word2, self.word1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.word1.word} - {self.word2.word} ({self.relationship_type})"

# Add methods to WordsBank model
class WordsBankExtended:
    def get_synonyms(self):
        """Get all synonyms for this word"""
        synonym_relationships = WordRelationship.objects.filter(
            models.Q(word1=self, relationship_type='synonym') |
            models.Q(word2=self, relationship_type='synonym')
        )
        
        synonyms = []
        for rel in synonym_relationships:
            if rel.word1 == self:
                synonyms.append(rel.word2)
            else:
                synonyms.append(rel.word1)
        return synonyms
    
    def get_antonyms(self):
        """Get all antonyms for this word"""
        antonym_relationships = WordRelationship.objects.filter(
            models.Q(word1=self, relationship_type='antonym') |
            models.Q(word2=self, relationship_type='antonym')
        )
        
        antonyms = []
        for rel in antonym_relationships:
            if rel.word1 == self:
                antonyms.append(rel.word2)
            else:
                antonyms.append(rel.word1)
        return antonyms
    
    def add_synonym(self, other_word):
        """Add bidirectional synonym relationship"""
        WordRelationship.objects.get_or_create(
            word1=min(self, other_word, key=lambda w: w.id),
            word2=max(self, other_word, key=lambda w: w.id),
            relationship_type='synonym'
        )
    
    def add_antonym(self, other_word):
        """Add bidirectional antonym relationship"""
        WordRelationship.objects.get_or_create(
            word1=min(self, other_word, key=lambda w: w.id),
            word2=max(self, other_word, key=lambda w: w.id),
            relationship_type='antonym'
        )