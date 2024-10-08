Feature: CRUD категории
  Scenario: Вход под админом
    Given Я открыл страницу "Входа"
    When Я ввожу текст "admin" в поле "username"
    And Я ввожу текст "admin" в поле "password"
    And Я отправляю форму "login"
    Then Я должен быть на главной странице

  Scenario: Создать новую категорию
    Given Я нахожусь на главной странице
    When Я нажимаю на кнопку "add_category"
    And Я перехожу на страницу создания категории
    And Я ввожу текст "Что-то" в поле "category_name"
    And Я отправляю форму "create_category"
    Then Я должен быть на главной странице
    And Я должен видеть категорию "Что-то" в списке

  Scenario: Изменить название категории
    Given Я нахожусь на главной странице
    When Я нажимаю на кнпоку детального просмотра категории "Что-то"
    And Я перехожу на страницу категории
    And Я нажимаю на кнопку изменения категории
    And Перехожу на страницу изменения категории
    And Я очищаю поле "category_name"
    And Я ввожу текст "Что-то-2" в поле "category_name"
    And Я отправляю форму "create_category"
    Then Я должен быть на главной странице
    And Я должен видеть категорию "Что-то-2" в списке

