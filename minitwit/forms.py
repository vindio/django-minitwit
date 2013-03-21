from django.forms import EmailField  # , ModelForm
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
# from models import Message, Follower


#class MessageForm(ModelForm):
#    class Meta:
#        model = Message
#
#    exclude = ('author', 'pub_date')
#
#class FollowerForm(ModelForm):
#    class Meta:
#        model = Follower

class UserCreationForm(auth_forms.UserCreationForm):
    email = EmailField(label='Email',
                       help_text='Valid email address',
                       error_messages={'invalid':
                       'You have to enter a valid email address'})

    class Meta:
        model = User
        fields = ("username", "email")
