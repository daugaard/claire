
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>CLAIRE Model Visualizer</title>

    <!-- Bootstrap core CSS -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="/static/css/claire.css" rel="stylesheet">
  </head>

  <body>

    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
      <a class="navbar-brand" href="#">CLAIRE Model Visualizer</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarsExampleDefault">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
          </li>
        </ul>
      </div>
    </nav>

    <main role="main">

      <!-- Main jumbotron for a primary marketing message or call to action -->
      <div class="jumbotron">
        <div class="container">
          <h1 class="display-3">CLAIRE Model Visualizer!</h1>
          <p>This visualizer will help you understand how changing sensor and time values will impact the state of your devices for a specific AI model.</p>
          <p>To use the visualizer simply change the sensor and time values and press the "Calculate" button to see the result of running the AI model on the sensor input parameters.</p>
        </div>
      </div>

      <form id="main-form" action="/calculate">
        <div class="container">
          <div class="row">
            <div class="col-md-12">
              <h2>{{home.name}}</h2>
              <p>Home ID: {{home.home_id}}</p>
              <div class="row">
                <div class="col-md-4">
                  <div class="form-group">
                    <label for="time">Time:</label>
                    <input name="time" type="datetime-local" value="{{time.strftime("%Y-%m-%dT%H:%M")}}" class="form-control">
                  </div>
                </div>
              </div>
              <p><input type="submit" class="btn btn-primary" value="Calculate"/></p>
            </div>
          </div>

          <hr/>


          <!-- Example row of columns -->
          <div class="row">
            % for device in home.devices:
                % if device.type in ('BinarySensorDevice', 'BinaryPowerSwitchDevice', 'DimmerDevice', 'MultiSensorDevice'):
                  <div class="col-md-4" id="device_id_{{device.device_id}}">
                    <h2>{{device.name}} <span class="location">{{device.location}}</span></h2>
                    % if device.type == 'BinarySensorDevice':
                    <div class="form-group">
                      <label for="binary-sensor">Sensor State</label>
                      <select name="{{device.device_id}}-state" class="form-control">
                        <option value="255" {{"selected" if device.state > 0 else ""}}>On</option>
                        <option value="0" {{"selected" if device.state == 0 else ""}}>Off</option>
                      </select>
                    </div>
                    % elif device.type == 'MultiSensorDevice':
                    <div class="form-group">
                      <label for="binary-sensor">Sensor State</label>
                      <select name="{{device.device_id}}-state" class="form-control">
                        <option value="255" {{"selected" if device.state > 0 else ""}}>On</option>
                        <option value="0" {{"selected" if device.state == 0 else ""}}>Off</option>
                      </select>
                    </div>
                    <div class="form-group">
                      <label for="lux">Lux:</label>
                      <input name="{{device.device_id}}-lux" value="{{device.lux}}" class="form-control">
                    </div>
                    <div class="form-group">
                      <label for="temperature">Temperature:</label>
                      <input name="{{device.device_id}}-temperature" value="{{device.temperature}}" class="form-control">
                    </div>
                    % elif device.type == 'BinaryPowerSwitchDevice':
                    <div class="form-group">
                      <label for="binary-switch">Switch State</label>
                      <select name="{{device.device_id}}-state" class="form-control {{"updated" if device_updated[device.device_id] else ""}}" readonly>
                        <option value="255" {{"selected" if prediction[device.device_id] > 0 else ""}}>On</option>
                        <option value="0" {{"selected" if prediction[device.device_id] == 0 else ""}}>Off</option>
                      </select>
                    </div>
                    <div class="form-group">
                      <label for="power_state">Power State (Watts):</label>
                      <input name="{{device.device_id}}-power_state" value="{{device.power_state}}" class="form-control">
                    </div>
                    % elif device.type == 'DimmerDevice':
                    <div class="form-group">
                      <label for="state">Dimmer State:</label>
                      <input name="{{device.device_id}}-state" value="{{prediction[device.device_id]}}" class="form-control {{"updated" if device_updated[device.device_id] else ""}}" readonly="readonly">
                    </div>
                    % else:
                    <span>No controls</span>
                    % end
                  </div>
              % end
            % end
          </div>
          <hr>
        </div> <!-- /container -->
      </form>
    </main>

    <footer class="container">
      <p>&copy; PracticalAI.io 2017</p>
    </footer>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="/static/js/bootstrap.min.js"></script>
  </body>
</html>
