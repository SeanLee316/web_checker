import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import re
from openpyxl import Workbook
with open("conflict_keywords.txt", "r", encoding="utf-8") as f:
    conflict_keywords = [line.strip() for line in f]
with open("undesirable_categories.txt", "r", encoding="utf-8") as f:
    undesirable_categories = [line.strip() for line in f]
sia = SentimentIntensityAnalyzer()
def analyze_domain(domain):
    try:
        response = requests.get("http://" + domain, stream=True)
        response.raise_for_status()

        max_content_size = 10 * 1024 * 1024
        content = b''
        for chunk in response.iter_content(chunk_size=1024):
            content += chunk
            if len(content) > max_content_size:
                raise Exception("Превышен максимальный размер контента")
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        url = response.url
        tokens = nltk.word_tokenize(text.lower())
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stopwords.words('russian')]
        if any(category in filtered_tokens for category in undesirable_categories) or \
           any(keyword in filtered_tokens for keyword in conflict_keywords):
            return "Небезопасный", "Содержит нежелательный контент или новости о конфликтах", None, None
        sentiment_scores = sia.polarity_scores(text)
        if sentiment_scores['compound'] < -0.5:  
            return "Небезопасный", "Отрицательная тональность текста", None, None
        content_category = None
        if any(keyword in filtered_tokens for keyword in ["новости", "события", "происшествия", "репортаж", "журналистика"]):
            content_category = "Новости"
        elif any(keyword in filtered_tokens for keyword in ["спорт", "футбол", "баскетбол", "хоккей", "олимпиада"]):
            content_category = "Спорт"
        elif any(keyword in filtered_tokens for keyword in ["технологии", "гаджеты", "программы", "инновации", "IT"]):
            content_category = "Технологии"
        elif any(keyword in filtered_tokens for keyword in ["здоровье", "медицина", "болезни", "лечение", "фитнес"]):
            content_category = "Здоровье"
        elif any(keyword in filtered_tokens for keyword in ["образование", "университет", "школа", "курсы", "обучение"]):
            content_category = "Образование"
        elif any(keyword in filtered_tokens for keyword in ["бизнес", "финансы", "экономика", "маркетинг", "инвестиции"]):
            content_category = "Бизнес"
        elif any(keyword in filtered_tokens for keyword in ["путешествия", "туризм", "страны", "отели", "авиабилеты"]):
            content_category = "Путешествия"
        elif any(keyword in filtered_tokens for keyword in ["развлечения", "кино", "музыка", "игры", "шоу"]):
            content_category = "Развлечения"
        elif any(keyword in filtered_tokens for keyword in ["автомобили", "машины", "мотоциклы", "транспорт"]):
            content_category = "Автомобили"
        elif any(keyword in filtered_tokens for keyword in ["дом", "сад", "ремонт", "интерьер", "дизайн"]):
            content_category = "Дом и сад"
        elif any(keyword in filtered_tokens for keyword in ["мода", "стиль", "одежда", "аксессуары", "красота"]):
            content_category = "Мода и красота"
        elif any(keyword in filtered_tokens for keyword in ["еда", "рецепты", "кулинария", "рестораны"]):
            content_category = "Еда и кулинария"
        elif any(keyword in filtered_tokens for keyword in ["наука", "исследования", "технологии", "эксперименты"]):
            content_category = "Наука"
        elif any(keyword in filtered_tokens for keyword in ["искусство", "живопись", "скульптура", "музеи", "галереи"]):
            content_category = "Искусство и культура"
        elif any(keyword in filtered_tokens for keyword in ["политика", "правительство", "выборы", "партии"]):
            content_category = "Политика"
        elif any(keyword in filtered_tokens for keyword in ["юмор", "анекдоты", "шутки", "приколы"]):
            content_category = "Юмор"
        elif any(keyword in filtered_tokens for keyword in ["фотография", "фото", "изображения", "галерея"]):
            content_category = "Фотография"
        elif any(keyword in filtered_tokens for keyword in ["литература", "книги", "романы", "поэзия", "авторы"]):
            content_category = "Литература"
        elif any(keyword in filtered_tokens for keyword in ["история", "археология", "цивилизации", "события"]):
            content_category = "История"
        elif any(keyword in filtered_tokens for keyword in ["религия", "вера", "духовность", "бог", "церковь"]):
            content_category = "Религия"
        elif any(keyword in filtered_tokens for keyword in ["философия", "мышление", "идеи", "концепции"]):
            content_category = "Философия"
        elif any(keyword in filtered_tokens for keyword in ["психология", "эмоции", "поведение", "отношения"]):
            content_category = "Психология"
        site_type = None
        if "/blog/" in url or any(keyword in filtered_tokens for keyword in ["блог", "дневник", "записи", "комментарии"]):
            site_type = "Блог"
        elif any(keyword in filtered_tokens for keyword in ["купить", "продажа", "товары", "корзина", "заказ"]):
            site_type = "Интернет-магазин"
        elif any(keyword in filtered_tokens for keyword in ["форум", "обсуждение", "темы", "сообщения"]):
            site_type = "Форум"
        elif any(keyword in filtered_tokens for keyword in ["портфолио", "работы", "услуги", "контакты"]):
            site_type = "Портфолио/Сайт услуг"
        elif any(keyword in filtered_tokens for keyword in ["компания", "о нас", "команда", "вакансии"]):
            site_type = "Корпоративный сайт"
        elif any(keyword in filtered_tokens for keyword in ["новости", "события", "происшествия", "репортаж", "журналистика"]):
            site_type = "Новостной портал"
        elif any(keyword in filtered_tokens for keyword in ["скачать", "файлы", "программы", "фильмы", "музыка"]):
            site_type = "Файлообменник"
        elif any(keyword in filtered_tokens for keyword in ["поиск", "результаты", "запросы"]):
            site_type = "Поисковая система"
        elif any(keyword in filtered_tokens for keyword in ["социальная сеть", "друзья", "сообщения", "профиль"]):
            site_type = "Социальная сеть"
        elif "wikipedia.org" in url: 
            site_type = "Энциклопедия"
        elif any(keyword in filtered_tokens for keyword in ["образование", "университет", "школа", "курсы", "обучение"]):
            site_type = "Образовательный портал"
        elif any(keyword in filtered_tokens for keyword in ["каталог", "список", "компании", "организации"]):
            site_type = "Каталог/Справочник"
        elif any(keyword in filtered_tokens for keyword in ["лендинг", "продукт", "услуга", "заказать", "купить"]):
            site_type = "Лендинг"
        return "Безопасный", "Нет явных признаков нежелательного контента", content_category, site_type
    except requests.exceptions.RequestException as e:
        return "Ошибка", str(e), None, None
with open("domains.txt", "r") as f:
    domains = [domain.strip() for domain in f]
wb = Workbook()
ws = wb.active
ws.append(["Домен", "Статус", "Причина", "Категория", "Тип"])
total_domains = len(domains)
for i, domain in enumerate(domains):
    print(f"Анализирую домен {i+1} из {total_domains}: {domain}")
    status, reason, content_category, site_type = analyze_domain(domain)
    ws.append([domain, status, reason, content_category, site_type])
    wb.save("analysis_results.xlsx")
    print(f"Результат: {status}, Причина: {reason}, Категория: {content_category}, Тип: {site_type}\n")
wb.save("analysis_results.xlsx")