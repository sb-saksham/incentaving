from django.shortcuts import render, redirect
from .models import Action, ConservationCount
from django.contrib.auth.decorators import login_required


@login_required
def user_home(request):
    user = request.user
    actions = Action.objects.all()
    context = {'actions': actions}
    cc_obj, is_created = ConservationCount.objects.get_or_create(user=user)
    if not is_created and cc_obj.score != 0:
        context['c_score'] = cc_obj.score
        context['is_apt'] = cc_obj.is_apt
    return render(request, 'action/user_home.html', context)


@login_required
def take_cc(request):
    actions = []
    cc_value = 0
    total_req_cc = 0
    context = {}
    qs = Action.objects.all()
    if qs.exists():
        for action in qs:
            actions.append(action)
            total_req_cc = total_req_cc + action.required_cc
    context['actions'] = actions
    if request.method == 'POST':
        data = request.POST
        for action in actions:
            cc_temp = int(data.get(str(action.id)), 0)
            cc_value = cc_value + cc_temp
        is_apt = False
        if cc_value >= total_req_cc:
            is_apt = True
        cc_obj = ConservationCount.objects.get(user=request.user, is_apt=is_apt)
        cc_obj.score = cc_value
        cc_obj.save()
        return redirect('action:home')
    return render(request, "action/cc_take.html", context=context)
