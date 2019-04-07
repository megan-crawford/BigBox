from django.contrib import admin
from .models import Post, Report, Profile, SeekerReview, CreatorReview, Seeker, Creator
# Register your models here

admin.site.register(Post)

admin.site.register(Report)

admin.site.register(Profile)

admin.site.register(SeekerReview)

admin.site.register(CreatorReview)

admin.site.register(Seeker)

admin.site.register(Creator)

