from django.shortcuts import render


def about(request):
    """Обрабатывает запрос на страницу описания сайта."""
    return render(request, 'pages/about.html')


def rules(request):
    """Обрабатывает запрос на страницу правил сайта."""
    return render(request, 'pages/rules.html')
