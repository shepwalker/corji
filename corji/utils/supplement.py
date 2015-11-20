from corji.data_sources.supplements import(
	get_all,
	load
) 
from corji.models import emoji_customer
from corji.settings import Config


load(Config.SUPPLEMENTS_URL)
list_of_supplements = get_all()


def get_supplement_messsage(customer_phone_number, message):
	"""
	Returns first matched supplement to the message or
	none if no supplements match.
	"""
	customer = emoji_customer.get(customer_phone_number)
	
	for s in list_of_supplements:
		if s.TriggerType == "messagecount":
			#TODO: Have a flag for user metadata that notes that they've been 
			#marketed-to. Maybe change this to a name
			print(customer)
			if "message_count" in customer and int(customer["message_count"]['N']) >= int(s.Param) and not s.Name in customer:
				emoji_customer.add_metadata(customer_phone_number, s.Name, "true")
				return s.Text
	return None