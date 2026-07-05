from django.shortcuts import render
from .models import Shift
from datetime import datetime, timedelta

def shift_search(request):
    date_str = request.GET.get("date")
    if not date_str:
        return render(request, "search_shift.html")

    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # ★ 今日の勤務一覧
    shifts = Shift.objects.filter(date=target_date)

    # ★ 夜勤明け判定（A の前日の C1/C2 を拾う）
    night1 = []   # 1階夜勤明け
    night2 = []   # 2階夜勤明け

    for s in shifts:
        if s.code == "A":  # 今日が夜勤明け勤務
            prev_date = target_date - timedelta(days=1)
            prev_shift = Shift.objects.filter(date=prev_date, staff=s.staff).first()

            if prev_shift:
                if prev_shift.code == "C1":
                    night1.append(s.staff.name)
                elif prev_shift.code == "C2":
                    night2.append(s.staff.name)

    # ★ 洗濯担当（西畑 真由美）
    sentaku_shift = Shift.objects.filter(
        date=target_date,
        staff__name="西畑　真由美"
    ).first()

    if sentaku_shift:
        code = sentaku_shift.code
        if code in [None, "", " "]:
            laundry_display = "西畑　真由美"
        else:
            laundry_display = code
    else:
        laundry_display = None

    # ★ 施設行事
    event_display = None
    for s in shifts:
        if s.event not in [None, "", " "]:
            event_display = s.event
        break

    # ★ 1階・2階の分類（勤務コードで判定）
    floor1_codes = ["1-1", "1-2", "1-3", "1-4", "1-5", "C1"]
    floor2_codes = ["1", "2", "3", "4", "5", "C2"]

    floor1 = [s for s in shifts if s.code in floor1_codes]
    floor2 = [s for s in shifts if s.code in floor2_codes]

    # ★ 表示順（勤務表の並び順）
    order = [
        "1-1", "1-2", "1-3", "1-4", "1-5", "C1",
        "1", "2", "3", "4", "5", "C2",
        "A"
    ]

    # ★ 並び替え
    floor1_sorted = sorted(
        floor1,
        key=lambda x: order.index(x.code) if x.code in order else 999
    )

    floor2_sorted = sorted(
        floor2,
        key=lambda x: order.index(x.code) if x.code in order else 999
    )

    context = {
        "date": target_date,
        "weekday": target_date.strftime("%a"),
        "event": event_display,
        "laundry": laundry_display,
        "floor1": floor1_sorted,
        "floor2": floor2_sorted,
        "night1": night1,
        "night2": night2,
    }

    return render(request, "search_shift.html", context)

