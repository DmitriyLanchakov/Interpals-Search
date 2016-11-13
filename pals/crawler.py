from pals.models import UserProfile
from selenium import webdriver
from pals.add import AddToDb as add
from pals.add import AddAll, AddCustom
from pals.add import login as lg
import gc
import signal

gc.enable()
b = webdriver.PhantomJS()
# b = webdriver.Chrome('/home/anon/Downloads/chromedriver', service_args=['--load-images=no'])
b.get('https://www.interpals.net')

b.service.process.send_signal(signal.SIGTERM) # kill the specific phantomjs child proc
b.quit() 
