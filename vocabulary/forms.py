from django import forms
from .models import WordsBank, WordType, DifficultyLevel, WordList

class WordForm(forms.ModelForm):
    class Meta:
        model = WordsBank
        fields = ['word', 'word_type', 'difficulty_level', 'meaning_urdu', 'meaning_english', 
                 'example_sentence', 'synonyms', 'antonyms', 'pronunciation', 'word_lists']
        widgets = {
            'word': forms.TextInput(attrs={'class': 'form-control'}),
            'meaning_urdu': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'meaning_english': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'example_sentence': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'synonyms': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated'}),
            'antonyms': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated'}),
            'pronunciation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '/pronunciation/'}),
            'word_type': forms.Select(attrs={'class': 'form-control'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
            'word_lists': forms.CheckboxSelectMultiple(),
        }