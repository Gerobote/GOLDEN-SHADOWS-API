Golden Shadows API

REST API para la empresa Luna Lunera y Asociado S.A., desarrollada en FastAPI + MongoDB.

    Descripción

En la opulenta ciudad de Las Cariñosas, una ola de asesinatos ha sacudido a la élite.
La API permite gestionar y consultar las entidades principales del caso:

Victim → Personas asesinadas.

Family → Familias a las que pertenecen las víctimas.

MurderMethod → Método utilizado en el asesinato.

Case → Casos de investigación asociados.

Detective → Policías encargados de resolver los casos.

RelatedCase → Casos vinculados o relacionados.

MediaReport (opcional) → Reportes de prensa asociados a un caso.

    Requisitos cumplidos

Framework: FastAPI (Python)

Base de datos: MongoDB (Atlas o local)

CRUD completo con operaciones:

Victim → GET (uno/todos), POST, PATCH, DELETE

Case → GET (uno/todos), POST, PATCH, DELETE

Entidades adicionales implementadas: Family, MurderMethod, Detective, RelatedCase, MediaReport.

Diagramas incluidos: Entidad-Relación y Clases.

    Estructura del proyecto
golden-shadows-api/
├─ .env                  # Variables de entorno (Mongo URI, DB)
├─ main.py               # Entry point FastAPI
├─ app/
│  ├─ db.py              # Conexión MongoDB
│  ├─ utils.py           # Helpers (ObjectId, serialización)
│  ├─ schemas.py         # Modelos Pydantic
│  └─ routers/           # Rutas por entidad
│     ├─ victims.py
│     ├─ cases.py
│     ├─ families.py
│     ├─ murder_methods.py
│     ├─ detectives.py
│     ├─ related_cases.py
│     └─ media_reports.py (opcional)
└─ README.md

    Instalación y ejecución
1. Clonar repositorio
git clone <url-del-repo>
cd golden-shadows-api

2. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

3. Instalar dependencias
pip install fastapi "uvicorn[standard]" motor pydantic python-dotenv

4. Configurar variables de entorno

Crear archivo .env en la raíz:

MONGODB_URI="mongodb+srv://USER:PASS@CLUSTER/golden_shadows?retryWrites=true&w=majority"
MONGODB_DB="golden_shadows"

5. Ejecutar servidor
uvicorn main:app --reload


Servidor en:

Swagger: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

🔗 Endpoints principales
Victims

GET /victims/ → listar todas

GET /victims/{id} → obtener una

POST /victims/ → crear nueva

PATCH /victims/{id} → actualizar parcialmente

DELETE /victims/{id} → eliminar

Cases

GET /cases/

GET /cases/{id}

POST /cases/

PATCH /cases/{id}

DELETE /cases/{id}

Families

GET /families/

POST /families/

PATCH /families/{id}

DELETE /families/{id}

Murder Methods

GET /murder-methods/

POST /murder-methods/

PATCH /murder-methods/{id}

DELETE /murder-methods/{id}

Detectives

GET /detectives/

POST /detectives/

PATCH /detectives/{id}

DELETE /detectives/{id}

Related Cases

GET /related-cases/

POST /related-cases/

PATCH /related-cases/{id}

DELETE /related-cases/{id}

Media Reports (opcional)

GET /media-reports/

POST /media-reports/

PATCH /media-reports/{id}

DELETE /media-reports/{id}

🧪 Ejemplos cURL

Crear familia:

curl -X POST "http://127.0.0.1:8000/families/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Calle","motto":"Riqueza y secretos"}'


Crear víctima:

curl -X POST "http://127.0.0.1:8000/victims/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Mariana Calle","age":32,"family_id":null,"murder_method_id":null,"case_ids":[]}'


Listar víctimas:

curl "http://127.0.0.1:8000/victims/"

    Diagramas
Diagrama ER
erDiagram
  FAMILY { string _id string name string motto }
  MURDERMETHOD { string _id string name string description }
  DETECTIVE { string _id string name string rank string studies boolean rumored_to_be_killer }
  CASE { string _id string title string description datetime opened_at }
  VICTIM { string _id string name int age string family_id string murder_method_id }
  MEDIAREPORT { string _id string case_id string title string url datetime published_at }
  RELATEDCASE { string _id string case_id string related_to_case_id string relation }

  FAMILY ||--o{ VICTIM : has
  MURDERMETHOD ||--o{ VICTIM : used_for
  CASE ||--o{ VICTIM : includes
  CASE }o--o{ DETECTIVE : handled_by
  CASE }o--o{ CASE : related (via RELATEDCASE)
  CASE ||--o{ MEDIAREPORT : covered_by

Diagrama de clases
classDiagram
  class Victim { +id: str +name: str +age: int +family_id: str? +murder_method_id: str? +case_ids: list~str~ }
  class Case { +id: str +title: str +description: str? +opened_at: datetime +detective_ids: list~str~ +victim_ids: list~str~ +related_case_ids: list~str~ }
  class Family { +id: str +name: str +motto: str? }
  class MurderMethod { +id: str +name: str +description: str? }
  class Detective { +id: str +name: str +rank: str? +studies: str? +rumored_to_be_killer: bool }
  class RelatedCase { +id: str +case_id: str +related_to_case_id: str +relation: str? }
  class MediaReport { +id: str +case_id: str +title: str +url: str? +published_at: datetime }

  Victim --> "0..1" Family
  Victim --> "0..1" MurderMethod
  Case --> "0..*" Victim
  Case --> "0..*" Detective
  Case --> "0..*" RelatedCase
  Case --> "0..*" MediaReport# GOLDEN-SHADOWS-API
