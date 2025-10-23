#!/usr/bin/env python3
"""
Script de prueba para verificar que todos los DAGs se pueden importar correctamente.
Este script simula lo que Airflow hace al cargar DAGs.
"""
import sys
import os
from pathlib import Path

# Agregar el directorio de DAGs al path
dags_dir = Path(__file__).parent.parent / "dags"
sys.path.insert(0, str(dags_dir))

def test_dag_import(dag_file):
    """Intenta importar un archivo DAG y reporta cualquier error."""
    print(f"\n{'='*60}")
    print(f"Probando: {dag_file.name}")
    print('='*60)
    
    try:
        # Leer el contenido del archivo
        with open(dag_file, 'r') as f:
            code = f.read()
        
        # Intentar compilar el código
        compile(code, dag_file.name, 'exec')
        print(f"✅ ÉXITO: {dag_file.name} compila correctamente")
        
        # Intentar importar el módulo
        module_name = dag_file.stem
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        # Ejecutar el código en un namespace limpio
        namespace = {
            '__file__': str(dag_file),
            '__name__': module_name,
        }
        exec(code, namespace)
        
        # Verificar que se creó un DAG
        dags_found = []
        for name, obj in namespace.items():
            if hasattr(obj, 'dag_id'):
                dags_found.append(obj.dag_id)
        
        if dags_found:
            print(f"✅ DAG(s) encontrado(s): {', '.join(dags_found)}")
            return True, None
        else:
            print(f"⚠️  ADVERTENCIA: No se encontró ningún objeto DAG en {dag_file.name}")
            return True, "No DAG object found"
            
    except SyntaxError as e:
        error_msg = f"❌ ERROR DE SINTAXIS en {dag_file.name}:\n   {e}"
        print(error_msg)
        return False, str(e)
    except Exception as e:
        error_msg = f"❌ ERROR al importar {dag_file.name}:\n   {type(e).__name__}: {e}"
        print(error_msg)
        return False, str(e)

def main():
    """Función principal que prueba todos los DAGs."""
    print("\n" + "="*60)
    print("🚀 PRUEBA DE IMPORTACIÓN DE DAGs - Spaceflights")
    print("="*60)
    
    # Encontrar todos los archivos .py en el directorio dags
    dag_files = [
        f for f in dags_dir.glob("*.py") 
        if f.name not in ['__init__.py', 'config.py'] 
        and not f.name.endswith('.backup')
    ]
    
    if not dag_files:
        print("❌ No se encontraron archivos DAG para probar")
        return 1
    
    print(f"\n📋 Archivos DAG encontrados: {len(dag_files)}")
    for dag_file in dag_files:
        print(f"   - {dag_file.name}")
    
    # Probar cada DAG
    results = []
    for dag_file in dag_files:
        success, error = test_dag_import(dag_file)
        results.append((dag_file.name, success, error))
    
    # Resumen de resultados
    print("\n" + "="*60)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for _, success, _ in results if success)
    failed = total - passed
    
    print(f"\nTotal de DAGs probados: {total}")
    print(f"✅ Exitosos: {passed}")
    print(f"❌ Fallidos: {failed}")
    
    if failed > 0:
        print("\n⚠️  DAGs con problemas:")
        for name, success, error in results:
            if not success:
                print(f"   - {name}")
                if error:
                    print(f"     Error: {error[:100]}...")
    
    print("\n" + "="*60)
    if failed == 0:
        print("🎉 ¡TODOS LOS DAGs SE IMPORTARON CORRECTAMENTE!")
        print("="*60)
        return 0
    else:
        print("⚠️  Algunos DAGs tienen problemas. Revisa los errores arriba.")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())












