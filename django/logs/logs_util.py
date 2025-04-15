from .models import LogAction, UserLog


def user_log_action(user, action):
    """
    Creates a log entry for a specified user and action.

    :param user: A User instance (or any instance based on settings.AUTH_USER_MODEL).
    :param action: An integer (or LogAction enum member) representing the action.
                   It should be one of LogAction's choices.
    :return: The created Log instance.
    """
    if isinstance(action, LogAction):
        action_value = action.value
    else:
        action_value = action

    log_entry = UserLog.objects.create(
        user=user,
        action=action_value
    )
    return log_entry
