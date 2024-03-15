from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
#strange thing to investigate:
# I cannot init in ChangepasswordForm, it returns strange error



class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),required=False)
    address1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address1'}),required=False)
    address2 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address2'}),required=False)
    city = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),required=False)
    state = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),required=False)
    zipcode = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}),required=False)
    country = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}),required=False)

    class Meta:
        model = Profile
        fields = ('phone','address1','address2','city','state','zipcode','country')




class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class']='form-control'
        self.fields['new_password1'].widget.attrs['placeholder']='Password'
        self.fields['new_password1'].label=''
        self.fields['new_password1'].help_text='<ul class="form-text text-muted small"><li> Password cannot be similar to your other personal data </li> <li> Password cannot be entirely numeric </li><li> Password must contain at least 8 characters </li></ul>'
        self.fields['new_password2'].widget.attrs['class']='form-control'
        self.fields['new_password2'].widget.attrs['placeholder']='Confirm Password'
        self.fields['new_password2'].label=''
        self.fields['new_password2'].help_text='<span class="form-text text-muted"><small>To confirm enter the same password as above </small></span>'

    
   


class SignUpForm(UserCreationForm):
    email= forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),required=False)
    first_name= forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),required=False)
    last_name= forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),required=False)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
        
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder']='Username'
        self.fields['username'].label=''
        self.fields['username'].help_text='<span class="form-text text-muted"><small>Required. <=100 characters, Letters, digits and @/./+-/_ only </small></span>'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['placeholder']='Password'
        self.fields['password1'].label=''
        self.fields['password1'].help_text='<ul class="form-text text-muted small"><li> Password cannot be similar to your other personal data </li> <li> Password cannot be entirely numeric </li><li> Password must contain at least 8 characters </li></ul>'
        self.fields['password2'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['placeholder']='Confirm Password'
        self.fields['password2'].label=''
        self.fields['password2'].help_text='<span class="form-text text-muted"><small>To confirm enter the same password as above </small></span>'



class UpdateUserForm(UserChangeForm):
    #Hide password field
    password = None
    email= forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    first_name= forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name= forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')
        
    
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder']='Username'
        self.fields['username'].label=''
        self.fields['username'].help_text='<span class="form-text text-muted"><small>Required. <=100 characters, Letters, digits and @/./+-/_ only </small></span>'
      



class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")
    last_name = forms.CharField(max_length=100, required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")
    email = forms.CharField(max_length=100, required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
    phone = forms.CharField(max_length=100, required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
    address =forms.CharField(max_length=100, required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")
    city = forms.CharField(max_length=100, required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"City", "class":"form-control"}), label="")
    state = forms.CharField(max_length=100, required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"State", "class":"form-control"}), label="")
    zipcode = forms.CharField(max_length=100, required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Zipcode", "class":"form-control"}), label="")