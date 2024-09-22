/**
 *
    Author: Kahin Akram
    Date: Jan 24, 2020
    TNM048 Lab 1 - Visual Information-Seeking Mantra
    Leaflet map file
 *
*/


// Errors
// The dots does not sow up pin the right place on the map
// The dots, when brushing, does not always go back to its original size
// The y-axis does not go from 0-9 but ~1



function worldMap(data) {

    /**
     * Task 14 - Create a leaflet map and put center to 10,15 with zoom scale of 1
     * Create map.
     */

    var leaflet_map = L.map("mapid").setView([10, 15], 1); //&

    /**
     * Task 15 - Get the tileLayer from the link at the bottom of this file
     * and add it to the map created above.
     * Assign the variable mapLink to .tileLayer on L with map link() as the parameter. 
     * Then use .addTo() and add leaflet map to mapLink.
     * 
     * Display map in "tiles"
    */

    //tileLayer = L.tileLayer(map_link()).addTo(leaflet_map);
    L.tileLayer(map_link()).addTo(leaflet_map);

    /**
     * Task 16 - Create an svg call on top of the leaflet map.
     * Also append a g tag on this svg tag and add class leaflet-zoom-hide.
     * This g tag will be needed later.
     * 
     * svg map and use d3.select(), .getPanes().overlayPane, and .append() to
     * create the svg map. Assign svg map to d3.select() with .getPanes().overlayPane from leaflet map
     * as the parameter and then append “svg” to the d3.select(). Now create another variable
     * 
     * Svg lets us place the dots on toop of the map later. The g elemnt groups these svg elemnts togheter
     * 
     */

    let svg_map = d3.select(leaflet_map.getPanes().overlayPane).append("svg");
    let g = svg_map.append("g").attr("class", "leaflet-zoom-hide");

    /**
     * Task 17 - Create a function that projects lat/lng points on the map.
     * Use latLngToLayerPoint, remember which goes where.
     * 
     * Create a function called projectPointsOnMap that takes x, y points and projects it on the map.
     * Inside the function create a variable called point and use latLngToLayerPoint on leaflet map to
     * create a new L.LatLng(). Now use this.stream on the point with the point.x, point.y.
     * 
     * projectPointsOnMap takes latitude and longitude coordinates as input and projects them onto the Leaflet map. (coorect when zooming)
     * Leaflet's latLngToLayerPoint method is used to convert geographic coordinates 
     * (latitude and longitude) to pixel coordinates on the map's overlay pane
     */

    function projectPointsOnMap(x, y){
        var point = leaflet_map.latLngToLayerPoint(new L.LatLng(y, x));
        this.stream.point(point.x, point.y);
    }

    /**
     * Task 18 - Now we need to transform all to the specific projection
     * create a variable called transform and use d3.geoTransform with the function above a parameter
     * {point:function.}
     * Create another variable names d3geoPath to project this transformation to it.
     * 
     * Task 18 involves transforming geographic coordinates (latitude and longitude) into SVG coordinates 
     * for accurate plotting on the Leaflet map's SVG overlay. This transformation is necessary to ensure 
     * that data points or graphical elements are correctly positioned relative to the map's viewport.
     */
    //Transforming to the specific projection
    var d3path = d3.geoPath().projection(d3.geoTransform({ point: projectPointsOnMap }));

    // similar to projectPoint this function converts lat/long to
    //svg coordinates except that it accepts a point from our
    //GeoJSON
    function applyLatLngToLayer(d) {
        var x = d.geometry.coordinates[0];
        var y = d.geometry.coordinates[1];
        //Remove comment when reached task 19
        return leaflet_map.latLngToLayerPoint(new L.LatLng(y, x));
    }

    //<---------------------------------------------------------------------------------------------------->

    /**
     * Task 19 - Plot the dots on the map
     * Create a variable and name it feature.
     * select all circle from g tag and use data.features.
     * Also add a class called mapcircle and set opacity to 0.4
     * 
     * Create a variable and name it feature. Select all circle from g tag and use
     * data.features. Also, add a class called mapcircle and set opacity to a desired value.
     * 
     * Plot the points 
     * creating SVG circles to represent each data point and adding them to the map's SVG overlay.
     */
    //features for the points

    //select all existing circle elements within the SVG group (g) that was previously appended to the SVG overlay. 
    //It prepares to bind data to these circle elements.
    var feature = g.selectAll("circle")

    //binds the provided data (data.features) to the selected circle elements. This means each data point will 
    //be associated with a circle element, allowing for visualization on the map.
    .data(data.features)

    //returns a selection representing the data elements for which no corresponding circle element currently exists. 
    //It indicates the "enter" selection, representing new data points that need to be added to the visualization.
    .enter()

    //For each new data point in the "enter" selection, this line appends a new circle element to represent the 
    //data point visually on the map.
    .append("circle")

    //sets the "class" attribute of each circle element to "mapcircle". The "mapcircle" class can be used 
    //later for styling or targeting these circle elements in CSS or JavaScript.
    .attr("class", "mapcircle")

    //sets the "opacity" attribute of each circle element to 0.9, making them slightly transparent. 
    //This opacity value determines the level of transparency for the circles, with 0 being fully transparent and 1 being fully opaque.
    .attr("opacity", 0.3);


    /**
     * Task 20 - Call the plot function with feature variable
     * not integers needed.
     * 
     * Plot the points on the map
     */
    var points = new Points();
    points.plot(feature);

    //Redraw the dots each time we interact with the map
    //Remove comment tags when done with task 20
    leaflet_map.on("moveend", reset);
    reset();

    //Mouseover
    //Remove comment tags when done with task 20
    mouseOver(feature);
    mouseOut(feature);

    //Mouse over function
    function mouseOver(feature){

        feature
            .on("mouseover", function (d) {
                selection = d3.select(this)
                    .attr('r', 15)
                //Update the tooltip position and value
                points.tooltip(d);

                //Uncomment if implemented
                focus_plus_context.hovered();

            });
    }

    //Mouse out function
    function mouseOut(feature){

        feature
            .on("mouseout", function () {
                d3.select(this)
                    .transition()
                    .duration(500)
                    .attr("r", function (d) {
                        if (d.properties.DEATHS == null) {
                            return 3;
                        }
                        else {
                            return scaleQuantRad(d.properties.DEATHS);
                        }
                    });

            });
    }

    // Recalculating bounds for redrawing points each time map changes
    function reset() {
        var bounds = d3path.bounds(data)
        topLeft = [bounds[0][0] + 10, bounds[0][1] - 10]
        bottomRight = [bounds[1][0] + 10, bounds[1][1] + 10];

        // Setting the size and location of the overall SVG container
        svg_map
            .attr("width", bottomRight[0] - topLeft[0])
            .attr("height", bottomRight[1] - topLeft[1])
            .style("left", topLeft[0] + "px")
            .style("top", topLeft[1] + "px");

        g.attr("transform", "translate(" + (-topLeft[0]) + "," + (-topLeft[1]) + ")");

        feature.attr("transform",
            function (d) {
                return "translate(" +
                    applyLatLngToLayer(d).x + "," +
                    applyLatLngToLayer(d).y + ")";
            });
    }

    //<---------------------------------------------------------------------------------------------------->

    /**
     * Update the dots on the map after brushing
     */
    this.change_map_points = function (curr_view_erth) {

        map_points_change = d3.selectAll(".mapcircle")
            .filter(function (d) { return curr_view_erth.indexOf(d.id) != -1; })
            .attr('r', 7)
            .transition()
            .duration(800);

        //Call plot funtion.
        points.plot(map_points_change)

        d3.selectAll(".mapcircle")
            .filter(function (d) { return curr_view_erth.indexOf(d.id) == -1; })
            .transition()
            .duration(800)
            .attr('r', 0)
    }

    //<---------------------------------------------------------------------------------------------------->

    /**
     * Function for hovering the points, implement if time allows.
     */
    this.hovered = function (input_point) {
        console.log("If time allows you, implement something here!");
    }
    // We have time but the code does not work. :(

    //<---------------------------------------------------------------------------------------------------->

    //Link to get the leaflet map
    function map_link() {
        return "https://api.mapbox.com/styles/v1/josecoto/civ8gwgk3000a2ipdgnsscnai/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoiam9zZWNvdG8iLCJhIjoiY2l2OGZxZWNuMDAxODJ6cGdhcGFuN2IyaCJ9.7szLs0lc_2EjX6g21HI_Kg";
    }

}