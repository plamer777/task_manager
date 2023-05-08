"""This unit contains a BotActions class with actions for different states
of telegram bot"""
import os
from django.utils import timezone
from bot.models import TgUser
from bot.tg.dc import Update
from goals.models import Goal, Status, Category, Roles

# --------------------------------------------------------------------------


class BotActions:
    """The BotActions class providing necessary action methods"""

    def __init__(self) -> None:
        """Initialize the BotActions class"""
        self._user_category = {}

    @staticmethod
    def confirm_user(update_obj: Update, new_code: str) -> str:
        """This method used for confirm state of telegram bot
        :param update_obj: An instance of Update class
        :param new_code: A string representing randomly generated code
        :return: A string representing the message to send to telegram bot
        """
        message = (
            f"Пожалуйста подтвердите свой аккаунт.\n"
            f"Введите на сайте следующий код: {new_code}"
        )

        TgUser.objects.filter(
            username=update_obj.message.from_.username).update(
            verification_code=new_code
        )

        return message

    @staticmethod
    def get_user_goals(tg_user: TgUser) -> str:
        """This method used to get all available goals of provided user
        :param tg_user: An instance of TgUser class
        :return: A string representing the list of user's goals
        """
        Goal.objects.filter(due_date__lt=timezone.now().date()).update(
            status=Status.archived
        )

        goals = Goal.objects.select_related("category").filter(
            category__board__participants__user=tg_user.user,
            status__lt=Status.archived,
        )

        goals_list = [
            f"{num}: {goal.title}" for num, goal in enumerate(goals, 1)]

        return (
            "Список ваших целей:\n" + "\n".join(goals_list)
            if goals_list
            else "У вас нет активных целей"
        )

    @staticmethod
    def get_user_categories(tg_user: TgUser) -> str:
        """This method used to get all available categories of provided user
        :param tg_user: An instance of TgUser class
        :return: A string representing the list of user's categories
        """
        categories = Category.objects.filter(
            is_deleted=False,
            board__participants__user=tg_user.user,
            board__participants__role__in=[Roles.owner, Roles.writer],
        )
        if not categories:
            return "У вас нет категорий"

        tg_user.bot_state = TgUser.BotStates.wait_category
        tg_user.save()

        categories_list = [
            f"{num}: {category.title}"
            for num, category in enumerate(categories, 1)
        ]

        return (
            "Введите название категории:\n" + "\n".join(categories_list)
        )

    def set_category(self, category: str, tg_user: TgUser) -> str:
        """This method used to check provided category and save it for
        current user if category exists
        :param tg_user: An instance of TgUser class
        :param category: A string representing the category title to save
        :return: A string representing the result of the operation
        """
        if Category.objects.filter(
            is_deleted=False,
            title=category,
            board__participants__user=tg_user.user,
            board__participants__role__in=[Roles.owner, Roles.writer],
        ).exists():
            self._user_category[tg_user.username] = category
            tg_user.bot_state = TgUser.BotStates.wait_title
            tg_user.save()

            return f"Категория {category} сохранена успешно, введите имя цели"

        return "Категория указана неверно, попробуйте еще раз, пожалуйста"

    def create_goal(self, title: str, tg_user: TgUser) -> str:
        """This method used to create a new goal
        :param tg_user: An instance of TgUser class
        :param title: A string representing the goal's title to create
        :return: A string representing the result of the operation
        """
        if not title:
            return "Название цели не может быть пустым"

        category = Category.objects.get(
            title=self._user_category[tg_user.username])
        new_goal = Goal.objects.create(
            title=title, user=tg_user.user, category=category
        )

        tg_user.bot_state = TgUser.BotStates.confirmed
        tg_user.save()

        host = os.environ.get("WEB_HOST")
        goal_url = f"{host}/categories/goals?goal={new_goal.pk}"

        return f"Цель успешно создана и доступна по ссылке: {goal_url}"

    @staticmethod
    def remove_goal(title: str, tg_user: TgUser) -> str:
        """This method used to remove existing goal
        :param tg_user: An instance of TgUser class
        :param title: A string representing the goal's title to create
        :return: A string representing the result of the operation
        """
        goal = Goal.objects.select_related("category").filter(
            category__board__participants__user=tg_user.user,
            category__board__participants__role__in=[Roles.owner, Roles.writer],
            status__lt=Status.archived,
            title=title,
        )
        if goal.exists():
            goal.update(status=Status.archived)
            tg_user.bot_state = TgUser.BotStates.confirmed
            tg_user.save()
            return f"Цель {title} успешно удалена"

        return f"Не могу найти вашу цель с именем {title}, проверьте данные"

    def cancel_request(self, tg_user: TgUser) -> str:
        """This method used to cancel a requested action
        :param tg_user: An instance of TgUser class
        :return: A string representing the result of the operation
        """
        tg_user.bot_state = TgUser.BotStates.confirmed
        tg_user.save()
        self._user_category.pop(tg_user.username, None)

        return f"Запрос отменен успешно"

    def get_removable_goals(self, tg_user: TgUser):
        message = ("Введите имя цели:\n" + self.get_user_goals(tg_user))
        tg_user.bot_state = TgUser.BotStates.remove_goal
        tg_user.save()
        return message
