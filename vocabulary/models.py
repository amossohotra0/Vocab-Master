from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class WordList(models.Model):
    word_list_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['word_list_name']
    
    def __str__(self):
        return self.word_list_name

class WordType(models.Model):
    word_type = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10, blank=True)
    
    class Meta:
        ordering = ['word_type']

    def __str__(self):
        return self.word_type

class DifficultyLevel(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_level_display()

class WordsBank(models.Model):
    word = models.CharField(max_length=100, unique=True)
    word_type = models.ForeignKey(WordType, on_delete=models.CASCADE)
    word_lists = models.ManyToManyField(WordList, blank=True)
    difficulty_level = models.ForeignKey(DifficultyLevel, on_delete=models.SET_NULL, null=True, blank=True)
    meaning_urdu = models.TextField()
    meaning_english = models.TextField()
    example_sentence = models.TextField()
    synonyms = models.TextField(blank=True, help_text="Comma-separated synonyms")
    antonyms = models.TextField(blank=True, help_text="Comma-separated antonyms")
    pronunciation = models.CharField(max_length=200, blank=True)
    etymology = models.TextField(blank=True)
    frequency_rank = models.PositiveIntegerField(null=True, blank=True, help_text="Word frequency ranking")
    is_favorite = models.BooleanField(default=False)
    times_reviewed = models.PositiveIntegerField(default=0)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['word']
        verbose_name_plural = "Words Bank"
        
    def __str__(self):
        return self.word
    
    def get_synonyms_list(self):
        return [s.strip() for s in self.synonyms.split(',') if s.strip()]
    
    def get_antonyms_list(self):
        return [a.strip() for a in self.antonyms.split(',') if a.strip()]
    
    def get_related_synonyms(self):
        """Get all synonym words from WordRelationship model"""
        from django.db.models import Q
        synonym_relationships = WordRelationship.objects.filter(
            Q(word1=self, relationship_type='synonym') |
            Q(word2=self, relationship_type='synonym')
        )
        
        synonyms = []
        for rel in synonym_relationships:
            if rel.word1 == self:
                synonyms.append(rel.word2)
            else:
                synonyms.append(rel.word1)
        return synonyms
    
    def get_related_antonyms(self):
        """Get all antonym words from WordRelationship model"""
        from django.db.models import Q
        antonym_relationships = WordRelationship.objects.filter(
            Q(word1=self, relationship_type='antonym') |
            Q(word2=self, relationship_type='antonym')
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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    profile_picture = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True)
    user_timezone = models.CharField(max_length=50, blank=True)
    subscription_status = models.CharField(max_length=20, default='free', choices=[
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('pro', 'Pro')
    ])
    subscription_expires = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} Profile"

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

class UserProgress(models.Model):
    word = models.ForeignKey(WordsBank, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mastery_level = models.IntegerField(default=0, help_text="0-5 scale")
    times_correct = models.PositiveIntegerField(default=0)
    times_incorrect = models.PositiveIntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['word', 'user']
    
    def __str__(self):
        return f"{self.word.word} - {self.user.email} - Level {self.mastery_level}"