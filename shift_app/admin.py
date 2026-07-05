from django.contrib import admin
from .models import Staff, Shift, ShiftFile
from .utils import import_shift_excel

admin.site.register(Staff)
admin.site.register(Shift)

@admin.register(ShiftFile)
class ShiftFileAdmin(admin.ModelAdmin):

    # Excelアップロード時の処理
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        import_shift_excel(obj.file.path, obj.title)


    # ShiftFile削除時の処理
    def delete_model(self, request, obj):
        # 古い勤務データを全削除
        Shift.objects.all().delete()
        super().delete_model(request, obj)

