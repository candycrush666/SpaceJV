from folium import Map, Marker, Circle, Popup

# Crear un mapa
mymap = Map(location=[37.7749, -122.4194], zoom_start=10)

# Agregar marcador
marker = Marker(location=[37.7749, -122.4194], tooltip='San Francisco')
mymap.add_child(marker)

# Agregar círculo con popup
popup = Popup("Popup text", parse_html=True)
circle = Circle(location=[37.7749, -122.4194], radius=10000, color='blue', fill=True).add_child(popup)
mymap.add_child(circle)

# Guardar el mapa como un archivo HTML
mymap.save("map.html")
