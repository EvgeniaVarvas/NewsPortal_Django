# Проект News Portal


### Модели

##### Author
- **user:** Одно к одному с встроенной моделью User
- **rating:** Рейтинг пользователя, рассчитываемый на основе статей, новостей и комментариев

##### Category
- **name:** Уникальное название категории

##### Post
- **author:** Внешний ключ к модели Author
- **post_type:** Выбор между 'article' (статья) или 'news' (новость)
- **created:** Автоматически добавляемая дата и время
- **categories:** Многие ко многим с моделью Category через промежуточную модель PostCategory
- **title:** Заголовок статьи или новости
- **text:** Содержание статьи или новости
- **rating:** Рейтинг статьи или новости

##### PostCategory
- **post:** Внешний ключ к модели Post
- **category:** Внешний ключ к модели Category

##### Comment
- **post:** Внешний ключ к модели Post
- **user:** Внешний ключ к встроенной модели User (комментарии могут оставлять все пользователи, не только автор)
- **text:** Текст комментария
- **created:** Автоматически добавляемая дата и время
- **rating:** Рейтинг комментария

### Методы

##### В моделях Comment и Post
- **like():** Увеличивает рейтинг на 1
- **dislike():** Уменьшает рейтинг на 1

##### В модели Post
- **preview():** Возвращает начало статьи (124 символа) с троеточием в конце

##### В модели Author
- **update_rating():** Обновляет рейтинг автора на основе суммы рейтингов статей, рейтингов комментариев и рейтингов комментариев к статьям автора

### Команды консоли (Django Shell)


### Фильтры и пагинация

Добавьте постраничный вывод на /news/, чтобы на одной странице было не больше 10 новостей и видны номера лишь ближайших страниц, а также возможность перехода к первой или последней странице.
Добавьте страницу /news/search. На ней должна быть реализована возможность искать новости по определённым критериям. Критерии должны быть следующие:

 * по названию;
 * по категории;
 * позже указываемой даты.

### Создание, редактирование и удаление объектов

Запрограммируйте страницы создания, редактирования и удаления новостей и статей.


```python
# Создать пользователей
user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')

# Создать авторов
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Добавить категории
category1 = Category.objects.create(name='Спорт')
category2 = Category.objects.create(name='Политика')
category3 = Category.objects.create(name='Образование')
category4 = Category.objects.create(name='Технологии')

# Добавить статьи и новости
article1 = Post.objects.create(author=author1, post_type='article', title='Статья 1', text='Содержание статьи 1', rating=0)
article2 = Post.objects.create(author=author2, post_type='article', title='Статья 2', text='Содержание статьи 2', rating=0)
news1 = Post.objects.create(author=author1, post_type='news', title='Новость 1', text='Содержание новости 1', rating=0)

# Присвоить категории статьям и новостям
article1.categories.add(category1, category2)
article2.categories.add(category3, category4)
news1.categories.add(category1, category3)

# Добавить комментарии к статьям и новостям
comment1 = Comment.objects.create(post=article1, user=user1, text='Комментарий 1', rating=0)
comment2 = Comment.objects.create(post=article2, user=user2, text='Комментарий 2', rating=0)
comment3 = Comment.objects.create(post=article1, user=user2, text='Комментарий 3', rating=0)
comment4 = Comment.objects.create(post=news1, user=user1, text='Комментарий 4', rating=0)

# Лайки и дизлайки
article1.like()
comment2.dislike()

# Обновить рейтинги
author1.update_rating()
author2.update_rating()

# Вывести имя пользователя и рейтинг лучшего пользователя
best_user = Author.objects.order_by('-rating').first().user
print(f'Лучший пользователь: {best_user.username}, Рейтинг: {best_user.author.rating}')

# Вывести детали лучшей статьи
best_article = Post.objects.filter(post_type='article').order_by('-rating').first()
print(f'Дата: {best_article.created}, Автор: {best_article.author.user.username}, Рейтинг: {best_article.rating}, Заголовок: {best_article.title}, Превью: {best_article.preview()}')

# Выводим все комментарии к лучшей статье
all_comments = Comment.objects.filter(post=best_article)
for comments in all_comments:
    print(f'Дата: {comments.created}, Пользователь: {comments.user.username}, Рейтинг: {comments.rating}, Текст: {comments.text}')



