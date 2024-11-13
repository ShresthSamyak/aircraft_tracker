# Aircraft Search and Rescue System

## Overview
A sophisticated Python-based system designed to assist search and rescue operations for missing aircraft. The system calculates probable search areas, generates optimized search patterns, and provides resource allocation recommendations based on various flight and environmental parameters.

## Features
- Calculate probable crash sites based on last known position and environmental factors
- Generate probability-based search grids and optimal search patterns
- Visualize search areas with interactive maps and heatmaps
- Assess weather risks and search conditions
- Calculate required search resources and estimated search times
- Provide comprehensive search operation summaries

## Requirements
- Python 3.7+
- Required packages:
  ```bash
  numpy
  folium
  matplotlib
  dataclasses
  ```

## Installation
1. Clone the repository:

2. Install required packages:

## Usage
Run the main program:

The system will prompt for the following input data:
- Last known position (latitude, longitude, altitude)
- Speed information (ground speed, vertical speed)
- Heading
- Weather conditions (wind speed, direction, visibility, precipitation)
- Remaining fuel

## Output
The system generates several outputs:
1. Interactive HTML map (`search_area_map.html`)
2. Probability heatmap (`search_heatmap.png`)
3. Detailed search recommendations including:
   - Search area center and radius
   - Weather risk assessment
   - Required resources (helicopters, ground teams, drones)
   - Estimated search time
   - Optimized search pattern waypoints

## Core Components

### Position Class
Stores geographic coordinates and altitude information.

### WeatherData Class
Manages weather-related parameters affecting the search operation.

### SearchResources Class
Defines required search and rescue resources.

### AircraftTracker Class
Main class handling all search calculations and visualizations:
- Search area calculation
- Wind drift compensation
- Search pattern optimization
- Resource allocation
- Visualization generation

## Calculations
The system incorporates various factors in its calculations:
- Maximum range based on remaining fuel
- Wind drift effects
- Search probability distribution
- Resource requirements based on area size
- Weather risk assessment

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Search pattern algorithms based on standard SAR protocols
- Weather risk assessments aligned with aviation safety standards
- Resource calculations based on typical SAR operation requirements

## Contact
For questions and support, please open an issue in the GitHub repository.

## Disclaimer
This system is designed as a support tool for search and rescue operations and should not be used as the sole decision-making source in actual emergency situations.

## Quick Start Guide

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/aircraft-search-rescue.git
cd aircraft-search-rescue
```

2. **Install required packages**
```bash
pip install numpy folium matplotlib
```

3. **Run the program**
```bash
python main.py
```

4. **Input the required data when prompted:**
- Last Known Position:
  - Latitude (-90 to 90)
  - Longitude (-180 to 180)
  - Altitude (feet)
- Speed Information:
  - Ground Speed (km/h)
  - Vertical Speed (feet/min)
- Heading (0-360 degrees)
- Weather Information:
  - Wind Speed (knots)
  - Wind Direction (0-360 degrees)
  - Visibility (kilometers)
  - Precipitation (mm/hr)
- Remaining Fuel (kg)

5. **View Results**
- An interactive map will automatically open in your default web browser
- Check the terminal for detailed search recommendations
- Find generated files in your working directory:
  - `search_area_map.html`: Interactive search area map
  - `search_heatmap.png`: Probability distribution visualization
