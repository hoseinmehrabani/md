from googlesearch import search

def google_search(query, num_results):
    results = []
    for result in search(query, num_results=num_results):
        results.append(result)
    return results

def save_results_to_file(results, filename):
    with open(filename, 'w') as file:
        for result in results:
            file.write(result + '\n')

def main():
    query = input("لطفا موضوع جستجو را وارد کنید: ")
    search_type = input("به دنبال چه چیزی هستید؟ (1: کانال آپارات، 2: چنل یوتیوب، 3: سایت): ")

    num_results = 10  # تعداد نتایج برای هر جستجو

    if search_type == '1':
        full_query = f"{query} site:aparat.com"
        search_label = "کانال های آپارات"
    elif search_type == '2':
        full_query = f"{query} site:youtube.com"
        search_label = "چنل های یوتیوب"
    elif search_type == '3':
        full_query = query
        search_label = "سایت های مرتبط"
    else:
        print("انتخاب نامعتبر. لطفاً دوباره امتحان کنید.")
        return

    results = google_search(full_query, num_results)

    # نمایش نتایج در کنسول
    print(f"\nنتایج جستجو برای '{search_label}':")
    for idx, result in enumerate(results, start=1):
        print(f"{idx}. {result}")

    # ذخیره نتایج در فایل
    filename = f"search_results_{search_label.replace(' ', '_')}.txt"
    save_results_to_file(results, filename)
    print(f"\nنتایج '{search_label}' در فایل {filename} ذخیره شد.")

if __name__ == "__main__":
    main()
