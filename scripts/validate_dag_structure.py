#!/usr/bin/env python3
"""
Script de validación de estructura de DAGs sin dependencias de Airflow.
Verifica que los DAGs tengan la estructura correcta esperada.
"""
import re
from pathlib import Path

def validate_dag_structure(dag_file):
    """Valida la estructura de un archivo DAG."""
    print(f"\n{'='*60}")
    print(f"Validando estructura: {dag_file.name}")
    print('='*60)
    
    with open(dag_file, 'r') as f:
        content = f.read()
    
    checks = {
        'imports': False,
        'config_import': False,
        'dag_definition': False,
        'dag_id': False,
        'schedule': False,
        'default_args': False,
        'tasks': False,
    }
    
    # Verificar imports necesarios
    if re.search(r'from airflow import DAG', content):
        checks['imports'] = True
        print("✅ Imports de Airflow presentes")
    
    if re.search(r'from config import', content):
        checks['config_import'] = True
        print("✅ Import de config presente")
    
    # Verificar definición de DAG
    if re.search(r'with DAG\(', content):
        checks['dag_definition'] = True
        print("✅ Definición de DAG con context manager")
    
    # Verificar dag_id
    if re.search(r'dag_id\s*=\s*["\'][\w_]+["\']', content):
        dag_id_match = re.search(r'dag_id\s*=\s*["\']([^"\']+)["\']', content)
        if dag_id_match:
            checks['dag_id'] = True
            print(f"✅ dag_id definido: {dag_id_match.group(1)}")
    
    # Verificar schedule_interval
    if re.search(r'schedule_interval\s*=', content):
        checks['schedule'] = True
        print("✅ schedule_interval definido")
    
    # Verificar default_args
    if re.search(r'default_args\s*=|DEFAULT_DAG_ARGS', content):
        checks['default_args'] = True
        print("✅ default_args configurado")
    
    # Verificar que hay tareas definidas
    task_patterns = [
        r'KedroOperator\(',
        r'EmptyOperator\(',
        r'PythonOperator\(',
        r'BashOperator\(',
    ]
    for pattern in task_patterns:
        if re.search(pattern, content):
            checks['tasks'] = True
            print("✅ Tareas/operadores definidos")
            break
    
    # Calcular score
    passed = sum(checks.values())
    total = len(checks)
    score = (passed / total) * 100
    
    print(f"\n📊 Score: {passed}/{total} ({score:.1f}%)")
    
    if score == 100:
        print("🎉 ¡Estructura perfecta!")
        return True
    elif score >= 80:
        print("✅ Estructura buena")
        return True
    else:
        print("⚠️  Estructura necesita mejoras")
        return False

def main():
    """Función principal."""
    print("\n" + "="*60)
    print("🔍 VALIDACIÓN DE ESTRUCTURA DE DAGs")
    print("="*60)
    
    dags_dir = Path(__file__).parent.parent / "dags"
    dag_files = [
        f for f in dags_dir.glob("*.py") 
        if f.name not in ['__init__.py', 'config.py'] 
        and not f.name.endswith('.backup')
    ]
    
    results = []
    for dag_file in dag_files:
        is_valid = validate_dag_structure(dag_file)
        results.append((dag_file.name, is_valid))
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL")
    print("="*60)
    
    total = len(results)
    valid = sum(1 for _, is_valid in results if is_valid)
    
    print(f"\nTotal de DAGs: {total}")
    print(f"✅ Válidos: {valid}")
    print(f"⚠️  Con advertencias: {total - valid}")
    
    print("\n" + "="*60)
    if valid == total:
        print("🎉 ¡TODOS LOS DAGs TIENEN ESTRUCTURA VÁLIDA!")
    else:
        print("✅ Validación completada con algunas advertencias")
    print("="*60 + "\n")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())

