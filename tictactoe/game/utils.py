menu = [{'title':'Главная', 'url_name':'home'},
        {'title':'Играть', 'url_name':'play'},
        {'title':'Профиль', 'url_name':'profile'},
        {'title':'Таблица лидеров', 'url_name':'liders'},]
        # {'title':'Вход', 'url_name':'enter'}]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context