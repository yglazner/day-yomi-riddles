import toga


def button_handler(widget):
    print("hello")


def build(app):
    box = toga.Box()
    toga.Text
    button = toga.Button("Hello world", on_press=button_handler)
    button.style.padding = 50
    button.style.flex = 1
    box.add(button)
    button = toga.Button("Hello world", on_press=button_handler)
    button.style.padding = 50
    button.style.flex = 1
    box.add(button)

    return box


def main():
    return toga.App("Daf Yomi Riddles", "org.yoavglazner.daftomiriddles", startup=build)


if __name__ == "__main__":
    main().main_loop()
