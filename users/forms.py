from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        max_length=66,
        widget=forms.EmailInput(attrs={'placeholder': 'Your email'})
    )
    username = forms.CharField(
        required=True,
        max_length=66,
        widget=forms.TextInput(attrs={'placeholder': 'Your username'})
    )
    first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Your first name'})
    )
    last_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Your last name'})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password'})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )
    
    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name', 'last_name', 'password1', 'password2'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
        

class CustomUserLogin(AuthenticationForm):
    username = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'autofocus':True, 'placeholder': 'Your email'})
    )

    password = forms.CharField(
        label='Password',
        widget=forms.TextInput(attrs={'autofocus':True, 'placeholder': 'Your password'})
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid email or password.')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('This account is inactive.')
        return self.cleaned_data