#!/usr/bin/env python


# import correct version of Gtk
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import rospy
from lab4.srv import *
import gobject
import threading

# window class
class MyWindow(Gtk.Window):

	# init
	def __init__(self):
		self.handling = False
		Gtk.Window.__init__(self, title="jint operator")
		
		self.set_default_size(500, 500)
		self.set_resizable(False)

		grid = Gtk.Grid()
		self.add(grid)
		grid.set_row_spacing(5)
		grid.set_column_spacing(10)

	# slider 0

		slider0_frame = Gtk.Frame()
		slider0_frame.set_label("base_link_to_segment_1_joint_continous")
		slider0_frame.set_border_width(5)

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
		slider0_frame.add(self.scale0)
		grid.attach(slider0_frame, 0, 0, 1, 1)

	# slider 1
		slider1_frame = Gtk.Frame()
		slider1_frame.set_label("segment_1_to_segment_2_joint_continous")
		slider1_frame.set_border_width(5)

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
		slider1_frame.add(self.scale1)
		grid.attach(slider1_frame, 0, 1, 1, 1)

	# slider 2
		slider2_frame = Gtk.Frame()
		slider2_frame.set_label("segment_2_to_gripper_joint_continous")
		slider2_frame.set_border_width(5)

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
		slider2_frame.add(self.scale2)
		grid.attach(slider2_frame, 0, 2, 1, 1)

	# label_down
		self.msg_label = Gtk.Label()
		self.msg_label.set_label(" Ready...")
		self.msg_label.set_width_chars(40)
		self.msg_label.set_halign(Gtk.Align.START)
		self.msg_label.set_valign(Gtk.Align.START)
		grid.attach(self.msg_label, 0, 3, 4, 1) 

	# move_button
		move_button = Gtk.Button(label="Move")
		move_button.connect("clicked", self.on_button_clicked)
		grid.attach(move_button, 2, 0 ,1, 1)
	
	# time_text_box
		self.time_box = Gtk.Entry()
		self.time_box.set_text("1.00")
		self.time_box.set_width_chars(4)
        	grid.attach(self.time_box, 1, 0, 1, 1)

	# radios 
		self.chosen_type = "linear"
		radio_frame = Gtk.Frame()
		radio_frame.set_label("Interpolation type")
		radio_frame.set_border_width(5)
		radio1 = Gtk.RadioButton.new_with_label_from_widget(None, "linear")
		radio1.connect("toggled", self.on_button_toggled, "linear")
		radio2 = Gtk.RadioButton.new_with_label_from_widget(radio1, "quadratic")
		radio2.connect("toggled", self.on_button_toggled, "quad_spline")
		radio3 = Gtk.RadioButton.new_with_label_from_widget(radio1, "trapezoid_vel")
		radio3.connect("toggled", self.on_button_toggled, "trapezoid_vel")
		hbox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
		radio_frame.add(hbox)
		
		hbox.pack_start(radio1, False, False, 0)
		hbox.pack_start(radio2, False, False, 0)
		hbox.pack_start(radio3, False, False, 0)
		grid.attach(radio_frame, 1, 1, 2, 2) 

	def on_button_toggled(self, widget, name):
		self.chosen_type = name
		
	
	# click handler
	def on_button_clicked(self, widget):
		if self.handling == True:
			return
		self.handling = True
		handler = Handler(float(self.scale0.get_value()), float(self.scale1.get_value()), float(self.scale2.get_value()), float(self.time_box.get_text
()), str(self.chosen_type), self)
		handler.start()
		self.msg_label.set_label(" Waiting for response...")
	
# thread-safe handler
class Handler(threading.Thread):
	def __init__(self, angle0, angle1, angle2, time, type, obj):
		Thread.__init__(self)
		self.ang0 = angle0
		self.ang1 = angle1
		self.ang2 = angle2
		self.time = time
		self.type = type
		self.obj = obj

	def run(self):
		try:
			rospy.wait_for_service('jint', timeout=5)
		except rospy.ROSException:
			resp1 = JINTRequestResponse()
			resp1.state = "ERROR: Service unreachable or busy"

		jint = rospy.ServiceProxy('jint', JINTRequest)
		try:
			resp1 = jint(float(self.ang0), float(self.ang1), float(self.ang2), float(self.time), str(self.type))
			
		except rospy.ServiceException:
			resp1 = JINTRequestResponse()
			resp1.state = "ERROR: Service unreachable" 	
		#self.obj.msg_label.set_text(resp1.state)
		print(resp1)



win = MyWindow() # creating window
win.connect('destroy', Gtk.main_quit) # exit handler
win.show_all() # show 
Gtk.main() # main loop
