from pathlib import Path
p=Path('/tmp/src/PreBattle.gd')
s=p.read_text()

old='''var decision_timer_label: Label\nvar rps_revealing: bool = false\n'''
new='''var decision_timer_label: Label\nvar decision_timer_bar: ColorRect = null\nvar decision_timer_bar_max_width: float = 0.0\nvar rps_revealing: bool = false\n'''
assert old in s
s=s.replace(old,new,1)

old='''\t\tif urgent != decision_timer_last_urgent:\n\t\t\tdecision_timer_last_urgent = urgent\n\t\t\tdecision_timer_label.add_theme_color_override("font_color", Color("ef6659") if urgent else Color("f0d25e"))\n\tif decision_time_left <= 0.0:\n'''
new='''\t\tif urgent != decision_timer_last_urgent:\n\t\t\tdecision_timer_last_urgent = urgent\n\t\t\tdecision_timer_label.add_theme_color_override("font_color", Color("ef6659") if urgent else Color("f0d25e"))\n\tif is_instance_valid(decision_timer_bar):\n\t\tvar timer_ratio: float = clampf(decision_time_left / PREBATTLE_TIMER_SECONDS, 0.0, 1.0)\n\t\tdecision_timer_bar.size.x = decision_timer_bar_max_width * timer_ratio\n\t\tdecision_timer_bar.color = Color("ef6659") if decision_time_left <= 8.0 else Color("e7c85a")\n\tif decision_time_left <= 0.0:\n'''
assert old in s
s=s.replace(old,new,1)

start=s.index('func _timer_badge(parent: Node, rect: Rect2, context: String) -> void :')
end=s.index('\nfunc _on_prebattle_timeout', start)
new_func='''func _timer_badge(parent: Node, rect: Rect2, context: String) -> void :\n\tvar badge: Panel = _panel(parent, rect, Color(0.006, 0.018, 0.032, 0.74), Color(0.91, 0.78, 0.34, 0.82), 18, 9)\n\t_label(badge, "TEMPS RESTANT", Rect2(10, 5, rect.size.x - 20, 15), 8, Color("a9b7c5"), HORIZONTAL_ALIGNMENT_CENTER, true)\n\tdecision_timer_label = _label(badge, "%02d" % int(ceil(decision_time_left if decision_timer_active else PREBATTLE_TIMER_SECONDS)), Rect2(8, 17, rect.size.x - 16, 32), 24, Color("f0d25e"), HORIZONTAL_ALIGNMENT_CENTER, true)\n\tvar track: ColorRect = ColorRect.new()\n\ttrack.position = Vector2(15, rect.size.y - 11)\n\ttrack.size = Vector2(rect.size.x - 30, 3)\n\ttrack.color = Color(0.42, 0.50, 0.58, 0.24)\n\ttrack.mouse_filter = Control.MOUSE_FILTER_IGNORE\n\tbadge.add_child(track)\n\tdecision_timer_bar = ColorRect.new()\n\tdecision_timer_bar.position = track.position\n\tdecision_timer_bar_max_width = track.size.x\n\tdecision_timer_bar.size = Vector2(decision_timer_bar_max_width, 3)\n\tdecision_timer_bar.color = Color("e7c85a")\n\tdecision_timer_bar.mouse_filter = Control.MOUSE_FILTER_IGNORE\n\tbadge.add_child(decision_timer_bar)\n\tif not decision_timer_active or decision_context != context:\n\t\t_start_decision_timer(context)\n\t\tdecision_timer_label.text = "%02d" % int(PREBATTLE_TIMER_SECONDS)\n\tdecision_timer_bar.size.x = decision_timer_bar_max_width\n'''
s=s[:start]+new_func+s[end:]

old='''\tvar header: Panel = _glass_surface(self, Rect2(22, 16, 1556, 66), 20, 0.1, 0.44, 10)\n\theader.z_index = 30\n\t_logo_in_panel(header, Vector2(22, 13), 38)\n\t_label(header, "YUGITO", Rect2(72, 8, 160, 42), 26, Color("ffffff"), HORIZONTAL_ALIGNMENT_LEFT, true)\n\t_label(header, "PRÉPARATION DU COMBAT", Rect2(224, 13, 280, 20), 8, Color("f3f9fd"), HORIZONTAL_ALIGNMENT_LEFT, true)\n\ttitle_label = _label(header, "SHIFUMI", Rect2(540, 8, 470, 42), 20, Color("ffffff"), HORIZONTAL_ALIGNMENT_CENTER, true)\n\tvar cancel_btn: Button = _button(header, Rect2(1392, 12, 138, 40), "ANNULER", Color("f3a9b5"), false)\n\tcancel_btn.pressed.connect( func() -> void : cancelled.emit())\n'''
new='''\tvar header: Panel = _panel(self, Rect2(22, 16, 1556, 66), Color(0.006, 0.018, 0.032, 0.34), Color(0.72, 0.86, 0.96, 0.34), 20, 10)\n\theader.z_index = 30\n\t_logo_in_panel(header, Vector2(22, 13), 38)\n\t_label(header, "YUGITO", Rect2(72, 7, 150, 42), 26, Color("ffffff"), HORIZONTAL_ALIGNMENT_LEFT, true)\n\tvar prep_line: ColorRect = ColorRect.new()\n\tprep_line.position = Vector2(224, 20)\n\tprep_line.size = Vector2(3, 22)\n\tprep_line.color = Color(0.86, 0.16, 0.20, 0.78)\n\tprep_line.mouse_filter = Control.MOUSE_FILTER_IGNORE\n\theader.add_child(prep_line)\n\t_label(header, "PRÉPARATION DU COMBAT", Rect2(238, 16, 250, 28), 9, Color("c8d5e0"), HORIZONTAL_ALIGNMENT_LEFT, true)\n\tvar phase_pill: Panel = _panel(header, Rect2(570, 10, 416, 46), Color(0.008, 0.024, 0.042, 0.34), Color(0.68, 0.84, 0.95, 0.28), 16, 3)\n\ttitle_label = _label(phase_pill, "SHIFUMI", Rect2(14, 1, 388, 44), 19, Color("f7fbff"), HORIZONTAL_ALIGNMENT_CENTER, true)\n\tvar cancel_btn: Button = _button(header, Rect2(1384, 11, 146, 42), "ANNULER", Color("ef7880"), false)\n\tcancel_btn.add_theme_font_size_override("font_size", 11)\n\tcancel_btn.pressed.connect( func() -> void : cancelled.emit())\n'''
assert old in s
s=s.replace(old,new,1)

old='''\t_timer_badge(stage_root, Rect2(1430, 28, 92, 54), "rps")\n'''
new='''\t_timer_badge(stage_root, Rect2(1388, 22, 134, 68), "rps")\n'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)
print('V4 patch applied, chars=',len(s))
