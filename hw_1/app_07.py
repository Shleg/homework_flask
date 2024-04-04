"""
Задание No7
📌 Написать функцию, которая будет выводить на экран HTML страницу с блоками новостей.
📌 Каждый блок должен содержать заголовок новости, краткое описание и дату публикации.
📌 Данные о новостях должны быть переданы в шаблон через контекст.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def app_07():
    context = {'news':
        [
            {
                'title': 'Собянин оценил рост промпроизводства в Москве за семь лет',
                'description': 'Столичные промпредприятия за семь лет нарастили объем производства больше чем в два раза, сообщил мэр Москвы Сергей Собянин',
                'date': '25.03.2024',
                'source': 'Известия'
            },
            {
                'title': 'Ученый Язев предупредил о повышенной магнитной активности в ближайшие дни',
                'description': 'После крупной вспышки на Солнце в ближайшие дни будет наблюдаться повышенная магнитная активность.',
                'date': '24.03.2024',
                'source': 'Lenta.ru'
            },
            {
                'title': 'Суд отклонил иск инвесторов к ЦБ из-за остановки торгов на Мосбирже в 2022 году',
                'description': '"Отказать в признании решений и действий (бездействий) незаконными полностью", - говорится в информации на сайте суда.',
                'date': '23.03.2024',
                'source': 'Интерфакс'
            }
        ]
    }

    return render_template('news.html', **context)


if __name__ == '__main__':
    app.run(debug=True)