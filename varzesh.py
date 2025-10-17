import json
import tkinter as tk
from tkinter import messagebox, simpledialog, PhotoImage


class Exercise:
    def __init__(self, name, duration, repetitions, description):
        self.name = name
        self.duration = duration  # in minutes
        self.repetitions = repetitions
        self.description = description

    def __str__(self):
        return f"{self.name} - {self.duration} دقیقه, {self.repetitions} تکرار\n{self.description}"


class NutritionTip:
    def __init__(self, tip):
        self.tip = tip

    def __str__(self):
        return f"نکته تغذیه: {self.tip}"


class WorkoutRoutine:
    def __init__(self, name):
        self.name = name
        self.exercises = []
        self.completed_exercises = []  # To track completed exercises

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def remove_exercise(self, exercise_name):
        self.exercises = [ex for ex in self.exercises if ex.name.lower() != exercise_name.lower()]
        self.completed_exercises = [ex for ex in self.completed_exercises if ex.name.lower() != exercise_name.lower()]

    def update_exercise(self, exercise_name, new_exercise):
        for i, ex in enumerate(self.exercises):
            if ex.name.lower() == exercise_name.lower():
                self.exercises[i] = new_exercise
                return True
        return False

    def complete_exercise(self, exercise_name):
        exercise = next((ex for ex in self.exercises if ex.name.lower() == exercise_name.lower()), None)
        if exercise and exercise not in self.completed_exercises:
            self.completed_exercises.append(exercise)

    def display_routine(self):
        routine_str = f"\nروتین تمرینی: {self.name}\n"
        for exercise in self.exercises:
            routine_str += str(exercise) + "\n"
        return routine_str

    def display_progress(self):
        progress_str = f"\nپیشرفت برای روتین: {self.name}\n"
        for exercise in self.completed_exercises:
            progress_str += str(exercise) + " - انجام شده\n"
        return progress_str if self.completed_exercises else "هیچ تمرینی انجام نشده است."


def load_data():
    try:
        with open('workout_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            routines = []
            for routine_data in data['routines']:
                routine = WorkoutRoutine(routine_data['name'])
                for exercise_data in routine_data['exercises']:
                    exercise = Exercise(exercise_data['name'], exercise_data['duration'], exercise_data['repetitions'],
                                        exercise_data['description'])
                    routine.add_exercise(exercise)
                routine.completed_exercises = routine_data.get('completed_exercises', [])
                routines.append(routine)
            return routines, data['nutrition_tips']
    except FileNotFoundError:
        return [], []


def save_data(routines, nutrition_tips):
    data = {
        'routines': [{'name': routine.name, 'exercises': [
            {'name': ex.name, 'duration': ex.duration, 'repetitions': ex.repetitions, 'description': ex.description} for
            ex in routine.exercises],
                      'completed_exercises': [ex.name for ex in routine.completed_exercises]} for routine in routines],
        'nutrition_tips': nutrition_tips
    }
    with open('workout_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def add_exercise():
    routine_name = simpledialog.askstring("نام روتین", "نام روتین را وارد کنید:")
    exercise_name = simpledialog.askstring("نام تمرین", "نام تمرین را وارد کنید:")
    duration = simpledialog.askinteger("مدت زمان", "مدت زمان تمرین (دقیقه) را وارد کنید:")
    repetitions = simpledialog.askinteger("تعداد تکرار", "تعداد تکرار را وارد کنید:")
    description = simpledialog.askstring("توضیحات", "توضیحات را وارد کنید:")

    if routine_name and exercise_name:
        routine = next((r for r in routines if r.name == routine_name), None)
        if routine:
            exercise = Exercise(exercise_name, duration, repetitions, description)
            routine.add_exercise(exercise)
            save_data(routines, nutrition_tips)
            messagebox.showinfo("موفقیت", "تمرین با موفقیت اضافه شد.")
        else:
            messagebox.showerror("خطا", "روتینی با این نام وجود ندارد.")


def remove_exercise():
    routine_name = simpledialog.askstring("نام روتین", "نام روتین را وارد کنید:")
    exercise_name = simpledialog.askstring("نام تمرین", "نام تمرین را وارد کنید:")

    if routine_name and exercise_name:
        routine = next((r for r in routines if r.name == routine_name), None)
        if routine:
            routine.remove_exercise(exercise_name)
            save_data(routines, nutrition_tips)
            messagebox.showinfo("موفقیت", "تمرین با موفقیت حذف شد.")
        else:
            messagebox.showerror("خطا", "روتینی با این نام وجود ندارد.")


def update_exercise():
    routine_name = simpledialog.askstring("نام روتین", "نام روتین را وارد کنید:")
    exercise_name = simpledialog.askstring("نام تمرین", "نام تمرین را وارد کنید:")

    if routine_name and exercise_name:
        routine = next((r for r in routines if r.name == routine_name), None)
        if routine:
            new_exercise_name = simpledialog.askstring("نام جدید تمرین", "نام جدید تمرین را وارد کنید:")
            new_duration = simpledialog.askinteger("مدت زمان جدید", "مدت زمان تمرین (دقیقه) را وارد کنید:")
            new_repetitions = simpledialog.askinteger("تعداد تکرار جدید", "تعداد تکرار را وارد کنید:")
            new_description = simpledialog.askstring("توضیحات جدید", "توضیحات را وارد کنید:")

            new_exercise = Exercise(new_exercise_name, new_duration, new_repetitions, new_description)
            if routine.update_exercise(exercise_name, new_exercise):
                save_data(routines, nutrition_tips)
                messagebox.showinfo("موفقیت", "تمرین با موفقیت ویرایش شد.")
            else:
                messagebox.showerror("خطا", "تمرینی با این نام وجود ندارد.")
        else:
            messagebox.showerror("خطا", "روتینی با این نام وجود ندارد.")


def add_nutrition_tip():
    tip = simpledialog.askstring("نکته تغذیه", "نکته تغذیه جدید را وارد کنید:")
    if tip:
        nutrition_tips.append(tip)
        save_data(routines, nutrition_tips)
        messagebox.showinfo("موفقیت", "نکته تغذیه با موفقیت اضافه شد.")


def search_exercise():
    search_term = simpledialog.askstring("جستجو", "نام تمرین را وارد کنید:")
    results = []
    for routine in routines:
        for exercise in routine.exercises:
            if search_term.lower() in exercise.name.lower():
                results.append(f"{routine.name}: {exercise}")

    if results:
        messagebox.showinfo("نتایج جستجو", "\n".join(results))
    else:
        messagebox.showinfo("نتایج جستجو", "تمرینی یافت نشد.")


def show_routines():
    routines_display = ""
    for routine in routines:
        routines_display += routine.display_routine()
    messagebox.showinfo("روتین‌های تمرینی", routines_display)


def show_nutrition_tips():
    tips_display = "\n".join(nutrition_tips)
    messagebox.showinfo("نکات تغذیه‌ای", tips_display)


def complete_exercise():
    routine_name = simpledialog.askstring("نام روتین", "نام روتین را وارد کنید:")
    exercise_name = simpledialog.askstring("نام تمرین", "نام تمرین را وارد کنید:")

    if routine_name and exercise_name:
        routine = next((r for r in routines if r.name == routine_name), None)
        if routine:
            routine.complete_exercise(exercise_name)
            save_data(routines, nutrition_tips)
            messagebox.showinfo("موفقیت", "تمرین با موفقیت انجام شد.")
        else:
            messagebox.showerror("خطا", "روتینی با این نام وجود ندارد.")


def show_progress():
    routine_name = simpledialog.askstring("نام روتین", "نام روتین را وارد کنید:")

    if routine_name:
        routine = next((r for r in routines if r.name == routine_name), None)
        if routine:
            progress = routine.display_progress()
            messagebox.showinfo("پیشرفت تمرینی", progress)
        else:
            messagebox.showerror("خطا", "روتینی با این نام وجود ندارد.")


def main():
    global routines, nutrition_tips
    routines, nutrition_tips = load_data()

    # How to Use:
    # 1. Add Exercises: Enter details when prompted.
    # 2. Remove Exercises: Select a routine and exercise to delete it.
    # 3. Update Exercises: Change details of an existing exercise.
    # 4. Mark Exercises as Completed: Select a routine and exercise to mark it as done.
    # 5. View Progress: Check completed exercises for a routine.
    # 6. View Routines: Display all routines and exercises.
    # 7. View Nutrition Tips: Show all nutrition tips.
    # 8. Search for Exercises: Find exercises by name.
    # 9. Exit the Application: Close the program safely.

    # GUI Setup
    root = tk.Tk()
    root.title("برنامه تمرینات ورزشی")
    root.configure(bg="#f0f0f0")

    frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
    frame.pack(pady=20)

    logo = PhotoImage(file="fitness_logo.png")  # نام فایل آیکون شما
    logo_label = tk.Label(frame, image=logo, bg="#f0f0f0")
    logo_label.pack()

    btn_routines = tk.Button(frame, text="نمایش روتین‌های تمرینی", command=show_routines, bg="#4CAF50", fg="white",
                             width=25)
    btn_routines.pack(padx=10, pady=5)

    btn_tips = tk.Button(frame, text="نمایش نکات تغذیه‌ای", command=show_nutrition_tips, bg="#2196F3", fg="white",
                         width=25)
    btn_tips.pack(padx=10, pady=5)

    btn_add_exercise = tk.Button(frame, text="اضافه کردن تمرین", command=add_exercise, bg="#FFC107", fg="white",
                                 width=25)
    btn_add_exercise.pack(padx=10, pady=5)

    btn_remove_exercise = tk.Button(frame, text="حذف تمرین", command=remove_exercise, bg="#FF5722", fg="white",
                                    width=25)
    btn_remove_exercise.pack(padx=10, pady=5)

    btn_update_exercise = tk.Button(frame, text="ویرایش تمرین", command=update_exercise, bg="#9C27B0", fg="white",
                                    width=25)
    btn_update_exercise.pack(padx=10, pady=5)

    btn_add_nutrition_tip = tk.Button(frame, text="اضافه کردن نکته تغذیه", command=add_nutrition_tip, bg="#3F51B5",
                                      fg="white", width=25)
    btn_add_nutrition_tip.pack(padx=10, pady=5)

    btn_search_exercise = tk.Button(frame, text="جستجوی تمرین", command=search_exercise, bg="#FF9800", fg="white",
                                    width=25)
    btn_search_exercise.pack(padx=10, pady=5)

    btn_complete_exercise = tk.Button(frame, text="علامت‌گذاری تمرین به عنوان انجام‌شده", command=complete_exercise,
                                      bg="#8BC34A", fg="white", width=25)
    btn_complete_exercise.pack(padx=10, pady=5)

    btn_show_progress = tk.Button(frame, text="نمایش پیشرفت", command=show_progress, bg="#FFC107", fg="white", width=25)
    btn_show_progress.pack(padx=10, pady=5)

    btn_exit = tk.Button(frame, text="خروج", command=root.quit, bg="#f44336", fg="white", width=25)
    btn_exit.pack(padx=10, pady=5)

    root.mainloop()

    # ذخیره داده‌ها هنگام خروج
    save_data(routines, nutrition_tips)


if __name__ == "__main__":
    main()
