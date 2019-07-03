from django.contrib import admin

from .models import (
    Location, LocationRelationship, PostalLocation,
    TelecommunicationLocation, PhysicalLocation
)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(LocationRelationship)
class LocationRelationshipAdmin(admin.ModelAdmin):
    pass


@admin.register(PostalLocation)
class PostalLocationAdmin(admin.ModelAdmin):
    pass


@admin.register(TelecommunicationLocation)
class TelecommunicationLocationAdmin(admin.ModelAdmin):
    pass


@admin.register(PhysicalLocation)
class PhysicalLocationAdmin(admin.ModelAdmin):
    pass
