


def identify_message(incoming_message):


class AbstractCorgjiRequest(object):
	"""Abstract class for messages received to the service"""
	def __init__(self, body, sender):
		self.arg = arg
		self.body = body
		self.sender = sender
	def create_reply(self):
		raise NotImplementedError


class EmojiRequest(AbstractCorgjiRequest):
	"""docstring for ClassName"""
	def __init__(self, body, sender):
		super(ClassName, self).__init__(body, sender)
		self.arg = arg
	

	def create_reply(self):
