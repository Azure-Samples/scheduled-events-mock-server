# Scheduled Events Mock Server

A Flask-based web application for simulating Azure Scheduled Events and IMDS (Instance Metadata Service) event flows. This tool is designed for testing and development scenarios where you want to emulate Azure platform events, such as Live Migration, User Reboot, Maintenance, and more.

## Features

- Select from multiple predefined scenarios (Live Migration, User Reboot, Redeploy, etc.)
- Manually generate events for each scenario state (Scheduled, Started, Completed, etc.)
- Automatically run a scenario through all its states with realistic timing
- Set custom resources for each event (default: `vmss_vm1`)
- Endpoint simulates the IMDS endpoint `/metadata/scheduledevents` and can be called from  within our outside of the test  VM  
- Supports simulating event approvals  via IMDS POST 

## Getting Started

### Prerequisites

- Python 3.8+
- `pip` (Python package manager)

### Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/your-org/ScheduledEventsResponder.git
    cd ScheduledEventsResponder
    ```

2. Install dependencies:
    ```sh
    python -m venv .venv    
    .\.venv\Bin\Activate.ps1 #On PowerShell
    pip install -r requirements.txt
    ```

3. Run the application:
    ```sh
    python main.py
    ```

4. Open your browser and navigate to [http://localhost](http://localhost)

## Usage

### Selecting and Running Scenarios

1. **Select a Scenario**
    - Use the dropdown at the top of the page to select a scenario (e.g., Live Migration, User Reboot).
    - Click **Set Scenario** to activate it.

2. **Set Resources (Optional)**
    - Under "Run Scenario", enter a comma-separated list of resource names in the **Resources** field.
    - Default is `vmss_vm1`.

3. **Generate Events Manually**
    - Select an event status from the dropdown (e.g., Scheduled, Started).
    - Click **Generate Event** to create an event in that state.

4. **Automatically Run Scenario**
    - Click **Automatically Run Scenario** to progress through all states with realistic timing.
    - A countdown timer will appear showing time until the next event state.

5. **Stop Playback**
    - Click **Stop Playback** to halt automatic progression.

6. **View Last Event**
    - The "Last Event" section displays the most recent event in IMDS format.

### IMDS Endpoint

- The app exposes `/metadata/scheduledevents` for both GET and POST.
- **GET** returns the current event(s) in IMDS format.
- **POST** with a JSON body containing `StartRequests` and a matching `EventId` will immediately advance the event to the next state (simulating event approval).

    Example:
    ```sh
    curl -H "Metadata:true" -X POST -d '{"StartRequests": [{"EventId": "YOUR_EVENT_ID"}]}' http://localhost:80/metadata/scheduledevents?api-version=2020-07-01
    ```

- For more information on Azure Scheduled Events and the IMDS API, see the [Azure Scheduled Events documentation](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/scheduled-events).

## Scenarios
There are two types of scenarios available to automatically run. The base types have their timings based on median values  from a sample of scheduled events sent to Azure customer in July 2025. These timing can be used to understand how your application would respond to a real event. 

The "Dev Timing" scenarios have all the timing reduced by a factor of 60 to make it easier for development and inner loop testing. For example, instead of a 15 minute warning period before the live migration, the scenario will only give 15 seconds. This shouldn't used as a guideline for how Azure will work, but rather as a way to make your development easier.


## Customization

- A few common scenarios are defined in `main.py` in the `scenarios` dictionary.
- You can add or modify scenarios as needed. 

## CLI Tool: `mockcli`

In addition to the browser UI, this project now supports a CLI utility (`mockcli`) to simulate scheduled events via command line — useful for automation or testing in headless environments.

### Features
- Supports triggering all predefined scenarios
- Generates Scheduled → Started → Completed events in order
- Looping and delay support for continuous testing

### 📦 Usage

```bash
python tools/mockcli.py --scenario "Live Migration"
python tools/mockcli.py --all
python tools/mockcli.py --loop --interval 30


## Trademarks 

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft’s Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party’s policies.
