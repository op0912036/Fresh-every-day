from django.contrib import admin
from goods.models import *
from django.core.cache import cache


# Register your models here.
class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''新增或更新表中的数据时调用'''
        super().save_model(request, obj, form, change)
        from celery_tasks.tasks import task_generate_static_index
        task_generate_static_index.delay()
        cache.delete('cache_index')

    def delete_mode(self, request, obj):
        '''删除表中的数据时调用'''
        super().delete_model(request, obj)
        from celery_tasks.tasks import task_generate_static_index
        task_generate_static_index.delay()
        cache.delete('cache_index')


admin.site.register(GoodsType, BaseAdmin)
admin.site.register(GoodsSPU, BaseAdmin)
admin.site.register(GoodsSKU, BaseAdmin)
admin.site.register(GoodsImage)
admin.site.register(IndexGoodsBanner, BaseAdmin)
admin.site.register(IndexTypeGoodsBanner, BaseAdmin)
admin.site.register(IndexPromotionBanner, BaseAdmin)
