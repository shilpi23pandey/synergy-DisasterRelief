var map,infobox;
var credentials='Apv2l9wgX2-JuwgKuHx6Y8_1BM-LOksxxRa-6kGfdGWzNx4ZHEyuSyffdo1bOR0P'
function GetMap() {
      // Define the address on which to centre the map
      var addressLine = ""; // Street Address
      var locality = "joplin"; // City or town name
      var adminDistrict = ""; // County
      var country = "USA"; // Country, obviously
      var postalCode = "" //Postcode
        
      // Construct a request to the REST geocode service
      var geocodeRequest = "http://dev.virtualearth.net/REST/v1/Locations" 
                           + "?countryRegion=" + country
                           + "&addressLine=" + addressLine
                           + "&locality=" + locality
                           + "&adminDistrict=" + adminDistrict
                           + "&postalCode=" + postalCode
                           + "&key=" + credentials
                           + "&jsonp=GeocodeCallback"; // This function will be called after the geocode service returns its results
        
      // Call the service
      CallRestService(geocodeRequest);
    }
function GeocodeCallback(result) {
      // Check that we have a valid response
      if (result && result.resourceSets && result.resourceSets.length > 0 && result.resourceSets[0].resources && result.resourceSets[0].resources.length > 0) {
        
        // Create a Location based on the geocoded coordinates
        var coords = result.resourceSets[0].resources[0].point.coordinates;
        console.log("coords: ",coords)
        centerPoint = new Microsoft.Maps.Location(coords[0], coords[1]);
 
        // Create a map centred on the location
        map = new Microsoft.Maps.Map(document.getElementById("mapDiv"),
                           { credentials: credentials,
                             center: centerPoint,
                             mapTypeId: Microsoft.Maps.MapTypeId.aerial,
                             zoom: 15
                           });
        //Create an infobox at the center of the map but don't show it.
        infobox = new Microsoft.Maps.Infobox(map.getCenter(), {
            visible: false
        });

        //Assign the infobox to a map instance.
        infobox.setMap(map);
		{% for location in maps: %}
        var location={altitude:0,altitudeReference:-1,latitude:{{ location.latitude }},longitude:{{ location.longitude }}};
        var pin = new Microsoft.Maps.Pushpin(location);
        map.entities.push(pin);
		{% endfor %} 
      }
    }
    /*
function CreatePushPin() {
	{% for location in maps: %}
        centerPoint = new Microsoft.Maps.Location({{ location.longitude }}, {{ location.latitude }});
		map = new Microsoft.Maps.Map(document.getElementById("mapDiv"),
                           { credentials: credentials,
                             center: centerPoint,
                             mapTypeId: Microsoft.Maps.MapTypeId.aerial,
                             zoom: 18
                           });

        // Add a pushpin as well
        var pushpin = new Microsoft.Maps.Pushpin(map.getCenter());
        map.entities.push(pushpin);
}*/

 function CallRestService(request) {
      var script = document.createElement("script");
      script.setAttribute("type", "text/javascript");
      script.setAttribute("src", request);
      var dochead = document.getElementsByTagName("head").item(0);
      dochead.appendChild(script);
    }