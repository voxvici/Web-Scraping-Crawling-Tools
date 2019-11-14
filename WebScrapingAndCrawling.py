from kivy.config import Config
Config.set('graphics', 'resizable', 0)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import socket
from ip_country import IPCountry
from ip2geotools.databases.noncommercial import DbIpCity
import os
from search_engines import Google, Bing, Yahoo
import requests
from parsel import Selector
from kivy.core.window import Window

"""

__future__:
	Possible improvements: automatic website archiving tool, better gui design, ignoring robots.txt & unmasking cloudflare

"""

class MainWindow(Screen):
    pass

class SpyderSiteWindow(Screen):
	siteinput = ObjectProperty(None)

	def SpyderSite(self):
		try:
			siteinput = self.siteinput.text
			response = requests.get(siteinput)
			selector = Selector(response.text)
			href_links = selector.xpath('//a/@href').getall()
			image_links = selector.xpath('//img/@src').getall()
			href_linksresult = str(href_links)
			image_linksresult = str(image_links)
			href_linkstitle = "-----------------------------------------------href links-----------------------------------------------"
			image_linkstitle = "-----------------------------------------------image links-----------------------------------------------"
			self.siteinput.text = "Site Spydered: " + siteinput + "\n" + href_linkstitle + "\n" + href_linksresult + "\n" + image_linkstitle + "\n" + image_linksresult
		except ValueError:
			self.siteinput.text = "Error >>> Please write url with http://"
		except Exception:
			self.siteinput.text = "Error >>> Please write url with http://"


class ScrapeGBYWindow(Screen):
	searchinput = ObjectProperty(None)
	engine = ObjectProperty(None)

	def ScrapeGBY(self):
		searchinput = self.searchinput.text
		engine = self.engine.text

		engineG = Google()
		engineB = Bing()
		engineY = Yahoo()

		try:
			if engine == 'Google' or engine == 'google':
				resultsG = engineG.search(searchinput)
				linksG = resultsG.links()
				linksGresult = str(linksG)
				self.engine.text = "Scraped Links From Google: \n" + linksGresult
			elif engine == 'Bing' or engine == 'bing':
				resultsB = engineB.search(searchinput)
				linksB = resultsB.links()
				linksBresult = str(linksB)
				self.engine.text = "Scraped Links From Bing: \n" + linksBresult
			elif engine == 'Yahoo' or engine == 'yahoo':
				resultsY = engineY.search(searchinput)
				linksY = resultsY.links()
				linksYresult = str(linksY)
				self.engine.text = "Scraped Links From Yahoo: \n" + linksYresult
			else:
				self.engine.text = "Error >>> Type: 'Google' or 'google' without '' same for bing & yahoo"
		except KeyError:
			self.engine.text = "Error >>> Type: 'Google' or 'google' without '' same for bing & yahoo"
		except Exception:
			self.engine.text = "Error >>> Type: 'Google' or 'google' without '' same for bing & yahoo"

class IPLocationWindow(Screen):
	iplocation = ObjectProperty(None)

	def FindIPLocation(self):
		iplocation = self.iplocation.text
		findip = iplocation

		try:
			response = DbIpCity.get(findip,api_key='free')
			ip = IPCountry('IP2LOCATION-LITE-DB3.CSV')
			ip2geotools = "--------------------------------------ip2geotools--------------------------------------"
			ip2location = "-----------------------------------------ip2location----------------------------------------"
			ipt = "Scanned IP: " + findip + ", \n (If Different Locations Are Showing VPN is active)"
			ipdata = ip.get_ip_data(findip)
			ipdataresult = str(ipdata)

			self.iplocation.text = ipt + "\n" + ip2geotools + "\nCity: " + response.city + "," + " Region: " + response.region + "," + " Country: " + response.country + "\n" + ip2location + "\n" + ipdataresult
		except KeyError:
			self.iplocation.text = "Error >>> Type: IP address you want to scan, example:199.116.115.146, without letters"
		except Exception:
			self.iplocation.text = "Error >>> Type: IP address you want to scan, example:199.116.115.146, without letters"



class IPToolWindow(Screen):
	domain = ObjectProperty(None)

	def FindOutIP(self):
		domain = self.domain.text

		try:
			ip = socket.gethostbyname(domain)
			self.domain.text = domain + " IP address is " + ip
		except IOError:
			self.domain.text = "Error >>> Please write: google.com, without www., currently supports one domain per search"
		except Exception:
			self.domain.text = "Error >>> Please write: google.com, without www., currently supports one domain per search"

class Manager(ScreenManager):
	pass

kv = Builder.load_string('''
Manager:
    MainWindow:
    IPLocationWindow:
    IPToolWindow:
    ScrapeGBYWindow:
    SpyderSiteWindow:

<MainWindow>:
    name: 'main'
    FloatLayout:
    	canvas:
    		Rectangle:
    			source: 'imgs/bg.jpg'
    			pos: self.pos
    			size: self.size
        Label:
            text: 'Web Scraping & Crawling Tools'
            pos: 0, 129
        Label:
        	text: 'Note: Read all hints included in text input within tools to gain most from software.'
        	pos: -30, -285
        Button:
        	text: 'Spyder Crawl For Links & Images Tool'
        	on_press:
        		app.root.current = 'spyderlinkswindow'
        		root.manager.transition.direction = 'left'
        	size: 300, 75
        	size_hint: None, None
        	pos: 300, 36
        	background_color: 0, 126, 0, .33
        	color: 0, 0, 0, 1
        Button:
        	text: 'Scrape Google, Bing or Yahoo Tool'
        	on_press:
        		app.root.current = 'scrapegbywindow'
        		root.manager.transition.direction = 'left'
        	size: 300, 75
        	size_hint: None, None
        	pos: 300, 126
        	background_color: 0, 126, 0, .33
        	color: 0, 0, 0, 1
        Button:
        	text: 'IP Location Tool'
        	on_press:
        		app.root.current = 'iplocationwindow'
        		root.manager.transition.direction = 'left'
        	size: 300, 75
        	size_hint: None, None
        	pos: 300, 216
        	background_color: 0, 126, 0, .33
        	color: 0, 0, 0, 1
        Button:
            text: 'Site IP Tool'
            on_press:
                app.root.current = 'iptoolwindow'
                root.manager.transition.direction = 'left'
            size: 300, 75
            size_hint: None, None
            pos: 300, 306
            background_color: 0, 126, 0, .33
            color: 0, 0, 0, 1


<SpyderSiteWindow>:
	siteinput: siteinput
	name: 'spyderlinkswindow'
	FloatLayout:
		Label:
			text: 'Spyder All Links & Images From A Website'
			pos: 0, 270
		Label:
			text: 'voxvici'
			pos: 414, -285
		TextInput:
			id: siteinput
			hint_text: 'Type link you want to spyder. Note: write full link with http://'
			multiline: True
			size: 900, 426
			size_hint: None, None
			pos: 0, 117
			background_color: 0, 0, 0, 0
			foreground_color: 0, 126, 0, .33
		Button:
			text: 'Release Spyder'
			on_press:
				root.SpyderSite()
			size: 300, 75
			size_hint: None, None
			pos: 135, 18
			background_color: 0, 39, 0, .30
			color: 0, 0, 0, 1
		Button:
			text: 'Go Back'
			on_press:
				app.root.current = 'main'
				root.manager.transition.direction = 'right'
			size: 300, 75
			size_hint: None, None
			pos: 441, 24
			background_color: 0, 39, 0, .30
			color: 0, 0, 0, 1

<ScrapeGBYWindow>:
	searchinput: searchinput
	engine: engine

	name: 'scrapegbywindow'
	FloatLayout:
		Label:
			text: 'Scrape Google, Bing or Yahoo'
			pos: 0, 270
		Label:
			text: 'Engine:'
			pos: -420, 183
		Label:
			text: 'Keyword:'
			pos: -414, 246
		Label:
			text: 'voxvici'
			pos: 414, -285
		TextInput:
			id: searchinput
			hint_text: 'Type anything you want to scrape from Google, Bing or Yahoo. As this software was created to catch scammers. Suggested search is: expert.contact-support-phone-number'
			multiline: True
			size: 900, 60
			size_hint: None, None
			pos: 0, 480
			background_color: 0, 0, 0, 0
			foreground_color: 0, 126, 0, .33
		TextInput:
			id: engine
			hint_text: 'If program is not responding wait < 3 mins and it will display result, usually takes between 1 - 3mins. Type: Google, Bing or Yahoo (output will be displayed here)'
			multiline: True
			size: 900, 369
			size_hint: None, None
			pos: 0, 108
			background_color: 0, 0, 0, 0
			foreground_color: 0, 126, 0, .33
		Button:
			text: 'Scrape Search Engine'
			on_press:
				root.ScrapeGBY()
			size: 300, 75
			size_hint: None, None
			pos: 135, 18
			background_color: 0, 39, 0, .30
			color: 0, 0, 0, 1
		Button:
			text: 'Go Back'
			on_press:
				app.root.current = 'main'
				root.manager.transition.direction = 'right'
			size: 300, 75
			size_hint: None, None
			pos: 441, 18
			background_color: 0, 39, 0, .30
			color: 0, 0, 0, 1


<IPLocationWindow>:

	iplocation: iplocation

    name: 'iplocationwindow'
    FloatLayout:
        Label:
            text: 'Find IP Location Tool'
            pos: 0, 270
        Label:
			text: 'voxvici'
			pos: 414, -285
        TextInput:
        	id: iplocation
        	hint_text: 'Type: IP address you want to scan, example:199.116.115.146, if you see multiple locations that means host is using VPN, one IP address per search'
        	multiline: True
        	size: 900, 426
			size_hint: None, None
			pos: 0, 111
			background_color: 0, 0, 0, 0
			foreground_color: 0, 126, 0, .33
        Button:
        	text: 'Find IP Location'
        	on_press:
        		root.FindIPLocation()
        	size: 300, 75
			size_hint: None, None
			pos: 135, 18
			background_color: 0, 39, 0, .30
			color: 0, 0, 0, 1
        Button:
            text: 'Go Back'
            on_press:
                app.root.current = 'main'
                root.manager.transition.direction = 'right'
            size: 300, 75
			size_hint: None, None
			pos: 441, 18
			background_color: 0, 39, 0, .30
			color: 0, 0, 0, 1

<IPToolWindow>:

	domain: domain

    name: 'iptoolwindow'
    FloatLayout:
        Label:
            text: 'Find Out Site IP Tool'
            pos: 0, 270
        Label:
			text: 'voxvici'
			pos: 414, -285
        TextInput:
        	id: domain
        	hint_text: 'Write: google.com, without www., currently supports one domain per search'
        	multiline: False
        	size: 900, 426
			size_hint: None, None
			pos: 0, 111
			background_color: 0, 0, 0, 0
			foreground_color: 0, 126, 0, .33
        Button:
        	text: 'Find Out IP'
        	on_press:
        		root.FindOutIP()
        	size: 300, 75
			size_hint: None, None
			pos: 135, 18
			background_color: 0, 39, 0, .30
			color: 0, 0, 0, 1
        Button:
            text: 'Go Back'
            on_press:
                app.root.current = 'main'
                root.manager.transition.direction = 'right'
            size: 300, 75
			size_hint: None, None
			pos: 441, 18
			background_color: 0, 39, 0, .30
			color: 0, 0, 0, 1
''')

class WebScrapingAndCrawling(App):
    def build(self):
    	Window.size = 900,600
    	self.title = 'Web Scraping & Crawling Tools'
    	return(kv)

if __name__ == '__main__':
    WebScrapingAndCrawling().run()