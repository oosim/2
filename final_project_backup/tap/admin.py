from django.contrib import admin
from .models import Post, Category, Tag, Region, RealTimeTomatoData, Farm

admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class RegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(RealTimeTomatoData)
class RealTimeTomatoDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'temperature', 'humidity')
    list_filter = ('timestamp',)
    search_fields = ('timestamp',)

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('farm', 'farm_slug', 'farm_owner', 'owner_image', 'location', 'created_at', 'updated_at')

    def get_farm_owner(self, obj):
        return obj.farm_owner

    get_farm_owner.short_description = '농부 이름'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Region, RegionAdmin)