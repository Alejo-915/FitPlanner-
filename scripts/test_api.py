import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_endpoints():
    print("🧪 Pruebas de API FitPlanner\n")

    # Test 1: Verificar usuario
    print("1️⃣ Probando GET /usuarios/1")
    try:
        response = requests.get(f"{BASE_URL}/usuarios/1")
        print(f"   Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"   ✅ Usuario: {data.get('nombre', 'N/A')}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Excepción: {e}")

    print()

    # Test 2: Obtener rutinas
    print("2️⃣ Probando GET /rutinas/")
    try:
        response = requests.get(f"{BASE_URL}/rutinas/")
        print(f"   Status: {response.status_code}")
        if response.ok:
            data = response.json()
            rutinas = data.get('rutinas', [])
            print(f"   ✅ Rutinas disponibles: {len(rutinas)}")
            if rutinas:
                print(f"   Primera rutina: {rutinas[0].get('nombre_rutina', 'N/A')}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Excepción: {e}")

    print()

    # Test 3: Verificar sesión activa
    print("3️⃣ Probando GET /sesiones/usuario/1/activa")
    try:
        response = requests.get(f"{BASE_URL}/sesiones/usuario/1/activa")
        print(f"   Status: {response.status_code}")
        if response.ok:
            data = response.json()
            if data.get('sesion_id'):
                print(f"   ✅ Sesión activa encontrada: ID {data['sesion_id']}")
                print(f"   Ejercicios: {len(data.get('ejercicios', []))}")
            else:
                print(f"   ℹ️  No hay sesión activa")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Excepción: {e}")

    print()

    # Test 4: Iniciar sesión (solo si hay rutinas)
    print("4️⃣ Probando POST /sesiones/iniciar")
    try:
        # Primero obtenemos una rutina
        rutinas_response = requests.get(f"{BASE_URL}/rutinas/")
        if rutinas_response.ok:
            rutinas = rutinas_response.json().get('rutinas', [])
            if rutinas:
                rutina_id = rutinas[0]['id']

                payload = {
                    "usuario_id": 1,
                    "rutina_id": rutina_id
                }

                print(f"   Payload: {json.dumps(payload)}")

                response = requests.post(
                    f"{BASE_URL}/sesiones/iniciar",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )

                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")

                if response.ok:
                    data = response.json()
                    print(f"   ✅ {data.get('mensaje', 'OK')}")
                else:
                    print(f"   ❌ Error al iniciar sesión")
            else:
                print(f"   ⚠️  No hay rutinas disponibles para probar")
        else:
            print(f"   ⚠️  No se pudieron obtener rutinas")
    except Exception as e:
        print(f"   ❌ Excepción: {e}")


if __name__ == "__main__":
    test_endpoints()