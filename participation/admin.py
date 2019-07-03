from django.contrib import admin

from .models import ActorParticipation, TargetParticipation


@admin.register(ActorParticipation)
class ActorParticipationAdmin(admin.ModelAdmin):
    pass


@admin.register(TargetParticipation)
class TargetParticipationAdmin(admin.ModelAdmin):
    pass
