from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, BaseUserAdmin
from django import forms

# Register your models here.
from .models import Driver, Vehicle, CoDriver, Product, Product

admin.site.register(Driver)
admin.site.register(CoDriver)
admin.site.register(Vehicle)
admin.site.register(Product)





class CustomUserSignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('staff_no', 'first_name', 'second_name', 'department', 'role')

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserSignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('staff_no', 'first_name', 'second_name', 'department', 'role', 'is_active', 'is_staff')

class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserSignUpForm
    add_form = CustomUserSignUpForm

    list_display = ('staff_no', 'first_name', 'second_name', 'department', 'role', 'is_staff')
    list_filter = ('is_staff', 'role')
    fieldsets = (
        (None, {'fields': ('staff_no', 'password')}),
        ('Personal info', {'fields': ('first_name', 'second_name', 'department', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('staff_no', 'first_name', 'second_name', 'department', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('staff_no', 'first_name', 'second_name')
    ordering = ('staff_no',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)
