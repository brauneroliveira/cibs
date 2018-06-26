var listRRAS = [];
var listRegions = [];
var listMapLabel = [];
var listCities = [];
var listMapCity = [];
var listMarkers = [];

var map;
var markerCluster;
var mapLabel;


$(function() {

	map = new google.maps.Map(document.getElementById('map'), {
		zoom: 7,
		center: new google.maps.LatLng('-22.0185153','-47.897502'),
	});
	
	mapLabel = new MapLabel({
		map: map,
		align: 'center',
		fontSize: 30,
		fontColor: "#fffff",
		strokeWeight: 1,
		strokeColor: "#fffff"
	});

	insertRRAS();
});


function defineColor(avaliableBeds, totalBeds){
	var taxa = avaliableBeds/totalBeds;

	if (taxa >= 0 && taxa <= 0.1){
		return "#E67C73";
	} else if (taxa > 0.1 && taxa <= 0.2){
		return "#EC9170";
	} else if (taxa > 0.2 && taxa <= 0.3){
		return "#F2A46D";
	} else if (taxa > 0.3 && taxa <= 0.4){
		return "#F7B96A";
	} else if (taxa > 0.4 && taxa <= 0.5){
		return "#FDCC67";
	} else if (taxa > 0.5 && taxa <= 0.6){
		return "#ECD36A";
	} else if (taxa > 0.6 && taxa <= 0.7){
		return "#C7CD72";
	} else if (taxa > 0.7 && taxa <= 0.8){
		return "#A1C77A";
	} else if (taxa > 0.8 && taxa <= 0.9){
		return "#7CC182";
	} else if (taxa > 0.9 && taxa <= 1.0){
		return "#57BB8A";
	}
}

var varFillColor;
//--------------------------------------------------------------------------//
//-------------------------------- RRAS ------------------------------------//
function insertRRAS(){
	$.ajax({
		url: 'dist/js/rras/RAAS.js',
		dataType: 'JSON'
	}).done(function(listALLRAAS) {
		
		$.each(listALLRAAS, function(i, objRRAS){
			
			$.ajax({
				url: 'http://127.0.0.1:5001/getAvailableHospitalBedsFromRRAS/' + objRRAS.id,
				dataType: 'text'
			}).done(function(avaliableBeds){
				$.ajax({
					url: 'http://127.0.0.1:5001/getTotalNumberOfHospitalBedsFromRRAS/' + objRRAS.id,
					dataType: 'text'
				}).done(function(totalBeds){
					varFillColor = defineColor(avaliableBeds, totalBeds);

					var mapRRAS = new google.maps.Polygon({
						paths: objRRAS.latlng,
						strokeWeight: 2.5,
						strokeOpacity: 1,
						strokeColor: "#000000",
						fillOpacity: .75,
						fillColor: varFillColor
					});
		
					var centerRRAS = new google.maps.LatLngBounds();
					for (i = 0; i < objRRAS.latlng.length; i++) {
					  centerRRAS.extend(objRRAS.latlng[i]);
					}
				
					mapLabelRRAS = new MapLabel({
						map: map,
						align: 'center',
						fontSize: 18,
						fontColor: "#000000",
						strokeWeight: 1,
						strokeColor: "#FFFFFF"
					});
				
					mapRRAS.setMap(map);
		
					mapLabelRRAS.set('text', objRRAS.name);
					mapLabelRRAS.set('position', centerRRAS.getCenter());
					
					listMapLabel.push(mapLabelRRAS);
					listRRAS.push(mapRRAS);
					
					mapRRAS.addListener('click', function(){
						insertRegion(objRRAS);
						cleanMapLabel();
					});
				});
			});
		});
	}).fail(function(e) {
		console.log("error", e);
	});
}

function cleanRRAS(){
	$.each(listRRAS, function(i, delRegion){
		delRegion.setMap(null);
	});
	listRRAS = [];
}

function cleanMapLabel(){
	$.each(listMapLabel, function(i, delLabel){
		delLabel.setMap(null);
	});
	
	listMapLabel = [];
}
//--------------------------------------------------------------------------//
//------------------------------- Region -----------------------------------//
function insertRegion(objRRAS){
	cleanListCity();
	cleanCity();
	cleanRegion();
	cleanMapLabel();

	$.ajax({
		//search region by RRAS!
		url: 'dist/js/rras/' + objRRAS.name + '.js',
		dataType: 'JSON'
 	}).done(function(ListRegionsByRRAS) {

		$.each(ListRegionsByRRAS, function(i, objRegion){
			var mapRegion = new google.maps.Polygon({
				paths: objRegion.latlng,
				strokeWeight: 1,
				strokeOpacity: 0.5,
				strokeColor: "#000000",
				fillOpacity: 0,
				fillColor: "#FFFFFF"
			});

			var centerRegion = new google.maps.LatLngBounds();
			for (i = 0; i < objRRAS.latlng.length; i++) {
				centerRegion.extend(objRRAS.latlng[i]);
			}
		
			mapLabelRegion = new MapLabel({
				map: map,
				align: 'center',
				fontSize: 15,
				fontColor: "#000000",
				strokeWeight: 1,
				strokeColor: "#FFFFFF"
			});
		
			mapRegion.setMap(map);
			
			mapLabelRegion.set('text', objRRAS.name);
			mapLabelRegion.set('position', centerRegion.getCenter());

			listRegions.push(mapRegion);
			listMapLabel.push(mapLabelRegion);

			mapRegion.setMap(map);
			mapRegion.addListener('click', function(){
				selectCities(objRegion);
			});

		});
	}).fail(function(e) {
		console.log("error", e);
	});
}

function cleanRegion(){
	$.each(listRegions, function(i, delRegion){
		delRegion.setMap(null);
	});
	listRegions = [];
}

//--------------------------------------------------------------------------//
//------------------------------- cities -----------------------------------//
function selectCities(objRegion){

	$.ajax({
		url: 'dist/js/rras/cities.js',
		dataType: 'JSON'
	}).done(function(listALLMAPS) {
		$.ajax({
			url: 'http://127.0.0.1:5001/getMunicipiosFromRS/' + objRegion.id,
			dataType: 'JSON'
		}).done(function(listCitySelect) {
			$.each(listCitySelect, function(i, citySelect){	
				$.each(listALLMAPS, function(i, cityMap){
					if(citySelect.cod_ibge == cityMap.id){
						listCities.push(cityMap);
					}
				});
			});
		});
	});

	insertCities(listCities);
	insertHospitals(objRegion);
}

function insertCities(listCities){
	cleanCity();
	cleanMapLabel();

	$.each(listCities, function(i, objCity){
		
		var mapCity = new google.maps.Polygon({
				paths: objCity.latlng,
				strokeWeight: 1,
				strokeOpacity: 0.5,
				strokeColor: "#000000",
				fillOpacity: 0,
				fillColor: "#FFFFFF"
			});

			mapCity.setMap(map);
			listMapCity.push(mapCity);
	});
	cleanListCity();
}

function cleanListCity(){
	listCities = [];
}

function cleanCity(){
	$.each(listMapCity, function(i, delCity){
		delCity.setMap(null);
	});
	listMapCity = [];
}

//--------------------------------------------------------------------------//
//------------------------------- hospitals -----------------------------------//
function insertHospitals(objRegion){
	cleanMarkers();

	$.ajax({
		url: 'http://127.0.0.1:5001/getHealthcareEstablishmentsFromRS/' + objRegion.id,
		dataType: 'JSON'
	}).done(function(listHospitals) {

		$.each(listHospitals, function(i, objHospital) {
			var marker = new google.maps.Marker({
				map: map,
				position: new google.maps.LatLng(objHospital.lat, objHospital.lng),
				label: objHospital.idHospital
			});

			listMarkers.push(marker);

			marker.addListener('click', function() {
				var infoWindow = new google.maps.InfoWindow;
				var infoWinContent = document.createElement('div');
	
				var nameHospital = document.createElement('strong');
				nameHospital.textContent = objHospital.nome_fantasia;
				infoWinContent.appendChild(nameHospital).appendChild(document.createElement('br'));
		
				infoWindow.setContent(infoWinContent);
				infoWindow.open(map, marker);
			});

		});
		setCluster();
	});
}

function setCluster(){

	markerCluster = new MarkerClusterer(map, listMarkers, {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
}

function cleanMarkers(){
	if(markerCluster != null){
		markerCluster.removeMarkers(listMarkers);
	}

	$.each(listMarkers, function(i, marker){
		marker.setMap(null);
	});
	listMarkers = [];
}