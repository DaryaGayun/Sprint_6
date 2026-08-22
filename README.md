# Selenium tests for Yandex Samokat

Автотесты для учебного сервиса «Яндекс.Самокат».
Реализован по паттерну Page Object, с параметризацией тестов и отчётом в Allure.

## Технологии

- PythonS
- Selenium
- PyTest
- Allure
- Page Object Model

## Структура проекта

```
/
├─ allure-report/
├─ allure-results/
├─ pages/
├─ tests/
├─ conftest.py
├─ ...
```

## Запуск тестов

```
pytest
```

## Запуск с сохранением результатов для Allure

```
pytest --alluredir=allure-results
```

## Просмотр отчёта Allure

```
allure serve allure-results
```

## Генерация статического отчета

```
allure generate allure-results -o allure-report --clean
```
