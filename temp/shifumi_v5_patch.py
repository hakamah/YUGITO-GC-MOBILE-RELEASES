from pathlib import Path
p=Path('/tmp/src/PreBattle.gd')
s=p.read_text()

# RPS seconds display: keep plain seconds on draft/lineup, add "s" only on Shifumi.
old='''\t\tif shown_second != decision_timer_last_second:\n\t\t\tdecision_timer_last_second = shown_second\n\t\t\tdecision_timer_label.text = "%02d" % shown_second\n'''
new='''\t\tif shown_second != decision_timer_last_second:\n\t\t\tdecision_timer_last_second = shown_second\n\t\t\tdecision_timer_label.text = ("%02d s" % shown_second) if decision_context == "rps" else ("%02d" % shown_second)\n'''
assert old in s
s=s.replace(old,new,1)

# Add a dedicated premium bottom timer for Shifumi. Generic timer remains untouched for draft/lineup.
marker='''func _on_prebattle_timeout(context: String) -> void :\n'''
assert marker in s
rps_dock='''func _rps_timer_dock(parent: Node, rect: Rect2) -> void :\n\tvar dock: Panel = _panel(parent, rect, Color(0.006, 0.018, 0.032, 0.80), Color(0.72, 0.86, 0.96, 0.28), 18, 6)\n\tdock.mouse_filter = Control.MOUSE_FILTER_IGNORE\n\tvar time_box: Panel = _panel(dock, Rect2(10, 9, 204, rect.size.y - 18), Color(0.012, 0.03, 0.05, 0.72), Color(0.91, 0.78, 0.34, 0.38), 13, 2)\n\t_label(time_box, "TEMPS RESTANT", Rect2(14, 4, 176, 16), 9, Color("a9b7c5"), HORIZONTAL_ALIGNMENT_LEFT, true)\n\tdecision_timer_label = _label(time_box, "%02d s" % int(ceil(decision_time_left if decision_timer_active else PREBATTLE_TIMER_SECONDS)), Rect2(14, 18, 176, 28), 22, Color("f0d25e"), HORIZONTAL_ALIGNMENT_LEFT, true)\n\t_label(dock, "CHOISIS AVANT LA FIN DU TEMPS", Rect2(238, 8, rect.size.x - 260, 17), 8, Color("7f96aa"), HORIZONTAL_ALIGNMENT_LEFT, true)\n\tvar track: ColorRect = ColorRect.new()\n\ttrack.position = Vector2(238, 34)\n\ttrack.size = Vector2(rect.size.x - 264, 10)\n\ttrack.color = Color(0.42, 0.50, 0.58, 0.24)\n\ttrack.mouse_filter = Control.MOUSE_FILTER_IGNORE\n\tdock.add_child(track)\n\tdecision_timer_bar = ColorRect.new()\n\tdecision_timer_bar.position = track.position\n\tdecision_timer_bar_max_width = track.size.x\n\tdecision_timer_bar.size = Vector2(decision_timer_bar_max_width, 10)\n\tdecision_timer_bar.color = Color("e7c85a")\n\tdecision_timer_bar.mouse_filter = Control.MOUSE_FILTER_IGNORE\n\tdock.add_child(decision_timer_bar)\n\t_label(dock, "L'IA choisit en même temps • Révélation après verrouillage", Rect2(238, 49, rect.size.x - 264, 16), 8, Color("c7d5df"), HORIZONTAL_ALIGNMENT_LEFT, false)\n\tif not decision_timer_active or decision_context != "rps":\n\t\t_start_decision_timer("rps")\n\t\tdecision_timer_label.text = "%02d s" % int(PREBATTLE_TIMER_SECONDS)\n\tdecision_timer_bar.size.x = decision_timer_bar_max_width\n\n'''
s=s.replace(marker,rps_dock+marker,1)

# Bottom footer becomes a clean contextual status bar instead of a tiny single line.
old='''\tvar foot: Panel = _glass_surface(self, Rect2(22, 856, 1556, 30), 12, 0.08, 0.26, 3)\n\tfoot.z_index = 30\n\tfooter = _label(foot, "Shifumi → Draft → 3 Ninjas → Shifumi → Combat", Rect2(14, 3, 1510, 24), 8, Color("f4f9fc"), HORIZONTAL_ALIGNMENT_LEFT, false)\n'''
new='''\tvar foot: Panel = _glass_surface(self, Rect2(22, 850, 1556, 36), 12, 0.10, 0.28, 4)\n\tfoot.z_index = 30\n\t_label(foot, "YUGITO  •  PRÉPARATION", Rect2(16, 6, 250, 24), 8, Color("9bb1c2"), HORIZONTAL_ALIGNMENT_LEFT, true)\n\tfooter = _label(foot, "Shifumi → Draft → 3 Ninjas → Shifumi → Combat", Rect2(274, 6, 1258, 24), 8, Color("e9f2f8"), HORIZONTAL_ALIGNMENT_RIGHT, false)\n'''
assert old in s
s=s.replace(old,new,1)

# Move the Shifumi timer out of the right side and into the free lower area.
old='''\t_timer_badge(stage_root, Rect2(1388, 22, 134, 68), "rps")\n'''
new='''\t_rps_timer_dock(stage_root, Rect2(260, 642, 1044, 72))\n'''
assert old in s
s=s.replace(old,new,1)

# Slightly strengthen hierarchy while preserving the validated card layout.
old='''\t_label(stage_root, subtitle, Rect2(330, 74, 900, 30), 12, Color("a8bac9"), HORIZONTAL_ALIGNMENT_CENTER, false)\n'''
new='''\t_label(stage_root, subtitle, Rect2(330, 74, 900, 30), 13, Color("bed0dc"), HORIZONTAL_ALIGNMENT_CENTER, false)\n'''
assert old in s
s=s.replace(old,new,1)

# Footer copy: shorter and more useful now that timing is visible in the dock.
old='''\t\tfooter.text = "30 secondes • L'IA choisit en même temps • La révélation se fait après ton verrouillage."\n'''
new='''\t\tfooter.text = "Choisis ton signe • L'IA joue simultanément • Révélation après verrouillage"\n'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)
print('V5 patch applied, chars=',len(s))
