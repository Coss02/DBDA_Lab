#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 09:31:39 2022

@author: armano
"""

# -----------------------------------------------------------------------------

class Switch(object):
  
  "A simple switch with getter/setter/toggle"
  
  def __init__(self):
    "Init the switch"
    self.status = 'off'
    
  def set_status(self, status):
    "Set the status of the switch"
    assert status in ('off', 'on')
    self.status = status
    
  def get_status(self):
    "Get the current status"
    return self.status

  def toggle(self):
    "Toggle the current status"
    self.status = 'off' if self.status == 'on' else 'on'
    
  def isOn(self):
    "Check whether the switch is 'on'"
    return self.status == 'on'
  
  def display(self):
    "Print the current status"
    print(f"The switch is currently {self.status}")

# -----------------------------------------------------------------------------

class XSwitch(Switch):
  
  "A switch that also remembers all statuses (from the beginning)"
  
  STATUS = property(lambda self: self.status)
  
  def __init__(self):
    "Init the switch"
    super().__init__() # call the initializer of the 'Switch' superclass
    self.history = [ self.status ] # store the initial status...
    
  def __iter__(self):
    "Make an XSwitch iterable"
    return iter(self.history)

  def set_status(self, status):
    "Set the status of the switch (and remember it)"
    super().set_status(status)
    self.history += [ self.status ]
    
  def __lshift__(self, status):
    "Alternative way to set the set_status..."
    self.set_status(status)
    return self

  def __call__(self, status): # better to use __call__ instead of set_status...
    "Yet another alternative way to set the status..."
    self.set_status(status)
    
  def toggle(self):
    "Toggle the status of the switch (and remember it)"
    super().toggle()
    self.history += [self.status ]

  def display_history(self, comment='The switch history is'):
    "Display the history of the switch"
    print(f"\n{comment}: {self.history}\n")

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  switch = XSwitch() # history = [ 'off' ]
  
  switch.set_status('on') # history = [ 'off', 'on' ]
  
  switch.toggle() # history = [ 'off', 'on', 'off' ]
  
  switch << 'on' << 'on' # history = [ 'off', 'on', 'off', 'on', 'on' ]
  
  switch('off') # history = [ 'off', 'on', 'off', 'on', 'on', 'off' ]
  
  switch.toggle() # history = [ 'off', 'on', 'off', 'on', 'on', 'off', 'on' ]
  
  print(f"\nCurrent status is '{switch.get_status()}'") # should be 'on'
  
  print(f"\nIs the switch 'on'?: {switch.isOn()}")
  
  switch.display_history() # [ 'off', 'on', 'off', 'on', 'on', 'off', 'on' ]
  
  print("Iterating over the history", end="\n\n")
  
  for k, status in enumerate(switch): print(f"{k+1}: {status}")
  
  print(f"\nGetting the status using the 'STATUS' property: {switch.STATUS}")
  
  try:
  
    switch.STATUS = 'off' # ERROR! The STATUS property has only a getter...
    
  except:
    
    print("\nAttributeError: can't set attribute 'STATUS'")

# -----------------------------------------------------------------------------

    