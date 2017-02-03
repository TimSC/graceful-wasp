from django.shortcuts import render
from django.http import HttpResponse
from pyMbTiles import MBTiles
import zlib

def index(request):
	coast = MBTiles.MBTiles("coast.mbtiles")

	return HttpResponse("foobar")

def tiles(request, tileZoom, tileColumn, tileRow):
	coast = MBTiles.MBTiles("coast.mbtiles")
	tile = coast.GetTile(tileZoom, tileColumn, tileRow)

	#uncompressed = zlib.decompress(tile, 16+zlib.MAX_WBITS)
	response = HttpResponse(tile, content_type='application/vnd.mapbox-vector-tile')
	response['Content-Encoding'] = 'gzip'
	response['Content-Length'] = str(len(tile))
	return response

