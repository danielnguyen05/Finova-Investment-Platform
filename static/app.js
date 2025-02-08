particlesJS('particles-js',
  
  {
    "particles": {
      "number": {
        "value": 80,
        "density": {
          "enable": true,
          "value_area": 800
        }
      },
      "color": {
        "value": "#ffffff"
      },
      "shape": {
        "type": "circle",
        "stroke": {
          "width": 0,
          "color": "#000000"
        },
        "polygon": {
          "nb_sides": 5
        },
        "image": {
          "src": "img/github.svg",
          "width": 100,
          "height": 100
        }
      },
      "opacity": {
        "value": 0.5,
        "random": false,
        "anim": {
          "enable": false,
          "speed": 1,
          "opacity_min": 0.1,
          "sync": false
        }
      },
      "size": {
        "value": 5,
        "random": true,
        "anim": {
          "enable": false,
          "speed": 40,
          "size_min": 0.1,
          "sync": false
        }
      },
      "line_linked": {
        "enable": true,
        "distance": 150,
        "color": "#ffffff",
        "opacity": 0.4,
        "width": 1
      },
      "move": {
        "enable": true,
        "speed": 6,
        "direction": "none",
        "random": false,
        "straight": false,
        "out_mode": "out",
        "attract": {
          "enable": false,
          "rotateX": 600,
          "rotateY": 1200
        }
      }
    },
    "interactivity": {
      "detect_on": "canvas",
      "events": {
        "onhover": {
          "enable": true,
          "mode": "repulse"
        },
        "onclick": {
          "enable": true,
          "mode": "push"
        },
        "resize": true
      },
      "modes": {
        "grab": {
          "distance": 400,
          "line_linked": {
            "opacity": 1
          }
        },
        "bubble": {
          "distance": 400,
          "size": 40,
          "duration": 2,
          "opacity": 8,
          "speed": 3
        },
        "repulse": {
          "distance": 200
        },
        "push": {
          "particles_nb": 4
        },
        "remove": {
          "particles_nb": 2
        }
      }
    },
    "retina_detect": true,
    "config_demo": {
      "hide_card": false,
      "background_color": "#b61924",
      "background_image": "",
      "background_position": "50% 50%",
      "background_repeat": "no-repeat",
      "background_size": "cover"
    }
  }
);

// Function to fetch investment data from Flask API and update the graph
function updateGraph() {
  // Get user input values from the form
  const principal = parseFloat(document.getElementById("principal").value);
  const aggro = document.getElementById("risk").value;

  // Validate user input
  if (isNaN(principal) || principal <= 0) {
      alert("Please enter a valid principal amount.");
      return;
  }

  // Send POST request to Flask API
  fetch("https://finova-du4r.onrender.com/api/investment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ principal, aggro }) // Send input as JSON
  })
  .then(response => response.json()) // Parse JSON response
  .then(data => {
      // Prepare Plotly traces
      let trace1 = {
          x: data.t,
          y: data.expected,
          mode: "lines",
          name: "Expected Growth",
          line: { color: "white", width: 2 }
      };

      let trace2 = {
          x: [...data.t, ...data.t.reverse()],
          y: [...data.upper, ...data.lower.reverse()],
          fill: "toself",
          fillcolor: "rgba(173, 216, 230, 0.3)",
          line: { color: "transparent" },
          name: "Variance Range",
          type: "scatter"
      };

      let layout = {
          title: "Investment Growth Over Time",
          xaxis: { title: "Years" },
          yaxis: { title: "Investment Value ($)", type: "log" }, // Log scale to manage exponential growth
          plot_bgcolor: "rgb(51, 153, 255)",
          paper_bgcolor: "rgb(51, 153, 255)",
          font: { color: "white" }
      };

      // Render the graph in the "graph" div
      Plotly.newPlot("graph", [trace2, trace1], layout);
  })
  .catch(error => console.error("Error fetching investment data:", error));
}

