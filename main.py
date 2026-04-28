import flet as ft
import json
import os

DATA_FILE = "data.json"

products = {
    "chicken": {"cal": 150, "p": 25, "f": 10, "c": 2},
    "rice": {"cal": 370, "p": 8, "f": 1, "c": 85},
    "pasta": {"cal": 350, "p": 12, "f": 2, "c": 70},
    "buckwheat": {"cal": 350, "p": 13, "f": 2, "c": 70},
    "tuna": {"cal": 100, "p": 25, "f": 3, "c": 0},
    "yoghurt": {"cal": 670, "p": 28, "f": 26, "c": 70},
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"cal": 0, "p": 0, "f": 0, "c": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def main(page: ft.Page):
    page.title = "My Food"
    page.theme_mode = ft.ThemeMode.DARK

    total = load_data()
    current_product = {"name": None}

    result_text = ft.Text(size=20)

    def update_ui():
        result_text.value = f"Kcal: {int(total['cal'])}  P: {int(total['p'])}  F: {int(total['f'])}  C: {int(total['c'])}"
        page.update()

    update_ui()

    grams_input = ft.TextField(label="Grams", keyboard_type=ft.KeyboardType.NUMBER)

    def confirm(e):
        try:
            grams = int(grams_input.value)
            data = products[current_product["name"]]

            total["cal"] += data["cal"] * grams / 100
            total["p"] += data["p"] * grams / 100
            total["f"] += data["f"] * grams / 100
            total["c"] += data["c"] * grams / 100

            save_data(total)
            update_ui()

            sheet.open = False
            page.update()

        except:
            grams_input.value = "Error"
            page.update()

    # ✅ BottomSheet вместо Dialog
    sheet = ft.BottomSheet(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Enter grams", size=20),
                    grams_input,
                    ft.ElevatedButton("Add", on_click=confirm),
                ],
                tight=True,
            ),
            padding=20,
        ),
        open=False,
    )

    page.overlay.append(sheet)

    def add_food(product_name):
        current_product["name"] = product_name
        grams_input.value = ""
        sheet.open = True
        page.update()

    def reset(e):
        total["cal"] = 0
        total["p"] = 0
        total["f"] = 0
        total["c"] = 0
        save_data(total)
        update_ui()

    page.add(
        ft.Column(
            [
                ft.Text("My Food", size=30),

                ft.Row([
                    ft.ElevatedButton("Chicken", on_click=lambda e: add_food("chicken")),
                    ft.ElevatedButton("Rice", on_click=lambda e: add_food("rice")),
                ]),

                ft.Row([
                    ft.ElevatedButton("Pasta", on_click=lambda e: add_food("pasta")),
                    ft.ElevatedButton("Buckwheat", on_click=lambda e: add_food("buckwheat")),
                ]),

                ft.Row([
                    ft.ElevatedButton("Tuna", on_click=lambda e: add_food("tuna")),
                    ft.ElevatedButton("Yoghurt", on_click=lambda e: add_food("yoghurt")),
                ]),

                result_text,

                ft.ElevatedButton("RESET", on_click=reset),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


import flet as ft
import json
import os

DATA_FILE = "data.json"

products = {
    "chicken": {"cal": 150, "p": 25, "f": 10, "c": 2},
    "rice": {"cal": 370, "p": 8, "f": 1, "c": 85},
    "pasta": {"cal": 350, "p": 12, "f": 2, "c": 70},
    "buckwheat": {"cal": 350, "p": 13, "f": 2, "c": 70},
    "tuna": {"cal": 100, "p": 25, "f": 3, "c": 0},
    "yoghurt": {"cal": 670, "p": 28, "f": 26, "c": 70},
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"cal": 0, "p": 0, "f": 0, "c": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def main(page: ft.Page):
    page.title = "My Food"
    page.theme_mode = ft.ThemeMode.DARK

    total = load_data()

    result_text = ft.Text(
        f"Kcal: {int(total['cal'])}  P: {int(total['p'])}  F: {int(total['f'])}  C: {int(total['c'])}",
        size=20,
    )

    def update_ui():
        result_text.value = f"Kcal: {int(total['cal'])}  P: {int(total['p'])}  F: {int(total['f'])}  C: {int(total['c'])}"
        page.update()

    def add_food(product_name):
        grams_input = ft.TextField(label=f"Grams of {product_name}", keyboard_type=ft.KeyboardType.NUMBER)

        def confirm(e):
            try:
                grams = int(grams_input.value)
                data = products[product_name]

                total["cal"] += data["cal"] * grams / 100
                total["p"] += data["p"] * grams / 100
                total["f"] += data["f"] * grams / 100
                total["c"] += data["c"] * grams / 100

                save_data(total)
                update_ui()
                dialog.open = False
                page.update()
            except:
                grams_input.value = "Error"
                page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Enter grams"),
            content=grams_input,
            actions=[
                ft.TextButton("Add", on_click=confirm)
            ]
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    def reset(e):
        total["cal"] = 0
        total["p"] = 0
        total["f"] = 0
        total["c"] = 0
        save_data(total)
        update_ui()

    # UI
    page.add(
        ft.Column(
            [
                ft.Text("My Food", size=30),

                ft.Row([
                    ft.ElevatedButton("Chicken", on_click=lambda e: add_food("chicken")),
                    ft.ElevatedButton("Rice", on_click=lambda e: add_food("rice")),
                ]),

                ft.Row([
                    ft.ElevatedButton("Pasta", on_click=lambda e: add_food("pasta")),
                    ft.ElevatedButton("Buckwheat", on_click=lambda e: add_food("buckwheat")),
                ]),

                ft.Row([
                    ft.ElevatedButton("Tuna", on_click=lambda e: add_food("tuna")),
                    ft.ElevatedButton("Yoghurt", on_click=lambda e: add_food("yoghurt")),
                ]),

                result_text,

                ft.ElevatedButton("RESET", on_click=reset, color="red"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


ft.app(target=main)