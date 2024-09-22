

async function run() {
    // Initialize variable to track locked state
    var isLocked = false;

    // Function to display nodes and links in the SVG
    function display(svg, nodes, links) {
        console.log("Display function called with nodes:", nodes);
        // Create links
        var link = svg.selectAll(".link")
            .data(links)
            .enter().append("line")
            .attr("class", "link")
            .style("stroke-width", 1)
            .style("stroke", "black");

        // Create nodes
        var node = svg.selectAll(".node")
            .data(nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("id", d => "node-" + d.name.replace(/[^a-zA-Z0-9]/g, '')) // Assign unique identifier
            .attr("r", d => Math.sqrt(d.value) * 2)
            .style("fill", d => d.colour)
            .each(function (d) {
                // Store original radius in node data
                d.originalRadius = Math.sqrt(d.value) * 2;
            })
            .on("click", function (event, d) {
                // Toggle node selection
                var selected = d3.select(this).classed("selected");
                d3.select(this).classed("selected", !selected);

                // Lock or unlock hover effects and info box based on click state
                isLocked = !isLocked;

                // Find corresponding node in the other SVG
                var correspondingNode = svg === svg1 ? svg2.select("#node-" + d.name.replace(/[^a-zA-Z0-9]/g, '')) :
                    svg1.select("#node-" + d.name.replace(/[^a-zA-Z0-9]/g, ''));
                if (!correspondingNode.empty()) {
                    // Highlight corresponding node in the other SVG
                    correspondingNode.classed("selected", !correspondingNode.classed("selected"));
                }
            })
            // Mouseover event for nodes
            .on("mouseover", function (event, d) {
                if (!isLocked) {
                    // Increase the radius when hovering over the node
                    d3.select(this)
                        .attr("r", d.originalRadius * 2);

                    // Highlight links connected to the hovered node
                    link.filter(link => link.source === d || link.target === d)
                        .style("stroke", "green")
                        .style("stroke-width", 2);

                    // Reduce opacity of all other links
                    link.filter(link => !(link.source === d || link.target === d))
                        .style("opacity", 0.09);
                }
            })

            // Mouseout event for nodes
            .on("mouseout", function (event, d) {
                if (!isLocked) {
                    // Restore the original radius when hovering out
                    d3.select(this)
                        .attr("r", d.originalRadius);

                    // Revert the color of links connected to the hovered node
                    link.filter(link => link.source === d || link.target === d)
                        .style("stroke", "black")
                        .style("stroke-width", 1);

                    // Restore opacity of all other links
                    link.filter(link => !(link.source === d || link.target === d))
                        .style("opacity", 1);
                }
            });



        // Add node labels
        var text = svg.selectAll(".text")
            .data(nodes)
            .enter().append("text")
            .attr("class", "text")

            .text(d => "")
            .style("opacity", 0); // Initially hide the names

        // Mouseenter event to display name and update info boxes
        node.on("mouseenter", function (event, d) {
            // Determine which info box to update based on the position of the mouse
            var mouseX = event.pageX;
            var windowWidth = window.innerWidth;
            var infoBoxId = mouseX < windowWidth / 2 ? "info-box1" : "info-box2";

            // Display node name and directly linked node names in the corresponding info box
            var linkedNodeNames = [];
            links.forEach(link => {
                if (link.source === d || link.target === d) {
                    if (link.source === d) linkedNodeNames.push(link.target.name);
                    if (link.target === d) linkedNodeNames.push(link.source.name);
                }
            });

            document.getElementById(infoBoxId).innerText = d.name + ", appears in " + d.value + " scenes. Appears with: " + linkedNodeNames.join(", ");

            d3.select(this.parentNode).select(".text")
                .text(d.name)
                .style("opacity", 1) // Show the name
                .attr("x", d.x + 12) // Position the text next to the node
                .attr("y", d.y);
        });



        // Mouseleave event to hide name and clear info boxes
        node.on("mouseleave", function (event, d) {
            // Determine which info box to clear based on the position of the mouse
            var mouseX = event.pageX;
            var windowWidth = window.innerWidth;
            var infoBoxId = mouseX < windowWidth / 2 ? "info-box1" : "info-box2";

            // Display node name and directly linked node names in the corresponding info box
            var linkedNodeNames = [];
            links.forEach(link => {
                if (link.source === d || link.target === d) {
                    if (link.source === d) linkedNodeNames.push(link.target.name);
                    if (link.target === d) linkedNodeNames.push(link.source.name);
                }
            });

            // Clear the corresponding info box
            document.getElementById(infoBoxId).innerText = "";

            d3.select(this.parentNode).select(".text")
                .text("")
                .style("opacity", 0); // Hide the name
        });

        // Mouseenter event for links
        link.on("mouseenter", function (event, d) {
            // Determine which info box to update based on the position of the mouse
            var mouseX = event.pageX;
            var windowWidth = window.innerWidth;
            var infoBoxId = mouseX < windowWidth / 2 ? "info-box1" : "info-box2";

            // Display source and target node names and their values in the corresponding info box
            document.getElementById(infoBoxId).innerText = "Link between " + d.source.name + " and " + d.target.name + ". Value: " + d.value;

            // Highlight source and target nodes
            d3.select("#node-" + d.source.name.replace(/[^a-zA-Z0-9]/g, '')).classed("selected-link", true);
            d3.select("#node-" + d.target.name.replace(/[^a-zA-Z0-9]/g, '')).classed("selected-link", true);

            // Make the link thicker and pink
            d3.select(this)
                .style("stroke-width", 4)
                .style("stroke", "pink");
        });

        // Mouseleave event for links
        link.on("mouseleave", function (event, d) {
            // Determine which info box to clear based on the position of the mouse
            var mouseX = event.pageX;
            var windowWidth = window.innerWidth;
            var infoBoxId = mouseX < windowWidth / 2 ? "info-box1" : "info-box2";

            // Clear the corresponding info box
            document.getElementById(infoBoxId).innerText = "";

            // Remove highlight from source and target nodes
            d3.select("#node-" + d.source.name.replace(/[^a-zA-Z0-9]/g, '')).classed("selected-link", false);
            d3.select("#node-" + d.target.name.replace(/[^a-zA-Z0-9]/g, '')).classed("selected-link", false);

            // Restore the default link style
            d3.select(this)
                .style("stroke-width", d => Math.sqrt(d.value))
                .style("stroke", "black")
                .style("stroke-width", 1);
        });

        // Define the width and height of your SVG container
        var width = +svg.attr("width");
        var height = +svg.attr("height");
        // Configure the force simulation
        var simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.name).distance(250)) // Increase the distance between nodes
            .force("charge", d3.forceManyBody(-600))
            .force("center", d3.forceCenter(svg.attr("width") / 2, svg.attr("height") / 2))
            // Add forces from the sides
            .force("x", d3.forceX().strength(0.01).x(0.5 * width)) // Attraction towards the horizontal center
            .force("y", d3.forceY().strength(0.01).y(0.5 * height)); // Attraction towards the vertical center

        // Update node and link positions during simulation
        simulation.on("tick", () => {
            link.attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node.attr("cx", d => d.x)
                .attr("cy", d => d.y);

            text.attr("x", d => d.x + 10)
                .attr("y", d => d.y);
        });
    }

    // Function to create nodes and links
    function createNodesAndLinks(episodeData) {
        var nodes = episodeData.nodes.map(node => ({
            name: node.name,
            value: node.value,
            colour: node.colour
        }));

        var links = episodeData.links.map(link => ({
            source: link.source,
            target: link.target,
            value: link.value
        }));

        return { nodes, links };
    }

    // Update nodes and links based on checked episodes
    function updateNodesAndLinks(svg, checkedEpisodes) {
        var combinedNodesMap = {};
        var combinedLinks = {};

        Object.values(checkedEpisodes).forEach(episodesData => {
            var { nodes, links } = createNodesAndLinks(episodesData);

            nodes.forEach(node => {
                if (combinedNodesMap[node.name]) {
                    combinedNodesMap[node.name].value += node.value;
                } else {
                    combinedNodesMap[node.name] = { ...node };
                }
            });

            links.forEach(link => {
                var sourceName = nodes[link.source].name;
                var targetName = nodes[link.target].name;
                var combinedLinkKey = sourceName + "-" + targetName;

                if (combinedLinks[combinedLinkKey]) {
                    combinedLinks[combinedLinkKey].value += link.value;
                } else {
                    combinedLinks[combinedLinkKey] = {
                        source: sourceName,
                        target: targetName,
                        value: link.value
                    };
                }
            });
        });

        var combinedNodes = Object.values(combinedNodesMap);
        var combinedLinksArray = Object.values(combinedLinks);

        svg.selectAll("*").remove();
        display(svg, combinedNodes, combinedLinksArray);
    }

    // Initialize objects to store episode data for checked episodes
    var checkedEpisodes1 = {};
    var checkedEpisodes2 = {};

    // Fetch data for all episodes
    var episodesData = [];
    for (let i = 1; i <= 7; i++) {
        var episodeData = await fetch(`data/starwars-episode-${i}-interactions-allCharacters.json`).then(response => response.json());
        episodesData.push(episodeData);
    }

    // Create SVG for episode data (svg1)
    var svg1 = d3.select("body").append("svg")
        .attr("width", window.innerWidth / 2)
        .attr("height", window.innerHeight)
        .classed("svg-container1", true);

    // Create SVG for episode data (svg2)
    var svg2 = d3.select("body").append("svg")
        .attr("width", window.innerWidth / 2)
        .attr("height", window.innerHeight)
        .classed("svg-container2", true);

    // Add event listeners for the checkboxes in menu1
    document.querySelectorAll('#menu .episode').forEach(item => {
        item.addEventListener('change', async event => {
            var episodeNumber = parseInt(event.target.value);
            if (event.target.checked) {
                // Load data for the selected episode if not already loaded
                if (!checkedEpisodes1[episodeNumber]) {
                    checkedEpisodes1[episodeNumber] = await fetch(`data/starwars-episode-${episodeNumber}-interactions-allCharacters.json`).then(response => response.json());
                }
            } else {
                delete checkedEpisodes1[episodeNumber];
            }

            // Update nodes and links based on checked episodes for svg1
            updateNodesAndLinks(svg1, checkedEpisodes1);
        });
    });

    // Add event listeners for the checkboxes in menu2
    document.querySelectorAll('#menu2 .episode').forEach(item => {
        item.addEventListener('change', async event => {
            var episodeNumber = parseInt(event.target.value);
            if (event.target.checked) {
                // Load data for the selected episode if not already loaded
                if (!checkedEpisodes2[episodeNumber]) {
                    checkedEpisodes2[episodeNumber] = await fetch(`data/starwars-episode-${episodeNumber}-interactions-allCharacters.json`).then(response => response.json());
                }
            } else {
                delete checkedEpisodes2[episodeNumber];
            }

            // Update nodes and links based on checked episodes for svg2
            updateNodesAndLinks(svg2, checkedEpisodes2);
        });
    });
}

run();
