from json import loads
import urllib2

class jsonRPC(object):
	"""
	Json request class
	This class implements the remote process call on json specs
	"""
	def request(self,url,args):
		"""
		Do the request
		@param url string the json RPC server
		@param params dict args to send
		"""
		for item in args.keys():
			url = url.replace("{"+item+"}",args[item])

		resp= None
		try:
			req = urllib2.Request(url,None,headers={"Connection" : "Keep-Alive","User-Agent": "SHEF Test Tool"})
			respdata = urllib2.urlopen(req).read()

			if(len(respdata)>0):	
				resp = loads(respdata)
			
		except:
			pass
		
		return resp