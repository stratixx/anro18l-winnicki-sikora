#!/usr/bin/env python


# import correct version of Gtk
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# window class
class MyWindow(Gtk.Window):

	# init
	def __init__(self):
		Gtk.Window.__init__(self, title="jint operator")
		self.set_resizable(False)

		grid = Gtk.Grid()
		self.add(grid)
		grid.set_row_spacing(5)
		grid.set_column_spacing(10)

	# fillers 
		filler_left = Gtk.Label()
		filler_left.set_label('')
		grid.attach(filler_left, 0, 0, 1, 12)

		filler_right = Gtk.Label()
		filler_right.set_label('')
		grid.attach(filler_right, 10, 0, 1, 12)

		filler_top = Gtk.Label()
		filler_top.set_label('')
		grid.attach(filler_top, 1, 0, 9, 1)

	# slider 0
		# label0
		label0 = Gtk.Label()
		label0.set_label("base_link_to_segment_1_joint_continous")		
		label0.set_halign(Gtk.Align.START)
		grid.attach(label0, 1, 0, 4, 1)

		# scale0 
		self.scale0 = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=Gtk.Adjustment(0,-3.14,3.14,0.01,0,0))

		# marks on slider
		self.scale0.add_mark(0, Gtk.PositionType.TOP, None)
		self.scale0.add_mark(1, Gtk.PositionType.TOP, None)
		self.scale0.add_mark(2, Gtk.PositionType.TOP, None)
		self.scale0.add_mark(3, Gtk.PositionType.TOP, None)
		self.scale0.add_mark(-1, Gtk.PositionType.TOP, None)
		self.scale0.add_mark(-2, Gtk.PositionType.TOP, None)
		self.scale0.add_mark(-3, Gtk.PositionType.TOP, None)

		# slider value 
		self.scale0.set_digits(2)	
		self.scale0.set_value_pos(Gtk.PositionType.RIGHT)
		self.scale0.set_valign(Gtk.Align.START)	
		grid.attach_next_to(self.scale0, label0, Gtk.PositionType.BOTTOM, 4, 1)

	# slider 1
		# label1
		label1 = Gtk.Label()
		label1.set_label("segment1_to_segment_2_joint_continous")		
		label1.set_halign(Gtk.Align.START)
		grid.attach(label1, 1, 4, 4, 1)

		# scale1
		self.scale1 = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=Gtk.Adjustment(0,-1.54, 0, 0.01, 0, 0))

		# marks on slider
		self.scale1.add_mark(0, Gtk.PositionType.TOP, None)
		self.scale1.add_mark(-1, Gtk.PositionType.TOP, None)
		self.scale1.add_mark(-0.5, Gtk.PositionType.TOP, None)
		self.scale1.add_mark(-1.54, Gtk.PositionType.TOP, None)

		# slider value 
		self.scale1.set_digits(2)	
		self.scale1.set_value_pos(Gtk.PositionType.RIGHT)
		self.scale1.set_valign(Gtk.Align.START)	
		grid.attach_next_to(self.scale1, label1, Gtk.PositionType.BOTTOM, 4, 1)

	# slider 2
		# label2
		label2 = Gtk.Label()
		label2.set_label("segment2_to_gripper_joint_continous")		
		label2.set_halign(Gtk.Align.START)
		grid.attach(label2, 1, 8, 4, 1)

		# scale2
		self.scale2 = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=Gtk.Adjustment(0, 0, 1.54, 0.01, 0, 0))

		# marks on slider
		self.scale2.add_mark(0, Gtk.PositionType.TOP, None)
		self.scale2.add_mark(1, Gtk.PositionType.TOP, None)
		self.scale2.add_mark(0.5, Gtk.PositionType.TOP, None)
		self.scale2.add_mark(1.54, Gtk.PositionType.TOP, None)

		# slider value 
		self.scale2.set_digits(2)	
		self.scale2.set_value_pos(Gtk.PositionType.RIGHT)
		self.scale2.set_valign(Gtk.Align.START)	
		grid.attach_next_to(self.scale2, label2, Gtk.PositionType.BOTTOM, 4, 1)

	# move_button
		move_button = Gtk.Button(label="Move")
		move_button.connect("clicked", self.on_button_clicked)
		grid.attach_next_to(move_button, filler_right, Gtk.PositionType.LEFT, 1, 1)
	
	# click handler
	def on_button_clicked(self, widget):
		print(self.scale0.get_value())
		print(self.scale1.get_value())
		print(self.scale2.get_value())

win = MyWindow() # creating window
win.connect('destroy', Gtk.main_quit) # exit handler
win.show_all() # show 
Gtk.main() # main loop
