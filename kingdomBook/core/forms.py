from django import forms
from core.models import BookReview


class BookReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review"}))

    class Meta:
        model = BookReview
        fields = ['review', 'rating']
        
        