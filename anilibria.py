from requests import Session
from random import choices
from string import ascii_letters

from .objects import *

class Anilibria:
	_second_api = "https://a.anilibria.sbs/public/{}".format
	_headers = {
		"user-agent": "Mozilla/5.0 (Linux; U; Linux x86_64; en-US) AppleWebKit/600.8 (KHTML, like Gecko) Chrome/47.0.1452.400 Safari/536",
		"x-requested-with": "XMLHttpRequest"
	}

	@classmethod
	def __method_request(cls, method: str, url: str, data: dict = None):
		session = Session()

		if method == 'get': req = session.get(url = url, headers = cls._headers)
		else: req = session.post(url = url, headers = cls._headers, data = data)

		return req.status_code if req.status_code != 200 else req

	@classmethod
	def login(cls, email: str, password: str) -> Login:
		data = {
			"csrf": 1,
			"mail": email,
			"passwd": password
		}
		req = Login(**cls.__method_request(method = 'post', url = cls._second_api('/login.php'), data = data).json())
		cls._headers['cookie'] = f'PHPSESSID={req.sessionId}'
		return req

	@classmethod
	def logout(cls) -> None:
		cls.__method_request(method = 'get', url = cls._second_api('/logout.php'))

	@classmethod
	def set_new_password(cls, old_password: str, new_password: str) -> dict:
		data = {
			'oldPasswd': old_password,
			'newPasswd': new_password,
			'repPasswd': new_password
		}
		return cls.__method_request(method = 'post', url = cls._second_api('change/passwd.php'), data = data).json()

	@classmethod
	def set_new_mail(cls, new_email: str, password: str) -> dict:
		data = {
			'mail': new_email,
			'passwd': password
		}
		return cls.__method_request(method = 'post', url = cls._second_api('change/mail.php'), data = data).json()

	@classmethod
	def set_vk(cls, vk_id: int) -> dict:
		data = {
			'vk': vk_id
		}
		return cls.__method_request(method = 'post', url = cls._second_api('change/vk.php'), data = data).json()

	@classmethod
	def search_anime(cls, search: str) -> dict:
		data = {
			"search": search,
			"small": 1
		}
		return cls.__method_request(method = 'post', url = cls._second_api('search.php'), data = data).json()

	@classmethod
	def get_random_anime(cls) -> str:
		data = {
			"js": 1
		}
		return cls.__method_request(method = 'post', url = cls._second_api('random.php'), data = data).text

	@classmethod
	def catalog(cls, page: int = 1, sort: int = 1, finish: int = 1, year: int = None, genre: str = None, season: str = None) -> Catalog:
		data = {
			"page": page,
			'xpage': 'catalog',
			"sort": sort,
			"finish": finish,
			"search": {
				"year": year,
				"genre": genre,
				"season": season
			}
		}
		return Catalog(**cls.__method_request(method = 'post', url = cls._second_api('catalog.php'), data = data).json())

	@classmethod
	def favorites(cls, page: int = 1) -> Catalog:
		data = {
			"page": page,
			'xpage': 'favorites',
			"sort": sort,
			"finish": finish
		}
		return Catalog(**cls.__method_request(method = 'post', url = cls._second_api('catalog.php'), data = data).json())

