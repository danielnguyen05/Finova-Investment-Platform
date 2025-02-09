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

const API_BASE = "https://finova-du4r.onrender.com/api";

// 📌 Fetch Investment Data
function updateInvestmentGraph() {
    const principal = parseFloat(document.getElementById("principal").value);
    const aggro = document.getElementById("risk").value;

    if (isNaN(principal) || principal <= 0) {
        alert("Please enter a valid principal amount.");
        return;
    }

    fetch(`${API_BASE}/investment`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ principal, aggro })
    })
    .then(response => response.json())
    .then(data => {
        let trace1 = { x: data.t, y: data.expected, mode: "lines", name: "Expected Growth", line: { color: "white", width: 2 }};
        let trace2 = { x: [...data.t, ...data.t.reverse()], y: [...data.upper, ...data.lower.reverse()], fill: "toself", fillcolor: "rgba(173, 216, 230, 0.3)", line: { color: "transparent" }, name: "Variance Range", type: "scatter" };
        let layout = { title: "Investment Growth Over Time", xaxis: { title: "Years" }, yaxis: { title: "Investment Value ($)" }, plot_bgcolor: "rgb(51, 153, 255)", paper_bgcolor: "rgb(51, 153, 255)", font: { color: "white" } };
        Plotly.newPlot("investmentGraph", [trace2, trace1], layout);
    })
    .catch(error => console.error("Error fetching investment data:", error));
}

// 📌 Fetch Real GDP Data
function updateGDPGraph() {
    fetch(`${API_BASE}/economic`)
    .then(response => response.json())
    .then(data => {
        let trace = { x: data.dates, y: data.values, mode: "lines", name: "Real GDP", line: { color: "blue", width: 2 }};
        let layout = { title: "Real GDP Over Time", xaxis: { title: "Years" }, yaxis: { title: "Real GDP ($)" } };
        Plotly.newPlot("gdpGraph", [trace], layout);
    })
    .catch(error => console.error("Error fetching GDP data:", error));
}

// 📌 Fetch Real GDP Per Capita
function updateGDPPerCapitaGraph() {
    fetch(`${API_BASE}/economic/percapita`)
    .then(response => response.json())
    .then(data => {
        let trace = { x: data.dates, y: data.values, mode: "lines", name: "Real GDP Per Capita", line: { color: "green", width: 2 }};
        let layout = { title: "Real GDP Per Capita Over Time", xaxis: { title: "Years" }, yaxis: { title: "GDP Per Capita ($)" } };
        Plotly.newPlot("gdpPerCapitaGraph", [trace], layout);
    })
    .catch(error => console.error("Error fetching GDP Per Capita data:", error));
}

// 📌 Fetch Company Dividend Trends
function updateDividendsGraph() {
    const company = document.getElementById("company").value.toUpperCase();
    if (!company) {
        alert("Please enter a valid company ticker.");
        return;
    }

    fetch(`${API_BASE}/dividends/${company}`)
    .then(response => response.json())
    .then(data => {
        let trace = { x: data.dates, y: data.dividends, mode: "lines+markers", name: `Dividends for ${company}`, line: { color: "purple", width: 2 }};
        let layout = { title: `Dividend Trends for ${company}`, xaxis: { title: "Years" }, yaxis: { title: "Dividend Amount ($)" } };
        Plotly.newPlot("dividendsGraph", [trace], layout);
    })
    .catch(error => console.error("Error fetching dividend data:", error));
}

// 📌 Fetch Company Overview
function fetchCompanyOverview(company) {
    fetch(`${API_BASE}/company/${company}`)
    .then(response => response.json())
    .then(data => {
        let output = `
            <h3>${data.Name} (${data.Symbol})</h3>
            <p><strong>Sector:</strong> ${data.Sector}</p>
            <p><strong>Market Capitalization:</strong> ${data.MarketCapitalization}</p>
            <p><strong>Description:</strong> ${data.Description}</p>
        `;
        document.getElementById("companyOverview").innerHTML = output;
    })
    .catch(error => console.error("Error fetching company overview:", error));
}
