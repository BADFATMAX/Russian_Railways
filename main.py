import flet as ft
from editor import create_editor_tab
from history import create_history_tab
from joint_mode import create_joint_mode_tab
from story_game import create_story_game_tab
from rhythm_game import create_rhythm_game_tab
from training_cards import create_training_cards_tab
from verification import create_verification_tab
from documentation import create_documentation_tab
from leaderboard import create_leaderboard_tab
from admin_panel import create_admin_panel_tab

def main(page: ft.Page):
    page.title = "Flet Mode Tabs"

    editor_tab = create_editor_tab()
    history_tab = create_history_tab()
    joint_mode_tab = create_joint_mode_tab()
    story_game_tab = create_story_game_tab()
    rhythm_game_tab = create_rhythm_game_tab()
    training_cards_tab = create_training_cards_tab()
    verification_tab = create_verification_tab()
    documentation_tab = create_documentation_tab()
    leaderboard_tab = create_leaderboard_tab()
    admin_panel_tab = create_admin_panel_tab()
    

    tabs = ft.Tabs(
        tabs=[
            editor_tab,
            history_tab,
            joint_mode_tab,
            story_game_tab,
            rhythm_game_tab,
            training_cards_tab,
            verification_tab,
            documentation_tab,
            leaderboard_tab,
            admin_panel_tab,
        ],
        selected_index=0,
        animation_duration=300
    )

    page.add(tabs)

ft.app(target=main)
