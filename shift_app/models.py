from django.db import models

class Staff(models.Model):
    name = models.CharField(max_length=100)
    floor = models.IntegerField()  # 1階 or 2階

    def __str__(self):
        return self.name


class Shift(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
    code = models.CharField(max_length=20, blank=True, null=True)
    laundry = models.CharField(max_length=20, blank=True, null=True)
    weekday = models.CharField(max_length=5, blank=True, null=True)
    event = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.staff.name} - {self.date} - {self.code}"



class ShiftFile(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="shift_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # ★ 遅延 import（循環を防止）
        from .utils import import_shift_excel
        from .models import Shift
        
        #古いデータの削除
        Shift.objects.all().delete()

        # ★ Excel → Shift の取り込み処理を自動実行
        import_shift_excel(self.file, self.title)