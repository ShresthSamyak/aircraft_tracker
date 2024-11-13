import numpy as np
from dataclasses import dataclass
from typing import Tuple, List
import math
import folium
from folium import plugins
import matplotlib.pyplot as plt

@dataclass
class Position:
    latitude: float
    longitude: float
    altitude: float

@dataclass
class WeatherData:
    wind_speed: float
    wind_direction: float
    visibility: float
    precipitation: float

@dataclass
class SearchResources:
    helicopters: int
    ground_teams: int
    drones: int
    estimated_time: float  # hours

class AircraftTracker:
    def __init__(self):
        self.last_known_position = None  # Position object
        self.last_known_speed = None     # (ground_speed, vertical_speed)
        self.last_known_heading = None   # degrees
        self.weather_data = None         # WeatherData object
        self.fuel_status = None          # fuel in kg
        self.fuel_consumption_rate = 0.8  # kg per minute (example value)

    def calculate_search_area(self) -> Tuple[Position, float]:
        """
        Calculates probable crash site and search radius based on aircraft parameters
        Returns: (center_position, radius_km)
        """
        if not all([self.last_known_position, self.last_known_speed, 
                   self.last_known_heading, self.weather_data]):
            raise ValueError("Missing required tracking data")

        # Calculate maximum range based on remaining fuel
        max_range_km = self.calculate_max_range()

        # Account for wind drift
        wind_drift = self.calculate_wind_drift()

        # Calculate probable center point
        center_lat = self.last_known_position.latitude + \
            (wind_drift[0] / 111.32)  # 1 degree = 111.32 km
        center_lon = self.last_known_position.longitude + \
            (wind_drift[1] / (111.32 * math.cos(math.radians(self.last_known_position.latitude))))

        # Add uncertainty radius (20% of max range)
        search_radius = max_range_km * 0.2

        return (Position(center_lat, center_lon, 0), search_radius)

    def generate_search_grid(self, center: Position, radius: float) -> np.ndarray:
        """
        Creates a grid of search cells with probability weights
        Returns: 2D numpy array of probability values
        """
        # Create a grid with 1km resolution
        grid_size = int(radius * 2)
        grid = np.zeros((grid_size, grid_size))

        # Generate probability distribution (gaussian)
        x = np.linspace(-radius, radius, grid_size)
        y = np.linspace(-radius, radius, grid_size)
        X, Y = np.meshgrid(x, y)
        
        # Bivariate normal distribution
        sigma = radius / 3  # 3-sigma rule
        grid = np.exp(-(X**2 + Y**2) / (2 * sigma**2))
        
        # Normalize probabilities
        grid = grid / np.sum(grid)
        
        return grid

    def optimize_search_pattern(self, grid: np.ndarray) -> List[Tuple[float, float]]:
        """
        Generates optimal search waypoints using spiral pattern
        Returns: List of (lat, lon) coordinates
        """
        rows, cols = grid.shape
        center = (rows // 2, cols // 2)
        
        # Spiral search pattern
        waypoints = []
        x, y = center
        dx, dy = 0, -1
        steps = max(rows, cols) ** 2
        
        for _ in range(steps):
            if (-rows//2 <= x <= rows//2) and (-cols//2 <= y <= cols//2):
                waypoints.append((x, y))
            
            if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
                dx, dy = -dy, dx
            
            x, y = x + dx, y + dy
            
        return self.convert_grid_to_coordinates(waypoints, center)

    def calculate_max_range(self) -> float:
        """Helper method to calculate maximum range based on fuel"""
        if not self.fuel_status:
            return 100  # Default 100km range if fuel status unknown
        
        flight_time_remaining = self.fuel_status / self.fuel_consumption_rate
        ground_speed = self.last_known_speed[0]  # km/h
        return (ground_speed * flight_time_remaining) / 60  # km

    def calculate_wind_drift(self) -> Tuple[float, float]:
        """Calculate wind drift vector in kilometers"""
        wind_speed_kmh = self.weather_data.wind_speed * 1.852  # convert knots to km/h
        wind_rad = math.radians(self.weather_data.wind_direction)
        
        # Decompose wind vector
        wind_x = wind_speed_kmh * math.sin(wind_rad)
        wind_y = wind_speed_kmh * math.cos(wind_rad)
        
        return (wind_x, wind_y)

    def convert_grid_to_coordinates(self, waypoints: List[Tuple[int, int]], 
                                  center: Tuple[int, int]) -> List[Tuple[float, float]]:
        """Convert grid positions to geographic coordinates"""
        geo_waypoints = []
        for wx, wy in waypoints:
            # Convert grid offsets to kilometers
            dx = (wx - center[0])
            dy = (wy - center[1])
            
            # Convert to lat/lon
            lat = self.last_known_position.latitude + (dy / 111.32)
            lon = self.last_known_position.longitude + \
                (dx / (111.32 * math.cos(math.radians(self.last_known_position.latitude))))
            
            geo_waypoints.append((lat, lon))
            
        return geo_waypoints

    def visualize_search_area(self, center_position: Position, radius: float) -> folium.Map:
        """Creates an interactive map showing the search area"""
        # Create map centered on the probable crash site
        m = folium.Map(
            location=[center_position.latitude, center_position.longitude],
            zoom_start=10
        )
        
        # Add circle for search radius
        folium.Circle(
            radius=radius * 1000,  # Convert km to meters
            location=[center_position.latitude, center_position.longitude],
            color="red",
            fill=True,
            popup=f"Search Radius: {radius:.2f}km"
        ).add_to(m)
        
        # Add last known position marker
        folium.Marker(
            [self.last_known_position.latitude, self.last_known_position.longitude],
            popup="Last Known Position",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

        # Add flight path line
        folium.PolyLine(
            locations=[
                [self.last_known_position.latitude, self.last_known_position.longitude],
                [center_position.latitude, center_position.longitude]
            ],
            color="yellow",
            weight=2,
            opacity=0.8
        ).add_to(m)
        
        return m

    def assess_weather_risk(self) -> str:
        """Assess search conditions based on weather"""
        risk_level = "LOW"
        reasons = []
        
        if self.weather_data.wind_speed > 25:
            risk_level = "HIGH"
            reasons.append("High winds")
            
        if self.weather_data.visibility < 5:
            risk_level = "HIGH"
            reasons.append("Poor visibility")
            
        if self.weather_data.precipitation > 5:
            risk_level = "MEDIUM"
            reasons.append("Significant precipitation")
            
        if not reasons:
            reasons.append("Good weather conditions")
            
        return f"Search Risk Level: {risk_level}\nFactors: {', '.join(reasons)}"

    def calculate_required_resources(self, search_radius: float) -> SearchResources:
        """Calculate required search resources based on area"""
        area = math.pi * (search_radius ** 2)  # km²
        
        # Resource calculation based on area
        helicopters = max(1, int(area / 100))  # 1 helicopter per 100 km²
        ground_teams = max(2, int(area / 50))  # 1 team per 50 km²
        drones = max(2, int(area / 25))        # 1 drone per 25 km²
        
        # Estimate search time
        coverage_rate = (helicopters * 30 + ground_teams * 5 + drones * 15)  # km²/hour
        estimated_time = area / coverage_rate
        
        return SearchResources(helicopters, ground_teams, drones, estimated_time)

    def plot_probability_heatmap(self, center: Position, radius: float) -> None:
        """Generate and display a heatmap of search probabilities"""
        grid = self.generate_search_grid(center, radius)
        
        plt.figure(figsize=(10, 8))
        plt.imshow(grid, cmap='hot', interpolation='nearest')
        plt.colorbar(label='Search Probability')
        plt.title('Search Area Probability Heatmap')
        plt.xlabel('Distance (km)')
        plt.ylabel('Distance (km)')
        plt.savefig('search_heatmap.png')
        plt.close()

    def get_search_summary(self) -> dict:
        """Generate a comprehensive search summary"""
        return {
            'last_known_position': {
                'latitude': self.last_known_position.latitude,
                'longitude': self.last_known_position.longitude,
                'altitude': self.last_known_position.altitude
            },
            'speed': {
                'ground_speed': self.last_known_speed[0],
                'vertical_speed': self.last_known_speed[1]
            },
            'heading': self.last_known_heading,
            'weather': {
                'wind_speed': self.weather_data.wind_speed,
                'wind_direction': self.weather_data.wind_direction,
                'visibility': self.weather_data.visibility,
                'precipitation': self.weather_data.precipitation
            },
            'fuel_status': self.fuel_status
        }