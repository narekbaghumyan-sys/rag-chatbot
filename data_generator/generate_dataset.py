import csv
import random
import os
import uuid

# =========================
# CONFIG
# =========================
TOTAL_CONVERSATIONS = 5_000
OUTPUT_DIR = "dataset"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "train_1m.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

languages = ["ru", "en"]
topics = ["programming", "debug", "optimization", "chat", "disaster"]

# =========================
# TEXT VARIATIONS
# =========================
USER_CONFUSION = {
    "en": ["I don't understand", "This doesn't work", "Why is this wrong?", "I'm confused"],
    "ru": ["Я не понимаю", "Это не работает", "Почему это ошибка?", "Я запутался"]
}

ASSISTANT_STYLE = {
    "en": ["Let me explain step by step.", "Here is a clear explanation.", "Let's break it down."],
    "ru": ["Давай разберём по шагам.", "Вот понятное объяснение.", "Объясняю подробно."]
}

# =========================
# DIALOGS
# =========================
def programming_dialog(lang):
    if lang == "en":
        return [
            ("user", "How do I create a website from scratch?"),
            ("assistant", "You need HTML for structure, CSS for styling, and JavaScript for logic."),
            ("user", random.choice(USER_CONFUSION["en"])),
            ("assistant", random.choice(ASSISTANT_STYLE["en"]) +
             " Start with a basic HTML file, then add styles and scripts."),
            ("user", "Can you show a simple example?"),
            ("assistant", "<!DOCTYPE html>\n<html>\n<body>\n<h1>Hello World</h1>\n</body>\n</html>")
        ]
    else:
        return [
            ("user", "Как создать сайт с нуля?"),
            ("assistant", "Нужны HTML для структуры, CSS для стилей и JavaScript для логики."),
            ("user", random.choice(USER_CONFUSION["ru"])),
            ("assistant", random.choice(ASSISTANT_STYLE["ru"]) +
             " Начни с HTML, потом добавь стили и скрипты."),
            ("user", "Покажи простой пример"),
            ("assistant", "<!DOCTYPE html>\n<html>\n<body>\n<h1>Привет, мир</h1>\n</body>\n</html>")
        ]

def debug_dialog(lang):
    if lang == "en":
        return [
            ("user", "My Python code crashes"),
            ("assistant", "What error message do you see?"),
            ("user", "IndexError: list index out of range"),
            ("assistant", "This means you're accessing an index that doesn't exist."),
            ("user", "How do I fix it?"),
            ("assistant", "Check the list length before accessing elements.")
        ]
    else:
        return [
            ("user", "Мой Python код падает"),
            ("assistant", "Какое сообщение об ошибке?"),
            ("user", "IndexError: list index out of range"),
            ("assistant", "Это значит, что индекс выходит за пределы списка."),
            ("user", "Как исправить?"),
            ("assistant", "Проверяй длину списка перед обращением.")
        ]

def optimization_dialog(lang):
    if lang == "en":
        return [
            ("user", "My algorithm is very slow"),
            ("assistant", "What is the time complexity?"),
            ("user", "O(n^2)"),
            ("assistant", "You can optimize it using sorting or a hash map."),
            ("user", "Can you explain why?"),
            ("assistant", "Because it reduces repeated comparisons and nested loops.")
        ]
    else:
        return [
            ("user", "Мой алгоритм очень медленный"),
            ("assistant", "Какая временная сложность?"),
            ("user", "O(n^2)"),
            ("assistant", "Можно оптимизировать с помощью сортировки или хеш-таблицы."),
            ("user", "Почему это быстрее?"),
            ("assistant", "Потому что уменьшается количество вложенных циклов.")
        ]

def disaster_dialog(lang):
    if lang == "en":
        return [
            ("user", "What should I do during an earthquake?"),
            ("assistant", "Stay calm and take cover under sturdy furniture."),
            ("user", "Any tips to prepare in advance?"),
            ("assistant", "Keep emergency supplies, know evacuation routes, and secure heavy objects."),
            ("user", "What about communication?"),
            ("assistant", "Have a family plan and keep a charged phone and backup power.")
        ]
    else:
        return [
            ("user", "Что делать при землетрясении?"),
            ("assistant", "Сохраняйте спокойствие и укройтесь под прочной мебелью."),
            ("user", "Как подготовиться заранее?"),
            ("assistant", "Имейте запас еды и воды, знайте пути эвакуации, закрепите тяжёлые предметы."),
            ("user", "А как быть с коммуникацией?"),
            ("assistant", "Составьте семейный план и держите зарядный телефон и запас энергии.")
        ]

def chat_dialog(lang):
    if lang == "en":
        return [
            ("user", "Hi"),
            ("assistant", "Hello! How can I help you today?"),
            ("user", "Can you help me learn programming?"),
            ("assistant", "Of course. We can learn step by step."),
            ("user", "I want to become a developer"),
            ("assistant", "Practice daily and build real projects.")
        ]
    else:
        return [
            ("user", "Привет"),
            ("assistant", "Привет! Чем могу помочь?"),
            ("user", "Ты можешь помочь выучить программирование?"),
            ("assistant", "Конечно. Будем учиться шаг за шагом."),
            ("user", "Я хочу стать разработчиком"),
            ("assistant", "Практикуйся каждый день и делай проекты.")
        ]

def generate_dialog(topic, lang):
    return {
        "programming": programming_dialog,
        "debug": debug_dialog,
        "optimization": optimization_dialog,
        "disaster": disaster_dialog,
        "chat": chat_dialog
    }[topic](lang)

def main():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["conversation_id", "turn", "role", "content", "language", "topic"])

        for _ in range(TOTAL_CONVERSATIONS):
            conversation_id = str(uuid.uuid4())
            lang = random.choice(languages)
            topic = random.choice(topics)

            dialog = generate_dialog(topic, lang)

            for turn, (role, content) in enumerate(dialog, start=1):
                writer.writerow([
                    conversation_id,
                    turn,
                    role,
                    content,
                    lang,
                    topic
                ])

    print("✅ Dataset generated:", OUTPUT_FILE)

if __name__ == "__main__":
    main()


'''
curl --request POST 'https://fbzvkjnvlsanjeezmkup.supabase.co/functions/v1/smart-processor' \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZienZram52bHNhbmplZXpta3VwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg0NjY3NjYsImV4cCI6MjA4NDA0Mjc2Nn0.dnJe8f9TkjyhpW6p35mnxXX8oQUPs8SWl_kiew-EVf0' \
  --header 'Content-Type: application/json'
'''