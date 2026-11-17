import flet as ft
from src.services.audio_service import AudioService
from src.services.theme_service import get_theme_by_name, load_themes
from src.ui.screens.home_screen import HomeScreen
from src.ui.screens.search_screen import SearchScreen
from src.ui.screens.player_screen import PlayerScreen
from src.ui.widgets.theme_picker import ThemePicker

def main(page: ft.Page):
    page.title = "VIBRALYS"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # TARGET 5: Kunci ukuran HP portrait biar di laptop pun keliatan HP
    page.window_width = 400
    page.window_height = 800
    page.window_resizable = False
    page.padding = 0
    page.spacing = 0

    themes = load_themes()
    current_theme = themes[0] if themes else {"bg":"#121212","card":"#1E1E1E","primary":"#1DB954","text":"#FFFFFF","nav":"#1E1E1E"}
    current_song = None
    audio = AudioService(page)

    content_area = ft.Container(expand=True, padding=0)

    def apply_theme(theme_name):
        nonlocal current_theme
        new_theme = get_theme_by_name(theme_name)
        if new_theme:
            current_theme = new_theme
            page.bgcolor = current_theme["bg"]
            # Re-render current screen biar warna ikut ganti
            if nav_bar.selected_index == 0:
                render_home()
            elif nav_bar.selected_index == 1:
                render_search()
            else:
                render_player()
            page.update()

    def on_play_song(song):
        nonlocal current_song
        current_song = song
        content_area.content = PlayerScreen(page, audio, current_theme, song)
        nav_bar.selected_index = 2
        page.update()

    def render_home():
        content_area.content = HomeScreen(page, audio, current_theme, on_play_song)
        page.update()

    def render_search():
        content_area.content = SearchScreen(page, audio, current_theme, on_play_song)
        page.update()

    def render_player():
        content_area.content = PlayerScreen(page, audio, current_theme, current_song)
        page.update()

    def nav_change(e):
        idx = e.control.selected_index
        if idx == 0: render_home()
        elif idx == 1: render_search()
        elif idx == 2: render_player()

    page.bgcolor = current_theme["bg"]
    theme_picker = ThemePicker(apply_theme, current_theme["name"])
    
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.HOME_OUTLINED, selected_icon=ft.icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.icons.SEARCH_OUTLINED, selected_icon=ft.icons.SEARCH, label="Search"),
            ft.NavigationBarDestination(icon=ft.icons.MUSIC_NOTE_OUTLINED, selected_icon=ft.icons.MUSIC_NOTE, label="Player"),
        ],
        on_change=nav_change,
        bgcolor=current_theme["nav"],
        indicator_color=current_theme["primary"],
        selected_index=0
    )

    header = ft.Container(
        content=ft.Row([
            ft.Text("VIBRALYS", weight=ft.FontWeight.BOLD, color=current_theme["primary"], size=18),
            theme_picker
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        bgcolor=current_theme["card"]
    )

    page.add(
        ft.Column([
            header,
            ft.Divider(height=1, thickness=1, opacity=0.1),
            content_area,
            nav_bar
        ], expand=True, spacing=0)
    )
    
    render_home()

ft.app(target=main)