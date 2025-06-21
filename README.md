# Functions Untuk Scripting
# Fitur
- class Requests
- class Functions
- class Display
- class Baypas captcha Multibot & xevil
- Baypas Icon Captcha
- html scrap (menggunakan BeautifulSoup)

# Example
#### Cara Import 
```from class import*```
#### Requests
```response = Requests.curl('https://example.com')```
#### Functions 
```Functions.setConfig('nama_data')```
#### Baypas Captcha 
panggil function menu api dulu sebelum memanggil class Baypas Captch 
###### Example
function menu api 
```HOST_CAP,API_CAP = Functions.menu_api()`
lalu panggil function Baypas Captcha nya
cap = Captcha.Recaptchav2(sitekey,pageurl)```
#### Baypass Icon Captcha 
###### Example
```baypas = IconBypass(host, headers)``` 
```icon = baypas.icon_bypass(iconToken)```




