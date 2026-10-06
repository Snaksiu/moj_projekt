from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})

import sys
import time
import django
from django.http import JsonResponse
from .data import GAMES

START_TIME = time.time()

# Zadanie 2
def health_check(request):
    return JsonResponse({"status": "ok"})

# Zadanie 4 i Zadanie 6 (lista i filtrowanie)
def list_games(request):
    category = request.GET.get('category')
    max_players = request.GET.get('players')
    
    filtered_games = GAMES
    if category:
        filtered_games = [g for g in filtered_games if g['category'] == category]
    if max_players:
        filtered_games = [g for g in filtered_games if g['players'] <= int(max_players)]
        
    return JsonResponse(filtered_games, safe=False)

# Zadanie 5 (szczegóły i obsługa 404)
def game_detail(request, id):
    game = next((g for g in GAMES if g['id'] == id), None)
    if not game:
        return JsonResponse({"error": f"Game with id {id} not found."}, status=404)
    return JsonResponse(game)

# Zadanie 7 (info)
def info(request):
    categories = list(set(g['category'] for g in GAMES))
    uptime = round(time.time() - START_TIME, 2)
    
    data = {
        "app_name": "boardgames",
        "app_version": "1.0.0",
        "python_version": sys.version,
        "django_version": django.get_version(),
        "database_type": "in-memory static file",
        "total_records": len(GAMES),
        "available_categories": categories,
        "uptime_seconds": uptime
    }
    return JsonResponse(data)

# Zadanie 8 (statystyki)
def stats(request):
    prices = [g['price'] for g in GAMES]
    
    category_counts = {}
    for g in GAMES:
        cat = g['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
        
    data = {
        "total_records": len(GAMES),
        "category_counts": category_counts,
        "avg_price": round(sum(prices) / len(prices), 2) if prices else 0,
        "min_price": min(prices) if prices else 0,
        "max_price": max(prices) if prices else 0,
    }
    return JsonResponse(data)