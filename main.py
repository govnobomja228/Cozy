from aiogram import bot
import flet as ft
import asyncio
from data_base import *

bot = bot(token='7246774026:AAGZ-ZQ2LAqlYT3snykLCWe6Cx-pF6p_8HI')
DATABASE_PATH = 'database.db'
user_id = 0
url_ref = "CookiesClickerGameBot"


async def main(page: ft.Page) -> None:
    init_db()
    page.bgcolor = "#000000"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {"appetite-italic": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf"}
    page.theme = ft.Theme(font_family="appetite-italic")
    user_id_holder = {"value": 0}

    user_id_input = ft.TextField(label="Enter your user ID", autofocus=True)
    submit_button = ft.TextButton(text="Submit")

    
    score_text = ft.Text(value="", size=20, color="#ffb700")
    energy_text = ft.Text(value="", size=15, color="#00FFFF")

    async def restore_energy():
        while True:
            await asyncio.sleep(40)  
            
            for user_id in get_all_user_ids():  
                score, energy = get_game_data(user_id)
                energy += 1
                if energy > 5000:  
                    energy = 5000
                update_game_data(user_id, score, energy) 

    async def submit_click(event):
        user_id = int(user_id_input.value)  
        user_id_holder["value"] = user_id  
        
        score, energy = get_game_data(user_id)
        print("Score:", score, "Energy:", energy)  
        score_text.value = f"Score: {score}"
        energy_text.value = f"Energy: {energy}"

        page.remove(user_id_input)
        page.remove(submit_button)

        
        page.add(score_text, energy_text)

       
        await page.update()

    submit_button.on_click = submit_click

   
    page.add(user_id_input, submit_button)

    async def handle_click(event: ft.ContainerTapEvent) -> None:
        nonlocal score_text, energy_text
        user_id = user_id_holder["value"]
        score, energy = get_game_data(user_id)
        if energy > 0:
            score += 1
            energy -= 1

            score_text.value = "{:.2f}".format(score)
            energy_text.value = f"Energy: {energy}"
            energy_progress_bar_fg.width = 250 * (energy / 5000)

            await page.update_async()
            await asyncio.sleep(0.1)
            clickable_image.scale = 0.95
            await page.update_async()
            await asyncio.sleep(0.1)
            clickable_image.scale = 1.0
            await page.update_async()

            
            update_game_data(user_id, score, energy)
            print("Score updated to:", score, "Energy updated to:", energy)  # Отладочное сообщение

            
            await page.update()

    async def handle_ref_button(event: ft.TapEvent) -> None:
       
        ref_link = f"https://t.me/{url_ref}?start={user_id_holder['value']}"
        print("Referral link:", ref_link)  # Выводим ссылку в консоль

    
        ref_link_text = ft.Text(value=ref_link, selectable=True)

        
        async def remove_elements(event: ft.TapEvent):
            page.remove(stack) 
            await page.update()

        
        remove_button = ft.TextButton(text="Remove", on_click=remove_elements)

        
        remove_button_row = ft.Row(controls=[remove_button], alignment=ft.MainAxisAlignment.CENTER)

        
        container = ft.Container(
            content=ft.Column(controls=[ref_link_text, remove_button_row], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ft.colors.WHITE,
            border_radius=10
        )

        
        stack = ft.Stack(controls=[container])

        
        page.add(stack)
        await page.update()

    async def show_leaderboard(event: ft.TapEvent) -> None:
        top_users = await get_top_users(10) 
        user_score_texts = [ft.Text(value=f"User ID: {user_id}, Score: {score:.2g}", color=ft.colors.WHITE) for user_id, score in top_users]

        async def close_leaderboard(event: ft.TapEvent) -> None:
            page.remove(stack)  
            await page.update()

        
        leaderboard_container = ft.Container(
            content=ft.Column(controls=user_score_texts, alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ft.colors.BLACK,
            border_radius=10
        )

        
        close_button = ft.TextButton(text="Close", on_click=close_leaderboard)

        
        container_with_close_button = ft.Column(controls=[leaderboard_container, close_button])

        
        stack = ft.Stack(controls=[container_with_close_button])

    
        page.add(stack)
        await page.update()

    score, energy = get_game_data(user_id)
    score_text.value = "{:.2f}".format(score)
    energy_text.value = f"Energy: {energy}"

    leaderboard_button = ft.TextButton(text="Leaderboard", on_click=show_leaderboard)
    ref_button = ft.TextButton(text="Referral Link", on_click=handle_ref_button)

    buttons_row = ft.Row(controls=[leaderboard_button, ref_button], alignment=ft.MainAxisAlignment.CENTER)

    page.add(buttons_row)

    
    energy_text = ft.Text(value=f"Energy: {energy}", size=15, color="#00FFFF")

    energy_progress_bar_bg = ft.Container(
        height=10,
        width=250,
        bgcolor="#000000",
        margin=ft.Margin(top=30, right=0, left=15, bottom=-20)  # Сдвигаем влево на 50 пикселей
    )

    
    energy_progress_bar_fg = ft.Container(
        height=10,
        width=250 * (energy / 50),
        bgcolor="#FFFF00",
        margin=ft.Margin(top=30, right=0, left=15, bottom=-20),  # Сдвигаем влево на 50 пикселей

    )

    
    progress_bar_stack = ft.Stack(controls=[energy_progress_bar_bg, energy_progress_bar_fg])

    
    clickable_image = ft.Image(src="cookies.png", fit=ft.ImageFit.CONTAIN, width=300, height=300)
    image_container = ft.Container(content=clickable_image, on_click=handle_click, margin=ft.Margin(top=50, right=0, left=0, bottom=0))
    page.add(image_container)

    
    progress_bar_container = ft.Container(
        content=ft.Stack(controls=[energy_progress_bar_bg, energy_progress_bar_fg]),

        margin=ft.Margin(top=0, left=0, bottom=0, right=0),
        

    )

    
    column = ft.Column(
        controls=[progress_bar_stack],
        expand=True,
    )

    
    page.add(column)


    # Additional elements such as buttons, leaderboard, and referral link are already added
    page.clickable_image = clickable_image
    page.energy_progress_bar_fg = energy_progress_bar_fg

    asyncio.create_task(restore_energy())

if __name__ == "__main__":
    #ft.app(target=main, view=None, port=3001)
    ft.app(target=main, view=ft.WEB_BROWSER)
