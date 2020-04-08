from django.shortcuts import render

from .models import ActiveUser


def room_view(request, room_name=''):
    return render(request, 'active_users/index.html', {})