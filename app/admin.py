from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import *

class AgentAdmin(admin.ModelAdmin):
    class Meta:
        model = Agent
        exclude = ['__all__']

class TeamLeaderAdmin(admin.ModelAdmin):
    class Meta:
        model = TeamLeader
        exclude = ['__all__']

@admin.register(Project)
class Admin(admin.ModelAdmin):
    pass


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Agent, AgentAdmin)
admin.site.register(TeamLeader, TeamLeaderAdmin)