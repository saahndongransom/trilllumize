from django import forms
from .models import Comment
from ckeditor.widgets import CKEditorWidget
import re



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']



class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200, required=False)
    message = forms.CharField(widget=forms.Textarea)



#class NewsletterForm(forms.Form):
    
   
 #   receivers = forms.CharField()
  #  name = forms.CharField(max_length=100)
   # email = forms.EmailField()
    #message = forms.CharField( label="Email content")


    #class Meta:
     #   fields = ('content', )
      #  from django import forms
    




class NewsletterForm(forms.Form):
    receivers = forms.CharField()
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)  # Use default textarea widget


class SubscriptionPurchaseForm(forms.Form):
    credit_amount = forms.DecimalField(max_digits=10, decimal_places=2)

# forms.py

from django import forms

class OrderForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16)
    expiration_date = forms.CharField(label='Expiration Date', max_length=5)
    cvv = forms.CharField(label='CVV', max_length=3)

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not card_number.isdigit() or len(card_number) != 16:
            raise forms.ValidationError('Invalid card number. Please enter a 16-digit number.')
        return card_number

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        if not re.match(r'^\d{2}/\d{2}$', expiration_date):
            raise forms.ValidationError('Invalid expiration date. Please use the format MM/YY.')
        return expiration_date

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if not cvv.isdigit() or len(cvv) != 3:
            raise forms.ValidationError('Invalid CVV. Please enter a 3-digit number.')
        return cvv






