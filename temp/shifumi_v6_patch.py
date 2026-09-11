from pathlib import Path
p=Path('/tmp/src/PreBattle.gd')
s=p.read_text()

# Give the locked state enough time to be visually perceived without slowing the flow much.
s=s.replace('const RPS_REVEAL_DELAY: float = 0.42','const RPS_REVEAL_DELAY: float = 0.75',1)

# Do not restart/show the countdown once the player's choice is locked.
old='''\t_label(stage_root, subtitle, Rect2(330, 74, 900, 30), 13, Color("bed0dc"), HORIZONTAL_ALIGNMENT_CENTER, false)\n\t_rps_timer_dock(stage_root, Rect2(260, 642, 1044, 72))\n\n\tif rps_player_choice.is_empty():\n'''
new='''\t_label(stage_root, subtitle, Rect2(330, 74, 900, 30), 13, Color("bed0dc"), HORIZONTAL_ALIGNMENT_CENTER, false)\n\n\tif rps_player_choice.is_empty():\n\t\t_rps_timer_dock(stage_root, Rect2(260, 642, 1044, 72))\n'''
assert old in s
s=s.replace(old,new,1)

# Replace the waiting state by a stronger selected/locked feedback state.
start=s.index('func _draw_rps_wait() -> void :')
end=s.index('\nfunc _animate_rps_choice_card', start)
new_wait='''func _draw_rps_wait() -> void :\n\tvar selected_accent: Color = Color("ef6659")\n\tif rps_player_choice == "feuille":\n\t\tselected_accent = Color("55d58b")\n\telif rps_player_choice == "ciseaux":\n\t\tselected_accent = Color("58aff0")\n\n\t_label(stage_root, "CHOIX VERROUILLÉ", Rect2(360, 130, 844, 38), 22, selected_accent.lightened(0.14), HORIZONTAL_ALIGNMENT_CENTER, true)\n\t_label(stage_root, "Ton signe est enregistré • Révélation simultanée dans un instant", Rect2(330, 166, 904, 24), 10, Color("a9bac7"), HORIZONTAL_ALIGNMENT_CENTER, false)\n\n\tvar ally_panel: Panel = _result_card(Rect2(312, 210, 380, 300), "TON CHOIX", rps_player_choice, selected_accent)\n\tvar lock_badge: Panel = _panel(ally_panel, Rect2(88, 246, 204, 34), Color(selected_accent.r * 0.12, selected_accent.g * 0.12, selected_accent.b * 0.12, 0.92), Color(selected_accent.r, selected_accent.g, selected_accent.b, 0.88), 12, 5)\n\t_label(lock_badge, "VERROUILLÉ", Rect2(10, 2, 184, 28), 11, Color("f7fbff"), HORIZONTAL_ALIGNMENT_CENTER, true)\n\n\tvar enemy_panel: Panel = _panel(stage_root, Rect2(872, 210, 380, 300), Color(0.012, 0.028, 0.048, 0.92), Color(0.36, 0.47, 0.58, 0.46), 22, 9)\n\t_label(enemy_panel, "IA", Rect2(22, 30, 336, 32), 17, Color("d5dde5"), HORIZONTAL_ALIGNMENT_CENTER, true)\n\tvar hidden_frame: Panel = _panel(enemy_panel, Rect2(48, 78, 284, 128), Color(0.004, 0.014, 0.025, 0.86), Color(0.34, 0.44, 0.55, 0.32), 16, 3)\n\t_label(hidden_frame, "?", Rect2(20, 12, 244, 76), 48, Color("7990a5"), HORIZONTAL_ALIGNMENT_CENTER, true)\n\t_label(hidden_frame, "CHOIX CACHÉ", Rect2(20, 82, 244, 28), 10, Color("8fa4b7"), HORIZONTAL_ALIGNMENT_CENTER, true)\n\t_label(enemy_panel, "L'IA a verrouillé son signe", Rect2(28, 224, 324, 28), 10, Color("70869a"), HORIZONTAL_ALIGNMENT_CENTER, false)\n\n\t_label(stage_root, "VS", Rect2(705, 316, 154, 52), 28, Color("73869a"), HORIZONTAL_ALIGNMENT_CENTER, true)\n\t_animate_result_panel(ally_panel, Vector2(-70, 0))\n\t_animate_result_panel(enemy_panel, Vector2(70, 0))\n\n\tvar status_dock: Panel = _panel(stage_root, Rect2(260, 642, 1044, 72), Color(0.006, 0.018, 0.032, 0.82), Color(selected_accent.r, selected_accent.g, selected_accent.b, 0.42), 18, 6)\n\tvar pulse: ColorRect = ColorRect.new()\n\tpulse.position = Vector2(22, 20)\n\tpulse.size = Vector2(12, 32)\n\tpulse.color = selected_accent\n\tpulse.mouse_filter = Control.MOUSE_FILTER_IGNORE\n\tstatus_dock.add_child(pulse)\n\t_label(status_dock, "SIGNE VERROUILLÉ", Rect2(50, 10, 260, 24), 11, selected_accent.lightened(0.12), HORIZONTAL_ALIGNMENT_LEFT, true)\n\t_label(status_dock, "Révélation simultanée…", Rect2(50, 34, 420, 22), 10, Color("d4e0e8"), HORIZONTAL_ALIGNMENT_LEFT, false)\n\t_label(status_dock, "L'adversaire ne voit pas ton choix avant la révélation", Rect2(480, 24, 536, 24), 9, Color("879bad"), HORIZONTAL_ALIGNMENT_RIGHT, false)\n\tvar tw: Tween = pulse.create_tween().set_loops(3)\n\ttw.tween_property(pulse, "modulate:a", 0.35, 0.12)\n\ttw.tween_property(pulse, "modulate:a", 1.0, 0.12)\n\tfooter.text = "Ton choix est verrouillé • Révélation simultanée en cours"\n'''
s=s[:start]+new_wait+s[end:]

p.write_text(s)
print('V6 patch applied, chars=',len(s))
