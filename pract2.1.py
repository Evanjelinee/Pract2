import getpass
from datetime import datetime

users = [
    {'username': 'joh', 'password': 'password', 'role': 'user', 'history': [], 'cart': []},
    {'username': 'admin_user', 'password': 'password', 'role': 'admin'},
]

products = [
    {'id': 1, 'name': 'Платье летнее', 'price': 2500, 'category': 'женское', 'size': 'M', 'color': 'синее'},
    {'id': 2, 'name': 'Рубашка мужская', 'price': 1800, 'category': 'мужское', 'size': 'L', 'color': 'белая'},
    {'id': 3, 'name': 'Джинсы', 'price': 3200, 'category': 'мужское', 'size': 'XL', 'color': 'синие'},
    {'id': 4, 'name': 'Куртка', 'price': 4500, 'category': 'женское', 'size': 'S', 'color': 'черная'},
    {'id': 5, 'name': 'Свитер', 'price': 2200, 'category': 'мужское', 'size': 'M', 'color': 'серый'},
    {'id': 6, 'name': 'Юбка', 'price': 1900, 'category': 'женское', 'size': 'S', 'color': 'красная'},
    {'id': 7, 'name': 'Брюки', 'price': 2800, 'category': 'женское', 'size': 'L', 'color': 'черные'},
    {'id': 8, 'name': 'Футболка', 'price': 1200, 'category': 'мужское', 'size': 'M', 'color': 'зеленая'},
    {'id': 9, 'name': 'Пальто', 'price': 6000, 'category': 'женское', 'size': 'M', 'color': 'бежевое'},
    {'id': 10, 'name': 'Костюм', 'price': 5500, 'category': 'мужское', 'size': 'L', 'color': 'серый'}
]

def authenticate():
    username = input("Введите имя пользователя: ")
    password = getpass.getpass("Введите пароль: ")

    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None


def change_password(user):
    while True:
        new_password = getpass.getpass("Введите новый пароль: ")
        confirm_password = getpass.getpass("Подтвердите новый пароль: ")
        if new_password == confirm_password:
            user['password'] = new_password
            print("Пароль успешно изменен.")
            break
        else:
            print("Пароли не совпадают. Попробуйте снова.")


def add_product(products):
    new_product = {}
    new_product['id'] = len(products) + 1
    new_product['name'] = input("Введите название товара: ")
    while True:
        try:
            new_product['price'] = float(input("Введите цену товара: "))
            if new_product['price'] <= 0:
                raise ValueError("Цена должна быть больше 0.")
            break
        except ValueError as e:
            print(f"Ошибка: {e}")
    new_product['category'] = input("Введите категорию (мужское/женское): ").lower()
    new_product['size'] = input("Введите размер (S, M, L, XL, XXL): ").upper()
    new_product['color'] = input("Введите цвет: ")
    products.append(new_product)
    print("Товар добавлен.")


def delete_product(products):
    display_products(products)
    while True:
        try:
            product_id = int(input("Введите ID товара для удаления: "))
            product_to_delete = next((p for p in products if p['id'] == product_id), None)
            if product_to_delete:
                products.remove(product_to_delete)
                print("Товар удален.")
                break
            else:
                print("Товар не найден.")
        except ValueError:
            print("Ошибка ввода. Введите число.")


def search_products(products):
    search_term = input("Введите поисковый запрос (по названию): ").lower()
    results = [p for p in products if search_term in p['name'].lower()]
    display_products(results, f"Результаты поиска для '{search_term}':")


def filter_products(products):
    criteria = {}
    criteria['category'] = input("Введите категорию для фильтрации (мужское/женское, или оставьте пустым): ").lower() or None
    criteria['size'] = input("Введите размер для фильтрации (S, M, L, XL, XXL, или оставьте пустым): ").upper() or None
    criteria['color'] = input("Введите цвет для фильтрации (или оставьте пустым): ") or None

    filtered_products = products
    for key, value in criteria.items():
        if value:
            filtered_products = list(filter(lambda p: p.get(key) == value, filtered_products))
    display_products(filtered_products, "Отфильтрованные товары:")


def display_products(products, title="Список товаров"):
    if not products:
        print("Список товаров пуст.")
        return
    print(f"\n{title}:")
    for product in products:
        print(f"{product['id']}. {product['name']} ({product['price']} руб.), Размер: {product['size']}, Цвет: {product['color']}, Категория: {product['category']}")
        print("-" * 20)


def sort_products(products):
    sort_by = input("Сортировать по (name/price): ").lower()
    reverse = input("Обратный порядок (yes/no): ").lower() == 'yes'
    if sort_by == 'name':
        products.sort(key=lambda x: x['name'], reverse=reverse)
    elif sort_by == 'price':
        products.sort(key=lambda x: x['price'], reverse=reverse)
    else:
        print("Неверный параметр сортировки.")
    display_products(products)


def add_to_cart(user, products):
    while True:
        try:
            product_id = int(input("Введите ID товара для добавления в корзину: "))
            product = next((p for p in products if p['id'] == product_id), None)
            if product:
                user['cart'].append(product)
                print(f"Товар '{product['name']}' добавлен в корзину.")
            else:
                print("Товар не найден.")
            another_item = input("Добавить ещё товар в корзину? (yes/no): ").lower()
            if another_item != 'yes':
                break
        except ValueError:
            print("Неверный ID товара. Попробуйте снова.")


def view_cart(user):
    if not user['cart']:
        print("Корзина пуста.")
        return
    total_price = sum(product['price'] for product in user['cart'])
    print("\nВаша корзина:")
    for product in user['cart']:
        print(f"- {product['name']} ({product['price']} руб.)")
    print(f"\nОбщая стоимость: {total_price} руб.")


def edit_product(products):
    display_products(products)
    while True:
        try:
            product_id = int(input("Введите ID товара для редактирования: "))
            product_to_edit = next((p for p in products if p['id'] == product_id), None)
            if product_to_edit:
                print(f"Текущие данные товара: {product_to_edit}")
                product_to_edit['name'] = input("Введите новое название (или оставьте пустым для сохранения): ") or product_to_edit['name']
                while True:
                    try:
                        new_price = input("Введите новую цену (или оставьте пустым для сохранения): ")
                        product_to_edit['price'] = float(new_price) if new_price else product_to_edit['price']
                        if product_to_edit['price'] <= 0:
                            raise ValueError("Цена должна быть больше 0.")
                        break
                    except ValueError as e:
                        print(f"Ошибка: {e}")
                product_to_edit['category'] = input("Введите новую категорию (или оставьте пустым для сохранения): ").lower() or product_to_edit['category']
                product_to_edit['size'] = input("Введите новый размер (или оставьте пустым для сохранения): ").upper() or product_to_edit['size']
                product_to_edit['color'] = input("Введите новый цвет (или оставьте пустым для сохранения): ") or product_to_edit['color']
                print("Данные товара успешно изменены.")
                break
            else:
                print("Товар не найден.")
        except ValueError:
            print("Ошибка ввода. Введите число.")


def add_user():
    new_user = {}
    new_user['username'] = input("Введите имя пользователя: ")
    while True:
        new_password = getpass.getpass("Введите пароль: ")
        confirm_password = getpass.getpass("Подтвердите пароль: ")
        if new_password == confirm_password:
            new_user['password'] = new_password
            break
        else:
            print("Пароли не совпадают. Попробуйте снова.")
    new_user['role'] = input("Введите роль (user/admin): ").lower()
    new_user['history'] = []
    new_user['cart'] = []
    new_user['created_at'] = datetime.now()
    users.append(new_user)
    print("Пользователь добавлен.")


def delete_user():
    display_users()
    while True:
        try:
            username_to_delete = input("Введите имя пользователя для удаления: ")
            user_to_delete = next((u for u in users if u['username'] == username_to_delete), None)
            if user_to_delete:
                users.remove(user_to_delete)
                print("Пользователь удален.")
                break
            else:
                print("Пользователь не найден.")
        except ValueError:
            print("Ошибка ввода.")


def edit_user():
    display_users()
    while True:
        try:
            username_to_edit = input("Введите имя пользователя для редактирования: ")
            user_to_edit = next((u for u in users if u['username'] == username_to_edit), None)
            if user_to_edit:
                print(f"Текущие данные пользователя: {user_to_edit}")
                user_to_edit['username'] = input("Введите новое имя пользователя (или оставьте пустым для сохранения): ") or user_to_edit['username']
                while True:
                    new_password = getpass.getpass("Введите новый пароль (или оставьте пустым для сохранения): ")
                    if new_password:
                        confirm_password = getpass.getpass("Подтвердите новый пароль: ")
                        if new_password == confirm_password:
                            user_to_edit['password'] = new_password
                            break
                        else:
                            print("Пароли не совпадают. Попробуйте снова.")
                    else:
                        break
                user_to_edit['role'] = input("Введите новую роль (user/admin, или оставьте пустым для сохранения): ").lower() or user_to_edit['role']
                user_to_edit['subscription_type'] = input("Введите новый тип подписки (Premium/Basic, или оставьте пустым для сохранения): ").lower() or user_to_edit['subscription_type']
                print("Данные пользователя успешно изменены.")
                break
            else:
                print("Пользователь не найден.")
        except ValueError:
            print("Ошибка ввода.")


def display_users():
    if not users:
        print("Список пользователей пуст.")
        return
    print("\nСписок пользователей:")
    for user in users:
        print(f"- {user['username']} (роль: {user['role']})")


def analyze_statistics():
    if not users:
        print("Нет данных для анализа.")
        return

    product_popularity = {}
    for user in users:
        for product_id in user.get('history', []):
            product = next((p for p in products if p['id'] == product_id), None)
            if product:
                product_popularity[product['name']] = product_popularity.get(product['name'], 0) + 1

    print("\nСтатистика:")
    if product_popularity:
        print("Популярность товаров:")
        for product, count in product_popularity.items():
            print(f"- {product}: {count} покупок")
    else:
        print("Нет данных о покупках.")

def buy_from_cart(user, products):
    """Покупка товаров из корзины пользователя."""
    if not user['cart']:
        print("Ваша корзина пуста.")
        return

    print("\nТовары в корзине:")
    for i, product in enumerate(user['cart']):
        print(f"{i+1}. {product['name']} (ID: {product['id']})")

    while True:
        try:
            choice = int(input("\nВведите номер товара для покупки (или 0 для отмены): "))
            if 0 < choice <= len(user['cart']):
                product = user['cart'].pop(choice - 1)  
                user['history'].append(product['id'])  
                print(f"Товар '{product['name']}' успешно куплен!")
                break
            elif choice == 0:
                break
            else:
                print("Неверный номер товара. Попробуйте снова.")
        except ValueError:
            print("Неверный ввод. Попробуйте снова.")


def main():
    while(True):
        user = authenticate()
        if user:
            print(f"Вход выполнен. Ваша роль: {user['role']}")
            while True:
                print("\nМеню:")
                if user['role'] == 'user':
                    print("1. Фильтровать товары")
                    print("2. Сортировать товары")
                    print("3. Показать все товары")
                    print("4. Добавить в корзину")
                    print("5. Просмотреть корзину")
                    print("6. Изменить пароль")
                    print("7. Купить")
                    print("8. Выход")
                else:  # admin
                    print("1. Добавить товар")
                    print("2. Удалить товар")
                    print("3. Изменить товар")
                    print("4. Найти товар")
                    print("5. Показать все товары")
                    print("6. Добавить пользователя")
                    print("7. Удалить пользователя")
                    print("8. Изменить данные пользователя")
                    print("9. Показать всех пользователей")
                    print("10. Анализ статистики")
                    print("11. Выход")

                choice = input("Выберите действие: ")

                if user['role'] == 'user':
                    if choice == '1':
                        filter_products(products)
                    elif choice == '2':
                        sort_products(products)
                    elif choice == '3':
                        display_products(products)
                    elif choice == '4':
                        add_to_cart(user, products)
                    elif choice == '5':
                        view_cart(user)
                    elif choice == '6':
                        change_password(user)
                    elif choice == '7':
                        buy_from_cart(user, products)
                    elif choice == '8':
                        break
                    else:
                        print("Неверный выбор.")

                else:  # admin
                    if choice == '1':
                        add_product(products)
                    elif choice == '2':
                        delete_product(products)
                    elif choice == '3':
                        edit_product(products)
                    elif choice == '4':
                        search_products(products)
                    elif choice == '5':
                        display_products(products)
                    elif choice == '6':
                        add_user()
                    elif choice == '7':
                        delete_user()
                    elif choice == '8':
                        edit_user()
                    elif choice == '9':
                        display_users()
                    elif choice == '10':
                        analyze_statistics()
                    elif choice == '11':
                        break
                    else:
                        print("Неверный выбор.")

        else:
            print("Неверный логин или пароль.")


if __name__ == "__main__":
    main()