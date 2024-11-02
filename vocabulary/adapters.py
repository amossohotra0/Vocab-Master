from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.contrib.auth.models import User
from .models import UserProfile

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    
    def pre_social_login(self, request, sociallogin):
        """
        Check if user exists with same email and connect accounts
        """
        if sociallogin.is_existing:
            return
        
        if not sociallogin.email_addresses:
            return
            
        email = sociallogin.email_addresses[0].email
        
        # Check if user with this email already exists
        try:
            existing_user = User.objects.get(email=email)
            # Connect the social account to existing user
            sociallogin.connect(request, existing_user)
        except User.DoesNotExist:
            pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        Save user and create comprehensive profile from Google data
        """
        user = super().save_user(request, sociallogin, form)
        
        # Extract Google user data
        google_data = sociallogin.account.extra_data
        
        # Create or update user profile
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'google_id': google_data.get('id', ''),
                'first_name': google_data.get('given_name', ''),
                'last_name': google_data.get('family_name', ''),
                'profile_picture': google_data.get('picture', ''),
            }
        )
        
        # Update user's first and last name if not set
        if not user.first_name and google_data.get('given_name'):
            user.first_name = google_data.get('given_name', '')
        if not user.last_name and google_data.get('family_name'):
            user.last_name = google_data.get('family_name', '')
        user.save()
        
        return user
    
    def populate_user(self, request, sociallogin, data):
        """
        Populate user fields from social account data
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Set names from Google data
        google_data = sociallogin.account.extra_data
        user.first_name = google_data.get('given_name', '')
        user.last_name = google_data.get('family_name', '')
        
        return user