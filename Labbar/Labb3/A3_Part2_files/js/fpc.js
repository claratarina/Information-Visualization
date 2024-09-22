/**
 *
    Author: Kahin Akram
    Date: Jan 24, 2020
    TNM048 Lab 1 - Visual Information-Seeking Mantra
    Focus+Context file
 *
*/
function focusPlusContext(data) {

    // Creating margins and figure sizes
    var margin = { top: 20, right: 20, bottom: 150, left: 40 },
        margin2 = { top: 100, right: 20, bottom: 50, left: 40 },
        width = $("#scatterplot").parent().width() - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom,
        height2 = 200 - margin2.top - margin2.bottom;

    /**
     * Select Scatter plot div and append svg tag to it.
     * Set position to relative and width to 100% and an arbitrary height
     * Then add the clipping area with clipPath -
     * The clipping path restricts the region to which paint can be applied.
     * After that, append the two g tags we will be using for drawing the focus plus context graphs
     */
    var svg = d3.select("#scatterplot").append("svg")
        .attr("postion", "relative")
        .attr("width", "100%")
        .attr("height", height + margin.top + margin.bottom);

    svg.append("defs").append("clipPath")
        .attr("id", "clip")
        .append("rect")
        .attr("width", width)
        .attr("height", height);

    var focus = svg.append("g")
        .attr("class", "focus")
        .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

    var context = svg.append("g")
        .attr("class", "context")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    //<---------------------------------------------------------------------------------------------------->

    /**
     * Task 1 - Parse date with timeParse to year-month-day
     * Create time variable to use it later, when ooming in on the scale
     */
     let parseDate = d3.timeParse("%Y-%m-%d");

    /**
     * Task 2 - Define scales and axes for scatterplot
     * Create scale and axis for the scatterplot, scale for when "zooming" in and axis for the axis.
     */
    // Import D3 library
    var xScale = d3.scaleTime().range([0, width]);
    var yScale = d3.scaleLinear().range([height, 0]);
    var xAxis = d3.axisBottom(xScale);
    var yAxis = d3.axisLeft(yScale);

    /**
     * Task 3 - Define scales and axes for context (Navigation through the data)
     * Create the scale and the axis for the smail plot on the top, to navigate through the system.
     */
    // Define width and height of the context area
    var navXScale = d3.scaleTime().range([0, width]);
    var navYScale = d3.scaleLinear().range([height2, 0]); //height2 - 0
    var navXAxis = d3.axisBottom(navXScale);


    /**
     * Task 4 - Define the brush for the context graph (Navigation)
     * The brush functionality is the change in size and aditional information when brushing the mouse over a specific dot.
     * Several views of the same information. 
     */
    //brush functionality implemented
    // Define the brush variable and assign it to d3.brushX()
    var brush = d3
    .brushX()
    .extent([[0, 0], [width, height2]]) //([[0, 0], [width, height]])
    .on("brush end", brushed);

    //Setting scale parameters
    var maxDate = d3.max(data.features, function (d) { return parseDate(d.properties.Date) });
    var minDate = d3.min(data.features, function (d) { return parseDate(d.properties.Date) });
    var maxMag = d3.max(data.features, function (d) { return d.properties.EQ_PRIMARY });
    var minMag = d3.min(data.features, function (d) { return d.properties.EQ_PRIMARY })

    //Calculate todays date.
    maxDate_plus = new Date(maxDate.getTime() + 300 * 144000000)

    /**
     * Task 5 - Set the axes scales, both for focus and context.
     * We have deifined these scale variables and now we will use them by settign the axis. 
     */
    // Assuming you have already defined xScale, yScale, navXScale, and navYScale

    // Scale using parameters
    xScale.domain([minDate, maxDate]);

    yScale.domain([0, maxMag]); 

    navXScale.domain([minDate, maxDate]);

    navYScale.domain([minMag, maxMag]);


    //<---------------------------------------------------------------------------------------------------->

    /**
    * 1. Rendering the context chart
    */

    //Append g tag for plotting the dots and axes
    var dots = context.append("g");
    dots.attr("clip-path", "url(#clip)");

    /**
    * Task 6 - Call the navigation axis on context.
    */
    context.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height2 + ")")
        //here..
        .call(navXAxis);

    /**
     * Task 7 - Plot the small dots on the context graph.
     * To get the overview we plot the dots in the context-bar. 
     */
    small_points = dots
        .selectAll("dot")
        //here...
        .data(data.features)
        .enter()
        .append("circle")
        .attr("class", "dotContext")
        .filter(function (d) { return d.properties.EQ_PRIMARY != null })
        .attr("cx", function (d) {
            return navXScale(parseDate(d.properties.Date));
        })
        .attr("cy", function (d) {
            return navYScale(d.properties.EQ_PRIMARY);
        });

     /**
      * Task 8 - Call plot function.
      * plot(points,nr,nr) try to use different numbers for the scaling.
      * Parameters:
      * small dots: the points
      * 100: affects if the parameter "no data availabel" is shown or not
      * 2: size of dots
      */
      let points = new Points();
      points.plot(small_points, 100, 2); 
      // 1st attribute: affects if "no data available" is shown or not
      // 2nd attribute: dot size, bigger number -> smaller dots

    //<---------------------------------------------------------------------------------------------------->

    /**
    * 2. Rendering the focus chart
    */

    //Append g tag for plotting the dots and axes
    var dots = focus.append("g");
    dots.attr("clip-path", "url(#clip)");

    /**
     * Task 10 - Call x and y axis
     * Here the x and y axis are called and used. The axix gets its placement on the visualsation board. 
     * translate is used to place it below the context graph. 
     */
    focus.append("g")
    //here..
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0, " + height + ")")
    .call(xAxis);
    
    focus.append("g")
    //here..
    .attr("class", "axis axis--y")
    .call(yAxis);

    //Add y axis label to the scatter plot
    d3.select(".legend")
        .style('left', "170px")
        .style('top', '300px');
    svg.append("text")
        .attr('class', "axis-label")
        .attr("transform", "rotate(-90)")
        .attr("y", 0)
        .attr('x', -margin2.top - 120)
        .attr('text-anchor', "end")
        .attr('dy', ".75em")
        .style("font-size", "20px")
        .text("Magnitude");

    /**
     * Task 11 - Plot the dots on the focus graph.
     * 
     * Use data.features together with .enter() and append “circle” as well as appending a class “dot” to
     * selected dots. Finally set the opacity to a desired value.
     */

    selected_dots = dots.selectAll("dot")
        //here..
        .data(data.features)
        .enter()
        .append("circle")
        .attr("class", "dot")
        .attr("style", "opacity: 0.9;")

        .filter(function (d) { return d.properties.EQ_PRIMARY != null })
        .attr("cx", function (d) {
            return xScale(parseDate(d.properties.Date));
        })
        .attr("cy", function (d) {
            return yScale(d.properties.EQ_PRIMARY);
        });


    /**
     * Task 12 - Call plot function
     * plot(points,nr,nr) no need to send any integers!
     */
     points.plot(selected_dots);

    //<---------------------------------------------------------------------------------------------------->

    //Mouseover function
    mouseOver(selected_dots);
    //Mouseout function
    mouseOut(selected_dots);

    //Mouse over function
    function mouseOver(selected_dots){
        selected_dots
        .on("mouseover",function(d){

            /**
             * Task 13 - Update information in the "tooltip" by calling the tooltip function.
             * .tooltip() on the points variable with d as the parameter
             * The hoover function, determine size of the dots when hoovering, 
             */
             points.tooltip(d);

            //Rescale the dots onhover
            d3.select(this).attr('r', 15)

            //Rescale the dots on the map.
            curent_id = d3.select(this)._groups[0][0].__data__.id.toString()
            d3.selectAll(".mapcircle")
                .filter(function (d) { return d.id === curent_id; })
                .attr('r', 15)

            //Call map hover function if implemented!
            //world_map.hovered(d.id);
        });
    }

    //Mouse out function
    function mouseOut(selected_dots){
        selected_dots
            .on("mouseout", function () {
                //Returning to original characteristics
                d3.select(this)
                    .transition()
                    .duration(500)
                    .attr("r", function (d) {
                        if (d.properties.DEATHS == null) {
                            return 3
                        }
                        else {
                            return scaleQuantRad(d.properties.DEATHS);
                        }
                    })

                //Reset all the dots on the map
                d3.selectAll(".mapcircle")
                    .filter(function (d) { return d.id === curent_id; })
                    .transition()
                    .duration(500)
                    .attr("r", function (d) {
                        if (d.properties.DEATHS == null) {
                            return 3
                        }
                        else {
                            return scaleQuantRad(d.properties.DEATHS);
                        }
                    })
            });
    }
    //<---------------------------------------------------------------------------------------------------->

    /**
     * Task 9 - Append the brush.
     * Brush must come last because we changes places of the focus and context plots.
     * The brush function is trying to access things in scatter plot which are not yet
     * implmented if we put the brush before.
     * 
     * use .append(), .attr(), and .call() to append a d3 g tag and a class named
     * brush to the context variable. Then call brush and use brush.move on xScale
     * .range() in another call.
     */

    //here..
    context
        .append("g")
        .attr("class", "brush")
        .call(brush)
        .call(brush.move, xScale.range());

    //<---------------------------------------------------------------------------------------------------->

    //Brush function for filtering through the data.
    function brushed(){
        //Function that updates scatter plot and map each time brush is used
        var s = d3.event.selection || navXScale.range();
        xScale.domain(s.map(navXScale.invert, navXScale));
        focus.selectAll(".dot")
            .filter(function (d) { return d.properties.EQ_PRIMARY != null })
            .attr("cx", function (d) {
                return xScale(parseDate(d.properties.Date));
            })
            .attr("cy", function (d) {
                return yScale(d.properties.EQ_PRIMARY);
            })

        focus.select(".axis--x").call(xAxis);

        if (d3.event.type == "end") {
            var curr_view_erth = []
            d3.selectAll(".dot").each(
                function (d, i) {
                    if (parseDate(d.properties.Date) >= xScale.domain()[0] &&
                        parseDate(d.properties.Date) <= xScale.domain()[1]) {
                        curr_view_erth.push(d.id.toString());
                    }
                });
            /**
             * Remove comment for updating dots on the map.
             */
            curr_points_view = world_map.change_map_points(curr_view_erth)
        }
    }

    //<---------------------------------------------------------------------------------------------------->

    /**
     * Function for hovering the points, implement if time allows.
     */
    this.hovered = function(){
        console.log("If time allows you, implement something here!");
    }

}