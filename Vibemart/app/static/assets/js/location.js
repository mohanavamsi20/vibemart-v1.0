var apiKey = '50032e12944a48a29093404c35c83981'; // Replace with your API key

function getStates() {
  var country = document.getElementById('countrySelect').value;
  
  // Make an API request to get states based on the selected country
  $.getJSON(`https://api.opencagedata.com/geocode/v1/json?q=${country}&key=${apiKey}`, function(data) {
    var stateSelect = document.getElementById('stateSelect');
    stateSelect.innerHTML = '<option value="">Select State</option>'; // Reset state dropdown
    
    var results = data.results;
    var states = results[0].components.state || results[0].components.region; // Extract state or region information
    
    if (states) {
      if (Array.isArray(states)) {
        for (var i = 0; i < states.length; i++) {
          var state = states[i];
          var option = document.createElement('option');
          option.text = state;
          option.value = state;
          stateSelect.appendChild(option);
        }
      } else {
        var option = document.createElement('option');
        option.text = states;
        option.value = states;
        stateSelect.appendChild(option);
      }
    }
  });
}

function getCities() {
  var country = document.getElementById('countrySelect').value;
  var state = document.getElementById('stateSelect').value;
  
  // Make an API request to get cities based on the selected country and state
  $.getJSON(`https://api.opencagedata.com/geocode/v1/json?q=${state},${country}&key=${apiKey}`, function(data) {
    var citySelect = document.getElementById('citySelect');
    citySelect.innerHTML = '<option value="">Select City</option>'; // Reset city dropdown
    
    var results = data.results;
    for (var i = 0; i < results.length; i++) {
      var city = results[i].components.city || results[i].components.town || results[i].components.village; // Extract city, town, or village information
      if (city) {
        var option = document.createElement('option');
        option.text = city;
        option.value = city;
        citySelect.appendChild(option);
      }
    }
  });
}

function getZipCodes() {
  var country = document.getElementById('countrySelect').value;
  var state = document.getElementById('stateSelect').value;
  var city = document.getElementById('citySelect').value;
  
  // Make an API request to get zip codes based on the selected country, state, and city
  $.getJSON(`https://api.opencagedata.com/geocode/v1/json?q=${city},${state},${country}&key=${apiKey}`, function(data) {
    var zipSelect = document.getElementById('zipSelect');
    zipSelect.innerHTML = '<option value="">Select Zip Code</option>'; // Reset zip code dropdown
    
    var results = data.results;
    for (var i = 0; i < results.length; i++) {
      var zipCode = results[i].components.postcode; // Extract zip code information
      if (zipCode) {
        var option = document.createElement('option');
        option.text = zipCode;
        option.value = zipCode;
        zipSelect.appendChild(option);  
      }
    }
  });
}
