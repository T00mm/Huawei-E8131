# (Huawei) E8131

This python wrapper works with the Huawei E8131 mobile stick. 

 * Reads SMS, set them as read, deletes them,...
 * Send SMSes
 * Import SMS from SIM-card
 * Get status of connections, logins, device, PIN,...
 * ...

## Functions

Still need to write these documentation. Here are some test thingies from me

```python
from E8131 import E8131
cell = E8131();
print cell.get_connection_status()
print cell.get_device_info()
print cell.get_check_notifications()
print cell.get_network_info()
print cell.get_sms_count()
print cell.get_traffic_stats()
print cell.get_check_notifications()
print cell.get_user_status()
print cell.get_sms_send_status()
print cell.get_pin_status()
print cell.get_converged_status()
print cell.get_user_remind()
print cell.get_update_status()

if not cell.user_logged_in():
	print "Going to login"
	cell.post_user_login("admin","admin")
else:
	print "Already logged in"

sms_stuff = cell.post_get_sms_list()

if sms_stuff:
	print sms_stuff["Count"]
	for message in sms_stuff['Messages']['Message']:
		print message['Phone']

print cell.post_sms_delete("40001")
print cell.post_import_from_sim()
print cell.post_set_sms_as_read("40002")
print cell.post_clear_statistics()
print cell.post_user_session_refresh()
print cell.post_send_sms("0499454545","hey")
print cell.post_send_sms(["0499454545","0499454546","0499454547"],"array test")
print cell.user_logged_in()

````

For most post functions you need to be logged in, but if you login after already being logged in, you will be logged out!

### To-do
 * All settings POST
 * More error logging, haven't reserved them all yet
 
### Stuff used to make this:

 * [Python docs](https://www.python.org/doc/)
 * [xmltodict](https://github.com/martinblech/xmltodict)
