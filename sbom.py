from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.output import Serializers
from cyclonedx.model import License

# Erstellen einer neuen BOM
bom = Bom()

# Füge die Bibliotheken als Komponenten hinzu
libraries = [
    {"name": "opencv-python", "version": "4.5.4", "type": ComponentType.LIBRARY},
    {"name": "scikit-image", "version": "0.18.3", "type": ComponentType.LIBRARY},
    {"name": "img2pdf", "version": "0.4.0", "type": ComponentType.LIBRARY}
]

for lib in libraries:
    component = Component(
        name=lib["name"],
        version=lib["version"],
        type=lib["type"],
        licenses=[License(name='MIT')]  # Beispiel für eine Lizenz
    )
    bom.add_component(component)

# Serialisierung der BOM in JSON-Format
bom_json = Serializers().serialize(bom, output_format='json')

# Speichern der BOM in einer Datei
with open('sbom.json', 'w') as f:
    f.write(bom_json)

print("SBOM erfolgreich erstellt und gespeichert!")
