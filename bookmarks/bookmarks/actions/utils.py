from django.contrib.contenttypes.models import ContentType
from .models import Action
from django.utils import timezone

import datetime


def create_action(user, verb, target=None):
    # Поиск похожего действия, совершенного за последнюю минуту.
    now = timezone.now()

    last_minute = now - datetime.timedelta(seconds=60)
    simular_actions = Action.objects.filter(
        user_id=user.id, 
        verb=verb, 
        created__gte=last_minute
    )

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        simular_actions = simular_actions.filter(
            target_ct=target_ct,
            target_id=target.id,
        )
    if not simular_actions:
        # Похожее действие не найдено, создаем новое.
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False