from django.shortcuts import render
from django.http import HttpResponse
from pyMbTiles import MBTiles
import zlib

def index(request):
	coast = MBTiles.MBTiles("coast.mbtiles")

	return HttpResponse("foobar")

def tiles(request, tileZoom, tileColumn, tileRow):
	coastTiles = MBTiles.MBTiles("coast.mbtiles")
	coastTile = coastTiles.GetTile(tileZoom, tileColumn, tileRow)

	mapTiles = MBTiles.MBTiles("map.mbtiles")
	mapTile = mapTiles.GetTile(tileZoom, tileColumn, tileRow)

	#Merge these
	#uncompressed = zlib.decompress(tile, 16+zlib.MAX_WBITS)



	
	#Send response
	response = HttpResponse(mapTile, content_type='application/vnd.mapbox-vector-tile')
	response['Content-Encoding'] = 'gzip'
	response['Content-Length'] = str(len(mapTile))
	return response

