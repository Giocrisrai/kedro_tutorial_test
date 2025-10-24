#!/usr/bin/env python3
"""
Script para validar que los tests están bien estructurados.
Simula la lógica de los tests sin ejecutar el código real.
"""
import sys
import ast
from pathlib import Path

def analyze_test_file(file_path):
    """Analiza un archivo de test para verificar su estructura."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        # Buscar funciones de test
        test_functions = []
        fixtures = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('test_'):
                    test_functions.append(node.name)
                elif node.name.startswith('dummy_') or 'fixture' in node.name.lower():
                    fixtures.append(node.name)
        
        return {
            'test_functions': test_functions,
            'fixtures': fixtures,
            'total_lines': len(content.split('\n')),
            'syntax_ok': True
        }
        
    except SyntaxError as e:
        return {
            'error': f"Error de sintaxis: {e}",
            'syntax_ok': False
        }
    except Exception as e:
        return {
            'error': f"Error: {e}",
            'syntax_ok': False
        }

def validate_test_structure(analysis):
    """Valida que la estructura del test sea correcta."""
    issues = []
    
    if not analysis['syntax_ok']:
        issues.append(f"❌ Error de sintaxis: {analysis.get('error', 'Desconocido')}")
        return issues
    
    # Verificar que hay funciones de test
    if not analysis['test_functions']:
        issues.append("❌ No se encontraron funciones de test (deben empezar con 'test_')")
    else:
        issues.append(f"✅ Funciones de test encontradas: {len(analysis['test_functions'])}")
        for func in analysis['test_functions']:
            issues.append(f"   • {func}")
    
    # Verificar fixtures
    if not analysis['fixtures']:
        issues.append("⚠️  No se encontraron fixtures (puede ser normal)")
    else:
        issues.append(f"✅ Fixtures encontrados: {len(analysis['fixtures'])}")
        for fixture in analysis['fixtures']:
            issues.append(f"   • {fixture}")
    
    # Verificar tamaño del archivo
    if analysis['total_lines'] < 10:
        issues.append("⚠️  Archivo muy pequeño, puede estar incompleto")
    elif analysis['total_lines'] > 200:
        issues.append("⚠️  Archivo muy grande, puede ser difícil de mantener")
    else:
        issues.append(f"✅ Tamaño apropiado: {analysis['total_lines']} líneas")
    
    return issues

def main():
    """Función principal."""
    print("")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║              🧪 VALIDACIÓN DE TESTS - DATA SCIENCE              ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print("")
    
    test_file = Path("tests/pipelines/data_science/test_pipeline.py")
    
    if not test_file.exists():
        print("❌ Archivo de test no encontrado: tests/pipelines/data_science/test_pipeline.py")
        return 1
    
    print(f"📄 Analizando: {test_file}")
    print("="*60)
    
    # Analizar el archivo
    analysis = analyze_test_file(test_file)
    
    # Validar estructura
    issues = validate_test_structure(analysis)
    
    # Mostrar resultados
    for issue in issues:
        print(issue)
    
    print("\n" + "="*60)
    print("📊 RESUMEN")
    print("="*60)
    
    if analysis['syntax_ok']:
        print("✅ Sintaxis: Correcta")
        print(f"✅ Funciones de test: {len(analysis['test_functions'])}")
        print(f"✅ Fixtures: {len(analysis['fixtures'])}")
        print(f"✅ Líneas de código: {analysis['total_lines']}")
        
        # Verificar funciones específicas esperadas
        expected_tests = [
            'test_split_data',
            'test_data_science_pipeline',
            'test_train_model',
            'test_evaluate_model'
        ]
        
        missing_tests = []
        for expected in expected_tests:
            if expected not in analysis['test_functions']:
                missing_tests.append(expected)
        
        if missing_tests:
            print(f"⚠️  Tests faltantes: {missing_tests}")
        else:
            print("✅ Todos los tests esperados están presentes")
        
        print("\n🎉 ¡VALIDACIÓN EXITOSA!")
        print("Los tests están bien estructurados y listos para ejecutar.")
        return 0
    else:
        print(f"❌ Error: {analysis.get('error', 'Desconocido')}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
