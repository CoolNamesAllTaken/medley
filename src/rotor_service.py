import threading
import time

from utils import *

HA_PIN = 6 # hall sensor for 
HB_PIN = 13
H_DEBOUNCE_PERIOD_MILLIS = 5

MOT_PIN = 12
MOT_MIN_PWM_DUTY_CYCLE = 1
MOT_MAX_PWM_DUTY_CYCLE = 10

PWM_INCREMENT = 1
PWM_INCREMENT_PERIOD_MILLIS = 100
NUM_COMPARTMENTS = 8

class RotorEncoder:
	def __init__(self, gpio):
		self.gpio = gpio
		self.gpio.setup([HA_PIN, HB_PIN], self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
		gpio.setup(MOT_PIN, gpio.OUT, initial=gpio.HIGH)

		self.motor_pwm = gpio.PWM(MOT_PIN, MOT_MAX_PWM_DUTY_CYCLE)    # create an object p for PWM on port 25 at MOT_MAX_PWM_DUTY_CYCLE Hertz  
							# you can have more than one of these, but they need  
							# different names for each port   
							# e.g. p1, p2, motor, servo1 etc.  
	  
		self.motor_pwm_duty_cycle = 0
		self.motor_pwm.start(self.motor_pwm_duty_cycle) # duty cycle value can be 0.0 to MOT_MAX_PWM_DUTY_CYCLE.0%, floats are OK
		self.motor_pwm_increment_millis = millis()

		self.rotor_pos = 0
		self.target_rotor_pos = 0

		self.last_ha_val = 0
		self.last_ha_0_millis = millis()
		self.last_hb_val = 0
		self.last_hb_0_millis = millis()

	def increment_rotor_pos(self):
		self.target_rotor_pos += 1
		# if self.target_rotor_pos > NUM_COMPARTMENTS - 1:
		# 	self.target_rotor_pos = 0

	def run_rotor_listener(self):
		while True:
			if not self.gpio.input(HA_PIN) and self.last_ha_val == 1 and \
			millis() - self.last_ha_0_millis > H_DEBOUNCE_PERIOD_MILLIS:
				print("HA")
				# captured HA falling edge
				# self.rotor_pos += 1
				self.rotor_pos = self.target_rotor_pos
				self.last_ha_val = 0
				self.last_ha_0_millis = millis()
			elif self.gpio.input(HA_PIN):
				self.last_ha_val = 1

			if not self.gpio.input(HB_PIN) and self.last_hb_val == 1 and \
			millis() - self.last_hb_0_millis > H_DEBOUNCE_PERIOD_MILLIS:
				print("HB")
				# captured HB falling edge
				# self.rotor_pos = 0
				# self.motor_pwm_duty_cycle = 0
				# time.sleep(1)
				self.rotor_pos = self.target_rotor_pos
				self.last_hb_val = 0
				self.last_hb_0_millis = millis()
			elif self.gpio.input(HB_PIN):
				self.last_hb_val = 1

			if self.target_rotor_pos > self.rotor_pos:
				# rotor not at target: rotate
				if self.motor_pwm_duty_cycle < MOT_MAX_PWM_DUTY_CYCLE and \
				millis() - self.motor_pwm_increment_millis > PWM_INCREMENT_PERIOD_MILLIS:
					self.motor_pwm_increment_millis = millis()
					if self.motor_pwm_duty_cycle == 0:
						# start beyond stall
						self.motor_pwm_duty_cycle = MOT_MIN_PWM_DUTY_CYCLE
					elif MOT_MAX_PWM_DUTY_CYCLE - self.motor_pwm_duty_cycle <= PWM_INCREMENT:
						# jump to full
						self.motor_pwm_duty_cycle = MOT_MAX_PWM_DUTY_CYCLE
					else:
						# continue ramp
						self.motor_pwm_duty_cycle += PWM_INCREMENT
			else:
				# rotor at target
				self.motor_pwm_duty_cycle = 0
			self.motor_pwm.ChangeDutyCycle(self.motor_pwm_duty_cycle)
			print("{}->{} {}".format(self.rotor_pos, self.target_rotor_pos, self.motor_pwm_duty_cycle))

