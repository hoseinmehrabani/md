import openai

# کلید API خود را وارد کنید
openai.api_key = "YOUR_API_KEY"

class ChatGPT:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.7, max_tokens=150, n=1):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.n = n
        self.history = []

    def ask(self, question):
        # افزودن سوال به تاریخچه
        self.history.append({"role": "user", "content": question})

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.history,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                n=self.n
            )
            answer = response.choices[0].message['content']
            # افزودن پاسخ به تاریخچه
            self.history.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            return f"خطا در برقراری ارتباط با API: {str(e)}"

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []

if __name__ == "__main__":
    model_choice = input("مدل مورد نظر خود را وارد کنید (gpt-3.5-turbo یا gpt-4): ")
    temperature = float(input("درجه حرارت (0.0 تا 1.0) را وارد کنید (پیش‌فرض 0.7): ") or 0.7)
    max_tokens = int(input("حداکثر تعداد توکن‌ها را وارد کنید (پیش‌فرض 150): ") or 150)
    n = int(input("تعداد پاسخ‌ها را وارد کنید (پیش‌فرض 1): ") or 1)

    chat_gpt = ChatGPT(model=model_choice, temperature=temperature, max_tokens=max_tokens, n=n)

    while True:
        question = input("سوال خود را وارد کنید (برای خروج 'exit' را وارد کنید یا برای پاک‌سازی تاریخچه 'clear' را وارد کنید): ")
        if question.lower() == 'exit':
            break
        elif question.lower() == 'clear':
            chat_gpt.clear_history()
            print("تاریخچه پاک شد.")
            continue
        answer = chat_gpt.ask(question)
        print("پاسخ:", answer)

        # نمایش تاریخچه گفتگو
        print("\nتاریخچه گفتگو:")
        for message in chat_gpt.get_history():
            role = "شما" if message["role"] == "user" else "ChatGPT"
            print(f"{role}: {message['content']}")
