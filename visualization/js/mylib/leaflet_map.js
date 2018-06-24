function leaflet_map(){

	var map = new L.map('main');
	map.setView([40.73, -74.0060], 2);          // larger value, zoom in

	// var CartoDB_Positron = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
	// 	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
	// 	subdomains: 'abcd'
	// }).addTo(map);
	var OpenStreetMap_BlackAndWhite = L.tileLayer('http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', {
		maxZoom: 18,
		attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
	}).addTo(map);

	this.drawAirport = function (airport_file){
		$.getJSON(airport_file, function(data){
			console.log('data length: ', data.features.length);
			var style = {"radius": 3, "color": "steelblue", "opacity": .4, "fillOpacity": .4};

			var circle_layer = L.geoJson(data, {pointToLayer: function(feature, latlng){

				var circle = L.circle(latlng, {radius: style.radius, color: style.color, opacity: style.opacity,
										       fillOpacity: style.fillOpacity});	
				circle.on("click", function(e){
					var clickedCircle = e.target;
					circle.bindPopup('Code:'+ feature.properties.code);
				});

				return circle;

			}}).addTo(map);

		});
	}


	this.drawRoute = function(route_file){ 
		var routes = [];

		var routesOverlay = L.d3SvgOverlay(function(sel,proj){

		    var routesUpd = sel.selectAll('line').data(routes);
		    routesUpd.enter()
			         .append('line')
			         .attr('x1',function(d){return proj.latLngToLayerPoint(d.src_latLng).x;})
			         .attr('y1',function(d){return proj.latLngToLayerPoint(d.src_latLng).y;})
			         .attr('x2',function(d){return proj.latLngToLayerPoint(d.tar_latLng).x;})
			         .attr('y2',function(d){return proj.latLngToLayerPoint(d.tar_latLng).y;})
			         .attr('stroke','black')
			         .attr('stroke-width', .5);
		});

		d3.csv("../../data/csv/routes2008.csv",function(data){

		  	routes = data.map(function(r){
		  		var src_pos_str = r.src_pos.slice(1,-1), tar_pos_str = r.tar_pos.slice(1,-1);
		  		r.src_latLng = [parseFloat(src_pos_str.split(',')[0]), parseFloat(src_pos_str.split(',')[1])],     // [lat, lng]
		  		r.tar_latLng = [parseFloat(tar_pos_str.split(',')[0]), parseFloat(tar_pos_str.split(',')[1])];

		  		return r;
		  	});
	
		 	routesOverlay.addTo(map);
		});

	}


}

