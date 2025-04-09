from django.shortcuts import render
from .models import Player
from .predictor import get_injury_risk
from datetime import datetime
from django.db.models import Sum, Avg
import json
from django.shortcuts import get_object_or_404, redirect
from .forms import PlayerForm

def recovery_plans(request):
    players = Player.objects.all()
    
    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0

    recovery_plans = []
    for player in players:
        risk_prob = get_injury_risk(
            player.minutes_played,
            player.training_load,
            player.prev_injuries,
            player.age
        )
        risk_percent = round(risk_prob * 100, 2)

        if risk_prob > 0.7:
            high_risk_count += 1
            recovery_plan = {
                'plan': "تقليل الحمل التدريبي هذا الأسبوع وإجراء فحص طبي.",
                'details': "يجب تقليل شدة التمرين بشكل ملحوظ هذا الأسبوع مع استشارة طبية وعلاج طبيعي مكثف.",
                'recommendation': "لا بد من تقييم مستمر لحالة العضلات والمفاصل.",
            }
        elif risk_prob > 0.4:
            medium_risk_count += 1
            recovery_plan = {
                'plan': "مراقبة شدة التمرين بعناية والتركيز على استشفاء العضلات.",
                'details': "ينبغي على اللاعب التركيز على استراحة العضلات والقيام بتمارين منخفضة الشدة.",
                'recommendation': "الاستمرار في التمارين المعتدلة مع مراقبة الأداء البدني.",
            }
        else:
            low_risk_count += 1
            recovery_plan = {
                'plan': "مواصلة البرنامج الاعتيادي مع مراقبة الحالة.",
                'details': "إمكان اللاعب متابعة البرنامج التدريبي بشكل طبيعي مع مراقبة أي أعراض غير متوقعة.",
                'recommendation': "تقديم تغذية متوازنة ودعوة للاعب للانضمام إلى جلسات تدريبية لتحسين الأداء.",
            }

        recovery_plans.append({
            'player_name': player.name,
            'risk_percent': risk_percent,
            'recovery_plan': recovery_plan
        })

    context = {
        'recovery_plans': recovery_plans,
        'high_risk_count': high_risk_count,
        'medium_risk_count': medium_risk_count,
        'low_risk_count': low_risk_count,
        'current_year': datetime.now().year,
    }

    return render(request, 'recovery_plans.html', context)


def player_list(request):
    players = Player.objects.all()
    
    high_risk_count = players.filter(prev_injuries__gt=2).count()
    
    training_load_avg = players.aggregate(Avg('training_load'))['training_load__avg']
    if training_load_avg:
        training_load_avg = round(training_load_avg, 1)
    else:
        training_load_avg = 0
    
    total_injuries = players.aggregate(Sum('prev_injuries'))['prev_injuries__sum'] or 0
    
    context = {
        'players': players,
        'high_risk_count': high_risk_count,
        'training_load_avg': training_load_avg,
        'total_injuries': total_injuries,
        'current_year': datetime.now().year,
    }
    return render(request, 'player_list.html', context)


def player_add(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_list')
    else:
        form = PlayerForm()
    
    return render(request, 'player_add.html', {'form': form})


def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    
    risk_prob = get_injury_risk(
        player.minutes_played,
        player.training_load,
        player.prev_injuries,
        player.age
    )
    risk_percent = round(risk_prob * 100, 2)
    
    recommendations = []
    if risk_prob > 0.7:
        recommendations.append("تقليل الحمل التدريبي هذا الأسبوع.")
        recommendations.append("إجراء فحص طبي واستشارة طبية.")
    elif risk_prob > 0.4:
        recommendations.append("مراقبة شدة التمرين بعناية.")
        recommendations.append("التركيز على التعافي واستشفاء العضلات.")
    else:
        recommendations.append("يمكن متابعة البرنامج الاعتيادي.")

    context = {
        'player': player,
        'risk_percent': risk_percent,
        'recommendations': recommendations,
        'current_year': datetime.now().year,
    }
    return render(request, 'player_detail.html', context)


def player_delete(request, pk):
    player = get_object_or_404(Player, pk=pk)
    if request.method == 'POST':
        player.delete()
        return redirect('player_list')
    return render(request, 'player_confirm_delete.html', {'player': player})


def reports(request):
    players = Player.objects.all()
    
    high_risk_count = players.filter(prev_injuries__gt=2).count()
    total_injuries = players.aggregate(Sum('prev_injuries'))['prev_injuries__sum'] or 0
    training_load_avg = players.aggregate(Avg('training_load'))['training_load__avg'] or 0
    training_load_avg = round(training_load_avg, 1)

    training_load_labels = []
    training_load_values = []
    for p in players:
        training_load_labels.append(p.name)
        training_load_values.append(p.training_load)

    training_load_data = {
        "labels": training_load_labels,
        "values": training_load_values,
    }
    
    no_injury_count = players.filter(prev_injuries=0).count()
    mild_injury_count = players.filter(prev_injuries__gte=1, prev_injuries__lte=2).count()
    high_injury_count = players.filter(prev_injuries__gte=3).count()
    injury_distribution_data = {
        "labels": ["بدون إصابات", "إصابات متوسطة", "إصابات متعددة"],
        "values": [no_injury_count, mild_injury_count, high_injury_count],
    }

    context = {
        'players': players,
        'high_risk_count': high_risk_count,
        'total_injuries': total_injuries,
        'training_load_avg': training_load_avg,
        'current_year': datetime.now().year,
        'training_load_data': json.dumps(training_load_data),
        'injury_distribution_data': json.dumps(injury_distribution_data),
    }
    return render(request, 'reports.html', context)


def tests(request):
    players = Player.objects.all()
    
    tests_data = []
    for player in players:
        test_result = {
            'name': player.name,
            'age': player.age,
            'minutes_played': player.minutes_played,
            'training_load': player.training_load,
            'prev_injuries': player.prev_injuries,
            'risk_percent': round(get_injury_risk(
                player.minutes_played,
                player.training_load,
                player.prev_injuries,
                player.age
            ) * 100, 2),
        }
        tests_data.append(test_result)

    context = {
        'tests_data': tests_data,
        'current_year': datetime.now().year,
    }
    return render(request, 'tests.html', context)
