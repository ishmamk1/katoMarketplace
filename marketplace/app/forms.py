from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Item, Conversation, ConversationMessage

class SignUp(UserCreationForm):
    """
        Form for user sign-up.

        Attributes:
            username (CharField): The username chosen by the user.
            email (CharField): The email address of the user.
            password1 (CharField): The user's password.
            password2 (CharField): The confirmation of the user's password.

    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Username',
        'class' : 'w-full py-4 px-6 rounded-xl',
    }))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Email',
        'class': 'w-full py-4 px-6 rounded-xl',
    }))

    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'w-full py-4 px-6 rounded-xl',
    }))

    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'w-full py-4 px-6 rounded-xl',
    }))

class Login(AuthenticationForm):
    """
        Form for user login.

        Attributes:
            username (CharField): The username provided by the user.
            password (CharField): The user's password.

    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Username',
        'class': 'w-full py-4 px-6 rounded-xl',
    }))

    password = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'w-full py-4 px-6 rounded-xl',
    }))

inputClass = 'w-full py-4 px-6 rounded-xl border'

class NewItem(forms.ModelForm):
    """
        Form for creating a new item.

        Attributes:
            category (ModelChoiceField): The category to which the new item belongs.
            name (CharField): The name of the new item.
            description (Textarea): A description of the new item.
            price (CharField): The price of the new item.
            image (FileInput): An image representing the new item.

    """
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image',)

        widgets = {
            'category' : forms.Select(attrs={
                'class': inputClass,
            }),
            'name': forms.TextInput(attrs={
                'class': inputClass,
            }),
            'description': forms.Textarea(attrs={
                'class': inputClass,
            }),
            'price': forms.TextInput(attrs={
                'class': inputClass,
            }),
            'image': forms.FileInput(attrs={
                'class': inputClass,
            }),

        }

class EditItem(forms.ModelForm):
    """
        Form for editing an existing item.

        Attributes:
            name (CharField): The updated name of the item.
            description (Textarea): The updated description of the item.
            price (CharField): The updated price of the item.
            image (FileInput): The updated image representing the item.
            isSold (CheckboxInput): Indicates whether the item is sold or not.

    """
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image','isSold')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': inputClass,
            }),
            'description': forms.Textarea(attrs={
                'class': inputClass,
            }),
            'price': forms.TextInput(attrs={
                'class': inputClass,
            }),
            'image': forms.FileInput(attrs={
                'class': inputClass,
            }),

        }

class MessageForm(forms.ModelForm):
    """
    Form for sending a message in a conversation.

    Attributes:
        content (Textarea): The content of the message.

    """
    class Meta:
        model = ConversationMessage
        fields = ('content', )
        widgets = {
            'content' : forms.Textarea(attrs={
                'class' : 'w-full py-4 px-6 rounded-xl border'
            })
        }