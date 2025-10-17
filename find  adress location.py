import webbrowser


def search_location():

    address = input("لطفاً آدرس مورد نظر خود را وارد کنید: ")


    search_url = f"https://www.google.com/maps/search/?api=1&query={address.replace(' ', '+')}"


    webbrowser.open(search_url)


if __name__ == "__main__":
    search_location()
