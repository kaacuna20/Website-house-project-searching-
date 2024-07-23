from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db
from app.models import Project
import folium
from folium.plugins import MarkerCluster


maps_bp = Blueprint('maps', __name__)

@maps_bp.route('/maps', methods=["GET"])
def maps_projects():
    # Obtener los proyectos de la base de datos
    projects = db.session.execute(db.select(Project.name, Project.latitude, Project.longitude, Project.city, Project.slug)).fetchall()
    
    # Crear un mapa base
    map_center = [10.9584569, -74.8338985]  # Coordenadas del centro del mapa
    m = folium.Map(location=map_center, zoom_start=12)
    
    # Agregar un marcador cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Definir colores para las ciudades
    colors = {
        'barranquilla': 'blue',
        'puerto colombia': 'green',
        'soledad': 'red'
    }
    
    for project in projects:
        city = project.city.lower()
        color = colors.get(city, 'gray')  # Color por defecto si la ciudad no está en el diccionario
        popup_html = f"""
        <div>
            <h4>{project.name.title()}</h4>
            <h4>{project.city}</h4>
            <a href="/{project.slug}">Ver Proyecto</a>
        </div>
        """
        folium.Marker(
            location=[project.latitude, project.longitude],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=color)
        ).add_to(marker_cluster)
    
    # Guardar el mapa en un archivo HTML en la carpeta templates
    map_html_path = 'app/templates/projects_map.html'
    m.save(map_html_path)
    
    # Renderizar el archivo HTML guardado
    return render_template('projects_map.html')


@maps_bp.route('/ubication/<slug>', methods=["GET"])
def ubication_projects(slug):
    
    project = db.session.execute(db.select(Project).where(Project.slug == slug)).scalar()
    
    # Crear un mapa base
    map_center = [project.latitude, project.longitude]  # Coordenadas del centro del mapa
    m = folium.Map(location=map_center, zoom_start=15)
    
    # Agregar un marcador cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Color por defecto si la ciudad no está en el diccionario
    popup_html = f"""
    <div>
        <h4>{project.name.title()}</h4>
        <h4>{project.city}</h4>
        <h4>{project.location}</h4>
        <h4>{project.address}</h4>
        <a href="/{project.slug}">Ver Proyecto</a>
    </div>
    """
    folium.Marker(
        location=[project.latitude, project.longitude],
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color="gray")
    ).add_to(marker_cluster)
    
    # Guardar el mapa en un archivo HTML en la carpeta templates
    map_html_path = 'app/templates/project_ubication.html'
    m.save(map_html_path)
    
    return render_template("project_ubication.html")
    