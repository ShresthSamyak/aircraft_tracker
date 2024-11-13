from aircraft_tracker import AircraftTracker, Position, WeatherData, SearchResources
import webbrowser
import os

def get_aircraft_data():
    """Get aircraft data from user input"""
    print("\n=== Aircraft Search and Rescue System ===\n")
    
    # 1. Get Position Data
    print("Enter Last Known Position:")
    try:
        latitude = float(input("Latitude (decimal degrees, -90 to 90): "))
        longitude = float(input("Longitude (decimal degrees, -180 to 180): "))
        altitude = float(input("Altitude (feet): "))
    except ValueError:
        raise ValueError("Position values must be numbers")

    # 2. Get Speed Data
    print("\nEnter Speed Information:")
    try:
        ground_speed = float(input("Ground Speed (km/h): "))
        vertical_speed = float(input("Vertical Speed (feet/min): "))
    except ValueError:
        raise ValueError("Speed values must be numbers")

    # 3. Get Heading
    try:
        heading = float(input("\nEnter Last Known Heading (0-360 degrees): "))
    except ValueError:
        raise ValueError("Heading must be a number")

    # 4. Get Weather Data
    print("\nEnter Weather Information:")
    try:
        wind_speed = float(input("Wind Speed (knots): "))
        wind_direction = float(input("Wind Direction (0-360 degrees): "))
        visibility = float(input("Visibility (kilometers): "))
        precipitation = float(input("Precipitation (mm/hr): "))
    except ValueError:
        raise ValueError("Weather values must be numbers")

    # 5. Get Fuel Data
    try:
        fuel = float(input("\nEnter Remaining Fuel (kg): "))
    except ValueError:
        raise ValueError("Fuel must be a number")

    return {
        'position': Position(latitude, longitude, altitude),
        'speed': (ground_speed, vertical_speed),
        'heading': heading,
        'weather': WeatherData(wind_speed, wind_direction, visibility, precipitation),
        'fuel': fuel
    }

def main():
    try:
        # Get data from user
        data = get_aircraft_data()
        
        # Initialize tracker
        tracker = AircraftTracker()
        
        # Set the data
        tracker.last_known_position = data['position']
        tracker.last_known_speed = data['speed']
        tracker.last_known_heading = data['heading']
        tracker.weather_data = data['weather']
        tracker.fuel_status = data['fuel']
        
        # Calculate search area
        center_position, search_radius = tracker.calculate_search_area()
        
        # Generate visualization
        search_map = tracker.visualize_search_area(center_position, search_radius)
        map_file = "search_area_map.html"
        search_map.save(map_file)
        
        # Generate probability heatmap
        tracker.plot_probability_heatmap(center_position, search_radius)
        
        # Generate search pattern
        grid = tracker.generate_search_grid(center_position, search_radius)
        waypoints = tracker.optimize_search_pattern(grid)
        
        # Assess weather conditions
        weather_assessment = tracker.assess_weather_risk()
        
        # Calculate required resources
        resources = tracker.calculate_required_resources(search_radius)
        
        # Get search summary
        summary = tracker.get_search_summary()
        
        # Display comprehensive results
        print("\n=== Search Results ===")
        print(f"Search Center Position:")
        print(f"  Latitude:  {center_position.latitude:.4f}°")
        print(f"  Longitude: {center_position.longitude:.4f}°")
        print(f"Search Radius: {search_radius:.2f} km")
        
        print(f"\n{weather_assessment}")
        
        print("\nRequired Resources:")
        print(f"  Helicopters: {resources.helicopters}")
        print(f"  Ground Teams: {resources.ground_teams}")
        print(f"  Drones: {resources.drones}")
        print(f"  Estimated Search Time: {resources.estimated_time:.1f} hours")
        
        print("\nSearch Pattern Generated:")
        print(f"  Number of Waypoints: {len(waypoints)}")
        
        print("\nVisualization Files Generated:")
        print(f"  Map: {map_file}")
        print(f"  Heatmap: search_heatmap.png")
        
        # Open the map in default web browser
        webbrowser.open('file://' + os.path.realpath(map_file))
        
    except ValueError as e:
        print(f"\nError: {e}")
        return
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return

if __name__ == "__main__":
    main()
    