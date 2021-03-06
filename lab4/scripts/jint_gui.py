#!/usr/bin/env python


# import correct version of Gtk
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import rospy
from lab4.srv import *
from threading import Thread
import Queue

# window class
class MyWindow(Gtk.Window):

	# init
	def __init__(self):
		self.handling = False
		Gtk.Window.__init__(self, title="jint operator")
		
		self.set_default_size(500, 500)
		self.set_resizable(False)
		self.request_queue = None
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
		self.msg_label.set_xalign(0.0)
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
		
	
	def add_queue(self, queue):	
		self.request_queue = queue

	def print_response(self, msg, handling=False):
		self.msg_label.set_text(msg)
		self.handling = handling

	# click handler
	def on_button_clicked(self, widget):
		if self.handling == True:
			return
		self.handling = True
		try:
			task = Task(float(self.scale0.get_value()), 
				    float(self.scale1.get_value()), 
			  	    float(self.scale2.get_value()), 
				    float(self.time_box.get_text()), 
				    str(self.chosen_type), self)
		except Exception:
			self.print_response(" ERROR: Invalid Time")
			return

		self.msg_label.set_label(" Waiting for service...")
		self.request_queue.put(task)
		
	
class Task:
	def __init__(self, angle0, angle1, angle2, time, typ, obj):
		self.sup =  obj
		self.ang0 = angle0
		self.ang1 = angle1
		self.ang2 = angle2
		self.time = time
		self.type = typ



class RequestHandler(Thread):
	def __init__(self, task_queue, result_queue, win):
		self.window_alive = True
		Thread.__init__(self)
		self.window = win
		self.task_queue = task_queue
		self.result_queue = result_queue
	def run(self):	
		while self.window_alive == True:
			req = self.task_queue.get()
			if req is None:
				continue
			else:
				try:
					rospy.wait_for_service('jint', timeout=3)

				except rospy.ROSException:
					resp1 = JINTRequestResponse()
					resp1.state = "ERROR: Service unreachable or busy"
					self.result_queue.put(resp1)
					continue

				self.window.print_response(" Moving...", handling=True)
				jint = rospy.ServiceProxy('jint', JINTRequest)
				try:
					resp1 = jint(float(req.ang0), 
						     float(req.ang1), 
						     float(req.ang2), 
						     float(req.time), 
						     str(req.type))
				
				except ValueError:
					resp1 = JINTRequestResponse()
					resp1.state = "ERROR: Invalid time"

				except rospy.ServiceException:
					resp1 = JINTRequestResponse()
					resp1.state = "ERROR: Service unreachable" 	
				self.result_queue.put(resp1)

class ResultHandler(Thread):
	def __init__(self, result_queue, window):
		self.window_alive = True
		Thread.__init__(self)
		self.result_queue = result_queue
		self.win = window

	def run(self):
		while self.window_alive == True:
			result = self.result_queue.get()
			if result is None:
				continue
			else:
				try:
					self.win.print_response(result.state)
				except:
					pass
				continue
				
	
def quit_handler(arg):
	request_handler.window_alive = False
	result_handler.window_alive = False
	tasks.put(None)
	results.put(None)
	Gtk.main_quit(arg)
	
			
win = MyWindow() # creating window
tasks = Queue.Queue()
results = Queue.Queue()
request_handler = RequestHandler(tasks, results, win)
request_handler.start()
result_handler = ResultHandler(results, win)
result_handler.start()
win.add_queue(tasks)
win.connect('destroy', quit_handler) # exit handler
win.show_all() # show 
Gtk.main() # main loop
