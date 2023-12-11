import datetime
import os
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from DriverWrapper import BrowserWrapper
from entity.UserEntity import User, WorkItems
from entity.db import db
from logutil import logger
from util import split_path, md5, download

brower_wrapper:BrowserWrapper = BrowserWrapper()
limit_time = 1
download_path="data/download/"
useragent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

def checkOneVideo(url:str,userid:int):
	global brower_wrapper
	work = WorkItems.get_or_none(WorkItems.url==url)
	if work is None:
		work=WorkItems(url=url,userid=userid)
		work.save()
	else:
		delta = datetime.datetime.now() - work.last_access_time
		if delta.total_seconds() < limit_time :
			logger.info(f"{url} 更新时间不足一小时，不更新")
			return

	brower_wrapper.get(url)
	ele = brower_wrapper.find_element(By.CLASS_NAME, 'dy-account-close')
	ele.click()
	video_info_wrap = brower_wrapper.find_element(By.TAG_NAME, "h1")
	# digg = brower_wrapper.find_element(By.CSS_SELECTOR,'div[data-e2e="video-player-digg"]')
	span = brower_wrapper.find_element(By.CSS_SELECTOR, "span[class='CE7XkkTw']")
	logger.info(video_info_wrap.text + " like:" + span.text)
	work.title=video_info_wrap.text
	work.like=span.text
	work.last_access_time=datetime.datetime.now()
	work.save()

def downloadVideo(url:str,userid:int):
	global brower_wrapper
	work = WorkItems.get_or_none(WorkItems.url==url)
	if work is None:
		work=WorkItems(url=url,userid=userid)
		work.save()
	if work.downloadpath is not None:
		logger.info(f"已经下载过{url}，忽略")
		return

	brower_wrapper.get(url)
	video_source = brower_wrapper.find_element(By.CSS_SELECTOR, 'video source')
	videoDownloadUrl = video_source.get_attribute("src")
	download_location = download_path + split_path(md5(videoDownloadUrl))+".mp4"
	os.makedirs(os.path.dirname(download_location),exist_ok=True)
	curl_cmd=f"curl --user-agent \"${useragent}\" --referer 'https://www.douyin.com/' -o '{download_location}' '{videoDownloadUrl}'"
	logger.info(f"下载命令:{curl_cmd}")
	# os.system(curl_cmd)
	if download(url=videoDownloadUrl,output=download_location):
		work.downloadpath=download_location
		work.save()

def updateUser(url:str):
	global brower_wrapper
	ele:WebElement = None
	user = User.get_or_none(User.mainurl == url)
	if user is None:
		user = User(mainurl=url, count=0)
		user.save()
	else:
		delta = datetime.datetime.now() - user.last_access_time
		if delta.total_seconds() < limit_time :
			logger.info(f"{url} 更新时间不足一小时，不更新")
			return

	brower_wrapper.get(url)
	try:
		WebDriverWait(brower_wrapper.driver, 10).until(
			presence_of_element_located((By.CLASS_NAME, "dy-account-close"))
		)
	except Exception as e:
		logger.warning(e)

	ele=brower_wrapper.find_element(By.CLASS_NAME, 'dy-account-close')
	ele.click()

	itemNumber= brower_wrapper.find_element(By.CSS_SELECTOR, "span[data-e2e='user-tab-count']").text
	logger.info("作品数量:" + itemNumber)


	user.count=int(itemNumber)
	user.last_access_time=datetime.datetime.now()
	user.save()
	list = brower_wrapper.find_element(By.CSS_SELECTOR,"div[data-e2e='user-post-list']")
	videolist = list.find_elements(By.TAG_NAME,"a")
	logger.info(f"size of videolist is {len(videolist)}")
	urllist=[]
	for video in videolist:
		url=video.get_attribute("href")
		if url.find("note") != -1:
			continue
		logger.info(video.get_attribute("href"))
		urllist.append(url)
		pele = video.find_elements(By.CSS_SELECTOR,"p")
		title_p = pele[len(pele)-1].text
		like = video.find_element(By.CSS_SELECTOR, "div span span").text
		work = WorkItems.get_or_none(WorkItems.url==url, WorkItems.userid==user.id)
		if work is None:
			work = WorkItems(url=url, userid=user.id)
			work.title=title_p
			work.like=like
			work.save()
			logger.info(f"create new {url},like={like}")
		elif work.like != like:
			work.like=like
			logger.info(f"update {url} like={like}")
			work.save()

	for url in urllist:
		downloadVideo(url,user.id)
		logger.info(f"{url} completed")
		sleep(1)


def main():
	db.connect()
	db.create_tables([User,WorkItems])
	updateUser('https://www.douyin.com/user/MS4wLjABAAAAmrmjkxbqs4nVOgQP6MgbjHcoE3R4tp_RF_i6WQjtusRrP7mn--VNRBVFRptILrv9')
	# checkUser("https://www.douyin.com/user/MS4wLjABAAAAyrIMbWizXolJqgdp7kC8mIeasj0PS9lzCxRAQmjKUGzM_FadezXkcZm2KgitjKtW?vid=7310599614904700200")
	db.close()

if __name__ == "__main__":
	main()

