import poe
import openai
import time

class ChatAPI:
	def __init__(self, openai_key = None, poe_key = None):
		if openai_key is not None:
			pass
		elif poe_key is not None:
			loop_count = 0
			while loop_count < 15:
				loop_count += 1
				try:
					self.using = "poe"
					self.client = poe.Client(poe_key)
					break
				except:
					print(f"*** Failed, Retrying {loop_count} Times")
		else:
			raise Exception("*** Please Provide at least one key")

	def generate(self, message, clear_context = False, model = "chinchilla", layer = 0):
		if layer > 5:
			raise Exception(f"*** Retry Message {message} Too Many Times")

		if self.using == 'poe':
			try:
				for chunk in self.client.send_message(
					"chinchilla", 
					message, 
					with_chat_break=clear_context,
					timeout = 30
				): 
					pass
				response = chunk["text"]
				return response
			except Exception as e:
				print(f"***Caught Exception {e}, Retrying")
				time.sleep(3)
				return self.generate(message, clear_context, model, layer + 1)