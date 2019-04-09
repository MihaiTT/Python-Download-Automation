#! python3
# script care sa descarce toate comic-urile de pe xkcd.com
# nu uita sa creezi un bat file cu @py.exe C:\Users\User\MyPythonScripts\downloadXkcd.py %*
import requests,os,bs4
url='http://xkcd.com'    #de pe site-ul acesta descarc
os.makedirs('xkcd',exist_ok=True)
while not url.endswith('#'):
	print('Downloading page %s...' % url)
	res=requests.get(url)
	res.raise_for_status()
	soup=bs4.BeautifulSoup(res.text)
	comicElem=soup.select('#comic img')
	if comicElem == []:
		print('Nu am gasit imaginea')
	else:
		try:
			comicUrl='http:' + comicElem[0].get('src')
			# descarca imaginea
			print('Downloading image %s...' % (comicUrl))
			res=requests.get(comicUrl)
			res.raise_for_status()
			imageFile=open(os.path.join('xkcd',os.path.basename(comicUrl)),'wb')
			for chunk in res.iter_content(100000):
				imageFile.write(chunk)
			imageFile.close()
			prevLink=soup.select('a[rel="prev"]')[0]
			url='http://xkcd.com' + prevLink.get('href')
		except requests.exceptions.MissingSchema:
			# treci peste acest comic
			prevLink=soup.select('a[rel="prev"]')[0]
			url='http://xkcd.com' + prevLink.get('href')
			continue

