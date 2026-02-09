from django.contrib import admin
from .models import CustomUser, Event
from django.contrib.auth.admin import UserAdmin


# Admin pannel for users
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Login with email
    ordering = ('email',)
    list_display = ('email', 'first_name', 'is_host', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name')

    readonly_fields = ('date_joined', 'last_login')

    # User edit form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональна інформація', {'fields': ('first_name', 'avatar', 'phone_number', 'location')}),
        ('Права доступу',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_host', 'groups', 'user_permissions')}),
        ('Соціальні мережі і дані про себе', {'fields': ('contacts', 'instagram', 'facebook', 'about')}),
        ('Важливі дати', {'fields': ('last_login', 'date_joined')}),
    )

    # User creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password', 'confirm_password'),
        }),
    )


# 2. Admin pannel for events
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'date', 'ticket_price')
    list_filter = ('category', 'date')
    search_fields = ('title', 'address', 'description')

    # Hide automatically set fields
    exclude = ('owner', 'guests', 'created_at')

    def get_queryset(self, request):
        # Filtering only this host's events
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        # Assign owner automatically
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    # Access rights

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return getattr(request.user, 'is_host', False)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.owner != request.user:
            return False
        return getattr(request.user, 'is_host', False)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.owner != request.user:
            return False
        return getattr(request.user, 'is_host', False)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.owner != request.user:
            return False
        return getattr(request.user, 'is_host', False)
