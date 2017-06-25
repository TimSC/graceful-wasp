from django.shortcuts import render
from django.http import HttpResponse
from pyMbTiles import MBTiles, VectorTile
import zlib, cStringIO

def index(request):
	coast = MBTiles.MBTiles("coast.mbtiles")

	return HttpResponse("foobar")

def tiles(request, tileZoom, tileColumn, tileRow):
	tileZoom = int(tileZoom)
	tileColumn = int(tileColumn)
	tileRow = int(tileRow)

	coastTiles = MBTiles.MBTiles("coast.mbtiles")
	coastTile = coastTiles.GetTile(tileZoom, tileColumn, tileRow)
	coastUncompressed = zlib.decompress(coastTile, 16+zlib.MAX_WBITS)

	mapTiles = MBTiles.MBTiles("map.mbtiles")
	try:
		mapTile = mapTiles.GetTile(tileZoom, tileColumn, (2 ** tileZoom) - tileRow - 1)
		mapUncompressed = zlib.decompress(mapTile, 16+zlib.MAX_WBITS)
	except RuntimeError:
		mapUncompressed = None

	#Merge these
	data = cStringIO.StringIO()
	enc = VectorTile.EncodeVectorTile(tileZoom, tileColumn, tileRow, data)
	encFilterFinish = VectorTile.FilterFinish(enc)
	
	dec = VectorTile.DecodeVectorTile(tileZoom, tileColumn, tileRow, encFilterFinish)
	dec.DecodeTileData(coastUncompressed)
	if mapUncompressed is not None:
		dec.DecodeTileData(mapUncompressed)
	enc.Finish()

	#Recompress
	comp = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, 16+zlib.MAX_WBITS)
	compData = [comp.compress(data.getvalue())]
	compData.append(comp.flush())
	recompressedData = b"".join(compData)

	#Send response
	response = HttpResponse(recompressedData, content_type='application/vnd.mapbox-vector-tile')
	response['Content-Encoding'] = 'gzip'
	response['Content-Length'] = str(len(recompressedData))

	return response

